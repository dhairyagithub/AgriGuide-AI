# AgriGuide AI — KJS-AGR-01

A small end-to-end Generative AI sugarcane irrigation chatbot using Streamlit,
Google's Gemini API, and a transparent keyword-based agricultural knowledge base.

## What it does

1. Accepts a user's question in a Streamlit chat interface.
2. Retrieves up to three relevant entries from `knowledge_base.py`.
3. sends the question and retrieved source context to an existing LLM.
4. Displays the generated answer in the chat interface.

This is a student educational prototype, not a validated irrigation controller.
It does not calculate a verified field-specific water quantity.

## 1. Get an API key

Create a Gemini API key in Google AI Studio:
https://aistudio.google.com/app/apikey

Check the current model availability and API limits in the official Gemini documentation:
https://ai.google.dev/gemini-api/docs/get-started

## 2. Install dependencies

Use Python 3.10+ in a terminal, inside this project folder:

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Then run:

```bash
pip install -r requirements.txt
```

## 3. Configure the API key

Create `.streamlit/secrets.toml` (copy the example file and rename it), then set:

```toml
GEMINI_API_KEY = "paste-your-key-here"
GEMINI_MODEL = "gemini-2.5-flash"
```

If that model is not available to your API key, choose a currently available text-generation model from your Google AI Studio/API documentation and change `GEMINI_MODEL`.

Do not upload `secrets.toml` to GitHub. It is included in `.gitignore`.

## 4. Run the app

```bash
streamlit run app.py
```

Open the local URL printed in the terminal, normally http://localhost:8501.

## 5. Basic tests

Run:

```bash
python -m unittest discover -s tests -v
```

These tests check that the local retrieval component returns relevant entries and that sources have URLs. They do not test the quality or factual correctness of generated answers.

## 6. Manual test questions

Try these in the chat:
- What factors should I check before irrigating sugarcane?
- Why does crop growth stage matter for irrigation?
- Does one irrigation schedule work for every location?
- Is excessive irrigation always beneficial?
- Can you give an exact number of litres per day for my field?

Expected behavior:
- Answers should mention factors such as soil moisture, crop stage, rainfall, soil type, weather and irrigation method when relevant.
- The chatbot should avoid unsupported exact water quantities and explain that field-specific recommendations need local validation.
- The answer should not present the sample dataset's precomputed predictions as verified ground truth.

## 7. Deploy on Streamlit Community Cloud

1. Create a GitHub repository and upload the project files, excluding `.streamlit/secrets.toml`.
2. Go to https://share.streamlit.io/ and choose **Create app**.
3. Select your repository, branch, and `app.py` as the main file.
4. Open **Advanced settings → Secrets** and paste:

```toml
GEMINI_API_KEY = "paste-your-key-here"
GEMINI_MODEL = "gemini-2.5-flash"
```

5. Deploy and test the public app URL.

Official instructions:
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management

## Knowledge sources included

- TNAU, Irrigation Management: Sugarcane
  https://www.agritech.tnau.ac.in/agriculture/agri_irrigationmgt_sugarcane.html
- TNAU Expert System for Sugarcane
  https://agritech.tnau.ac.in/expert_system/sugar/irrigationmanagement.html
- ICAR, Scheduling of irrigation for sugarcane
  https://epubs.icar.org.in/index.php/IJAgS/article/view/27734
- ICAR, Ikshu Kedar: mobile app for sugarcane water productivity
  https://epubs.icar.org.in/index.php/IndFarm/article/view/133002

## Viva explanation in one minute

"AgriGuide AI is a Generative AI chatbot for the KJS-AGR-01 sugarcane irrigation use case. The frontend is built with Streamlit. When a user asks a question, a simple keyword-retrieval function selects relevant summaries from a small knowledge base based on TNAU and ICAR sources. The selected context and question are sent to an existing Gemini language model through its API. The model generates a natural-language answer, which is displayed in the chat interface. We did not fine-tune or train an LLM. We use retrieval and prompting to ground the answer in reference material. The prototype avoids unsupported exact water quantities because irrigation depends on local soil, weather, rainfall, crop stage and field conditions."
