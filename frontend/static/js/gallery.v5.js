/* moments is injected by the Jinja2 template via gallery.html */
if (typeof moments === 'undefined') {
  window.moments = [];
}

function bgFor(m) {
  const imgs  = m.images && m.images.length ? m.images : (m.image ? [m.image] : []);
  const thumb = imgs[0];
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
    rebuildFlat();
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

/* ===== Lightbox — flat media list ===================================
   Every photo and video from every visible event is one entry.
   Prev/next and arrow keys navigate through all of them in order.
   Counter shows "3 / 10" = photo 3 out of 10 total.
================================================================== */
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

let flatList = [];   // [{moment, type:'image'|'video'|'placeholder', src}]
let lbCurrent = 0;

function buildFlatList() {
  const visible = moments.filter(m => {
    if (currentFilter === 'all') return true;
    return m.ensemble === currentFilter || m.type === currentFilter || m.year === currentFilter;
  });
  flatList = [];
  visible.forEach(m => {
    const imgs = m.images && m.images.length ? m.images : (m.image ? [m.image] : []);
    if (imgs.length) {
      imgs.forEach(src => flatList.push({ moment: m, type: 'image', src }));
    }
    if (m.video) {
      flatList.push({ moment: m, type: 'video', src: m.video });
    }
    if (!imgs.length && !m.video) {
      flatList.push({ moment: m, type: 'placeholder', src: null });
    }
  });
}

function rebuildFlat() {
  buildFlatList();
}

function showAt(i) {
  if (!flatList.length) return;
  lbCurrent = (i + flatList.length) % flatList.length;
  const item = flatList[lbCurrent];
  const m    = item.moment;

  if (item.type === 'video') {
    lbImage.innerHTML = `<video src="${item.src}" controls autoplay
      style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000"></video>`;
  } else if (item.type === 'image') {
    lbImage.innerHTML = `<img src="${item.src}" alt="${m.title}"
      style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">`;
  } else {
    lbImage.innerHTML = bgFor(m);
  }

  lbTitle.innerHTML = `<span class="en">${m.title}</span><span class="ar" style="font-family:'Noto Naskh Arabic',serif;">${m.titleAr}</span>`;
  lbDate.innerHTML  = `<span class="en">${m.date}</span><span class="ar">${m.dateAr}</span>`;
  lbVenue.innerHTML = `<span class="en">${m.venue}</span><span class="ar">${m.venueAr}</span>`;
  lbIdx.textContent   = lbCurrent + 1;
  lbTotal.textContent = flatList.length;
}

function openLightbox(id) {
  buildFlatList();
  const i = flatList.findIndex(item => item.moment.id === id);
  if (i < 0) return;
  showAt(i);
  lb.classList.add('open');
  document.documentElement.classList.add('no-scroll');
}

function closeLightbox() {
  lb.classList.remove('open');
  document.documentElement.classList.remove('no-scroll');
  const vid = lb.querySelector('video');
  if (vid) vid.pause();
}

lbClose.addEventListener('click', closeLightbox);
lbPrev.addEventListener('click',  () => showAt(lbCurrent - 1));
lbNext.addEventListener('click',  () => showAt(lbCurrent + 1));
lb.addEventListener('click', e => { if (e.target === lb) closeLightbox(); });
document.addEventListener('keydown', e => {
  if (!lb.classList.contains('open')) return;
  if (e.key === 'Escape')      closeLightbox();
  if (e.key === 'ArrowRight')  showAt(lbCurrent + 1);
  if (e.key === 'ArrowLeft')   showAt(lbCurrent - 1);
});

buildFlatList();
console.log('[Gallery v5] moments:', moments.length, '| flatList:', flatList.length, '| sample:', JSON.stringify(flatList[0]));
