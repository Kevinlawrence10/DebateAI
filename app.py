# ============================================================
# DEBATEAI — THE CHAMBER
# Streamlit + Ollama + Whisper
# ============================================================

import streamlit as st
import requests
import json
import random
import html
import os
import io
import hashlib
import tempfile
import textwrap


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="The Chamber — DebateAI",
    page_icon="◈",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CHAMBER CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');


:root {
    --bg: #12141b;
    --surface: #1a1d28;
    --surface2: #20232f;

    --border: rgba(245,241,232,.08);
    --border2: rgba(245,241,232,.16);

    --text: #f2ede1;
    --dim: #9aa0ae;
    --faint: #666c7a;

    --brass: #c9a15c;
    --brass-dim: rgba(201,161,92,.35);

    --green: #3aa88a;
    --green-dim: rgba(58,168,138,.14);

    --red: #d0555f;
    --red-dim: rgba(208,85,95,.14);
}


/* ============================================================
   GLOBAL
   ============================================================ */

* {
    box-sizing: border-box;
}

.stApp {
    background:
        radial-gradient(
            1200px 600px at 50% -10%,
            rgba(140,60,60,.16),
            transparent 60%
        ),
        radial-gradient(
            900px 500px at 90% 100%,
            rgba(60,110,100,.12),
            transparent 60%
        ),
        var(--bg);

    color: var(--text);
}

