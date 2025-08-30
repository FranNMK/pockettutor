const API_BASE = "http://127.0.0.1:5000";

function toast(msg){ alert(msg); }

async function api(path, method="GET", body=null){
  const opts = { method, headers: { "Content-Type":"application/json" } };
  if(body) opts.body = JSON.stringify(body);
  const res = await fetch(`${API_BASE}${path}`, opts);
  const data = await res.json().catch(()=> ({}));
  if(!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

// theme
const root = document.documentElement;
function toggleTheme(){
  const cur = root.getAttribute("data-theme") || document.documentElement.dataset.theme || "dark";
  const next = cur === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
}
document.addEventListener("DOMContentLoaded", ()=>{
  const t = document.getElementById("themeBtn");
  if(t) t.addEventListener("click", toggleTheme);
});
