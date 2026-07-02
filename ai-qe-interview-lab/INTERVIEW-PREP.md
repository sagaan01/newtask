# FINAL INTERVIEW PREP — One-Stop Mock Quiz (All Categories, Basics Up)

Every answer is written in the ARCHITECT voice: outcome first, "we" not "I did
a script", trade-offs named, evidence cited. Each answer ends with PROOF - the
artifact in this repo you can point to.

---

## HOW TO SOUND LIKE AN ARCHITECT, NOT AN ENGINEER (read first)

| Engineer says | Architect says |
|---|---|
| "I wrote a script that..." | "We removed X hours of toil per sprint by..." |
| "I used ChromaDB" | "I chose an embedded vector store for the prototype and designed the swap path to OpenSearch for scale" |
| "The model gets 0.83 accuracy" | "We gate every AI change on measured accuracy - regression fails the build, same as code" |
| "AI generates the tests" | "AI drafts, gates validate, humans own the merge - autonomy is earned by evidence" |
| "That's a dev problem" | "I negotiated the contract at the boundary: devs own X, QE owns Y" |
| "It works" | "It's green in CI and here are the numbers" |

Three rules: (1) lead with the business outcome, (2) name the trade-off you
considered, (3) end with evidence.

---

# CATEGORY 1 — AI, LLMs & AGENTIC SYSTEMS

**Q1. What is an LLM?**
A model trained to predict the next token over huge text corpora - it writes
and reasons in language, but knows nothing about OUR product until we supply
context. My whole architecture follows from that one limitation: RAG for facts,
guardrails for trust. PROOF: qe-copilot exists because of this gap.

**Q2. What is a prompt, and what is prompt engineering?**
The instruction contract with the model. Engineering it means: fixed role,
explicit constraints, structured output, and versioning prompts in Git like
code - because a prompt change is a behavior change and must be regression-tested.
PROOF: `qe-copilot/src/llm_client.py` TRIAGE_PROMPT - role + "context only" +
fixed 3-section output + temperature 0.

