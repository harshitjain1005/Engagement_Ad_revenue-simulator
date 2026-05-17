"""
Engagement to Ad Revenue Simulator
JioStar | Monetization Intelligence
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
  .block-container { padding-top: 0.6rem !important; padding-bottom: 1rem !important; }
 
  /* Tabs pushed down */
  div[data-testid="stTabs"] { margin-top: 2.2rem; }
  div[data-testid="stTabsContent"] { padding-top: 0.5rem; }
 
  div[data-testid="metric-container"] {
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 10px; padding: 14px 16px;
  }
  div[data-testid="metric-container"] label {
    font-size: 10px !important; font-weight: 700 !important;
    text-transform: uppercase; letter-spacing: 0.6px; opacity: 0.65;
  }
  div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 20px !important; font-weight: 700 !important;
  }
 
  .sec-hdr {
    font-size: 10px; font-weight: 700; opacity: 0.55;
    text-transform: uppercase; letter-spacing: 1px;
    padding-bottom: 5px;
    border-bottom: 2px solid rgba(128,128,128,0.18);
    margin: 14px 0 9px 0;
  }
 
  .badge-high   { border:1.5px solid #6EE7B7; border-left:5px solid #059669; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .badge-medium { border:1.5px solid #FCD34D; border-left:5px solid #D97706; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .badge-low    { border:1.5px solid #FCA5A5; border-left:5px solid #DC2626; border-radius:8px; padding:12px 16px; margin:8px 0; }
  .badge-title  { font-size:13px; font-weight:700; margin-bottom:3px; }
  .badge-desc   { font-size:12px; margin-bottom:4px; line-height:1.5; opacity:0.85; }
  .badge-stats  { font-size:11px; opacity:0.6; }
 
  .insight-box  { border-left:5px solid #EA580C; border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0; font-size:12.5px; line-height:1.6; }
  .insight-info { border-left:5px solid #3B82F6; border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0; font-size:12.5px; line-height:1.6; }
  .insight-warn { border-left:5px solid #DC2626; border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0; font-size:12.5px; line-height:1.6; }
  .insight-title { font-weight:700; margin-bottom:2px; }
 
  .pct-card {
    border: 1px solid rgba(128,128,128,0.2);
    border-radius: 12px; padding: 16px 20px; margin: 3px 0;
  }
  .pct-label { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; opacity:0.55; margin-bottom:6px; }
  .pct-big-pos { font-size:38px; font-weight:800; color:#059669; line-height:1.05; }
  .pct-big-neg { font-size:38px; font-weight:800; color:#DC2626; line-height:1.05; }
  .pct-big-neu { font-size:38px; font-weight:800; opacity:0.35; line-height:1.05; }
 
  /* STR context box */
  .str-box {
    border: 1px dashed rgba(128,128,128,0.32);
    border-radius: 10px; margin: 10px 0;
    display: flex; align-items: stretch; overflow: hidden;
  }
  .str-dims {
    flex: 1; padding: 14px 18px;
    display: flex; flex-direction: column; justify-content: center; gap: 4px;
  }
  .str-dims-title { font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:0.6px; opacity:0.45; margin-bottom:5px; }
  .str-dim-row { font-size:12px; line-height:1.55; }
  .str-dim-k { opacity:0.55; }
  .str-dim-v { font-weight:600; }
  .str-note { font-size:10.5px; opacity:0.45; margin-top:7px; padding-top:7px; border-top:1px solid rgba(128,128,128,0.15); font-style:italic; }
  .str-ecpm { font-size:11px; opacity:0.55; margin-top:5px; }
  .str-val {
    min-width:120px; display:flex; flex-direction:column; align-items:center; justify-content:center;
    padding:14px 20px;
    border-left:1px solid rgba(128,128,128,0.18);
  }
  .str-val-lbl { font-size:9px; font-weight:700; text-transform:uppercase; letter-spacing:0.6px; opacity:0.4; margin-bottom:4px; }
  .str-val-num { font-size:40px; font-weight:800; color:#3B82F6; line-height:1; }
  .str-val-sub { font-size:9.5px; opacity:0.35; margin-top:3px; }
 
  /* Equation box */
  .eq-wrap { border:1.5px dashed rgba(128,128,128,0.28); border-radius:10px; padding:16px 20px; margin:8px 0; }
  .eq-title { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.7px; opacity:0.45; margin-bottom:10px; }
  .eq-base { font-family:'Courier New',monospace; font-size:13px; line-height:1.7; background:rgba(128,128,128,0.07); padding:8px 12px; border-radius:6px; margin-bottom:10px; }
  .eq-vals { font-family:'Courier New',monospace; font-size:13px; line-height:1.9; }
  .eq-similarly { font-size:12px; opacity:0.65; margin:8px 0 4px 0; }
  .eq-coeff-row { font-size:11px; opacity:0.5; font-family:'Courier New',monospace; margin-top:4px; }
  .rpos { color:#059669; font-weight:800; }
  .rneg { color:#DC2626; font-weight:800; }
  .rneu { opacity:0.4; }
  .enote { color:#EA580C; font-size:10.5px; margin-left:6px; font-family:'Segoe UI',sans-serif; }
 
  .sb-lbl { font-size:9.5px; font-weight:700; opacity:0.55; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:2px; }
  .sb-divider { border:none; border-top:1px dashed rgba(128,128,128,0.3); margin:10px 0; }
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


### PASTE BLOCK 1: METADATA ###
METADATA = {"total_platform_inventory": 768495767.0, "midroll_platform_inventory": 445076969.0, "preroll_platform_inventory": 107168029.0, "midroll_share_of_total": 57.92, "preroll_share_of_total": 13.95, "coverage_total": 98.29, "coverage_midroll": 98.1, "coverage_preroll": 98.21, "high_pct_total": 36.8, "high_pct_midroll": 36.8, "high_pct_preroll": 36.8, "total_parents": 117, "total_cohorts_7dim": 3222}


### PASTE BLOCK 2: DIMENSION VALUES ###
DIMENSION_VALUES = {
  "lagged_engagement_quadrant": ["Ent Only", "Sports & Ent", "Fringe", "Sports Only"],
  "platform_group": ["Mobile", "CTV", "Web"],
  "gender_clean": ["Male", "Female", "Unknown", "Other"],
  "subs_status": ["Active (SVOD)", "Non Subscriber (AVOD)", "Newly Acquired", "Churned"],
  "seasonality": ["Ent", "Mixed"],
  "age_group": ["GenZ (18-24)", "Young Adult (25-34)", "Unknown", "Mid Adult (35-44)", "45+", "Teen (13-17)"],
  "dominant_proposition": ["network fiction gec", "network non fiction gec", "indian movies", "specials", "international", "kids", "others", "creator content", "Unknown"],
  "dominant_plan_type" : ["singledevice","hotstarmobile","hotstarbundle","hotstarsuper","free"]
}


### PASTE BLOCK 3: ELASTICITY — TOTAL ###
ELASTICITY_TOTAL = {
"Ent Only | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.2649, "elasticity_active_days": 2.5966, "intercept": 0.8085, "r2_in_sample": 0.919, "r2_loocv": 0.8851, "n_segments": 37, "total_hid": 149518, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.5758, "elasticity_active_days": 3.8152, "intercept": -0.6792, "r2_in_sample": 0.9697, "r2_loocv": 0.9577, "n_segments": 40, "total_hid": 204893, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7491, "elasticity_active_days": 1.3841, "intercept": -2.7129, "r2_in_sample": 0.9598, "r2_loocv": 0.9433, "n_segments": 31, "total_hid": 72325, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.578, "elasticity_active_days": 1.4211, "intercept": -2.1059, "r2_in_sample": 0.9526, "r2_loocv": 0.9318, "n_segments": 38, "total_hid": 81533, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.5619, "elasticity_active_days": 3.3587, "intercept": -7.8956, "r2_in_sample": 0.9701, "r2_loocv": 0.9572, "n_segments": 46, "total_hid": 120772, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.769, "elasticity_active_days": 1.5312, "intercept": -4.1261, "r2_in_sample": 0.953, "r2_loocv": 0.9371, "n_segments": 36, "total_hid": 55861, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.1282, "elasticity_active_days": 2.9057, "intercept": -1.0788, "r2_in_sample": 0.9681, "r2_loocv": 0.9573, "n_segments": 33, "total_hid": 84045, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.1728, "elasticity_active_days": 2.0767, "intercept": -0.9493, "r2_in_sample": 0.9498, "r2_loocv": 0.7349, "n_segments": 8, "total_hid": 48818, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7753, "elasticity_active_days": 3.4449, "intercept": -9.4357, "r2_in_sample": 0.9767, "r2_loocv": 0.9713, "n_segments": 42, "total_hid": 92313, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.3244, "elasticity_active_days": 3.1822, "intercept": -5.7455, "r2_in_sample": 0.9805, "r2_loocv": 0.976, "n_segments": 35, "total_hid": 42845, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.2871, "elasticity_active_days": 1.7482, "intercept": -0.7806, "r2_in_sample": 0.9423, "r2_loocv": 0.917, "n_segments": 32, "total_hid": 28186, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.4162, "elasticity_active_days": 1.6598, "intercept": -0.5392, "r2_in_sample": 0.9452, "r2_loocv": 0.928, "n_segments": 34, "total_hid": 102631, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.6053, "elasticity_active_days": 3.8496, "intercept": -0.4429, "r2_in_sample": 0.9718, "r2_loocv": 0.8932, "n_segments": 21, "total_hid": 27760, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9967, "elasticity_active_days": 0.7685, "intercept": -3.2533, "r2_in_sample": 0.9673, "r2_loocv": 0.9581, "n_segments": 35, "total_hid": 29099, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9713, "elasticity_active_days": 1.8165, "intercept": -4.3297, "r2_in_sample": 0.8147, "r2_loocv": 0.7854, "n_segments": 48, "total_hid": 146503, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.375, "elasticity_active_days": 4.5483, "intercept": -4.6358, "r2_in_sample": 0.9566, "r2_loocv": 0.6693, "n_segments": 7, "total_hid": 21858, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.794, "elasticity_active_days": 1.8319, "intercept": -2.9354, "r2_in_sample": 0.9722, "r2_loocv": 0.9672, "n_segments": 38, "total_hid": 102405, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.4678, "elasticity_active_days": 2.93, "intercept": -5.6556, "r2_in_sample": 0.952, "r2_loocv": 0.9314, "n_segments": 28, "total_hid": 16137, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.0307, "elasticity_active_days": 2.5788, "intercept": -0.725, "r2_in_sample": 0.9765, "r2_loocv": 0.4594, "n_segments": 7, "total_hid": 19312, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.039, "elasticity_active_days": 2.4093, "intercept": -4.3377, "r2_in_sample": 0.8799, "r2_loocv": 0.8421, "n_segments": 48, "total_hid": 190254, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.2028, "elasticity_active_days": 4.3191, "intercept": -5.1238, "r2_in_sample": 0.9807, "r2_loocv": 0.8832, "n_segments": 7, "total_hid": 16736, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.0761, "elasticity_active_days": 1.4461, "intercept": -2.7554, "r2_in_sample": 0.8027, "r2_loocv": 0.694, "n_segments": 42, "total_hid": 100265, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.0014, "elasticity_active_days": 3.3347, "intercept": -3.6562, "r2_in_sample": 0.9481, "r2_loocv": 0.9267, "n_segments": 24, "total_hid": 10703, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7622, "elasticity_active_days": 1.1066, "intercept": -2.3855, "r2_in_sample": 0.9623, "r2_loocv": 0.9502, "n_segments": 25, "total_hid": 11783, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9871, "elasticity_active_days": 1.2332, "intercept": -2.8503, "r2_in_sample": 0.8156, "r2_loocv": 0.7442, "n_segments": 39, "total_hid": 43568, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.102, "elasticity_active_days": 2.162, "intercept": -0.362, "r2_in_sample": 0.8562, "r2_loocv": 0.7664, "n_segments": 20, "total_hid": 13591, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.0051, "elasticity_active_days": 1.2778, "intercept": -2.6743, "r2_in_sample": 0.9844, "r2_loocv": 0.9771, "n_segments": 27, "total_hid": 48067, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.1505, "elasticity_active_days": 3.6605, "intercept": -2.9286, "r2_in_sample": 0.9474, "r2_loocv": 0.928, "n_segments": 29, "total_hid": 18689, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8508, "elasticity_active_days": 2.0002, "intercept": -5.4847, "r2_in_sample": 0.9818, "r2_loocv": 0.9768, "n_segments": 25, "total_hid": 13147, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.0181, "elasticity_active_days": 3.4477, "intercept": -3.7951, "r2_in_sample": 0.9818, "r2_loocv": 0.9756, "n_segments": 23, "total_hid": 8666, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.2736, "elasticity_active_days": 2.2409, "intercept": -1.8122, "r2_in_sample": 0.9628, "r2_loocv": 0.7421, "n_segments": 15, "total_hid": 11196, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.0391, "elasticity_active_days": 2.4311, "intercept": -0.2898, "r2_in_sample": 0.9463, "r2_loocv": 0.9233, "n_segments": 19, "total_hid": 13499, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.0403, "elasticity_active_days": 1.459, "intercept": -3.3763, "r2_in_sample": 0.9828, "r2_loocv": 0.9773, "n_segments": 30, "total_hid": 43351, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.0657, "elasticity_active_days": 3.4585, "intercept": -2.9527, "r2_in_sample": 0.973, "r2_loocv": 0.9662, "n_segments": 27, "total_hid": 16384, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6147, "elasticity_active_days": 2.7647, "intercept": -6.4668, "r2_in_sample": 0.9601, "r2_loocv": 0.8381, "n_segments": 12, "total_hid": 11076, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8141, "elasticity_active_days": 1.7235, "intercept": -3.141, "r2_in_sample": 0.6942, "r2_loocv": 0.5997, "n_segments": 42, "total_hid": 56787, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.916, "elasticity_active_days": 1.9642, "intercept": -4.8831, "r2_in_sample": 0.9076, "r2_loocv": 0.885, "n_segments": 36, "total_hid": 24941, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.0959, "elasticity_active_days": 2.1757, "intercept": -3.8122, "r2_in_sample": 0.9462, "r2_loocv": 0.9286, "n_segments": 34, "total_hid": 46039, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.187, "elasticity_active_days": 2.6202, "intercept": -5.1457, "r2_in_sample": 0.8849, "r2_loocv": 0.8431, "n_segments": 45, "total_hid": 81554, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0541, "elasticity_active_days": 0.8976, "intercept": -3.0183, "r2_in_sample": 0.873, "r2_loocv": 0.7885, "n_segments": 20, "total_hid": 8802, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8084, "elasticity_active_days": 4.3773, "intercept": -11.2969, "r2_in_sample": 0.925, "r2_loocv": 0.9139, "n_segments": 49, "total_hid": 79586, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.1669, "elasticity_active_days": 2.3655, "intercept": -0.7007, "r2_in_sample": 0.87, "r2_loocv": 0.2473, "n_segments": 20, "total_hid": 18181, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.1863, "elasticity_active_days": 3.6912, "intercept": -2.6207, "r2_in_sample": 0.7977, "r2_loocv": 0.7564, "n_segments": 30, "total_hid": 20185, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9046, "elasticity_active_days": 1.4618, "intercept": -3.662, "r2_in_sample": 0.9, "r2_loocv": 0.8645, "n_segments": 34, "total_hid": 21491, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2104, "elasticity_active_days": -0.6165, "intercept": -0.2757, "r2_in_sample": 0.8588, "r2_loocv": 0.5079, "n_segments": 24, "total_hid": 57541, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.866, "elasticity_active_days": 3.0165, "intercept": -8.7207, "r2_in_sample": 0.9937, "r2_loocv": 0.9483, "n_segments": 7, "total_hid": 8443, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6108, "elasticity_active_days": 1.8182, "intercept": -2.6721, "r2_in_sample": 0.9388, "r2_loocv": 0.9152, "n_segments": 16, "total_hid": 5336, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7191, "elasticity_active_days": 1.3185, "intercept": -3.0269, "r2_in_sample": 0.7868, "r2_loocv": 0.7334, "n_segments": 45, "total_hid": 63748, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5421, "elasticity_active_days": 2.7419, "intercept": -3.8911, "r2_in_sample": 0.9569, "r2_loocv": 0.8466, "n_segments": 7, "total_hid": 14929, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2132, "elasticity_active_days": 0.2463, "intercept": -3.6824, "r2_in_sample": 0.813, "r2_loocv": 0.7032, "n_segments": 24, "total_hid": 8421, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5896, "elasticity_active_days": 1.5864, "intercept": -2.0676, "r2_in_sample": 0.9396, "r2_loocv": 0.8934, "n_segments": 16, "total_hid": 5102, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.3005, "elasticity_active_days": 2.6881, "intercept": -3.1327, "r2_in_sample": 0.9683, "r2_loocv": 0.9516, "n_segments": 18, "total_hid": 5564, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4136, "elasticity_active_days": 2.2283, "intercept": -2.795, "r2_in_sample": 0.9764, "r2_loocv": 0.9651, "n_segments": 18, "total_hid": 5600, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1687, "elasticity_active_days": -0.7728, "intercept": -0.2547, "r2_in_sample": 0.7477, "r2_loocv": 0.4312, "n_segments": 21, "total_hid": 15800, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7576, "elasticity_active_days": 3.9254, "intercept": -10.1811, "r2_in_sample": 0.9278, "r2_loocv": 0.8884, "n_segments": 20, "total_hid": 5977, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.2776, "elasticity_active_days": 1.928, "intercept": -6.0024, "r2_in_sample": 0.8882, "r2_loocv": 0.8315, "n_segments": 32, "total_hid": 21099, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1066, "elasticity_active_days": 1.306, "intercept": -3.2115, "r2_in_sample": 0.9906, "r2_loocv": 0.9722, "n_segments": 13, "total_hid": 7854, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5113, "elasticity_active_days": 4.5708, "intercept": -10.4507, "r2_in_sample": 0.9674, "r2_loocv": 0.9569, "n_segments": 22, "total_hid": 7357, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9994, "elasticity_active_days": 0.4526, "intercept": -2.4565, "r2_in_sample": 0.879, "r2_loocv": 0.8187, "n_segments": 18, "total_hid": 3409, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.08, "elasticity_active_days": 0.5382, "intercept": -1.0028, "r2_in_sample": 0.8983, "r2_loocv": 0.5771, "n_segments": 22, "total_hid": 25309, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.3085, "elasticity_active_days": 4.6319, "intercept": -5.8151, "r2_in_sample": 0.9255, "r2_loocv": 0.9006, "n_segments": 21, "total_hid": 5425, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9387, "elasticity_active_days": 3.7051, "intercept": -8.7765, "r2_in_sample": 0.9044, "r2_loocv": 0.8767, "n_segments": 24, "total_hid": 9010, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.755, "elasticity_active_days": 2.3064, "intercept": -4.222, "r2_in_sample": 0.9135, "r2_loocv": 0.8875, "n_segments": 17, "total_hid": 3522, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7813, "elasticity_active_days": 2.4354, "intercept": -4.6446, "r2_in_sample": 0.9495, "r2_loocv": 0.925, "n_segments": 24, "total_hid": 8331, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8779, "elasticity_active_days": 2.6166, "intercept": -5.5957, "r2_in_sample": 0.9171, "r2_loocv": 0.8965, "n_segments": 45, "total_hid": 52157, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1467, "elasticity_active_days": 0.5539, "intercept": -3.1628, "r2_in_sample": 0.9241, "r2_loocv": 0.8859, "n_segments": 22, "total_hid": 5239, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.86, "elasticity_active_days": 1.7844, "intercept": -3.7764, "r2_in_sample": 0.8213, "r2_loocv": 0.7783, "n_segments": 31, "total_hid": 11670, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.1311, "elasticity_active_days": -1.4676, "intercept": -5.139, "r2_in_sample": 0.9169, "r2_loocv": 0.8629, "n_segments": 17, "total_hid": 2487, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6568, "elasticity_active_days": 1.019, "intercept": -5.6101, "r2_in_sample": 0.8838, "r2_loocv": 0.795, "n_segments": 24, "total_hid": 13885, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.0118, "elasticity_active_days": 4.239, "intercept": -6.696, "r2_in_sample": 0.881, "r2_loocv": 0.8, "n_segments": 21, "total_hid": 4283, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9279, "elasticity_active_days": 3.0742, "intercept": -8.9133, "r2_in_sample": 0.8895, "r2_loocv": 0.8584, "n_segments": 18, "total_hid": 4472, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0795, "elasticity_active_days": 3.5126, "intercept": -10.7861, "r2_in_sample": 0.8951, "r2_loocv": 0.8595, "n_segments": 18, "total_hid": 4245, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7246, "elasticity_active_days": 0.8347, "intercept": -1.2597, "r2_in_sample": 0.7811, "r2_loocv": 0.7034, "n_segments": 40, "total_hid": 37545, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6097, "elasticity_active_days": 1.7734, "intercept": -2.2125, "r2_in_sample": 0.8443, "r2_loocv": 0.7941, "n_segments": 26, "total_hid": 11210, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.776, "elasticity_active_days": 1.1428, "intercept": -2.5854, "r2_in_sample": 0.936, "r2_loocv": 0.9099, "n_segments": 17, "total_hid": 2437, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8182, "elasticity_active_days": 2.6416, "intercept": -6.9256, "r2_in_sample": 0.929, "r2_loocv": 0.9023, "n_segments": 31, "total_hid": 9852, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6331, "elasticity_active_days": -0.3537, "intercept": -3.2058, "r2_in_sample": 0.8448, "r2_loocv": 0.7423, "n_segments": 16, "total_hid": 3934, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7196, "elasticity_active_days": 1.9988, "intercept": -2.6008, "r2_in_sample": 0.7209, "r2_loocv": 0.6354, "n_segments": 30, "total_hid": 13481, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.7965, "elasticity_active_days": -1.3073, "intercept": -3.3747, "r2_in_sample": 0.9501, "r2_loocv": 0.9262, "n_segments": 18, "total_hid": 2415, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.2685, "elasticity_active_days": 2.249, "intercept": -1.1896, "r2_in_sample": 0.9204, "r2_loocv": 0.7685, "n_segments": 8, "total_hid": 9503, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4425, "elasticity_active_days": 3.3923, "intercept": -2.9824, "r2_in_sample": 0.8376, "r2_loocv": 0.5538, "n_segments": 8, "total_hid": 11900, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.663, "elasticity_active_days": 1.3842, "intercept": -2.8513, "r2_in_sample": 0.7886, "r2_loocv": 0.7189, "n_segments": 27, "total_hid": 10022, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.0806, "elasticity_active_days": 2.3589, "intercept": -1.4617, "r2_in_sample": 0.7776, "r2_loocv": 0.5331, "n_segments": 19, "total_hid": 3249, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2181, "elasticity_active_days": 1.1481, "intercept": -5.489, "r2_in_sample": 0.9505, "r2_loocv": 0.9398, "n_segments": 24, "total_hid": 4866, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0443, "elasticity_active_days": 0.7903, "intercept": -2.1604, "r2_in_sample": 0.6877, "r2_loocv": 0.0232, "n_segments": 14, "total_hid": 6576, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8058, "elasticity_active_days": 1.6566, "intercept": -2.8394, "r2_in_sample": 0.9072, "r2_loocv": 0.8667, "n_segments": 21, "total_hid": 5919, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.5256, "elasticity_active_days": 1.866, "intercept": -6.826, "r2_in_sample": 0.9157, "r2_loocv": 0.8288, "n_segments": 15, "total_hid": 4149, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.4865, "elasticity_active_days": 0.448, "intercept": -4.9548, "r2_in_sample": 0.9471, "r2_loocv": 0.9279, "n_segments": 18, "total_hid": 2200, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.3892, "elasticity_active_days": 1.0439, "intercept": -6.0853, "r2_in_sample": 0.8979, "r2_loocv": 0.8649, "n_segments": 20, "total_hid": 4300, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9044, "elasticity_active_days": -0.1775, "intercept": 0.1204, "r2_in_sample": 0.8814, "r2_loocv": 0.8477, "n_segments": 30, "total_hid": 5676, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | CTV | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8471, "elasticity_active_days": 1.5231, "intercept": -4.4371, "r2_in_sample": 0.9593, "r2_loocv": 0.9172, "n_segments": 10, "total_hid": 971, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5723, "elasticity_active_days": 2.7145, "intercept": -2.7641, "r2_in_sample": 0.7458, "r2_loocv": 0.6793, "n_segments": 21, "total_hid": 5349, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Female | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.1147, "elasticity_active_days": 2.7567, "intercept": -0.6102, "r2_in_sample": 0.8588, "r2_loocv": 0.5961, "n_segments": 10, "total_hid": 1274, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.9398, "elasticity_active_days": 0.8326, "intercept": -6.3943, "r2_in_sample": 0.974, "r2_loocv": 0.9562, "n_segments": 13, "total_hid": 2936, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.952, "elasticity_active_days": 0.1579, "intercept": -0.8978, "r2_in_sample": 0.7751, "r2_loocv": 0.6805, "n_segments": 24, "total_hid": 4817, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5792, "elasticity_active_days": 0.9838, "intercept": -1.0241, "r2_in_sample": 0.5648, "r2_loocv": 0.3668, "n_segments": 20, "total_hid": 4016, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.8868, "elasticity_active_days": -4.9479, "intercept": -0.6392, "r2_in_sample": 0.829, "r2_loocv": 0.7379, "n_segments": 16, "total_hid": 3444, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.4881, "elasticity_active_days": 1.2898, "intercept": -5.6921, "r2_in_sample": 0.8822, "r2_loocv": 0.8147, "n_segments": 17, "total_hid": 4314, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2832, "elasticity_active_days": 1.3198, "intercept": -4.2163, "r2_in_sample": 0.653, "r2_loocv": 0.4874, "n_segments": 21, "total_hid": 5418, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.7493, "elasticity_active_days": 0.6856, "intercept": -5.9011, "r2_in_sample": 0.8495, "r2_loocv": 0.796, "n_segments": 15, "total_hid": 2732, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9398, "elasticity_active_days": -0.5696, "intercept": 1.1389, "r2_in_sample": 0.881, "r2_loocv": 0.8464, "n_segments": 29, "total_hid": 6167, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports Only | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8178, "elasticity_active_days": 1.3882, "intercept": -3.5592, "r2_in_sample": 0.8529, "r2_loocv": 0.8126, "n_segments": 28, "total_hid": 6462, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6813, "elasticity_active_days": 3.3307, "intercept": -7.8305, "r2_in_sample": 0.7703, "r2_loocv": 0.5066, "n_segments": 11, "total_hid": 4918, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8784, "elasticity_active_days": 1.342, "intercept": -2.2782, "r2_in_sample": 0.6724, "r2_loocv": 0.4736, "n_segments": 19, "total_hid": 4907, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Other | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.703, "elasticity_active_days": 0.4292, "intercept": -3.9535, "r2_in_sample": 0.8718, "r2_loocv": 0.7643, "n_segments": 13, "total_hid": 2443, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8781, "elasticity_active_days": 0.7027, "intercept": -1.2331, "r2_in_sample": 0.7775, "r2_loocv": 0.6635, "n_segments": 23, "total_hid": 4573, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.4681, "elasticity_active_days": 2.0272, "intercept": 3.2391, "r2_in_sample": 0.507, "r2_loocv": -0.1529, "n_segments": 11, "total_hid": 1922, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | CTV | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.5128, "elasticity_active_days": 1.3031, "intercept": -5.2392, "r2_in_sample": 0.5963, "r2_loocv": 0.3183, "n_segments": 14, "total_hid": 2276, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9112, "elasticity_active_days": 0.8317, "intercept": -1.5374, "r2_in_sample": 0.4462, "r2_loocv": -0.0507, "n_segments": 12, "total_hid": 2269, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8124, "elasticity_active_days": 0.5775, "intercept": -1.5256, "r2_in_sample": 0.6906, "r2_loocv": 0.5483, "n_segments": 20, "total_hid": 3584, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.496, "elasticity_active_days": 2.5114, "intercept": 2.0403, "r2_in_sample": 0.6955, "r2_loocv": 0.3709, "n_segments": 16, "total_hid": 2333, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Other | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6202, "elasticity_active_days": -3.1534, "intercept": 1.7913, "r2_in_sample": 0.784, "r2_loocv": 0.4294, "n_segments": 10, "total_hid": 951, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.5109, "elasticity_active_days": 4.0303, "intercept": -0.1191, "r2_in_sample": 0.6645, "r2_loocv": 0.2143, "n_segments": 10, "total_hid": 1481, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.0435, "elasticity_active_days": 1.0182, "intercept": -8.3193, "r2_in_sample": 0.6586, "r2_loocv": 0.3773, "n_segments": 11, "total_hid": 1737, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8789, "elasticity_active_days": 1.239, "intercept": -2.6157, "r2_in_sample": 0.8753, "r2_loocv": 0.6155, "n_segments": 13, "total_hid": 3764, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0557, "elasticity_active_days": 2.0764, "intercept": -5.4907, "r2_in_sample": 0.9283, "r2_loocv": 0.841, "n_segments": 10, "total_hid": 1198, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2508, "elasticity_active_days": 0.7609, "intercept": -3.2829, "r2_in_sample": 0.2772, "r2_loocv": -0.1747, "n_segments": 10, "total_hid": 1737, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False}
}

### PASTE BLOCK 4: ELASTICITY — MIDROLL ###
ELASTICITY_MIDROLL = {
"Ent Only | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.5075, "elasticity_active_days": 2.7212, "intercept": 1.5167, "r2_in_sample": 0.892, "r2_loocv": 0.8488, "n_segments": 37, "total_hid": 149518, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.899, "elasticity_active_days": 4.1323, "intercept": -0.0197, "r2_in_sample": 0.95, "r2_loocv": 0.9357, "n_segments": 40, "total_hid": 204893, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.3113, "elasticity_active_days": 1.8234, "intercept": -1.5993, "r2_in_sample": 0.944, "r2_loocv": 0.9212, "n_segments": 31, "total_hid": 72325, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.3504, "elasticity_active_days": 1.9517, "intercept": -2.2386, "r2_in_sample": 0.9406, "r2_loocv": 0.9152, "n_segments": 38, "total_hid": 81533, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.0777, "elasticity_active_days": 1.4199, "intercept": -6.4023, "r2_in_sample": 0.8845, "r2_loocv": 0.826, "n_segments": 46, "total_hid": 120772, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.4805, "elasticity_active_days": 2.4874, "intercept": -5.1828, "r2_in_sample": 0.9379, "r2_loocv": 0.9162, "n_segments": 36, "total_hid": 55861, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.8212, "elasticity_active_days": 3.6179, "intercept": 0.88, "r2_in_sample": 0.9374, "r2_loocv": 0.9213, "n_segments": 33, "total_hid": 84045, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4162, "elasticity_active_days": 1.6967, "intercept": -1.9267, "r2_in_sample": 0.9382, "r2_loocv": 0.6898, "n_segments": 8, "total_hid": 48818, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.2751, "elasticity_active_days": 1.6727, "intercept": -8.3629, "r2_in_sample": 0.8686, "r2_loocv": 0.8094, "n_segments": 42, "total_hid": 92313, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.1795, "elasticity_active_days": 4.8364, "intercept": -7.3031, "r2_in_sample": 0.9696, "r2_loocv": 0.9628, "n_segments": 35, "total_hid": 42845, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.1769, "elasticity_active_days": 1.9698, "intercept": -0.8692, "r2_in_sample": 0.9274, "r2_loocv": 0.8951, "n_segments": 32, "total_hid": 28186, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.1963, "elasticity_active_days": 1.9195, "intercept": 1.286, "r2_in_sample": 0.8369, "r2_loocv": 0.7793, "n_segments": 34, "total_hid": 102631, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.7924, "elasticity_active_days": 3.8962, "intercept": 0.0744, "r2_in_sample": 0.9548, "r2_loocv": 0.8525, "n_segments": 21, "total_hid": 27760, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9104, "elasticity_active_days": 1.0336, "intercept": -3.6398, "r2_in_sample": 0.945, "r2_loocv": 0.928, "n_segments": 35, "total_hid": 29099, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.2122, "elasticity_active_days": 0.5417, "intercept": -3.7792, "r2_in_sample": 0.8088, "r2_loocv": 0.771, "n_segments": 48, "total_hid": 146503, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -1.6882, "elasticity_active_days": 8.2562, "intercept": -6.3025, "r2_in_sample": 0.9466, "r2_loocv": 0.6754, "n_segments": 7, "total_hid": 21858, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6569, "elasticity_active_days": 1.6974, "intercept": -2.7939, "r2_in_sample": 0.9004, "r2_loocv": 0.8629, "n_segments": 38, "total_hid": 102405, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.228, "elasticity_active_days": 3.3373, "intercept": -5.8306, "r2_in_sample": 0.9148, "r2_loocv": 0.8809, "n_segments": 28, "total_hid": 16137, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.0148, "elasticity_active_days": 2.6641, "intercept": -1.3166, "r2_in_sample": 0.9619, "r2_loocv": 0.1919, "n_segments": 7, "total_hid": 19312, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.3577, "elasticity_active_days": -0.3165, "intercept": -2.1508, "r2_in_sample": 0.8847, "r2_loocv": 0.839, "n_segments": 48, "total_hid": 190254, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | CTV | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.9497, "elasticity_active_days": 6.4408, "intercept": -6.2361, "r2_in_sample": 0.9727, "r2_loocv": 0.9262, "n_segments": 7, "total_hid": 16736, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.2516, "elasticity_active_days": 0.526, "intercept": -2.8705, "r2_in_sample": 0.7105, "r2_loocv": 0.5716, "n_segments": 42, "total_hid": 100265, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.197, "elasticity_active_days": 3.8917, "intercept": -4.1284, "r2_in_sample": 0.9351, "r2_loocv": 0.9086, "n_segments": 24, "total_hid": 10703, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9089, "elasticity_active_days": 0.9617, "intercept": -3.3084, "r2_in_sample": 0.9459, "r2_loocv": 0.9262, "n_segments": 25, "total_hid": 11783, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.1748, "elasticity_active_days": 0.4269, "intercept": -3.0402, "r2_in_sample": 0.7651, "r2_loocv": 0.6945, "n_segments": 39, "total_hid": 43568, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.1859, "elasticity_active_days": 2.2289, "intercept": 0.6914, "r2_in_sample": 0.7443, "r2_loocv": 0.614, "n_segments": 20, "total_hid": 13591, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.4535, "elasticity_active_days": 0.9472, "intercept": -5.0235, "r2_in_sample": 0.9307, "r2_loocv": 0.8804, "n_segments": 27, "total_hid": 48067, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.3038, "elasticity_active_days": 3.5209, "intercept": -2.2571, "r2_in_sample": 0.9011, "r2_loocv": 0.87, "n_segments": 29, "total_hid": 18689, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.574, "elasticity_active_days": 2.6117, "intercept": -5.9947, "r2_in_sample": 0.9727, "r2_loocv": 0.9663, "n_segments": 25, "total_hid": 13147, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.3615, "elasticity_active_days": 4.3764, "intercept": -4.2831, "r2_in_sample": 0.9812, "r2_loocv": 0.9753, "n_segments": 23, "total_hid": 8666, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.2604, "elasticity_active_days": 2.7956, "intercept": -0.3848, "r2_in_sample": 0.9564, "r2_loocv": 0.8161, "n_segments": 15, "total_hid": 11196, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.176, "elasticity_active_days": 2.3834, "intercept": 0.0591, "r2_in_sample": 0.9243, "r2_loocv": 0.8928, "n_segments": 19, "total_hid": 13499, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.1288, "elasticity_active_days": 1.1457, "intercept": -4.1147, "r2_in_sample": 0.9403, "r2_loocv": 0.9176, "n_segments": 30, "total_hid": 43351, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.1838, "elasticity_active_days": 3.3036, "intercept": -2.5243, "r2_in_sample": 0.9423, "r2_loocv": 0.9278, "n_segments": 27, "total_hid": 16384, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2674, "elasticity_active_days": 0.485, "intercept": -4.9068, "r2_in_sample": 0.8923, "r2_loocv": 0.477, "n_segments": 12, "total_hid": 11076, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.2932, "elasticity_active_days": -0.3874, "intercept": -2.6817, "r2_in_sample": 0.7511, "r2_loocv": 0.6663, "n_segments": 42, "total_hid": 56787, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.2269, "elasticity_active_days": 0.1179, "intercept": -3.0953, "r2_in_sample": 0.8745, "r2_loocv": 0.8374, "n_segments": 36, "total_hid": 24941, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.4902, "elasticity_active_days": 1.7115, "intercept": -5.6433, "r2_in_sample": 0.9565, "r2_loocv": 0.9397, "n_segments": 34, "total_hid": 46039, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.684, "elasticity_active_days": 0.9182, "intercept": -5.497, "r2_in_sample": 0.9399, "r2_loocv": 0.9171, "n_segments": 45, "total_hid": 81554, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0915, "elasticity_active_days": 0.521, "intercept": -3.0585, "r2_in_sample": 0.7915, "r2_loocv": 0.6837, "n_segments": 20, "total_hid": 8802, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.7852, "elasticity_active_days": 3.6293, "intercept": -14.7871, "r2_in_sample": 0.8897, "r2_loocv": 0.8486, "n_segments": 49, "total_hid": 79586, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6147, "elasticity_active_days": 1.8658, "intercept": -2.6284, "r2_in_sample": 0.7893, "r2_loocv": -0.2689, "n_segments": 20, "total_hid": 18181, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.5104, "elasticity_active_days": 3.0606, "intercept": -3.9663, "r2_in_sample": 0.8097, "r2_loocv": 0.7692, "n_segments": 30, "total_hid": 20185, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.1091, "elasticity_active_days": 1.063, "intercept": -4.3519, "r2_in_sample": 0.8631, "r2_loocv": 0.8212, "n_segments": 34, "total_hid": 21491, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.388, "elasticity_active_days": -1.1775, "intercept": -0.8901, "r2_in_sample": 0.8901, "r2_loocv": 0.6204, "n_segments": 24, "total_hid": 57541, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4617, "elasticity_active_days": 4.0444, "intercept": -9.6408, "r2_in_sample": 0.9772, "r2_loocv": 0.9251, "n_segments": 7, "total_hid": 8443, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5799, "elasticity_active_days": 1.8026, "intercept": -3.1231, "r2_in_sample": 0.8984, "r2_loocv": 0.8314, "n_segments": 16, "total_hid": 5336, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.599, "elasticity_active_days": -4.1774, "intercept": 5.9293, "r2_in_sample": 0.8497, "r2_loocv": 0.7996, "n_segments": 45, "total_hid": 63748, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.727, "elasticity_active_days": 2.4736, "intercept": -4.74, "r2_in_sample": 0.9218, "r2_loocv": 0.6853, "n_segments": 7, "total_hid": 14929, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9299, "elasticity_active_days": 0.7188, "intercept": -3.3063, "r2_in_sample": 0.7574, "r2_loocv": 0.6083, "n_segments": 24, "total_hid": 8421, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.241, "elasticity_active_days": 1.9426, "intercept": -1.4513, "r2_in_sample": 0.908, "r2_loocv": 0.85, "n_segments": 16, "total_hid": 5102, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.0597, "elasticity_active_days": 2.5389, "intercept": -2.0638, "r2_in_sample": 0.8618, "r2_loocv": 0.7882, "n_segments": 18, "total_hid": 5564, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.2019, "elasticity_active_days": 2.5389, "intercept": -2.0638, "r2_in_sample": 0.8618, "r2_loocv": 0.7882, "n_segments": 18, "total_hid": 5600, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1687, "elasticity_active_days": -0.7728, "intercept": -0.2547, "r2_in_sample": 0.7477, "r2_loocv": 0.4312, "n_segments": 21, "total_hid": 15800, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7576, "elasticity_active_days": 3.9254, "intercept": -10.1811, "r2_in_sample": 0.9278, "r2_loocv": 0.8884, "n_segments": 20, "total_hid": 5977, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.2776, "elasticity_active_days": 1.928, "intercept": -6.0024, "r2_in_sample": 0.8882, "r2_loocv": 0.8315, "n_segments": 32, "total_hid": 21099, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1066, "elasticity_active_days": 1.306, "intercept": -3.2115, "r2_in_sample": 0.9906, "r2_loocv": 0.9722, "n_segments": 13, "total_hid": 7854, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5113, "elasticity_active_days": 4.5708, "intercept": -10.4507, "r2_in_sample": 0.9674, "r2_loocv": 0.9569, "n_segments": 22, "total_hid": 7357, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9994, "elasticity_active_days": 0.4526, "intercept": -2.4565, "r2_in_sample": 0.879, "r2_loocv": 0.8187, "n_segments": 18, "total_hid": 3409, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.08, "elasticity_active_days": 0.5382, "intercept": -1.0028, "r2_in_sample": 0.8983, "r2_loocv": 0.5771, "n_segments": 22, "total_hid": 25309, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.3085, "elasticity_active_days": 4.6319, "intercept": -5.8151, "r2_in_sample": 0.9255, "r2_loocv": 0.9006, "n_segments": 21, "total_hid": 5425, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9387, "elasticity_active_days": 3.7051, "intercept": -8.7765, "r2_in_sample": 0.9044, "r2_loocv": 0.8767, "n_segments": 24, "total_hid": 9010, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.755, "elasticity_active_days": 2.3064, "intercept": -4.222, "r2_in_sample": 0.9135, "r2_loocv": 0.8875, "n_segments": 17, "total_hid": 3522, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7813, "elasticity_active_days": 2.4354, "intercept": -4.6446, "r2_in_sample": 0.9495, "r2_loocv": 0.925, "n_segments": 24, "total_hid": 8331, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.8471, "elasticity_active_days": 1.111, "intercept": -6.7903, "r2_in_sample": 0.8753, "r2_loocv": 0.8284, "n_segments": 44, "total_hid": 52097, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2194, "elasticity_active_days": 0.4529, "intercept": -3.6678, "r2_in_sample": 0.9089, "r2_loocv": 0.8634, "n_segments": 22, "total_hid": 5239, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.0319, "elasticity_active_days": 0.2812, "intercept": -2.2282, "r2_in_sample": 0.8277, "r2_loocv": 0.7876, "n_segments": 30, "total_hid": 11602, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.1985, "elasticity_active_days": -1.5413, "intercept": -5.6981, "r2_in_sample": 0.9017, "r2_loocv": 0.8412, "n_segments": 17, "total_hid": 2487, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6983, "elasticity_active_days": 1.0343, "intercept": -6.7523, "r2_in_sample": 0.9128, "r2_loocv": 0.8671, "n_segments": 24, "total_hid": 13885, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.3904, "elasticity_active_days": 5.1791, "intercept": -7.1556, "r2_in_sample": 0.82, "r2_loocv": 0.7026, "n_segments": 21, "total_hid": 4283, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6141, "elasticity_active_days": 3.9288, "intercept": -10.1659, "r2_in_sample": 0.7985, "r2_loocv": 0.7498, "n_segments": 18, "total_hid": 4472, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7255, "elasticity_active_days": 4.2941, "intercept": -11.6324, "r2_in_sample": 0.8331, "r2_loocv": 0.7716, "n_segments": 18, "total_hid": 4245, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.5146, "elasticity_active_days": -0.5744, "intercept": -1.9474, "r2_in_sample": 0.8797, "r2_loocv": 0.8567, "n_segments": 40, "total_hid": 37545, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7329, "elasticity_active_days": 1.7173, "intercept": -3.086, "r2_in_sample": 0.8307, "r2_loocv": 0.7708, "n_segments": 26, "total_hid": 11210, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4347, "elasticity_active_days": 1.8809, "intercept": -2.462, "r2_in_sample": 0.9107, "r2_loocv": 0.8772, "n_segments": 17, "total_hid": 2437, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.5561, "elasticity_active_days": 2.4122, "intercept": -10.8542, "r2_in_sample": 0.9205, "r2_loocv": 0.8834, "n_segments": 31, "total_hid": 9852, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.8213, "elasticity_active_days": -1.2304, "intercept": -3.1492, "r2_in_sample": 0.8041, "r2_loocv": 0.7024, "n_segments": 16, "total_hid": 3934, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9525, "elasticity_active_days": 1.9512, "intercept": -3.9689, "r2_in_sample": 0.7414, "r2_loocv": 0.6583, "n_segments": 30, "total_hid": 13481, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.8844, "elasticity_active_days": -1.436, "intercept": -3.9519, "r2_in_sample": 0.9057, "r2_loocv": 0.8652, "n_segments": 18, "total_hid": 2415, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4749, "elasticity_active_days": 2.2287, "intercept": -2.5343, "r2_in_sample": 0.9367, "r2_loocv": 0.7012, "n_segments": 8, "total_hid": 9503, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6447, "elasticity_active_days": 3.4481, "intercept": -4.3425, "r2_in_sample": 0.8648, "r2_loocv": 0.5495, "n_segments": 8, "total_hid": 11900, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.4398, "elasticity_active_days": -3.0566, "intercept": 3.7301, "r2_in_sample": 0.8111, "r2_loocv": 0.7223, "n_segments": 27, "total_hid": 10022, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.1953, "elasticity_active_days": 2.8599, "intercept": -1.2133, "r2_in_sample": 0.6923, "r2_loocv": 0.3522, "n_segments": 19, "total_hid": 3249, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports Only | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.5307, "elasticity_active_days": 0.5591, "intercept": -6.1358, "r2_in_sample": 0.9291, "r2_loocv": 0.8998, "n_segments": 24, "total_hid": 4866, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.3987, "elasticity_active_days": -0.0977, "intercept": -3.2896, "r2_in_sample": 0.7855, "r2_loocv": 0.5784, "n_segments": 14, "total_hid": 6576, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8097, "elasticity_active_days": 1.6688, "intercept": -3.2022, "r2_in_sample": 0.8845, "r2_loocv": 0.8253, "n_segments": 21, "total_hid": 5919, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2493, "elasticity_active_days": 2.0954, "intercept": -6.7698, "r2_in_sample": 0.83, "r2_loocv": 0.6234, "n_segments": 15, "total_hid": 4149, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6091, "elasticity_active_days": 0.4118, "intercept": -5.8811, "r2_in_sample": 0.9265, "r2_loocv": 0.9015, "n_segments": 18, "total_hid": 2200, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.4618, "elasticity_active_days": 1.3276, "intercept": -7.4956, "r2_in_sample": 0.84, "r2_loocv": 0.7923, "n_segments": 20, "total_hid": 4300, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 2.0537, "elasticity_active_days": 1.1855, "intercept": -9.5685, "r2_in_sample": 0.9225, "r2_loocv": 0.8989, "n_segments": 30, "total_hid": 5676, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6397, "elasticity_active_days": 2.2045, "intercept": -5.1941, "r2_in_sample": 0.9442, "r2_loocv": 0.894, "n_segments": 10, "total_hid": 971, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7034, "elasticity_active_days": 2.6523, "intercept": -3.6202, "r2_in_sample": 0.7359, "r2_loocv": 0.6578, "n_segments": 21, "total_hid": 5349, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Female | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.5185, "elasticity_active_days": 3.4064, "intercept": 0.2498, "r2_in_sample": 0.812, "r2_loocv": 0.5135, "n_segments": 10, "total_hid": 1274, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.5483, "elasticity_active_days": 1.3729, "intercept": -6.4718, "r2_in_sample": 0.957, "r2_loocv": 0.926, "n_segments": 13, "total_hid": 2936, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.501, "elasticity_active_days": -1.5562, "intercept": -0.0805, "r2_in_sample": 0.8158, "r2_loocv": 0.7427, "n_segments": 24, "total_hid": 4817, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4152, "elasticity_active_days": 1.0474, "intercept": -0.5209, "r2_in_sample": 0.392, "r2_loocv": 0.0933, "n_segments": 20, "total_hid": 4016, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.3577, "elasticity_active_days": -3.4381, "intercept": -1.7586, "r2_in_sample": 0.7302, "r2_loocv": 0.572, "n_segments": 16, "total_hid": 3444, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.4206, "elasticity_active_days": 1.4655, "intercept": -5.9691, "r2_in_sample": 0.867, "r2_loocv": 0.7939, "n_segments": 17, "total_hid": 4314, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.5172, "elasticity_active_days": 1.1914, "intercept": -5.4461, "r2_in_sample": 0.6982, "r2_loocv": 0.5432, "n_segments": 21, "total_hid": 5418, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.8868, "elasticity_active_days": 0.5769, "intercept": -6.7133, "r2_in_sample": 0.8176, "r2_loocv": 0.747, "n_segments": 15, "total_hid": 2732, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.8586, "elasticity_active_days": -0.2035, "intercept": -3.9027, "r2_in_sample": 0.8901, "r2_loocv": 0.8517, "n_segments": 29, "total_hid": 6167, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports Only | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 2.1177, "elasticity_active_days": 1.7162, "intercept": -10.8566, "r2_in_sample": 0.8641, "r2_loocv": 0.7913, "n_segments": 27, "total_hid": 6412, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.8516, "elasticity_active_days": 1.1749, "intercept": -8.6937, "r2_in_sample": 0.861, "r2_loocv": 0.3819, "n_segments": 11, "total_hid": 4918, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0597, "elasticity_active_days": 0.8483, "intercept": -2.7682, "r2_in_sample": 0.6714, "r2_loocv": 0.443, "n_segments": 19, "total_hid": 4907, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Other | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6611, "elasticity_active_days": -0.3108, "intercept": -3.4322, "r2_in_sample": 0.7791, "r2_loocv": 0.5824, "n_segments": 13, "total_hid": 2443, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports Only | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.4678, "elasticity_active_days": 0.531, "intercept": -3.8642, "r2_in_sample": 0.9541, "r2_loocv": 0.9229, "n_segments": 23, "total_hid": 4573, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.3332, "elasticity_active_days": 1.7341, "intercept": 2.7566, "r2_in_sample": 0.4565, "r2_loocv": -0.2375, "n_segments": 11, "total_hid": 1922, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | CTV | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6222, "elasticity_active_days": 1.223, "intercept": -5.9431, "r2_in_sample": 0.6126, "r2_loocv": 0.3406, "n_segments": 14, "total_hid": 2276, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.783, "elasticity_active_days": 0.7899, "intercept": -1.1268, "r2_in_sample": 0.3949, "r2_loocv": -0.1424, "n_segments": 12, "total_hid": 2269, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6079, "elasticity_active_days": -4.4889, "intercept": 6.7267, "r2_in_sample": 0.8344, "r2_loocv": 0.729, "n_segments": 20, "total_hid": 3584, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | Web | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.2917, "elasticity_active_days": 2.1049, "intercept": 1.3809, "r2_in_sample": 0.601, "r2_loocv": 0.175, "n_segments": 16, "total_hid": 2333, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Other | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.5438, "elasticity_active_days": -4.154, "intercept": 3.2183, "r2_in_sample": 0.6839, "r2_loocv": 0.1764, "n_segments": 10, "total_hid": 951, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.8408, "elasticity_active_days": 4.5132, "intercept": 0.5968, "r2_in_sample": 0.5427, "r2_loocv": -0.066, "n_segments": 10, "total_hid": 1481, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.0159, "elasticity_active_days": 1.2021, "intercept": -8.9171, "r2_in_sample": 0.6946, "r2_loocv": 0.432, "n_segments": 11, "total_hid": 1737, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.4562, "elasticity_active_days": 5.8455, "intercept": -18.3426, "r2_in_sample": 0.8551, "r2_loocv": 0.4983, "n_segments": 13, "total_hid": 3764, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0204, "elasticity_active_days": 2.3351, "intercept": -6.1563, "r2_in_sample": 0.9286, "r2_loocv": 0.8474, "n_segments": 10, "total_hid": 1198, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2769, "elasticity_active_days": -0.0743, "intercept": -2.6594, "r2_in_sample": 0.274, "r2_loocv": -0.2044, "n_segments": 10, "total_hid": 1737, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True}
}


### PASTE BLOCK 5: ELASTICITY — PREROLL ###
ELASTICITY_PREROLL = {
"Ent Only | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.3272, "elasticity_active_days": 2.531, "intercept": -0.6275, "r2_in_sample": 0.9248, "r2_loocv": 0.8899, "n_segments": 37, "total_hid": 149518, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.0622, "elasticity_active_days": 2.7143, "intercept": -3.0712, "r2_in_sample": 0.9504, "r2_loocv": 0.9237, "n_segments": 40, "total_hid": 204893, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.5803, "elasticity_active_days": 1.473, "intercept": -3.895, "r2_in_sample": 0.9881, "r2_loocv": 0.9846, "n_segments": 31, "total_hid": 72325, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9643, "elasticity_active_days": 0.6483, "intercept": -4.6714, "r2_in_sample": 0.9402, "r2_loocv": 0.9168, "n_segments": 38, "total_hid": 81533, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6518, "elasticity_active_days": 2.601, "intercept": -8.1579, "r2_in_sample": 0.9567, "r2_loocv": 0.9403, "n_segments": 46, "total_hid": 120772, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.3379, "elasticity_active_days": -0.2022, "intercept": -4.9957, "r2_in_sample": 0.9451, "r2_loocv": 0.9269, "n_segments": 36, "total_hid": 55861, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.4317, "elasticity_active_days": 1.9118, "intercept": -4.0839, "r2_in_sample": 0.9867, "r2_loocv": 0.9838, "n_segments": 33, "total_hid": 84045, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.7049, "elasticity_active_days": 3.703, "intercept": -1.0799, "r2_in_sample": 0.9281, "r2_loocv": 0.6241, "n_segments": 8, "total_hid": 48818, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8589, "elasticity_active_days": 2.8158, "intercept": -10.0639, "r2_in_sample": 0.9839, "r2_loocv": 0.98, "n_segments": 42, "total_hid": 92313, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.2392, "elasticity_active_days": 0.383, "intercept": -5.9998, "r2_in_sample": 0.9696, "r2_loocv": 0.9616, "n_segments": 35, "total_hid": 42845, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6118, "elasticity_active_days": 1.2134, "intercept": -3.6692, "r2_in_sample": 0.9305, "r2_loocv": 0.9014, "n_segments": 32, "total_hid": 28186, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.0606, "elasticity_active_days": 1.8412, "intercept": -1.0777, "r2_in_sample": 0.9012, "r2_loocv": 0.869, "n_segments": 34, "total_hid": 102631, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.342, "elasticity_active_days": 3.1691, "intercept": -2.3405, "r2_in_sample": 0.9514, "r2_loocv": 0.6748, "n_segments": 21, "total_hid": 27760, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.291, "elasticity_active_days": 0.2268, "intercept": -5.8424, "r2_in_sample": 0.9656, "r2_loocv": 0.958, "n_segments": 35, "total_hid": 29099, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8242, "elasticity_active_days": 1.8238, "intercept": -5.4514, "r2_in_sample": 0.7937, "r2_loocv": 0.7593, "n_segments": 48, "total_hid": 146503, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.5376, "elasticity_active_days": -3.5343, "intercept": -3.921, "r2_in_sample": 0.9453, "r2_loocv": 0.4998, "n_segments": 7, "total_hid": 21858, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.675, "elasticity_active_days": 1.8504, "intercept": -4.2355, "r2_in_sample": 0.9255, "r2_loocv": 0.9114, "n_segments": 38, "total_hid": 102405, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6824, "elasticity_active_days": 2.1786, "intercept": -6.9217, "r2_in_sample": 0.9512, "r2_loocv": 0.929, "n_segments": 28, "total_hid": 16137, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.1891, "elasticity_active_days": 2.7455, "intercept": -2.0822, "r2_in_sample": 0.9575, "r2_loocv": 0.5872, "n_segments": 7, "total_hid": 19312, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.8166, "elasticity_active_days": 2.8511, "intercept": -5.9124, "r2_in_sample": 0.7595, "r2_loocv": 0.6909, "n_segments": 48, "total_hid": 190254, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0981, "elasticity_active_days": 0.7097, "intercept": -5.9144, "r2_in_sample": 0.9643, "r2_loocv": 0.4855, "n_segments": 7, "total_hid": 16736, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.82, "elasticity_active_days": 1.7687, "intercept": -4.0196, "r2_in_sample": 0.7288, "r2_loocv": 0.5998, "n_segments": 42, "total_hid": 100265, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5014, "elasticity_active_days": 2.0712, "intercept": -5.5932, "r2_in_sample": 0.9349, "r2_loocv": 0.9076, "n_segments": 24, "total_hid": 10703, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.5619, "elasticity_active_days": 1.4632, "intercept": -4.0025, "r2_in_sample": 0.9606, "r2_loocv": 0.95, "n_segments": 25, "total_hid": 11783, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9416, "elasticity_active_days": 1.1097, "intercept": -4.3991, "r2_in_sample": 0.8197, "r2_loocv": 0.7315, "n_segments": 39, "total_hid": 43568, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.0302, "elasticity_active_days": 2.2094, "intercept": -1.6871, "r2_in_sample": 0.839, "r2_loocv": 0.7334, "n_segments": 20, "total_hid": 13591, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6894, "elasticity_active_days": 1.3398, "intercept": -3.1957, "r2_in_sample": 0.9385, "r2_loocv": 0.9077, "n_segments": 27, "total_hid": 48067, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.0604, "elasticity_active_days": 2.9947, "intercept": -4.4917, "r2_in_sample": 0.9146, "r2_loocv": 0.8753, "n_segments": 29, "total_hid": 18689, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.0016, "elasticity_active_days": 1.495, "intercept": -7.0811, "r2_in_sample": 0.9926, "r2_loocv": 0.9896, "n_segments": 25, "total_hid": 13147, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6036, "elasticity_active_days": 1.9282, "intercept": -5.9268, "r2_in_sample": 0.9709, "r2_loocv": 0.9609, "n_segments": 23, "total_hid": 8666, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4578, "elasticity_active_days": 1.7439, "intercept": -3.7572, "r2_in_sample": 0.9911, "r2_loocv": 0.9859, "n_segments": 15, "total_hid": 11196, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.0292, "elasticity_active_days": 2.2958, "intercept": -2.0103, "r2_in_sample": 0.9398, "r2_loocv": 0.9126, "n_segments": 19, "total_hid": 13499, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9468, "elasticity_active_days": 1.3334, "intercept": -4.4964, "r2_in_sample": 0.9384, "r2_loocv": 0.9177, "n_segments": 30, "total_hid": 43351, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.1793, "elasticity_active_days": 2.7944, "intercept": -4.6958, "r2_in_sample": 0.9666, "r2_loocv": 0.9539, "n_segments": 27, "total_hid": 16384, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6565, "elasticity_active_days": 2.1414, "intercept": -6.8295, "r2_in_sample": 0.9534, "r2_loocv": 0.8333, "n_segments": 12, "total_hid": 11076, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7031, "elasticity_active_days": 2.3093, "intercept": -5.4217, "r2_in_sample": 0.7123, "r2_loocv": 0.63, "n_segments": 42, "total_hid": 56787, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7983, "elasticity_active_days": 1.8819, "intercept": -5.9472, "r2_in_sample": 0.9017, "r2_loocv": 0.8685, "n_segments": 36, "total_hid": 24941, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7961, "elasticity_active_days": 2.3135, "intercept": -4.6149, "r2_in_sample": 0.8545, "r2_loocv": 0.8164, "n_segments": 34, "total_hid": 46039, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.9384, "elasticity_active_days": 2.2314, "intercept": -5.3211, "r2_in_sample": 0.6927, "r2_loocv": 0.5794, "n_segments": 45, "total_hid": 81554, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0829, "elasticity_active_days": 0.6871, "intercept": -4.7972, "r2_in_sample": 0.8627, "r2_loocv": 0.7835, "n_segments": 20, "total_hid": 8802, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.5975, "elasticity_active_days": 3.6905, "intercept": -10.343, "r2_in_sample": 0.8287, "r2_loocv": 0.7952, "n_segments": 49, "total_hid": 79586, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.0248, "elasticity_active_days": 2.7435, "intercept": -2.5544, "r2_in_sample": 0.7921, "r2_loocv": -0.0299, "n_segments": 20, "total_hid": 18181, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.1701, "elasticity_active_days": 3.7169, "intercept": -4.6155, "r2_in_sample": 0.8668, "r2_loocv": 0.8363, "n_segments": 30, "total_hid": 20185, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.3973, "elasticity_active_days": 2.8865, "intercept": -5.5074, "r2_in_sample": 0.885, "r2_loocv": 0.8449, "n_segments": 34, "total_hid": 21491, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1313, "elasticity_active_days": -0.9615, "intercept": -1.348, "r2_in_sample": 0.7358, "r2_loocv": 0.1305, "n_segments": 24, "total_hid": 57541, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0353, "elasticity_active_days": 1.9061, "intercept": -8.6002, "r2_in_sample": 0.987, "r2_loocv": 0.9368, "n_segments": 7, "total_hid": 8443, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Female | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7651, "elasticity_active_days": 1.6322, "intercept": -5.2604, "r2_in_sample": 0.9751, "r2_loocv": 0.9563, "n_segments": 16, "total_hid": 5336, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Active (SVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.5424, "elasticity_active_days": 0.3279, "intercept": -1.5519, "r2_in_sample": 0.5932, "r2_loocv": 0.4854, "n_segments": 45, "total_hid": 63748, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Unknown | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.4109, "elasticity_active_days": 5.2037, "intercept": -5.0105, "r2_in_sample": 0.9725, "r2_loocv": 0.9013, "n_segments": 7, "total_hid": 14929, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.1164, "elasticity_active_days": -1.3985, "intercept": -7.1135, "r2_in_sample": 0.894, "r2_loocv": 0.8488, "n_segments": 24, "total_hid": 8421, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | Mobile | Female | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7605, "elasticity_active_days": 1.4292, "intercept": -4.7839, "r2_in_sample": 0.9672, "r2_loocv": 0.9514, "n_segments": 16, "total_hid": 5102, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7291, "elasticity_active_days": 1.9518, "intercept": -5.8864, "r2_in_sample": 0.9754, "r2_loocv": 0.9641, "n_segments": 18, "total_hid": 5564, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5823, "elasticity_active_days": 1.8156, "intercept": -4.6828, "r2_in_sample": 0.9883, "r2_loocv": 0.9844, "n_segments": 18, "total_hid": 5600, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.976, "elasticity_active_days": -0.0199, "intercept": -2.5264, "r2_in_sample": 0.706, "r2_loocv": 0.2111, "n_segments": 21, "total_hid": 15800, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9055, "elasticity_active_days": 2.9704, "intercept": -10.3644, "r2_in_sample": 0.9176, "r2_loocv": 0.8742, "n_segments": 20, "total_hid": 5977, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 1.1875, "elasticity_active_days": 1.883, "intercept": -7.2464, "r2_in_sample": 0.7704, "r2_loocv": 0.6575, "n_segments": 32, "total_hid": 21099, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Mobile | Unknown | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.3397, "elasticity_active_days": 1.2339, "intercept": -6.1146, "r2_in_sample": 0.9662, "r2_loocv": 0.8868, "n_segments": 13, "total_hid": 7854, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6541, "elasticity_active_days": 3.6788, "intercept": -10.7204, "r2_in_sample": 0.9597, "r2_loocv": 0.9414, "n_segments": 22, "total_hid": 7357, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1178, "elasticity_active_days": 0.183, "intercept": -4.2894, "r2_in_sample": 0.8738, "r2_loocv": 0.78, "n_segments": 18, "total_hid": 3409, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9373, "elasticity_active_days": 0.6921, "intercept": -2.3356, "r2_in_sample": 0.7536, "r2_loocv": -0.0698, "n_segments": 22, "total_hid": 25309, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0628, "elasticity_active_days": 0.6285, "intercept": -5.4176, "r2_in_sample": 0.9388, "r2_loocv": 0.9184, "n_segments": 21, "total_hid": 5425, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8921, "elasticity_active_days": 3.1826, "intercept": -9.2441, "r2_in_sample": 0.9177, "r2_loocv": 0.8936, "n_segments": 24, "total_hid": 9010, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.756, "elasticity_active_days": 2.3357, "intercept": -6.4037, "r2_in_sample": 0.9366, "r2_loocv": 0.906, "n_segments": 17, "total_hid": 3522, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6452, "elasticity_active_days": 2.2913, "intercept": -5.5608, "r2_in_sample": 0.888, "r2_loocv": 0.7315, "n_segments": 24, "total_hid": 8331, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6141, "elasticity_active_days": 3.0186, "intercept": -7.1659, "r2_in_sample": 0.7513, "r2_loocv": 0.6725, "n_segments": 45, "total_hid": 52157, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.901, "elasticity_active_days": 1.2896, "intercept": -5.1713, "r2_in_sample": 0.9089, "r2_loocv": 0.8589, "n_segments": 22, "total_hid": 5239, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6608, "elasticity_active_days": 2.4172, "intercept": -5.9271, "r2_in_sample": 0.7618, "r2_loocv": 0.6985, "n_segments": 31, "total_hid": 11670, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.1102, "elasticity_active_days": -1.4987, "intercept": -6.8648, "r2_in_sample": 0.8964, "r2_loocv": 0.8337, "n_segments": 17, "total_hid": 2487, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.8018, "elasticity_active_days": 0.2457, "intercept": -6.355, "r2_in_sample": 0.7935, "r2_loocv": 0.6129, "n_segments": 24, "total_hid": 13885, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.6985, "elasticity_active_days": 2.1116, "intercept": -7.046, "r2_in_sample": 0.9343, "r2_loocv": 0.8968, "n_segments": 21, "total_hid": 4283, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1218, "elasticity_active_days": 2.1182, "intercept": -9.3666, "r2_in_sample": 0.923, "r2_loocv": 0.9027, "n_segments": 18, "total_hid": 4472, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.3775, "elasticity_active_days": 2.5808, "intercept": -11.9591, "r2_in_sample": 0.9369, "r2_loocv": 0.9146, "n_segments": 18, "total_hid": 4245, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.3457, "elasticity_active_days": -0.251, "intercept": 0.5937, "r2_in_sample": 0.3545, "r2_loocv": 0.1012, "n_segments": 40, "total_hid": 37545, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": -0.0177, "elasticity_active_days": 2.671, "intercept": -2.4033, "r2_in_sample": 0.712, "r2_loocv": 0.6215, "n_segments": 26, "total_hid": 11210, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | CTV | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.4427, "elasticity_active_days": -0.0147, "intercept": -6.0234, "r2_in_sample": 0.9474, "r2_loocv": 0.9239, "n_segments": 17, "total_hid": 2437, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports Only | Mobile | Male | Newly Acquired | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6448, "elasticity_active_days": 3.2165, "intercept": -9.3967, "r2_in_sample": 0.8587, "r2_loocv": 0.8073, "n_segments": 31, "total_hid": 9852, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Female | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.368, "elasticity_active_days": 0.1836, "intercept": -4.844, "r2_in_sample": 0.8361, "r2_loocv": 0.7017, "n_segments": 16, "total_hid": 3934, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.0035, "elasticity_active_days": 3.2278, "intercept": -2.802, "r2_in_sample": 0.5602, "r2_loocv": 0.4285, "n_segments": 30, "total_hid": 13481, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Newly Acquired | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.7287, "elasticity_active_days": -1.0209, "intercept": -5.5274, "r2_in_sample": 0.9643, "r2_loocv": 0.9389, "n_segments": 18, "total_hid": 2415, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.7206, "elasticity_active_days": 3.7163, "intercept": -0.4943, "r2_in_sample": 0.9108, "r2_loocv": 0.7989, "n_segments": 8, "total_hid": 9503, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | CTV | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.462, "elasticity_active_days": 5.2634, "intercept": -3.0629, "r2_in_sample": 0.7668, "r2_loocv": 0.3678, "n_segments": 8, "total_hid": 11900, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Newly Acquired | Mixed": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.5388, "elasticity_active_days": 1.0685, "intercept": -3.3222, "r2_in_sample": 0.6383, "r2_loocv": 0.5074, "n_segments": 27, "total_hid": 10022, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9285, "elasticity_active_days": 0.7178, "intercept": -4.5289, "r2_in_sample": 0.9029, "r2_loocv": 0.8228, "n_segments": 19, "total_hid": 3249, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | CTV | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9158, "elasticity_active_days": 1.8538, "intercept": -7.4147, "r2_in_sample": 0.8723, "r2_loocv": 0.796, "n_segments": 24, "total_hid": 4866, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Unknown | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.872, "elasticity_active_days": 1.3372, "intercept": -4.0876, "r2_in_sample": 0.7236, "r2_loocv": -0.1153, "n_segments": 14, "total_hid": 6576, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.3434, "elasticity_active_days": 2.5642, "intercept": -3.9735, "r2_in_sample": 0.8885, "r2_loocv": 0.8528, "n_segments": 21, "total_hid": 5919, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.8509, "elasticity_active_days": 1.4483, "intercept": -9.3358, "r2_in_sample": 0.9348, "r2_loocv": 0.8895, "n_segments": 15, "total_hid": 4149, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1999, "elasticity_active_days": 0.8487, "intercept": -6.1093, "r2_in_sample": 0.9336, "r2_loocv": 0.9051, "n_segments": 18, "total_hid": 2200, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | CTV | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.4552, "elasticity_active_days": 0.1667, "intercept": -6.2776, "r2_in_sample": 0.904, "r2_loocv": 0.8676, "n_segments": 20, "total_hid": 4300, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Active (SVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.6579, "elasticity_active_days": -0.0488, "intercept": -0.9298, "r2_in_sample": 0.7666, "r2_loocv": 0.6873, "n_segments": 30, "total_hid": 5676, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports & Ent | CTV | Male | Churned | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.1549, "elasticity_active_days": 0.6949, "intercept": -6.1067, "r2_in_sample": 0.9742, "r2_loocv": 0.9406, "n_segments": 10, "total_hid": 971, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -0.3417, "elasticity_active_days": 4.5074, "intercept": -2.7824, "r2_in_sample": 0.7142, "r2_loocv": 0.6538, "n_segments": 21, "total_hid": 5349, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Ent Only | Web | Female | Active (SVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.9298, "elasticity_active_days": 0.7966, "intercept": -4.5505, "r2_in_sample": 0.8596, "r2_loocv": 0.484, "n_segments": 10, "total_hid": 1274, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.1684, "elasticity_active_days": 0.2224, "intercept": -8.073, "r2_in_sample": 0.9303, "r2_loocv": 0.8802, "n_segments": 13, "total_hid": 2936, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.8152, "elasticity_active_days": -0.1297, "intercept": -1.5483, "r2_in_sample": 0.7197, "r2_loocv": 0.5856, "n_segments": 24, "total_hid": 4817, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | Web | Male | Active (SVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.0935, "elasticity_active_days": 0.5892, "intercept": -4.7824, "r2_in_sample": 0.8583, "r2_loocv": 0.8177, "n_segments": 20, "total_hid": 4016, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.5379, "elasticity_active_days": -3.2073, "intercept": -4.1328, "r2_in_sample": 0.8695, "r2_loocv": 0.8053, "n_segments": 16, "total_hid": 3444, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.076, "elasticity_active_days": 1.6333, "intercept": -11.0974, "r2_in_sample": 0.8911, "r2_loocv": 0.8319, "n_segments": 17, "total_hid": 4314, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.723, "elasticity_active_days": 2.4699, "intercept": -5.0512, "r2_in_sample": 0.418, "r2_loocv": 0.1386, "n_segments": 21, "total_hid": 5418, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Ent Only | CTV | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.0869, "elasticity_active_days": 1.0318, "intercept": -10.1968, "r2_in_sample": 0.8821, "r2_loocv": 0.8417, "n_segments": 15, "total_hid": 2732, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.7054, "elasticity_active_days": -0.3784, "intercept": -0.147, "r2_in_sample": 0.7437, "r2_loocv": 0.66, "n_segments": 29, "total_hid": 6167, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Sports Only | Mobile | Male | Churned | Ent": {"effective_tier": "High", "confidence_tier": "High", "elasticity_wt_per_vv": 0.5946, "elasticity_active_days": 2.1839, "intercept": -6.3072, "r2_in_sample": 0.7609, "r2_loocv": 0.6931, "n_segments": 28, "total_hid": 6462, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Unknown | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5326, "elasticity_active_days": 2.2682, "intercept": -6.3046, "r2_in_sample": 0.6757, "r2_loocv": 0.3823, "n_segments": 11, "total_hid": 4918, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4828, "elasticity_active_days": 2.4116, "intercept": -3.3482, "r2_in_sample": 0.6147, "r2_loocv": 0.483, "n_segments": 19, "total_hid": 4907, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Mobile | Other | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.4587, "elasticity_active_days": 0.6068, "intercept": -4.9746, "r2_in_sample": 0.8428, "r2_loocv": 0.6875, "n_segments": 13, "total_hid": 2443, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.4533, "elasticity_active_days": -0.4039, "intercept": 0.7168, "r2_in_sample": 0.4882, "r2_loocv": 0.2304, "n_segments": 23, "total_hid": 4573, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | Web | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": -1.0824, "elasticity_active_days": 2.8055, "intercept": 3.4565, "r2_in_sample": 0.5388, "r2_loocv": -0.123, "n_segments": 11, "total_hid": 1922, "overfit_flag": True, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | CTV | Female | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.3988, "elasticity_active_days": 1.9638, "intercept": -7.5791, "r2_in_sample": 0.6062, "r2_loocv": 0.3662, "n_segments": 14, "total_hid": 2276, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Female | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.978, "elasticity_active_days": 1.2245, "intercept": -3.9919, "r2_in_sample": 0.5174, "r2_loocv": 0.0586, "n_segments": 12, "total_hid": 2269, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Male | Churned | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.7016, "elasticity_active_days": -0.2819, "intercept": -0.6998, "r2_in_sample": 0.6684, "r2_loocv": 0.5115, "n_segments": 20, "total_hid": 3584, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Ent Only | Web | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": -1.2346, "elasticity_active_days": 3.5915, "intercept": 2.4271, "r2_in_sample": 0.8068, "r2_loocv": 0.6176, "n_segments": 16, "total_hid": 2333, "overfit_flag": False, "neg_wtvv_warning": True, "neg_ad_warning": False},
"Fringe | Mobile | Other | Active (SVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.6142, "elasticity_active_days": -3.1357, "intercept": -0.1747, "r2_in_sample": 0.8357, "r2_loocv": 0.5971, "n_segments": 10, "total_hid": 951, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": True},
"Fringe | Web | Male | Active (SVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.2418, "elasticity_active_days": 2.9055, "intercept": -3.9445, "r2_in_sample": 0.8532, "r2_loocv": 0.6945, "n_segments": 10, "total_hid": 1481, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 2.7372, "elasticity_active_days": 1.1905, "intercept": -13.8323, "r2_in_sample": 0.7104, "r2_loocv": 0.487, "n_segments": 11, "total_hid": 1737, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports Only | Mobile | Unknown | Non Subscriber (AVOD) | Ent": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 0.5866, "elasticity_active_days": 0.9274, "intercept": -2.6292, "r2_in_sample": 0.7342, "r2_loocv": 0.1547, "n_segments": 13, "total_hid": 3764, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Sports & Ent | CTV | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Medium", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.2879, "elasticity_active_days": 2.0133, "intercept": -8.3128, "r2_in_sample": 0.8314, "r2_loocv": 0.7106, "n_segments": 10, "total_hid": 1198, "overfit_flag": False, "neg_wtvv_warning": False, "neg_ad_warning": False},
"Fringe | Web | Male | Non Subscriber (AVOD) | Mixed": {"effective_tier": "Low", "confidence_tier": "Medium", "elasticity_wt_per_vv": 1.388, "elasticity_active_days": 1.813, "intercept": -6.7006, "r2_in_sample": 0.2885, "r2_loocv": -0.0899, "n_segments": 10, "total_hid": 1737, "overfit_flag": True, "neg_wtvv_warning": False, "neg_ad_warning": False}
}




STR_LOOKUP = {"Mobile|network fiction gec|Ent|Ent Only|singledevice":{"baseline_str":0.3421,"str_p25":0.2613,"str_p50":0.4111,"str_p75":0.5782,"preroll_str":0.5885,"midroll_str":0.5039,"midroll_share":0.5243,"hid_count":76416,"wt_per_vv":968.8,"avg_active_days":18.11,"confidence":"High"},"Mobile|network fiction gec|Ent|Ent Only|hotstarmobile":{"baseline_str":0.3409,"str_p25":0.2626,"str_p50":0.4124,"str_p75":0.5815,"preroll_str":0.5994,"midroll_str":0.5134,"midroll_share":0.5174,"hid_count":51831,"wt_per_vv":1212.7,"avg_active_days":20.92,"confidence":"High"},"Mobile|network non fiction gec|Ent|Ent Only|singledevice":{"baseline_str":0.3809,"str_p25":0.2822,"str_p50":0.46,"str_p75":0.618,"preroll_str":0.5773,"midroll_str":0.6102,"midroll_share":0.4975,"hid_count":81653,"wt_per_vv":1189.6,"avg_active_days":18.0,"confidence":"High"},"Mobile|network non fiction gec|Ent|Ent Only|hotstarmobile":{"baseline_str":0.3751,"str_p25":0.2727,"str_p50":0.4621,"str_p75":0.6245,"preroll_str":0.5783,"midroll_str":0.6419,"midroll_share":0.4713,"hid_count":50485,"wt_per_vv":1442.2,"avg_active_days":20.14,"confidence":"High"},"Mobile|network fiction gec|Mixed|Ent Only|singledevice":{"baseline_str":0.422,"str_p25":0.3409,"str_p50":0.5277,"str_p75":0.7009,"preroll_str":0.7257,"midroll_str":0.6469,"midroll_share":0.5044,"hid_count":35478,"wt_per_vv":1019.9,"avg_active_days":18.29,"confidence":"High"},"Mobile|network fiction gec|Ent|Ent Only|free":{"baseline_str":0.3419,"str_p25":0.2343,"str_p50":0.375,"str_p75":0.5556,"preroll_str":0.5542,"midroll_str":0.528,"midroll_share":0.4907,"hid_count":113340,"wt_per_vv":193.1,"avg_active_days":9.53,"confidence":"High"},"Mobile|network fiction gec|Mixed|Ent Only|hotstarmobile":{"baseline_str":0.424,"str_p25":0.3371,"str_p50":0.5267,"str_p75":0.7019,"preroll_str":0.7251,"midroll_str":0.6629,"midroll_share":0.5033,"hid_count":23829,"wt_per_vv":1245.7,"avg_active_days":21.01,"confidence":"High"},"CTV|network fiction gec|Ent|Ent Only|hotstarbundle":{"baseline_str":0.5022,"str_p25":0.4223,"str_p50":0.5642,"str_p75":0.7149,"preroll_str":0.6838,"midroll_str":0.5165,"midroll_share":0.7917,"hid_count":17002,"wt_per_vv":2366.0,"avg_active_days":21.97,"confidence":"High"},"CTV|network fiction gec|Ent|Ent Only|hotstarsuper":{"baseline_str":0.5189,"str_p25":0.4255,"str_p50":0.5768,"str_p75":0.7211,"preroll_str":0.7021,"midroll_str":0.5327,"midroll_share":0.7897,"hid_count":15402,"wt_per_vv":2506.4,"avg_active_days":22.78,"confidence":"High"},"CTV|network fiction gec|Ent|Sports & Ent|hotstarbundle":{"baseline_str":0.5152,"str_p25":0.433,"str_p50":0.5791,"str_p75":0.7394,"preroll_str":0.7167,"midroll_str":0.5344,"midroll_share":0.7734,"hid_count":13108,"wt_per_vv":2727.0,"avg_active_days":24.29,"confidence":"High"},"CTV|network fiction gec|Mixed|Sports & Ent|hotstarbundle":{"baseline_str":0.5739,"str_p25":0.4926,"str_p50":0.6485,"str_p75":0.7933,"preroll_str":0.7681,"midroll_str":0.5969,"midroll_share":0.7972,"hid_count":11599,"wt_per_vv":2565.6,"avg_active_days":24.6,"confidence":"High"},"CTV|network fiction gec|Ent|Ent Only|singledevice":{"baseline_str":0.4968,"str_p25":0.3993,"str_p50":0.5533,"str_p75":0.7143,"preroll_str":0.7034,"midroll_str":0.5021,"midroll_share":0.7979,"hid_count":13517,"wt_per_vv":2000.9,"avg_active_days":19.84,"confidence":"High"},"Mobile|network non fiction gec|Ent|Sports & Ent|singledevice":{"baseline_str":0.3696,"str_p25":0.2911,"str_p50":0.4948,"str_p75":0.6796,"preroll_str":0.6567,"midroll_str":0.6158,"midroll_share":0.4406,"hid_count":26379,"wt_per_vv":1133.2,"avg_active_days":20.12,"confidence":"High"},"Mobile|network non fiction gec|Ent|Ent Only|free":{"baseline_str":0.3678,"str_p25":0.25,"str_p50":0.4386,"str_p75":0.6364,"preroll_str":0.57,"midroll_str":0.644,"midroll_share":0.4416,"hid_count":82506,"wt_per_vv":204.0,"avg_active_days":7.86,"confidence":"High"},"Mobile|network non fiction gec|Mixed|Ent Only|singledevice":{"baseline_str":0.4185,"str_p25":0.3273,"str_p50":0.5316,"str_p75":0.7045,"preroll_str":0.7472,"midroll_str":0.7209,"midroll_share":0.4375,"hid_count":33461,"wt_per_vv":758.2,"avg_active_days":13.18,"confidence":"High"},"Mobile|network fiction gec|Mixed|Ent Only|free":{"baseline_str":0.4092,"str_p25":0.2976,"str_p50":0.4643,"str_p75":0.6772,"preroll_str":0.707,"midroll_str":0.6512,"midroll_share":0.4701,"hid_count":51576,"wt_per_vv":190.6,"avg_active_days":9.13,"confidence":"High"},"Mobile|network fiction gec|Ent|Ent Only|hotstarsuper":{"baseline_str":0.3584,"str_p25":0.2736,"str_p50":0.4262,"str_p75":0.5941,"preroll_str":0.6106,"midroll_str":0.5242,"midroll_share":0.5347,"hid_count":9630,"wt_per_vv":1381.1,"avg_active_days":21.5,"confidence":"High"},"CTV|network non fiction gec|Ent|Ent Only|hotstarsuper":{"baseline_str":0.6126,"str_p25":0.5245,"str_p50":0.6667,"str_p75":0.7895,"preroll_str":0.7605,"midroll_str":0.6845,"midroll_share":0.7344,"hid_count":14431,"wt_per_vv":2368.9,"avg_active_days":21.91,"confidence":"High"},"Mobile|network fiction gec|Ent|Fringe|free":{"baseline_str":0.33,"str_p25":0.2308,"str_p50":0.3889,"str_p75":0.6,"preroll_str":0.5862,"midroll_str":0.4579,"midroll_share":0.5217,"hid_count":85533,"wt_per_vv":101.5,"avg_active_days":4.78,"confidence":"High"},"CTV|network fiction gec|Ent|Sports & Ent|hotstarsuper":{"baseline_str":0.5428,"str_p25":0.4566,"str_p50":0.6129,"str_p75":0.7531,"preroll_str":0.7358,"midroll_str":0.5557,"midroll_share":0.7831,"hid_count":8027,"wt_per_vv":2709.9,"avg_active_days":24.42,"confidence":"High"},"CTV|network non fiction gec|Ent|Ent Only|hotstarbundle":{"baseline_str":0.608,"str_p25":0.5433,"str_p50":0.6709,"str_p75":0.8008,"preroll_str":0.7409,"midroll_str":0.6742,"midroll_share":0.7485,"hid_count":13541,"wt_per_vv":2202.1,"avg_active_days":20.64,"confidence":"High"},"Mobile|network non fiction gec|Mixed|Ent Only|hotstarmobile":{"baseline_str":0.4148,"str_p25":0.328,"str_p50":0.5457,"str_p75":0.7159,"preroll_str":0.7626,"midroll_str":0.7467,"midroll_share":0.4261,"hid_count":20394,"wt_per_vv":950.5,"avg_active_days":15.12,"confidence":"High"},"CTV|network fiction gec|Mixed|Ent Only|hotstarbundle":{"baseline_str":0.5517,"str_p25":0.4737,"str_p50":0.6267,"str_p75":0.7705,"preroll_str":0.7178,"midroll_str":0.5673,"midroll_share":0.8135,"hid_count":7760,"wt_per_vv":2232.3,"avg_active_days":21.55,"confidence":"High"},"Mobile|network fiction gec|Ent|Sports & Ent|singledevice":{"baseline_str":0.3547,"str_p25":0.2878,"str_p50":0.4613,"str_p75":0.649,"preroll_str":0.6692,"midroll_str":0.5102,"midroll_share":0.5067,"hid_count":13860,"wt_per_vv":923.5,"avg_active_days":20.08,"confidence":"High"},"Mobile|network non fiction gec|Ent|Fringe|free":{"baseline_str":0.3879,"str_p25":0.2695,"str_p50":0.4932,"str_p75":0.7241,"preroll_str":0.646,"midroll_str":0.6496,"midroll_share":0.4467,"hid_count":119335,"wt_per_vv":104.8,"avg_active_days":5.17,"confidence":"High"},"CTV|network fiction gec|Mixed|Sports & Ent|hotstarsuper":{"baseline_str":0.6048,"str_p25":0.5256,"str_p50":0.6796,"str_p75":0.812,"preroll_str":0.7886,"midroll_str":0.6228,"midroll_share":0.7996,"hid_count":7224,"wt_per_vv":2487.5,"avg_active_days":24.38,"confidence":"High"},"CTV|network fiction gec|Mixed|Ent Only|hotstarsuper":{"baseline_str":0.577,"str_p25":0.4923,"str_p50":0.6446,"str_p75":0.7763,"preroll_str":0.7466,"midroll_str":0.5955,"midroll_share":0.8002,"hid_count":6926,"wt_per_vv":2514.1,"avg_active_days":22.79,"confidence":"High"},"CTV|network non fiction gec|Ent|Sports & Ent|hotstarbundle":{"baseline_str":0.6129,"str_p25":0.5525,"str_p50":0.6863,"str_p75":0.8202,"preroll_str":0.8,"midroll_str":0.6883,"midroll_share":0.7171,"hid_count":10731,"wt_per_vv":2606.0,"avg_active_days":23.48,"confidence":"High"},"Mobile|network non fiction gec|Ent|Fringe|singledevice":{"baseline_str":0.3793,"str_p25":0.2923,"str_p50":0.5,"str_p75":0.75,"preroll_str":0.6578,"midroll_str":0.6142,"midroll_share":0.472,"hid_count":46936,"wt_per_vv":306.0,"avg_active_days":7.88,"confidence":"High"},"Mobile|network non fiction gec|Ent|Sports & Ent|hotstarmobile":{"baseline_str":0.3673,"str_p25":0.2916,"str_p50":0.4912,"str_p75":0.678,"preroll_str":0.6548,"midroll_str":0.648,"midroll_share":0.4237,"hid_count":13997,"wt_per_vv":1242.1,"avg_active_days":21.14,"confidence":"High"},"CTV|network non fiction gec|Ent|Ent Only|singledevice":{"baseline_str":0.5961,"str_p25":0.5023,"str_p50":0.6484,"str_p75":0.7916,"preroll_str":0.7497,"midroll_str":0.6524,"midroll_share":0.7528,"hid_count":12799,"wt_per_vv":1850.9,"avg_active_days":19.09,"confidence":"High"},"Mobile|network non fiction gec|Ent|Ent Only|hotstarsuper":{"baseline_str":0.4105,"str_p25":0.3014,"str_p50":0.4851,"str_p75":0.6433,"preroll_str":0.6035,"midroll_str":0.6325,"midroll_share":0.5206,"hid_count":10638,"wt_per_vv":1640.8,"avg_active_days":20.19,"confidence":"High"},"Mobile|network fiction gec|Ent|Fringe|singledevice":{"baseline_str":0.323,"str_p25":0.25,"str_p50":0.4153,"str_p75":0.625,"preroll_str":0.6031,"midroll_str":0.4586,"midroll_share":0.5232,"hid_count":27131,"wt_per_vv":299.5,"avg_active_days":7.05,"confidence":"High"},"Mobile|network fiction gec|Mixed|Sports & Ent|singledevice":{"baseline_str":0.4335,"str_p25":0.3568,"str_p50":0.56,"str_p75":0.7569,"preroll_str":0.7708,"midroll_str":0.6616,"midroll_share":0.4906,"hid_count":10703,"wt_per_vv":889.5,"avg_active_days":20.0,"confidence":"High"},"Mobile|network fiction gec|Ent|Sports & Ent|hotstarmobile":{"baseline_str":0.363,"str_p25":0.297,"str_p50":0.4688,"str_p75":0.6522,"preroll_str":0.6631,"midroll_str":0.5389,"midroll_share":0.5034,"hid_count":8704,"wt_per_vv":995.6,"avg_active_days":21.45,"confidence":"High"},"Mobile|network fiction gec|Ent|Ent Only|hotstarbundle":{"baseline_str":0.3515,"str_p25":0.2685,"str_p50":0.4254,"str_p75":0.5805,"preroll_str":0.6053,"midroll_str":0.503,"midroll_share":0.544,"hid_count":5042,"wt_per_vv":1484.1,"avg_active_days":21.01,"confidence":"High"},"CTV|network fiction gec|Ent|Sports & Ent|singledevice":{"baseline_str":0.5059,"str_p25":0.419,"str_p50":0.5742,"str_p75":0.7429,"preroll_str":0.7312,"midroll_str":0.513,"midroll_share":0.7843,"hid_count":4893,"wt_per_vv":2396.5,"avg_active_days":22.91,"confidence":"High"},"Mobile|network fiction gec|Mixed|Fringe|free":{"baseline_str":0.4289,"str_p25":0.3333,"str_p50":0.5,"str_p75":0.7447,"preroll_str":0.7508,"midroll_str":0.626,"midroll_share":0.5011,"hid_count":45587,"wt_per_vv":104.8,"avg_active_days":4.67,"confidence":"High"},"CTV|network non fiction gec|Ent|Sports & Ent|hotstarsuper":{"baseline_str":0.6431,"str_p25":0.5636,"str_p50":0.7089,"str_p75":0.8318,"preroll_str":0.8327,"midroll_str":0.7164,"midroll_share":0.7156,"hid_count":7532,"wt_per_vv":2487.4,"avg_active_days":23.55,"confidence":"High"},"Mobile|network non fiction gec|Mixed|Sports & Ent|singledevice":{"baseline_str":0.4128,"str_p25":0.3459,"str_p50":0.5833,"str_p75":0.7925,"preroll_str":0.8113,"midroll_str":0.7133,"midroll_share":0.4051,"hid_count":16947,"wt_per_vv":712.0,"avg_active_days":16.89,"confidence":"High"},"Mobile|network fiction gec|Mixed|Sports & Ent|hotstarmobile":{"baseline_str":0.4449,"str_p25":0.3543,"str_p50":0.5581,"str_p75":0.7508,"preroll_str":0.7754,"midroll_str":0.6893,"midroll_share":0.494,"hid_count":6922,"wt_per_vv":975.9,"avg_active_days":21.42,"confidence":"High"},"Mobile|network non fiction gec|Ent|Ent Only|hotstarbundle":{"baseline_str":0.4026,"str_p25":0.3099,"str_p50":0.4772,"str_p75":0.6264,"preroll_str":0.6099,"midroll_str":0.5969,"midroll_share":0.5383,"hid_count":6214,"wt_per_vv":1679.1,"avg_active_days":20.47,"confidence":"High"},"Mobile|network fiction gec|Mixed|Ent Only|hotstarsuper":{"baseline_str":0.4344,"str_p25":0.3519,"str_p50":0.5444,"str_p75":0.7118,"preroll_str":0.733,"midroll_str":0.6618,"midroll_share":0.5154,"hid_count":4361,"wt_per_vv":1408.3,"avg_active_days":21.4,"confidence":"High"},"Web|international|Mixed|Sports Only|hotstarmobile":{"baseline_str":0.5357,"str_p25":0.5357,"str_p50":0.5357,"str_p75":0.5357,"preroll_str":0.7778,"midroll_str":1.0,"midroll_share":0.2857,"hid_count":1,"wt_per_vv":3.7,"avg_active_days":7.0,"confidence":"Low"} }


STR_FALLBACK = {"level2_4dim":{"Web|international|Mixed|Sports Only":0.577,"Mobile|others|Mixed|Ent Only":0.421,"CTV|others|Mixed|Sports & Ent":0.5037,"CTV|specials|Ent|Sports & Ent":0.5665,"Mobile|network fiction gec|Ent|Sports Only":0.399,"CTV|creator content|Ent|Fringe":0.4903,"CTV|network non fiction gec|Mixed|Sports Only":0.756,"Web|specials|Mixed|Fringe":0.4588,"Mobile|creator content|Mixed|Ent Only":0.3707,"Web|kids|Mixed|Fringe":0.2173,"Web|specials|Ent|Sports & Ent":0.3603,"CTV|others|Ent|Sports Only":0.9129,"Mobile|others|Ent|Ent Only":0.3913,"CTV|network fiction gec|Mixed|Sports Only":0.5728,"CTV|kids|Mixed|Sports & Ent":0.395,"Web|kids|Ent|Sports Only":0.6206,"CTV|network fiction gec|Mixed|Ent Only":0.5567,"Web|international|Mixed|Ent Only":0.4253,"Web|international|Mixed|Fringe":0.4435,"Mobile|international|Mixed|Ent Only":0.4473,"Web|network non fiction gec|Mixed|Sports Only":0.6146,"Web|network non fiction gec|Mixed|Ent Only":0.4868,"Mobile|network fiction gec|Ent|Fringe":0.3227,"Mobile|network non fiction gec|Ent|Ent Only":0.3777,"Web|indian movies|Ent|Sports & Ent":0.3509,"Web|indian movies|Mixed|Fringe":0.3539,"Mobile|others|Mixed|Fringe":0.4434,"Web|network fiction gec|Ent|Sports & Ent":0.3348,"CTV|international|Ent|Sports Only":0.7185,"Web|network fiction gec|Mixed|Sports & Ent":0.4215,"CTV|international|Ent|Fringe":0.5405,"Mobile|network non fiction gec|Mixed|Sports & Ent":0.4253,"CTV|international|Mixed|Fringe":0.5665,"CTV|network non fiction gec|Ent|Fringe":0.6285,"Mobile|international|Ent|Sports & Ent":0.4238,"Web|indian movies|Mixed|Sports & Ent":0.454,"Mobile|specials|Mixed|Fringe":0.5189,"Mobile|network fiction gec|Mixed|Sports Only":0.4647,"Web|indian movies|Mixed|Ent Only":0.3654,"Web|network non fiction gec|Mixed|Sports & Ent":0.516,"Mobile|network non fiction gec|Mixed|Sports Only":0.6633,"Web|indian movies|Mixed|Sports Only":0.4849,"Web|others|Mixed|Sports & Ent":0.3826,"Web|others|Mixed|Ent Only":0.2621,"CTV|indian movies|Ent|Sports & Ent":0.5982,"Mobile|network non fiction gec|Ent|Sports & Ent":0.377,"Mobile|indian movies|Ent|Fringe":0.4271,"Mobile|creator content|Ent|Fringe":0.4499,"CTV|kids|Mixed|Fringe":0.3796,"CTV|indian movies|Mixed|Sports Only":0.7046,"Web|indian movies|Ent|Sports Only":0.3921,"CTV|specials|Mixed|Sports & Ent":0.6448,"CTV|creator content|Mixed|Ent Only":0.3727,"CTV|creator content|Mixed|Sports & Ent":0.5644,"Web|kids|Ent|Sports & Ent":0.21,"CTV|creator content|Ent|Sports Only":0.8366,"Mobile|kids|Mixed|Fringe":0.3069,"Web|network non fiction gec|Ent|Sports & Ent":0.4089,"Mobile|kids|Ent|Ent Only":0.1889,"CTV|network fiction gec|Mixed|Fringe":0.5434,"CTV|network fiction gec|Ent|Fringe":0.5063,"CTV|kids|Ent|Sports Only":0.5409,"Web|specials|Ent|Ent Only":0.313,"Mobile|kids|Ent|Sports Only":0.6423,"Mobile|others|Mixed|Sports & Ent":0.4915,"CTV|indian movies|Ent|Sports Only":0.6807,"Mobile|specials|Mixed|Ent Only":0.4754,"Web|creator content|Mixed|Fringe":0.1095,"Mobile|indian movies|Mixed|Sports & Ent":0.5754,"Web|creator content|Ent|Fringe":0.2238,"Mobile|others|Mixed|Sports Only":0.5483,"Web|kids|Mixed|Sports & Ent":0.2452,"CTV|indian movies|Ent|Fringe":0.5457,"Web|creator content|Mixed|Ent Only":0.2125,"CTV|kids|Ent|Sports & Ent":0.3738,"Web|network fiction gec|Ent|Sports Only":0.4295,"Mobile|creator content|Ent|Ent Only":0.3934,"CTV|indian movies|Mixed|Sports & Ent":0.6535,"Web|network fiction gec|Ent|Ent Only":0.2951,"Web|network fiction gec|Mixed|Ent Only":0.3952,"Web|others|Ent|Ent Only":0.2495,"CTV|network fiction gec|Ent|Sports & Ent":0.5213,"CTV|network non fiction gec|Ent|Sports Only":0.7288,"CTV|creator content|Ent|Ent Only":0.5028,"Mobile|kids|Ent|Fringe":0.2767,"Web|international|Ent|Sports & Ent":0.3719,"Web|network non fiction gec|Ent|Sports Only":0.4937,"CTV|kids|Ent|Fringe":0.3619,"Mobile|creator content|Ent|Sports & Ent":0.6049,"CTV|kids|Mixed|Ent Only":0.3485,"CTV|network fiction gec|Ent|Ent Only":0.5074,"CTV|international|Ent|Ent Only":0.509,"Mobile|kids|Mixed|Sports Only":0.55,"Mobile|indian movies|Ent|Ent Only":0.3998,"Web|international|Ent|Fringe":0.357,"Mobile|network fiction gec|Mixed|Ent Only":0.414,"Mobile|creator content|Mixed|Sports & Ent":0.4883,"Mobile|indian movies|Ent|Sports & Ent":0.4852,"Mobile|specials|Mixed|Sports & Ent":0.548,"Mobile|indian movies|Ent|Sports Only":0.6765,"Web|network non fiction gec|Ent|Ent Only":0.3829,"CTV|network fiction gec|Mixed|Sports & Ent":0.5811,"Mobile|kids|Mixed|Ent Only":0.2769,"Web|kids|Mixed|Sports Only":0.2826,"Mobile|specials|Ent|Fringe":0.3918,"Mobile|kids|Ent|Sports & Ent":0.2908,"Web|network fiction gec|Mixed|Sports Only":0.4881,"Mobile|indian movies|Mixed|Fringe":0.5,"CTV|others|Ent|Sports & Ent":0.4847,"CTV|specials|Mixed|Sports Only":0.7098,"Mobile|network fiction gec|Mixed|Sports & Ent":0.4382,"Mobile|kids|Mixed|Sports & Ent":0.3644,"Mobile|indian movies|Mixed|Sports Only":0.6938,"Web|specials|Ent|Sports Only":0.4078,"Web|kids|Ent|Fringe":0.1689,"Web|creator content|Ent|Ent Only":0.2624,"CTV|others|Mixed|Sports Only":0.3498,"Web|indian movies|Ent|Fringe":0.2637,"Web|creator content|Ent|Sports Only":0.3291,"CTV|network non fiction gec|Mixed|Ent Only":0.6486,"Mobile|network non fiction gec|Ent|Fringe":0.3737,"CTV|others|Ent|Ent Only":0.4243,"Mobile|international|Mixed|Fringe":0.4493,"CTV|network non fiction gec|Mixed|Sports & Ent":0.6731,"CTV|international|Mixed|Sports & Ent":0.6091,"CTV|specials|Ent|Ent Only":0.5263,"CTV|indian movies|Mixed|Fringe":0.5838,"CTV|international|Ent|Sports & Ent":0.5578,"Mobile|specials|Ent|Sports & Ent":0.4479,"Web|creator content|Mixed|Sports & Ent":0.3926,"Web|creator content|Ent|Sports & Ent":0.473,"Mobile|international|Ent|Sports Only":0.7296,"Mobile|network non fiction gec|Ent|Sports Only":0.5081,"CTV|network non fiction gec|Mixed|Fringe":0.6766,"CTV|specials|Mixed|Fringe":0.6116,"CTV|indian movies|Ent|Ent Only":0.533,"Web|specials|Ent|Fringe":0.33,"CTV|creator content|Ent|Sports & Ent":0.6486,"Mobile|international|Ent|Fringe":0.4113,"CTV|specials|Ent|Sports Only":0.6897,"CTV|specials|Ent|Fringe":0.5405,"CTV|indian movies|Mixed|Ent Only":0.5787,"Web|international|Ent|Ent Only":0.34,"Mobile|network non fiction gec|Mixed|Fringe":0.4323,"Web|others|Ent|Sports & Ent":0.3447,"Mobile|network fiction gec|Ent|Ent Only":0.341,"CTV|others|Ent|Fringe":0.5292,"Mobile|specials|Mixed|Sports Only":0.7102,"Web|specials|Mixed|Sports Only":0.5187,"Web|others|Mixed|Sports Only":0.285,"Web|indian movies|Ent|Ent Only":0.2792,"Mobile|network non fiction gec|Mixed|Ent Only":0.4128,"CTV|network non fiction gec|Ent|Ent Only":0.6066,"Web|network fiction gec|Ent|Fringe":0.2604,"CTV|network non fiction gec|Ent|Sports & Ent":0.6203,"Mobile|indian movies|Mixed|Ent Only":0.466,"Mobile|network fiction gec|Mixed|Fringe":0.4161,"CTV|creator content|Mixed|Fringe":0.425,"Mobile|specials|Ent|Ent Only":0.3921,"Web|international|Mixed|Sports & Ent":0.487,"Mobile|others|Ent|Sports & Ent":0.4942,"Web|kids|Ent|Ent Only":0.1659,"Web|network fiction gec|Mixed|Fringe":0.3712,"Web|specials|Mixed|Sports & Ent":0.4863,"Mobile|international|Ent|Ent Only":0.3861,"CTV|network fiction gec|Ent|Sports Only":0.5519,"Mobile|international|Mixed|Sports Only":0.6551,"CTV|specials|Mixed|Ent Only":0.6015,"CTV|others|Mixed|Ent Only":0.444,"Mobile|specials|Ent|Sports Only":0.6946,"Web|specials|Mixed|Ent Only":0.4127,"CTV|international|Mixed|Sports Only":0.7414,"Web|others|Ent|Fringe":0.3155,"Mobile|creator content|Mixed|Fringe":0.4233,"Web|network non fiction gec|Mixed|Fringe":0.4913,"Mobile|others|Ent|Fringe":0.5933,"Web|network non fiction gec|Ent|Fringe":0.3915,"Mobile|international|Mixed|Sports & Ent":0.4889,"CTV|kids|Mixed|Sports Only":0.5257,"Web|international|Ent|Sports Only":0.4747,"Mobile|network fiction gec|Ent|Sports & Ent":0.3603,"Web|kids|Mixed|Ent Only":0.1799,"CTV|international|Mixed|Ent Only":0.5454,"CTV|others|Mixed|Fringe":0.4507,"CTV|kids|Ent|Ent Only":0.3249,"Web|others|Ent|Sports Only":0.6213,"Web|others|Mixed|Fringe":0.2544},"level3_3dim":{"Web|creator content|Mixed":0.2084,"CTV|others|Mixed":0.4713,"CTV|network non fiction gec|Mixed":0.6629,"Mobile|network non fiction gec|Mixed":0.422,"Web|international|Mixed":0.4556,"CTV|specials|Mixed":0.6255,"Mobile|kids|Mixed":0.3204,"Mobile|indian movies|Mixed":0.54,"Mobile|creator content|Mixed":0.5811,"CTV|creator content|Mixed":0.4917,"CTV|indian movies|Mixed":0.6149,"Web|network fiction gec|Mixed":0.4036,"Web|kids|Mixed":0.2202,"Mobile|network non fiction gec|Ent":0.3788,"Web|specials|Ent":0.3281,"Mobile|network fiction gec|Mixed":0.4193,"Web|specials|Mixed":0.4539,"CTV|kids|Mixed":0.3749,"CTV|international|Mixed":0.5822,"Web|others|Mixed":0.31,"Mobile|others|Mixed":0.4501,"Mobile|specials|Mixed":0.5203,"Mobile|international|Mixed":0.4828,"Web|indian movies|Mixed":0.4004,"CTV|network fiction gec|Mixed":0.5691,"Web|network non fiction gec|Mixed":0.4998,"CTV|creator content|Ent":0.5341,"CTV|network fiction gec|Ent":0.5125,"CTV|indian movies|Ent":0.5567,"Mobile|network fiction gec|Ent":0.3419,"Web|indian movies|Ent":0.2964,"Mobile|creator content|Ent":0.5475,"Web|international|Ent":0.3529,"Mobile|specials|Ent":0.4092,"CTV|specials|Ent":0.5405,"Mobile|international|Ent":0.4189,"CTV|network non fiction gec|Ent":0.6128,"CTV|others|Ent":0.4638,"Web|kids|Ent":0.1779,"Mobile|others|Ent":0.5258,"CTV|kids|Ent":0.345,"Web|network non fiction gec|Ent":0.3919,"Mobile|indian movies|Ent":0.4537,"Mobile|kids|Ent":0.2457,"Web|network fiction gec|Ent":0.3032,"Web|creator content|Ent":0.2651,"CTV|international|Ent":0.5294,"Web|others|Ent":0.3047}}






# =============================================================================
#  END OF JSON PASTE ZONE
# =============================================================================

PARENT_DIMS_5 = ["lagged_engagement_quadrant","platform_group","gender_clean","subs_status","seasonality"]
DIM_LABELS = {
    "lagged_engagement_quadrant": "Engagement Quadrant",
    "platform_group":             "Platform",
    "gender_clean":               "Gender",
    "subs_status":                "Subscription Status",
    "seasonality":                "Seasonality",
    "dominant_plan_type":         "Plan Type",
    "dominant_proposition":       "Content Proposition",
}
TIER_COLORS   = {"High": "#059669", "Medium": "#D97706", "Low": "#DC2626"}
BADGE_CLASSES = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}
 
# Confidence explanation logic — not just R² but actual reasoning
def tier_explanation(tier, r2_in, r2_cv, n_seg):
    gap = round(r2_in - (r2_cv or 0), 3)
    if tier == "High":
        return (f"Model fitted on {n_seg} sub-segments with strong out-of-sample stability "
                f"(R² drops only {gap:.2f} from in-sample to LOOCV). "
                f"Large segment count means the regression is not sensitive to any single data point. "
                f"Directional estimates are reliable.")
    elif tier == "Medium":
        return (f"Fitted on {n_seg} sub-segments — adequate but limited. "
                f"R² gap between in-sample and LOOCV is {gap:.2f}, suggesting mild sensitivity. "
                f"Direction is reliable; treat magnitude with ±20–30% uncertainty.")
    else:
        return (f"R² drops sharply from {r2_in:.3f} (in-sample) to {r2_cv:.3f} (LOOCV) — "
                f"a gap of {gap:.2f}, exceeding the overfit threshold of 0.20. "
                f"The model memorises the {n_seg} training segments rather than generalising. "
                f"Use direction only; do not commit on magnitude.")
 
DEFAULT_ECPM_MID = {"Mobile": 80.0, "CTV": 150.0, "Web": 100.0}
DEFAULT_ECPM_PRE = {"Mobile": 50.0, "CTV": 100.0, "Web": 65.0}
 
def fmt_pct(v, decimals=2):
    if v is None: return "—"
    sign = "+" if v >= 0 else ""
    return f"{sign}{v:.{decimals}f}%"
 
def make_elasticity_key(sel):
    return " | ".join(str(sel[d]) for d in PARENT_DIMS_5)
 
def make_str_data_key(sel):
    return "|".join([
        sel.get("platform_group",""),
        sel.get("dominant_proposition",""),
        sel.get("seasonality",""),
        sel.get("lagged_engagement_quadrant",""),
        sel.get("dominant_plan_type",""),
    ])
 
def get_elasticity(sel, model_dict):
    return model_dict.get(make_elasticity_key(sel))
 
def get_str(sel):
    result = STR_LOOKUP.get(make_str_data_key(sel))
    if result is not None:
        return result.get("baseline_str")
    plat = sel.get("platform_group","")
    prop = sel.get("dominant_proposition","")
    sea  = sel.get("seasonality","")
    quad = sel.get("lagged_engagement_quadrant","")
    val4 = STR_FALLBACK.get("level2_4dim",{}).get(f"{plat}|{prop}|{sea}|{quad}")
    if val4 is not None: return val4
    return STR_FALLBACK.get("level3_3dim",{}).get(f"{plat}|{prop}|{sea}")
 
def pct_change(e_dict, wt, ad):
    if e_dict is None: return None
    b1 = float(e_dict.get("elasticity_wt_per_vv", 0))
    b2 = float(e_dict.get("elasticity_active_days", 0))
    return (((1+wt/100)**b1) * ((1+ad/100)**b2) - 1) * 100
 
 
# ─── Cohort Explorer dataframe (cached, fully independent) ──────────────────
@st.cache_data
def build_explorer_df():
    rows = []
    for key, e in ELASTICITY_TOTAL.items():
        parts = key.split(" | ")
        if len(parts) != 5: continue
        rows.append({
            "Quadrant":    parts[0], "Platform": parts[1],
            "Gender":      parts[2], "Subs Status": parts[3], "Seasonality": parts[4],
            "Confidence":  e.get("effective_tier",""),
            "Sub-segs":    e.get("n_segments", 0),
            "HID-months":  e.get("total_hid", 0),
            "WT/VV β":     round(e.get("elasticity_wt_per_vv",0), 4),
            "AD β":        round(e.get("elasticity_active_days",0), 4),
            "R² in":       round(e.get("r2_in_sample",0), 3),
            "R² LOOCV":    round(e.get("r2_loocv",0) if e.get("r2_loocv") is not None else 0, 3),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        s = df["HID-months"].sum()
        df["HID %"] = (df["HID-months"] / s * 100).round(2) if s > 0 else 0.0
    return df
 
 
# ═════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════
st.sidebar.markdown("## Cohort Configuration")
st.sidebar.markdown("---")
 
sel = {}
st.sidebar.markdown('<div class="sb-lbl">Forecasting Dimensions</div>', unsafe_allow_html=True)
for d in PARENT_DIMS_5:
    opts = DIMENSION_VALUES.get(d, [])
    sel[d] = st.sidebar.selectbox(DIM_LABELS[d], opts, key=f"s_{d}")
 
st.sidebar.markdown('<hr class="sb-divider">', unsafe_allow_html=True)
 
st.sidebar.markdown('<div class="sb-lbl">STR Lookup Dimensions</div>', unsafe_allow_html=True)
for d in ["dominant_proposition", "dominant_plan_type"]:
    opts = DIMENSION_VALUES.get(d, [])
    sel[d] = st.sidebar.selectbox(DIM_LABELS[d], opts, key=f"s_{d}")
 
st.sidebar.markdown("---")
st.sidebar.markdown("**Engagement Levers**")
 
st.sidebar.markdown('<div class="sb-lbl">WT/VV change (%)</div>', unsafe_allow_html=True)
wc1, wc2 = st.sidebar.columns([3,1])
with wc1:
    wt_sl = st.slider("wt_sl_", -10.0, 100.0, 0.0, 0.5, label_visibility="collapsed", key="wt_sl_")
with wc2:
    wt_nb = st.number_input("wt_nb_", -10.0, 100.0, float(wt_sl), 0.5, label_visibility="collapsed", key="wt_nb_")
wt_pct = wt_nb
 
st.sidebar.markdown('<div class="sb-lbl" style="margin-top:6px;">Active Days change (%)</div>', unsafe_allow_html=True)
ac1, ac2 = st.sidebar.columns([3,1])
with ac1:
    ad_sl = st.slider("ad_sl_", -10.0, 50.0, 0.0, 0.5, label_visibility="collapsed", key="ad_sl_")
with ac2:
    ad_nb = st.number_input("ad_nb_", -10.0, 50.0, float(ad_sl), 0.5, label_visibility="collapsed", key="ad_nb_")
ad_pct = ad_nb
 
st.sidebar.markdown("---")
st.sidebar.markdown("**eCPM**")
plat = sel.get("platform_group","Mobile")
ecpm_mid = st.sidebar.number_input("Midroll eCPM (Rs./1K)", 10.0, 500.0,
    float(DEFAULT_ECPM_MID.get(plat,80.0)), 5.0, key="ecpm_mid_")
ecpm_pre = st.sidebar.number_input("Preroll eCPM (Rs./1K)", 10.0, 500.0,
    float(DEFAULT_ECPM_PRE.get(plat,50.0)), 5.0, key="ecpm_pre_")
 
run_sim = st.sidebar.button("Run Simulation", type="primary", use_container_width=True)
 
 
# ═════════════════════════════════════════════════════════════════════
# TABS
# ═════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["Simulator", "Cohort Explorer", "Model Architecture"])
 
 
# ────────────────────────────────────────────────────────────────────
# TAB 1 — SIMULATOR
# ────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("## Engagement to Ad Revenue Simulator")
    st.caption("Shows how changes in WT/VV and Active Days translate into % change in ad revenue.")
 
    m1, m2, m3 = st.columns(3)
    m1.metric("Inventory Coverage", f"{METADATA.get('coverage_total',0):.1f}%")
    m2.metric("Midroll Coverage",   f"{METADATA.get('coverage_midroll',0):.1f}%")
    m3.metric("Preroll Coverage",   f"{METADATA.get('coverage_preroll',0):.1f}%")
 
    with st.expander("What this simulator shows — and what it intentionally hides"):
        st.markdown("""
