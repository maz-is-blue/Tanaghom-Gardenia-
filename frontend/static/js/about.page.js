// counter animation for stats band
document.querySelectorAll('[data-counter]').forEach(el => {
  const target = +el.dataset.counter;
  const fmt = el.dataset.format || '';
  const duration = 1800;
  const step = target / (duration / 16);
  let current = 0;
  const io = new IntersectionObserver(entries => {
    if (!entries[0].isIntersecting) return;
    io.disconnect();
    const tick = () => {
      current = Math.min(current + step, target);
      el.textContent = Math.round(current) + fmt;
      if (current < target) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }, { threshold: 0.5 });
  io.observe(el);
});
