import sys
import os

# Add project root to path for robust imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import streamlit as st
from PIL import Image
import io
import api_client
import ui_components

# Page Config
st.set_page_config(
    page_title="AgroVision AI Crop Doctor",
    page_icon="🌿",
    layout="wide"
)

# Premium Custom Styling
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f8faf8 0%, #e8f5e9 100%);
    }
    
    /* Centered Header */
    .main-title {
        text-align: center;
        color: #1B5E20;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #388E3C;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #2E7D32 !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: white !important;
    }
    
    /* Premium Button */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background-color: #1B5E20;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #2E7D32;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Cards and Containers */
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Centered Header Section
    st.markdown("<h1 class='main-title'>🏥 AgroVision AI Crop Doctor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Precision Diagnostics & Expert Agricultural Advice</p>", unsafe_allow_html=True)

    # Layout: Sidebar for inputs, Main for results
    with st.sidebar:
        st.markdown("### 🌿 Diagnostics Hub")
        uploaded_file = st.file_uploader("Upload Leaf Sample", type=["jpg", "jpeg", "png"])
        location = st.text_input("📍 Farm Location", value="Chicago", help="Localized weather risk data")
        
        analyze_btn = st.button("🚀 Analyze Crop Health")

        st.markdown("---")
        st.markdown("### 🕒 Recent Scans")
        
        history = api_client.get_history()
        if isinstance(history, list) and len(history) > 0:
            for record in history:
                disease = record.get("disease", "Unknown")
                crop = disease.split("___")[0] if "___" in disease else "Unknown"
                diag = disease.split("___")[1].replace("_", " ") if "___" in disease else disease
                ts = record.get("timestamp", "").split("T")[0]
                
                with st.expander(f"📅 {ts} - {crop}"):
                    st.write(f"**Diag:** {diag}")
                    st.write(f"**Conf:** {record.get('confidence', 'N/A')}")
        else:
            st.caption("No history available.")

    if uploaded_file is not None:
        # Sample Preview
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown("<h3 style='text-align: center; color: #2E7D32;'>📸 Uploaded Leaf</h3>", unsafe_allow_html=True)
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True, channels="RGB")

        if analyze_btn:
            with st.spinner("Doctor is performing multi-service analysis..."):
                # Save temp file
                import uuid
                temp_dir = "temp_uploads"
                os.makedirs(temp_dir, exist_ok=True)
                
                file_id = str(uuid.uuid4())
                temp_path = os.path.join(temp_dir, f"{file_id}.jpg")
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # API Call
                report = api_client.analyze_crop(temp_path, location)
                
                if "error" in report:
                    # Cleanup immediately on error
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    st.error(f"Diagnostic Error: {report['error']}")
                else:
                    # Keep temp_path for report generation
                    report["original_image_path"] = temp_path
                    
                    st.balloons()
                    
                    # Uploaded Leaf & AI Heatmap
                    st.markdown("<h2 style='color: #1B5E20;'>📸 Vision Analysis: Uploaded Leaf & AI Heatmap</h2>", unsafe_allow_html=True)
                    vcol1, vcol2 = st.columns(2)
                    with vcol1:
                        st.image(image, caption="Uploaded Leaf", use_container_width=True)
                    with vcol2:
                        if "heatmap_path" in report and report["heatmap_path"] and os.path.exists(report["heatmap_path"]):
                            st.image(
                                report["heatmap_path"], 
                                caption="AI Heatmap", 
                                use_container_width=True
                            )
                        else:
                            st.warning("Heatmap image not available")

                    # Disease Diagnosis
                    ui_components.display_prediction_analysis(
                        report.get("disease", "Healthy"), 
                        report.get("confidence", "0%")
                    )

                    # Disease Severity
                    if "severity" in report:
                        st.markdown("<h3 style='color: #1B5E20; margin-top: 30px;'>📉 Disease Severity</h3>", unsafe_allow_html=True)
                        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                        sev_col1, sev_col2 = st.columns(2)
                        sev_col1.metric("Severity Level", report["severity"].get("severity", "Unknown"))
                        sev_col2.metric("Infected Area", f"{report['severity'].get('infected_area', 0)} %")
                        st.markdown("</div>", unsafe_allow_html=True)

                    # Disease Spread Forecast
                    if "spread_prediction" in report:
                        st.markdown("<h3 style='color: #1B5E20; margin-top: 30px;'>📈 Disease Spread Forecast</h3>", unsafe_allow_html=True)
                        st.info(report["spread_prediction"].get("spread_risk", "Unknown risk"))
                        if "explanation" in report["spread_prediction"]:
                            st.write(report["spread_prediction"]["explanation"])

                    # Environmental Intelligence Panel
                    st.markdown("<h3 style='color: #1B5E20; margin-top: 30px;'>🌍 Environmental Intelligence</h3>", unsafe_allow_html=True)
                    if "temperature" in report and "humidity" in report and "risk_level" in report:
                        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                        env_col1, env_col2, env_col3 = st.columns(3)
                        env_col1.metric("Temperature", f"{report['temperature']} °C")
                        env_col2.metric("Humidity", f"{report['humidity']} %")
                        
                        # Style risk level based on severity
                        risk = report["risk_level"]
                        risk_color = "red" if "HIGH" in risk else "orange" if "MODERATE" in risk else "green"
                        env_col3.metric("Disease Risk", risk)
                        
                        if "explanation" in report:
                            st.info(report["explanation"])
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.info("Environmental data is not available for this location.")

                    # Action Plan Sections
                    ui_components.display_action_plan_header()
                    ui_components.display_soil_npk_advice(report)
                    ui_components.display_crop_rotation(report)
                    ui_components.display_treatment_strategy(report)

                    # 9. Generate PDF report
                    st.markdown("---")
                    st.markdown("<h3 style='color: #1B5E20;'>📥 Downloadable Report</h3>", unsafe_allow_html=True)
                    from services.report_generator import generate_report
                    pdf_result = generate_report(report)
                    if pdf_result.get("report_path") and os.path.exists(pdf_result["report_path"]):
                        with open(pdf_result["report_path"], "rb") as pdf_file:
                            st.download_button(
                                label="Download Full AI Crop Report",
                                data=pdf_file,
                                file_name="crop_diagnosis_report.pdf",
                                mime="application/pdf",
                                key="download_report_btn"
                            )
                    
                    # Final Cleanup of temp upload
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
    else:
        # Modern Welcome State
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1 style='font-size: 3rem;'>🔬</h1>
                <h3 style='color: #1B5E20;'>AI Vision</h3>
                <p>Identifies 38+ disease classes with deep neural precision.</p>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1 style='font-size: 3rem;'>☁️</h1>
                <h3 style='color: #1B5E20;'>Weather IQ</h3>
                <p>Localized risk assessment using real-time OpenWeather data.</p>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1 style='font-size: 3rem;'>🤖</h1>
                <h3 style='color: #1B5E20;'>Groq Expert</h3>
                <p>Organic and chemical treatment strategies powered by LLaMA 3.3.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: center; margin-top: 50px;'><p style='color: #666;'>👈 Please upload a leaf sample in the sidebar to begin.</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
