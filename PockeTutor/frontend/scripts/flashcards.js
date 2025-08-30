document.addEventListener("DOMContentLoaded", ()=>{
  const gen = document.getElementById("genFcBtn");
  if(!gen) return;
  gen.onclick = async ()=>{
    const user = JSON.parse(localStorage.getItem("pt_user"));
    const title = document.getElementById("fcTitle").value.trim() || "My Flashcards";
    const text = document.getElementById("fcText").value.trim();
    const file = document.getElementById("fcFile").files[0];
    try{
      // For simplicity, only text route here (file upload route can be added later)
      const data = await api("/api/flashcards/from-text","POST",{user_id:user.id, title, text});
      renderFlashcards(data);
    }catch(e){ toast(e.message); }
  };

  document.getElementById("downloadPDF").onclick = ()=> toast("TODO: implement PDF export");
  document.getElementById("downloadPNG").onclick = ()=> toast("TODO: implement PNG export");
  document.getElementById("downloadJPEG").onclick = ()=> toast("TODO: implement JPEG export");
});

function renderFlashcards(data){
  document.getElementById("fcSummary").textContent = data.summary || "";
  const wrap = document.getElementById("fcCards");
  wrap.innerHTML = data.flashcards.map(c=>`
    <div class="flip-wrap">
      <div class="panel card" onclick="this.classList.toggle('flip')">
        <div class="face">
          <div class="small">QUESTION</div>
          <h4>${c.q}</h4>
        </div>
        <div class="face back">
          <div class="small">ANSWER</div>
          <p>${c.a}</p>
        </div>
      </div>
    </div>
  `).join("");

  // Links & videos placeholder
  document.getElementById("fcLinks").innerHTML = `<div class="small">References: <a class="link" href="https://www.w3schools.com" target="_blank">W3Schools</a></div>`;
  document.getElementById("fcVideos").innerHTML = `<div class="small">Videos: (embed YouTube results later)</div>`;
}
// frontend/scripts/flashcards.js (add)
async function downloadFlashcardsPNG() {
  const el = document.getElementById("fcCards");
  if (!el) return alert("No cards");
  const canvas = await html2canvas(el, {backgroundColor: null, scale: 2});
  const dataUrl = canvas.toDataURL("image/png");
  const a = document.createElement("a");
  a.href = dataUrl;
  a.download = "flashcards.png";
  a.click();
}
document.getElementById("downloadPNG").addEventListener("click", downloadFlashcardsPNG);
