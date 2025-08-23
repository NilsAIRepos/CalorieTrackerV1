document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('provider').value = localStorage.getItem('llmProvider') || 'ollama';
  document.getElementById('base-url').value = localStorage.getItem('llmBaseUrl') || 'http://localhost:11434';
  document.getElementById('model').value = localStorage.getItem('llmModel') || 'llama3.2:latest';
});

document.getElementById('settings-form').addEventListener('submit', e => {
  e.preventDefault();
  localStorage.setItem('llmProvider', document.getElementById('provider').value);
  localStorage.setItem('llmBaseUrl', document.getElementById('base-url').value);
  localStorage.setItem('llmModel', document.getElementById('model').value);
  alert('Settings saved');
});

document.getElementById('test-btn').addEventListener('click', async () => {
  const provider = document.getElementById('provider').value;
  const baseUrl = document.getElementById('base-url').value;
  const model = document.getElementById('model').value;
  const res = await fetch(`/api/llm/chat?provider=${encodeURIComponent(provider)}&base_url=${encodeURIComponent(baseUrl)}&model=${encodeURIComponent(model)}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages: [{ role: 'user', content: 'Hello' }] })
  });
  const data = await res.json();
  alert(data.reply);
});
