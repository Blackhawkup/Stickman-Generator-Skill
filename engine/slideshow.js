/* Slideshow Engine: Deterministic, seek-driven, timed to narration.
   Supports centered presentation with matching background fill for 1080x1920 (phone 9:16) and 1920x1080 (laptop 16:9),
   plus synced high-contrast phrase subtitles rendered across every video. */
(function () {
  const FILM = window.FILM || {};
  const WORDS = window.WORDS || [];
  const SLIDES = window.SLIDES || [];
  const W = FILM.W || 1080;
  const H = FILM.H || 1920;
  const FORMAT = FILM.format || '9:16';
  const SUBTITLES_ENABLED = !(FILM.subtitles && FILM.subtitles.enabled === false);
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

  // Build Synced Word-Highlighted Subtitle Cues
  function buildSubtitleCues(words) {
    if (!SUBTITLES_ENABLED || !words || !words.length) return [];
    const isPortrait = H > W;
    const maxWords = isPortrait ? 3 : 6;
    const maxChars = isPortrait ? 22 : 44;
    const cues = [];
    let buf = [];
    let charCount = 0;

    function flush() {
      if (!buf.length) return;
      cues.push({
        start: buf[0].s,
        end: buf[buf.length - 1].e,
        words: buf
      });
      buf = [];
      charCount = 0;
    }

    for (let i = 0; i < words.length; i++) {
      const w = words[i];
      const text = (w.w || '').trim();
      if (!text) continue;

      if (buf.length > 0) {
        const gap = w.s - buf[buf.length - 1].e;
        if (gap > 0.38 || buf.length >= maxWords || (charCount + text.length + 1) > maxChars) {
          flush();
        }
      }

      buf.push({ w: text, s: Number(w.s) || 0, e: Number(w.e) || 0 });
      charCount += text.length + 1;

      if (/[.!?,;:]$/.test(text)) {
        flush();
      }
    }
    flush();

    // Extend cue end slightly across tiny breath gaps so subtitles read smoothly without flickering
    for (let i = 0; i < cues.length; i++) {
      const nextStart = (i + 1 < cues.length) ? cues[i + 1].start : (cues[i].end + 0.35);
      cues[i].displayEnd = Math.min(nextStart - 0.01, cues[i].end + 0.40);
    }
    return cues;
  }

  const subtitleCues = buildSubtitleCues(WORDS);
  const viewport = document.getElementById('viewport') || document.body;
  let subOverlay = null;
  if (SUBTITLES_ENABLED && subtitleCues.length > 0) {
    const isPortrait = H > W;
    const fontSize = isPortrait ? Math.round(W * 0.064) : Math.round(H * 0.050);
    const strokeW = isPortrait ? 10 : 8;
    const sideMargin = 110;
    const bottomPos = isPortrait ? `${Math.max(480, Math.round(H * 0.26))}px` : '42px';

    subOverlay = document.createElement('div');
    subOverlay.id = 'subtitle-overlay';
    subOverlay.style.cssText = `
      position: absolute;
      left: ${sideMargin}px;
      right: ${sideMargin}px;
      bottom: ${bottomPos};
      z-index: 25;
      pointer-events: none;
      display: none;
      text-align: center;
    `;
    subOverlay.innerHTML = `<div id="subtitle-pill" style="
      display: inline-block;
      background: transparent;
      border: none;
      padding: 0;
      box-shadow: none;
      font-family: 'Inter', 'Segoe UI', 'Arial Rounded MT Bold', system-ui, sans-serif;
      font-size: ${fontSize}px;
      font-weight: 900;
      line-height: 1.25;
      color: #FFFFFF;
      letter-spacing: 0.01em;
      -webkit-text-stroke: ${strokeW}px #0F172A;
      paint-order: stroke fill;
      text-shadow: 0 4px 12px rgba(15, 23, 42, 0.38);
    "></div>`;
    viewport.appendChild(subOverlay);
  }

  let lastCueIdx = -2;
  let lastWordIdx = -2;

  function renderSubtitles(timeInSeconds) {
    if (!subOverlay || !subtitleCues.length) return;
    let cueIdx = -1;
    for (let i = 0; i < subtitleCues.length; i++) {
      const c = subtitleCues[i];
      if (timeInSeconds >= c.start && timeInSeconds <= c.displayEnd) {
        cueIdx = i;
        break;
      }
    }

    if (cueIdx === -1) {
      if (lastCueIdx !== -1) {
        subOverlay.style.display = 'none';
        lastCueIdx = -1;
        lastWordIdx = -1;
      }
      return;
    }

    const cue = subtitleCues[cueIdx];
    let activeWordIdx = -1;
    for (let j = 0; j < cue.words.length; j++) {
      if (timeInSeconds >= cue.words[j].s) {
        activeWordIdx = j;
      }
    }

    if (cueIdx === lastCueIdx && activeWordIdx === lastWordIdx) {
      return;
    }

    const pill = subOverlay.firstElementChild;
    pill.innerHTML = cue.words.map((w, idx) => {
      const color = (idx === activeWordIdx) ? '#FACC15' : '#FFFFFF';
      return `<span style="color:${color};">${w.w.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</span>`;
    }).join(' ');

    subOverlay.style.display = 'block';
    lastCueIdx = cueIdx;
    lastWordIdx = activeWordIdx;
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

    renderSubtitles(timeInSeconds);
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
