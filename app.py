import os
import json
from datetime import date, timedelta
import streamlit as st

st.set_page_config(page_title="CelebrateAI | Smart Event Planner", page_icon="🎉", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
:root { --ink:#20243a; --muted:#6c7187; --accent:#7657e8; --pink:#f47eae; }
.stApp { background: linear-gradient(135deg,#fbf9ff 0%,#fff7fb 52%,#f5f8ff 100%); color:var(--ink); }
.block-container { max-width: 1180px; padding-top: 2rem; }
.hero { padding: 1.5rem 1.8rem; border-radius: 24px; color: white;
background: linear-gradient(120deg,#5d49cf,#8a62e8 58%,#ed79ad); box-shadow: 0 14px 36px #6d54c526; }
.hero h1 { font-size: 2.55rem; margin:0; color:white; }
.hero p { font-size:1.05rem; opacity:.94; margin:.45rem 0 0; }
.pill { display:inline-block; border:1px solid #ffffff65; border-radius:999px; padding:.25rem .7rem; font-size:.78rem; margin-bottom:.6rem; }
.panel { background:#ffffffd9; border:1px solid #ece8f8; border-radius:18px; padding:1.1rem 1.25rem; }
div[data-testid="stMetric"] { background:white; border:1px solid #eee8fa; padding:14px; border-radius:14px; }
h2,h3 { color:#282343; }
.smallnote { color:#73758a; font-size:.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <span class="pill">✨ Generative AI Celebration Planner</span>
  <h1>CelebrateAI</h1>
  <p>Every celebration. One smart plan. Turn your event idea into a budget, timeline, vendor checklist, and memorable moments.</p>
</div>
""", unsafe_allow_html=True)

st.write("")
with st.sidebar:
    st.markdown("## 🎉 CelebrateAI")
    st.caption("Plan less. Celebrate more.")
    event_type = st.selectbox("What are you celebrating?", ["Birthday", "Wedding", "Anniversary", "Community event", "Baby shower", "Graduation", "Other"])
    event_name = st.text_input("Event name (optional)", placeholder="e.g. Aarav's 10th birthday")
    location = st.text_input("City / location", value="Gurugram")
    event_date = st.date_input("Event date", value=date.today()+timedelta(days=30), min_value=date.today())
    budget = st.number_input("Total budget (₹)", min_value=1000, max_value=100000000, value=50000, step=5000)
    guests = st.number_input("Expected guests", min_value=1, max_value=100000, value=100, step=10)
    style = st.selectbox("Preferred vibe", ["Elegant", "Fun & colorful", "Minimal", "Traditional", "Luxury", "Eco-friendly"])
    notes = st.text_area("Extra preferences", placeholder="Dietary needs, theme, accessibility, must-have activities…")
    generate = st.button("✨ Generate my event plan", type="primary", use_container_width=True)

def make_prompt():
    return f"""You are CelebrateAI, a practical and creative event-planning assistant.
Create a clear plan for a {event_type} event.
Event name: {event_name or 'Not specified'}
Location: {location}
Date: {event_date}
Budget: INR {budget:,}
Guest count: {guests}
Style: {style}
Preferences: {notes or 'None specified'}

Return concise, useful Markdown with these exact sections:
1. Event concept (theme and guest experience)
2. Budget breakdown (table; category, estimated INR, reason; sum must equal the budget)
3. Planning timeline (relative dates/days, with tasks and owners)
4. Vendor checklist (venue, food, decor, photography, sound, etc. as relevant; include questions to ask)
5. Personal touches and activity ideas
6. Day-of run sheet (time, activity)
7. Risks and practical tips

Keep costs clearly labelled as illustrative estimates, not live vendor quotes. Don't claim vendor availability, booking, or exact local market prices. Respect the user's preferences and event scale. Make the response actionable."""

def demo_plan():
    # Deterministic fallback keeps the app usable without an API key.
    food = round(budget * 0.38)
    venue = round(budget * 0.22)
    decor = round(budget * 0.13)
    photo = round(budget * 0.10)
    activities = round(budget * 0.07)
    buffer = budget - food - venue - decor - photo - activities
    return f"""## 1. Event concept
**{style} {event_type.lower()}** in {location} for {guests} guests. Build a welcoming experience around a simple focal point, coordinated colors, and one memorable group moment.

## 2. Budget breakdown
*Illustrative planning estimates only — not live vendor quotes.*

| Category | Estimate (INR) | Planning note |
|---|---:|---|
| Food & refreshments | ₹{food:,} | Plan menu and dietary options |
| Venue / seating | ₹{venue:,} | Compare packages and inclusions |
| Decoration | ₹{decor:,} | Focus on one photo-friendly area |
| Photography | ₹{photo:,} | Confirm hours and delivery |
| Activities / music | ₹{activities:,} | Match activities to guest mix |
| Contingency | ₹{buffer:,} | Keep for last-minute needs |
| **Total** | **₹{budget:,}** | |

## 3. Planning timeline
- **4 weeks before:** shortlist venues and vendors; confirm guest list.
- **3 weeks before:** finalize theme, menu, and invitations.
- **2 weeks before:** confirm vendors, schedule, and accessibility needs.
- **1 week before:** reconfirm headcount, payments, and supplies.
- **1 day before:** prepare signage, favors, and a contact sheet.
- **Event day:** use the run sheet below; keep one person as coordinator.

## 4. Vendor checklist
- **Venue:** capacity, setup/cleanup time, power, parking, weather backup.
- **Catering:** per-person inclusions, tasting, dietary/allergen handling, service staff.
- **Decor:** setup window, materials, breakdown, and what is included.
- **Photo/video:** coverage duration, deliverables, turnaround, permissions.
- **Sound/entertainment:** equipment, volume limits, power, backup plan.
- Get written quotes and cancellation terms; availability is not verified by this demo.

## 5. Personal touches & activities
- Welcome board with the event name.
- A photo corner using the chosen colors.
- A short guest message or memory activity.
- One inclusive activity suitable for different ages and abilities.
- Reusable or low-waste decorations where practical.

## 6. Day-of run sheet
| Time | Activity |
|---|---|
| 2 hours before | Venue setup and vendor arrival |
| 1 hour before | Sound check, decor check, guest welcome area |
| Event start | Welcome and refreshments |
| Mid-event | Main activity / meal |
| Final 30 minutes | Group photo, thank-you, favors |
| After event | Vendor checkout and cleanup |

## 7. Risks & practical tips
- Keep a weather/indoor backup for outdoor events.
- Confirm final guest count and dietary needs with vendors.
- Keep a contingency reserve and track advances.
- Share one coordinator's phone number with vendors.
- This demo uses a sample plan; verify prices, vendors, and local requirements before booking.
"""

if "plan" not in st.session_state:
    st.session_state.plan = None
if generate:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
                contents=make_prompt()
            )
            st.session_state.plan = response.text
            st.session_state.plan_mode = "Gemini AI"
        except Exception as exc:
            st.session_state.plan = demo_plan()
            st.session_state.plan_mode = "Demo mode (API call unavailable)"
            st.warning(f"Gemini request failed; showing a local sample plan instead. Details: {exc}")
    else:
        st.session_state.plan = demo_plan()
        st.session_state.plan_mode = "Demo mode (no API key configured)"

# Quick overview metrics
c1,c2,c3 = st.columns(3)
c1.metric("Event", event_type)
c2.metric("Guests", f"{guests:,}")
c3.metric("Budget", f"₹{budget:,.0f}")

st.write("")
if st.session_state.plan:
    st.markdown("""
    <style>
    .results-banner { padding: 1rem 1.25rem; border-radius: 16px; margin: .5rem 0 1rem;
      background: linear-gradient(110deg,#f0ebff,#fff0f7); border: 1px solid #e6dcff; }
    .results-banner h2 { margin: 0; color:#302452; font-size:1.45rem; }
    .results-banner p { margin:.25rem 0 0; color:#6b6680; font-size:.9rem; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-color:#e9e3f6 !important; border-radius:16px !important; }
    </style>
    <div class="results-banner"><h2>✨ Your celebration blueprint</h2>
    <p>A practical, personalized plan—ready to review, refine, and share.</p></div>
    """, unsafe_allow_html=True)
    st.caption(f"Generated with: {st.session_state.get('plan_mode','Demo mode')}  ·  Estimates are illustrative")

    # Present each major section in its own readable card while preserving Markdown tables/lists.
    import re
    sections = re.split(r"(?m)(?=^##\s+)", st.session_state.plan.strip())
    section_icons = ["🎨", "💰", "🗓️", "📋", "💫", "⏱️", "🛡️"]
    for idx, section in enumerate(sections):
        if not section.strip():
            continue
        heading_match = re.match(r"(?m)^##\s+(.+)$", section.strip())
        heading = heading_match.group(1).strip() if heading_match else "Event plan details"
        body = re.sub(r"(?m)^##\s+.+\n?", "", section.strip(), count=1)
        icon = section_icons[idx] if idx < len(section_icons) else "✨"
        with st.container(border=True):
            st.markdown(f"### {icon} {heading}")
            st.markdown(body)

    st.download_button("⬇️ Download your event plan", data=st.session_state.plan,
                       file_name="celebrateai_event_plan.md", mime="text/markdown",
                       use_container_width=True)
else:
    st.markdown("""
    <div class="panel">
    <h3>Ready to plan something memorable?</h3>
    <p>Choose your event details in the sidebar and press <b>Generate my event plan</b>.</p>
    <p class="smallnote">Works in demo mode without an API key. Add a Gemini API key to generate a customized AI plan.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    a,b,c = st.columns(3)
    a.markdown("### 💰 Smart budget\nSplit the budget into practical event categories.")
    b.markdown("### 🗓️ Timeline\nKnow what to prepare and when.")
    c.markdown("### 📋 Vendor checklist\nOrganize questions and confirmations.")

st.divider()
st.caption("CelebrateAI • PromptWars Virtual — Celebration & Event Planner • Planning estimates are illustrative; verify vendors and prices independently.")