**Core output:** % change in ad inventory — not absolute slot counts.
 
Model fitted on 1% sample of Oct–Dec 2025 data. Elasticity = historical co-variation, not causation.
 
`% Δ Inventory = [(1 + WT/VV%)^β₁ × (1 + AD%)^β₂ − 1] × 100`
 
Three independent log-log WLS models: Total | Midroll | Preroll.
Revenue direction assumes STR and eCPM are stable. STR is demand-side and may not co-move with inventory.
        """)
 
    st.markdown("---")
 
    if not run_sim:
        st.info("Configure the cohort in the sidebar and click **Run Simulation**.")
        st.stop()
 
    e_total  = get_elasticity(sel, ELASTICITY_TOTAL)
    e_mid    = get_elasticity(sel, ELASTICITY_MIDROLL)
    e_pre    = get_elasticity(sel, ELASTICITY_PREROLL)
    base_str = get_str(sel)
 
    if e_total is None:
        st.error(f"No model for **{make_elasticity_key(sel)}**. Try a different Gender or Subscription Status.")
        st.stop()
 
    delta_total = pct_change(e_total, wt_pct, ad_pct)
    delta_mid   = pct_change(e_mid,   wt_pct, ad_pct)
    delta_pre   = pct_change(e_pre,   wt_pct, ad_pct)
 
    tier  = str(e_total.get("effective_tier","Medium"))
    r2_in = e_total.get("r2_in_sample", 0)
    r2_cv = e_total.get("r2_loocv", 0)
    n_seg = e_total.get("n_segments", 0)
 
    # Confidence badge
    conf_exp = tier_explanation(tier, r2_in, r2_cv or 0, n_seg)
    st.markdown(f"""
    <div class="{BADGE_CLASSES.get(tier,'badge-medium')}">
      <div class="badge-title" style="color:{TIER_COLORS.get(tier,'#888')};">{tier} Confidence</div>
      <div class="badge-desc">{conf_exp}</div>
    </div>
    """, unsafe_allow_html=True)
 
    # % Change cards
    st.markdown('<div class="sec-hdr">Projected % Change in Ad Inventory</div>', unsafe_allow_html=True)
    st.caption(f"WT/VV lever: **{fmt_pct(wt_pct)}** &nbsp;|&nbsp; Active Days lever: **{fmt_pct(ad_pct)}**")
 
    pc1, pc2, pc3, pc4 = st.columns(4)
    def big_card(col, label, delta, e_dict):
        with col:
            if delta is None:
                css, disp = "pct-big-neu", "—"
            elif delta >= 0:
                css, disp = "pct-big-pos", f"+{delta:.2f}%"
            else:
                css, disp = "pct-big-neg", f"{delta:.2f}%"
            tbadge = ""
            if e_dict:
                t = e_dict.get("effective_tier","")
                tbadge = f'<span style="font-size:9px;font-weight:700;color:{TIER_COLORS.get(t,"#888")};margin-left:5px;">{t}</span>'
            st.markdown(f'<div class="pct-card"><div class="pct-label">{label}{tbadge}</div><div class="{css}">{disp}</div></div>', unsafe_allow_html=True)
 
    big_card(pc1, "TOTAL",   delta_total, e_total)
    big_card(pc2, "MIDROLL", delta_mid,   e_mid)
    big_card(pc3, "PREROLL", delta_pre,   e_pre)
    with pc4:
        # Combined midroll+preroll weighted by platform share
        mid_share = METADATA.get("midroll_share_of_total", 57.92) / 100
        pre_share = METADATA.get("preroll_share_of_total", 13.95) / 100
        if delta_mid is not None and delta_pre is not None:
            combined = (delta_mid * mid_share + delta_pre * pre_share) / (mid_share + pre_share)
            css2 = "pct-big-pos" if combined >= 0 else "pct-big-neg"
            disp2 = f"+{combined:.2f}%" if combined >= 0 else f"{combined:.2f}%"
        else:
            css2, disp2 = "pct-big-neu", "—"
        st.markdown(f'<div class="pct-card"><div class="pct-label">AD-WEIGHTED AVG</div><div class="{css2}">{disp2}</div></div>', unsafe_allow_html=True)
 
    # STR box
    str_dims_html = "".join([
        f'<div class="str-dim-row"><span class="str-dim-k">Platform &nbsp;&nbsp;</span><span class="str-dim-v">{sel.get("platform_group","—")}</span></div>',
        f'<div class="str-dim-row"><span class="str-dim-k">Seasonality &nbsp;&nbsp;</span><span class="str-dim-v">{sel.get("seasonality","—")}</span></div>',
        f'<div class="str-dim-row"><span class="str-dim-k">Proposition &nbsp;&nbsp;</span><span class="str-dim-v">{sel.get("dominant_proposition","—")}</span></div>',
        f'<div class="str-dim-row"><span class="str-dim-k">Quadrant &nbsp;&nbsp;</span><span class="str-dim-v">{sel.get("lagged_engagement_quadrant","—")}</span></div>',
        f'<div class="str-dim-row"><span class="str-dim-k">Plan Type &nbsp;&nbsp;</span><span class="str-dim-v">{sel.get("dominant_plan_type","—")}</span></div>',
    ])
    str_num   = f"{base_str*100:.1f}%" if base_str is not None else "N/A"
    str_color = "#3B82F6" if base_str is not None else "#888"
    str_src   = "Exact 5-dim match" if base_str is not None and STR_LOOKUP.get(make_str_data_key(sel)) else "Fallback average"
 
    st.markdown(f"""
    <div class="str-box">
      <div class="str-dims">
        <div class="str-dims-title">STR Lookup Dimensions</div>
        {str_dims_html}
        <div class="str-note">STR is primarily driven by Platform, Seasonality and Content Proposition.
        Quadrant and Plan Type refine the estimate where sample is sufficient.</div>
        <div class="str-ecpm">Midroll eCPM: <strong>Rs.{ecpm_mid:.0f}/1K</strong> &nbsp;|&nbsp; Preroll eCPM: <strong>Rs.{ecpm_pre:.0f}/1K</strong> &nbsp;|&nbsp; Source: {str_src}</div>
      </div>
      <div class="str-val">
        <div class="str-val-lbl">STR</div>
        <div class="str-val-num" style="color:{str_color};">{str_num}</div>
        <div class="str-val-sub">Sell-through Rate</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
 
    # Revenue cards
    st.markdown('<div class="sec-hdr">Revenue</div>', unsafe_allow_html=True)
    st.caption("Expected % change in revenue. STR is affected by Platform, Seasonality and Content Proposition.")
 
    if base_str is not None and delta_total is not None:
        rv1, rv2, rv3 = st.columns(3)
        for col, lbl, dv in [
            (rv1, "MIDROLL", delta_mid if delta_mid is not None else delta_total),
            (rv2, "PREROLL", delta_pre if delta_pre is not None else delta_total),
            (rv3, "TOTAL",   delta_total),
        ]:
            with col:
                color = "#059669" if dv >= 0 else "#DC2626"
                css2  = "pct-big-pos" if dv >= 0 else "pct-big-neg"
                st.markdown(f'<div class="pct-card"><div class="pct-label">{lbl}</div><div class="{css2}">~{abs(dv):.1f}%</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-info"><div class="insight-title">Revenue Unavailable</div>STR not found for selected combination. Adjust Content Proposition or Plan Type.</div>', unsafe_allow_html=True)
 
    # Equation box
    st.markdown('<div class="sec-hdr">How the % Change Was Computed</div>', unsafe_allow_html=True)
 
    def eq_block(e_dict, label_total, e_mid_d, e_pre_d, wt, ad):
        if e_dict is None:
            return f"<div style='opacity:0.4;font-size:12px;padding:8px 0;'>{label_total}: no model for this cohort.</div>"
 
        def calc(ed):
            if ed is None: return None, None, None, None, None, None
            b1 = float(ed.get("elasticity_wt_per_vv",0))
            b2 = float(ed.get("elasticity_active_days",0))
            ic = float(ed.get("intercept",0))
            wf = (1+wt/100)**b1
            af = (1+ad/100)**b2
            jp = (wf*af-1)*100
            return b1, b2, ic, wf, af, jp
 
        b1,b2,ic,wf,af,jp = calc(e_dict)
        wt_s = f"(1{'+' if wt>=0 else ''}{wt:.1f}%)"  if wt!=0 else "1"
        ad_s = f"(1{'+' if ad>=0 else ''}{ad:.1f}%)"  if ad!=0 else "1"
        b1s = f"{'+' if b1>=0 else ''}{b1:.4f}"
        b2s = f"{'+' if b2>=0 else ''}{b2:.4f}"
        b1_note = '<span class="enote">(negative — higher WT/VV reduces ad density)</span>' if b1<0 else ""
        b2_note = '<span class="enote">(negative — more active days reduces per-user inventory)</span>' if b2<0 else ""
        jp_css = "rpos" if jp>=0 else "rneg"
        jp_str = fmt_pct(jp)
        r2cv   = f"{e_dict.get('r2_loocv',0):.3f}" if e_dict.get("r2_loocv") is not None else "N/A"
 
        # Midroll / Preroll similarly lines
        sim_parts = []
        for ed2, lbl2 in [(e_mid_d,"Midroll"), (e_pre_d,"Preroll")]:
            if ed2 is not None:
                res2 = calc(ed2)
                b1_2,b2_2,ic_2,wf_2,af_2,jp_2 = res2
                jp2_css = "rpos" if jp_2>=0 else "rneg"
                b1s2 = ("+" if b1_2>=0 else "") + f"{b1_2:.4f}"
                b2s2 = ("+" if b2_2>=0 else "") + f"{b2_2:.4f}"
                r2cv2 = f"{ed2.get('r2_loocv',0):.3f}" if ed2.get("r2_loocv") is not None else "N/A"
                jp2_str = fmt_pct(jp_2)
                r2in2 = f"{ed2.get('r2_in_sample',0):.3f}"
                nseg2 = ed2.get("n_segments","—")
                sim_parts.append(
                    f'<div class="eq-similarly">Similarly &mdash; <strong>{lbl2}:</strong> &nbsp;<span class="{jp2_css}">{jp2_str}</span></div>'
                    f'<div class="eq-coeff-row">&beta;&#8321;(WT/VV)={b1s2} &nbsp;|&nbsp; &beta;&#8322;(AD)={b2s2} &nbsp;|&nbsp; R&sup2;(in)={r2in2} &nbsp;|&nbsp; R&sup2;(LOOCV)={r2cv2} &nbsp;|&nbsp; n={nseg2}</div>'
                )
        sim_lines = "".join(sim_parts)
 
        return f"""
        <div class="eq-wrap">
          <div class="eq-title">Total Inventory Model</div>
          <div class="eq-base">
            ln(Inv/HID) = α + β₁·ln(WT/VV) + β₂·ln(Active Days)<br>
            where &nbsp; α = {ic:+.4f}, &nbsp; β₁ = <strong>{b1s}</strong>{b1_note}, &nbsp; β₂ = <strong>{b2s}</strong>{b2_note}
          </div>
          <div class="eq-vals">
            % Δ Inventory &nbsp;=&nbsp; [ {wt_s}<sup>{b1s}</sup> × {ad_s}<sup>{b2s}</sup> − 1 ] × 100<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            =&nbsp; [ {wf:.4f} × {af:.4f} − 1 ] × 100 &nbsp;=&nbsp; <span class="{jp_css}"><strong>{jp_str}</strong></span>
          </div>
          <div class="eq-coeff-row" style="margin-top:6px;">R²(in-sample)={e_dict.get("r2_in_sample",0):.3f} &nbsp;|&nbsp; R²(LOOCV)={r2cv} &nbsp;|&nbsp; n sub-segments={e_dict.get("n_segments","—")} &nbsp;|&nbsp; Confidence={tier}</div>
          {sim_lines}
        </div>"""
 
    st.markdown(eq_block(e_total, "Total", e_mid, e_pre, wt_pct, ad_pct), unsafe_allow_html=True)
 
    # Analytical insights — only warnings, not confidence (already shown above)
    insights = []
    if e_total.get("neg_wtvv_warning"):
        insights.append(("insight-box","Negative WT/VV Elasticity",
            f"β₁ = {e_total.get('elasticity_wt_per_vv',0):.4f}. Deeper per-session engagement is associated with lower ad density — users shift into premium SVOD content with reduced ad load. <strong>Active Days is the primary inventory lever here.</strong>"))
    if e_total.get("neg_ad_warning"):
        insights.append(("insight-box","Negative Active Days Elasticity",
            f"β₂ = {e_total.get('elasticity_active_days',0):.4f}. More active days correlates with lower per-user inventory — likely binge behaviour or sports calendar concentration. <strong>WT/VV is the stronger lever here.</strong>"))
    if e_mid and e_mid.get("neg_wtvv_warning") and not e_total.get("neg_wtvv_warning"):
        insights.append(("insight-info","WT/VV Sign Diverges: Midroll vs Total",
            f"Midroll β₁ = {e_mid.get('elasticity_wt_per_vv',0):.4f} (negative) vs Total β₁ = {e_total.get('elasticity_wt_per_vv',0):.4f} (positive). Incremental inventory likely comes from non-midroll formats."))
    if tier == "Low":
        insights.append(("insight-warn","Low Confidence — Overfit Detected",
            f"R²(in-sample)={r2_in:.3f} vs R²(LOOCV)={r2_cv:.3f}. Gap exceeds 0.20. Direction is indicative only."))
 
    if insights:
        st.markdown('<div class="sec-hdr">Analytical Insights</div>', unsafe_allow_html=True)
        for cls, title, body in insights:
            st.markdown(f'<div class="{cls}"><div class="insight-title">{title}</div>{body}</div>', unsafe_allow_html=True)
 
 
    # ── TOP OPPORTUNITIES EXPANDER ────────────────────────────────────────────
    with st.expander("Top Cohort Opportunities — Highest Expected Revenue Lift"):
        st.caption(
            "Ranks all modelled cohorts by expected % inventory lift at the current lever settings. "
            "Filters to cohorts where both Total and Midroll models exist and confidence is not Low. "
            "Revenue lift = Inventory lift (assumes STR stable)."
        )
 
        mid_share_pct = METADATA.get("midroll_share_of_total", 57.92) / 100
        pre_share_pct = METADATA.get("preroll_share_of_total", 13.95) / 100
        total_hid_universe = 9_170_000  # 1% sample × 100 = full universe approximation
 
        opp_rows = []
        for key, et in ELASTICITY_TOTAL.items():
            # Skip Low confidence
            if et.get("effective_tier") == "Low":
                continue
            em = ELASTICITY_MIDROLL.get(key)
            ep = ELASTICITY_PREROLL.get(key)
            if em is None:
                continue
 
            dt = pct_change(et, wt_pct, ad_pct)
            dm = pct_change(em, wt_pct, ad_pct)
            dp = pct_change(ep, wt_pct, ad_pct) if ep else dm
 
            if dt is None or dm is None:
                continue
 
            # Weighted avg revenue lift across ad formats
            rev_lift = (dm * mid_share_pct + dp * pre_share_pct) / (mid_share_pct + pre_share_pct)
 
            parts = key.split(" | ")
            hid = et.get("total_hid", 0)
            # Inventory coverage: this cohort's HID-months as % of total modelled
            total_modelled_hid = sum(e.get("total_hid", 0) for e in ELASTICITY_TOTAL.values()) or 1
            inv_cov_pct = hid / total_modelled_hid * 100
            # HID share of 9.17M universe (1% sample × 100)
            hid_universe_pct = hid / total_hid_universe * 100
 
            opp_rows.append({
                "Quadrant":        parts[0] if len(parts)>0 else "—",
                "Platform":        parts[1] if len(parts)>1 else "—",
                "Gender":          parts[2] if len(parts)>2 else "—",
                "Subs Status":     parts[3] if len(parts)>3 else "—",
                "Seasonality":     parts[4] if len(parts)>4 else "—",
                "Confidence":      et.get("effective_tier","—"),
                "Total Inv Lift":  round(dt, 2),
                "Midroll Lift":    round(dm, 2),
                "Preroll Lift":    round(dp, 2),
                "Rev Lift (wtd)":  round(rev_lift, 2),
                "HID-months":      hid,
                "% of Modelled":   round(inv_cov_pct, 2),
                "% of Universe":   round(hid_universe_pct, 3),
                "Sub-segs":        et.get("n_segments", 0),
            })
 
        if not opp_rows:
            st.info("Paste ELASTICITY_TOTAL and ELASTICITY_MIDROLL to see opportunities.")
        else:
            opp_df = pd.DataFrame(opp_rows).sort_values("Rev Lift (wtd)", ascending=False)
 
            # Show top N
            top_n = st.slider("Show top N cohorts", 5, min(30, len(opp_df)), 10, key="opp_n")
            opp_display = opp_df.head(top_n).reset_index(drop=True).copy()
            opp_display.insert(0, "Rank", range(1, len(opp_display)+1))
 
            # Highlight current selected cohort
            curr_key = make_elasticity_key(sel)
            st.caption(
                f"Current simulator selection: **{curr_key}** — "
                f"ranked #{opp_df.index[opp_df.apply(lambda r: r['Quadrant']+' | '+r['Platform']+' | '+r['Gender']+' | '+r['Subs Status']+' | '+r['Seasonality']==curr_key, axis=1)].tolist()[0]+1 if curr_key in [r['Quadrant']+' | '+r['Platform']+' | '+r['Gender']+' | '+r['Subs Status']+' | '+r['Seasonality'] for r in opp_rows] else 'outside top cohorts'} "
                f"by weighted revenue lift."
            )
 
            st.dataframe(
                opp_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rank":           st.column_config.NumberColumn(format="%d"),
                    "Total Inv Lift": st.column_config.NumberColumn("Total Inv Lift %", format="%.2f%%"),
                    "Midroll Lift":   st.column_config.NumberColumn("Midroll Lift %",   format="%.2f%%"),
                    "Preroll Lift":   st.column_config.NumberColumn("Preroll Lift %",   format="%.2f%%"),
                    "Rev Lift (wtd)": st.column_config.NumberColumn("Rev Lift % (wtd)", format="%.2f%%"),
                    "HID-months":     st.column_config.NumberColumn(format="%d"),
                    "% of Modelled":  st.column_config.NumberColumn("% Modelled HIDs",  format="%.2f%%"),
                    "% of Universe":  st.column_config.NumberColumn("% Universe HIDs",  format="%.3f%%"),
                    "Sub-segs":       st.column_config.NumberColumn(format="%d"),
                }
            )
 
            st.caption(
                "Rev Lift (wtd) = Midroll lift × midroll share + Preroll lift × preroll share. "
                f"Midroll share = {mid_share_pct*100:.1f}%, Preroll share = {pre_share_pct*100:.1f}% (from METADATA). "
                "Low-confidence cohorts excluded. Lifts are at the lever settings currently set in the sidebar."
            )
 
    with st.expander("Full model coefficients"):
        rows = []
        for lbl, ed in [("Total", e_total),("Midroll", e_mid),("Preroll", e_pre)]:
            if ed is None:
                rows.append({"Model":lbl,"Tier":"—","β_WT":"—","β_AD":"—","Intercept":"—","R² in":"—","R² LOOCV":"—","n":"—"})
            else:
                rows.append({"Model":lbl,"Tier":ed.get("effective_tier","—"),
                    "β_WT":f"{ed.get('elasticity_wt_per_vv',0):.4f}",
                    "β_AD":f"{ed.get('elasticity_active_days',0):.4f}",
                    "Intercept":f"{ed.get('intercept',0):.4f}",
                    "R² in":f"{ed.get('r2_in_sample',0):.4f}",
                    "R² LOOCV":f"{ed.get('r2_loocv',0):.4f}" if ed.get("r2_loocv") is not None else "—",
                    "n":ed.get("n_segments","—")})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
 
 
