/* Submit any [data-kind] form to the backend /api/submissions endpoint. */
(() => {
  const forms = document.querySelectorAll('form[data-kind]');
  forms.forEach((form) => {
    const statusEl = form.querySelector('[data-status]');
    const btn = form.querySelector('button[type="submit"]');

    function setStatus(msg, kind) {
      if (!statusEl) return;
      statusEl.textContent = msg;
      statusEl.className = 'form-status ' + (kind || '');
      statusEl.hidden = !msg;
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        kind: form.dataset.kind || 'contact',
        name: (form.name && form.name.value || '').trim(),
        email: (form.email && form.email.value || '').trim(),
        message: (form.message && form.message.value || '').trim(),
      };
      if (!payload.name || !payload.email) {
        setStatus('Please enter your name and email.', 'error');
        return;
      }
      if (btn) btn.disabled = true;
      setStatus('Sending…', '');
      try {
        const res = await fetch('/api/submissions', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (res.ok && data.ok) {
          form.reset();
          setStatus('Thank you — we’ll be in touch soon.', 'ok');
        } else {
          setStatus(data.error || 'Something went wrong. Please try again.', 'error');
        }
      } catch (err) {
        setStatus('Network error. Please try again.', 'error');
      } finally {
        if (btn) btn.disabled = false;
      }
    });
  });
})();
