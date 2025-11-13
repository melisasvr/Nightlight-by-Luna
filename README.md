# Nightlight by Luna 🌙✨
A soothing AI anxiety hotline that feels like a late-night whisper 🤫 from a friend  
**Luna** listens, validates, and gently calms you anytime you need. 🤗

## Features 🔑
- **Text Chat**💬: WhatsApp-style bubbles with auto-playing soft voice 🗣️
- **Voice Call (Browser)** 📞: Click "Call Luna" → speak → she answers live (100% free!) 🆓 
- **Session History** 📜:  Save, revisit, or delete your moments 🗑️
- **Safety First** 🛡️🚨: Crisis hotlines + clear disclaimer  
- **Midnight Magic Theme**🌌🎨: Gradient blues, Caveat font, moon emoji, pulsing glow  

## Prerequisites 🛠️
- Python 3.10+ 🐍
- **Groq API key** (free → https://console.groq.com) ⚡🔑
- **ElevenLabs API key** (free tier → https://elevenlabs.io) 🗣️🔑

## Installation ⚙️
1. **Download** the project folder ⬇️
2. Open a terminal inside the folder 💻
3. Create a virtual environment 🧑‍💻 
   ```
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```
4. Install packages
- `pip install streamlit groq elevenlabs python-dotenv`
5. Create .env file (your secrets! 🤫)
 ```
- GROQ_API_KEY=your_groq_key_here
- ELEVENLABS_API_KEY=your_elevenlabs_key_here
```

## How to Run
- Run:
- `streamlit run streamlit_app.py`

- → Opens in browser. → Luna is waiting. 💖

## How to Use:
- Chat Tab ⌨️ → Type anything → Luna replies with text + soft voice. 🔊
- Call Tab 🎙️ → Click "Start Talking to Luna" → allow mic → speak! (Note: Voice sounds a bit robotic in calls using browser TTS. That's okay for now!)

## Privacy & Safety 🔒
- All processing happens locally + API calls only.
- No data stored. 🚫💾
- Luna is not a therapist for crisis:
- USA: 988 🇺🇸 | UK: 116 123 🇬🇧 | Canada: 988 🇨🇦

## Credits & Closing Thoughts ❤️
- Built with love for anyone who needs a safe space at 2 AM. 🌃 Inspired by ASMR hotline videos (like this one: https://youtu.be/5C0y2IePMgs). You are not alone. Luna is here. Always. ✨

- "I'll be right here when you need me again. This is always your safe space. Goodnight… or good morning." 😴

## 🤝 Contribute!
- Want to help improve Nightlight? We welcome contributions! Check the repository for open issues or submit a pull request with your ideas for new features, bug fixes, or theme enhancements. Your help keeps the light on! 🌟
