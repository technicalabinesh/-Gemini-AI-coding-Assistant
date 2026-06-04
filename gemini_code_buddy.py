"""
Gemini AI Code Buddy — A Streamlit-based coding assistant powered by Google Gemini.
Install dependencies: pip install streamlit google-generativeai
Run: streamlit run gemini_code_buddy.py
"""

import streamlit as st
import google.generativeai as genai
import re

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gemini Code Buddy",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #0d0d14;
    --surface:   #13131e;
    --border:    #1e1e30;
    --accent:    #6ee7f7;
    --accent2:   #a78bfa;
    --green:     #4ade80;
    --red:       #f87171;
    --yellow:    #fbbf24;
    --text:      #e2e8f0;
    --muted:     #6b7280;
    --radius:    12px;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp { background-color: var(--bg); }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--accent);
}

/* ── Sidebar inputs ── */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] select {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: var(--radius);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    transition: all 0.2s ease;
    padding: 0.5rem 1.2rem;
}
.stButton > button:hover {
    background: var(--accent);
    color: var(--bg);
    box-shadow: 0 0 20px rgba(110, 231, 247, 0.3);
    transform: translateY(-1px);
}

/* ── Primary button (Send) ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: var(--bg);
    border: none;
    font-weight: 700;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 30px rgba(110, 231, 247, 0.5);
    transform: translateY(-2px);
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-bottom: 0.75rem !important;
    padding: 1rem !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: var(--radius) !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(110, 231, 247, 0.15) !important;
}

/* ── Text area (code input) ── */
.stTextArea textarea {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
    border-radius: var(--radius) !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(110, 231, 247, 0.15) !important;
}

/* ── Code blocks ── */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: #0a0a14 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0.25rem;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    border-radius: 8px 8px 0 0 !important;
    border: 1px solid transparent !important;
    transition: all 0.2s;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--accent) !important;
    border-color: var(--border) var(--border) var(--bg) !important;
    background: var(--surface) !important;
}

