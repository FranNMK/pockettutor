// Frontend/src/api.js

// Base URL of your backend API
const API_BASE = "http://127.0.0.1:5000/api";  // change if needed

// Generic function to make authenticated requests
export async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem("pt_token");

  const headers = {
    "Content-Type": "application/json",
    ...(token ? { "Authorization": `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
