import streamlit as st
import json
from memory_engine import MemoryEngine

st.set_page_config(
    page_title="SIMP — Smart Institutional Memory Pipeline",
    page_icon="🧠",
    layout="wide"
)

# ── Styling ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  body { background: #0f1117; }
  .main { background: #0f1117; }
  .stTextArea textarea { font-size: 15px; }
  .block-container { padding-top: 2rem; }

  .simp-header {
    background: linear-gradient(135deg, #1a1f2e 0%, #0f1117 100%);
    border: 1px solid #2a3142;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
  }
  .simp-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin: 0;
  }
  .simp-subtitle {
    color: #6b7280;
    font-size: 0.95rem;
    margin-top: 0.4rem;
  }
  .ws-badge {
    background: #00d4aa22;
    color: #00d4aa;
    border: 1px solid #00d4aa44;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 0.8rem;
  }

  .result-card {
    background: #1a1f2e;
    border: 1px solid #2a3142;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
  }
  .result-card.warning {
    border-left: 4px solid #f59e0b;
  }
  .result-card.danger {
    border-left: 4px solid #ef4444;
  }
  .result-card.info {
    border-left: 4px solid #3b82f6;
  }
  .result-card.success {
    border-left: 4px solid #00d4aa;
  }

  .moment-badge {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 3px 10px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 0.6rem;
  }
  .badge-tried    { background: #ef444422; color: #ef4444; }
  .badge-stale    { background: #f59e0b22; color: #f59e0b; }
  .badge-people   { background: #3b82f622; color: #3b82f6; }
  .badge-context  { background: #00d4aa22; color: #00d4aa; }

  .decision-title { font-size: 1.05rem; font-weight: 700; color: #f1f5f9; margin: 0.3rem 0; }
  .decision-meta  { font-size: 0.8rem; color: #6b7280; margin-bottom: 0.6rem; }
  .decision-body  { font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; }

  .assumption-chip {
    display: inline-block;
    background: #f59e0b11;
    border: 1px solid #f59e0b33;
    color: #fbbf24;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.78rem;
    margin: 2px 3px 2px 0;
  }
  .people-chip {
    display: inline-block;
    background: #3b82f611;
    border: 1px solid #3b82f633;
    color: #93c5fd;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.78rem;
    margin: 2px 3px 2px 0;
  }

  .ai-summary {
    background: #0f1117;
    border: 1px solid #2a3142;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    font-size: 0.92rem;
    color: #cbd5e1;
    line-height: 1.7;
  }
  .ai-summary-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #00d4aa;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
  }

  .stat-box {
    background: #1a1f2e;
    border: 1px solid #2a3142;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
  }
  .stat-number { font-size: 1.8rem; font-weight: 800; color: #00d4aa; }
  .stat-label  { font-size: 0.78rem; color: #6b7280; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="simp-header">
  <div class="ws-badge">WEALTHSIMPLE INTERNAL</div>
  <p class="simp-title">🧠 SIMP</p>
  <p class="simp-subtitle">Smart Institutional Memory Pipeline — Before you build, know what was already tried.</p>
</div>
""", unsafe_allow_html=True)

# ── Init engine ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    engine = MemoryEngine()
    engine.load_synthetic_data()
    return engine

engine = get_engine()

# ── Stats row ─────────────────────────────────────────────────────────────────
total = engine.count()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{total}</div><div class="stat-label">Decisions in memory</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="stat-box"><div class="stat-number">3</div><div class="stat-label">Domains indexed</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-box"><div class="stat-number">18</div><div class="stat-label">Contributors tracked</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="stat-box"><div class="stat-number">24mo</div><div class="stat-label">History depth</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Query interface ───────────────────────────────────────────────────────────
st.markdown("### What are you about to work on?")
st.markdown("<p style='color:#6b7280;font-size:0.88rem;margin-top:-0.5rem'>Describe a problem, proposal, or initiative. SIMP will surface what the org already knows.</p>", unsafe_allow_html=True)

example_queries = [
    "We want to redesign the onboarding flow to reduce drop-off",
    "We're considering rebuilding our fraud detection system with ML",
    "We should migrate our mobile app from React Native to Flutter",
    "Let's build a real-time spending insights feature for clients",
]

# session_state persists values across Streamlit reruns triggered by button clicks
if "query_text" not in st.session_state:
    st.session_state.query_text = ""

col_q, col_ex = st.columns([3, 1])
with col_ex:
    st.markdown("<p style='color:#6b7280;font-size:0.8rem;margin-bottom:0.4rem'>Try an example:</p>", unsafe_allow_html=True)
    for ex in example_queries:
        if st.button(ex[:45] + "…", key=ex, use_container_width=True):
            st.session_state.query_text = ex
            st.rerun()

with col_q:
    query = st.text_area(
        "",
        value=st.session_state.query_text,
        placeholder="e.g. We're thinking of rebuilding the onboarding flow to reduce friction...",
        height=100,
        label_visibility="collapsed"
    )

use_ai = st.toggle("Enable synthesis layer", value=True)

search_btn = st.button("🔍  Search Institutional Memory", type="primary", use_container_width=False)

# ── Results ───────────────────────────────────────────────────────────────────
if search_btn and query.strip():
    with st.spinner("Searching memory..."):
        results = engine.search(query, n_results=5)
        ai_summary = engine.reason(query, results) if use_ai else None

    if not results:
        st.info("No relevant decisions found in memory for this query.")
    else:
        st.markdown("---")
        st.markdown("### What the org already knows")

        # ── MOMENT 1: Already tried this ──────────────────────────────────────
        tried = [r for r in results if r.get("outcome") in ["rejected", "failed", "abandoned"]]
        if tried:
            st.markdown("#### 🚨 We already tried this")
            for r in tried[:2]:
                assumptions_html = "".join(f'<span class="assumption-chip">{a}</span>' for a in r.get("assumptions", []))
                people_html = "".join(f'<span class="people-chip">👤 {p}</span>' for p in r.get("people", []))
                st.markdown(f"""
                <div class="result-card danger">
                  <span class="moment-badge badge-tried">⛔ Previously attempted</span>
                  <div class="decision-title">{r['title']}</div>
                  <div class="decision-meta">📅 {r['date']} &nbsp;·&nbsp; 🏷 {r['domain']} &nbsp;·&nbsp; Outcome: <b style="color:#ef4444">{r['outcome'].upper()}</b></div>
                  <div class="decision-body">{r['what_happened']}</div>
                  <br>
                  <div><b style="color:#94a3b8;font-size:0.8rem">Why it failed:</b><br>
                  <span class="decision-body">{r.get('why_failed','Not recorded.')}</span></div>
                  <br>
                  <div>{assumptions_html}</div>
                  <div style="margin-top:0.5rem">{people_html}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── MOMENT 2: Stale assumptions ───────────────────────────────────────
        stale = [r for r in results if r.get("assumptions_stale")]
        if stale:
            st.markdown("#### ⚠️ Assumptions that may no longer be true")
            for r in stale[:2]:
                stale_html = "".join(f'<span class="assumption-chip">⚠ {a}</span>' for a in r.get("assumptions_stale", []))
                st.markdown(f"""
                <div class="result-card warning">
                  <span class="moment-badge badge-stale">⚠️ Stale assumption detected</span>
                  <div class="decision-title">{r['title']}</div>
                  <div class="decision-meta">📅 {r['date']} &nbsp;·&nbsp; 🏷 {r['domain']}</div>
                  <div class="decision-body">{r['what_happened']}</div>
                  <br>
                  <div><b style="color:#f59e0b;font-size:0.8rem">These assumptions were true then — verify now:</b><br>
                  <div style="margin-top:0.4rem">{stale_html}</div></div>
                </div>
                """, unsafe_allow_html=True)

        # ── MOMENT 3: People with context ─────────────────────────────────────
        all_people = {}
        for r in results:
            for p in r.get("people", []):
                all_people[p] = all_people.get(p, [])
                all_people[p].append(r["title"])

        if all_people:
            st.markdown("#### 👥 People who have context on this")
            people_cols = st.columns(min(len(all_people), 3))
            for i, (person, decisions) in enumerate(list(all_people.items())[:3]):
                with people_cols[i]:
                    decisions_list = "".join(f"<li style='color:#94a3b8;font-size:0.8rem'>{d}</li>" for d in decisions[:2])
                    st.markdown(f"""
                    <div class="result-card info">
                      <span class="moment-badge badge-people">👤 Context holder</span>
                      <div class="decision-title">{person}</div>
                      <div style="margin-top:0.5rem"><b style="color:#94a3b8;font-size:0.78rem">Involved in:</b>
                      <ul style="margin:0.3rem 0 0 1rem;padding:0">{decisions_list}</ul></div>
                    </div>
                    """, unsafe_allow_html=True)

        # ── Successful decisions also surfaced ────────────────────────────────
        successful = [r for r in results if r.get("outcome") in ["shipped", "adopted", "approved"]]
        if successful:
            st.markdown("#### ✅ Related decisions that shipped")
            for r in successful[:2]:
                people_html = "".join(f'<span class="people-chip">👤 {p}</span>' for p in r.get("people", []))
                st.markdown(f"""
                <div class="result-card success">
                  <span class="moment-badge badge-context">✅ Shipped</span>
                  <div class="decision-title">{r['title']}</div>
                  <div class="decision-meta">📅 {r['date']} &nbsp;·&nbsp; 🏷 {r['domain']}</div>
                  <div class="decision-body">{r['what_happened']}</div>
                  <div style="margin-top:0.6rem">{people_html}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── AI Reasoning layer ────────────────────────────────────────────────
        if ai_summary:
            st.markdown("---")
            st.markdown(f"""
            <div class="ai-summary">
              <div class="ai-summary-label">🤖 Claude's synthesis</div>
              {ai_summary.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

elif search_btn:
    st.warning("Please enter a query first.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style='color:#374151;font-size:0.78rem;text-align:center'>
SIMP — The one decision that must remain human: <b style='color:#4b5563'>what to act on</b>. 
AI surfaces context. Humans decide direction.
</p>
""", unsafe_allow_html=True)