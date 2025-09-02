// scripts/utils.js
export function apiFetch(url, opts = {}) {
  const base = localStorage.getItem('pt_api') || window.PT_API_BASE || '';
  const token = localStorage.getItem('pt_token');
  const headers = opts.headers || {};
  headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return fetch(base + url, {...opts, headers}).then(async res => {
    const text = await res.text();
    const data = text ? JSON.parse(text) : {};
    if (!res.ok) throw {status: res.status, data};
    return data;
  });
}

export function showToast(msg, type = 'info', timeout = 3500) {
  const t = document.getElementById('toast');
  if(!t) return alert(msg);
  t.textContent = msg;
  t.classList.remove('hidden');
  t.style.background = type === 'error' ? 'linear-gradient(90deg,#ff4d4f,#c92a2a)' : 'linear-gradient(90deg,#10b981,#06b6d4)';
  setTimeout(()=> t.classList.add('hidden'), timeout);
}
