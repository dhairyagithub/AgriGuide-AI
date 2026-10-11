"""Small, transparent keyword-retrieval knowledge base for AgriGuide AI."""

SOURCES = [
    {
        "name": "Tamil Nadu Agricultural University (TNAU) — Irrigation Management: Sugarcane",
        "url": "https://www.agritech.tnau.ac.in/agriculture/agri_irrigationmgt_sugarcane.html",
    },
    {
        "name": "TNAU Expert System for Sugarcane — Irrigation Management",
        "url": "https://agritech.tnau.ac.in/expert_system/sugar/irrigationmanagement.html",
    },
    {
        "name": "ICAR — Scheduling of irrigation for sugarcane",
        "url": "https://epubs.icar.org.in/index.php/IJAgS/article/view/27734",
    },
    {
        "name": "ICAR — Ikshu Kedar mobile app for sugarcane water productivity",
        "url": "https://epubs.icar.org.in/index.php/IndFarm/article/view/133002",
    },
]

DOCUMENTS = [
    {
        "id": "tnau_stages",
        "name": SOURCES[0]["name"],
        "url": SOURCES[0]["url"],
        "keywords": ["stage", "growth", "germination", "tillering", "grand growth", "maturity", "schedule", "interval"],
        "content": (
            "TNAU explains that sugarcane irrigation should depend on crop phase. "
            "Its guidance describes germination, tillering, grand-growth and maturity "
            "phases. Example irrigation intervals differ by soil texture; the page "
            "lists different intervals for sandy and clay soils. These are regional "
            "reference values, not universal prescriptions. Adjust for rainfall, "
            "local conditions, and current extension advice."
        ),
    },
    {
        "id": "tnau_factors",
        "name": SOURCES[1]["name"],
        "url": SOURCES[1]["url"],
        "keywords": ["soil", "moisture", "rain", "rainfall", "weather", "temperature", "evaporation", "water requirement", "drought"],
        "content": (
            "Sugarcane water needs vary with agro-climatic conditions, soil type, "
            "planting method, crop stage, weather and rainfall. Hot weather and dry "
            "winds can increase water demand. The guidance warns that both water "
            "shortage and waterlogging can harm the crop. Check field soil moisture "
            "and recent rainfall rather than relying on a fixed schedule alone."
        ),
    },
    {
        "id": "tnau_methods",
        "name": SOURCES[0]["name"],
        "url": SOURCES[0]["url"],
        "keywords": ["drip", "irrigation method", "sprinkler", "furrow", "flood", "water saving", "efficiency"],
        "content": (
            "TNAU discusses different irrigation approaches, including sprinkler "
            "irrigation during early stages and drip irrigation. The appropriate "
            "method and amount depend on field layout, soil, crop phase, available "
            "water and local recommendations. Avoid assuming that one method or "
            "schedule fits every farm."
        ),
    },
    {
        "id": "icar_schedule",
        "name": SOURCES[2]["name"],
        "url": SOURCES[2]["url"],
        "keywords": ["region", "climate", "location", "schedule", "water requirement", "weather data"],
        "content": (
            "An ICAR-published study reports that irrigation schedules and water "
            "requirements for sugarcane varied substantially among Indian locations "
            "because climate and local conditions differ. This supports treating "
            "irrigation schedules as location-dependent rather than using one "
            "nationwide fixed quantity."
        ),
    },
    {
        "id": "icar_ict",
        "name": SOURCES[3]["name"],
        "url": SOURCES[3]["url"],
        "keywords": ["technology", "mobile app", "advisory", "water productivity", "sensor", "decision support"],
        "content": (
            "ICAR has described ICT tools for improving sugarcane irrigation "
            "scheduling and water productivity. A decision-support chatbot should "
            "help users review relevant factors and trusted guidance; it should not "
            "claim to replace field measurements or local agricultural expertise."
        ),
    },
]


def _tokens(text):
    """Simple tokenization; no extra NLP library is required."""
    return {
        word.strip(".,?!:;()[]{}'\"").lower()
        for word in text.split()
        if len(word.strip(".,?!:;()[]{}'\"")) > 2
    }


def retrieve_context(query, top_k=3):
    """Return the top matching knowledge entries using keyword overlap."""
    query_tokens = _tokens(query)
    scored = []
    for doc in DOCUMENTS:
        searchable = " ".join(doc["keywords"]) + " " + doc["content"]
        score = len(query_tokens & _tokens(searchable))
        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]
