/* Slideshow Engine: Deterministic, seek-driven, timed to narration.
   Supports instant cuts, letterbox 1:1 canvas on 9:16 vertical video, and real-time audio playback preview. */
(function () {
  const FILM = window.FILM || {};
  const WORDS = window.WORDS || [];
  const SLIDES = window.SLIDES || [];
  const W = FILM.W || 1080;
  const H = FILM.H || 1920;
  const FORMAT = FILM.format || '9:16';
  const CANVAS_CFG = FILM.canvas || {};
  const IS_SQUARE_IN_VERTICAL = (FORMAT === '9:16' && CANVAS_CFG.aspect_ratio === '1:1');
  const CANVAS_H = IS_SQUARE_IN_VERTICAL ? W : H;
  const CANVAS_TOP = IS_SQUARE_IN_VERTICAL ? Math.round((H - CANVAS_H) / 2) : 0;
  
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
    
    if (IS_SQUARE_IN_VERTICAL) {
      wrap.style.cssText = `
        position: absolute;
        top: ${CANVAS_TOP}px;
        left: 0;
        width: ${W}px;
        height: ${CANVAS_H}px;
        opacity: 0;
        overflow: hidden;
        background: ${CANVAS_CFG.canvas_bg || '#FBF6EF'};
        display: flex;
        align-items: center;
        justify-content: center;
        will-change: transform, opacity;
      `;
    } else {
      wrap.style.cssText = `
        position: absolute;
        inset: 0;
        opacity: 0;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        will-change: transform, opacity;
      `;
    }

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

    // Foreground main image
    const img = document.createElement('img');
    img.className = 'slide-img';
    img.src = item.src;
    
    if (IS_SQUARE_IN_VERTICAL) {
      img.style.cssText = `
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        object-fit: contain;
        z-index: 2;
        will-change: transform;
      `;
    } else {
      img.style.cssText = `
        position: relative;
        max-width: 96%;
        max-height: 94%;
        object-fit: contain;
        border-radius: ${CANVAS_CFG.border_radius || 0}px;
        box-shadow: ${CANVAS_CFG.shadow ? '0 25px 60px rgba(0,0,0,0.5)' : 'none'};
        z-index: 2;
        will-change: transform;
      `;
    }

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

  // Deterministic Seek Function: window.__seek(t)
  window.__seek = function (t) {
    let activeIdx = 0;
    for (let i = 0; i < timeline.length; i++) {
      if (t >= timeline[i].start) {
        activeIdx = i;
      } else {
        break;
      }
    }

    const cur = timeline[activeIdx];
    const isCut = (cur.transition === 'cut' || FADE_DUR <= 0.05);

    slideElements.forEach((el, idx) => {
      if (idx === activeIdx) {
        if (isCut) {
          el.wrap.style.opacity = '1.0';
          el.wrap.style.zIndex = '3';
        } else {
          let opacity = 1.0;
          if (t < cur.start + FADE_DUR && activeIdx > 0) {
            opacity = (t - cur.start) / FADE_DUR;
          }
          el.wrap.style.opacity = opacity.toFixed(3);
          el.wrap.style.zIndex = '3';
        }

        // Ken Burns zoom if configured
        if (KEN_BURNS > 1.0) {
          const progress = Math.max(0, Math.min(1, (t - cur.start) / Math.max(0.1, cur.totalDuration)));
          const zoom = 1.0 + (KEN_BURNS - 1.0) * progress;
          el.img.style.transform = `scale(${zoom.toFixed(4)})`;
        } else {
          el.img.style.transform = 'scale(1.0)';
        }

      } else if (!isCut && idx === activeIdx - 1 && t < cur.start + FADE_DUR) {
        // Crossfade Out for previous slide
        const fadeOut = 1.0 - ((t - cur.start) / FADE_DUR);
        el.wrap.style.opacity = Math.max(0, fadeOut).toFixed(3);
        el.wrap.style.zIndex = '2';
      } else {
        el.wrap.style.opacity = '0';
        el.wrap.style.zIndex = '1';
      }
    });
  };

  // Live browser playback controller
  window.addEventListener('load', () => {
    window.__seek(0);
    const audio = document.getElementById('narration-audio');
    if (audio) {
      let isPlaying = false;
      function tick() {
        if (!isPlaying) return;
        window.__seek(audio.currentTime);
        requestAnimationFrame(tick);
      }
      window.addEventListener('click', () => {
        if (audio.paused) {
          audio.play().then(() => {
            isPlaying = true;
            requestAnimationFrame(tick);
          }).catch(() => {});
        } else {
          audio.pause();
          isPlaying = false;
        }
      });
      window.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
          e.preventDefault();
          if (audio.paused) {
            audio.play().then(() => {
              isPlaying = true;
              requestAnimationFrame(tick);
            });
          } else {
            audio.pause();
            isPlaying = false;
          }
        }
      });
    }
  });

  window.CLOCK = { dur: window.DUR || 30.0 };
})();
