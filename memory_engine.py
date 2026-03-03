"""
SIMP — Memory Engine
Handles storage, retrieval, and AI reasoning over institutional decisions.
Uses ChromaDB for vector search + OpenRouter LLM for synthesis.
"""

import os
import requests
import chromadb
from chromadb.utils import embedding_functions

# ── OpenRouter config ─────────────────────────────────────────────────────────
# Get a free key at openrouter.ai → Dashboard → API Keys
# Then: export OPENROUTER_API_KEY=your_key_here
#
# Free models that work well:
#   "meta-llama/llama-3.1-8b-instruct:free"
#   "mistralai/mistral-7b-instruct:free"
#   "google/gemma-2-9b-it:free"
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL   = os.environ.get("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")


SYNTHETIC_DECISIONS = [
    # ── ONBOARDING ────────────────────────────────────────────────────────────
    {
        "id": "onb-001",
        "title": "Social login onboarding (Google/Apple OAuth)",
        "domain": "Onboarding",
        "date": "March 2023",
        "outcome": "rejected",
        "what_happened": "Team proposed replacing email/password signup with OAuth-only (Google + Apple) to reduce onboarding friction. Built a prototype, ran A/B test on 2,000 users.",
        "why_failed": "Regulatory flagged it: FINTRAC KYC rules require collecting specific identity fields that OAuth tokens don't surface. Legal blocked the rollout 2 weeks before launch. 6 weeks of engineering time lost.",
        "alternatives_rejected": ["Hybrid flow (OAuth + identity questions)", "Progressive identity collection post-signup"],
        "assumptions": ["OAuth tokens contain sufficient KYC data", "Regulatory review would happen post-launch"],
        "assumptions_stale": ["FINTRAC rules may have updated — re-verify with compliance before any auth change"],
        "people": ["Priya Mehta (PM)", "Jordan Lee (Eng Lead)", "Sarah Okonkwo (Compliance)"],
        "tags": ["onboarding", "auth", "oauth", "kyc", "compliance", "signup", "friction"],
        "search_text": "onboarding social login oauth google apple signup friction KYC identity"
    },
    {
        "id": "onb-002",
        "title": "Single-page onboarding flow redesign",
        "domain": "Onboarding",
        "date": "August 2023",
        "outcome": "shipped",
        "what_happened": "Collapsed 7-step onboarding into a single scrollable page with inline validation. Reduced drop-off by 34%. Shipped to 100% of users by Sept 2023.",
        "why_failed": None,
        "alternatives_rejected": ["Progressive disclosure (step-by-step wizard)", "Conversational onboarding (chatbot style)"],
        "assumptions": ["Users prefer fewer screens over granular progress indicators", "Inline validation reduces error rate"],
        "assumptions_stale": [],
        "people": ["Priya Mehta (PM)", "Amara Singh (Design)", "Felix Oduya (Frontend)"],
        "tags": ["onboarding", "ux", "drop-off", "conversion", "redesign", "single-page"],
        "search_text": "onboarding redesign drop-off conversion UX single page flow friction reduce"
    },
    {
        "id": "onb-003",
        "title": "Pre-fill onboarding from CRA MyAccount data",
        "domain": "Onboarding",
        "date": "January 2024",
        "outcome": "abandoned",
        "what_happened": "Explored using CRA MyAccount API to pre-populate SIN, address, and income data during TFSA/RRSP account opening. Would have cut form completion time by ~60%.",
        "why_failed": "CRA's API is not open to private fintechs — only banks with Schedule I status. Wealthsimple doesn't qualify. This was discovered after 3 weeks of API integration work.",
        "alternatives_rejected": ["Screen scraping (illegal)", "Asking users to manually upload NOA"],
        "assumptions": ["CRA API is accessible to registered fintechs", "Users comfortable sharing CRA credentials"],
        "assumptions_stale": ["CRA open banking API timeline may have shifted — check federal open banking roadmap"],
        "people": ["Jordan Lee (Eng Lead)", "Tanvir Ahmed (Backend)", "Aisha Fernandez (PM)"],
        "tags": ["onboarding", "cra", "prefill", "open banking", "tfsa", "rrsp", "data"],
        "search_text": "onboarding prefill CRA MyAccount government data autofill account opening TFSA RRSP"
    },
    {
        "id": "onb-004",
        "title": "Reduce onboarding drop-off with progress persistence",
        "domain": "Onboarding",
        "date": "November 2022",
        "outcome": "shipped",
        "what_happened": "Users who started onboarding but didn't finish were losing all progress on app close. Implemented server-side draft state so users resume exactly where they left off. Completion rate +18%.",
        "why_failed": None,
        "alternatives_rejected": ["Local storage only (lost on reinstall)", "Email reminders to complete"],
        "assumptions": ["Users abandon due to friction, not disinterest", "Resume flow is technically simple to add"],
        "assumptions_stale": [],
        "people": ["Felix Oduya (Frontend)", "Tanvir Ahmed (Backend)", "Priya Mehta (PM)"],
        "tags": ["onboarding", "drop-off", "persistence", "resume", "completion", "ux"],
        "search_text": "onboarding drop-off persistence resume state completion rate reduce friction"
    },

    # ── FRAUD DETECTION ───────────────────────────────────────────────────────
    {
        "id": "fraud-001",
        "title": "ML-based transaction fraud scoring (v1)",
        "domain": "Fraud Detection",
        "date": "June 2022",
        "outcome": "shipped",
        "what_happened": "Replaced rule-based fraud flags with a gradient boosted model trained on 18 months of transaction history. False positive rate dropped from 12% to 3.4%. Now flags ~40 suspicious transactions/day for human review.",
        "why_failed": None,
        "alternatives_rejected": ["Pure rules engine (too brittle)", "Third-party vendor (Kount, Sift) — cost and data ownership concerns"],
        "assumptions": ["Internal data sufficient to train model", "3.4% false positive acceptable to ops team"],
        "assumptions_stale": ["Transaction volume 3x since training — model may be drifting, check AUC monthly"],
        "people": ["Kofi Asante (ML Eng)", "Maria Chen (Data Science)", "Devon Walsh (Fraud Ops)"],
        "tags": ["fraud", "ml", "machine learning", "transactions", "model", "scoring", "detection"],
        "search_text": "fraud detection machine learning model transactions scoring ML gradient boost"
    },
    {
        "id": "fraud-002",
        "title": "Real-time device fingerprinting for account takeover",
        "domain": "Fraud Detection",
        "date": "February 2023",
        "outcome": "shipped",
        "what_happened": "Integrated device fingerprinting (via internal JS library) to detect when known fraudsters use new devices. Reduced account takeover incidents by 61% in first 90 days.",
        "why_failed": None,
        "alternatives_rejected": ["Hardware-based attestation (Android only)", "IP-only blocking (too many false positives)"],
        "assumptions": ["Fraudsters reuse device signatures", "JS fingerprinting not easily spoofed at scale"],
        "assumptions_stale": ["Browser privacy changes (Firefox/Safari) may degrade fingerprint accuracy — audit quarterly"],
        "people": ["Lena Park (Security Eng)", "Kofi Asante (ML Eng)", "Devon Walsh (Fraud Ops)"],
        "tags": ["fraud", "security", "device", "fingerprinting", "account takeover", "ATO"],
        "search_text": "fraud account takeover device fingerprint security detection ATO"
    },
    {
        "id": "fraud-003",
        "title": "AI document verification for identity fraud",
        "domain": "Fraud Detection",
        "date": "September 2023",
        "outcome": "rejected",
        "what_happened": "Evaluated building in-house document verification (passport/DL scanning + liveness check) to replace our Jumio contract. Prototype reached 91% accuracy on clean scans.",
        "why_failed": "91% accuracy sounds good but means ~1 in 11 legitimate users get incorrectly flagged or passed. At our volume that's hundreds of daily errors. Jumio reaches 99.3%. Compliance also flagged that in-house models require annual OSFI validation — expensive. Shelved.",
        "alternatives_rejected": ["Hybrid (Jumio for edge cases only)", "Open source OCR + custom liveness model"],
        "assumptions": ["91% accuracy would be acceptable at our volume", "OSFI validation would not apply to internal tools"],
        "assumptions_stale": ["Jumio contract renewal coming Q2 2025 — renegotiate before rebuilding in-house"],
        "people": ["Maria Chen (Data Science)", "Sarah Okonkwo (Compliance)", "Lena Park (Security Eng)"],
        "tags": ["fraud", "identity", "document verification", "kyc", "liveness", "jumio", "ocr"],
        "search_text": "fraud identity verification document passport liveness check KYC in-house build vs buy"
    },
    {
        "id": "fraud-004",
        "title": "Behavioral biometrics for continuous auth",
        "domain": "Fraud Detection",
        "date": "May 2024",
        "outcome": "abandoned",
        "what_happened": "Researched typing cadence and swipe pattern analysis to continuously authenticate users without re-prompting. Proof of concept worked in lab conditions.",
        "why_failed": "Privacy legal review concluded this constitutes continuous biometric surveillance under PIPEDA. Storing behavioral patterns requires explicit user consent + right to deletion infrastructure we don't have. Estimated 6 months of compliance work before we could ship anything.",
        "alternatives_rejected": ["Opt-in only rollout", "Anonymized aggregate patterns only"],
        "assumptions": ["Behavioral data collection is covered under existing privacy policy", "Users would consent if asked"],
        "assumptions_stale": ["PIPEDA reform (Bill C-27 / CPPA) still moving through Parliament — rules may change"],
        "people": ["Kofi Asante (ML Eng)", "Sarah Okonkwo (Compliance)", "Ravi Nair (Legal)"],
        "tags": ["fraud", "biometrics", "behavioral", "privacy", "pipeda", "continuous auth", "security"],
        "search_text": "fraud behavioral biometrics continuous authentication privacy PIPEDA typing swipe pattern"
    },

    # ── MOBILE / ARCHITECTURE ─────────────────────────────────────────────────
    {
        "id": "mob-001",
        "title": "React Native to Flutter migration assessment",
        "domain": "Mobile Architecture",
        "date": "October 2022",
        "outcome": "rejected",
        "what_happened": "Engineering assessed full migration of our React Native app to Flutter after performance complaints on Android. 3-week technical spike.",
        "why_failed": "Estimated 18 months of migration work for a team of 8. Performance gains were real (~20% faster render) but not worth the opportunity cost. We had 3 major product launches planned. Decision: optimize RN instead of migrating.",
        "alternatives_rejected": ["Gradual migration screen by screen", "Flutter for new features only (brownfield)"],
        "assumptions": ["18 months estimate is accurate", "Performance is the primary user complaint driver"],
        "assumptions_stale": ["React Native has had major architecture updates (New Architecture/JSI) since this assessment — re-benchmark before any migration discussion"],
        "people": ["Felix Oduya (Frontend)", "Jordan Lee (Eng Lead)", "Amara Singh (Design)"],
        "tags": ["mobile", "react native", "flutter", "migration", "android", "performance", "architecture"],
        "search_text": "React Native Flutter migration mobile app android performance architecture rewrite"
    },
    {
        "id": "mob-002",
        "title": "Offline mode for portfolio viewing",
        "domain": "Mobile Architecture",
        "date": "March 2023",
        "outcome": "shipped",
        "what_happened": "Cached last-known portfolio state locally so users can open the app without connectivity and see their holdings. Uses Redis-backed sync on reconnect.",
        "why_failed": None,
        "alternatives_rejected": ["PWA offline (web only)", "Full offline trading (regulatory complexity too high)"],
        "assumptions": ["Users want to check portfolios in low-connectivity situations (subway, travel)", "Stale data is acceptable if clearly labeled"],
        "assumptions_stale": [],
        "people": ["Tanvir Ahmed (Backend)", "Felix Oduya (Frontend)", "Aisha Fernandez (PM)"],
        "tags": ["mobile", "offline", "cache", "portfolio", "ux", "connectivity"],
        "search_text": "offline mode mobile portfolio cache viewing connectivity low signal"
    },
    {
        "id": "mob-003",
        "title": "Microservices split: monolith decomposition phase 1",
        "domain": "Mobile Architecture",
        "date": "January 2024",
        "outcome": "shipped",
        "what_happened": "Extracted authentication and notification services from the Rails monolith into standalone services. Reduced deploy frequency conflicts and enabled per-service scaling. Phase 2 (trading engine extraction) planned for H2 2024.",
        "why_failed": None,
        "alternatives_rejected": ["Full big-bang rewrite", "Strangler fig pattern starting with trading engine"],
        "assumptions": ["Auth and notifications are the lowest-risk extraction candidates", "Phase 2 timeline realistic given current team size"],
        "assumptions_stale": ["Phase 2 was originally scoped for H2 2024 — confirm status before planning anything that depends on trading engine being a separate service"],
        "people": ["Jordan Lee (Eng Lead)", "Tanvir Ahmed (Backend)", "Kofi Asante (ML Eng)"],
        "tags": ["architecture", "microservices", "monolith", "rails", "decomposition", "backend", "scaling"],
        "search_text": "microservices monolith decomposition Rails backend architecture scaling services split"
    },
    {
        "id": "mob-004",
        "title": "Real-time push notifications for price alerts",
        "domain": "Mobile Architecture",
        "date": "July 2023",
        "outcome": "shipped",
        "what_happened": "Replaced polling-based price alerts with WebSocket push via our notification service. Latency dropped from ~45s to <2s. Used by 38% of active users within first month.",
        "why_failed": None,
        "alternatives_rejected": ["Server-Sent Events (iOS background restrictions)", "Increased polling frequency (too expensive at scale)"],
        "assumptions": ["WebSocket connections scale within our AWS Lambda + Redis setup", "Users want real-time over battery savings"],
        "assumptions_stale": [],
        "people": ["Tanvir Ahmed (Backend)", "Lena Park (Security Eng)", "Aisha Fernandez (PM)"],
        "tags": ["mobile", "notifications", "push", "websocket", "real-time", "price alerts"],
        "search_text": "push notifications real-time price alerts WebSocket mobile app latency"
    },
    {
        "id": "mob-005",
        "title": "Spending insights AI feature (cancelled)",
        "domain": "Mobile Architecture",
        "date": "November 2023",
        "outcome": "abandoned",
        "what_happened": "PM proposed an AI-powered monthly spending insights feature — categorize transactions, surface anomalies, suggest savings opportunities. Design was well-received in user research.",
        "why_failed": "Deprioritized during a reorg. The team owning transaction data was merged into the banking product team. New leadership wanted to focus on RRSP contribution tooling for tax season. Work was 60% complete. No handoff document was created. The Figma files and prototype exist but the context for why certain categorization decisions were made is lost.",
        "alternatives_rejected": ["Partner with Mint/YNAB", "Lightweight version (manual categories only)"],
        "assumptions": ["Feature would ship before reorg", "Context would be transferred during team merge"],
        "assumptions_stale": ["This work is 60% done — before re-scoping, find Figma files and talk to Aisha Fernandez who was the original PM"],
        "people": ["Aisha Fernandez (PM)", "Maria Chen (Data Science)", "Amara Singh (Design)"],
        "tags": ["spending", "insights", "ai", "categorization", "transactions", "reorg", "abandoned"],
        "search_text": "spending insights AI categorization transactions savings feature mobile reorg abandoned"
    },
]