# ────────────────────────────────────────────────────────────────────
# TAB 2 — COHORT EXPLORER  (completely standalone, no shared state)
# ────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("## Cohort Explorer")
    st.caption("Browse all modelled 5-dim parent cohorts. Filters apply instantly — independent of the simulator.")
 
    # Load data — cached, never depends on run_sim or tab1 state
    _df = build_explorer_df()
 
    if _df.empty:
        st.warning("No data. Paste ELASTICITY_TOTAL (Block 3) from Databricks.")
    else:
        # Summary metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Cohorts",     len(_df))
        c2.metric("High Confidence",   int((_df["Confidence"]=="High").sum()))
        c3.metric("Medium Confidence", int((_df["Confidence"]=="Medium").sum()))
        c4.metric("Low / Overfit",     int((_df["Confidence"]=="Low").sum()))
 
        st.markdown("---")
 
        # Filters
        fc1, fc2, fc3, fc4, fc5 = st.columns(5)
        f_quad = fc1.multiselect("Quadrant",   sorted(_df["Quadrant"].dropna().unique()),     default=[], key="cf_q")
        f_plat = fc2.multiselect("Platform",   sorted(_df["Platform"].dropna().unique()),     default=[], key="cf_p")
        f_gend = fc3.multiselect("Gender",     sorted(_df["Gender"].dropna().unique()),       default=[], key="cf_g")
        f_subs = fc4.multiselect("Subs",       sorted(_df["Subs Status"].dropna().unique()), default=[], key="cf_s")
        f_conf = fc5.multiselect("Confidence", ["High","Medium","Low"],                       default=[], key="cf_c")
 
        # Apply filters to a fresh copy — never touches any tab1 variable
        filtered = _df.copy()
        if f_quad: filtered = filtered[filtered["Quadrant"].isin(f_quad)]
        if f_plat: filtered = filtered[filtered["Platform"].isin(f_plat)]
        if f_gend: filtered = filtered[filtered["Gender"].isin(f_gend)]
        if f_subs: filtered = filtered[filtered["Subs Status"].isin(f_subs)]
        if f_conf: filtered = filtered[filtered["Confidence"].isin(f_conf)]
 
        # Sort preset
        sort_opt = st.radio("Sort by", ["HID volume ↓","HID volume ↑","Top 10 HID","Bottom 10 HID","Negative WT/VV β","Negative AD β"],
                            horizontal=True, key="cf_sort")
        if sort_opt == "HID volume ↓":      filtered = filtered.sort_values("HID-months", ascending=False)
        elif sort_opt == "HID volume ↑":    filtered = filtered.sort_values("HID-months", ascending=True)
        elif sort_opt == "Top 10 HID":      filtered = filtered.nlargest(10,"HID-months")
        elif sort_opt == "Bottom 10 HID":   filtered = filtered.nsmallest(10,"HID-months")
        elif sort_opt == "Negative WT/VV β":filtered = filtered[filtered["WT/VV β"]<0].sort_values("HID-months",ascending=False)
        elif sort_opt == "Negative AD β":   filtered = filtered[filtered["AD β"]<0].sort_values("HID-months",ascending=False)
 
        st.caption(f"Showing **{len(filtered)}** of {len(_df)} cohorts.")
 
        if filtered.empty:
            st.info("No cohorts match selected filters.")
        else:
            # Add S.No. column (always 1,2,3… regardless of sort/filter)
            display_df = filtered.reset_index(drop=True).copy()
            display_df.insert(0, "S.No.", range(1, len(display_df)+1))
 
            show_cols = ["S.No.","Quadrant","Platform","Gender","Subs Status","Seasonality",
                         "Confidence","Sub-segs","HID-months","HID %","WT/VV β","AD β","R² in","R² LOOCV"]
            st.dataframe(
                display_df[[c for c in show_cols if c in display_df.columns]],
                use_container_width=True, height=480, hide_index=True,
                column_config={
                    "S.No.":     st.column_config.NumberColumn(format="%d"),
                    "HID-months":st.column_config.NumberColumn(format="%d"),
                    "HID %":     st.column_config.NumberColumn(format="%.2f%%"),
                    "WT/VV β":   st.column_config.NumberColumn(format="%.4f"),
                    "AD β":      st.column_config.NumberColumn(format="%.4f"),
                    "R² in":     st.column_config.NumberColumn(format="%.3f"),
                    "R² LOOCV":  st.column_config.NumberColumn(format="%.3f"),
                }
            )
 
        st.markdown('<div class="sec-hdr">Distribution</div>', unsafe_allow_html=True)
        d1, d2, d3 = st.columns(3)
        with d1:
            q = _df.groupby("Quadrant")["HID-months"].sum().sort_values(ascending=False)
            st.bar_chart((q/q.sum()*100).round(1).rename("HID %"), height=180)
            st.caption("HID Share — Quadrant")
        with d2:
            p = _df.groupby("Platform")["HID-months"].sum().sort_values(ascending=False)
            st.bar_chart((p/p.sum()*100).round(1).rename("HID %"), height=180)
            st.caption("HID Share — Platform")
        with d3:
            c = _df.groupby("Confidence")["Sub-segs"].count().sort_values(ascending=False)
            st.bar_chart(c.rename("Cohorts"), height=180)
            st.caption("Cohorts by Confidence Tier")
 
 
