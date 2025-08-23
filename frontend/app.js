async function fetchEntries() {
  const res = await fetch('/api/entries/');
  const entries = await res.json();
  const list = document.getElementById('entries');
  list.innerHTML = '';
  entries.forEach(e => {
    const li = document.createElement('li');
    li.textContent = `${e.name} - ${e.calories} kcal`;
    list.appendChild(li);
  });
}

document.getElementById('entry-form').addEventListener('submit', async e => {
  e.preventDefault();
  const name = document.getElementById('name').value;
  const protein = parseFloat(document.getElementById('protein').value) || 0;
  const carbs = parseFloat(document.getElementById('carbs').value) || 0;
  const fat = parseFloat(document.getElementById('fat').value) || 0;
  const calories = parseInt(document.getElementById('calories').value) || null;
  const body = {
    name,
    calories,
    nutrition: calories ? null : { protein, carbs, fat }
  };
  await fetch('/api/entries/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  e.target.reset();
  fetchEntries();
});

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('service-worker.js');
}

fetchEntries();
