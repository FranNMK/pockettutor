// scripts/flashcards.js
import { apiFetch, showToast } from './utils.js';

// ensure supabase client is available
const supabase = window.supabase;

// DOM
const generateCourseBtn = document.getElementById('generate-course-btn');
const generateFlashcardsBtn = document.getElementById('generate-flashcards-btn');
const remainingEl = document.getElementById('remaining-generation');
const topicInput = document.getElementById('generate-topic');

async function loadProfile() {
  const s = await supabase.auth.getUser();
  if (!s?.data?.user) return;
  const user = s.data.user;
  document.getElementById('user-info').textContent = user.email || user.id;
  // get subscription status from your profile table
  const { data: profile } = await supabase
    .from('profiles')
    .select('subscription,last_generated_at')
    .eq('id', user.id)
    .single();
  const isPro = profile?.subscription === 'pro';
  // compute remaining generation (if free)
  let remaining = 1;
  if (isPro) remaining = 'Unlimited';
  else {
    // simple logic: if last_generated_at is today then 0 else 1
    const last = profile?.last_generated_at ? new Date(profile.last_generated_at) : null;
    if (last) {
      const now = new Date();
      if (last.toDateString() === now.toDateString()) remaining = 0;
    }
  }
  remainingEl.textContent = remaining;
}

loadProfile();

// clicking generate course calls backend endpoint that runs HF + creates course in DB
generateCourseBtn.addEventListener('click', async () => {
  const topic = topicInput.value.trim();
  if (!topic) return showToast('Type a topic or paste notes first', 'error');
  try {
    showToast('Generating course — this may take a moment', 'info');
    // POST to your secure endpoint that calls Hugging Face / OpenAI and stores course in DB
    // Endpoint must implement daily-limits logic and check subscription status
    const res = await apiFetch('/api/generate/course', {
      method: 'POST',
      body: JSON.stringify({ topic })
    });
    showToast('Course generated: ' + (res.title || 'Untitled'), 'info', 4000);
    // refresh UI (e.g., fetch courses list)
    loadCourses();
  } catch (err) {
    console.error(err);
    showToast(err.data?.error || 'Could not generate course', 'error', 5000);
  }
});

// generate flashcards from text directly (client sends text to server to call HF)
generateFlashcardsBtn.addEventListener('click', async () => {
  const text = topicInput.value.trim();
  if (!text) return showToast('Enter text or topic to generate flashcards', 'error');
  try {
    showToast('Generating flashcards...');
    const out = await apiFetch('/api/generate/flashcards', { method: 'POST', body: JSON.stringify({ text }) });
    // show flashcards quickly in modal
    openModal('Generated flashcards', renderFlashcardsPreview(out.cards || out));
  } catch (err) {
    console.error(err);
    showToast(err.data?.error || 'Flashcard generation failed', 'error', 5000);
  }
});

function renderFlashcardsPreview(cards) {
  if (!cards || cards.length === 0) return '<p>No flashcards generated.</p>';
  const el = document.createElement('div');
  cards.forEach((c, i) => {
    const d = document.createElement('div');
    d.className = 'panel';
    d.innerHTML = `<strong>Q${i+1}:</strong> ${escapeHtml(c.question)}<br/><strong>A${i+1}:</strong> ${escapeHtml(c.answer)}`;
    el.appendChild(d);
  });
  return el;
}

// helpers for modal (dashboard)
function openModal(title, content) {
  const modal = document.getElementById('modal');
  modal.classList.remove('hidden');
  document.getElementById('modal-title').textContent = title;
  const body = document.getElementById('modal-body');
  body.innerHTML = '';
  if (typeof content === 'string') body.innerHTML = content;
  else body.appendChild(content);
  document.getElementById('modal-close').onclick = () => modal.classList.add('hidden');
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (m) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
}

// load courses (simple)
async function loadCourses() {
  const user = (await supabase.auth.getUser()).data.user;
  if (!user) return;
  const { data } = await supabase.from('courses').select('*').eq('user_id', user.id);
  const grid = document.getElementById('courses-grid');
  grid.innerHTML = '';
  data.forEach(c => {
    const card = document.createElement('div');
    card.className = 'panel';
    card.innerHTML = `<h4>${c.title}</h4><p>Status: ${c.status}</p><div class="row"><button class="btn" onclick="viewCourse('${c.id}')">Open</button></div>`;
    grid.appendChild(card);
  });
}
window.loadCourses = loadCourses;
loadCourses();