class MemoryEngine:
    def __init__(self):
        self.client = chromadb.Client()
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="simp_decisions",
            embedding_function=self.ef
        )
        self.decisions = {}
        self._loaded = False

    def load_synthetic_data(self):
        if self._loaded:
            return
        for d in SYNTHETIC_DECISIONS:
            self.decisions[d["id"]] = d
            try:
                self.collection.add(
                    ids=[d["id"]],
                    documents=[d["search_text"] + " " + d["title"] + " " + d["what_happened"]],
                    metadatas=[{"domain": d["domain"], "outcome": d["outcome"]}]
                )
            except Exception:
                pass
        self._loaded = True

    def count(self):
        return len(SYNTHETIC_DECISIONS)

    def search(self, query: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, len(SYNTHETIC_DECISIONS))
        )
        ids = results["ids"][0] if results["ids"] else []
        return [self.decisions[i] for i in ids if i in self.decisions]

    def _call_openrouter(self, prompt: str) -> str:
        """
        Calls OpenRouter API. Works exactly like OpenAI's API format.
        Any model on openrouter.ai works here — just change OPENROUTER_MODEL.
        """
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/simp-wealthsimple",  # optional but good practice
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are SIMP — Wealthsimple's institutional memory system. You write like a senior colleague who has seen things go wrong before. Direct, concise, no fluff. Max 180 words."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.4,  # lower = more consistent, less creative
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _rule_based_reason(self, results: list) -> str:
        """
        Fallback synthesis when no API key is set.
        Constructs a briefing from the data directly using if-then logic.
        """
        failed  = [r for r in results if r.get("outcome") in ["rejected", "failed", "abandoned"]]
        shipped = [r for r in results if r.get("outcome") in ["shipped", "adopted", "approved"]]
        stale   = [r for r in results if r.get("assumptions_stale")]

        all_people = {}
        for r in results:
            for p in r.get("people", []):
                all_people[p] = all_people.get(p, 0) + 1
        top_people = sorted(all_people, key=all_people.get, reverse=True)[:2]

        lines = []

        if failed:
            r = failed[0]
            lines.append(
                f"⚠️ <b>Stop. This was attempted before.</b> '{r['title']}' ({r['date']}) "
                f"ended as <b>{r['outcome']}</b>. {r.get('why_failed', 'Reason not fully documented.')} "
                f"Do not assume conditions have changed without verifying first."
            )
        elif shipped:
            r = shipped[0]
            lines.append(
                f"✅ <b>Related work shipped successfully.</b> '{r['title']}' ({r['date']}) "
                f"gives you a foundation. Review it before scoping new work — you may be able to extend rather than rebuild."
            )

        all_stale = [(a, r["title"]) for r in stale for a in r.get("assumptions_stale", [])]
        if all_stale:
            assumption, source = all_stale[0]
            lines.append(
                f"🔍 <b>Assumption to verify:</b> \"{assumption}\" — flagged as potentially outdated from '{source}'. "
                f"If this has shifted, your approach may need to change entirely."
            )

        if top_people:
            lines.append(
                f"👤 <b>Talk to these people first:</b> {', '.join(top_people)} — "
                f"they appear across multiple related decisions and carry context that isn't written down anywhere."
            )

        compliance_keywords = ["kyc", "fintrac", "pipeda", "osfi", "regulatory", "compliance", "legal", "privacy"]
        compliance_hits = [r for r in results if any(k in " ".join(r.get("tags", [])) for k in compliance_keywords)]
        if compliance_hits:
            lines.append(
                f"🚨 <b>Compliance touchpoint required.</b> {len(compliance_hits)} related decision(s) were blocked or altered by regulatory review. "
                f"Loop in compliance <i>before</i> prototyping, not after."
            )

        return "<br><br>".join(lines)

    def reason(self, query: str, results: list) -> str:
        """
        Main reasoning function.
        Uses OpenRouter LLM if API key is set, otherwise falls back to rule-based synthesis.
        """
        if not results:
            return "No relevant history found. This appears to be genuinely new territory — proceed, but document decisions as you go."

        # ── Try OpenRouter first ──────────────────────────────────────────────
        if OPENROUTER_API_KEY:
            context_blocks = []
            for r in results[:4]:
                block = (
                    f"Decision: {r['title']}\n"
                    f"Date: {r['date']} | Outcome: {r['outcome']}\n"
                    f"What happened: {r['what_happened']}\n"
                    f"Why failed: {r.get('why_failed') or 'N/A'}\n"
                    f"Stale assumptions: {', '.join(r.get('assumptions_stale', [])) or 'None flagged'}\n"
                    f"People with context: {', '.join(r.get('people', []))}"
                )
                context_blocks.append(block)

            prompt = (
                f"A Wealthsimple team member has proposed:\n\"{query}\"\n\n"
                f"Here is what the organization has already learned:\n\n"
                + "\n---\n".join(context_blocks)
                + "\n\nWrite a concise briefing (max 180 words) covering:\n"
                "1. The single most important thing they need to know before proceeding\n"
                "2. The assumption most likely to burn them if unchecked\n"
                "3. Who they should talk to first\n\n"
                "Be direct. No fluff. Write like a senior colleague who has seen this go wrong before. "
                "Use plain text — no markdown, no bullet points, just short paragraphs."
            )

            try:
                return self._call_openrouter(prompt)
            except Exception as e:
                # If API call fails for any reason, fall back gracefully
                return self._rule_based_reason(results) + f"<br><br><small style='color:#6b7280'>Note: LLM synthesis unavailable ({str(e)[:60]}). Showing rule-based analysis.</small>"

        # ── Fallback: rule-based ──────────────────────────────────────────────
        return self._rule_based_reason(results)