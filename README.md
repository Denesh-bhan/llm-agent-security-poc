# LLM & Agentic AI Security Testing Lab

A beginner-friendly defensive proof of concept for testing selected OWASP LLM and Agentic AI risks against Claude and Gemini using fictional data.

## Safety design
- Fake knowledge base and marker strings only (`SECRET-FLAG-123`, `INTERNAL-CONTEXT-MARKER-456`).
- Email capability creates a draft only; it cannot send.
- HTTP tool is a local mock and has no network client.
- File tool reads from an in-memory fake filesystem.
- Calculator accepts arithmetic AST nodes only; it never uses `eval`, `exec`, a shell, or OS commands.
- Do not add real secrets or real user data.

## 1. Install on Windows
Install Python 3.11 or newer from https://www.python.org/downloads/ and select **Add Python to PATH**.

Open PowerShell in this project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Configure API keys
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
notepad .env
```
Add your own Anthropic and Google API keys. Never commit `.env` to GitHub. The project can be explored without keys, but real model tests require valid provider keys and may incur charges.

## 3. Start the app
```powershell
streamlit run app.py
```
A browser tab should open at the local Streamlit address.

## 4. Run tests
Open **Run security tests**, select the configured models and phases, then start the suite.
- 30 test cases per model
- Before = baseline behavior
- After = hardened application behavior
- Full run = 120 model calls

The CSV is saved to `results/results.csv`. Review each response and correct any heuristic misclassification. A model response alone does not prove a tool action occurred; inspect tool execution logs separately.

## 5. Generate PDF report
After running tests:
```powershell
python generate_report.py
```
The report is saved to `reports/security_report.pdf`. Add your own manually reviewed analysis and model/version details before submission.

## Risks covered
| ID | Risk | Main mitigation in this POC |
|---|---|---|
| LLM01 | Prompt Injection | Treat user/retrieved content as untrusted; fixed system policy |
| LLM02 | Sensitive Information Disclosure | Data minimization; secret data excluded from hardened model context |
| LLM03 | Excessive Agency | Least privilege; no send capability; explicit authorization |
| LLM08 | Hidden Context Exposure | Do not put hidden/internal fields in model context |
| LLM10 | Improper Output Handling | Output checks and redaction before display/use |
| ASI01 | Agent Goal Hijack | Separate trusted policy from untrusted data |
| ASI02 | Tool Misuse | Tool registry and allowlists |
| ASI03 | Identity & Privilege Abuse | No admin identity; explicit authorization gates |
| ASI05 | Unexpected Code Execution | Arithmetic-only AST calculator; no arbitrary execution |
| ASI06 | Memory & Context Poisoning | No persistent writable agent memory; untrusted content labeling |

## Important methodology note
The automated classifier is deliberately simple and should be treated as triage, not ground truth. The assignment's Result field is `Blocked`, `Partial`, or `Succeeded`. Manually inspect outputs, especially cases where a model refuses in text but a separate application tool could still execute. Record actual tool events separately if extending the project.

## Suggested extensions
- Add structured JSON tool-call proposals and record every actual tool invocation.
- Add a Wazuh integration using a local JSONL event file as an intermediate.
- Add human-reviewed expected outcomes and per-risk evaluation rules.
- Pin exact model versions and SDK versions in the final report.

## GitHub checklist
- Commit source code, README, `.env.example`, and safe fake test data.
- Do not commit `.env`, API keys, or result files containing sensitive data.
- Include a screenshot of the dashboard and the manually reviewed PDF report.
