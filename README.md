# 🧠 SIMP — Smart Institutional Memory Pipeline

> *Before you build, know what was already tried.*

---

## The Problem

Wealthsimple moves fast. Reorgs happen. Teams merge. Context disappears.

A PM proposes redesigning the onboarding flow. Nobody in the room knows it was tried 8 months ago and killed by a FINTRAC compliance issue that cost 6 weeks of engineering time. The debate happens again. The prototype gets built again. Compliance blocks it again.

This isn't a people problem. It's an infrastructure problem. **Organizational memory has never been treated as a system.**

Every company that has survived a reorg, a leadership change, or a fast hiring sprint has the same wound: the reasoning behind past decisions lives in people's heads, not in any tool. When those people move teams, the knowledge walks out with them. What remains is a Jira ticket marked "closed" with no explanation of why.

SIMP fixes this. It is the first system that captures not just *what* was decided, but *why* — and surfaces that context automatically, at the exact moment a team is about to repeat a mistake.

---

## What SIMP Does

You type a proposal — *"we want to redesign the onboarding flow"* or *"let's rebuild fraud detection with ML"* — and SIMP tells you in seconds:

**1. Whether the org has already tried this — and what happened**
Not a keyword search. Meaning-based retrieval. If you type "reduce signup friction," it finds the OAuth onboarding failure even though those words don't appear in the original decision record.

**2. Which assumptions your predecessors made that may no longer be true**
The world changes. A decision made in 2022 rested on assumptions about FINTRAC rules, transaction volume, or team capacity that may have shifted. SIMP flags these explicitly so you check before you commit.

**3. Who still has context on this**
People who were in the room when the original decision was made. Before you write a single line of code or schedule a single design sprint, SIMP tells you who to have coffee with first.

---

## The Three Demo Moments

### Moment 1 — "We already tried this"
Query: *"We want to redesign onboarding with social login"*

SIMP surfaces the OAuth/FINTRAC failure from March 2023. The team built a prototype, ran an A/B test on 2,000 users, and got blocked by regulatory 2 weeks before launch. 6 weeks of engineering time. Gone. SIMP shows you this before you open a Jira ticket.

### Moment 2 — "This assumption is no longer true"
Query: *"Let's rebuild our fraud detection system with ML"*

SIMP surfaces the shipped v1 model — but immediately flags: *"Transaction volume is 3x since this model was trained. Check for drift before extending this work."* The decision was right at the time. The context has changed. SIMP knows the difference.

### Moment 3 — "Here's who to talk to"
Every result surfaces the people who were involved in the original decision. Not org chart titles. Actual humans with actual context, ranked by how many related decisions they touched. Before the reorg scattered them, they knew things that aren't written down anywhere. SIMP finds them for you.

---

## What the Human Can Now Do

A PM or engineering lead can walk into a planning session with full organizational context on any topic — in under 30 seconds. Without SIMP, gathering that same context requires hunting through old Jira tickets, asking around Slack, and hoping someone remembers. That process takes days if it happens at all. Usually it doesn't happen, and the team finds out the hard way.

With SIMP, the question *"has anyone looked at this before?"* gets answered before the meeting starts.

---

## What AI Is Responsible For

- **Semantic retrieval** — finding relevant past decisions even when the query uses completely different words than the original record
- **Pattern recognition across results** — identifying which decisions are related and why
- **Synthesis** — reading multiple past decisions and producing a single coherent briefing that surfaces what matters most
- **Assumption staleness detection** — flagging which historical assumptions are most likely to have shifted given the current query

---

## Where AI Must Stop

**SIMP never recommends a course of action.**

It surfaces context. It does not decide. A PM reading SIMP's output about a failed onboarding attempt still has to judge whether the conditions that caused that failure still apply today, whether the risk is worth taking again, and whether this is the right moment to try. Those judgments require accountability to real people — clients whose money is at stake, regulators who set the rules, colleagues who will build the thing.

That accountability cannot be automated. The human decides. SIMP informs.

This is especially true in a regulated financial environment. A system that *recommended* courses of action based on past decisions would need to be audited, validated, and potentially licensed. A system that *surfaces context* for humans to act on is a productivity tool. The line between those two things is the most important design decision in SIMP.

---

## What Would Break First at Scale

The synthetic dataset has 12 decisions. Real deployment at Wealthsimple means tens of thousands of decisions across Jira, GitHub, Slack, and Confluence — accumulated over a decade.

**The ingestion problem is the hardest part.**

Right now, a human has to write a structured decision record. At scale, that habit either needs to become part of how Wealthsimple closes Jira tickets and merges PRs, or an ingestion agent needs to extract decision records automatically from existing tools. The second option is technically harder but more realistic — you cannot ask 400 engineers to change how they close tickets.

The second thing that would break is **retrieval quality**. With 12 decisions, almost every query finds something relevant. With 50,000 decisions, the signal-to-noise ratio degrades. The embedding model and retrieval strategy would need to evolve — likely toward a hybrid of semantic search and structured filtering by team, date range, and domain.

The third is **trust**. SIMP only works if people believe what it surfaces is accurate and complete. If it misses a relevant decision once and a team wastes two months as a result, confidence collapses. Accuracy of the memory is as important as the intelligence of the retrieval.

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run
streamlit run app.py
```

Opens at `http://localhost:8501`. No API key required. Runs fully offline.

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| UI | Streamlit | Ships in hours, not weeks |
| Vector database | ChromaDB | Local, fast, semantic search |
| Embedding model | sentence-transformers | Converts text to meaning |
| Language | Python | Fast to write, easy to read |

---

## Architecture

```
User types a proposal
        │
        ▼
ChromaDB converts query to numbers (embeddings)
and finds the most semantically similar past decisions
        │
        ▼
Results filtered into three buckets:
  - Previously attempted (failed / rejected / abandoned)
  - Stale assumptions flagged
  - People with context
        │
        ▼
Synthesis layer reads buckets and writes briefing:
  most important thing → assumption to verify → who to talk to
        │
        ▼
Streamlit UI displays three moments in sequence
```

---

## Why This Matters for Wealthsimple Specifically

Wealthsimple's own employees describe the same pattern repeatedly: reorgs that scatter context, debates that repeat themselves, velocity that creates debt. The company is navigating the transition from startup to institution — and that transition has a specific failure mode: moving fast enough to keep growing while losing enough memory to keep making the same mistakes.

Legacy banks like RBC and TD are slow partly because of bureaucracy, but partly because they have decades of institutional memory baked into their processes. Wealthsimple cannot afford the bureaucracy. But it also cannot afford to keep paying the tax of forgotten context.

SIMP is the infrastructure that lets Wealthsimple have both: the velocity of a startup with the memory of an institution.

---

*Built in 3 days. Designed to run in production.*
*SIMP — Smart Institutional Memory Pipeline*
