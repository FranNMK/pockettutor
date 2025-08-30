document.addEventListener("DOMContentLoaded", ()=>{
  const user = JSON.parse(localStorage.getItem("pt_user")||"null");
  if(!user){ window.location.href="index.html"; return; }
  const uName = document.getElementById("userName"); if(uName) uName.textContent = user.name;

  // tabs
  const tabs = document.querySelectorAll(".tab");
  const sections = { flashcards: document.getElementById("flashcards"), "ai-course":document.getElementById("ai-course"), library:document.getElementById("library") };
  tabs.forEach(t => t.addEventListener("click", ()=>{
    tabs.forEach(x=>x.classList.remove("active"));
    t.classList.add("active");
    Object.values(sections).forEach(s=>s.style.display="none");
    sections[t.dataset.tab].style.display="block";
  }));

  // profile dropdown
  const profileBtn = document.getElementById("profileBtn");
  const dropdown = document.getElementById("dropdown");
  profileBtn.addEventListener("click", ()=> dropdown.classList.toggle("show"));
  document.addEventListener("click", (e)=>{ if(!profileBtn.contains(e.target) && !dropdown.contains(e.target)) dropdown.classList.remove("show"); });

  // load library
  loadLibrary();
});

async function loadLibrary(){
  try{
    const items = await api("/api/courses/library");
    const list = document.getElementById("courseList");
    list.innerHTML = items.map(i=>`
      <div class="panel">
        <div class="badge">${i.kind}</div>
        <h4>${i.title}</h4>
        <p class="small">${i.description || ""}</p>
        <button class="btn" onclick="enroll(${i.id})">Enroll</button>
      </div>
    `).join("");
  }catch(e){ toast(e.message); }
}

async function enroll(courseId){
  const user = JSON.parse(localStorage.getItem("pt_user"));
  try{
    await api("/api/courses/enroll","POST",{user_id:user.id, course_id:courseId});
    toast("Enrolled!");
  }catch(e){ toast(e.message); }
}
import React, { useEffect, useState } from "react";
import { apiFetch } from "../api";

function Dashboard() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await apiFetch("/auth/me");
        setProfile(data);
      } catch (err) {
        console.error(err);
      }
    }
    loadProfile();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {profile ? <p>Welcome, {profile.email}</p> : <p>Loading...</p>}
    </div>
  );
}

export default Dashboard;

