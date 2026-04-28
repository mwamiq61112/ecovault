import streamlit as st
import random
import string
from datetime import datetime

# Credits earned per kg for each waste type at drop-off centers
DROPOFF_RATES = {
    "📦 Paper / Cardboard": {
        "credits_per_kg": 6,
        "bonus": 5,
        "co2_per_kg": 0.9,
        "icon": "📦",
        "tip": "Flatten all cardboard boxes. Remove plastic liners and tape.",
        "accepted_at": ["ITC Paperkraft Collection Point", "MCD Dry Waste Collection Centre"],
    },
    "🧴 Plastic": {
        "credits_per_kg": 9,
        "bonus": 8,
        "co2_per_kg": 1.5,
        "icon": "🧴",
        "tip": "Rinse bottles, crush them flat, and sort by resin code if possible.",
        "accepted_at": ["Kabadiwala.com Collection Hub", "ITC WOW (Well Being Out of Waste)", "MCD Dry Waste Collection Centre"],
    },
    "💻 E-Waste": {
        "credits_per_kg": 30,
        "bonus": 20,
        "co2_per_kg": 3.2,
        "icon": "💻",
        "tip": "Wipe personal data from devices before dropping off. Keep batteries separate.",
        "accepted_at": ["Attero Recycling Pvt Ltd", "Cerebra Integrated Technologies", "E-Parisaraa E-Waste Center"],
    },
    "🫙 Glass": {
        "credits_per_kg": 7,
        "bonus": 5,
        "co2_per_kg": 0.3,
        "icon": "🫙",
        "tip": "Rinse all jars and bottles. Remove metal lids and caps before dropping off.",
        "accepted_at": ["HiGlass Recyclers"],
    },
    "🔩 Metal / Aluminium": {
        "credits_per_kg": 20,
        "bonus": 15,
        "co2_per_kg": 9.0,
        "icon": "🔩",
        "tip": "Separate aluminium cans from steel. Clean containers are worth more.",
        "accepted_at": ["Sadar Bazar Scrap Market", "Mayapuri Scrap Market", "Delhi Ferrous & Non-Ferrous Hub"],
    },
}

def generate_ref():
    return "EV-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

