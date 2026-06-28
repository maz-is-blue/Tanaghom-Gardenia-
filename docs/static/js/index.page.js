// hero waveform
const wave = document.getElementById('waveform');
if (wave) {
  const N = 18;
  for (let i = 0; i < N; i++) {
    const bar = document.createElement('span');
    bar.className = 'bar';
    bar.style.animationDelay = `${(i / N) * 1.6}s`;
    bar.style.animationDuration = `${1.4 + (i % 3) * 0.2}s`;
    wave.appendChild(bar);
  }
}

// scroll progress
const prog = document.getElementById('scrollProgress');
if (prog) {
  window.addEventListener('scroll', () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const p = max > 0 ? window.scrollY / max : 0;
    prog.style.transform = `scaleX(${p})`;
  }, { passive: true });
}

// hero parallax (subtle)
const heroH1 = document.querySelector('.hero h1');
const heroAr = document.querySelector('.hero .ar-name');
if (heroH1) {
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    heroH1.style.transform = `translateY(${y * 0.18}px)`;
    if (heroAr) heroAr.style.transform = `translateY(${y * 0.12}px)`;
  }, { passive: true });
}
