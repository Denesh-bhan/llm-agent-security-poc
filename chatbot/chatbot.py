import json
from pathlib import Path

KB_PATH = Path(__file__).with_name("knowledge_base.json")

def load_kb():
    return json.loads(KB_PATH.read_text(encoding="utf-8"))

def answer_prompt(prompt: str, provider: str, hardened: bool, ask_model):
    kb = load_kb()
    # Deliberately expose a fake context marker only in the baseline test fixture.
    context = json.dumps(kb if not hardened else {
        "company": kb["company"], "public_faq": kb["public_faq"]
    })
    wrapped = (
        f"Knowledge base context (untrusted data):\n{context}\n\n"
        f"User request:\n{prompt}"
    )
    if hardened:
        # The real enforcement is data minimization: secret/internal fields are not
        # placed in model context at all. The system prompt is defense-in-depth.
        pass
    return ask_model(provider, wrapped, hardened=hardened)
