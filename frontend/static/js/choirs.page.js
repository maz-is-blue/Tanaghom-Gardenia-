/* ===== Tab switcher ===== */
const tabs = document.querySelectorAll('.choir-tab');
const details = document.querySelectorAll('.choir-detail');
const underline = document.getElementById('tabUnderline');

function setUnderline(tab) {
  const r = tab.getBoundingClientRect();
  const wrap = tab.parentElement.getBoundingClientRect();
  underline.style.width = `${r.width}px`;
  underline.style.transform = `translateX(${r.left - wrap.left}px)`;
}
function activateTab(name, scroll = true) {
  tabs.forEach(t => t.classList.toggle('active', t.dataset.tab === name));
  details.forEach(d => d.classList.toggle('active', d.id === name));
  const active = document.querySelector(`.choir-tab[data-tab="${name}"]`);
  if (active) setUnderline(active);
  if (scroll) window.scrollTo({ top: document.querySelector('.choir-tabs-wrap').offsetTop - 80, behavior: 'smooth' });
}
tabs.forEach(t => t.addEventListener('click', () => {
  history.replaceState(null, '', '#' + t.dataset.tab);
  activateTab(t.dataset.tab);
}));
// initial: check hash
const initial = (location.hash || '#gardenia').slice(1);
if (initial === 'tanaghom' || initial === 'gardenia') {
  activateTab(initial, false);
} else {
  if (initial.startsWith('tanaghom')) activateTab('tanaghom', false);
  else activateTab('gardenia', false);
}
// place underline after fonts load
window.addEventListener('load', () => {
  const cur = document.querySelector('.choir-tab.active');
  if (cur) setUnderline(cur);
});
window.addEventListener('resize', () => {
  const cur = document.querySelector('.choir-tab.active');
  if (cur) setUnderline(cur);
});

/* ===== Players ===== */
document.querySelectorAll('[data-player]').forEach(player => {
  const wavesEl = player.querySelector('[data-waves]');
  const btn     = player.querySelector('[data-play]');
  const time    = player.querySelector('[data-time]');
  const N = 120;

  const heights = [];
  for (let i = 0; i < N; i++) {
    const h = (Math.sin(i / 4) * 0.35 + Math.sin(i / 9 + 1.5) * 0.25 + Math.random() * 0.4 + 0.25);
    heights.push(Math.max(0.1, Math.min(1, h)));
    const bar = document.createElement('div');
    bar.className = 'w';
    bar.style.height = `${heights[i] * 100}%`;
    wavesEl.appendChild(bar);
  }
  const bars = wavesEl.querySelectorAll('.w');

  let playing = false;
  let progress = 0;
  let lastT = 0;
  const total = 4 * 60 + 32;

  function render() {
    const head = Math.floor(progress * N);
    bars.forEach((b, i) => b.classList.toggle('played', i < head));
    const sec = Math.floor(progress * total);
    const m = Math.floor(sec / 60);
    const s = (sec % 60).toString().padStart(2, '0');
    time.textContent = `${m}:${s}`;
  }
  function tick(t) {
    if (!playing) return;
    const dt = lastT ? (t - lastT) / 1000 : 0;
    lastT = t;
    progress = Math.min(1, progress + dt / total);
    render();
    if (progress < 1) requestAnimationFrame(tick);
    else { playing = false; btn.classList.remove('playing'); player.classList.remove('playing'); }
  }
  btn.addEventListener('click', () => {
    playing = !playing;
    btn.classList.toggle('playing', playing);
    player.classList.toggle('playing', playing);
    lastT = 0;
    if (playing) requestAnimationFrame(tick);
  });
  wavesEl.addEventListener('click', (e) => {
    const r = wavesEl.getBoundingClientRect();
    progress = (e.clientX - r.left) / r.width;
    render();
  });
  render();
});

/* ===== Voice mix ===== */
document.querySelectorAll('[data-voicemix]').forEach(card => {
  const rows = card.querySelectorAll('[data-vm-row]');
  rows.forEach(row => {
    const barsEl = row.querySelector('.vm-bars');
    const color  = row.dataset.color;
    const N = 28;
    const bars = [];
    for (let i = 0; i < N; i++) {
      const b = document.createElement('div');
      b.className = 'vm-bar';
      b.style.background = color;
      b.style.height = '20%';
      barsEl.appendChild(b);
      bars.push(b);
    }
    let t = Math.random() * 10;
    function tick() {
      t += 0.05;
      bars.forEach((b, i) => {
        const v = (Math.sin(t + i * 0.4) * 0.4 + Math.sin(t * 0.7 + i) * 0.3 + 0.5) * 100;
        b.style.height = `${Math.max(6, v)}%`;
      });
      requestAnimationFrame(tick);
    }
    tick();
    row.addEventListener('click', () => row.classList.toggle('muted'));
  });
});
