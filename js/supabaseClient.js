// scripts/supabaseClient.js
import { createClient } from "https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm";

// 🔑 Replace these with your actual Supabase project values
const SUPABASE_URL = "https://yzpfwftrgvqexkkegpbo.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl6cGZ3ZnRyZ3ZxZXhra2VncGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTY3MzA4MzMsImV4cCI6MjA3MjMwNjgzM30.GohDsDqwLR3EDjzdZYGtI0PUSuD4EqXQwG6UenAaAC8";

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