.block-container {
    max-width: 760px !important;
    padding-top: 30px !important;
    padding-bottom: 60px !important;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

* {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Fraunces', serif !important;
    color: var(--text) !important;
}

h1 {
    font-size: clamp(30px, 5vw, 42px) !important;
    line-height: 1.15 !important;
    font-weight: 600 !important;
    letter-spacing: -.01em !important;
    margin-bottom: 10px !important;
}

p {
    color: var(--dim);
}


/* ============================================================
   BRAND
   ============================================================ */

.chamber-mark {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;

    margin-bottom: 32px;

    color: var(--dim);

    letter-spacing: .16em;
    text-transform: uppercase;

    font-size: 11px;
    font-weight: 600;
}

.chamber-mark::before,
.chamber-mark::after {
    content: "";

    width: 24px;
    height: 1px;

    background: var(--brass-dim);
}

.chamber-mark b {
    color: var(--brass);
}


/* ============================================================
   LEDE
   ============================================================ */

.lede {
    color: var(--dim);
    font-size: 15px;
    max-width: 52ch;
    margin-bottom: 30px;
    line-height: 1.65;
}


/* ============================================================
   LABELS
   ============================================================ */

.field-label {
    display: block;

    font-family: 'JetBrains Mono', monospace;

    font-size: 11px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: .1em;

    color: var(--faint);

    margin-bottom: 11px;
}

.section-label {
    font-family: 'JetBrains Mono', monospace;

    font-size: 11px;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: .12em;

    color: var(--brass);

    margin: 28px 0 12px;
}


/* ============================================================
   BIG INTERACTIVE CHOICE BUTTONS
   ============================================================ */

.big-choice-row {
    margin-top: 12px;
    margin-bottom: 24px;
}


/* Every button is a proper large interactive surface */

.stButton > button {

    width: 100% !important;

    min-height: 58px !important;

    border-radius: 14px !important;

    background: var(--surface2) !important;

    border: 1px solid var(--border2) !important;

    color: var(--text) !important;

    font-family: 'Inter', sans-serif !important;

    font-size: 14px !important;

    font-weight: 700 !important;

    padding: 12px 18px !important;

    transition:
        transform .18s ease,
        border-color .18s ease,
        background .18s ease,
        box-shadow .18s ease !important;

    box-shadow: none !important;
}


.stButton > button:hover {

    background: #262a38 !important;

    border-color: var(--brass-dim) !important;

    color: var(--text) !important;

    transform: translateY(-2px) !important;

    box-shadow:
        0 8px 24px rgba(0,0,0,.18) !important;
}


.stButton > button:active {

    transform: translateY(0) !important;

}


/* Primary buttons */

.stButton > button[kind="primary"] {

    background: var(--brass) !important;

    color: #1a1408 !important;

    border-color: var(--brass) !important;

}


.stButton > button[kind="primary"]:hover {

    background: #d6b16d !important;

    color: #1a1408 !important;

}


/* ============================================================
   TOPIC CHOICE BUTTONS
   ============================================================ */

.topic-choice {

    min-height: 125px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    text-align: center !important;

    padding: 22px !important;

    font-size: 16px !important;

    line-height: 1.5 !important;

}


/* ============================================================
   STANCE BUTTONS
   ============================================================ */

.stance-button {

    min-height: 170px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    text-align: center !important;

    font-family: 'Fraunces', serif !important;

    font-size: 25px !important;

}


.stance-for-button {

    border-color: rgba(58,168,138,.30) !important;

}


.stance-for-button:hover {

    border-color: var(--green) !important;

    background: var(--green-dim) !important;

}


.stance-against-button {

    border-color: rgba(208,85,95,.30) !important;

}


.stance-against-button:hover {

    border-color: var(--red) !important;

    background: var(--red-dim) !important;

}


/* ============================================================
   TOPIC PLAQUE
   ============================================================ */

.topic-plaque {

    background: var(--surface);

    border: 1px solid var(--border);

    border-left: 3px solid var(--brass);

    border-radius: 4px 14px 14px 4px;

    padding: 22px 25px;

    margin: 20px 0 28px;
}

.topic-eyebrow {

    font-family: 'JetBrains Mono', monospace;

    font-size: 10px;

    text-transform: uppercase;

    letter-spacing: .14em;

    color: var(--brass);

    font-weight: 700;

    margin-bottom: 8px;
}

.topic-resolution {

    font-family: 'Fraunces', serif;

    font-size: 20px;

    font-weight: 500;

    line-height: 1.45;

    color: var(--text);
}


/* ============================================================
   DEBATE HEADER
   ============================================================ */

.debate-header {

    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    gap: 16px;

    margin-bottom: 20px;
}

.debate-resolution {

    font-family: 'Fraunces', serif;

    font-size: 19px;

    font-weight: 500;

    line-height: 1.4;

    color: var(--text);
}

.side-tag {

    display: inline-block;

    font-family: 'JetBrains Mono', monospace;

    font-size: 10px;

    text-transform: uppercase;

    letter-spacing: .08em;

    padding: 5px 10px;

    border-radius: 20px;

    margin-top: 8px;

    font-weight: 700;
}

.side-for {

    background: var(--green-dim);

    color: var(--green);
}

.side-against {

    background: var(--red-dim);

    color: var(--red);
}


/* ============================================================
   ROUND TRACKER
   ============================================================ */

.round-tracker {

    display: flex;

    align-items: center;

    gap: 6px;

    flex-shrink: 0;
}

.round-dot {

    width: 9px;
    height: 9px;

    border-radius: 50%;

    background: var(--border2);
}

.round-dot.done {

    background: var(--brass);
}

.round-dot.now {

    background: var(--brass);

    box-shadow:
        0 0 0 4px rgba(201,161,92,.18);
}

.round-number {

    font-family: 'JetBrains Mono', monospace;

    font-size: 10px;

    color: var(--dim);

    margin-left: 7px;

    white-space: nowrap;
}


/* ============================================================
   BUBBLES
   ============================================================ */

.bubble {

    border-radius: 16px;

    padding: 20px 22px;

    border: 1px solid var(--border);

    margin-bottom: 15px;
}

.bubble-user {

    background: var(--surface);

    border-left: 3px solid var(--brass);
}

.bubble-ai {

    background: var(--surface2);
}

.bubble-label {

    font-family: 'JetBrains Mono', monospace;

    font-size: 10px;

    text-transform: uppercase;

    letter-spacing: .1em;

    font-weight: 700;

    color: var(--brass);

    margin-bottom: 10px;
}

.bubble-ai .bubble-label {

    color: var(--dim);
}

.bubble-text {

    font-size: 15px;

    line-height: 1.65;

    color: var(--text);

    white-space: pre-wrap;
}


/* ============================================================
   AI OWN POINT
   ============================================================ */

.ai-point {

    margin-top: 16px;

    padding-top: 16px;

    border-top: 1px dashed var(--border2);
}

.ai-point-label {

    font-family: 'JetBrains Mono', monospace;

    font-size: 10px;

    text-transform: uppercase;

    letter-spacing: .1em;

    font-weight: 700;

    color: var(--faint);

    margin-bottom: 8px;
}


/* ============================================================
   SCORE
   ============================================================ */

.score-card {

    display: flex;

    align-items: center;

    gap: 18px;

    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 16px;

    padding: 18px 22px;

    margin-bottom: 18px;
}

.score-dial {

    width: 68px;
    height: 68px;

    position: relative;

    flex-shrink: 0;
}

.score-dial svg {

    transform: rotate(-90deg);
}

.score-track {

    fill: none;

    stroke: var(--border2);

    stroke-width: 6;
}

.score-fill {

    fill: none;

    stroke: var(--brass);

    stroke-width: 6;

    stroke-linecap: round;
}

.score-number {

    position: absolute;

    inset: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    font-family: 'JetBrains Mono', monospace;

    font-weight: 700;

    font-size: 16px;

    color: var(--text);
}

.score-label {

    font-family: 'JetBrains Mono', monospace;

    font-size: 10px;

    text-transform: uppercase;

    letter-spacing: .1em;

    color: var(--faint);

    font-weight: 700;

    margin-bottom: 5px;
}

.score-reason {

    font-size: 13px;

    line-height: 1.55;

    color: var(--dim);
}


/* ============================================================
   INPUT
   ============================================================ */

.input-card {

    background: var(--surface);

    border: 1px solid var(--border);

    border-radius: 16px;

    padding: 20px;

    margin-bottom: 12px;
}

.stTextArea textarea,
.stTextInput input {

    background: var(--surface2) !important;

    color: var(--text) !important;

    border: 1px solid var(--border2) !important;

    border-radius: 12px !important;

    font-family: 'Inter', sans-serif !important;

    font-size: 15px !important;
}

.stTextArea textarea {

    min-height: 115px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {

    border-color: var(--brass-dim) !important;
}


/* ============================================================
   STATUS
   ============================================================ */

.status {

    background: var(--surface2);

    border: 1px solid var(--border);

    border-radius: 12px;

    padding: 11px 14px;

    color: var(--dim);

    font-size: 12px;

    margin: 10px 0;
}


/* ============================================================
   LOADING
   ============================================================ */

.loading {

    display: flex;

    align-items: center;

    gap: 5px;

    color: var(--dim);

    font-size: 13px;

    padding: 8px 2px;
}


/* ============================================================
   VERDICT
   ============================================================ */

.verdict-card {

    background:
        linear-gradient(
            160deg,
            var(--surface),
            var(--surface2)
        );

    border: 1px solid var(--border);

    border-radius: 18px;

    padding: 34px;

    text-align: center;

    margin-bottom: 25px;
}

.verdict-score {

    font-family: 'Fraunces', serif;

    font-size: 58px;

    font-weight: 600;

    color: var(--brass);

    line-height: 1;
}

.verdict-score span {

    font-family: 'JetBrains Mono', monospace;

    font-size: 20px;

    color: var(--faint);
}

.verdict-label {

    font-family: 'JetBrains Mono', monospace;

    font-size: 10px;

    text-transform: uppercase;

    letter-spacing: .12em;

    color: var(--faint);

    font-weight: 700;

    margin-top: 10px;
}

.verdict-overview {

    margin-top: 18px;

    font-size: 14px;

    line-height: 1.7;

    color: var(--dim);
}


/* ============================================================
   CORRECTIONS
   ============================================================ */

.correction {

    border: 1px solid var(--border);

    border-radius: 14px;

    padding: 18px 20px;

    margin-bottom: 12px;

    background: var(--surface);
}

.correction-head {

    display: flex;

    align-items: center;

    gap: 10px;

    margin-bottom: 8px;
}

.round-badge {

    font-family: 'JetBrains Mono', monospace;

    font-size: 10px;

    font-weight: 700;

    color: #1a1408;

    background: var(--brass);

    padding: 4px 9px;

    border-radius: 20px;
}

.correction-score {

    font-family: 'JetBrains Mono', monospace;

    font-size: 11px;

    color: var(--faint);
}

.correction p {

    font-size: 14px;

    line-height: 1.6;

    color: var(--dim);
}


/* ============================================================
   FOOTER
   ============================================================ */

.chamber-footer {

    margin-top: 40px;

    color: var(--faint);

    font-size: 11px;

    text-align: center;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media(max-width:700px) {

    .block-container {

        padding-left: 1rem !important;

        padding-right: 1rem !important;
    }

    .debate-header {

        flex-direction: column;
    }

    .topic-choice {

        min-height: 110px !important;
    }

    .stance-button {

        min-height: 130px !important;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def render_html(content):

    cleaned = textwrap.dedent(content).strip()

    if hasattr(st, "html"):

        st.html(cleaned)

    else:

        st.markdown(
            cleaned,
            unsafe_allow_html=True
        )


def chamber_brand():

    render_html(
        """
        <div class="chamber-mark">
            the <b>chamber</b> · live debate
        </div>
        """
    )


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {

    "screen": "topic",

    "topic": "",

    "topic_mode": "",

    "user_side": "",

    "ai_side": "",

    "max_rounds": 4,

    "round": 0,

    "history": [],

    "scores": [],

    "voice_text": "",

    "voice_status": "",

    "last_audio_hash": "",

    "argument_version": 0,

    "final_report": None,
}


for key, value in DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# TOPICS
# ============================================================

TOPICS = [

    "Should artificial intelligence be regulated?",

    "Should social media companies be responsible for misinformation?",

    "Should college education be completely free?",

    "Should space exploration receive more public funding?",

    "Should AI-generated content always be labelled?",

    "Should mobile phones be banned in classrooms?",

    "Should autonomous vehicles be allowed to make life-or-death decisions?",

    "Should students be allowed to use AI for academic work?",

    "Should online education replace traditional classrooms?",

    "Should governments provide universal basic income?",
]


# ============================================================
# OLLAMA
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "llama3.2:3b"


def call_ollama(prompt):

    response = requests.post(

        OLLAMA_URL,

        json={

            "model": OLLAMA_MODEL,

            "prompt": prompt,

            "stream": False,

            "format": "json",

        },

        timeout=120,

    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "response",
        ""
    ).strip()


# ============================================================
# JSON PARSER
# ============================================================

def parse_json(text):

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    text = text.strip()

    start = text.find("{")

    end = text.rfind("}")

    if start != -1 and end != -1:

        text = text[start:end + 1]

    return json.loads(text)


# ============================================================
# AI TOPIC GENERATION
# ============================================================

def generate_topic():

    prompt = """
You are generating a formal debate resolution.

Create ONE fresh and balanced debate topic.

The topic must:

- have strong arguments on both sides
- be suitable for college students
- encourage real disagreement
- be interesting enough for a live debate
- avoid extremely obvious topics
- avoid requiring specialist knowledge

Return JSON only.

Format:

{
    "topic": "..."
}
"""

    try:

        raw = call_ollama(prompt)

        data = parse_json(raw)

        topic = data.get(
            "topic",
            ""
        ).strip()

        if topic:

            return topic

    except Exception:

        pass

    return random.choice(TOPICS)


# ============================================================
# FALLBACK DEBATE RESPONSE
# ============================================================

def fallback_debate(argument):

    return {

        "rebuttal":
            "I disagree with your argument because it does not fully "
            "consider the consequences of the position you're defending. "
            "Even if your point is valid in some situations, it does not "
            "necessarily prove that your overall position is correct. "
            "There are practical limitations and opposing considerations "
            "that need to be addressed.",

        "bot_point":
            "My position is that the opposing side has a stronger case "
            "because decisions on this issue should consider the broader "
            "impact, not just the benefit described in your argument. "
            "A policy or idea should also be judged by what happens when "
            "it is applied in real-world situations.",

        "score": 6,

        "score_reason":
            "Your argument is relevant, but the reasoning could be supported with stronger evidence and a clearer response to the opposing position.",

    }


# ============================================================
# HUMAN-LIKE DEBATE AI
# ============================================================

def debate_ai(argument):

    topic = st.session_state.topic

    user_side = st.session_state.user_side

    ai_side = st.session_state.ai_side

    current_round = st.session_state.round


    # --------------------------------------------------------
    # Build previous debate context
    # --------------------------------------------------------

    history_text = ""


    for item in st.session_state.history:

        history_text += f"""

ROUND {item['round']}

USER ({user_side}):
{item['argument']}

CHAMBER ({ai_side}) REBUTTAL:
{item['result'].get('rebuttal', '')}

CHAMBER ({ai_side}) OWN ARGUMENT:
{item['result'].get('bot_point', '')}

"""


    # --------------------------------------------------------
    # MAIN DEBATE PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are "The Chamber", a REAL HUMAN DEBATE OPPONENT.

You are currently debating another person.

This is NOT a coaching session.

This is NOT a feedback session.

This is NOT an interview.

This is a LIVE DEBATE.

==================================================
DEBATE TOPIC
==================================================

{topic}

==================================================
POSITIONS
==================================================

USER POSITION:
{user_side}

YOUR POSITION:
{ai_side}

You MUST defend {ai_side}.

The user is defending {user_side}.

You must NEVER switch sides.

You must NEVER simply agree with the user.

==================================================
USER'S CURRENT ARGUMENT
==================================================

{argument}

==================================================
PREVIOUS ROUNDS
==================================================

{history_text if history_text else "No previous rounds. This is the opening argument."}

==================================================
YOUR ROLE
==================================================

You are the user's OPPONENT.

Your job is to actually DEBATE the user.

You must do TWO separate things:

1. Directly REBUT the argument the user just made.
2. Present YOUR OWN NEW ARGUMENT supporting your side.

You are not merely evaluating what the user said.

You are actively arguing against them.

==================================================
VERY IMPORTANT — NO COACHING DURING THE DEBATE
==================================================

Do NOT turn your response into coaching.

Do NOT tell the user:

- how to improve
- what they should change
- what mistakes they made
- how to structure their argument
- how to make their argument stronger
- what evidence they should add
- what they could have said instead
- what they should do in the next round

Those things belong in the FINAL REPORT.

During the live debate, behave like an actual opponent.

==================================================
PART 1 — REBUTTAL
==================================================

Directly challenge the user's latest argument.

Your rebuttal must:

- respond specifically to what the user said
- defend {ai_side}
- identify weaknesses in their reasoning
- challenge assumptions when appropriate
- question unsupported claims
- address their examples
- provide counter-reasoning
- introduce relevant opposing considerations
- move the debate forward

Do not simply say that you disagree.

Explain WHY you disagree.

Make it sound like spoken human debate.

Examples of natural debate language:

"That's a fair point, but I don't think it proves the conclusion you're drawing."

"I disagree with that. The problem is..."

"But that argument assumes that..."

"That's exactly where I think your reasoning breaks down."

"Even if we accept that point, there's still a much bigger issue."

"You're focusing on the immediate benefit, but what about the long-term consequence?"

"Let me challenge that assumption."

"That example doesn't necessarily support the broader claim you're making."

Use different openings across rounds.

Do not repeatedly start with:

"Your argument..."

"While I understand..."

"According to..."

Do NOT insult the user.

Do NOT attack the user's personality.

Attack the ARGUMENT.

Rebuttal length:

4–7 sentences.

==================================================
PART 2 — THE CHAMBER'S OWN ARGUMENT
==================================================

This part is EXTREMELY IMPORTANT.

After rebutting the user, you MUST introduce a NEW argument supporting:

{ai_side}

You are not just responding to the user.

You are an ACTIVE DEBATER.

Bring a point that the user has not already addressed.

The Chamber's own point should:

- clearly support {ai_side}
- be relevant to the resolution
- be different from previous Chamber arguments
- introduce a new angle
- give the user something to respond to
- sound like a real person making a debate point

Do NOT turn this into advice.

Do NOT say:

"You should consider..."

"You could improve..."

"You need to..."

Instead, STATE YOUR OWN POSITION.

Examples:

"Another issue is the practical impact this would have on ordinary people."

"My position is that the larger concern is..."

"There's another reason I support {ai_side}: ..."

"The stronger case for {ai_side} is..."

"Consider what happens when this idea is applied at scale..."

The Chamber's own point should be an actual ARGUMENT.

Length:

3–5 sentences.

==================================================
DEBATE PERSONALITY
==================================================

Sound:

- intelligent
- confident
- competitive
- natural
- spontaneous
- persuasive
- respectful
- occasionally challenging
- emotionally engaged when appropriate

You can use:

- rhetorical questions
- short emphatic sentences
- concessions
- challenges
- examples
- comparisons
- practical situations

You should sound like a person sitting across the table from the user.

Do not sound like an AI textbook.

Do not write an essay.

Do not repeat the same argument every round.

==================================================
SIDE CONSISTENCY
==================================================

The user's side:

{user_side}

The Chamber's side:

{ai_side}

The Chamber MUST defend {ai_side} throughout the entire debate.

If the user makes a strong argument, acknowledge the specific point
briefly if appropriate, but STILL defend {ai_side}.

Do not switch sides simply because the user's argument is convincing.

==================================================
SCORING
==================================================

After producing the debate response, evaluate ONLY the user's latest
argument.

Give a score from 1 to 10.

Consider:

- logical strength
- relevance
- clarity
- evidence
- response to the opposing side
- persuasiveness

Do not automatically give high scores.

A weak argument should receive a lower score.

A strong argument should receive a higher score.

The score is separate from your debate response.

==================================================
SCORE REASON
==================================================

Give ONE short sentence explaining the score.

Mention something specific about the user's latest argument.

Do not turn this into a long coaching paragraph.

==================================================
FINAL RESPONSE STRUCTURE
==================================================

The output should conceptually look like this:

THE CHAMBER RESPONDS:
[direct rebuttal]

THE CHAMBER'S OWN POINT:
[new argument supporting {ai_side}]

SCORE:
[number]/10

SCORE REASON:
[one short sentence]

==================================================
OUTPUT
==================================================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "rebuttal": "Direct rebuttal against the user's latest argument.",
    "bot_point": "A completely new argument supporting {ai_side}.",
    "score": 7,
    "score_reason": "Short explanation of the user's score."
}}
"""


    # --------------------------------------------------------
    # Ask Ollama
    # --------------------------------------------------------

    try:

        raw = call_ollama(prompt)

        data = parse_json(raw)


        # ----------------------------------------------------
        # Validate score
        # ----------------------------------------------------

        data["score"] = max(

            1,

            min(

                10,

                int(

                    float(

                        data.get(
                            "score",
                            5
                        )

                    )

                )

            )

        )


        # ----------------------------------------------------
        # Make sure rebuttal exists
        # ----------------------------------------------------

        if not data.get("rebuttal"):

            data["rebuttal"] = (
                "I disagree with that argument because "
                "it does not fully address the opposing position."
            )


        # ----------------------------------------------------
        # Make sure Chamber's own argument exists
        # ----------------------------------------------------

        if not data.get("bot_point"):

            data["bot_point"] = (

                f"My position remains {ai_side}. "
                f"There is another important consideration that "
                f"supports this side of the resolution."

            )


        # ----------------------------------------------------
        # Make sure score reason exists
        # ----------------------------------------------------

        if not data.get("score_reason"):

            data["score_reason"] = (
                "The argument was relevant, but some parts "
                "needed stronger reasoning or supporting evidence."
            )


        return data


    except Exception:

        return fallback_debate(argument)


# ============================================================
# VOICE
# ============================================================

def audio_suffix(audio):

    mime = getattr(
        audio,
        "type",
        ""
    ) or ""

    if "webm" in mime:

        return ".webm"

    if "ogg" in mime:

        return ".ogg"

    if "mp4" in mime or "m4a" in mime:

        return ".m4a"

    return ".wav"


def transcribe_audio(audio):

    if audio is None:

        return ""

    audio_bytes = audio.getvalue()

    if not audio_bytes:

        return ""

    temp_path = None


    try:

        from faster_whisper import WhisperModel


        if "whisper_model" not in st.session_state:

            model_name = os.getenv(
                "WHISPER_MODEL",
                "base.en"
            )

            st.session_state.voice_status = (
                f"Loading voice model: {model_name}..."
            )

            st.session_state.whisper_model = WhisperModel(

                model_name,

                device="cpu",

                compute_type="int8",

            )


        suffix = audio_suffix(audio)


        with tempfile.NamedTemporaryFile(

            delete=False,

            suffix=suffix

        ) as tmp:

            tmp.write(audio_bytes)

            tmp.flush()

            temp_path = tmp.name


        segments, info = (

            st.session_state.whisper_model.transcribe(

                temp_path,

                beam_size=5,

                vad_filter=True,

                language="en",

                condition_on_previous_text=False,

            )

        )


        parts = []


        for segment in segments:

            text = segment.text.strip()

            if text:

                parts.append(text)


        transcript = " ".join(parts).strip()


        if transcript:

            st.session_state.voice_status = (

                f"Voice transcription completed · "
                f"{len(transcript.split())} words"
            )

            return transcript


    except Exception:

        pass


    finally:

        if temp_path:

            try:

                os.remove(temp_path)

            except OSError:

                pass


    # Backup recognizer

    try:

        import speech_recognition as sr

        recognizer = sr.Recognizer()


        with sr.AudioFile(

            io.BytesIO(audio_bytes)

        ) as source:

            audio_data = recognizer.record(
                source
            )


        transcript = recognizer.recognize_google(

            audio_data,

            language="en-IN",

        ).strip()


        if transcript:

            st.session_state.voice_status = (

                f"Voice transcription completed · "
                f"{len(transcript.split())} words"
            )

            return transcript


    except Exception:

        pass


    st.session_state.voice_status = (

        "Could not transcribe the recording. "
        "Try speaking clearly and recording again."
    )

    return ""


# ============================================================
# FINAL REPORT
# ============================================================

def generate_final_report():

    transcript = ""


    for item in st.session_state.history:

        transcript += f"""

ROUND {item['round']}

USER ARGUMENT:
{item['argument']}

SCORE:
{item['result'].get('score', 0)}/10

SCORE REASON:
{item['result'].get('score_reason', '')}

AI REBUTTAL:
{item['result'].get('rebuttal', '')}

AI POINT:
{item['result'].get('bot_point', '')}

"""


    prompt = f"""
You are an expert human debate coach.

Review this COMPLETE debate.

TOPIC:
{st.session_state.topic}

USER POSITION:
{st.session_state.user_side}

COMPLETE TRANSCRIPT:
{transcript}

Return ONLY JSON.

Format:

{{
    "overview": "3-5 sentences describing the user's overall performance.",

    "corrections": [
        {{
            "round": 1,
            "correction": "Specific correction for this round."
        }}
    ]
}}

Rules:

- Include exactly one correction for every round.
- Reference the actual argument made by the user.
- Identify specific weaknesses.
- Explain how the argument could be stronger.
- Do not invent facts.
- Be constructive.
- Do not simply repeat the score.
"""


    try:

        raw = call_ollama(prompt)

        return parse_json(raw)


    except Exception:

        return {

            "overview":
                "The debate has been completed. Your arguments remained connected to the resolution, but several points could be strengthened with clearer reasoning, direct responses and concrete evidence.",

            "corrections": [

                {

                    "round": item["round"],

                    "correction":
                        item["result"].get(

                            "score_reason",

                            "Develop the claim with clearer reasoning and supporting evidence."

                        )

                }

                for item in st.session_state.history

            ],

        }


# ============================================================
# RESET
# ============================================================

def reset_app():

    for key, value in DEFAULTS.items():

        st.session_state[key] = value

    st.rerun()


# ============================================================
# SCREEN 1 — TOPIC
# ============================================================

def topic_screen():

    chamber_brand()

    st.title(
        "What shall we resolve tonight?"
    )


    st.markdown(
        """
        <div class="lede">
        Bring your own resolution, or let the Chamber propose one.
        Either way, you'll argue one side and the Chamber will argue the other.
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="section-label">STEP 1 — THE RESOLUTION</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # BIG CLICKABLE TOPIC OPTIONS
    # ========================================================

    c1, c2 = st.columns(2)


    with c1:

        if st.button(

            "I'll give the topic\n\nType your own resolution",

            use_container_width=True,

            key="topic_own",

        ):

            st.session_state.topic_mode = "own"

            st.session_state.topic = ""

            st.rerun()


    with c2:

        if st.button(

            "Let the Chamber pick\n\nAI generates the resolution",

            use_container_width=True,

            key="topic_ai",

        ):

            st.session_state.topic_mode = "auto"

            with st.spinner(
                "The Chamber is choosing a topic..."
            ):

                st.session_state.topic = (
                    generate_topic()
                )

            st.rerun()


    # ========================================================
    # USER TOPIC
    # ========================================================

    if st.session_state.topic_mode == "own":

        st.markdown(
            '<div class="section-label">YOUR RESOLUTION</div>',
            unsafe_allow_html=True
        )


        topic = st.text_input(

            "Topic",

            placeholder=
                "e.g. Social media does more harm than good",

            label_visibility="collapsed",

            max_chars=160,

        )


        if topic.strip():

            st.session_state.topic = topic.strip()


    # ========================================================
    # AI TOPIC
    # ========================================================

    elif st.session_state.topic_mode == "auto":

        render_html(

            f"""
            <div class="topic-plaque">

                <div class="topic-eyebrow">
                    Proposed resolution
                </div>

                <div class="topic-resolution">
                    {html.escape(st.session_state.topic)}
                </div>

            </div>
            """

        )


        if st.button(

            "🎲 Generate another topic",

            use_container_width=True,

        ):

            with st.spinner(
                "Thinking of another resolution..."
            ):

                st.session_state.topic = (
                    generate_topic()
                )

            st.rerun()


    # ========================================================
    # ROUNDS
    # ========================================================

    if st.session_state.topic:

        st.markdown(
            '<div class="section-label">NUMBER OF ROUNDS</div>',
            unsafe_allow_html=True
        )


        round_cols = st.columns(3)


        for col, number in zip(

            round_cols,

            [3, 4, 5]

        ):

            with col:

                selected = (
                    st.session_state.max_rounds == number
                )


                label = (
                    f"✓  {number} ROUNDS"
                    if selected
                    else f"{number} ROUNDS"
                )


                if st.button(

                    label,

                    use_container_width=True,

                    type=
                        "primary"
                        if selected
                        else "secondary",

                    key=f"round_select_{number}",

                ):

                    st.session_state.max_rounds = number

                    st.rerun()


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        if st.button(

            "Continue →",

            use_container_width=True,

            type="primary",

            key="continue_topic",

        ):

            if len(
                st.session_state.topic.strip()
            ) < 6:

                st.error(
                    "Please enter a meaningful topic."
                )

            else:

                st.session_state.screen = "stance"

                st.rerun()


    render_html(
        """
        <div class="chamber-footer">
            DebateAI · arguments and feedback generated locally by Ollama
        </div>
        """
    )


# ============================================================
# SCREEN 2 — STANCE
# ============================================================

def stance_screen():

    chamber_brand()


    st.title(
        "Choose your side"
    )


    st.markdown(
        """
        <div class="lede">
        The Chamber will argue whichever side you don't.
        Your position stays locked for the entire debate.
        </div>
        """,
        unsafe_allow_html=True,
    )


    render_html(

        f"""
        <div class="topic-plaque">

            <div class="topic-eyebrow">
                Resolved
            </div>

            <div class="topic-resolution">
                {html.escape(st.session_state.topic)}
            </div>

        </div>
        """

    )


    st.markdown(
        '<div class="section-label">YOUR POSITION</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # BIG CLICKABLE FOR / AGAINST BUTTONS
    # ========================================================

    c1, c2 = st.columns(2)


    with c1:

        if st.button(

            "FOR\n\nArgue in favor",

            use_container_width=True,

            key="stance_for",

        ):

            st.session_state.user_side = "FOR"

            st.session_state.ai_side = "AGAINST"

            st.session_state.round = 1

            st.session_state.history = []

            st.session_state.scores = []

            st.session_state.final_report = None

            st.session_state.screen = "debate"

            st.rerun()


    with c2:

        if st.button(

            "AGAINST\n\nArgue in opposition",

            use_container_width=True,

            key="stance_against",

        ):

            st.session_state.user_side = "AGAINST"

            st.session_state.ai_side = "FOR"

            st.session_state.round = 1

            st.session_state.history = []

            st.session_state.scores = []

            st.session_state.final_report = None

            st.session_state.screen = "debate"

            st.rerun()


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    if st.button(

        "← Back",

        use_container_width=True,

        key="back_to_topic",

    ):

        st.session_state.screen = "topic"

        st.rerun()


# ============================================================
# ROUND TRACKER
# ============================================================

def render_round_tracker():

    dots = ""


    for i in range(

        1,

        st.session_state.max_rounds + 1

    ):

        if i < st.session_state.round:

            cls = "done"

        elif i == st.session_state.round:

            cls = "now"

        else:

            cls = ""


        dots += (
            f'<div class="round-dot {cls}"></div>'
        )


    render_html(

        f"""
        <div class="round-tracker">

            {dots}

            <span class="round-number">

                ROUND {st.session_state.round}
                /
                {st.session_state.max_rounds}

            </span>

        </div>
        """

    )


# ============================================================
# SCORE DIAL
# ============================================================

def score_dial(score):

    score = float(score)

    radius = 26

    circumference = (
        2 * 3.14159 * radius
    )

    offset = circumference - (
        score / 10
    ) * circumference


    return f"""

    <div class="score-dial">

        <svg
            width="68"
            height="68"
            viewBox="0 0 68 68"
        >

            <circle
                class="score-track"
                cx="34"
                cy="34"
                r="{radius}"
            />

            <circle
                class="score-fill"
                cx="34"
                cy="34"
                r="{radius}"
                stroke-dasharray="{circumference}"
                stroke-dashoffset="{offset}"
            />

        </svg>


        <div class="score-number">
            {int(score)}
        </div>

    </div>

    """


# ============================================================
# TRANSCRIPT
# ============================================================

def render_round(item):

    result = item["result"]


    # ========================================================
    # USER ARGUMENT
    # ========================================================

    render_html(

        f"""
        <div class="bubble bubble-user">

            <div class="bubble-label">
                ✦ Your argument · Round {item['round']}
            </div>

            <div class="bubble-text">
                {html.escape(item['argument'])}
            </div>

        </div>
        """

    )


    # ========================================================
    # CHAMBER RESPONSE
    # ========================================================

    render_html(

        f"""
        <div class="bubble bubble-ai">

            <div class="bubble-label">
                ◈ The Chamber responds
            </div>

            <div class="bubble-text">
                {html.escape(
                    str(
                        result.get(
                            "rebuttal",
                            ""
                        )
                    )
                )}
            </div>


            <div class="ai-point">

                <div class="ai-point-label">

                    ◆ The Chamber's own point
                    ·
                    {html.escape(
                        st.session_state.ai_side
                    )}

                </div>


                <div class="bubble-text">

                    {html.escape(
                        str(
                            result.get(
                                "bot_point",
                                ""
                            )
                        )
                    )}

                </div>

            </div>

        </div>
        """

    )


    # ========================================================
    # SCORE
    # ========================================================

    score = result.get(
        "score",
        0
    )


    reason = result.get(
        "score_reason",
        ""
    )


    render_html(

        f"""
        <div class="score-card">

            {score_dial(score)}

            <div>

                <div class="score-label">
                    Score for your Round
                    {item['round']} argument
                </div>

                <div class="score-reason">
                    {html.escape(
                        str(reason)
                    )}
                </div>

            </div>

        </div>
        """

    )


# ============================================================
# SCREEN 3 — DEBATE
# ============================================================

def debate_screen():

    chamber_brand()


    render_html(

        f"""
        <div class="debate-header">

            <div>

                <div class="debate-resolution">
                    {html.escape(
                        st.session_state.topic
                    )}
                </div>

                <span class="side-tag
                    {
                        'side-for'
                        if st.session_state.user_side == 'FOR'
                        else 'side-against'
                    }">

                    {html.escape(
                        st.session_state.user_side
                    )}

                </span>

            </div>

        </div>
        """

    )


    render_round_tracker()


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # ========================================================
    # EXISTING TRANSCRIPT
    # ========================================================

    for item in st.session_state.history:

        render_round(item)


    # ========================================================
    # FINISHED
    # ========================================================

    if (
        st.session_state.round
        >
        st.session_state.max_rounds
    ):

        if st.button(

            "See final verdict →",

            use_container_width=True,

            type="primary",

            key="final_verdict",

        ):

            st.session_state.screen = "report"

            st.rerun()

        return


    # ========================================================
    # INPUT CARD
    # ========================================================

    render_html(

        f"""
        <div class="input-card">

            <div class="field-label">
                Your Round
                {st.session_state.round}
                argument
            </div>

        </div>
        """

    )


    # ========================================================
    # VOICE
    # ========================================================

    audio = st.audio_input(

        "🎙 Record your argument",

        key=f"voice_{st.session_state.round}",

    )


    if audio is not None:

        audio_bytes = audio.getvalue()


        if audio_bytes:

            audio_hash = hashlib.sha256(
                audio_bytes
            ).hexdigest()


            if (
                audio_hash
                !=
                st.session_state.last_audio_hash
            ):

                st.session_state.last_audio_hash = (
                    audio_hash
                )


                with st.spinner(
                    "The Chamber is transcribing your argument..."
                ):

                    transcript = (
                        transcribe_audio(audio)
                    )


                if transcript:

                    st.session_state.voice_text = (
                        transcript
                    )

                    st.session_state.argument_version += 1

                    st.rerun()


    if st.session_state.voice_status:

        render_html(

            f"""
            <div class="status">

                {html.escape(
                    st.session_state.voice_status
                )}

            </div>
            """

        )


    argument_key = (
        f"argument_{st.session_state.argument_version}"
    )


    argument = st.text_area(

        "Argument",

        value=st.session_state.voice_text,

        placeholder=(
            "Make your case...\n\n"
            "Speak using the microphone "
            "or type your argument here."
        ),

        height=130,

        label_visibility="collapsed",

        key=argument_key,

    )


    c1, c2 = st.columns([2, 1])


    with c1:

        submit = st.button(

            "Submit argument →",

            use_container_width=True,

            type="primary",

            key="submit_argument",

        )


    with c2:

        end = st.button(

            "End debate",

            use_container_width=True,

            key="end_debate",

        )


    if end:

        st.session_state.screen = "report"

        st.rerun()


    if submit:

        clean_argument = argument.strip()


        if not clean_argument:

            st.warning(
                "Make an argument before submitting."
            )

            return


        # ====================================================
        # THE CHAMBER ACTUALLY DEBATES HERE
        # ====================================================

        with st.spinner(
            "The Chamber is preparing its rebuttal..."
        ):

            result = debate_ai(
                clean_argument
            )


        completed_round = (
            st.session_state.round
        )


        st.session_state.history.append(

            {

                "round": completed_round,

                "argument": clean_argument,

                "result": result,

            }

        )


        st.session_state.scores.append(

            result.get(
                "score",
                0
            )

        )


        st.session_state.voice_text = ""

        st.session_state.voice_status = ""

        st.session_state.argument_version += 1


        if (
            completed_round
            >=
            st.session_state.max_rounds
        ):

            st.session_state.round = (
                st.session_state.max_rounds
                +
                1
            )

            st.session_state.screen = "report"

        else:

            st.session_state.round += 1


        st.rerun()


# ============================================================
# SCREEN 4 — FINAL VERDICT
# ============================================================

def report_screen():

    chamber_brand()


    st.title(
        "The Chamber's verdict"
    )


    st.markdown(

        f"""
        <div class="lede">

        "{html.escape(
            st.session_state.topic
        )}"

        — you argued
        {html.escape(
            st.session_state.user_side
        )}.

        </div>
        """,

        unsafe_allow_html=True,

    )


    # ========================================================
    # GENERATE REPORT
    # ========================================================

    if st.session_state.final_report is None:

        with st.spinner(
            "The Chamber is reviewing the full debate..."
        ):

            st.session_state.final_report = (
                generate_final_report()
            )


    report = (
        st.session_state.final_report
    )


    # ========================================================
    # AVERAGE
    # ========================================================

    scores = [

        float(x)

        for x in st.session_state.scores

    ]


    average = (

        sum(scores) / len(scores)

        if scores

        else 0

    )


    render_html(

        f"""
        <div class="verdict-card">

            <div class="verdict-score">

                {average:.1f}

                <span>/10</span>

            </div>

            <div class="verdict-label">
                Average round score
            </div>

            <div class="verdict-overview">

                {html.escape(
                    str(
                        report.get(
                            "overview",
                            ""
                        )
                    )
                )}

            </div>

        </div>
        """

    )


    # ========================================================
    # CORRECTIONS
    # ========================================================

    st.markdown(

        '<div class="section-label">'
        'ROUND-BY-ROUND CORRECTIONS'
        '</div>',

        unsafe_allow_html=True

    )


    corrections = report.get(
        "corrections",
        []
    )


    for correction in corrections:

        round_number = correction.get(
            "round",
            1
        )


        text = correction.get(
            "correction",
            ""
        )


        round_score = "?"


        if (

            round_number > 0

            and

            round_number <= len(
                st.session_state.history
            )

        ):

            round_score = (
                st.session_state.history[
                    round_number - 1
                ]["result"].get(
                    "score",
                    "?"
                )
            )


        render_html(

            f"""
            <div class="correction">

                <div class="correction-head">

                    <span class="round-badge">

                        ROUND
                        {round_number}

                    </span>

                    <span class="correction-score">

                        scored
                        {round_score}/10

                    </span>

                </div>

                <p>

                    {html.escape(
                        str(text)
                    )}

                </p>

            </div>
            """

        )


    # ========================================================
    # ROUND SCORES
    # ========================================================

    if st.session_state.scores:

        st.markdown(

            '<div class="section-label">'
            'ROUND SCORES'
            '</div>',

            unsafe_allow_html=True

        )


        for i, score in enumerate(

            st.session_state.scores,

            start=1

        ):

            render_html(

                f"""
                <div class="score-card">

                    {score_dial(score)}

                    <div>

                        <div class="score-label">
                            ROUND {i}
                        </div>

                        <div class="score-reason">
                            Argument strength:
                            {score}/10
                        </div>

                    </div>

                </div>
                """

            )


    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    if st.button(

        "Start a new debate",

        use_container_width=True,

        type="primary",

        key="new_debate",

    ):

        reset_app()


    render_html(

        """
        <div class="chamber-footer">
            The Chamber · DebateAI
        </div>
        """

    )


# ============================================================
# ROUTER
# ============================================================

if st.session_state.screen == "topic":

    topic_screen()


elif st.session_state.screen == "stance":

    stance_screen()


elif st.session_state.screen == "debate":

    debate_screen()


elif st.session_state.screen == "report":

    report_screen()