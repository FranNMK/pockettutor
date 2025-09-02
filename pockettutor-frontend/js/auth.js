import { supabase } from "./supabaseClient.js";
import { showToast } from "./utils.js";

// LOGIN
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  const { data, error } = await supabase.auth.signInWithPassword({ email, password });

  if (error) {
    showToast(error.message, "error");
  } else {
    showToast("Login successful!", "success");
    console.log("User:", data.user);
    // Redirect to dashboard.html
    window.location.href = "dashboard.html";
  }
});

// SIGNUP
document.getElementById("signup-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;

  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: document.getElementById("signup-name").value,
        country: document.getElementById("signup-country").value,
      },
    },
  });

  if (error) {
    showToast(error.message, "error");
  } else {
    showToast("Signup successful! Check your email to confirm.", "success");
  }
});

// FORGOT PASSWORD
document.getElementById("forgot-password").addEventListener("click", async (e) => {
  e.preventDefault();
  const email = document.getElementById("login-email").value;
  if (!email) {
    return showToast("Enter your email first", "error");
  }

  const { error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: "https://your-site.com/reset-password.html",
  });

  if (error) {
    showToast(error.message, "error");
  } else {
    showToast("Password reset email sent!", "success");
  }
});
