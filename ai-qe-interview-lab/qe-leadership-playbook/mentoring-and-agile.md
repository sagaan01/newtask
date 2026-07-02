# Mentoring Plan & Agile Operation

## Mentoring: making AI adoption a skill, not a mandate

**Structure:**
- **QE guild** (bi-weekly, 45 min): one topic, hands-on, using this repo's lab
  projects as exercises — e.g. "break the retrieval and watch the eval gate
  catch it" beats any slide deck.
- **Champions model:** one volunteer per squad gets deeper enablement and
  first-line-support duty; architects scale through champions, not heroics.
- **Pairing rotations:** architect pairs with each squad 2h/sprint on their
  actual hardest test problem — credibility is built in their codebase, not mine.

**Curriculum (maps to the lab projects):**
1. Prompt engineering + guardrails (qe-copilot llm_client)
2. RAG concepts + when NOT to use AI (qe-copilot knowledge_base)
3. TypeScript/Playwright framework patterns (typescript-playwright-concepts)
4. AI-generated tests + validation gates (ai-test-gen)
5. Reading eval metrics; contributing golden cases (both evaluate.py files)

**Handling resistance (the real leadership work):**
- Name the fear directly: "AI replaces QA" -> show the advisory-only policy and
  the human-owned decision list in writing (ai-governance.md).
- Give skeptics the QA job on the AI itself: designing golden sets and breaking
  the copilot is real QE work, and converts critics into the system's best testers.
- Publish the toil metric: hours on log-digging before/after. Reinvest saved
  time visibly in exploratory testing and design reviews, not headcount math.

## Agile/Scrum operation

- **QE is in refinement, not after it:** acceptance criteria drafted as Gherkin
  during refinement; untestable stories bounce before sprint start.
- **Definition of Done includes:** automated tests at the right pyramid layer,
  eval gate green if AI components changed, no new quarantined tests without tickets.
- **Vertical slicing:** platform features ship as thin end-to-end slices
  (e.g. "triage summaries for ONE squad's nightly run"), not horizontal layers
  that demo nothing.
- **Sprint ceremonies:** architect attends squad standups on rotation;
  runs the weekly triage; demos platform increments in sprint review like any
  other team — the QE platform is a product with users, not a shared chore.

## Collaboration with developers, SMEs, product

- **Developers:** locator contract (data-testid), contract-test ownership at the
  API boundary, shared flaky-fix rotation.
- **SMEs:** own the golden datasets — their judgment becomes the AI's exam.
- **Product:** risk tiers negotiated openly (what gets deep testing and why);
  quality KPIs on the same dashboard as delivery KPIs.
