/* ===== Gallery data ===== */
const moments = [
  { id: 1,  title: "Songs of the Levant",        date: "May 2025",  venue: "Al-Madina Hall",    ensemble: "gardenia", type: "concert",   year: "2025", size: "wide",   palette: ["#2a3d28", "#8DA086", "#F5D000"] },
  { id: 2,  title: "Winter Vespers",             date: "Dec 2024",  venue: "St. Joseph Church", ensemble: "tanaghom", type: "concert",   year: "2024", size: "tall",   palette: ["#1a1a1a", "#3a3414", "#F5D000"] },
  { id: 3,  title: "Open Rehearsal",             date: "Mar 2025",  venue: "Rehearsal Hall",    ensemble: "gardenia", type: "rehearsal", year: "2025", size: "square", palette: ["#4a4838", "#A8B8A2", "#FFFFFF"] },
  { id: 4,  title: "Three Adonis Poems",         date: "Oct 2024",  venue: "Sursock Museum",    ensemble: "tanaghom", type: "concert",   year: "2024", size: "normal", palette: ["#1a1a1a", "#F5D000", "#8DA086"] },
  { id: 5,  title: "Garden Recital",             date: "Jun 2024",  venue: "Beit Mery",         ensemble: "gardenia", type: "concert",   year: "2024", size: "wide",   palette: ["#8DA086", "#2a3d28", "#FFFFFF"] },
  { id: 6,  title: "Schools Programme",          date: "Apr 2025",  venue: "Rehearsal Hall",    ensemble: "gardenia", type: "rehearsal", year: "2025", size: "normal", palette: ["#F5D000", "#1a1a1a", "#A8B8A2"] },
  { id: 7,  title: "Maronite Sacred Hymns",      date: "Nov 2023",  venue: "Bkerké",            ensemble: "tanaghom", type: "concert",   year: "2023", size: "normal", palette: ["#1a1a1a", "#4a4838", "#F5D000"] },
  { id: 8,  title: "Sectional · Sopranos",       date: "Feb 2025",  venue: "Rehearsal Hall",    ensemble: "gardenia", type: "rehearsal", year: "2025", size: "square", palette: ["#A8B8A2", "#F5D000", "#1a1a1a"] },
  { id: 9,  title: "Layla Saade Premiere",       date: "Sep 2024",  venue: "Al-Madina Hall",    ensemble: "gardenia", type: "concert",   year: "2024", size: "tall",   palette: ["#2a3d28", "#1a1a1a", "#F5D000"] },
  { id: 10, title: "Tuning the Hall",            date: "Jan 2024",  venue: "Rehearsal Hall",    ensemble: "tanaghom", type: "rehearsal", year: "2024", size: "normal", palette: ["#3a3414", "#1a1a1a", "#A8B8A2"] },
  { id: 11, title: "Songs for a Difficult Year", date: "Aug 2023",  venue: "Private Garden",    ensemble: "gardenia", type: "concert",   year: "2023", size: "wide",   palette: ["#4a4838", "#A8B8A2", "#FFFFFF"] },
  { id: 12, title: "Wahdaki · وحدكِ",            date: "Mar 2024",  venue: "Sursock Museum",    ensemble: "tanaghom", type: "concert",   year: "2024", size: "normal", palette: ["#1a1a1a", "#3a3414", "#F5D000"] },
  { id: 13, title: "Section Read-Through",       date: "Sep 2023",  venue: "Rehearsal Hall",    ensemble: "tanaghom", type: "rehearsal", year: "2023", size: "square", palette: ["#1a1a1a", "#A8B8A2", "#F5D000"] },
  { id: 14, title: "Bruckner · Os justi",        date: "Apr 2024",  venue: "St. Joseph Church", ensemble: "gardenia", type: "concert",   year: "2024", size: "normal", palette: ["#2a3d28", "#1a1a1a", "#FFFFFF"] },
];

function bgFor(m) {
  const [a, b, c] = m.palette;
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
          <div class="cap-title">${m.title}</div>
          <div class="cap-meta">${m.date} · ${m.venue}</div>
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
let lbCurrent = 0;

function visibleMoments() {
  return moments.filter(m => {
    if (currentFilter === 'all') return true;
    return m.ensemble === currentFilter || m.type === currentFilter || m.year === currentFilter;
  });
}
function openLightbox(id) {
  const list = visibleMoments();
  const i = list.findIndex(m => m.id === id);
  if (i < 0) return;
  showLightbox(i);
  lb.classList.add('open');
  document.documentElement.classList.add('no-scroll');
}
function showLightbox(i) {
  const list = visibleMoments();
  if (!list.length) return;
  lbCurrent = (i + list.length) % list.length;
  const m = list[lbCurrent];
  lbImage.innerHTML = bgFor(m);
  lbTitle.textContent = m.title;
  lbDate.textContent  = m.date;
  lbVenue.textContent = m.venue;
  lbIdx.textContent   = lbCurrent + 1;
  lbTotal.textContent = list.length;
}
function closeLightbox() {
  lb.classList.remove('open');
  document.documentElement.classList.remove('no-scroll');
}
lbClose.addEventListener('click', closeLightbox);
lbPrev.addEventListener('click', () => showLightbox(lbCurrent - 1));
lbNext.addEventListener('click', () => showLightbox(lbCurrent + 1));
lb.addEventListener('click', (e) => { if (e.target === lb) closeLightbox(); });
document.addEventListener('keydown', (e) => {
  if (!lb.classList.contains('open')) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowRight') showLightbox(lbCurrent + 1);
  if (e.key === 'ArrowLeft')  showLightbox(lbCurrent - 1);
});
