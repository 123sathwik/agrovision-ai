import streamlit as st
import os

def display_prediction_analysis(disease="Healthy", confidence="0%"):
    """Section: Disease Diagnosis Results."""
    st.markdown("<h3 style='color: #1B5E20; margin-top: 30px;'>🦠 Disease Diagnosis</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style='background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #2E7D32;'>
            <p style='margin: 0; color: #666;'>Disease</p>
            <h2 style='margin: 0; color: #1B5E20;'>{disease}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #2E7D32;'>
            <p style='margin: 0; color: #666;'>Confidence</p>
            <h2 style='margin: 0; color: #1B5E20;'>{confidence}</h2>
        </div>
        """, unsafe_allow_html=True)

def display_action_plan_header():
    """Section: Action Plan Header (Optional, kept for spacing)."""
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #1B5E20;'>📋 Action Plan</h2>", unsafe_allow_html=True)

def display_soil_npk_advice(data):
    """Section: Soil & NPK Recommendation."""
    npk = data.get('npk_ratio') or "Unknown"
    fert = data.get('fertilizers') or "N/A"
    
    with st.expander("🧪 Soil & NPK Recommendation", expanded=True):
        st.markdown(f"""
        <div style='background-color: #E8F5E9; padding: 15px; border-radius: 10px;'>
            <p><strong>NPK Ratio:</strong> {npk}</p>
            <p><strong>Fertilizers:</strong> {fert}</p>
        </div>
        """, unsafe_allow_html=True)

def display_crop_rotation(data):
    """Section: Crop Rotation."""
    next_c = data.get('next_crop') or "N/A"
    
    with st.expander("🚜 Crop Rotation", expanded=True):
        st.markdown(f"""
        <div style='background-color: #FFF3E0; padding: 15px; border-radius: 10px;'>
            <p><strong>Successor Crop:</strong> {next_c}</p>
            <p><strong>Cycle:</strong> 2-3 season rotation recommended to break disease cycles.</p>
        </div>
        """, unsafe_allow_html=True)

def display_treatment_strategy(data):
    """Section: Treatment Strategy."""
    treatment_text = data.get('treatment') or "AI recommendation unavailable"
    # Clean markdown if present
    treatment_text = treatment_text.replace("**", "<b>").replace("\n", "<br/>")
    
    with st.expander("🩺 Treatment Strategy", expanded=False):
        st.markdown(f"""
        <div style='background-color: #DCEDC8; padding: 20px; border-radius: 10px; border: 1px solid #AED581;'>
            <p style='color: #33691E;'>{treatment_text}</p>
        </div>
        """, unsafe_allow_html=True)
