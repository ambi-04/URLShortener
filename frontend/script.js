const form = document.getElementById('shorten-form');
    const longurlInput = document.getElementById('longurl');
    const resultBox = document.getElementById('result');
    const errorBox = document.getElementById('error');
    const copyBtn = document.getElementById('copy-btn');
    const submitBtn = document.getElementById('submit-btn');
    let generatedShortUrl = '';

    const showError = (message) => {
      errorBox.textContent = message;
      errorBox.style.display = 'block';
      resultBox.style.display = 'none';
      copyBtn.disabled = true;
    };

    const showResult = (url) => {
      resultBox.textContent = `Short URL: ${url}`;
      resultBox.style.display = 'block';
      errorBox.style.display = 'none';
      copyBtn.disabled = false;
    };

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const longurl = longurlInput.value.trim();

      if (!longurl) {
        showError('Please provide a valid Http/Https URL.');
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = 'Generating...';

      try {
        const response = await fetch('http://192.168.29.77:8000/shorten', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ longurl })
        });

        const payload = await response.json().catch(() => ({}));

        if (!response.ok) {
          showError(payload.message || payload.error || 'Unable to generate short URL.');
          return;
        }

        generatedShortUrl = payload.shorturl;
        showResult(generatedShortUrl);
      } catch (_) {
        showError('Network issue. Please try again in a moment.');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Generate short URL';
      }
    });

  copyBtn.addEventListener('click', async () => {
  if (!generatedShortUrl) return;

  try {
    await navigator.clipboard.writeText(generatedShortUrl);
    copyBtn.textContent = 'Copied!';
    setTimeout(() => {
      copyBtn.textContent = 'Copy short URL';
    }, 1200);
  } catch (_) {
    // Don't hide result
    errorBox.textContent = 'Clipboard permission denied. Please copy manually above.';
    errorBox.style.display = 'block';
  }
});
