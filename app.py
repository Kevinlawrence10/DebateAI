# ============================================================
# DEBATEAI - CLEAN STREAMLIT APP
# ============================================================
# Install:
#   pip install streamlit requests faster-whisper SpeechRecognition
# Optional fallback:
#   pip install SpeechRecognition
#
# Ollama:
#   ollama pull llama3.2:3b
#   ollama serve
#
# Run:
#   streamlit run app.py
#
# Voice-to-text:
#   The first recording may take time because faster-whisper downloads
#   the selected model. Default model: base.en
#   You can use WHISPER_MODEL=tiny.en for a faster lightweight demo.
# ============================================================

import html
import io
import json
import os
import random
import textwrap
import hashlib
import tempfile

import requests
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DebateAI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# IMPORTANT:
# All custom HTML is passed through render_html(), which removes
# Python indentation before Streamlit receives the markdown.
# This prevents HTML from being displayed as a code block.
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #08090d;
    --panel: #111218;
    --panel-2: #151620;
    --border: #292b35;
    --muted: #858792;
    --text: #f5f5f7;
    --purple: #7c5cff;
    --blue: #4c8fff;
    --green: #55dfaa;
    --red: #ff8090;
}

* {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(124,92,255,.12), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(0,210,255,.08), transparent 30%),
        var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1250px;
    padding-top: 1.15rem;
    padding-bottom: 3rem;
}

#MainMenu,
footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ---------- Brand ---------- */

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}

.brand-icon {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #7c5cff, #3e8cff);
    font-size: 20px;
    box-shadow: 0 8px 30px rgba(124,92,255,.25);
}

.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
}

.brand-sub {
    font-size: 12px;
    color: #777985;
}

/* ---------- Hero ---------- */

.hero {
    text-align: center;
    padding: 35px 20px 25px;
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(38px, 5vw, 54px);
    line-height: 1.05;
    margin: 0;
    letter-spacing: -2px;
}

.hero h1 span {
    background: linear-gradient(90deg, #9b83ff, #55c7ff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.hero p {
    color: #92949f;
    font-size: 16px;
    margin-top: 16px;
}

/* ---------- Cards ---------- */

.card {
    background: rgba(19,20,27,.92);
    border: 1px solid #292b35;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0 15px 50px rgba(0,0,0,.16);
}

.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 17px;
    color: #f4f4f7;
}

.card-sub {
    color: #777985;
    font-size: 13px;
    margin-top: 4px;
}

/* ---------- Pills ---------- */

.pill {
    display: inline-flex;
    align-items: center;
    padding: 6px 11px;
    border-radius: 50px;
    font-size: 11px;
    line-height: 1;
    font-weight: 700;
    margin-right: 6px;
}

.pill-purple {
    background: rgba(124,92,255,.14);
    color: #a897ff;
}

.pill-green {
    background: rgba(50,210,140,.12);
    color: #55dfaa;
}

.pill-red {
    background: rgba(255,90,110,.12);
    color: #ff8090;
}

.pill-muted {
    background: #171820;
    color: #777985;
}

/* ---------- Topic ---------- */