**Q3. What is an embedding?**
A numeric fingerprint of meaning - similar meanings land close together.
It's what lets us search by concept instead of keyword. Layman: GPS coordinates
for sentences. PROOF: "refund stuck in pending" retrieved FLA-004 ("asserted
final state without polling") with almost zero shared words.

**Q4. What is a vector database?**
A store optimized for "find the nearest meanings fast." I used embedded
ChromaDB to prototype and designed for pgvector/OpenSearch at scale - the
retrieval pattern is identical, only the engine grows. PROOF:
`qe-copilot/src/knowledge_base.py`.

**Q5. What is RAG and why does it matter for QE?**
Retrieve relevant documents first, then generate an answer grounded in them.
It turns "have we seen this failure before?" - 60% of triage time - into a
two-second lookup, with citations so engineers can verify instead of trust.
PROOF: retrieval precision@3 = 1.0 on the golden set.

**Q6. RAG vs fine-tuning - when each?**
RAG when facts change (specs, incidents - every sprint); fine-tuning when
STYLE must be consistent and facts are stable. RAG also gives citations, which
is a governance requirement for us, not a nice-to-have. PROOF: adding one JSON
record updates the copilot's knowledge - no retraining.

**Q7. What is hallucination and your defense-in-depth?**
Plausible-but-false output. Six layers: grounding (RAG), prompt constraint
("do not invent"), temperature 0, mandatory citations, confidence routing to
humans, and advisory-only outputs. No single lock - a stack. PROOF: every
qe-copilot report carries cited incident IDs + the advisory flag.

**Q8. What is an AI agent vs a script?**
An agent chooses its path at runtime based on its own self-assessment; a
script executes a fixed sequence. Mine has one real decision: confident ->
recommend a CI action; uncertain -> route to a human. Minimal, deliberate,
and architected to grow. PROOF: conditional edge in
`qe-copilot/src/agent_graph.py`.

**Q9. LangChain vs LangGraph vs AutoGen vs CrewAI?**
LangChain: composition utilities - I use its prompt templates. LangGraph:
explicit state machines - my choice for CI-grade determinism, retries, audit.
AutoGen: multi-agent conversation - exploratory analysis. CrewAI: role-based
teams. I pick by workflow shape, and I'm honest when plain code is enough.
PROOF: LangGraph runs the triage graph; LangChain only supplies the template.

**Q10. What is MCP?**
An open standard for exposing tools to any LLM client - the universal socket.
Build the tool once with governance (least privilege, audit), and Cursor,
Claude, or a CI agent can all call it. PROOF: `qe-copilot/mcp_server.py` -
three tools, docstrings become the tool contracts.

**Q11. How do you evaluate an AI system?**
Like software: a golden set with expected answers, separate metrics per
component (retrieval precision@3, classification accuracy), thresholds, and a
gate that fails the build on regression. If you can't measure it, you can't
ship it. PROOF: `qe-copilot/src/evaluate.py` - exit 1 blocks deploy;
currently 1.0 / 0.83.

**Q12. Tell me about a time evaluation changed your design.**
The zero-shot classifier looked fine until measurement showed ~0.22-confidence
wrong answers on short error strings. We made it hybrid - trust the model above
a threshold, deterministic rules below. The eval drove the architecture; that's
its job. PROOF: HF_MIN_CONFIDENCE in `qe-copilot/src/classifier.py`.

**Q13. OpenAI vs Ollama - how and when?**
Same client, one env var - Ollama serves an OpenAI-compatible endpoint. Cloud
for reasoning power; local for sensitive data, cost, and vendor-outage
resilience. Making it a config decision means governance can choose per
workload. PROOF: LLM_BASE_URL switch in `qe-copilot/src/llm_client.py`.

**Q14. Reduce token cost?**
Three levers in order: fewer tokens (4 of my 5 pipeline stages never touch an
LLM), cheaper models (route by complexity, local for bulk), fewer calls
(dedup repeated failures, semantic cache, batch APIs). And govern it: token
spend belongs in the eval gate. PROOF: qe-copilot's classify/retrieve/route
stages are all local and free.

---

# CATEGORY 2 — AUTOMATION ENGINEERING

**Q15. What is test automation, really?**
Encoding quality checks so machines repeat them cheaply and honestly. The
strategic value isn't speed - it's that every merge gets the same scrutiny,
which changes team behavior. PROOF: whole `qe-automation-framework`.

**Q16. Explain the test pyramid.**
Many fast unit tests (dev-owned), fewer API/contract tests (QE-architected),
fewest E2E (business-critical journeys only). I enforce it economically: E2E
is expensive to own, so it must earn its place. PROOF: 8 API tests vs 3 BDD
scenarios - deliberate ratio.

**Q17. What is BDD and why use it?**
Behavior-Driven Development: scenarios in business language (Gherkin) that
execute as tests. The value is shared ownership - product can read and
challenge our coverage. It's a collaboration tool that happens to run.
PROOF: `ui-tests/features/checkout.feature`.

**Q18. What is the Page Object Model?**
All locators and UI mechanics live in page classes; tests speak business
actions. When the UI changes, one file changes - maintainability is the whole
game at scale. PROOF: `ui-tests/pages/CheckoutPage.ts`; steps contain zero
selectors by policy.

**Q19. What's your locator strategy?**
data-testid attributes, negotiated with developers as a contract: rename it
and you know you're breaking tests. Immune to styling and copy changes.
Role-based locators second - they double as accessibility checks.
PROOF: `app/index.html` + every locator in CheckoutPage.

**Q20. Playwright vs Selenium?**
Playwright for greenfield: auto-wait kills the biggest flake class, traces cut
triage, one API for three engines. Selenium when the estate demands it (Grid
investment, legacy). The patterns - POM, contracts - survive either choice.

**Q21. What is an API contract test?**
Asserting the exact response shape, not just the status code - so a breaking
change fails at the API layer in seconds, not in a UI test an hour later.
PROOF: `test_create_order_returns_201_with_contract` asserts
`set(body.keys()) == {id, email, total, status}`.

**Q22. How do you design performance testing?**
SLAs as code, not reports: define p95/error-rate targets, fail requests that
breach them, run a perf smoke in CI for critical paths, full load tests
scheduled. PROOF: `perf-tests/locustfile.py` marks >2s responses as failures;
last run 172 requests, 0 failures, p95 3ms.

**Q23. How do you handle flaky tests?**
Policy, not heroics: quarantine within 24h WITH a ticket (quarantine without a
ticket is where tests go to die), root-cause by class (timing/data/env), and an
ML ranker for the review queue. PROOF: flaky policy in
`qe-leadership-playbook/quality-strategy.md` + the ml-qe-pipeline predictor.

**Q24. How do you let AI write tests safely?**
AI drafts; gates validate; humans merge. Gate 1: schema allowlist - invented
endpoints reject the batch before anything runs. Gate 2: execution against a
live API. Then PR review. PROOF: the hallucinated batch is rejected with
exit 2 - and our CI asserts that rejection happens.

**Q25. What makes a framework "architected" vs "written"?**
Layers with contracts: config, clients, page/service objects, business flows,
thin tests. Anyone can add a test without touching plumbing; plumbing can
change without touching tests. PROOF: framework layout in
`qe-automation-framework/README.md`.

---

# TYPESCRIPT (asked with Category 2)

**Q26. Why TypeScript for test automation?**
It moves a whole class of bugs from runtime - where they look like flaky
tests - to compile time. In a large suite that converts triage hours into red
squiggles, and makes refactoring 200 usages safe. PROOF:
`typescript-playwright-concepts` - tsc clean, 9/9 tests.

**Q27. What's an interface, in testing terms?**
An executable API contract. If the response shape changes, tests fail to
COMPILE - we learn about breaking changes at build time, not from red CI.
PROOF: `src/types.ts` Order interface.

**Q28. What's a generic? Example?**
A type the caller fills in - one ApiClient serves every endpoint with typed
responses and zero casts. Layman: a labeled shipping container - same box,
label says what's inside. PROOF: `api.post<Order>(...)` in
`tests/api.spec.ts`.

**Q29. Type guard? `unknown` vs `any`?**
A guard is a runtime check that TEACHES the compiler ("after this if, body is
ApiError"). `any` disables safety; `unknown` demands proof before use - that
discipline is why we use it at boundaries. PROOF: `isApiError()` in types.ts.

**Q30. What are Playwright fixtures?**
Typed dependency injection: tests declare what they need in the signature and
receive constructed objects; setup/teardown lives once. PROOF:
`fixtures.ts` test.extend<QEFixtures>.

---

# CATEGORY 3 — ML/AI ENGINEERING & DATA PIPELINES

**Q31. Supervised learning in one line + our use case?**
Learn a mapping from labeled examples. Ours: test-execution features ->
is-flaky label, so machines rank the flaky-review queue and humans decide.
PROOF: `ml-qe-pipeline/src/train.py`.

**Q32. What are features? Which mattered most?**
The measurable signals the model learns from. rerun_pass_rate dominated
(importance 0.35) - failures that pass on rerun are the strongest flakiness
smell. That's a domain insight, not just a number. PROOF: feature importances
printed by train.py.

**Q33. Train/test split and why a FIXED holdout?**
Never grade a model on data it trained on. Our holdout is fixed (seed 777)
and never trained on, so champion and challenger are compared on identical
ground - no metric gaming. PROOF: `data/eval_holdout.csv` creation in
generate_data.py.

**Q34. Precision vs recall vs F1 - and which matters here?**
Precision: of flagged, how many were right. Recall: of actual, how many we
caught. For flaky-flagging, precision wins - a false quarantine hides real
regressions - so thresholds tune toward precision and humans own quarantine.
PROOF: evaluate.py reports all three; v2 precision 0.78.

**Q35. What is model versioning / a registry?**
Every trained model is an immutable, numbered artifact with its metrics and
lineage; a champion pointer says what's live. Change management for models,
same as tags for releases. PROOF: `models/registry.json` - v1 retired, v2
champion, metrics attached.

**Q36. Champion/challenger - explain like I'm product.**
The new model doesn't ship because its trainer likes it - it takes the same
exam as the current model on the same fixed questions, and only wins by
scoring at least as well. Layman: promotion by standardized test.
PROOF: retrain run - v2 (0.746) beat v1 (0.738), promoted; exit-code contract.

**Q37. What is drift and how do you respond?**
The world changes under the model - new frameworks, new infra - so yesterday's
patterns mislead. Response: scheduled retraining on fresh data, gated by
champion/challenger so a bad retrain can't ship. PROOF: `retrain.py` simulates
drift and the gate decides.

**Q38. Scikit-learn vs PyTorch - your honest take?**
We ran both on the same holdout: forest 0.746, small neural net 0.774 -
same band. I'd ship the forest: no feature scaling, instant training,
explainable importances. Model choice follows data shape and operating cost,
not hype. PROOF: `torch_model.py` comparison output.

**Q39. Walk me through your embedding pipeline.**
Ingest -> redact PII -> sentence-aware chunking (NLTK) with metadata ->
embed -> retrieval with optional metadata filtering. Redaction comes BEFORE
embedding because you cannot un-embed a leaked email - stage order IS the
security control. PROOF: `embedding_pipeline.py` - 3 PII values caught,
precision@1 4/4.

**Q40. What is retrieval optimization?**
Making the right chunk come back first, cheaply: chunking that follows meaning,
metadata pre-filters to shrink the candidate set, hybrid search and rerankers
at scale - each validated against a golden set, never guessed. PROOF: stage 5
plain-vs-filtered comparison.

---

# CATEGORY 4 — CLOUD, DEVOPS & INTEGRATION

**Q41. What is CI/CD, in outcome terms?**
Continuous Integration: every change is built and tested automatically -
quality scrutiny becomes uniform. Continuous Delivery: the path to production
is automated with gates. The outcome is trust at speed. PROOF: our live
pipeline - 7 jobs green on GitHub Actions.

**Q42. What is a quality gate?**
A deterministic pass/fail checkpoint with an exit-code contract. My rule: AI
informs gates, deterministic logic decides them. PROOF: six gates in
`.github/workflows/qe-pipeline.yml`, including two AI-quality gates.

**Q43. Why parallel jobs?**
Independent gates have no ordering dependency, so feedback time is the max
(~44s), not the sum. Sequencing is reserved for true dependencies.
PROOF: workflow structure + the aggregated report job with needs: [...].

**Q44. The most senior thing in your pipeline?**
We test the governance itself: a job asserts the hallucinated test batch gets
REJECTED (exit 2). If anyone weakens the schema gate, CI goes red. Layman:
the building inspection presses the smoke detector's test button.
PROOF: ai-testgen-validation job.

**Q45. GitHub Actions vs Jenkins vs Azure DevOps?**
Actions for GitHub-native teams - marketplace, OIDC, zero infra. Jenkins for
on-prem, plugin-heavy estates you operate yourself. Azure DevOps for
Microsoft-integrated shops. I wrote the same gates in all three dialects -
pipeline design should be tool-portable. PROOF: `qe-devops-pipeline/`
Jenkinsfile + azure-pipelines.yml.

**Q46. How do you handle secrets in CI?**
Identity over keys: CI assumes a cloud role via OIDC federation - no static
credentials to leak or rotate. Third-party keys live in a secrets manager,
never in prompts, never in the repo. PROOF: security section of
`cloud-architecture.md`; the pipeline itself needs zero secrets by design.

**Q47. Map your platform to AWS.**
ChromaDB -> OpenSearch + Titan embeddings on Bedrock; LangGraph -> Step
Functions + Lambda; MCP servers -> Fargate with task-role IAM; model registry
-> SageMaker; retraining cron -> EventBridge; observability -> CloudWatch with
token-spend alarms. Same patterns, managed engines. PROOF:
`cloud-architecture.md` mapping table (+ Azure/GCP columns).

**Q48. "Scalable, secure, governed" - your controls?**
Least privilege per tool (the BigQuery-reader role can't touch S3), VPC
endpoints so AI traffic never crosses public internet, PII redaction in the
ingest path, cost alarms, full audit of agent tool calls, and a three-tier
environment strategy ending with prod as advisory-only + human release
authority. PROOF: cloud-architecture.md security section maps each control
to a lab implementation.

---

# CATEGORY 5 — LEADERSHIP & DELIVERY EXCELLENCE

**Q49. Your leadership philosophy in one sentence?**
Automate toil, not judgment; expand AI autonomy only as evidence accumulates;
make every policy cheap to follow and expensive to ignore. PROOF: it's the
opening line of the playbook - and every project implements it.

**Q50. How would you roll out AI across QE teams?**
Four phases - Assist, Recommend, Act-with-supervision, Autonomous - each with
MEASURED exit criteria (e.g. Phase 1 exits at 30% triage-time reduction and
0.8 retrieval precision). Autonomy is earned by metrics, and release authority
is permanently human - policy, not a maturity gap. PROOF:
`ai-adoption-roadmap.md`.

**Q51. A team fears AI will replace them. What do you do?**
Name the fear in writing (the governance doc lists human-owned decisions),
publish the toil metric so saved time visibly funds better work - and give
skeptics the QA job on the AI itself: designing golden sets and breaking the
copilot is real QE work that converts critics into the system's best testers.
PROOF: resistance section of `mentoring-and-agile.md`.

**Q52. How do you run defect triage?**
AI prepares, humans decide: the copilot clusters overnight failures into root
causes with citations BEFORE the 15-minute meeting; humans set priority by
blast radius. Feedback loop: misclassifications become eval cases, confirmed
causes feed the knowledge base - the system learns from every meeting.
PROOF: `triage-and-prioritization.md` + the copilot that does the pre-work.

**Q53. How do you prioritize platform investment?**
Score = Impact x Feasibility x Risk-reduction / Cost - as a debate anchor, not
a verdict. And the discipline that matters: any pilot that can't beat its
baseline in 4-6 weeks is killed. Cheap kills are how you afford many bets.
PROOF: worked scoring table - summarization (60) shipped first, autonomous
authoring (4) deferred.

**Q54. How do you work with developers / product / SMEs?**
Contracts at boundaries: devs own unit tests + the data-testid locator
contract; QE owns API contract and E2E layers; SMEs own the golden datasets -
their judgment becomes the AI's exam; product negotiates risk tiers openly so
testing depth is transparent and challengeable. PROOF: collaboration section
of mentoring-and-agile.md.

**Q55. How do you operate in Agile/Scrum as an architect?**
QE joins refinement, not after it - untestable stories bounce before sprint
start. Definition of Done includes right-layer tests, green eval gate if AI
changed, and no quarantine without a ticket. The platform ships vertical
slices demoed in review - it's a product with users, not a shared chore.
PROOF: Agile section of mentoring-and-agile.md.

**Q56. How do you measure YOUR success?**
Triage time, escape-defect rate, eval metrics per release, cost per PR, and
engineer satisfaction - the last because adoption is a people problem. I put
quality KPIs on the same dashboard as delivery KPIs so quality is never a
side conversation. PROOF: KPI table in ai-adoption-roadmap.md.

**Q57. Tell me about something you'd do differently.**
Honest gaps, proactively: I'd build the golden eval set on day one instead of
after the first classifier surprise; I'd add a similarity floor so retrieval
says "no precedent" instead of returning weak matches; and I'd wire the
feedback loop (confirmed resolutions auto-append to the KB) earlier - learning
loops compound. PROOF: the classifier war story is in the code
(HF_MIN_CONFIDENCE).

**Q58. Compliance and AI - what does the auditor see?**
Citations on every answer, a versioned model registry, engine/mode fields on
every output, prompt versions in Git, tool-call audit logs, and PII redacted
before it can enter a vector store. Traceability is architecture here, not
paperwork. PROOF: governance rules 2, 4, 7, 8 in ai-governance.md - each
mapped to an implementation.

---

## THE NUMBERS CARD (memorize cold)

| Number | What it is |
|---|---|
| 1.0 | retrieval precision@3, copilot golden set |
| 0.83 | classification accuracy (and the honest 1-miss story) |
| 8/8, 3/3, 9/9 | API tests, BDD scenarios, TypeScript tests |
| 172 / 0 / 3ms | perf requests / failures / p95 |
| exit 2 | hallucinated batch rejection (and CI asserts it) |
| 0.746 vs 0.738 | v2 beat v1 -> promoted by the gate |
| 0.774 | PyTorch MLP on same holdout (honest comparison) |
| 3 | PII values redacted before embedding |
| 7/7 green | live GitHub Actions pipeline jobs |
| 30% / 0.8 | Phase 1 exit criteria (triage time / precision) |

## THE FIVE SENTENCES THAT WIN THE ROOM

1. "We test the AI with the same discipline we test software."
2. "Autonomy is earned by evidence, and release authority stays human - permanently."
3. "AI drafts, gates validate, humans merge."
4. "You cannot un-embed a leaked email - stage order is the security control."
5. "Any pilot that can't beat its baseline in six weeks gets killed - cheap kills are how you afford many bets."
