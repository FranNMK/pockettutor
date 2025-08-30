document.addEventListener("DOMContentLoaded", ()=>{
  const genBtn = document.getElementById("genCourseBtn");
  const enrollBtn = document.getElementById("enrollBtn");
  const saveProgressBtn = document.getElementById("saveProgressBtn");

  if(genBtn) genBtn.onclick = async ()=>{
    const user = JSON.parse(localStorage.getItem("pt_user"));
    const topic = document.getElementById("topicInput").value.trim();
    if(!topic) return toast("Enter a topic");
    try{
      const res = await api("/api/courses/generate","POST",{user_id:user.id, topic});
      document.getElementById("courseOutline").innerHTML = `<div class="panel"><h4>${res.title}</h4><p class="small">Outline generated. Enroll to start.</p></div>`;
      enrollBtn.dataset.courseId = res.course_id;
      enrollBtn.style.display = "inline-block";
    }catch(e){ toast(e.message); }
  };

  if(enrollBtn) enrollBtn.onclick = async ()=>{
    const user = JSON.parse(localStorage.getItem("pt_user"));
    const cid = parseInt(enrollBtn.dataset.courseId,10);
    try{
      await api("/api/courses/enroll","POST",{user_id:user.id, course_id: cid});
      toast("Enrolled. Track progress below.");
      document.getElementById("progressWrap").style.display = "block";
    }catch(e){ toast(e.message); }
  };

  if(saveProgressBtn) saveProgressBtn.onclick = async ()=>{
    const user = JSON.parse(localStorage.getItem("pt_user"));
    const pct = parseInt(document.getElementById("progressRange").value,10);
    const enrollBtn = document.getElementById("enrollBtn");
    const cid = parseInt(enrollBtn.dataset.courseId,10);
    try{
      const res = await api("/api/progress/update","POST",{user_id:user.id, course_id:cid, percent:pct});
      document.getElementById("progressPct").textContent = `${res.progress}%`;
      if(res.progress >= 100){
        document.getElementById("certificateWrap").style.display = "block";
      }
    }catch(e){ toast(e.message); }
  };

  const certBtn = document.getElementById("genCertBtn");
  if(certBtn) certBtn.onclick = ()=> toast("TODO: call backend to generate & email certificate PDF");
});
