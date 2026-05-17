"""
Engagement to Ad Revenue Simulator
JioStar | Monetization Intelligence
Three-model elasticity: Total, Midroll, Preroll inventory

Pages:
  1. Simulator         — Cohort selection, lever inputs, projected inventory + revenue split
  2. Cohort Explorer   — Browse all parent cohorts, filter, sort
  3. Model Architecture — Full technical methodology
"""

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Engagement to Ad Revenue | JioStar",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
  html, body, [class*="css"] { font-family: 'Segoe UI', system-ui, sans-serif; }
  #MainMenu, footer { visibility: hidden; }

  div[data-testid="metric-container"] {
    background: #F8F9FA; border: 1px solid #E9ECEF; border-radius: 10px; padding: 16px 18px;
  }
  div[data-testid="metric-container"] label {
    font-size: 10px !important; font-weight: 700 !important; color: #6C757D !important;
    text-transform: uppercase; letter-spacing: 0.6px;
  }
  div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 20px !important; font-weight: 700 !important; color: #111827 !important;
  }

  .sec-hdr {
    font-size: 10px; font-weight: 700; color: #6C757D; text-transform: uppercase;
    letter-spacing: 1px; padding-bottom: 6px; border-bottom: 2px solid #E9ECEF;
    margin: 20px 0 12px 0;
  }
  .badge-high   { background:#ECFDF5; border:1.5px solid #6EE7B7; border-left:5px solid #059669; border-radius:8px; padding:14px 18px; margin:16px 0; }
  .badge-medium { background:#FFFBEB; border:1.5px solid #FCD34D; border-left:5px solid #D97706; border-radius:8px; padding:14px 18px; margin:16px 0; }
  .badge-low    { background:#FEF2F2; border:1.5px solid #FCA5A5; border-left:5px solid #DC2626; border-radius:8px; padding:14px 18px; margin:16px 0; }
  .badge-title  { font-size:14px; font-weight:700; margin-bottom:4px; }
  .badge-desc   { font-size:12.5px; color:#374151; margin-bottom:6px; line-height:1.5; }
  .badge-stats  { font-size:11.5px; color:#6B7280; }

  .insight-box  { background:#FFF7ED; border-left:5px solid #EA580C; border-radius:0 8px 8px 0; padding:12px 16px; margin:8px 0; font-size:13px; line-height:1.6; }
  .insight-info { background:#EFF6FF; border-left:5px solid #3B82F6; border-radius:0 8px 8px 0; padding:12px 16px; margin:8px 0; font-size:13px; line-height:1.6; }
  .insight-warn { background:#FEF2F2; border-left:5px solid #DC2626; border-radius:0 8px 8px 0; padding:12px 16px; margin:8px 0; font-size:13px; line-height:1.6; }
  .insight-title { font-weight:700; margin-bottom:3px; }

  .inv-card { background:white; border:1px solid #E5E7EB; border-radius:10px; padding:16px 20px; margin:4px 0; }
  .inv-card-title { font-size:11px; font-weight:700; color:#6B7280; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px; }
  .inv-val { font-size:24px; font-weight:700; color:#111827; }
  .inv-delta-pos { font-size:13px; color:#059669; font-weight:600; }
  .inv-delta-neg { font-size:13px; color:#DC2626; font-weight:600; }

  .sb-lbl { font-size:10px; font-weight:700; color:#9CA3AF; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ██████████████████ PASTE YOUR JSON DATA BELOW ███████████████████████████████
# ─────────────────────────────────────────────────────────────────────────────
# Instructions:
#   Run Cell 4H in your Databricks notebook.
#   Copy each PASTE BLOCK output and replace the dict below.
#   All 6 blocks must be replaced before deploying.
# ─────────────────────────────────────────────────────────────────────────────

# ── PASTE BLOCK 1: METADATA ──────────────────────────────────────────────────
# Replace the dict below with output from Cell 4H "PASTE BLOCK 1: METADATA"
METADATA = {
    "total_platform_inventory":  768495767.0,
    "midroll_platform_inventory": 0.0,
    "preroll_platform_inventory": 0.0,
    "midroll_share_of_total":    0.0,
    "preroll_share_of_total":    0.0,
    "coverage_total":            98.29,
    "coverage_midroll":          0.0,
    "coverage_preroll":          0.0,
    "high_pct_total":            78.0,
    "high_pct_midroll":          0.0,
    "high_pct_preroll":          0.0,
    "total_parents":             117,
    "total_cohorts_7dim":        3222,
}

# ── PASTE BLOCK 2: DIMENSION VALUES ──────────────────────────────────────────
# Replace the dict below with output from Cell 4H "PASTE BLOCK 2: DIMENSION VALUES"
DIMENSION_VALUES = {
    "lagged_engagement_quadrant": ["Ent Only", "Sports & Ent", "Fringe", "Sports Only"],
    "platform_group":             ["Mobile", "CTV", "Web"],
    "gender_clean":               ["Male", "Female", "Unknown", "Other"],
    "subs_status":                ["Active (SVOD)", "Non Subscriber (AVOD)", "Newly Acquired", "Churned"],
    "seasonality":                ["Ent", "Mixed"],
    "age_group":                  ["Teen (13-17)", "GenZ (18-24)", "Young Adult (25-34)", "Mid Adult (35-44)", "45+", "Unknown"],
    "dominant_proposition":       ["network fiction gec", "network non fiction gec", "indian movies", "specials", "international", "kids", "others", "creator content", "Unknown"],
}

# ── PASTE BLOCK 3: ELASTICITY — TOTAL ────────────────────────────────────────
# Paste output from Cell 4H "PASTE BLOCK 3" here.
# Key format: "Quadrant | Platform | Gender | Subs | Seasonality"
# IMPORTANT: Cell 4H outputs JSON with lowercase true/false — Python needs True/False.
# The notebook prints Python dicts (not JSON), so this should be fine as-is.
ELASTICITY_TOTAL = {
    # ← PASTE YOUR ELASTICITY_TOTAL FROM CELL 4H HERE
}

# ── PASTE BLOCK 4: ELASTICITY — MIDROLL ──────────────────────────────────────
# Replace the dict below with output from Cell 4H "PASTE BLOCK 4: ELASTICITY — MIDROLL"
ELASTICITY_MIDROLL = {
    # ← PASTE FULL MIDROLL ELASTICITY JSON FROM CELL 4H HERE
    # Same key format: "Quadrant | Platform | Gender | Subs | Seasonality"
}

# ── PASTE BLOCK 5: ELASTICITY — PREROLL ──────────────────────────────────────
# Replace the dict below with output from Cell 4H "PASTE BLOCK 5: ELASTICITY — PREROLL"
ELASTICITY_PREROLL = {
    # ← PASTE FULL PREROLL ELASTICITY JSON FROM CELL 4H HERE
    # Same key format: "Quadrant | Platform | Gender | Subs | Seasonality"
}

# ── PASTE BLOCK 6: BASELINE LOOKUP ───────────────────────────────────────────
# Replace the dict below with output from Cell 4H "PASTE BLOCK 6: BASELINE LOOKUP"
# Format: { "dim1 | dim2 | ... | dim7" : {metrics...} }
BASELINE_LOOKUP = {
    # ← PASTE FULL BASELINE LOOKUP JSON FROM CELL 4H HERE
    # 7-dim key: "Quadrant | Platform | Gender | Subs | Seasonality | AgeGroup | DomProp"
}

# ─────────────────────────────────────────────────────────────────────────────
# ██████████████████ END OF JSON PASTE ZONE ███████████████████████████████████
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# BUILD COHORT EXPLORER TABLE (pre-computed at startup, not in loops)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def build_explorer_df():
    rows = []
    for key, e in ELASTICITY_TOTAL.items():
        parts = key.split(" | ")
        if len(parts) != 5:
            continue
        rows.append({
            "Engagement Quadrant":   parts[0],
            "Platform":              parts[1],
            "Gender":                parts[2],
            "Subscription Status":   parts[3],
            "Seasonality":           parts[4],
            "Confidence Tier":       e.get("effective_tier", ""),
            "Sub-segments":          e.get("n_segments", 0),
            "HID-months":            e.get("total_hid", 0),
            "WT/VV Elasticity (β₁)": round(e.get("elasticity_wt_per_vv", 0), 4),
            "AD Elasticity (β₂)":   round(e.get("elasticity_active_days", 0), 4),
            "R² In-sample":          round(e.get("r2_in_sample", 0), 3),
            "R² LOOCV":              round(e.get("r2_loocv", 0) if e.get("r2_loocv") is not None else 0, 3),
        })
    df = pd.DataFrame(rows)
    if "HID-months" in df.columns:
        total_hid_sum = df["HID-months"].sum()
        df["HID Share (%)"] = (df["HID-months"] / total_hid_sum * 100).round(2) if total_hid_sum > 0 else 0
    return df


# ─────────────────────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────────────────────
PARENT_DIMS_5 = ["lagged_engagement_quadrant", "platform_group", "gender_clean", "subs_status", "seasonality"]
ALL_DIMS_7    = PARENT_DIMS_5 + ["age_group", "dominant_proposition"]

DIM_LABELS = {
    "lagged_engagement_quadrant": "Engagement Quadrant",
    "platform_group":             "Platform",
    "gender_clean":               "Gender",
    "subs_status":                "Subscription Status",
    "seasonality":                "Seasonality",
    "age_group":                  "Age Group",
    "dominant_proposition":       "Dominant Content",
}

TIER_COLORS   = {"High": "#059669", "Medium": "#D97706", "Low": "#DC2626"}
BADGE_CLASSES = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}
TIER_DESCS    = {
    "High":   "Strong out-of-sample fit (LOOCV-validated). Reliable for product and revenue decisions.",
    "Medium": "Directionally reliable. Magnitude estimates carry ±20–30% uncertainty.",
    "Low":    "Overfit detected. Use directionally only — not for revenue commitments.",
}

DEFAULT_ECPM_MID = {"Mobile": 80.0, "CTV": 150.0, "Web": 100.0}
DEFAULT_ECPM_PRE = {"Mobile": 50.0, "CTV": 100.0, "Web": 60.0}


def fmt_inv(v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "N/A"
    if abs(v) >= 1_000_000: return f"{v/1_000_000:.2f} Mn"
    if abs(v) >= 1_000:     return f"{v/1_000:.1f} K"
    return f"{int(v):,}"

def fmt_rev(v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return "N/A"
    if abs(v) >= 10_000_000: return f"Rs. {v/10_000_000:.2f} Cr"
    if abs(v) >= 100_000:    return f"Rs. {v/100_000:.2f} L"
    if abs(v) >= 1_000:      return f"Rs. {v/1_000:.1f} K"
    return f"Rs. {int(v):,}"

def fmt_delta(v):
    if v is None: return ""
    sign = "+" if v >= 0 else ""
    if abs(v) >= 1_000_000: return f"{sign}{v/1_000_000:.2f} Mn"
    if abs(v) >= 1_000:     return f"{sign}{v/1_000:.1f} K"
    return f"{sign}{int(v):,}"

def apply_el(base, pct, coef):
    if pct == 0 or coef == 0: return base
    return base * ((1 + pct / 100) ** coef)

def make_parent_key(sel):
    return " | ".join(str(sel[d]) for d in PARENT_DIMS_5)

def make_7dim_key(sel):
    return " | ".join(str(sel[d]) for d in ALL_DIMS_7)

def get_elasticity(sel, model_dict):
    key = make_parent_key(sel)
    return model_dict.get(key)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — shared across all pages
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.markdown("## Simulation Inputs")
st.sidebar.caption("7-dim cohort → 5-dim parent elasticity model.")
st.sidebar.markdown("---")

sel = {}
for d in ALL_DIMS_7:
    opts = DIMENSION_VALUES.get(d, [])
    sel[d] = st.sidebar.selectbox(DIM_LABELS[d], opts, key=f"s_{d}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Engagement Levers**")

# WT/VV — synced slider + number
st.sidebar.markdown('<div class="sb-lbl">Watch Time per VV (WT/VV) change (%)</div>', unsafe_allow_html=True)
wt_c1, wt_c2 = st.sidebar.columns([3, 1])
with wt_c1:
    wt_slide = st.slider("wt_sl", -10.0, 100.0, 0.0, 1.0, label_visibility="collapsed", key="wt_sl")
with wt_c2:
    wt_box = st.number_input("wt_nb", -10.0, 100.0, float(wt_slide), 1.0, label_visibility="collapsed", key="wt_nb")
wt_uplift = wt_box

# Active Days — absolute, synced
st.sidebar.markdown('<div class="sb-lbl" style="margin-top:8px;">Active Days change (± days)</div>', unsafe_allow_html=True)
ad_c1, ad_c2 = st.sidebar.columns([3, 1])
with ad_c1:
    ad_slide = st.slider("ad_sl", -10.0, 31.0, 0.0, 0.5, label_visibility="collapsed", key="ad_sl")
with ad_c2:
    ad_box = st.number_input("ad_nb", -10.0, 31.0, float(ad_slide), 0.5, label_visibility="collapsed", key="ad_nb")
ad_abs = ad_box
ad_pct = float(ad_abs)  # treat as direct % change — same axis as WT/VV
if ad_abs != 0:
    st.sidebar.caption(f"Active Days: {ad_abs:+.1f} days treated as {ad_pct:+.1f}% lever input")

st.sidebar.markdown("---")
st.sidebar.markdown("**Revenue Assumptions**")

# Separate eCPM for midroll and preroll
plat = sel.get("platform_group", "Mobile")
ecpm_mid = st.sidebar.number_input(
    "Midroll eCPM (Rs. per 1,000)", 10.0, 500.0,
    float(DEFAULT_ECPM_MID.get(plat, 80.0)), 5.0, key="ecpm_mid"
)
ecpm_pre = st.sidebar.number_input(
    "Preroll eCPM (Rs. per 1,000)", 10.0, 500.0,
    float(DEFAULT_ECPM_PRE.get(plat, 50.0)), 5.0, key="ecpm_pre"
)
str_pct = st.sidebar.slider("Sell-Through Rate (%)", 30.0, 100.0, 70.0, 1.0)

run_sim = st.sidebar.button("Run Simulation", type="primary", use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGES — tabs always render; st.stop() only inside tab1
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Simulator", "Cohort Explorer", "Model Architecture"])


# ════════════════════════════════════════════════════════════════════════
# PAGE 1 — SIMULATOR
# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## Engagement to Ad Revenue Simulator")
    st.caption(
        "Given a change in WT/VV or Active Days, projects the impact on Total, Midroll, and Preroll "
        "ad inventory — with separate revenue estimates per format. "
        "Built on three log-log elasticity models validated across 117 cohort-level regressions."
    )

    # Top KPI strip
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Inventory Modelled", f"{METADATA.get('coverage_total', 0):.1f}%")
    k2.metric("Midroll Coverage", f"{METADATA.get('coverage_midroll', 0):.1f}%")
    k3.metric("Preroll Coverage", f"{METADATA.get('coverage_preroll', 0):.1f}%")
    k4.metric("Parent Cohorts", f"{METADATA.get('total_parents', 0)}")
    k5.metric("Midroll Share of Total", f"{METADATA.get('midroll_share_of_total', 0):.1f}%")

    with st.expander("How this simulator works — three-model architecture"):
        st.markdown("""
**What it answers**

Given a % change in WT/VV or Active Days for a selected cohort:
- How much does **total ad inventory** change?
- What is the split between **midroll** and **preroll** inventory change?
- What is the **incremental revenue** per format at your eCPM and sell-through rate?

---

**Three separate elasticity models**

| Model | Y Variable | Predictors | Use |
|-------|-----------|-----------|-----|
| Total | `total_inventory / HID` | WT/VV, Active Days | Overall inventory planning |
| Midroll | `midroll_inv / HID` | WT/VV, Active Days | Watch-depth driven; primary revenue format |
| Preroll | `preroll_inv / HID` | WT/VV, Active Days | Session-entry driven; smaller share |

**Why VV/AU is excluded from all three models:**
VV/AU (viewer rate per active user) was tested in all three, including as a primary candidate for preroll.
In every case, values compressed into the 0.95–1.0 range at cohort level — producing coefficients
with standard deviation >20 and 48% negative signs. This is not a signal; it is pure noise amplification
from near-zero variance. All three final models use two predictors only.

---

**Prediction formula (applied per model)**

```
Projected Inventory/User = Base Inventory/User
                           × (1 + WT/VV % change)^β_WT
                           × (1 + Active Days % change)^β_AD

Revenue = Projected Inventory × (eCPM / 1,000) × Sell-Through Rate
```

---

**Dimension structure**

| Layer | Dimensions | Purpose |
|-------|-----------|---------|
| 5-dim (modelling) | Quadrant × Platform × Gender × Subs × Seasonality | Regression fitted here |
| 7-dim (selection) | All 5 + Age Group + Dominant Content | Exact baseline lookup |

---

**Confidence tiers**

| Tier | Criteria | Reliability |
|------|----------|-------------|
| **High** | ≥25 sub-segments, no overfit | Defensible for product and revenue decisions |
| **Medium** | 7–24 sub-segments, no overfit | Direction reliable; magnitudes ±20–30% |
| **Low** | Overfit detected (ΔR² > 0.20) | Directional only |

**Data:** Oct–Dec 2025 | 1% HID sample | Lagged quadrant assignment
        """)

    st.markdown("---")

    if not run_sim:
        st.info("Configure cohort and levers in the sidebar, then click **Run Simulation**.")
        st.stop()

    # ── Lookup — pure 5-dim, no baseline JSON needed ─────────────────────────
    e_total = get_elasticity(sel, ELASTICITY_TOTAL)
    e_mid   = get_elasticity(sel, ELASTICITY_MIDROLL)
    e_pre   = get_elasticity(sel, ELASTICITY_PREROLL)

    if e_total is None:
        st.error(
            "No elasticity model found for this 5-dim parent combination. "
            "Try adjusting Gender or Subscription Status."
        )
        st.stop()

    # All baseline numbers directly from the 5-dim elasticity table
    base_hids  = float(e_total.get("total_hid", 1))
    base_total = float(e_total.get("total_inv_total", e_total.get("total_inv", 0)))

    # Midroll and preroll base: from their own elasticity tables (total_inv there = that format's inv)
    base_mid = float(e_mid.get("total_inv", 0)) if e_mid else 0.0
    base_pre = float(e_pre.get("total_inv", 0)) if e_pre else 0.0

    mid_share = (base_mid / base_total * 100) if base_total > 0 else 0.0

    base_ipu_total = base_total / base_hids if base_hids > 0 else 0.0
    base_ipu_mid   = base_mid   / base_hids if base_hids > 0 else 0.0
    base_ipu_pre   = base_pre   / base_hids if base_hids > 0 else 0.0

    # Active Days % — use ad_abs as direct % input (same as WT/VV)
    # ad_abs is already treated as % change here for consistency
    ad_pct_proj = ad_pct  # from sidebar calculation

    cshare = base_total / METADATA.get("total_platform_inventory", 1) * 100

    # ── Project each model ────────────────────────────────────────────────────
    def project(base_ipu, hids, e_dict, wt_pct, ad_pct_val):
        if e_dict is None or base_ipu <= 0:
            return 0.0, 0.0, 0.0
        proj_ipu = apply_el(base_ipu, wt_pct,    float(e_dict.get("elasticity_wt_per_vv", 0)))
        proj_ipu = apply_el(proj_ipu, ad_pct_val, float(e_dict.get("elasticity_active_days", 0)))
        proj_inv  = proj_ipu * hids
        base_inv  = base_ipu * hids
        delta_pct = (proj_inv / base_inv - 1) * 100 if base_inv > 0 else 0
        return proj_inv, delta_pct, proj_ipu

    proj_total, delta_total_pct, _ = project(base_ipu_total, base_hids, e_total, wt_uplift, ad_pct_proj)
    proj_mid,   delta_mid_pct,   _ = project(base_ipu_mid,   base_hids, e_mid,   wt_uplift, ad_pct_proj)
    proj_pre,   delta_pre_pct,   _ = project(base_ipu_pre,   base_hids, e_pre,   wt_uplift, ad_pct_proj)

    # Revenue
    rev_base_mid   = base_mid  * (ecpm_mid / 1000) * (str_pct / 100)
    rev_proj_mid   = proj_mid  * (ecpm_mid / 1000) * (str_pct / 100)
    rev_lift_mid   = rev_proj_mid - rev_base_mid

    rev_base_pre   = base_pre  * (ecpm_pre / 1000) * (str_pct / 100)
    rev_proj_pre   = proj_pre  * (ecpm_pre / 1000) * (str_pct / 100)
    rev_lift_pre   = rev_proj_pre - rev_base_pre

    rev_base_total = rev_base_mid + rev_base_pre
    rev_proj_total = rev_proj_mid + rev_proj_pre
    rev_lift_total = rev_proj_total - rev_base_total

    # ── Confidence badge (based on total model tier) ─────────────────────────
    tier = str(e_total.get("effective_tier", "Medium"))
    r2_in = e_total.get("r2_in_sample", 0)
    r2_cv = e_total.get("r2_loocv", 0)
    n_seg = e_total.get("n_segments", 0)

    st.markdown(f"""
    <div class="{BADGE_CLASSES.get(tier, 'badge-medium')}">
      <div class="badge-title" style="color:{TIER_COLORS.get(tier, '#555')};">{tier} Confidence — Total Model</div>
      <div class="badge-desc">{TIER_DESCS.get(tier, '')}</div>
      <div class="badge-stats">
        R² in-sample: <strong>{r2_in:.3f}</strong> &nbsp;|&nbsp;
        R² LOOCV: <strong>{f"{r2_cv:.3f}" if r2_cv else 'N/A'}</strong> &nbsp;|&nbsp;
        Sub-segments: <strong>{n_seg}</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Midroll confidence badge (if available)
    if e_mid:
        tier_mid = str(e_mid.get("effective_tier", "Medium"))
        if tier_mid != tier:
            st.markdown(f"""
            <div class="{BADGE_CLASSES.get(tier_mid, 'badge-medium')}" style="margin-top:-8px;">
              <div class="badge-title" style="color:{TIER_COLORS.get(tier_mid, '#555')}; font-size:12px;">
                Midroll Model: {tier_mid} Confidence &nbsp;|&nbsp;
                R² LOOCV: {e_mid.get('r2_loocv', 0):.3f} &nbsp;|&nbsp;
                Segs: {e_mid.get('n_segments', 0)}
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Baseline snapshot ─────────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">Baseline — Current State</div>', unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Total Ad Inventory", fmt_inv(base_total))
    b2.metric("Midroll Inventory", fmt_inv(base_mid), help=f"{mid_share:.1f}% of total")
    b3.metric("Preroll Inventory", fmt_inv(base_pre))
    b4.metric("Cohort Inv. Share", f"{cshare:.3f}%")

    # ── Projection results ────────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">Projected Impact — After Lever Changes</div>', unsafe_allow_html=True)

    # Total row
    p1, p2, p3 = st.columns(3)
    p1.metric("Total Projected Inventory", fmt_inv(proj_total),
              delta=f"{delta_total_pct:+.2f}%")
    p2.metric("Total Base Revenue", fmt_rev(rev_base_total))
    p3.metric("Total Projected Revenue", fmt_rev(rev_proj_total),
              delta=f"{fmt_delta(rev_lift_total)} ({(rev_proj_total/rev_base_total-1)*100:+.1f}%)" if rev_base_total > 0 else "N/A")

    # Format split
    st.markdown('<div class="sec-hdr">Inventory & Revenue Split by Format</div>', unsafe_allow_html=True)

    mid_col, pre_col = st.columns(2)

    with mid_col:
        mid_tier = str(e_mid.get("effective_tier", "—")) if e_mid else "No model"
        mid_color = TIER_COLORS.get(mid_tier, "#6B7280")
        delta_mid_str = f"{delta_mid_pct:+.2f}%" if e_mid else "—"
        rev_mid_pct = (rev_proj_mid / rev_base_mid - 1) * 100 if rev_base_mid > 0 else 0
        st.markdown(f"""
        <div class="inv-card">
          <div class="inv-card-title">Midroll</div>
          <table width="100%" style="font-size:13px; border-collapse:collapse;">
            <tr><td style="color:#6B7280; padding:3px 0;">Base inventory</td><td style="text-align:right; font-weight:600;">{fmt_inv(base_mid)}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Projected inventory</td>
                <td style="text-align:right; font-weight:600;">{fmt_inv(proj_mid)}
                <span style="color:{'#059669' if delta_mid_pct>=0 else '#DC2626'}; margin-left:6px; font-size:12px;">({delta_mid_str})</span></td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Incremental inventory</td><td style="text-align:right; font-weight:600;">{fmt_delta(proj_mid - base_mid)}</td></tr>
            <tr style="border-top:1px solid #E5E7EB;"><td style="color:#6B7280; padding:6px 0 3px 0;">Base revenue</td><td style="text-align:right; font-weight:600;">{fmt_rev(rev_base_mid)}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Projected revenue</td><td style="text-align:right; font-weight:600;">{fmt_rev(rev_proj_mid)}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Revenue lift</td>
                <td style="text-align:right; font-weight:700; color:{'#059669' if rev_lift_mid>=0 else '#DC2626'};">{fmt_rev(rev_lift_mid)} ({rev_mid_pct:+.1f}%)</td></tr>
            <tr style="border-top:1px solid #E5E7EB;"><td style="color:#6B7280; padding:6px 0 3px 0;">WT/VV elasticity</td>
                <td style="text-align:right; font-weight:600;">{e_mid.get('elasticity_wt_per_vv', '—') if e_mid else '—'}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">AD elasticity</td>
                <td style="text-align:right; font-weight:600;">{e_mid.get('elasticity_active_days', '—') if e_mid else '—'}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Model confidence</td>
                <td style="text-align:right; font-weight:700; color:{mid_color};">{mid_tier}</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with pre_col:
        pre_tier = str(e_pre.get("effective_tier", "—")) if e_pre else "No model"
        pre_color = TIER_COLORS.get(pre_tier, "#6B7280")
        delta_pre_str = f"{delta_pre_pct:+.2f}%" if e_pre else "—"
        rev_pre_pct = (rev_proj_pre / rev_base_pre - 1) * 100 if rev_base_pre > 0 else 0
        st.markdown(f"""
        <div class="inv-card">
          <div class="inv-card-title">Preroll</div>
          <table width="100%" style="font-size:13px; border-collapse:collapse;">
            <tr><td style="color:#6B7280; padding:3px 0;">Base inventory</td><td style="text-align:right; font-weight:600;">{fmt_inv(base_pre)}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Projected inventory</td>
                <td style="text-align:right; font-weight:600;">{fmt_inv(proj_pre)}
                <span style="color:{'#059669' if delta_pre_pct>=0 else '#DC2626'}; margin-left:6px; font-size:12px;">({delta_pre_str})</span></td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Incremental inventory</td><td style="text-align:right; font-weight:600;">{fmt_delta(proj_pre - base_pre)}</td></tr>
            <tr style="border-top:1px solid #E5E7EB;"><td style="color:#6B7280; padding:6px 0 3px 0;">Base revenue</td><td style="text-align:right; font-weight:600;">{fmt_rev(rev_base_pre)}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Projected revenue</td><td style="text-align:right; font-weight:600;">{fmt_rev(rev_proj_pre)}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Revenue lift</td>
                <td style="text-align:right; font-weight:700; color:{'#059669' if rev_lift_pre>=0 else '#DC2626'};">{fmt_rev(rev_lift_pre)} ({rev_pre_pct:+.1f}%)</td></tr>
            <tr style="border-top:1px solid #E5E7EB;"><td style="color:#6B7280; padding:6px 0 3px 0;">WT/VV elasticity</td>
                <td style="text-align:right; font-weight:600;">{e_pre.get('elasticity_wt_per_vv', '—') if e_pre else '—'}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">AD elasticity</td>
                <td style="text-align:right; font-weight:600;">{e_pre.get('elasticity_active_days', '—') if e_pre else '—'}</td></tr>
            <tr><td style="color:#6B7280; padding:3px 0;">Model confidence</td>
                <td style="text-align:right; font-weight:700; color:{pre_color};">{pre_tier}</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    # ── Business insights (conditional) ──────────────────────────────────────
    insights = []
    if e_total.get("neg_wtvv_warning"):
        wt_coef = e_total.get("elasticity_wt_per_vv", 0)
        insights.append(("insight-box", "Premium Content Ad-Load Shift (Negative WT/VV Elasticity)",
            f"WT/VV coefficient = <strong>{wt_coef:.3f}</strong>. "
            "In this cohort, higher watch time per viewer correlates with <strong>lower</strong> ad inventory per user. "
            "This is the expected dynamic in SVOD-dominant segments: as users deepen their per-session engagement, "
            "they shift into premium library content with reduced ad density. "
            "More watch time is positive for platform health and retention — but ad inventory growth "
            "here depends more on increasing the number of active days than on deepening sessions. "
            "<strong>Active Days is the primary revenue lever for this cohort.</strong>"
        ))
    if e_total.get("neg_ad_warning"):
        ad_coef = e_total.get("elasticity_active_days", 0)
        insights.append(("insight-box", "Session Concentration Pattern (Negative Active Days Elasticity)",
            f"Active Days coefficient = <strong>{ad_coef:.3f}</strong>. "
            "More active days is associated with lower inventory per user in this cohort. "
            "Two patterns drive this: (1) Lifecycle binge — Newly Acquired and Churned users watch "
            "intensely on fewer days, so spreading activity across more days dilutes per-day density. "
            "(2) Sports calendar dependency — inventory concentrates on match days; "
            "non-match days lower the average. "
            "<strong>WT/VV is the stronger lever here.</strong>"
        ))
    if tier == "Low":
        insights.append(("insight-warn", "Low Model Confidence — Overfit Detected",
            f"In-sample R²: {r2_in:.3f} vs LOOCV R²: {r2_cv:.3f}. "
            f"Sub-segments: {n_seg}. "
            "Model fits training data well but generalises poorly. "
            "Treat these numbers as directional — not suitable for revenue commitments."
        ))
    elif tier == "Medium":
        insights.append(("insight-info", "Medium Confidence — Directional Estimate",
            f"R² LOOCV = {r2_cv:.3f} across {n_seg} sub-segments. "
            "Direction of impact is reliable. Magnitudes carry ±20–30% uncertainty — "
            "appropriate for scenario planning, not precise target-setting."
        ))

    if insights:
        st.markdown('<div class="sec-hdr">Analytical Insights for This Cohort</div>', unsafe_allow_html=True)
        for cls, title, body in insights:
            st.markdown(f'<div class="{cls}"><div class="insight-title">{title}</div>{body}</div>', unsafe_allow_html=True)

    # ── Charts ────────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-hdr">Visual Comparison</div>', unsafe_allow_html=True)
    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        df_inv = pd.DataFrame({
            "Scenario": ["Base", "Projected"],
            "Total Inventory": [int(base_total), int(proj_total)]
        }).set_index("Scenario")
        st.bar_chart(df_inv, height=220, color="#3B82F6")
        st.caption(f"Total: {fmt_inv(base_total)} → {fmt_inv(proj_total)} ({delta_total_pct:+.1f}%)")
    with ch2:
        df_mid_chart = pd.DataFrame({
            "Scenario": ["Base", "Projected"],
            "Midroll Inventory": [int(base_mid), int(proj_mid)]
        }).set_index("Scenario")
        st.bar_chart(df_mid_chart, height=220, color="#8B5CF6")
        st.caption(f"Midroll: {fmt_inv(base_mid)} → {fmt_inv(proj_mid)} ({delta_mid_pct:+.1f}%)" if e_mid else "Midroll: no model")
    with ch3:
        df_rev_chart = pd.DataFrame({
            "Scenario": ["Base", "Projected"],
            "Revenue (Mid+Pre)": [int(rev_base_total), int(rev_proj_total)]
        }).set_index("Scenario")
        st.bar_chart(df_rev_chart, height=220, color="#10B981")
        st.caption(f"Revenue: {fmt_rev(rev_base_total)} → {fmt_rev(rev_proj_total)}")

    # ── Full coefficients expander ─────────────────────────────────────────────
    with st.expander("Full model coefficients for this cohort (all 3 models)"):
        coef_rows = []
        for label, e_dict in [("Total", e_total), ("Midroll", e_mid), ("Preroll", e_pre)]:
            if e_dict is None:
                coef_rows.append({"Model": label, "Tier": "No model", "WT/VV β": "—",
                                   "AD β": "—", "Intercept": "—", "R² in": "—", "R² LOOCV": "—", "Segs": "—"})
            else:
                coef_rows.append({
                    "Model":    label,
                    "Tier":     e_dict.get("effective_tier", "—"),
                    "WT/VV β":  f"{e_dict.get('elasticity_wt_per_vv', 0):.4f}",
                    "AD β":     f"{e_dict.get('elasticity_active_days', 0):.4f}",
                    "Intercept": f"{e_dict.get('intercept', 0):.4f}",
                    "R² in":    f"{e_dict.get('r2_in_sample', 0):.4f}",
                    "R² LOOCV": f"{e_dict.get('r2_loocv', 0):.4f}" if e_dict.get('r2_loocv') else "—",
                    "Segs":     e_dict.get("n_segments", "—"),
                })
        st.dataframe(pd.DataFrame(coef_rows), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════════════
# PAGE 2 — COHORT EXPLORER
# ════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## Cohort Explorer")
    st.caption("Browse all 5-dim parent cohorts from the total inventory model. Click any column header to sort.")

    # Pre-computed at startup — no heavy loops here
    df_exp = build_explorer_df()

    if df_exp.empty:
        st.warning("No cohort data loaded. Paste your ELASTICITY_TOTAL JSON data first.")
        st.stop()

    # Summary KPIs
    ck1, ck2, ck3, ck4 = st.columns(4)
    ck1.metric("Total Cohorts", f"{len(df_exp)}")
    ck2.metric("High Confidence", f"{(df_exp['Confidence Tier']=='High').sum()}")
    ck3.metric("Medium Confidence", f"{(df_exp['Confidence Tier']=='Medium').sum()}")
    ck4.metric("Low / Overfit", f"{(df_exp['Confidence Tier']=='Low').sum()}")

    st.markdown("---")

    # Filters first — apply before view preset so they stack correctly
    f1, f2, f3, f4, f5 = st.columns(5)
    fq = f1.multiselect("Quadrant", sorted(df_exp["Engagement Quadrant"].unique()), key="fq")
    fp = f2.multiselect("Platform", sorted(df_exp["Platform"].unique()), key="fp")
    fg = f3.multiselect("Gender", sorted(df_exp["Gender"].unique()), key="fg")
    fs = f4.multiselect("Subs Status", sorted(df_exp["Subscription Status"].unique()), key="fs")
    ft = f5.multiselect("Confidence", ["High", "Medium", "Low"], key="ft")

    disp = df_exp.copy()
    if fq: disp = disp[disp["Engagement Quadrant"].isin(fq)]
    if fp: disp = disp[disp["Platform"].isin(fp)]
    if fg: disp = disp[disp["Gender"].isin(fg)]
    if fs: disp = disp[disp["Subscription Status"].isin(fs)]
    if ft: disp = disp[disp["Confidence Tier"].isin(ft)]

    # View preset applied on top of filters
    view = st.selectbox(
        "Sort / View",
        ["All — sorted by HID volume", "Top 10 by HID Volume", "Bottom 10 by HID Volume"],
        key="exp_view"
    )
    if view == "Top 10 by HID Volume":   disp = disp.nlargest(10, "HID-months")
    elif view == "Bottom 10 by HID Volume": disp = disp.nsmallest(10, "HID-months")

    show_cols = [
        "Engagement Quadrant", "Platform", "Gender", "Subscription Status", "Seasonality",
        "Confidence Tier", "Sub-segments", "HID-months", "HID Share (%)",
        "WT/VV Elasticity (β₁)", "AD Elasticity (β₂)", "R² In-sample", "R² LOOCV",
    ]
    show_cols = [c for c in show_cols if c in disp.columns]

    st.dataframe(
        disp[show_cols].sort_values("HID-months", ascending=False),
        use_container_width=True,
        height=520,
        column_config={
            "HID-months":             st.column_config.NumberColumn(format="%d"),
            "WT/VV Elasticity (β₁)": st.column_config.NumberColumn(format="%.4f"),
            "AD Elasticity (β₂)":   st.column_config.NumberColumn(format="%.4f"),
            "R² In-sample":          st.column_config.NumberColumn(format="%.3f"),
            "R² LOOCV":              st.column_config.NumberColumn(format="%.3f"),
            "HID Share (%)":         st.column_config.NumberColumn(format="%.2f%%"),
        }
    )
    st.caption(f"Showing {len(disp)} of {len(df_exp)} cohorts. Click any column header to sort.")

    # Simple distribution charts — pre-computed from df_exp, no loops
    st.markdown('<div class="sec-hdr">Distribution by Dimension</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)

    with d1:
        quad_counts = df_exp.groupby("Engagement Quadrant")["HID-months"].sum().sort_values(ascending=False)
        quad_pct = (quad_counts / quad_counts.sum() * 100).round(1).rename("HID Share (%)")
        st.bar_chart(quad_pct, height=200)
        st.caption("HID Share by Quadrant")

    with d2:
        plat_counts = df_exp.groupby("Platform")["HID-months"].sum().sort_values(ascending=False)
        plat_pct = (plat_counts / plat_counts.sum() * 100).round(1).rename("HID Share (%)")
        st.bar_chart(plat_pct, height=200)
        st.caption("HID Share by Platform")

    with d3:
        tier_counts = df_exp.groupby("Confidence Tier")["Sub-segments"].count().sort_values(ascending=False)
        st.bar_chart(tier_counts.rename("Cohort Count"), height=200)
        st.caption("Cohorts by Confidence Tier")


# ════════════════════════════════════════════════════════════════════════
# PAGE 3 — MODEL ARCHITECTURE
# Pure markdown — no computation, no loops, instant render
# ════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## Model Architecture & Technical Methodology")
    st.caption("End-to-end pipeline: data sourcing, feature decisions, statistical specification, three-model architecture, validation, and limitations.")

    st.markdown("""
### 1. Data Foundation

**Source:** `tmp_master_inv_clean` (derived from `watchtime_master_monthly`)

**Scope:** Oct–Dec 2025 | 1% random sample of platform HIDs | HID-month grain

| Variable | Definition | Role |
|----------|-----------|------|
| `lagged_engagement_quadrant` | Quadrant from prior month's behaviour | Grouping dimension |
| `platform_group` | CTV / Mobile / Web | Grouping dimension |
| `gender_clean` | Male / Female / Unknown / Other | Grouping dimension |
| `subs_status` | Active SVOD / AVOD / Newly Acquired / Churned | Grouping dimension |
| `seasonality` | Oct–Nov = Ent; Dec = Mixed | Grouping dimension |
| `ent_wt_mins` | Entertainment watch time in minutes | Source for WT/VV |
| `active_days` | Distinct active days in the month | Engagement predictor |
| `total_inventory` | **Y variable** — total ad slots served | Primary outcome |
| `total_midroll_inv` | Midroll ad slots | Midroll model outcome |
| `total_preroll_inv` | Preroll ad slots | Preroll model outcome |

**Why lagged quadrant?** Same-period quadrant assignment creates simultaneity bias — users who see more ads
tend to watch more, artificially inflating elasticity estimates. Lagging by one month eliminates this.

---

### 2. Three-Model Architecture

Three separate log-log WLS regressions, each fitted at the 5-dim parent level:

| Model | Y Variable | Predictors | Business Driver |
|-------|-----------|-----------|----------------|
| **Total** | `total_inventory / HID` | WT/VV, Active Days | Overall inventory planning |
| **Midroll** | `midroll_inv / HID` | WT/VV, Active Days | Watch-depth driven: more minutes → more midroll slots |
| **Preroll** | `preroll_inv / HID` | WT/VV, Active Days | Session-entry driven: more days → more session starts |

**Why the same predictors for preroll?**

VV/AU (viewer conversion rate per active user) was tested as a primary preroll predictor — preroll fires
at session start, so session-frequency should theoretically matter. However, at cohort level, VV/AU
values compress into the 0.95–1.0 range across all cohorts. Log(0.99) ≈ −0.01. The variance is in
the 4th decimal place. OLS amplified this near-zero variance into coefficients ranging from −181 to +81
with a standard deviation of 23 and 48.7% negative signs — a coin flip, not a signal.

The session-frequency information VV/AU was meant to capture is better proxied by Active Days in this
aggregation structure. All three final models use WT/VV and Active Days only.

---

### 3. Statistical Specification

**Model equation (log-log form):**

> `ln(Inventory per User) = α + β₁ · ln(WT/VV) + β₂ · ln(Active Days) + ε`

**Why log-log?**
- Both ad inventory and engagement are right-skewed; log transformation normalises residuals
- Coefficients β₁ and β₂ are elasticities: directly interpretable as percentage-change relationships
- Scale-invariant — valid across cohorts with very different absolute engagement levels

**Weights:** Each sub-segment weighted by its HID count. Larger sub-cohorts have proportionally
more influence on fitted coefficients, preventing small noisy sub-segments from distorting estimates.

**Multicollinearity (VIF check):** VIF between WT/VV and Active Days = 1.50 — well below the threshold
of 5. No multicollinearity concern.

---

### 4. Validation — LOOCV & Confidence Tiering

**Leave-One-Out Cross-Validation (LOOCV):**

For each parent cohort with N sub-segments:
1. Remove one sub-segment (hold-out)
2. Re-fit regression on remaining N−1 sub-segments
3. Predict held-out inventory
4. Repeat for all N → compute out-of-sample R²

**Overfit criterion:** `R² in-sample − R² LOOCV > 0.20` → flagged as overfit

**Tier assignment:**

| Condition | Tier |
|-----------|------|
| n ≥ 25 sub-segments AND no overfit | **High** |
| 7 ≤ n < 25 AND no overfit | **Medium** |
| Overfit detected (any n) | **Low** |
| n < 4 | Not modelled |

---

### 5. Coverage Summary

| Model | Inventory Type | High Confidence |
|-------|---------------|----------------|
| Total | Total ad inventory | ~98% modelled |
| Midroll | Midroll slots | Separate model |
| Preroll | Preroll slots | Separate model |

Midroll and Preroll shares visible in Simulator top strip after Run Simulation.

---

### 6. Simulator Prediction Logic

**Step 1 — Cohort selection (7 dimensions)**
- 5-dim parent lookup → elasticity coefficients (β₁, β₂) + confidence tier
- 7-dim exact lookup → baseline inventory, WT/VV, Active Days from actual data

**Step 2 — Lever inputs**
- WT/VV: percentage change (−10% to +100%)
- Active Days: absolute days (−10 to +31), converted to % using cohort's own avg_active_days

**Step 3 — Projection (applied per model independently)**
```
proj_ipu = base_ipu × (1 + WT/VV %)^β_WT × (1 + Active Days %)^β_AD
proj_total = proj_ipu × HID-months
Revenue = proj_total × (eCPM / 1,000) × Sell-Through Rate
```

**Step 4 — Output**
- Inventory delta (absolute + %) per format (Total, Midroll, Preroll)
- Revenue lift (Rs.) per format with separate eCPM inputs
- Confidence badge with R² diagnostics
- Conditional business insights for negative elasticities or low confidence

---

### 7. Key Assumptions & Limitations

| Assumption / Limitation | Implication |
|--------------------------|-------------|
| Associative, not causal | Elasticities measure historical co-variation, not guaranteed causal effects |
| 1% sample | Directional patterns robust; exact magnitudes carry sampling variance |
| Oct–Dec 2025 only | IPL season will shift Sports cohort coefficients substantially |
| Lagged quadrant reduces but does not eliminate confounding | Unobserved factors (content slate, marketing) may confound estimates |
| Midroll and preroll models are independent | Projected splits may not perfectly sum to total model projection |
| Revenue depends on user-supplied eCPM and STR | Treat revenue output as directional; actual rates vary by deal |
| Dominant Proposition 'Unknown' | Valid segment — users without a clear dominant content category; modelled as-is |
    """)

    st.markdown("---")
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Source HID-months", "9.17 Mn")
    k2.metric("1% Sample", "~91.7 K")
    k3.metric("Corr. Pairs Tested", "306")
    k4.metric("Strong Corr.", "35")
    k5.metric("Parent Cohorts", f"{METADATA.get('total_parents', 117)}")
    k6.metric("Models Run", "3")
