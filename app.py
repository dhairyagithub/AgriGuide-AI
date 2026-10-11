import os
import streamlit as st
from google import genai
from knowledge_base import retrieve_context, SOURCES

st.set_page_config(page_title="AgriGuide AI", page_icon="🌱", layout="centered")

st.title("🌱 AgriGuide AI")
st.caption("Generative AI sugarcane irrigation assistant · KJS-AGR-01")

with st.sidebar:
    st.header("About this project")
    st.write(
        "AgriGuide AI combines an existing language model with a small, "
        "source-based sugarcane irrigation knowledge base."
    )
    st.markdown("**What it can help with**")
    st.write("- Irrigation concepts and crop stages")
    st.write("- Factors to check before irrigating")
    st.write("- Waterlogging, rainfall, and soil-moisture questions")
    st.markdown("**Important limitation**")
    st.write(
        "This is an educational prototype, not a validated irrigation controller. "
        "Confirm field-specific decisions with local agricultural experts."
    )
    st.markdown("**Knowledge sources**")
    for source in SOURCES:
        st.markdown(f"- [{source['name']}]({source['url']})")

def get_secret(name, default=""):
    value = os.getenv(name, default)
    try:
        value = st.secrets.get(name, value)
    except Exception:
        pass
    return value

api_key = get_secret("GEMINI_API_KEY")
model_name = get_secret("GEMINI_MODEL", "gemini-2.5-flash")

if not api_key:
    st.info(
        "To enable responses, add your Gemini API key to "
        "`.streamlit/secrets.toml`. See the README for setup instructions."
    )
    st.code('GEMINI_API_KEY = "paste-your-key-here"\\nGEMINI_MODEL = "gemini-2.5-flash"', language="toml")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask about sugarcane irrigation…")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    matched_docs = retrieve_context(question, top_k=3)
    context_text = "\n\n".join(
        f"Source: {doc['name']}\nGuidance summary: {doc['content']}\nURL: {doc['url']}"
        for doc in matched_docs
    )
    if not context_text:
        context_text = (
            "No directly matching entry was found in the local knowledge base. "
            "Be transparent about this and avoid inventing a specific recommendation."
        )

    recent_history = st.session_state.messages[-7:-1]
    history_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in recent_history
    )

    prompt = f"""
You are AgriGuide AI, an educational assistant for the KJS-AGR-01 sugarcane
irrigation advisory use case.

Rules:
1. Use the supplied source summaries as your primary agricultural context.
2. Do not invent exact litres/day, irrigation quantities, or sensor thresholds.
3. Irrigation needs depend on local weather, rainfall, soil type, crop stage,
   irrigation method, and actual soil moisture.
4. If the context does not support a precise answer, say so and suggest checking
   with a local agricultural officer or extension service.
5. Distinguish general guidance from a field-specific recommendation.
6. Keep the answer clear, practical, and concise.
7. Never claim that you measured the user's field or verified the dataset's
   predicted values.
8. When useful, name the source and include its URL.

Relevant agricultural context:
{context_text}

Recent conversation:
{history_text}

User question:
{question}

Answer in simple language. Give a short checklist when appropriate.
"""

    with st.chat_message("assistant"):
        with st.spinner("Preparing an answer…"):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                answer = (response.text or "").strip()
                if not answer:
                    answer = (
                        "I couldn't generate a response this time. Please try "
                        "rephrasing your question."
                    )
            except Exception as exc:
                answer = (
                    "I couldn't reach the language model. Check your API key, "
                    "model name, internet connection, and API usage limits. "
                    f"\n\nTechnical detail: `{type(exc).__name__}: {exc}`"
                )
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.messages:
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()
