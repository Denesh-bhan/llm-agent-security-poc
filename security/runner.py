import json, csv
from pathlib import Path
from datetime import datetime, timezone
from models.providers import ask_model
from security.mitigations import sanitize_user_prompt, output_is_safe, redact_secrets, evaluate_result

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "attacks" / "test_cases.json").read_text(encoding="utf-8"))

def run_suite(providers=("Claude", "Gemini"), modes=("Before", "After"), progress=None):
    rows = []
    total = len(CASES) * len(providers) * len(modes)
    done = 0
    for provider in providers:
        for mode in modes:
            hardened = mode == "After"
            for case in CASES:
                prompt = case["prompt"]
                model_prompt = sanitize_user_prompt(prompt) if hardened else prompt
                try:
                    response = ask_model(provider, model_prompt, hardened=hardened)
                    if hardened and not output_is_safe(response):
                        response = redact_secrets(response)
                    result = evaluate_result(case["risk_id"], response, hardened)
                    error = ""
                except Exception as exc:
                    response, result, error = "", "Partial", str(exc)
                rows.append({
                    "Timestamp_UTC": datetime.now(timezone.utc).isoformat(),
                    "Phase": mode, "Risk_ID": case["risk_id"],
                    "Risk": case["risk_name"], "Case_ID": case["case_id"],
                    "Model": provider, "Prompt": prompt, "Result": result,
                    "Response": response[:1200], "Error": error
                })
                done += 1
                if progress:
                    progress(done / total)
    out = ROOT / "results" / "results.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows, out