.topic-box {
    background: linear-gradient(135deg, #14151d, #101117);
    border: 1px solid #2c2e39;
    border-radius: 18px;
    padding: 20px 22px;
    margin: 14px 0;
}

.topic-label {
    color: #858792;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.topic-text {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 21px;
    font-weight: 600;
    line-height: 1.35;
    margin-top: 6px;
}

/* ---------- Position cards ---------- */

.side-for {
    border: 1px solid rgba(50,210,140,.35);
    background: rgba(50,210,140,.06);
}

.side-against {
    border: 1px solid rgba(255,90,110,.35);
    background: rgba(255,90,110,.06);
}

/* ---------- Debate transcript ---------- */

.message {
    display: flex;
    gap: 13px;
    margin: 18px 0;
}

.avatar {
    min-width: 38px;
    width: 38px;
    height: 38px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
}

.avatar-you {
    background: #242631;
    color: #fff;
}

.avatar-ai {
    background: linear-gradient(135deg, #765aff, #438fff);
    color: #fff;
}

.message-body {
    flex: 1;
    min-width: 0;
}

.message-name {
    font-size: 12px;
    color: #858792;
    margin-bottom: 6px;
    letter-spacing: .3px;
}

.message-text {
    font-size: 15px;
    line-height: 1.65;
    color: #e7e7eb;
}

.ai-response {
    background: linear-gradient(135deg, rgba(124,92,255,.08), rgba(55,145,255,.04));
    border: 1px solid rgba(124,92,255,.22);
    border-radius: 17px;
    padding: 20px;
}

.ai-label {
    color: #9b8cff;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin-bottom: 7px;
}

.ai-label.blue {
    color: #68c6ff;
}

.soft-divider {
    height: 1px;
    background: #252730;
    margin: 18px 0;
}

/* ---------- Score ---------- */

.score-card {
    background: #111218;
    border: 1px solid #292b35;
    border-radius: 16px;
    padding: 17px 10px;
    text-align: center;
    min-height: 100px;
}

.score-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(135deg, #9d8aff, #50baff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.score-label {
    color: #777985;
    font-size: 11px;
    margin-top: 3px;
}

/* ---------- Progress ---------- */

.progress-wrap {
    height: 7px;
    background: #242630;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 14px;
}

.progress {
    height: 100%;
    background: linear-gradient(90deg, #7c5cff, #43a5ff);
    border-radius: 20px;
    transition: width .3s ease;
}

/* ---------- Report ---------- */

.report-score {
    text-align: center;
    padding: 34px;
    border-radius: 23px;
    background:
        radial-gradient(circle at center, rgba(124,92,255,.18), transparent 60%),
        #111218;
    border: 1px solid #2c2e39;
}

.big-score {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 72px;
    font-weight: 700;
    background: linear-gradient(135deg, #9d8aff, #50baff);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.report-section {
    background: #111218;
    border: 1px solid #292b35;
    border-radius: 18px;
    padding: 21px;
    margin-bottom: 14px;
}

.report-section h3 {
    margin-top: 0;
}

/* ---------- Inputs ---------- */

.stTextInput input,
.stTextArea textarea {
    background: #111218 !important;
    color: #f5f5f7 !important;
    border: 1px solid #2c2e39 !important;
    border-radius: 13px !important;
}

.stTextArea textarea {
    min-height: 135px;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #111218 !important;
    border-color: #2c2e39 !important;
}

/* ---------- Buttons ---------- */

.stButton > button {
    border-radius: 12px !important;
    border: 1px solid #30323d !important;
    background: #171820 !important;
    color: #eeeeef !important;
    font-weight: 600 !important;
    min-height: 44px !important;
    transition: .2s !important;
}

.stButton > button:hover {
    border-color: #806aff !important;
    background: #1b1c26 !important;
}

.primary-btn .stButton > button,
.stButton.primary-btn > button {
    background: linear-gradient(135deg, #765aff, #4c8fff) !important;
    border: none !important;
    color: white !important;
}

/* ---------- Misc ---------- */

.footer {
    text-align: center;
    color: #555762;
    font-size: 11px;
    padding: 28px 0 10px;
}

.status-box {
    border: 1px solid #2c2e39;
    background: #101117;
    border-radius: 13px;
    padding: 12px 14px;
    color: #9b9da7;
    font-size: 12px;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding-top: 20px;
    }

    .topic-text {
        font-size: 18px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SAFE HTML RENDERER
# ============================================================

def render_html(markup: str) -> None:
    """Render UI HTML directly so Streamlit Markdown never treats it as code."""
    cleaned = textwrap.dedent(markup).strip()

    # Streamlit's native HTML renderer does not run the Markdown parser,
    # so indented nested <div>/<span> elements cannot accidentally become
    # visible code blocks.
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        # Compatibility fallback for older Streamlit versions.
        # Remove leading whitespace from every line before Markdown parsing.
        flat = "\n".join(line.strip() for line in cleaned.splitlines())
        st.markdown(flat, unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {
    "screen": "setup",
    "topic": "",
    "topic_mode": None,
    "user_side": None,
    "ai_side": None,
    "round": 0,
    "max_rounds": 3,
    "history": [],
    "scores": [],
    "voice_text": "",
    "voice_status": "",
    "last_audio_hash": "",
    "argument_editor_version": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# DATA
# ============================================================

TOPICS = [
    "Should artificial intelligence be regulated?",
    "Should college attendance be mandatory?",
    "Should social media have an age limit?",
    "Should AI-generated content be labelled?",
    "Should space exploration receive more government funding?",
    "Should students be allowed to use AI for assignments?",
    "Should online education replace traditional classrooms?",
    "Should mobile phones be banned in classrooms?",
    "Should electric vehicles completely replace petrol vehicles?",
    "Should school students have less homework?",
]


# ============================================================
# BRAND
# ============================================================

def brand():
    render_html(
        """
        <div class="brand">
            <div class="brand-icon">⚡</div>
            <div>
                <div class="brand-name">DebateAI</div>
                <div class="brand-sub">Think sharper. Argue better.</div>
            </div>
        </div>
        """
    )


# ============================================================
# SPEECH TO TEXT - ROBUST VERSION
# ============================================================

def _audio_suffix(audio_file):
    """Choose a useful temporary-file extension from the browser MIME type."""
    mime = getattr(audio_file, "type", "") or ""
    if "webm" in mime:
        return ".webm"
    if "ogg" in mime:
        return ".ogg"
    if "mp4" in mime or "m4a" in mime:
        return ".m4a"
    return ".wav"


def transcribe_audio(audio_file):
    """
    Convert Streamlit's audio_input recording into text.

    Primary:
        faster-whisper using a real temporary audio file.

    Fallback:
        SpeechRecognition + Google speech recognition.

    IMPORTANT:
    faster-whisper is given a file path, not BytesIO. This avoids the
    common situation where the UI stays on "Transcribing..." because
    the Whisper decoder cannot open the browser-recorded bytes directly.
    """
    if audio_file is None:
        return ""

    audio_bytes = audio_file.getvalue()
    if not audio_bytes:
        st.session_state.voice_status = "No audio was captured."
        return ""

    temp_path = None

    # ------------------------------------------------------------
    # METHOD 1: faster-whisper
    # ------------------------------------------------------------
    try:
        from faster_whisper import WhisperModel

        if "whisper_model" not in st.session_state:
            model_name = os.getenv("WHISPER_MODEL", "base.en")
            compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
            device = os.getenv("WHISPER_DEVICE", "cpu")

            st.session_state.voice_status = (
                f"Loading speech model ({model_name}) for the first time..."
            )

            st.session_state.whisper_model = WhisperModel(
                model_name,
                device=device,
                compute_type=compute_type,
            )

        # Write the browser recording to a real file.
        suffix = _audio_suffix(audio_file)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:
            tmp.write(audio_bytes)
            tmp.flush()
            temp_path = tmp.name

        segments, info = st.session_state.whisper_model.transcribe(
            temp_path,
            beam_size=5,
            vad_filter=True,
            language="en",
            condition_on_previous_text=False,
        )

        transcript_parts = []

        for segment in segments:
            piece = segment.text.strip()
            if piece:
                transcript_parts.append(piece)

        transcript = " ".join(transcript_parts).strip()

        if transcript:
            st.session_state.voice_status = (
                f"Voice transcription completed • "
                f"{len(transcript.split())} words"
            )
            return transcript

        raise RuntimeError("Whisper returned no speech text.")

    except Exception as whisper_error:
        # Continue to the fallback recognizer.
        st.session_state.voice_status = (
            "Whisper could not transcribe the recording. "
            "Trying the backup speech recognizer..."
        )

    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                pass

    # ------------------------------------------------------------
    # METHOD 2: SpeechRecognition fallback
    # ------------------------------------------------------------
    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 250
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8

        # Streamlit audio_input normally produces WAV audio. Use the
        # original bytes directly for the fallback.
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)

        transcript = recognizer.recognize_google(
            audio_data,
            language="en-IN",
        ).strip()

        if transcript:
            st.session_state.voice_status = (
                f"Voice transcription completed • "
                f"{len(transcript.split())} words"
            )
            return transcript

        raise RuntimeError("Backup recognizer returned empty text.")

    except Exception as fallback_error:
        st.session_state.voice_status = (
            "Could not transcribe this recording. "
            "Make sure faster-whisper is installed and try recording "
            "again with clear speech."
        )
        return ""


# ============================================================
# BUILT-IN FALLBACK AI
# ============================================================

def mock_ai(argument):
    templates = [
        (
            "That argument assumes that the benefit automatically outweighs "
            "the potential risks. That connection needs stronger justification.",
            "A stronger position considers both the immediate benefit and the "
            "long-term consequences before reaching a conclusion.",
        ),
        (
            "Your point is reasonable, but it does not fully address the "
            "opposing concern. Explain why the alternative would be less effective.",
            "The issue requires stronger safeguards rather than accepting the "
            "change without conditions.",
        ),
        (
            "The main weakness is the jump from one observation to a broader "
            "conclusion. One example is not enough to establish a general rule.",
            "A convincing position should connect the claim to a clear reason "
            "and explain why that reasoning applies more broadly.",
        ),
    ]

    counter, ai_point = random.choice(templates)

    scores = {
        "response": random.randint(6, 9),
        "relevance": random.randint(7, 10),
        "reasoning": random.randint(6, 9),
        "evidence": random.randint(5, 8),
        "fairness": random.randint(7, 10),
    }

    fallacy_detected = random.choice([False, False, True])

    return {
        "counterargument": counter,
        "ai_point": ai_point,
        "scores": scores,
        "possible_fallacy": {
            "detected": fallacy_detected,
            "type": "Hasty Generalization" if fallacy_detected else "",
            "evidence": argument[:120] if fallacy_detected else "",
        },
        "coaching_note": (
            "Support your main claim with a specific example, fact, "
            "statistic, observation, or clear cause-and-effect explanation."
        ),
        "better_argument": (
            "Your claim can be strengthened by directly answering the "
            "opposing point, explaining the reasoning step by step, and "
            "adding a concrete example or verifiable evidence."
        ),
    }


# ============================================================
# OLLAMA AI
# ============================================================

def ollama_ai(argument):
    prompt = f"""
You are DebateAI, a professional debate opponent and debate coach.

DEBATE TOPIC:
{st.session_state.topic}

USER SIDE:
{st.session_state.user_side}

AI SIDE:
{st.session_state.ai_side}

ROUND:
{st.session_state.round + 1}

USER'S ARGUMENT:
{argument}

Your job is to debate against the user AND evaluate their argument.

You MUST stay on your assigned side.
Do NOT simply agree with the user.

First directly counter the user's argument.
Then give your own strong argument supporting your side.
Then evaluate the user's argument.

Return ONLY valid JSON using exactly this structure:

{{
    "counterargument": "Direct response to the user's argument.",
    "ai_point": "A strong argument supporting the AI's position.",
    "scores": {{
        "response": 0,
        "relevance": 0,
        "reasoning": 0,
        "evidence": 0,
        "fairness": 0
    }},
    "possible_fallacy": {{
        "detected": false,
        "type": "",
        "evidence": ""
    }},
    "coaching_note": "Specific advice for improving the user's argument.",
    "better_argument": "Rewrite the user's argument in a stronger way."
}}

Give every score from 0 to 10.

Do not invent statistics or facts.
If you detect a logical fallacy, mark it only as a POSSIBLE fallacy.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
            "format": "json",
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()
    result = json.loads(data["response"])

    required = {
        "counterargument",
        "ai_point",
        "scores",
        "possible_fallacy",
        "coaching_note",
        "better_argument",
    }

    if not required.issubset(result):
        raise ValueError("Ollama returned incomplete debate JSON.")

    # Normalize score values.
    for key in ["response", "relevance", "reasoning", "evidence", "fairness"]:
        result["scores"][key] = max(
            0,
            min(10, float(result["scores"].get(key, 0))),
        )

    return result


def get_ai_response(argument):
    try:
        return ollama_ai(argument)
    except Exception:
        return mock_ai(argument)


# ============================================================
# START / RESET
# ============================================================

def start_debate():
    if not st.session_state.topic.strip():
        st.error("Please choose or enter a topic.")
        return

    if not st.session_state.user_side:
        st.error("Please choose FOR or AGAINST.")
        return

    st.session_state.ai_side = (
        "AGAINST"
        if st.session_state.user_side == "FOR"
        else "FOR"
    )

    st.session_state.round = 0
    st.session_state.history = []
    st.session_state.scores = []
    st.session_state.voice_text = ""
    st.session_state.voice_status = ""
    st.session_state.last_audio_hash = ""
    st.session_state.argument_editor_version += 1
    st.session_state.screen = "debate"

    st.rerun()


def reset_app():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.rerun()


# ============================================================
# SETUP SCREEN
# ============================================================

def setup_screen():
    brand()

    render_html(
        """
        <div class="hero">
            <h1>Enter the arena.<br><span>Make your argument.</span></h1>
            <p>
                A debate partner that challenges your reasoning,
                scores your arguments and helps you improve.
            </p>
        </div>
        """
    )

    render_html(
        """
        <div style="text-align:center;margin:0 0 26px;">
            <span class="pill pill-purple">01 TOPIC</span>
            <span style="color:#555;">→</span>
            <span class="pill pill-muted">02 POSITION</span>
            <span style="color:#555;">→</span>
            <span class="pill pill-muted">03 DEBATE</span>
        </div>
        """
    )

    render_html(
        """
        <div class="card">
            <div class="card-title">What are we debating?</div>
            <div class="card-sub">
                Bring your own topic or let DebateAI surprise you.
            </div>
        </div>
        """
    )

    c1, c2 = st.columns(2)

    with c1:
        if st.button("✦  I have a topic", use_container_width=True):
            st.session_state.topic_mode = "custom"
            st.session_state.topic = ""

    with c2:
        if st.button("✦  Give me a topic", use_container_width=True):
            st.session_state.topic_mode = "random"
            st.session_state.topic = random.choice(TOPICS)

    if st.session_state.topic_mode == "custom":
        topic = st.text_input(
            "Your topic",
            placeholder="e.g. Should AI-generated content be regulated?",
        )
        if topic.strip():
            st.session_state.topic = topic.strip()

    elif st.session_state.topic_mode == "random":
        render_html(
            f"""
            <div class="topic-box">
                <div class="topic-label">Your debate topic</div>
                <div class="topic-text">
                    {html.escape(st.session_state.topic)}
                </div>
            </div>
            """
        )

        if st.button("↻ Generate another", use_container_width=True):
            st.session_state.topic = random.choice(TOPICS)
            st.rerun()

    if st.session_state.topic:
        render_html(
            """
            <div style="height:4px;"></div>
            <div class="card">
                <div class="card-title">Choose your position</div>
                <div class="card-sub">
                    DebateAI will automatically argue the opposite side.
                </div>
            </div>
            """
        )

        p1, p2 = st.columns(2)

        with p1:
            if st.button("✓  FOR", use_container_width=True):
                st.session_state.user_side = "FOR"

            render_html(
                """
                <div class="card side-for">
                    <div style="font-size:21px;">✓</div>
                    <b>FOR</b>
                    <div class="card-sub">Support the motion.</div>
                </div>
                """
            )

        with p2:
            if st.button("✕  AGAINST", use_container_width=True):
                st.session_state.user_side = "AGAINST"

            render_html(
                """
                <div class="card side-against">
                    <div style="font-size:21px;">✕</div>
                    <b>AGAINST</b>
                    <div class="card-sub">Challenge the motion.</div>
                </div>
                """
            )

    if st.session_state.user_side:
        ai_side = (
            "AGAINST"
            if st.session_state.user_side == "FOR"
            else "FOR"
        )

        render_html(
            f"""
            <div class="card">
                <div>
                    <span class="pill pill-green">
                        YOU · {html.escape(st.session_state.user_side)}
                    </span>
                    <span class="pill pill-red">
                        AI · {html.escape(ai_side)}
                    </span>
                </div>
                <div style="margin-top:14px;color:#8b8d98;font-size:13px;">
                    Your position is locked for the entire debate.
                    Make your opening argument when you're ready.
                </div>
            </div>
            """
        )

        if st.button(
            "Start the debate  →",
            use_container_width=True,
            type="primary",
        ):
            start_debate()

    render_html(
        """
        <div class="footer">
            DebateAI · Think sharper. Argue better.
        </div>
        """
    )


# ============================================================
# DEBATE HEADER
# ============================================================

def debate_header():
    progress = (
        st.session_state.round / st.session_state.max_rounds * 100
        if st.session_state.max_rounds
        else 0
    )

    render_html(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:15px;
            margin-bottom:12px;
        ">
            <div>
                <div style="
                    font-family:'Space Grotesk',sans-serif;
                    font-size:24px;
                    font-weight:700;
                ">
                    Debate Arena
                </div>
                <div style="color:#777985;font-size:12px;">
                    Round {st.session_state.round}
                    of {st.session_state.max_rounds}
                </div>
            </div>

            <div>
                <span class="pill pill-green">
                    YOU · {html.escape(st.session_state.user_side or '')}
                </span>
                <span class="pill pill-red">
                    AI · {html.escape(st.session_state.ai_side or '')}
                </span>
            </div>
        </div>

        <div class="progress-wrap">
            <div class="progress" style="width:{progress:.1f}%;"></div>
        </div>
        """
    )

    render_html(
        f"""
        <div class="topic-box">
            <div class="topic-label">Motion</div>
            <div class="topic-text">
                {html.escape(st.session_state.topic)}
            </div>
        </div>
        """
    )


# ============================================================
# SCORE ROW
# ============================================================

def score_row(scores):
    safe_scores = {
        key: float(scores.get(key, 0))
        for key in ["response", "relevance", "reasoning", "evidence", "fairness"]
    }

    avg = sum(safe_scores.values()) / len(safe_scores)

    items = [
        ("Overall", avg),
        ("Response", safe_scores["response"]),
        ("Relevance", safe_scores["relevance"]),
        ("Reasoning", safe_scores["reasoning"]),
        ("Evidence", safe_scores["evidence"]),
        ("Fairness", safe_scores["fairness"]),
    ]

    cols = st.columns(6)

    for col, (label, value) in zip(cols, items):
        with col:
            render_html(
                f"""
                <div class="score-card">
                    <div class="score-number">{value:.1f}</div>
                    <div class="score-label">{html.escape(label)}</div>
                </div>
                """
            )


# ============================================================
# TRANSCRIPT ITEM
# ============================================================

def render_transcript_item(item):
    result = item["result"]

    render_html(
        f"""
        <div class="message">
            <div class="avatar avatar-you">Y</div>
            <div class="message-body">
                <div class="message-name">
                    YOU · ROUND {item['round']}
                </div>
                <div class="message-text">
                    {html.escape(item['argument'])}
                </div>
            </div>
        </div>
        """
    )

    render_html(
        f"""
        <div class="message">
            <div class="avatar avatar-ai">AI</div>
            <div class="message-body">
                <div class="message-name">
                    DEBATEAI · {html.escape(st.session_state.ai_side or '')}
                </div>

                <div class="ai-response">
                    <div class="ai-label">COUNTERARGUMENT</div>
                    <div class="message-text">
                        {html.escape(str(result.get('counterargument', '')))}
                    </div>

                    <div class="soft-divider"></div>

                    <div class="ai-label blue">AI'S POSITION</div>
                    <div class="message-text">
                        {html.escape(str(result.get('ai_point', '')))}
                    </div>
                </div>
            </div>
        </div>
        """
    )

    score_row(result.get("scores", {}))

    fallacy = result.get("possible_fallacy", {})

    if fallacy.get("detected"):
        st.warning(
            "⚠ Possible fallacy detected: "
            + str(fallacy.get("type", "Possible reasoning issue"))
        )
        st.caption(
            "Evidence: “"
            + str(fallacy.get("evidence", ""))
            + "”"
        )

    render_html('<div class="soft-divider"></div>')


# ============================================================
# DEBATE SCREEN
# ============================================================

def debate_screen():
    brand()
    debate_header()

    for item in st.session_state.history:
        render_transcript_item(item)

    if st.session_state.round >= st.session_state.max_rounds:
        st.success("All rounds completed. Your debate report is ready.")

        if st.button("View final report →", use_container_width=True):
            st.session_state.screen = "report"
            st.rerun()

        return

    render_html(
        """
        <div class="card">
            <div class="card-title">Your turn</div>
            <div class="card-sub">
                Respond to the AI's argument. Make your strongest case.
            </div>
        </div>
        """
    )

    render_html(
        """
        <div class="card">
            <div class="card-title">🎙 Voice-to-text</div>
            <div class="card-sub">
                Record your argument. Wait for transcription to finish.
                The text will automatically appear in the argument box below.
            </div>
        </div>
        """
    )

    # The key is stable during a debate, so Streamlit can keep the
    # recording widget and the argument editor independent.
    audio = st.audio_input(
        "🎤 Record your argument",
        key="voice_recorder",
    )

    if audio is not None:
        audio_bytes = audio.getvalue()

        if audio_bytes:
            audio_hash = hashlib.sha256(audio_bytes).hexdigest()

            # Transcribe ONLY when a genuinely new recording is present.
            # This prevents endless "Transcribing..." loops caused by
            # Streamlit rerunning the script after every widget change.
            if audio_hash != st.session_state.last_audio_hash:
                st.session_state.last_audio_hash = audio_hash

                with st.spinner(
                    "Transcribing your argument... "
                    "The first recording may take longer while Whisper loads."
                ):
                    transcript = transcribe_audio(audio)

                if transcript:
                    # This state is set before the text_area is created
                    # during this run, so Streamlit displays the transcript
                    # in the editor on the next render.
                    st.session_state.voice_text = transcript
                    # Do not modify a text-area key after its widget exists.
                    # Incrementing the version creates a fresh widget key on
                    # the next rerun, allowing the transcript to appear safely.
                    st.session_state.argument_editor_version += 1
                    st.rerun()
                else:
                    # Force the status to be visible even when no transcript
                    # was produced.
                    st.rerun()

    if st.session_state.voice_status:
        render_html(
            f"""
            <div class="status-box">
                {html.escape(st.session_state.voice_status)}
            </div>
            """
        )

    # IMPORTANT: never write to a Streamlit widget's session-state key
    # after the widget has been instantiated. Instead, use a versioned key.
    # A new version is created after transcription or after submitting a round.
    argument_key = f"argument_editor_{st.session_state.argument_editor_version}"

    argument = st.text_area(
        "Your argument",
        value=st.session_state.voice_text,
        placeholder=(
            "Your transcribed argument will appear here...\n\n"
            "You can edit it before sending."
        ),
        label_visibility="collapsed",
        key=argument_key,
        height=150,
    )

    c1, c2 = st.columns([3, 1])

    with c1:
        submit = st.button(
            "Send argument  →",
            use_container_width=True,
            type="primary",
        )

    with c2:
        end = st.button(
            "End debate",
            use_container_width=True,
        )

    if end:
        st.session_state.screen = "report"
        st.rerun()

    if submit:
        clean_argument = argument.strip()

        if not clean_argument:
            st.warning("Write an argument before sending it.")
            return

        with st.spinner("DebateAI is thinking..."):
            result = get_ai_response(clean_argument)

        st.session_state.round += 1

        st.session_state.history.append(
            {
                "round": st.session_state.round,
                "argument": clean_argument,
                "result": result,
            }
        )

        st.session_state.scores.append(result.get("scores", {}))
        st.session_state.voice_text = ""
        st.session_state.voice_status = ""
        # Keep last_audio_hash so the same recording is not transcribed
        # again after Streamlit reruns the page.
        # Create a fresh text-area key for the next round instead of
        # modifying the current widget's session-state value.
        st.session_state.argument_editor_version += 1

        if st.session_state.round >= st.session_state.max_rounds:
            st.session_state.screen = "report"

        st.rerun()


# ============================================================
# REPORT SCREEN
# ============================================================

def report_screen():
    brand()

    render_html(
        """
        <div class="hero" style="padding-top:15px;">
            <div style="
                color:#8e82ff;
                font-size:12px;
                letter-spacing:2px;
                font-weight:700;
            ">
                DEBATE COMPLETE
            </div>

            <h1 style="margin-top:12px;">
                Here's how you <span>did.</span>
            </h1>

            <p>
                Your debate has been analysed from the first
                argument to the final round.
            </p>
        </div>
        """
    )

    all_values = []

    for score in st.session_state.scores:
        all_values.extend(
            float(score.get(key, 0))
            for key in ["response", "relevance", "reasoning", "evidence", "fairness"]
        )

    overall = (
        sum(all_values) / len(all_values)
        if all_values
        else 0
    )

    render_html(
        f"""
        <div class="report-score">
            <div style="
                color:#858792;
                font-size:12px;
                letter-spacing:2px;
            ">
                OVERALL DEBATE SCORE
            </div>

            <div class="big-score">{overall:.1f}</div>

            <div style="color:#858792;font-size:13px;">
                out of 10
            </div>
        </div>
        """
    )

    categories = [
        "response",
        "relevance",
        "reasoning",
        "evidence",
        "fairness",
    ]

    averages = {}

    if st.session_state.scores:
        for category in categories:
            values = [
                float(score.get(category, 0))
                for score in st.session_state.scores
            ]
            averages[category] = sum(values) / len(values)

        render_html(
            """
            <div class="report-section">
                <h3>Performance breakdown</h3>
            </div>
            """
        )

        cols = st.columns(5)

        for col, category in zip(cols, categories):
            with col:
                value = averages[category]
                render_html(
                    f"""
                    <div class="score-card">
                        <div class="score-number">{value:.1f}</div>
                        <div class="score-label">
                            {html.escape(category.title())}
                        </div>
                    </div>
                    """
                )

    if averages:
        strongest = max(averages, key=averages.get)
        weakest = min(averages, key=averages.get)

        strength_text = {
            "response": "You did well at directly engaging with the opposing argument.",
            "relevance": "Your arguments stayed closely connected to the debate motion.",
            "reasoning": "Your reasoning was one of the strongest parts of the debate.",
            "evidence": "You supported your claims comparatively well with justification or examples.",
            "fairness": "You maintained a relatively fair and respectful debating style.",
        }[strongest]

        weakness_text = {
            "response": "Make your response explicitly answer the AI's strongest point before introducing a new claim.",
            "relevance": "Avoid points that are interesting but do not directly prove your position on the motion.",
            "reasoning": "Connect each claim to a clear reason and explain the cause-and-effect relationship.",
            "evidence": "Add concrete examples, observations, or verifiable evidence instead of relying only on assertions.",
            "fairness": "Avoid sweeping assumptions or personal attacks and acknowledge reasonable opposing concerns.",
        }[weakest]

        render_html(
            f"""
            <div class="report-section">
                <h3>✦ What you did well</h3>
                <p>{html.escape(strength_text)}</p>
                <p>
                    Your highest category was
                    <b>{html.escape(strongest.title())}</b>
                    at <b>{averages[strongest]:.1f}/10</b>.
                </p>
            </div>
            """
        )

        render_html(
            f"""
            <div class="report-section">
                <h3>△ What could be stronger</h3>
                <p>{html.escape(weakness_text)}</p>
                <p>
                    Your lowest category was
                    <b>{html.escape(weakest.title())}</b>
                    at <b>{averages[weakest]:.1f}/10</b>.
                </p>
            </div>
            """
        )

    render_html(
        """
        <div class="report-section">
            <h3>✎ Argument corrections</h3>
            <div style="
                color:#858792;
                font-size:13px;
                margin-bottom:18px;
            ">
                Here's how your arguments could have been stronger.
            </div>
        """
    )

    for item in st.session_state.history:
        result = item["result"]
        better = result.get(
            "better_argument",
            result.get(
                "coaching_note",
                "Support this claim with clearer reasoning and evidence.",
            ),
        )

        render_html(
            f"""
            <div style="
                padding:15px;
                background:#0d0e13;
                border-radius:14px;
                margin-bottom:12px;
                border:1px solid #20222c;
            ">
                <div style="
                    color:#8c8e99;
                    font-size:11px;
                    margin-bottom:6px;
                ">
                    ROUND {item['round']}
                </div>

                <div style="
                    font-size:14px;
                    line-height:1.55;
                    margin-bottom:12px;
                ">
                    “{html.escape(item['argument'])}”
                </div>

                <div style="
                    color:#65c6ff;
                    font-size:12px;
                    font-weight:600;
                ">
                    BETTER APPROACH
                </div>

                <div style="
                    color:#b1b2ba;
                    font-size:13px;
                    line-height:1.55;
                    margin-top:5px;
                ">
                    {html.escape(str(better))}
                </div>
            </div>
            """
        )

    render_html(
        """
        </div>
        """
    )

    render_html(
        """
        <div class="report-section">
            <h3>⚡ Your next move</h3>
            <p>In your next debate, focus on three things:</p>
            <p><b>01</b> Make your claim clearly.</p>
            <p><b>02</b> Support it with evidence or an example.</p>
            <p><b>03</b> Directly attack the opposing argument.</p>
        </div>
        """
    )

    if st.button(
        "↻  Start a new debate",
        use_container_width=True,
    ):
        reset_app()

    render_html(
        """
        <div class="footer">
            DebateAI · Think sharper. Argue better.
        </div>
        """
    )


# ============================================================
# ROUTER
# ============================================================

if st.session_state.screen == "setup":
    setup_screen()

elif st.session_state.screen == "debate":
    debate_screen()

elif st.session_state.screen == "report":
    report_screen()