def show(email, update_user_fn):
    st.markdown("""
    <div class="nav-header">
        <h1>📦 Drop & Earn</h1>
        <p>Physically drop waste at a center → log it here → earn Green Credits instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    # How it works banner
    st.markdown("""
    <div class="gs-card" style="margin-bottom:0.5rem;">
        <div class="sec-title">🗺️ How Drop & Earn Works</div>
        <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-top:1rem;">
            <div class="dropoff-step" style="flex-direction:column; align-items:center; text-align:center; background:transparent; border:none;">
                <div class="step-num">1</div>
                <div style="font-size:1.8rem; margin:0.5rem 0;">🗺️</div>
                <div style="font-weight:600; color:#1a3d2b; font-size:0.88rem;">Find a Center</div>
                <div style="color:#52b788; font-size:0.78rem; margin-top:0.2rem;">Use Eco-Navigator to find a center near you</div>
            </div>
            <div class="dropoff-step" style="flex-direction:column; align-items:center; text-align:center; background:transparent; border:none;">
                <div class="step-num">2</div>
                <div style="font-size:1.8rem; margin:0.5rem 0;">🚗</div>
                <div style="font-weight:600; color:#1a3d2b; font-size:0.88rem;">Drop It Off</div>
                <div style="color:#52b788; font-size:0.78rem; margin-top:0.2rem;">Take your waste to the center in person</div>
            </div>
            <div class="dropoff-step" style="flex-direction:column; align-items:center; text-align:center; background:transparent; border:none;">
                <div class="step-num">3</div>
                <div style="font-size:1.8rem; margin:0.5rem 0;">📋</div>
                <div style="font-weight:600; color:#1a3d2b; font-size:0.88rem;">Log it Here</div>
                <div style="color:#52b788; font-size:0.78rem; margin-top:0.2rem;">Fill in the form below with your drop-off details</div>
            </div>
            <div class="dropoff-step" style="flex-direction:column; align-items:center; text-align:center; background:transparent; border:none;">
                <div class="step-num">4</div>
                <div style="font-size:1.8rem; margin:0.5rem 0;">🪙</div>
                <div style="font-weight:600; color:#1a3d2b; font-size:0.88rem;">Earn Credits</div>
                <div style="color:#52b788; font-size:0.78rem; margin-top:0.2rem;">Green Credits land in your wallet immediately</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown('<div class="sec-title">Log Your Drop-Off</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Fill in the details of the waste you dropped off</div>', unsafe_allow_html=True)

        waste_type = st.selectbox("🗂️ Waste Type Dropped", list(DROPOFF_RATES.keys()))
        info = DROPOFF_RATES[waste_type]

        weight = st.number_input("⚖️ Weight Dropped (kg)", min_value=0.1, max_value=500.0, value=1.0, step=0.5)

        center_options = info["accepted_at"] + ["Other / Not Listed"]
        center = st.selectbox("🏢 Drop-Off Center Name", center_options)
        if center == "Other / Not Listed":
            center = st.text_input("Enter center name manually")

        drop_date = st.date_input("📅 Drop-Off Date", value=datetime.today())

        st.markdown(f"""
        <div class="gs-info" style="margin-top:0.5rem;">
            💡 <strong>Tip:</strong> {info['tip']}
        </div>
        """, unsafe_allow_html=True)

        photo = st.file_uploader("📸 Proof Photo (optional but recommended)", type=["jpg","jpeg","png"])
        if photo:
            st.image(photo, caption="Drop-off proof uploaded ✅", use_container_width=True)

        # Preview calculation
        base_credits = int(weight * info["credits_per_kg"])
        bonus = info["bonus"] if weight >= 2.0 else 0
        total_credits = base_credits + bonus
        co2_saved = round(weight * info["co2_per_kg"], 2)

        st.markdown(f"""
        <div class="impact-box" style="margin-top:1rem;">
            <h3>🧮 Credits Preview</h3>
            <p>Base: <strong>{base_credits} GC</strong> ({info['credits_per_kg']} GC/kg × {weight:.1f}kg)</p>
            {"<p>Bonus: <strong>+" + str(bonus) + " GC</strong> 🎉 (2kg+ drop-off bonus!)</p>" if bonus > 0 else "<p style='color:#888; font-size:0.85rem;'>Drop 2kg+ for a bonus!</p>"}
            <p>CO₂ Saved: <strong>{co2_saved} kg</strong></p>
            <p style='font-size:1.05rem;'>Total: <strong style='color:#1a3d2b;'>+{total_credits} Green Credits</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Confirm Drop-Off & Earn Credits", use_container_width=True):
            if not center or center.strip() == "":
                st.warning("Please enter or select a center name.")
            else:
                ref = generate_ref()
                history_item = {
                    "action": f"{info['icon']} Drop-off: {waste_type.split()[1]} at {center[:25]}",
                    "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "credits": total_credits
                }
                update_user_fn(
                    email,
                    credits_add=total_credits,
                    waste_add=weight,
                    co2_add=co2_saved,
                    history_item=history_item
                )
                st.session_state["last_dropoff_ref"] = ref
                st.session_state["last_dropoff_credits"] = total_credits
                st.session_state["last_dropoff_type"] = waste_type
                st.session_state["last_dropoff_done"] = True
                st.balloons()
                st.rerun()

    with col2:
        st.markdown('<div class="sec-title">Credit Rates</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-sub">Earn more by dropping heavier loads</div>', unsafe_allow_html=True)

        for wtype, winfo in DROPOFF_RATES.items():
            icon = winfo["icon"]
            rate = winfo["credits_per_kg"]
            bonus = winfo["bonus"]
            label = wtype.split(" ", 1)[1]
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:1rem; background:rgba(255,255,255,0.85); border:1px solid rgba(82,183,136,0.2); border-radius:1rem; padding:0.8rem 1.2rem; margin-bottom:0.5rem;">
                <span style="font-size:1.5rem;">{icon}</span>
                <div style="flex:1;">
                    <div style="font-weight:600; color:#1a3d2b; font-size:0.9rem;">{label}</div>
                    <div style="color:#52b788; font-size:0.78rem;">{rate} GC per kg · +{bonus} GC bonus at 2kg+</div>
                </div>
                <div style="font-family:'Syne',sans-serif; font-weight:800; color:#2d6a4f; font-size:1rem;">{rate} GC/kg</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.get("last_dropoff_done"):
            ref = st.session_state.get("last_dropoff_ref", "")
            earned = st.session_state.get("last_dropoff_credits", 0)
            dtype = st.session_state.get("last_dropoff_type", "")
            st.markdown(f"""
            <div class="gs-success" style="margin-top:1.5rem;">
                <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:#1a5c33;">🎉 Drop-Off Logged!</div>
                <div style="margin-top:0.5rem; font-size:0.88rem; color:#2d6a4f;">
                    <strong>+{earned} Green Credits</strong> added to your wallet.<br>
                    Reference: <code style="background:#d8eedf; padding:0.1rem 0.4rem; border-radius:4px;">{ref}</code><br>
                    Type: {dtype}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Log Another Drop-Off", use_container_width=True):
                st.session_state["last_dropoff_done"] = False
                st.rerun()
        else:
            st.markdown("""
            <div class="gs-card" style="text-align:center; margin-top:1.5rem; padding:2rem;">
                <div style="font-size:3rem;">♻️</div>
                <div style="font-family:'Syne',sans-serif; font-weight:700; color:#1a3d2b; margin:0.8rem 0 0.4rem;">Every kg counts!</div>
                <div style="color:#52b788; font-size:0.88rem; line-height:1.6;">E-Waste earns the most credits.<br>Bring 2kg+ for a bonus reward.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗺️ Find a Drop-Off Center", use_container_width=True):
            st.session_state["page"] = "🗺️  Eco-Navigator"
            st.rerun()