# ────────────────────────────────────────────────────────────────────
# TAB 3 — MODEL ARCHITECTURE
# ────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("## Model Architecture & Methodology")
    st.caption("Full technical spec — data, model, validation, STR, eCPM, assumptions.")
    st.markdown("""
### 1. Data Foundation
**Source:** `tmp_master_inv_clean` | **Scope:** Oct–Dec 2025 | 1% random HID sample | HID-month grain
 
| Column | Role |
|--------|------|
| `lagged_engagement_quadrant` | Grouping dim — prior month quadrant (eliminates simultaneity bias) |
| `platform_group` | Grouping dim |
| `gender_clean` | Grouping dim |
| `subs_status` | Grouping dim |
| `seasonality` | Oct-Nov = Ent; Dec = Mixed |
| `dominant_plan_type` | STR lookup only |
| `ent_wt_mins / vv_count` | WT/VV predictor |
| `au_days` | Active Days predictor |
| `total_inventory` | Y — Total model |
| `total_midroll_inv` | Y — Midroll model |
| `total_preroll_inv` | Y — Preroll model |
 
---
 
### 2. Elasticity Model
`ln(Inv/HID) = α + β₁·ln(WT/VV) + β₂·ln(Active Days) + ε`
 
Fitted at 5-dim parent level: Quadrant × Platform × Gender × Subs × Seasonality.
Weighted least squares by HID count. VIF(WT/VV, AD) = 1.50 — no multicollinearity.
 
**Why log-log?** Both Y and X are right-skewed. Coefficients are directly interpretable as % elasticities.
 
---
 
### 3. Confidence Tiering (LOOCV)
| Tier | Condition |
|------|-----------|
| **High** | n ≥ 25 sub-segments AND overfit gap ≤ 0.20 |
| **Medium** | 7 ≤ n < 25 AND overfit gap ≤ 0.20 |
| **Low** | Overfit gap > 0.20 (any n) |
 
---
 
### 4. STR Lookup
**Primary signal drivers:** Platform, Seasonality, Content Proposition.
Quadrant and Plan Type provide refinement where sample is sufficient.
 
Lookup cascade: 5-dim exact → 4-dim (drop plan type) → 3-dim (platform + proposition + seasonality).
 
STR is demand-side. Engagement drives inventory supply, not fill rate.
 
---
 
### 5. Assumptions & Limitations
| Assumption | Implication |
|-----------|-------------|
| Associative not causal | Elasticities = historical co-variation |
| 1% sample | Patterns robust; magnitudes carry sampling variance |
| Oct–Dec 2025 only | IPL season would shift Sports cohorts substantially |
| STR assumed stable | Fill rate is demand-side |
| eCPM assumed stable | Manual input; actual rates vary |
| Models independent | Mid + pre may not sum perfectly to total |
    """)
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Source HID-months","9.17 Mn")
    s2.metric("1% Sample","~91.7 K")
    s3.metric("Corr Pairs","306")
    s4.metric("Strong Corr","35")
