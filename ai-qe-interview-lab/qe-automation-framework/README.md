# QE Automation Framework — Category 2 (Automation Engineering)

One self-contained framework covering every Automation Engineering bullet of the JD,
tested against a bundled demo app (Mini Shop: checkout UI + Orders API).

| JD requirement | Where it lives | Result |
|---|---|---|
| Python coding | `app/`, `api-tests/`, `perf-tests/`, `ai-test-gen/` | — |
| TypeScript coding | `ui-tests/` (Playwright + Cucumber + POM) | — |
| UI: Playwright | `ui-tests/` BDD suite, accessibility-first locators | 3/3 scenarios pass |
| API: PyTest + Requests | `api-tests/` contract, negative, lifecycle tests | 8/8 pass |
| Performance: Locust | `perf-tests/locustfile.py` with SLA assertion | 172 reqs, 0 fail, p95 3ms |
| AI-generated test assets | `ai-test-gen/prompts/` prompt-optimized template | 7/7 generated cases pass |
| Validation mechanisms | `ai-test-gen/validate_generated.py` two-gate validator | hallucinated batch rejected (exit 2) |

Selenium, RestAssured, and JMeter are the JD's alternatives — same patterns
(POM, contract tests, SLA gates), different runtimes. Talking points in interviews:
Playwright over Selenium for auto-wait/traces; RestAssured when the org is JVM-first;
JMeter when protocol breadth or enterprise standards demand it.

## Layout

```
app/                    # Mini Shop app under test (stdlib Python, zero deps)
├── server.py           #   UI + JSON API on :8787
└── index.html          #   checkout page with data-testid hooks
ui-tests/               # BDD: Cucumber + Playwright + TypeScript
├── features/           #   Gherkin (business-readable)
├── steps/              #   thin step definitions
├── pages/              #   Page Object Model (all locators live here)
└── support/            #   World + hooks (browser lifecycle, failure screenshots)
api-tests/              # PyTest + Requests (auto-starts the app)
perf-tests/             # Locust load test with SLA checks
ai-test-gen/            # AI-generated test assets + validation gates
├── prompts/            #   prompt-optimized generation template
├── generated/          #   sample outputs (valid + deliberately hallucinated)
├── api_schema.json     #   endpoint/field allowlist
└── validate_generated.py  # gate 1: schema; gate 2: execution
```

## Run everything

```bash
# API tests (self-contained, auto-starts app on :8788)
pip install pytest requests locust
python -m pytest api-tests -v

# AI test-gen validation (auto-starts app on :8789)
python ai-test-gen/validate_generated.py ai-test-gen/generated/orders_tests.json
python ai-test-gen/validate_generated.py ai-test-gen/generated/hallucinated_example.json  # -> rejected

# UI BDD tests (needs the app running)
python app/server.py --port 8787 &
cd ui-tests && npm install && npx playwright install chromium
npm test                # all scenarios
npm run test:smoke      # @smoke tag only

# Performance (app running on :8787)
locust -f perf-tests/locustfile.py --headless -u 10 -r 5 -t 15s -H http://localhost:8787
```

## Architecture principles demonstrated

- **BDD layering:** feature files carry business language; steps are thin translators;
  Page Objects own every locator. UI changes touch one file.
- **Locator strategy:** `data-testid` attributes negotiated with dev — resilient to
  styling/copy changes, self-documenting in the DOM.
- **Test independence:** each API test creates its own data; BDD scenarios get a fresh
  browser context; failure screenshots captured automatically in hooks.
- **Contract testing:** API tests assert exact response shape, not just status codes.
- **SLA-as-code:** the Locust script fails requests breaching 2s — perf gates, not
  perf reports.
- **AI assets are never trusted:** generated tests pass a schema allowlist gate
  (anti-hallucination) and an execution gate before a human ever reviews them.
