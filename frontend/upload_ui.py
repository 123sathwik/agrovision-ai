"""
Streamlit interface for AgroVision AI.
Handles image uploads and displays analysis results from the FastAPI backend.
"""
import streamlit as st
import requests
import io
from PIL import Image

# Backend API URL
API_URL = "http://localhost:8000/analyze-crop"

st.set_page_config(page_title="AgroVision AI", layout="wide")

st.title("🌱 AgroVision AI: Crop Disease Analyzer")
st.markdown("""
Analyze crop health, generate infection heatmaps, and get AI-powered treatment recommendations.
""")

uploaded_file = st.file_uploader("Upload a crop leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Uploaded Image")
        st.image(uploaded_file, use_column_width=True)

    if st.button("Analyze Crop"):
        with st.spinner("Analyzing image..."):
            try:
                # Prepare the image for the API request
                files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                
                # Call the FastAPI backend
                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    with col2:
                        st.subheader("Infection Heatmap")
                        # Display heatmap image (if path is returned and accessible)
                        heatmap_path = data.get("heatmap")
                        if heatmap_path and io.os.path.exists(heatmap_path):
                            st.image(heatmap_path, use_column_width=True)
                        else:
                            st.info("Heatmap visualization pending...")
                    
                    st.divider()
                    
                    # Display Analysis Results
                    st.header("Analysis Results")
                    
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Detected Status", data.get("disease", "Unknown"))
                    with c2:
                        st.metric("Confidence Score", data.get("confidence", "0%"))
                    with c3:
                        st.metric("Recommended Next Crop", data.get("next_crop", "N/A"))
                    
                    st.subheader("Detailed Report")
                    st.write(f"**Cause of Disease:** {data.get('cause', 'N/A')}")
                    st.write(f"**Recommended Fertilizers:** {data.get('fertilizers', 'N/A')}")
                    st.write(f"**Required NPK Ratio:** {data.get('npk_ratio', 'N/A')}")
                    
                    st.success("**Preventive Measures:**")
                    st.write(data.get("prevention", "Maintain general soil health."))
                    
                else:
                    st.error(f"Error: Backend API returned {response.status_code}")
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

st.sidebar.info("""
**AgroVision AI** uses PyTorch for disease detection, GradCAM for heatmaps, and Groq for agricultural analysis.
""")
