/* ===== Gallery data =====
     Moments are loaded from the backend API (/api/gallery), which reads them
     from MongoDB. Each entry renders a stylized placeholder visual; drop in an
     `image` URL per moment and extend bgFor() to show real photographs.
  */
  let moments = [];

  /* Build a stylized "photo" placeholder per moment — gradient + abstract overlay,
     so it reads as intentional art direction not slop. Replace with <img> when real
     photographs are available. */
  function bgFor(m, large = false) {
    const [a, b, c] = m.palette;
    // a couple of variants depending on type
    const isRehearsal = m.type === 'rehearsal';
    return `
      <div style="position:absolute;inset:0;background:
        radial-gradient(ellipse at ${isRehearsal ? '30% 70%' : '50% 30%'}, ${b} 0%, ${a} 60%, ${a} 100%);"></div>
      <svg viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" style="position:absolute;inset:0;width:100%;height:100%;">
        ${isRehearsal ? `
          <!-- abstract figures -->
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
          <!-- spotlight / stage -->
          <defs>
            <radialGradient id="spot${m.id}" cx="50%" cy="20%" r="60%">
              <stop offset="0%" stop-color="${c}" stop-opacity="0.45"/>
              <stop offset="100%" stop-color="${c}" stop-opacity="0"/>
            </radialGradient>
          </defs>
          <rect width="400" height="300" fill="url(#spot${m.id})"/>
          <!-- choir silhouette: 2 rows of figures -->
          <g fill="${a}" opacity="0.92">
            ${Array.from({length: 9}).map((_, i) => {
              const x = 30 + i * 42;
              return `<ellipse cx="${x}" cy="245" rx="18" ry="30"/><circle cx="${x}" cy="215" r="13"/>`;
            }).join('')}
          </g>
          <g fill="${a}" opacity="0.62">
            ${Array.from({length: 9}).map((_, i) => {
              const x = 50 + i * 42;
              return `<ellipse cx="${x}" cy="225" rx="16" ry="28"/><circle cx="${x}" cy="198" r="11"/>`;
            }).join('')}
          </g>
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
    // wire clicks
    grid.querySelectorAll('.gal-card').forEach(card => {
      card.addEventListener('click', () => openLightbox(parseInt(card.dataset.id, 10)));
    });
  }

  /* Filter counts */
  function counts() {
    const c = { all: moments.length, concert: 0, rehearsal: 0, gardenia: 0, tanaghom: 0, '2023': 0, '2024': 0, '2025': 0 };
    moments.forEach(m => {
      c[m.type]++; c[m.ensemble]++; c[m.year]++;
    });
    document.querySelectorAll('.filter-chip .count').forEach(el => {
      const k = el.dataset.c;
      el.textContent = c[k] || 0;
    });
  }

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
      const match = f === 'all' ||
                    card.dataset.ensemble === f ||
                    card.dataset.type === f ||
                    card.dataset.year === f;
      card.classList.toggle('hide', !match);
      if (match) shown++;
    });
    document.getElementById('filterCount').textContent = shown;
  }

  /* ===== Lightbox ===== */
  const lb       = document.getElementById('lightbox');
  const lbClose  = document.getElementById('lbClose');
  const lbPrev   = document.getElementById('lbPrev');
  const lbNext   = document.getElementById('lbNext');
  const lbImage  = document.getElementById('lbImage');
  const lbTitle  = document.getElementById('lbTitle');
  const lbDate   = document.getElementById('lbDate');
  const lbVenue  = document.getElementById('lbVenue');
  const lbIdx    = document.getElementById('lbIdx');
  const lbTotal  = document.getElementById('lbTotal');
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
    lbImage.innerHTML = bgFor(m, true);
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

  /* ===== Load moments from the backend, then render ===== */
  fetch('api/gallery.json')
    .then((r) => r.json())
    .then((data) => {
      moments = data;
      renderGrid(moments);
      counts();
      applyFilter();
      lbTotal.textContent = moments.length;
    })
    .catch((err) => {
      console.error('Failed to load gallery', err);
      grid.innerHTML = '<p style="color: var(--gray); padding: 40px;">Gallery is unavailable right now.</p>';
    });
