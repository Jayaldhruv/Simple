# 🧠 SIMP — Smart Institutional Memory Pipeline

> Before you build, know what was already tried.

SIMP is an AI-native system that gives Wealthsimple's engineering and product teams 
instant access to the organization's decision history — what was tried, what failed, 
why it failed, and who to talk to before repeating the same mistakes.

Built for the Wealthsimple AI Builder application.

---

## The Problem It Solves

Wealthsimple moves fast. Reorgs happen. Teams merge. Context disappears.

Right now, when a PM proposes "let's redesign onboarding" or "let's rebuild fraud detection 
with ML," there is no system that says: *"We tried that 8 months ago. Here's why it failed. 
Here are the assumptions you're making that aren't true anymore. Here's who still has context."*

SIMP rebuilds that memory as infrastructure.

---

## The Three Demo Moments

**Moment 1 — "We already tried this"**  
Query: "We want to redesign onboarding with social login"  
→ SIMP surfaces the OAuth/FINTRAC failure from March 2023, exactly why it was blocked, and the 6 weeks of lost engineering time.

**Moment 2 — "This assumption is no longer true"**  
Query: "Let's build ML-based fraud detection"  
→ SIMP surfaces the shipped v1 model but flags: *"Transaction volume is 3x since training — model may be drifting."*

**Moment 3 — "Here's who has context on this"**  
Every result surfaces the 2-3 people who were in the room when the decision was made — before the reorg scattered them.

---

## Setup

```bash
# 1. Clone / copy files
cd simp

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Anthropic API key (for AI reasoning layer)
export ANTHROPIC_API_KEY=your_key_here

# 4. Run
streamlit run app.py
```

App opens at http://localhost:8501

---

## Architecture

```
User query (natural language)
        │
        ▼
ChromaDB vector search
(semantic similarity over 12 institutional decisions)
        │
        ▼
Retrieve top-5 relevant decisions
        │
        ├── Classify: previously attempted / stale assumptions / people
        │
        ▼
Claude reasoning layer
(synthesizes: what matters most, what assumption to check, who to talk to)
        │
        ▼
Streamlit UI (3 killer moments displayed in sequence)
```

## What AI Is Responsible For
- Semantic retrieval (finding relevant decisions even if query wording differs)
- Synthesizing patterns across multiple past decisions
- Flagging which assumptions are most likely stale
- Recommending the right person to talk to first

## What Must Stay Human
**Deciding what to actually do.**  
SIMP never recommends a course of action. It surfaces context. The PM or engineering lead decides whether to proceed, pivot, or dig deeper. That judgment call — especially in a regulated financial environment — cannot be automated.

## What Would Break First at Scale
The synthetic dataset has 12 decisions. Real deployment needs a pipeline that ingests 
Jira tickets, GitHub PR descriptions, Slack decision threads, and Confluence pages 
continuously. The quality of retrieval is only as good as the quality of what gets 
captured — which means humans need to form a habit of writing decisions into the system, 
or an ingestion agent needs to extract them automatically. That ingestion layer is the 
hardest part at scale.

---

## Tech Stack
- **Python** — backend logic
- **ChromaDB** — local vector database for semantic search
- **Anthropic Claude API** — reasoning and synthesis layer  
- **Streamlit** — UI (fast, functional, ships in days not weeks)
- **sentence-transformers** — embedding model for ChromaDB

---

*Built in 3 days. Designed to run in production.*
