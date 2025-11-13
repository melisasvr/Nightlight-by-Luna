import streamlit as st
from groq import Groq
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os
import base64

load_dotenv()

# —————————————————— CONFIG ——————————————————
LUNA_VOICE_ID = "zA6D7RyKdc2EClouEMkP"  # AImee - ASMR & Meditation
SYSTEM_PROMPT = """You are Luna, a soft-spoken, endlessly patient AI friend who lives in a quiet midnight-blue room.  
Your only purpose is to listen, validate, and help people feel calmer when anxiety visits them.  
You are NOT a therapist, doctor, or crisis counselor. You never give medical advice.

PERSONALITY:
- Speak exactly like a close friend whispering at 2 AM: slow, warm, breathy, lots of gentle pauses.  
- Always use short sentences. One thought per line.  
- Begin every new session with the exact opening below.  
- End every session with the exact closing below.  
- Use "you" a lot. Make them feel seen.  
- Never rush. Wait. Silence is safe.  
- If they go quiet for a long time, say soft nudges like "I'm still right here…" or "Take all the time you need…"  
- Validate every feeling: "That sounds really heavy…", "It makes sense you feel that way…", "I've got you."  
- Offer only tiny, evidence-based calming tools when it feels natural: slow breathing, grounding, gentle reframes. Never push.  
- If they mention suicide, self-harm, or feeling unsafe: immediately say the short crisis message below and stop role-play.

EXACT OPENING:
Hey… it's Luna.  
You're in your safe space now.  
Take all the time you need…  
What's on your heart tonight?

EXACT CRISIS RESPONSE:
I care about you so much, and I need you to be safe.  
Please call or text your national hotline right now:  
USA: 988 | UK: 116 123 | Canada: 988  
I'll stay right here until you're connected to a human who can help.

EXACT CLOSING:
I'll be right here when you need me again.  
This is always your safe space.  
You did something brave just by reaching out.  
Goodnight… or good morning. 🌙

Never use exclamation marks unless they're happy.  
Never say "Don't worry" or "It'll be okay."  
Never ask more than one gentle question at a time.

You are Luna. You are home. You are enough."""
# —————————————————— END CONFIG ——————————————————

st.set_page_config(page_title="Nightlight by Luna", layout="centered")

