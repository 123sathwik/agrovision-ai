# AgroVision AI

AgroVision AI is a comprehensive system designed to analyze crop diseases from uploaded images, provide visual feedback through heatmaps, and offer expert-level agricultural advice using AI-driven analysis.

## Features
- **Disease Detection**: AI-powered identification of crop diseases.
- **Visual Interpretation**: Heatmap generation using GradCAM to show regions of infection.
- **AI Analysis**: Groq API integration for detailed disease reports and treatment advice.
- **Fertilizer Engine**: Personalized recommendations based on disease and soil type.
- **Crop Recommendation**: Suitability analysis for different crops.

## Project Structure
- `app/`: FastAPI application backend logic and API endpoints.
- `ai_engine/`: Core AI logic, including disease detection, heatmap generation, and Groq analysis.
- `services/`: Integration scripts for external services like Firebase and recommendation engines.
- `utils/`: Image processing utilities and prompt templates.
- `frontend/`: Streamlit-based web interface.
- `data/`: Local database storage (e.g., fertilizer details).
- `models/`: Storage for trained AI model checkpoints (`.pth` files).
- `outputs/heatmaps/`: Directory for generated GradCAM visualization images.
- `logs/`: Centralized storage for training logs and system error reports.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables in `.env`.
3. Start the backend server first (must run before dashboard):
   ```bash
   python run_server.py
   ```
4. Start the Streamlit dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```
