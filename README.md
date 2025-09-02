
---

# 📘 Pocket Tutor AI

Pocket Tutor AI is an **AI-powered web tutoring platform** that helps learners create personalized flashcards, generate courses, and earn certificates of completion. It combines **Hugging Face AI models**, **Supabase authentication & database**, and **secure payment integration** to deliver a modern, affordable, and gamified learning experience.

---

## 🚀 Features

* 🔑 **Authentication** (Supabase): Email/Password + OAuth (Google, GitHub, Apple)
* 🤖 **AI-Powered Flashcards & Courses** (Hugging Face API)
* 🎓 **Certificates** generated after completing courses
* 💳 **Payment Integration** (\$10/month subscription for unlimited access)
* 📱 **Responsive Frontend** (React + TailwindCSS)
* 🔄 **Forgot Password & Account Management** with Supabase
* 🎯 **Gamified Dashboard** with enrolled courses and progress tracking

---

## 🏗️ Tech Stack

* **Frontend**: React + TailwindCSS
* **Backend & Auth**: Supabase (Postgres + Auth API)
* **AI Services**: Hugging Face Inference API
* **Payments**: Stripe (can be swapped with M-Pesa for Kenya users)
* **Deployment**: Vercel / Netlify (Frontend) + Supabase Cloud

---

## 📂 Project Structure

```
pocket-tutor-ai/
│── public/             # Static assets
│── src/
│   ├── components/     # UI components
│   ├── pages/          # Main pages (Home, Dashboard, Login, Signup)
│   ├── services/       # API integrations (Supabase, Hugging Face, Stripe)
│   ├── utils/          # Helper functions
│   ├── App.js          # Main app entry
│   └── index.js        # React entry point
│── .env.example        # Environment variables
│── package.json
│── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pocket-tutor-ai.git
cd pocket-tutor-ai
```

### 2️⃣ Install Dependencies

```bash
npm install
```

### 3️⃣ Configure Environment Variables

Create a `.env` file with the following:

```bash
REACT_APP_SUPABASE_URL=your_supabase_project_url
REACT_APP_SUPABASE_KEY=your_supabase_anon_key
REACT_APP_HF_API_KEY=your_huggingface_api_key
REACT_APP_STRIPE_KEY=your_stripe_publishable_key
```

### 4️⃣ Run Development Server

```bash
npm run dev
```

### 5️⃣ Build for Production

```bash
npm run build
```

---

## 🔑 Authentication

* Users can sign up with **Email/Password** or **Google/GitHub/Apple**.
* Supabase handles **secure JWT tokens** and session management.
* Includes **Forgot Password** and **Email Verification** flows.

---

## 💳 Payments

* Default integration: **Stripe Checkout** (\$10/month).
* Can be adapted for **M-Pesa** or other local payment gateways.
* Subscription unlocks **unlimited AI flashcards & courses**.

---

## 📚 Roadmap (Web Version Only)

* [ ] Improve dashboard UI
* [ ] Add certificate download feature
* [ ] Expand AI course generation with more subjects
* [ ] Enable dark mode customization

---

## 👥 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🌍 About

Pocket Tutor AI is built to empower learners everywhere with **affordable, personalized, AI-driven education**.

---
