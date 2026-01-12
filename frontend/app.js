/* app.js */

// --- State ---
const state = {
  messages: [],
  isLoading: false,
  entries: []
};

// --- DOM Elements ---
const chatList = document.getElementById('chat-list');
const chatInput = document.getElementById('chat-input');
const chatForm = document.getElementById('chat-form');
const entriesList = document.getElementById('entries-list');
const mainTab = document.getElementById('tab-main');
const manualTab = document.getElementById('tab-manual');
const viewChat = document.getElementById('view-chat');
const viewManual = document.getElementById('view-manual');

// --- Initialization ---
function init() {
  fetchEntries();
  setupEventListeners();
  // Initial greeting
  addMessage({ role: 'assistant', content: "Hello! What did you eat today? I can help you look up nutrition info." });
}

function setupEventListeners() {
  chatForm.addEventListener('submit', handleChatSubmit);

  // Tab switching
  document.getElementById('nav-chat').addEventListener('click', () => switchTab('chat'));
  document.getElementById('nav-manual').addEventListener('click', () => switchTab('manual'));

  // Manual form (Legacy)
  document.getElementById('manual-entry-form').addEventListener('submit', handleManualSubmit);
}

function switchTab(tab) {
  if (tab === 'chat') {
    viewChat.style.display = 'flex'; // Chat needs flex
    viewManual.style.display = 'none';
    document.getElementById('nav-chat').classList.add('active');
    document.getElementById('nav-manual').classList.remove('active');
  } else {
    viewChat.style.display = 'none';
    viewManual.style.display = 'block';
    document.getElementById('nav-chat').classList.remove('active');
    document.getElementById('nav-manual').classList.add('active');
  }
}

// --- Chat Logic ---

async function handleChatSubmit(e) {
  e.preventDefault();
  const text = chatInput.value.trim();
  if (!text) return;

  // Add User Message
  addMessage({ role: 'user', content: text });
  chatInput.value = '';
  state.isLoading = true;
  renderChat();

  // Call API
  try {
    const response = await fetch('/api/chat/message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: state.messages.map(m => ({ role: m.role, content: m.content })),
        // provider: 'ollama' // Removed hardcoded provider. Let backend decide or user config in future.
      })
    });

    const data = await response.json();

    // Add Assistant Response
    addMessage({
      role: 'assistant',
      content: data.text,
      draft_entry: data.draft_entry
    });

  } catch (err) {
    console.error(err);
    addMessage({ role: 'assistant', content: "Sorry, I encountered an error communicating with the server." });
  } finally {
    state.isLoading = false;
    renderChat();
  }
}

function addMessage(msg) {
  state.messages.push(msg);
  renderChat();
}

function renderChat() {
  chatList.innerHTML = '';

  state.messages.forEach(msg => {
    const div = document.createElement('div');
    div.className = `message message-${msg.role}`;

    // Text Content
    const p = document.createElement('div');
    p.className = 'message-content';
    p.textContent = msg.content;
    div.appendChild(p);

    // Draft Entry Card
    if (msg.draft_entry) {
      const card = document.createElement('div');
      card.className = 'draft-card';

      const title = document.createElement('h4');
      title.textContent = "Draft: " + msg.draft_entry.name;
      card.appendChild(title);

      const summary = document.createElement('div');
      summary.className = 'draft-summary';
      summary.innerHTML = `
        <span>${msg.draft_entry.total_calories} kcal</span>
        <span>P: ${msg.draft_entry.total_protein}g</span>
        <span>C: ${msg.draft_entry.total_carbs}g</span>
        <span>F: ${msg.draft_entry.total_fat}g</span>
      `;
      card.appendChild(summary);

      const btn = document.createElement('button');
      btn.className = 'btn btn-sm btn-primary';
      btn.textContent = 'Confirm & Save';
      btn.onclick = () => saveDraftEntry(msg.draft_entry);
      card.appendChild(btn);

      div.appendChild(card);
    }

    chatList.appendChild(div);
  });

  // Auto scroll
  chatList.scrollTop = chatList.scrollHeight;
}

async function saveDraftEntry(draft) {
  const body = {
    name: draft.name,
    calories: draft.total_calories,
    protein: draft.total_protein,
    carbs: draft.total_carbs,
    fat: draft.total_fat,
    sugar: draft.total_sugar,
    details: JSON.stringify(draft.ingredients)
  };

  await fetch('/api/entries/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  addMessage({ role: 'assistant', content: "Entry saved successfully! Check the daily log." });
  fetchEntries();
}

// --- Entries List Logic ---

async function fetchEntries() {
  const res = await fetch('/api/entries/');
  state.entries = await res.json();
  renderEntries();
}

function renderEntries() {
  entriesList.innerHTML = '';
  let totalCals = 0;

  state.entries.forEach(e => {
    totalCals += e.calories;

    const li = document.createElement('li');
    li.className = 'entry-item';

    // Header Row
    const header = document.createElement('div');
    header.className = 'entry-header';
    header.innerHTML = `
      <span class="entry-name">${e.name}</span>
      <span class="entry-cals">${e.calories} kcal</span>
      <i class="fa-solid fa-chevron-down entry-expand-icon"></i>
    `;
    header.onclick = () => toggleEntryDetails(li);
    li.appendChild(header);

    // Details Row (Hidden by default)
    const details = document.createElement('div');
    details.className = 'entry-details';
    details.innerHTML = `
      <div class="macro-grid">
        <div class="macro-item">
          <span class="label">Protein</span>
          <span class="value">${e.protein || 0}g</span>
        </div>
        <div class="macro-item">
          <span class="label">Carbs</span>
          <span class="value">${e.carbs || 0}g</span>
        </div>
        <div class="macro-item">
          <span class="label">Fat</span>
          <span class="value">${e.fat || 0}g</span>
        </div>
        <div class="macro-item">
          <span class="label">Sugar</span>
          <span class="value">${e.sugar || 0}g</span>
        </div>
      </div>
      ${e.details ? `<div class="ingredients-list"><small>${parseDetails(e.details)}</small></div>` : ''}
    `;
    li.appendChild(details);

    entriesList.appendChild(li);
  });

  // Update header summary if we had one, but we'll stick to the list for now
}

function parseDetails(detailsStr) {
    try {
        if (!detailsStr.startsWith('[')) return detailsStr;
        const items = JSON.parse(detailsStr);
        return items.map(i => `${i.name} (${i.calories} kcal)`).join(', ');
    } catch {
        return detailsStr;
    }
}

function toggleEntryDetails(li) {
  li.classList.toggle('expanded');
}

// --- Manual Legacy Logic ---

async function handleManualSubmit(e) {
  e.preventDefault();
  const name = document.getElementById('manual-name').value;
  const protein = parseFloat(document.getElementById('manual-protein').value) || 0;
  const carbs = parseFloat(document.getElementById('manual-carbs').value) || 0;
  const fat = parseFloat(document.getElementById('manual-fat').value) || 0;
  const sugar = parseFloat(document.getElementById('manual-sugar').value) || 0;
  const calories = parseInt(document.getElementById('manual-calories').value) || 0;

  const body = {
    name,
    calories,
    protein,
    carbs,
    fat,
    sugar
  };

  await fetch('/api/entries/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  e.target.reset();
  fetchEntries();
  switchTab('chat'); // Go back to chat/main view or stay? Let's stay but show toast?
  alert('Entry Added');
}

// Start
init();