/* ── Info / success / error boxes ── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
}
[data-testid="stMetricValue"] { color: var(--accent) !important; font-family: 'JetBrains Mono', monospace !important; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    display:flex;
    align-items:center;
    gap:1rem;
    padding:1.5rem 0 1rem;
    border-bottom:1px solid #1e1e30;
    margin-bottom:1.5rem;
">
    <div style="
        width:48px; height:48px;
        background:linear-gradient(135deg,#6ee7f7,#a78bfa);
        border-radius:12px;
        display:flex; align-items:center; justify-content:center;
        font-size:1.5rem;
        flex-shrink:0;
    ">⚡</div>
    <div>
        <h1 style="margin:0;font-size:1.6rem;font-weight:800;
                   background:linear-gradient(90deg,#6ee7f7,#a78bfa);
                   -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            Gemini Code Buddy
        </h1>
        <p style="margin:0;color:#6b7280;font-size:0.8rem;font-family:'JetBrains Mono',monospace;">
            Powered by Google Gemini  •  Your AI pair programmer
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    api_key = st.text_input(
        "🔑 Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get yours free at https://aistudio.google.com/app/apikey",
    )

    model_choice = st.selectbox(
        "🤖 Model",
        options=[
            "models/gemma-4-31b-it",
            
        ],
        index=0,
    )

    temperature = st.slider("🌡️ Creativity", min_value=0.0, max_value=1.0, value=0.3, step=0.05)

    st.markdown("---")
    st.markdown("### 🧰 Tools")

    mode = st.selectbox(
        "Mode",
        options=[
            "💬 Chat Assistant",
            "🐛 Debug Code",
            "✨ Explain Code",
            "🔄 Refactor Code",
            "🧪 Generate Tests",
            "📝 Document Code",
        ],
    )

    st.markdown("---")
    st.markdown("### 💬 Language")
    lang = st.selectbox(
        "Code language",
        ["Auto-detect", "Python", "JavaScript", "TypeScript", "Go", "Rust",
         "Java", "C++", "C#", "SQL", "Bash", "Ruby", "Swift", "Kotlin"],
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div style='margin-top:2rem;padding:1rem;background:#0d0d14;border-radius:10px;
                border:1px solid #1e1e30;font-size:0.75rem;color:#6b7280;'>
        <b style='color:#6ee7f7;'>Tip:</b> Paste your code in the chat or use a dedicated tool tab for richer analysis.
    </div>
    """, unsafe_allow_html=True)

# ─── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── Gemini helpers ───────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Gemini Code Buddy, an expert AI coding assistant.
- Provide clear, concise, working code.
- Always use proper syntax highlighting in Markdown code blocks.
- Explain *why*, not just *what*.
- Point out potential bugs, edge-cases, or performance concerns.
- Be friendly but precise.
"""

MODE_PROMPTS = {
    "💬 Chat Assistant":  SYSTEM_PROMPT,
    "🐛 Debug Code":      SYSTEM_PROMPT + "\nFocus on identifying and fixing bugs. List each bug, explain the cause, and provide the corrected code.",
    "✨ Explain Code":     SYSTEM_PROMPT + "\nExplain the provided code step-by-step in plain English. Use numbered points.",
    "🔄 Refactor Code":   SYSTEM_PROMPT + "\nRefactor the provided code for clarity, performance, and best practices. Show a before/after diff.",
    "🧪 Generate Tests":  SYSTEM_PROMPT + "\nGenerate comprehensive unit tests for the provided code. Use the appropriate testing framework for the language.",
    "📝 Document Code":   SYSTEM_PROMPT + "\nAdd thorough docstrings/comments to every function, class, and module in the code.",
}

def get_gemini_response(prompt: str, history: list, api_key: str, model: str, temp: float, mode: str):
    """Call Gemini and stream the response."""
    genai.configure(api_key=api_key)
    system = MODE_PROMPTS.get(mode, SYSTEM_PROMPT)
    
    # Build history for multi-turn
    chat_history = []
    for msg in history[:-1]:  # exclude the latest user message
        chat_history.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [msg["content"]],
        })

    gemini_model = genai.GenerativeModel(
        model_name=model,
        system_instruction=system,
        generation_config=genai.GenerationConfig(temperature=temp),
    )
    chat = gemini_model.start_chat(history=chat_history)
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        yield chunk.text


def extract_code_blocks(text: str) -> list[dict]:
    """Extract fenced code blocks from markdown text."""
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"lang": m[0] or "text", "code": m[1].strip()} for m in matches]


def count_tokens_approx(text: str) -> int:
    return len(text.split())

# ─── Main Content ─────────────────────────────────────────────────────────────
if not api_key:
    st.markdown("""
    <div style="
        background:#13131e;
        border:1px dashed #6ee7f7;
        border-radius:14px;
        padding:2.5rem;
        text-align:center;
        margin:2rem auto;
        max-width:520px;
    ">
        <div style="font-size:3rem;margin-bottom:0.75rem;">🔑</div>
        <h3 style="color:#6ee7f7;margin-bottom:0.5rem;">Enter Your API Key</h3>
        <p style="color:#6b7280;font-size:0.9rem;margin-bottom:1rem;">
            Add your <b>Google Gemini API key</b> in the sidebar to get started.<br>
            It's free at <a href="https://aistudio.google.com/app/apikey" target="_blank"
                style="color:#a78bfa;">aistudio.google.com</a>
        </p>
        <code style="background:#0d0d14;padding:0.4rem 0.8rem;border-radius:6px;
                     font-size:0.8rem;color:#4ade80;">pip install streamlit google-generativeai</code>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Stats bar ───────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💬 Messages", len(st.session_state.messages))
with col2:
    st.metric("🤖 Model", model_choice.split("-")[1].capitalize())
with col3:
    st.metric("🌡️ Temp", f"{temperature:.2f}")
with col4:
    words = sum(count_tokens_approx(m["content"]) for m in st.session_state.messages)
    st.metric("📊 ~Tokens", f"{words:,}")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

# ─── Tool Tabs ────────────────────────────────────────────────────────────────
if mode != "💬 Chat Assistant":
    st.markdown(f"#### {mode}")
    code_input = st.text_area(
        "Paste your code here",
        height=220,
        placeholder="# Paste code here...",
        key="tool_code",
    )
    lang_hint = "" if lang == "Auto-detect" else f" The code is written in {lang}."

    if st.button(f"Run {mode}", type="primary"):
        if not code_input.strip():
            st.warning("Please paste some code first.")
        else:
            action_map = {
                "🐛 Debug Code":    "Debug the following code and fix all bugs:",
                "✨ Explain Code":  "Explain the following code clearly:",
                "🔄 Refactor Code": "Refactor the following code:",
                "🧪 Generate Tests":"Generate unit tests for the following code:",
                "📝 Document Code": "Add documentation/docstrings to the following code:",
            }
            prompt = f"{action_map[mode]}{lang_hint}\n\n```\n{code_input}\n```"
            st.session_state.messages.append({"role": "user", "content": prompt})

    st.markdown("---")

# ─── Chat history ─────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "⚡"):
        st.markdown(msg["content"])

# ─── Chat input & response ────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything about code…  e.g. 'Write a FastAPI CRUD app'")

if user_input or (
    st.session_state.messages
    and st.session_state.messages[-1]["role"] == "user"
    and len(st.session_state.messages) % 2 != 0
):
    # New message from chat input
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

    last = st.session_state.messages[-1]
    if last["role"] == "user":
        with st.chat_message("assistant", avatar="⚡"):
            with st.spinner("Thinking…"):
                response_placeholder = st.empty()
                full_response = ""
                try:
                    for chunk in get_gemini_response(
                        last["content"],
                        st.session_state.messages,
                        api_key,
                        model_choice,
                        temperature,
                        mode,
                    ):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")

                    response_placeholder.markdown(full_response)

                    # If there are code blocks, offer a copy hint
                    blocks = extract_code_blocks(full_response)
                    if blocks:
                        st.markdown(
                            f"<p style='color:#6b7280;font-size:0.75rem;font-family:JetBrains Mono,monospace;'>"
                            f"↑ {len(blocks)} code block(s) detected — hover to copy</p>",
                            unsafe_allow_html=True,
                        )

                    st.session_state.messages.append(
                        {"role": "assistant", "content": full_response}
                    )

                except Exception as e:
                    err = str(e)
                    if "API_KEY" in err.upper() or "401" in err or "403" in err:
                        st.error("❌ Invalid API key. Please check your key in the sidebar.")
                    elif "quota" in err.lower():
                        st.error("⚠️ Quota exceeded. Check your Gemini usage limits.")
                    elif "not found" in err.lower():
                        st.error(f"🤖 Model `{model_choice}` not available with your API key.")
                    else:
                        st.error(f"Something went wrong: {err}")
