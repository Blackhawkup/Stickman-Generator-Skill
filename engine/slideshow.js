/* Slideshow Engine: Deterministic, seek-driven, timed to narration.
   Supports centered presentation with matching background fill for 720x1600 (phone) and 1920x1080 (laptop). */
(function () {
  const FILM = window.FILM || {};
  const WORDS = window.WORDS || [];
  const SLIDES = window.SLIDES || [];
  const W = FILM.W || 720;
  const H = FILM.H || 1600;
  const FORMAT = FILM.format || '720:1600';
  const CANVAS_CFG = FILM.canvas || {};
  let CANVAS_BG = CANVAS_CFG.canvas_bg || (FILM.theme && FILM.theme.canvas_bg) || (FILM.theme && FILM.theme.background) || '#FBF6EF';
  if (CANVAS_BG === '#000000' || CANVAS_BG === '#000' || CANVAS_BG.toLowerCase() === 'black') {
    CANVAS_BG = '#FBF6EF';
  }
  
  const FADE_DUR = (FILM.transitions && FILM.transitions.fade_duration != null) ? FILM.transitions.fade_duration : 0.0;
  const KEN_BURNS = (FILM.transitions && FILM.transitions.ken_burns_zoom != null) ? FILM.transitions.ken_burns_zoom : 1.0;

  // Helper: Normalize word tokens
  const norm = (w) => (w || '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '');
  const NWORDS = WORDS.map((x) => Object.assign({ k: norm(x.w) }, x));

  // Word Clock Query: findPhraseTime(phrase) returns timestamp in seconds
  function findPhraseTime(phrase, occurrence = 1) {
    if (typeof phrase === 'number') return phrase;
    const tokens = (phrase || '').split(/\s+/).map(norm).filter(Boolean);
    if (!tokens.length) return 0;
    let matchCount = 0;
    for (let i = 0; i + tokens.length <= NWORDS.length; i++) {
      if (tokens.every((t, j) => NWORDS[i + j].k === t)) {
        matchCount++;
        if (matchCount === occurrence) {
          return NWORDS[i].s;
        }
      }
    }
    // Fallback: If exact multi-word phrase not found, match first token
    for (let i = 0; i < NWORDS.length; i++) {
      if (NWORDS[i].k === tokens[0]) return NWORDS[i].s;
    }
    console.warn(`[Slideshow] Trigger phrase not found in audio: "${phrase}"`);
    return null;
  }

  // Pre-calculate start and end times for each slide
  const timeline = [];
  let prevTime = 0.0;
  for (let i = 0; i < SLIDES.length; i++) {
    const s = SLIDES[i];
    let startTime = s.time != null ? s.time : findPhraseTime(s.trigger, s.occurrence || 1);
    if (startTime == null || startTime < prevTime) {
      startTime = prevTime;
    }
    timeline.push({
      index: i,
      name: s.name,
      src: s.src || `../images/${s.name}.png`,
      caption: s.bottom_caption || s.caption || '',
      title: s.top_title || s.title || '',
      start: startTime,
      transition: s.transition || FILM.transitions?.default_type || 'cut',
      durationOverride: s.duration_override || null
    });
    prevTime = startTime;
  }

  // Calculate slide end times
  for (let i = 0; i < timeline.length; i++) {
    timeline[i].end = (i + 1 < timeline.length) ? timeline[i + 1].start : (window.DUR || 30.0);
    timeline[i].totalDuration = timeline[i].end - timeline[i].start;
  }

  // Build DOM Elements
  const container = document.getElementById('slides-container');
  const slideElements = [];

  timeline.forEach((item, idx) => {
    const wrap = document.createElement('div');
    wrap.className = 'slide-wrapper';
    wrap.id = `slide_${idx}`;
    
    // Fill full frame with matching background color, centering content
    wrap.style.cssText = `
      position: absolute;
      inset: 0;
      width: ${W}px;
      height: ${H}px;
      opacity: 0;
      overflow: hidden;
      background: ${CANVAS_BG};
      display: flex;
      align-items: center;
      justify-content: center;
      will-change: transform, opacity;
    `;

    // Optional backdrop blur only if enabled
    let bgBlur = null;
    if (CANVAS_CFG.blur_backdrop) {
      bgBlur = document.createElement('div');
      bgBlur.className = 'slide-bg-blur';
      bgBlur.style.cssText = `
        position: absolute;
        inset: -5%;
        width: 110%;
        height: 110%;
        background-image: url('${item.src}');
        background-size: cover;
        background-position: center;
        filter: blur(35px) brightness(0.35);
        z-index: 1;
      `;
      wrap.appendChild(bgBlur);
    }

    // Foreground main image centered with object-fit: contain
    const img = document.createElement('img');
    img.className = 'slide-img';
    img.src = item.src;
    img.style.cssText = `
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: contain;
      object-position: center;
      z-index: 2;
      will-change: transform;
    `;

    wrap.appendChild(img);
    container.appendChild(wrap);
    slideElements.push({ wrap, img, bgBlur, item });
  });

  // Preload all slide images
  let loadedCount = 0;
  const totalImgs = timeline.length;
  function checkReady() {
    loadedCount++;
    if (loadedCount >= totalImgs) {
      window.__READY = true;
      console.log('[Slideshow] All slide images loaded. Ready.');
    }
  }

  if (totalImgs === 0) {
    window.__READY = true;
  } else {
    slideElements.forEach((el) => {
      const tester = new Image();
      tester.onload = checkReady;
      tester.onerror = () => {
        console.warn(`[Slideshow] Image missing or failed to load: ${el.item.src}`);
        checkReady();
      };
      tester.src = el.item.src;
    });
  }

  // Active seek function called by Playwright renderer & live preview
  let activeSlideIdx = -1;
  window.__seek = function (timeInSeconds) {
    let currentIdx = 0;
    for (let i = 0; i < timeline.length; i++) {
      if (timeInSeconds >= timeline[i].start) {
        currentIdx = i;
      } else {
        break;
      }
    }

    for (let i = 0; i < slideElements.length; i++) {
      const el = slideElements[i];
      const tItem = el.item;
      const wrap = el.wrap;
      const img = el.img;

      if (i === currentIdx) {
        const elapsed = timeInSeconds - tItem.start;
        const dur = Math.max(0.1, tItem.totalDuration);
        const progress = Math.min(1.0, elapsed / dur);

        // Opacity transition
        if (FADE_DUR > 0 && elapsed < FADE_DUR) {
          wrap.style.opacity = (elapsed / FADE_DUR).toFixed(3);
        } else {
          wrap.style.opacity = '1';
        }

        // Subtle Ken Burns zoom if enabled
        if (KEN_BURNS > 1.0) {
          const zoom = 1.0 + (KEN_BURNS - 1.0) * progress;
          img.style.transform = `scale(${zoom.toFixed(4)})`;
        } else {
          img.style.transform = 'scale(1)';
        }
      } else if (i === currentIdx - 1 && FADE_DUR > 0) {
        // Crossfade previous slide out
        const timeSinceNext = timeInSeconds - timeline[currentIdx].start;
        if (timeSinceNext < FADE_DUR) {
          wrap.style.opacity = (1.0 - timeSinceNext / FADE_DUR).toFixed(3);
        } else {
          wrap.style.opacity = '0';
        }
      } else {
        wrap.style.opacity = '0';
      }
    }

    activeSlideIdx = currentIdx;
  };

  // Audio Playback Preview in Browser
  let audioEl = null;
  let isPlaying = false;
  let rafId = null;

  function tick() {
    if (!isPlaying || !audioEl) return;
    window.__seek(audioEl.currentTime);
    rafId = requestAnimationFrame(tick);
  }

  window.__play = function () {
    if (!audioEl) {
      audioEl = new Audio('../voice/mix.wav');
      audioEl.addEventListener('ended', () => {
        isPlaying = false;
        cancelAnimationFrame(rafId);
      });
      audioEl.addEventListener('error', () => {
        audioEl = new Audio('../voice/narration.wav');
        audioEl.play();
      });
    }
    audioEl.play();
    isPlaying = true;
    rafId = requestAnimationFrame(tick);
  };

  window.__pause = function () {
    if (audioEl) audioEl.pause();
    isPlaying = false;
    cancelAnimationFrame(rafId);
  };

  window.__toggle = function () {
    if (isPlaying) {
      window.__pause();
    } else {
      window.__play();
    }
  };

  // Spacebar toggle playback
  window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
      e.preventDefault();
      window.__toggle();
    }
  });

  // Initial seek to frame 0
  window.__seek(0.0);
  window.CLOCK = {
    timeline: timeline,
    dur: timeline.length ? timeline[timeline.length - 1].end : 30.0
  };
})();
