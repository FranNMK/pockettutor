document.addEventListener("DOMContentLoaded", ()=>{
  const gotoSignup = document.getElementById("gotoSignup");
  const gotoLogin = document.getElementById("gotoLogin");
  const signupPanel = document.getElementById("signupPanel");

  if(gotoSignup) gotoSignup.onclick = ()=> { window.scrollTo({top:0, behavior:"smooth"}); signupPanel.scrollIntoView({behavior:"smooth"}); };
  if(gotoLogin) gotoLogin.onclick = ()=> window.scrollTo({top:0, behavior:"smooth"});

  const sBtn = document.getElementById("signupBtn");
  if(sBtn) sBtn.onclick = async ()=>{
    const name = document.getElementById("sName").value.trim();
    const country = document.getElementById("sCountry").value.trim();
    const email = document.getElementById("sEmail").value.trim();
    const pass = document.getElementById("sPass").value;
    const robot = document.getElementById("robotChk").checked;
    if(!robot) return toast("Please confirm you're not a robot");
    try{
      const data = await api("/api/auth/signup", "POST", {name, country, email, password: pass});
      document.getElementById("signupMsg").textContent = "Check your email for verification link.";
      console.log("DEBUG verify link:", data.verify_link_debug);
    }catch(e){ toast(e.message); }
  };

  const lBtn = document.getElementById("loginBtn");
  if(lBtn) lBtn.onclick = async ()=>{
    const email = document.getElementById("loginEmail").value.trim();
    const pass = document.getElementById("loginPass").value;
    try{
      const data = await api("/api/auth/login","POST",{email,password:pass});
      localStorage.setItem("pt_user", JSON.stringify(data.user));
      window.location.href = "dashboard.html";
    }catch(e){ toast(e.message); }
  };
});
async function login(email, password) {
  const res = await fetch("http://127.0.0.1:5000/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (res.ok && data.access_token) {
    localStorage.setItem("pt_token", data.access_token); // save token
    return true;
  } else {
    throw new Error(data.message || "Login failed");
  }
}
