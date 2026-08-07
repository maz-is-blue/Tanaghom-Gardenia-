/* moments is injected by the Jinja2 template via gallery.html */
if (typeof moments === 'undefined') {
  window.moments = [];
}

function bgFor(m, imgIndex) {
  const imgs  = m.images && m.images.length ? m.images : (m.image ? [m.image] : []);
  const thumb = typeof imgIndex === 'number' ? (imgs[imgIndex] || imgs[0]) : imgs[0];
  if (thumb) {
    return `<div style="position:absolute;inset:0;background:url('${thumb}') center/cover no-repeat"></div>`;
  }
  if (m.video) {
    return `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:48px;background:#1a1a1a">▶</div>`;
  }
  const palette = m.palette || ['#2a3d28', '#8DA086', '#F5D000'];
  const [a, b, c] = palette;
  const isRehearsal = m.type === 'rehearsal';
  const figureRows = Array.from({length: 9}).map((_, i) => {
    const x = 30 + i * 42;
    return `<ellipse cx="${x}" cy="245" rx="18" ry="30"/><circle cx="${x}" cy="215" r="13"/>`;
  }).join('');
  const figureRows2 = Array.from({length: 9}).map((_, i) => {
    const x = 50 + i * 42;
    return `<ellipse cx="${x}" cy="225" rx="16" ry="28"/><circle cx="${x}" cy="198" r="11"/>`;
  }).join('');

  return `
    <div style="position:absolute;inset:0;background:
      radial-gradient(ellipse at ${isRehearsal ? '30% 70%' : '50% 30%'}, ${b} 0%, ${a} 60%, ${a} 100%);"></div>
    <svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:0;width:100%;height:100%;">
      ${isRehearsal ? `
        <g fill="${c}" opacity="0.18">
          <ellipse cx="100" cy="170" rx="36" ry="48"/>
          <circle cx="100" cy="120" r="22"/>
          <ellipse cx="200" cy="180" rx="40" ry="54"/>
          <circle cx="200" cy="128" r="24"/>
          <ellipse cx="300" cy="170" rx="36" ry="48"/>
          <circle cx="300" cy="120" r="22"/>
        </g>
        <g stroke="${c}" stroke-width="0.5" opacity="0.4" fill="none">
          <path d="M0 220 H 400 M0 240 H 400 M0 260 H 400"/>
        </g>
      ` : `
        <defs>
          <radialGradient id="spot${m.id}" cx="50%" cy="20%" r="60%">
            <stop offset="0%" stop-color="${c}" stop-opacity="0.45"/>
            <stop offset="100%" stop-color="${c}" stop-opacity="0"/>
          </radialGradient>
        </defs>
        <rect width="400" height="300" fill="url(#spot${m.id})"/>
        <g fill="${a}" opacity="0.92">${figureRows}</g>
        <g fill="${a}" opacity="0.62">${figureRows2}</g>
      `}
    </svg>
  `;
}

/* Render grid */
const grid = document.getElementById('galleryGrid');
function renderGrid(items) {
  grid.innerHTML = items.map((m, i) => `
    <button class="gal-card ${m.size === 'wide' ? 'size-wide' : m.size === 'tall' ? 'size-tall' : m.size === 'square' ? 'size-square' : ''}"
            data-ensemble="${m.ensemble}" data-type="${m.type}" data-year="${m.year}" data-id="${m.id}">
      <div class="bg">${bgFor(m)}</div>
      <div class="overlay"></div>
      <div class="corner-num">${String(i+1).padStart(2,'0')}</div>
      <div class="caption">
        <div>
          <div class="cap-title"><span class="en">${m.title}</span><span class="ar" style="font-family:'Noto Naskh Arabic',serif;">${m.titleAr}</span></div>
          <div class="cap-meta"><span class="en">${m.date} · ${m.venue}</span><span class="ar">${m.dateAr} · ${m.venueAr}</span></div>
        </div>
        <div class="cap-tag">${m.ensemble === 'gardenia' ? 'Gardenia' : 'Tanaghom'}</div>
      </div>
    </button>
  `).join('');
  grid.querySelectorAll('.gal-card').forEach(card => {
    card.addEventListener('click', () => openLightbox(parseInt(card.dataset.id, 10)));
  });
}
renderGrid(moments);

/* Filter counts */
function counts() {
  const c = { all: moments.length, concert: 0, rehearsal: 0, gardenia: 0, tanaghom: 0, '2023': 0, '2024': 0, '2025': 0 };
  moments.forEach(m => { c[m.type]++; c[m.ensemble]++; c[m.year]++; });
  document.querySelectorAll('.filter-chip .count').forEach(el => {
    const k = el.dataset.c;
    el.textContent = c[k] || 0;
  });
}
counts();

/* Filtering */
let currentFilter = 'all';
document.querySelectorAll('.filter-chip').forEach(chip => {
  chip.addEventListener('click', () => {
    document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    currentFilter = chip.dataset.filter;
    applyFilter();
  });
});
function applyFilter() {
  const f = currentFilter;
  let shown = 0;
  grid.querySelectorAll('.gal-card').forEach(card => {
    const match = f === 'all' || card.dataset.ensemble === f || card.dataset.type === f || card.dataset.year === f;
    card.classList.toggle('hide', !match);
    if (match) shown++;
  });
  document.getElementById('filterCount').textContent = shown;
  const fcAr = document.getElementById('filterCountAr');
  if (fcAr) fcAr.textContent = shown;
}