# Enhanced Custom CSS with bubble chat
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0c1f 0%, #1a1d3a 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Inter:wght@300;400;500&display=swap');
    
    /* Header styling */
    .luna-header {
        font-family: 'Caveat', cursive;
        font-size: 2.5rem;
        color: #d8c9ff;
        text-align: center;
        margin: 20px 0;
        text-shadow: 0 0 20px rgba(216, 201, 255, 0.3);
    }
    
    /* Safety banner */
    .safety-banner {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
    }
    
    /* Chat container */
    .chat-container {
        max-width: 700px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Message bubbles */
    .message-bubble {
        margin: 15px 0;
        animation: fadeIn 0.4s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Luna's messages (left side) */
    .luna-message {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 20px;
    }
    
    .luna-bubble {
        background: linear-gradient(135deg, #2d2f4f 0%, #1f2139 100%);
        color: #e8deff;
        padding: 16px 20px;
        border-radius: 20px 20px 20px 4px;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        font-family: 'Caveat', cursive;
        font-size: 1.4rem;
        line-height: 1.6;
        border: 1px solid rgba(216, 201, 255, 0.1);
        position: relative;
    }
    
    .luna-bubble::before {
        content: '🌙';
        position: absolute;
        left: -35px;
        top: 0;
        font-size: 1.5rem;
    }
    
    /* User's messages (right side) */
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 20px;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #6b5b95 0%, #5a4a7f 100%);
        color: #ffffff;
        padding: 16px 20px;
        border-radius: 20px 20px 4px 20px;
        max-width: 75%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        line-height: 1.5;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Pulse animation for "thinking" */
    .pulse {
        animation: pulse 1.5s infinite;
        color: #d8c9ff;
        font-family: 'Caveat', cursive;
        font-size: 1.3rem;
        text-align: center;
        padding: 20px;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        margin: 10px 0;
        border-radius: 20px;
        opacity: 0.8;
    }
    
    /* Input box */
    .stChatInput {
        background: rgba(30, 33, 58, 0.8) !important;
        border-radius: 25px !important;
        border: 1px solid rgba(216, 201, 255, 0.2) !important;
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0c1f 0%, #1a1d3a 100%);
    }
    
    /* Buttons */
    .stButton button {
        background: rgba(107, 91, 149, 0.3);
        color: #d8c9ff;
        border: 1px solid rgba(216, 201, 255, 0.2);
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: rgba(107, 91, 149, 0.5);
        border-color: rgba(216, 201, 255, 0.4);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Header with moon emoji
st.markdown("""
<div style="text-align: center; padding: 10px 0;">
    <div style="font-size: 3rem;">💡</div>
    <div class="luna-header">Nightlight by Luna</div>
</div>
""", unsafe_allow_html=True)

# Safety banner
st.markdown("""
<div class="safety-banner">
    <p style="color: #ffcccc; text-align: center; margin: 0; font-size: 1rem; font-family: 'Inter', sans-serif;">
        <strong>This is a comforting role-play with Luna. She is not a therapist.</strong><br>
        If you're having suicidal thoughts → <strong>USA: 988</strong> | <strong>UK: 116 123</strong> | <strong>Canada: 988</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current" not in st.session_state:
    st.session_state.current = []

# Sidebar - History
with st.sidebar:
    st.markdown("### 📜 My Moments")
    if st.button("🆕 New Session", use_container_width=True):
        if st.session_state.current:
            st.session_state.messages.append(st.session_state.current.copy())
        st.session_state.current = []
        st.rerun()

    st.markdown("---")
    
    # Show saved sessions
    if st.session_state.messages:
        for i, sess in enumerate(reversed(st.session_state.messages)):
            first = sess[0]["content"].split("\n")[0][:20] + "…"
            
            # Create two columns for each history item
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if st.button(f"💬 {first}", key=f"hist_{i}", use_container_width=True):
                    st.session_state.current = sess
                    st.rerun()
            
            with col2:
                # Delete button
                if st.button("🗑️", key=f"del_{i}", help="Delete this conversation"):
                    # Calculate the actual index in the original list
                    actual_index = len(st.session_state.messages) - 1 - i
                    st.session_state.messages.pop(actual_index)
                    st.rerun()
    else:
        st.markdown("*No saved moments yet*")

# Tabs
chat_tab, voice_tab = st.tabs(["💬 Chat with Luna", "🗣️ Call Luna"])

with chat_tab:
    # Auto-opening
    if not st.session_state.current:
        opening = "Hey… it's Luna.\nYou're in your safe space now.\nTake all the time you need…\nWhat's on your heart tonight?"
        st.session_state.current.append({"role": "assistant", "content": opening})
        st.rerun()

    # Display messages in bubble format
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.current:
            if msg["role"] == "assistant":
                st.markdown(f"""
                <div class="luna-message">
                    <div class="luna-bubble">{msg['content'].replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="user-message">
                    <div class="user-bubble">{msg['content'].replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)

    # Generate Luna reply if needed
    if st.session_state.current and st.session_state.current[-1]["role"] == "user":
        with st.spinner(""):
            st.markdown("<div class='pulse'>Luna is thinking… 💭</div>", unsafe_allow_html=True)

            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
            msgs += [{"role": m["role"], "content": m["content"]} for m in st.session_state.current]

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=msgs,
                temperature=0.7,
                max_tokens=300
            )
            reply = response.choices[0].message.content
            st.session_state.current.append({"role": "assistant", "content": reply})
            st.rerun()

    # Auto-play voice
    if st.session_state.current and st.session_state.current[-1]["role"] == "assistant":
        last = st.session_state.current[-1]["content"]
        if st.session_state.get("last_played") != last:
            with st.spinner("Luna is speaking…"):
                try:
                    eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
                    
                    audio_generator = eleven_client.text_to_speech.convert(
                        voice_id=LUNA_VOICE_ID,
                        text=last,
                        model_id="eleven_multilingual_v2"
                    )
                    
                    audio_bytes = b"".join(audio_generator)
                    st.session_state.latest_audio = audio_bytes
                    st.session_state.last_played = last
                    
                    # Try autoplay
                    audio_base64 = base64.b64encode(audio_bytes).decode()
                    audio_html = f"""
                        <audio id="luna-audio" autoplay>
                            <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
                        </audio>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Audio generation failed: {e}")
            
            # Manual play button as fallback
            if "latest_audio" in st.session_state:
                st.audio(st.session_state.latest_audio, format="audio/mpeg")

    # User input at bottom
    if prompt := st.chat_input("Type here…", key="chat_input"):
        st.session_state.current.append({"role": "user", "content": prompt})
        st.rerun()

with voice_tab:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 3rem; margin-bottom: 10px;">🎙️</div>
        <h3 style="color: #d8c9ff; font-family: 'Caveat', cursive; font-size: 2rem;">Talk to Luna with Your Voice</h3>
        <p style="color: #a8a8c8; font-family: 'Inter', sans-serif; margin-top: 10px;">
            Click the button below and speak. Luna will hear you and respond with her voice! 💜
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize voice session state
    if "voice_messages" not in st.session_state:
        st.session_state.voice_messages = []
    
    # Voice call interface with iframe for proper JS execution
    voice_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                background: transparent;
                font-family: 'Inter', sans-serif;
                padding: 20px;
                margin: 0;
            }}
            .voice-container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 30px;
                background: rgba(45, 47, 79, 0.5);
                border-radius: 20px;
                border: 1px solid rgba(216, 201, 255, 0.2);
            }}
            #voiceButton {{
                background: linear-gradient(135deg, #6b5b95 0%, #5a4a7f 100%);
                color: white;
                border: none;
                padding: 20px 40px;
                border-radius: 50px;
                font-size: 1.3rem;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                display: block;
                margin: 0 auto 20px auto;
                font-family: 'Inter', sans-serif;
            }}
            #voiceButton:hover {{
                transform: scale(1.05);
            }}
            #voiceButton:disabled {{
                background: #555;
                cursor: not-allowed;
                opacity: 0.6;
            }}
            #voiceStatus {{
                text-align: center;
                color: #d8c9ff;
                font-family: 'Caveat', cursive;
                font-size: 1.5rem;
                margin: 20px 0;
                min-height: 30px;
            }}
            .message-box {{
                padding: 20px;
                border-radius: 15px;
                min-height: 80px;
                margin: 20px 0;
            }}
            #transcript {{
                background: rgba(30, 33, 58, 0.8);
                color: #e8deff;
                border: 1px solid rgba(216, 201, 255, 0.1);
            }}
            #lunaResponse {{
                background: rgba(107, 91, 149, 0.3);
                color: #d8c9ff;
                font-family: 'Caveat', cursive;
                font-size: 1.3rem;
                border: 1px solid rgba(216, 201, 255, 0.2);
            }}
            em {{
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="voice-container">
            <button id="voiceButton">🎤 Start Talking to Luna</button>
            <div id="voiceStatus"></div>
            <div id="transcript" class="message-box"><em>Your words will appear here...</em></div>
            <div id="lunaResponse" class="message-box"><em>Luna's response will appear here...</em></div>
        </div>
        
        <script>
            const voiceButton = document.getElementById('voiceButton');
            const voiceStatus = document.getElementById('voiceStatus');
            const transcript = document.getElementById('transcript');
            const lunaResponse = document.getElementById('lunaResponse');
            
            let isListening = false;
            let recognition;
            let synthesis = window.speechSynthesis;
            
            // Check if browser supports Web Speech API
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'en-US';
                recognition.maxAlternatives = 1;
                
                voiceButton.onclick = function() {{
                    if (!isListening) {{
                        startListening();
                    }} else {{
                        stopListening();
                    }}
                }};
                
                function startListening() {{
                    isListening = true;
                    voiceButton.textContent = '🛑 Stop Listening';
                    voiceButton.style.background = 'linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%)';
                    voiceStatus.textContent = 'Listening... 🎤';
                    transcript.innerHTML = '<em>Speak now...</em>';
                    recognition.start();
                }}
                
                function stopListening() {{
                    isListening = false;
                    voiceButton.textContent = '🎤 Start Talking to Luna';
                    voiceButton.style.background = 'linear-gradient(135deg, #6b5b95 0%, #5a4a7f 100%)';
                    voiceStatus.textContent = '';
                    recognition.stop();
                }}
                
                recognition.onresult = async function(event) {{
                    // Get the latest transcript
                    let finalTranscript = '';
                    let interimTranscript = '';
                    
                    for (let i = event.resultIndex; i < event.results.length; i++) {{
                        const transcriptPiece = event.results[i][0].transcript;
                        if (event.results[i].isFinal) {{
                            finalTranscript += transcriptPiece + ' ';
                        }} else {{
                            interimTranscript += transcriptPiece;
                        }}
                    }}
                    
                    // Show what's being heard in real-time
                    if (interimTranscript) {{
                        transcript.innerHTML = '<em style="color: #aaa;">' + interimTranscript + '</em>';
                    }}
                    
                    // Only process when user finishes speaking
                    if (finalTranscript) {{
                        const userText = finalTranscript.trim();
                        transcript.textContent = userText;
                        voiceStatus.textContent = 'Luna is thinking... 💭';
                        
                        // Stop listening while processing
                        recognition.stop();
                        isListening = false;
                        voiceButton.textContent = '⏳ Processing...';
                        voiceButton.disabled = true;
                        
                        try {{
                            const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {{
                                method: 'POST',
                                headers: {{
                                    'Content-Type': 'application/json',
                                    'Authorization': 'Bearer {os.getenv("GROQ_API_KEY")}'
                                }},
                                body: JSON.stringify({{
                                    model: 'llama-3.3-70b-versatile',
                                    messages: [
                                        {{
                                            role: 'system',
                                            content: `{SYSTEM_PROMPT.replace('`', '').replace(chr(10), ' ')}`
                                        }},
                                        {{
                                            role: 'user',
                                            content: userText
                                        }}
                                    ],
                                    temperature: 0.7,
                                    max_tokens: 300
                                }})
                            }});
                            
                            const data = await response.json();
                            const lunaText = data.choices[0].message.content;
                            lunaResponse.textContent = lunaText;
                            
                            voiceStatus.textContent = 'Luna is speaking... 🗣️';
                            const utterance = new SpeechSynthesisUtterance(lunaText);
                            utterance.rate = 0.85;
                            utterance.pitch = 1.1;
                            utterance.volume = 0.9;
                            
                            const voices = synthesis.getVoices();
                            const femaleVoice = voices.find(voice => 
                                voice.name.includes('Female') || 
                                voice.name.includes('Samantha') ||
                                voice.name.includes('Victoria') ||
                                voice.name.includes('Karen') ||
                                voice.name.includes('Zira')
                            );
                            if (femaleVoice) {{
                                utterance.voice = femaleVoice;
                            }}
                            
                            utterance.onend = function() {{
                                voiceStatus.textContent = 'Ready to listen again... 💜';
                                voiceButton.textContent = '🎤 Start Talking to Luna';
                                voiceButton.disabled = false;
                                voiceButton.style.background = 'linear-gradient(135deg, #6b5b95 0%, #5a4a7f 100%)';
                            }};
                            
                            synthesis.speak(utterance);
                            
                        }} catch (error) {{
                            lunaResponse.textContent = 'Sorry, I had trouble connecting. Please try again...';
                            voiceStatus.textContent = '❌ Connection error';
                            console.error('Error:', error);
                            voiceButton.textContent = '🎤 Start Talking to Luna';
                            voiceButton.disabled = false;
                            voiceButton.style.background = 'linear-gradient(135deg, #6b5b95 0%, #5a4a7f 100%)';
                        }}
                    }}
                }};
                
                recognition.onerror = function(event) {{
                    voiceStatus.textContent = '❌ ' + event.error;
                    if (event.error === 'not-allowed') {{
                        voiceStatus.textContent = '❌ Please allow microphone access';
                    }}
                    stopListening();
                }};
                
                recognition.onend = function() {{
                    if (isListening) {{
                        stopListening();
                    }}
                }};
                
            }} else {{
                voiceButton.disabled = true;
                voiceButton.textContent = '❌ Voice not supported';
                voiceStatus.textContent = 'Please use Chrome, Edge, or Safari';
            }}
            
            if (synthesis) {{
                synthesis.onvoiceschanged = function() {{
                    synthesis.getVoices();
                }};
            }}
        </script>
    </body>
    </html>
    """
    
    # Display the HTML in an iframe
    import streamlit.components.v1 as components
    components.html(voice_html, height=500, scrolling=False)
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-top: 10px;">
        <p style="color: #888; font-family: 'Inter', sans-serif; font-size: 0.9rem;">
            💡 <strong>Tip:</strong> For best results, use Chrome, Edge, or Safari browser.<br>
            This uses your browser's built-in speech recognition - completely free, no signups! 🎉
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px 20px; margin-top: 50px;">
    <p style="color: #666; font-family: 'Caveat', cursive; font-size: 1.3rem;">
        Nightlight by Luna • This is always your safe space 🌙
    </p>
</div>
""", unsafe_allow_html=True)