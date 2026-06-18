// timeline: scroll-activate items
  const tlItems = document.querySelectorAll('.tl-item');
  const tlIo = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) e.target.classList.add('active');
    });
  }, { threshold: 0.45 });
  tlItems.forEach(it => tlIo.observe(it));