/* ===== Lightbox ===== */
const lb      = document.getElementById('lightbox');
const lbClose = document.getElementById('lbClose');
const lbPrev  = document.getElementById('lbPrev');
const lbNext  = document.getElementById('lbNext');
const lbImage = document.getElementById('lbImage');
const lbTitle = document.getElementById('lbTitle');
const lbDate  = document.getElementById('lbDate');
const lbVenue = document.getElementById('lbVenue');
const lbIdx   = document.getElementById('lbIdx');
const lbTotal = document.getElementById('lbTotal');
let lbCurrent  = 0;
let lbPhotoIdx = 0;  // index within current item's images array

function visibleMoments() {
  return moments.filter(m => {
    if (currentFilter === 'all') return true;
    return m.ensemble === currentFilter || m.type === currentFilter || m.year === currentFilter;
  });
}

function _mediaFor(m, idx) {
  const imgs = m.images && m.images.length ? m.images : (m.image ? [m.image] : []);
  // If the requested index is beyond images, show the video (if any)
  if (idx >= imgs.length && m.video) {
    return { type: 'video', src: m.video };
  }
  if (imgs[idx]) return { type: 'image', src: imgs[idx] };
  if (m.video)   return { type: 'video', src: m.video };
  return null;
}

function _mediaCount(m) {
  const imgs = m.images && m.images.length ? m.images : (m.image ? [m.image] : []);
  return imgs.length + (m.video ? 1 : 0);
}

function renderLbMedia(m, idx) {
  const media = _mediaFor(m, idx);
  if (!media) {
    lbImage.innerHTML = bgFor(m);
    return;
  }
  if (media.type === 'video') {
    lbImage.innerHTML = `<video src="${media.src}" controls autoplay style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000"></video>`;
  } else {
    lbImage.innerHTML = `<img src="${media.src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain">`;
  }

  // Dots navigation for multi-media items
  const total = _mediaCount(m);
  let dots = document.getElementById('lbDots');
  if (!dots) {
    dots = document.createElement('div');
    dots.id = 'lbDots';
    dots.style.cssText = 'position:absolute;bottom:12px;left:50%;transform:translateX(-50%);display:flex;gap:6px;z-index:10';
    lbImage.parentElement.appendChild(dots);
  }
  if (total > 1) {
    dots.style.display = 'flex';
    dots.innerHTML = Array.from({length: total}).map((_, di) =>
      `<span style="width:8px;height:8px;border-radius:50%;background:${di === idx ? '#F5D000' : 'rgba(255,255,255,.4)'};cursor:pointer;transition:.2s" data-di="${di}"></span>`
    ).join('');
    dots.querySelectorAll('span').forEach(dot => {
      dot.addEventListener('click', (e) => {
        e.stopPropagation();
        lbPhotoIdx = parseInt(dot.dataset.di, 10);
        renderLbMedia(visibleMoments()[lbCurrent], lbPhotoIdx);
      });
    });
  } else {
    dots.style.display = 'none';
  }
}

function openLightbox(id) {
  const list = visibleMoments();
  const i = list.findIndex(m => m.id === id);
  if (i < 0) return;
  lbPhotoIdx = 0;
  showLightbox(i);
  lb.classList.add('open');
  document.documentElement.classList.add('no-scroll');
}
function showLightbox(i) {
  const list = visibleMoments();
  if (!list.length) return;
  lbCurrent = (i + list.length) % list.length;
  lbPhotoIdx = 0;
  const m = list[lbCurrent];
  renderLbMedia(m, lbPhotoIdx);
  lbTitle.innerHTML = `<span class="en">${m.title}</span><span class="ar" style="font-family:'Noto Naskh Arabic',serif;">${m.titleAr}</span>`;
  lbDate.innerHTML  = `<span class="en">${m.date}</span><span class="ar">${m.dateAr}</span>`;
  lbVenue.innerHTML = `<span class="en">${m.venue}</span><span class="ar">${m.venueAr}</span>`;
  lbIdx.textContent   = lbCurrent + 1;
  lbTotal.textContent = list.length;
}
function closeLightbox() {
  lb.classList.remove('open');
  document.documentElement.classList.remove('no-scroll');
  // pause any video
  const vid = lb.querySelector('video');
  if (vid) vid.pause();
}
lbClose.addEventListener('click', closeLightbox);
lbPrev.addEventListener('click', () => showLightbox(lbCurrent - 1));
lbNext.addEventListener('click', () => showLightbox(lbCurrent + 1));
lb.addEventListener('click', (e) => { if (e.target === lb) closeLightbox(); });
document.addEventListener('keydown', (e) => {
  if (!lb.classList.contains('open')) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowRight') {
    const m = visibleMoments()[lbCurrent];
    if (m && lbPhotoIdx < _mediaCount(m) - 1) {
      lbPhotoIdx++;
      renderLbMedia(m, lbPhotoIdx);
    } else {
      showLightbox(lbCurrent + 1);
    }
  }
  if (e.key === 'ArrowLeft') {
    const m = visibleMoments()[lbCurrent];
    if (m && lbPhotoIdx > 0) {
      lbPhotoIdx--;
      renderLbMedia(m, lbPhotoIdx);
    } else {
      showLightbox(lbCurrent - 1);
    }
  }
});
