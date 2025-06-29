 🤖 MAHI 1.0 – Personal AI Assistant

MAHI 1.0 is a futuristic Python-based AI assistant that responds via **voice and text**, generates **images** using Hugging Face, writes **essays/emails/letters**, and handles **automation tasks** — all in a slick graphical interface.

---

🌟 Features

- 🎙️ Voice + Chat interaction
- 🎨 Image generation (Hugging Face API – `prompthero/openjourney`)
- ✍️ Essay, Email, Letter writing using Groq
- 🧠 Intent Detection (via LLM + DMM engine)
- 📅 Reminders and scheduling
- 📈 System Monitoring (CPU, RAM, Battery, Internet)
- 🌦 Weather reporting via OpenWeather API
- 📸 Webcam AI (face detection using OpenCV)
- 🖼 GUI built in PyQt5 with animated themes

---

 🧠 Technologies Used

- Python 3.11+
- Hugging Face Inference API
- Groq (LLaMA/Mixtral writer)
- OpenAI/Cohere (intent classification)
- Edge TTS (Neural voice)
- OpenCV (face detection)
- PyQt5 (GUI)
- dotenv, requests, asyncio, PIL, pyttsx3

---

 🔧 Setup

1. Clone the repo
```bash
git clone https://github.com/tejassapra1/mahi-1.0.git
cd mahi-1.0
