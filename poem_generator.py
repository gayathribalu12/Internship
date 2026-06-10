import streamlit as st
from huggingface_hub import InferenceClient

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="✦ Poem Generator",
    page_icon="✦",
    layout="centered",
)

# ══════════════════════════════════════════════════════════════════════════════
#  👇 PASTE YOUR HUGGINGFACE MODEL ID HERE (e.g. "mistralai/Mistral-7B-Instruct-v0.3")
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
# ══════════════════════════════════════════════════════════════════════════════

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500&display=swap');

  :root {
    --ink:    #1a1a2e;
    --parchm: #f5f0e8;
    --gold:   #c9a84c;
    --mist:   #e8e0d0;
    --soft:   #6b6570;
  }

  html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--parchm) !important;
    font-family: 'Inter', sans-serif;
    color: var(--ink);
  }

  [data-testid="stHeader"]  { background: transparent !important; }
  [data-testid="stToolbar"] { display: none; }

  /* Hero */
  .hero { text-align: center; padding: 3rem 0 1.5rem; }
  .hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem; font-weight: 700;
    color: var(--ink); letter-spacing: -0.02em; margin-bottom: 0.3rem;
  }
  .hero h1 span { color: var(--gold); font-style: italic; }
  .hero p {
    font-size: 1rem; color: var(--soft); font-weight: 300;
    letter-spacing: 0.06em; text-transform: uppercase;
  }

  /* Divider */
  .divider { width: 60px; height: 2px; background: var(--gold); margin: 0 auto 2rem; }

  /* Section labels */
  .input-label {
    font-family: 'Inter', sans-serif; font-size: 0.75rem; font-weight: 500;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--soft); margin-bottom: 0.4rem;
  }

  /* All text inputs — white background fix */
  [data-testid="stTextInput"] input,
  [data-testid="stTextInput"] input[type="password"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1rem !important;
    border: 1.5px solid var(--mist) !important;
    border-radius: 6px !important;
    background: #ffffff !important;
    color: var(--ink) !important;
    padding: 0.5rem 0.8rem !important;
    box-shadow: none !important;
  }
  [data-testid="stTextInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
  }

  /* Slider & selectbox labels */
  [data-testid="stSlider"] label,
  [data-testid="stSelectbox"] label {
    font-size: 0.75rem !important; letter-spacing: 0.1em !important;
    text-transform: uppercase !important; color: var(--soft) !important;
  }

  /* Generate button */
  .stButton > button {
    width: 100%;
    background: var(--ink) !important; color: #ffffff !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.8rem !important;
    font-weight: 500 !important; letter-spacing: 0.15em !important;
    text-transform: uppercase !important; border: none !important;
    border-radius: 6px !important; padding: 0.85rem !important;
    transition: background 0.2s !important;
  }
  .stButton > button:hover {
    background: var(--gold) !important; color: var(--ink) !important;
  }

  /* Poem output box */
  .poem-box {
    background: #ffffff;
    border-left: 3px solid var(--gold);
    border-radius: 0 8px 8px 0;
    padding: 1.8rem 2rem;
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem; line-height: 2;
    color: var(--ink); white-space: pre-wrap; margin-top: 0.5rem;
  }

  /* Expander */
  [data-testid="stExpander"] {
    border: 1px solid var(--mist) !important;
    border-radius: 8px !important; background: #ffffff !important;
  }

  /* Footer */
  .footer {
    text-align: center; padding: 2rem 0 1rem;
    font-size: 0.75rem; color: var(--soft); letter-spacing: 0.08em;
  }
</style>
""", unsafe_allow_html=True)


# ── Style prompts ──────────────────────────────────────────────────────────────
STYLE_PROMPTS = {
    "Free Verse": "Write a vivid, emotional free-verse poem about",
    "Haiku":      "Write a haiku (5-7-5 syllables) about",
    "Sonnet":     "Write a Shakespearean sonnet about",
    "Limerick":   "Write a humorous limerick about",
    "Ode":        "Write a lyrical ode celebrating",
}


def build_prompt(style: str, topic: str) -> str:
    prefix = STYLE_PROMPTS.get(style, "Write a poem about")
    return (
        f"[INST] {prefix} '{topic}'. "
        f"Write only the poem — no title, no explanation, just the verses. [/INST]\n\n"
    )


def generate_poem(token: str, topic: str, max_tokens: int, style: str) -> str:
    client = InferenceClient(token=token)
    prompt = build_prompt(style, topic)

    response = client.text_generation(
        prompt,
        model=MODEL_ID,
        max_new_tokens=max_tokens,
        temperature=0.9,
        top_p=0.92,
        repetition_penalty=1.3,
        do_sample=True,
    )

    poem = response.strip()

    # Remove prompt echo if model repeats it
    if poem.startswith(prompt.strip()):
        poem = poem[len(prompt.strip()):].strip()

    # Trim at last clean sentence end
    for end in [".", "!", "?"]:
        idx = poem.rfind(end)
        if idx > len(poem) // 2:
            poem = poem[: idx + 1]
            break

    return poem if poem else "Could not generate a poem. Try a different topic or style."


# ── UI ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>✦ <span>Poem</span> Generator</h1>
  <p>Craft poetry with artificial imagination</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# HF Token
st.markdown('<p class="input-label">HuggingFace API Token</p>', unsafe_allow_html=True)
hf_token = st.text_input(
    label="hf_token",
    type="password",
    placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxx  —  get yours at huggingface.co/settings/tokens",
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)

# Topic
st.markdown('<p class="input-label">Topic or Inspiration</p>', unsafe_allow_html=True)
topic = st.text_input(
    label="topic",
    placeholder="e.g. the monsoon, a forgotten city, longing…",
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)

# Options
with st.expander("⚙  Options", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("Poetry Style", list(STYLE_PROMPTS.keys()))
    with col2:
        max_tokens = st.slider("Length (tokens)", min_value=60, max_value=300, value=150, step=10)

st.markdown("<br>", unsafe_allow_html=True)

# Generate button
if st.button("Generate Poem ✦"):
    if not hf_token.strip():
        st.warning("Please enter your HuggingFace API token.")
    elif not topic.strip():
        st.warning("Please enter a topic to inspire the poem.")
    else:
        with st.spinner("Composing your poem…"):
            try:
                poem = generate_poem(hf_token.strip(), topic.strip(), max_tokens, style)
                st.markdown("### Your Poem")
                st.markdown(f'<div class="poem-box">{poem}</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="⬇  Download as .txt",
                    data=f"Topic: {topic}\nStyle: {style}\nModel: {MODEL_ID}\n\n{poem}",
                    file_name=f"poem_{topic[:20].replace(' ', '_')}.txt",
                    mime="text/plain",
                )
            except Exception as e:
                err = str(e)
                if "401" in err or "unauthorized" in err.lower():
                    st.error("❌ Invalid token. Check your HuggingFace API token and try again.")
                elif "loading" in err.lower() or "503" in err:
                    st.info("⏳ Model is loading on HuggingFace servers — wait ~20 seconds and try again.")
                else:
                    st.error(f"❌ Error: {err}")

st.markdown(
    '<div class="footer">Powered by HuggingFace Inference API · Streamlit</div>',
    unsafe_allow_html=True,
)
