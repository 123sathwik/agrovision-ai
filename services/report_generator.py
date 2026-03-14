import os
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_report(data):
    """
    Generates a professional premium PDF diagnostic report.
    """
    output_dir = "outputs/reports"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = int(time.time())
    report_path = os.path.join(output_dir, f"crop_report_{timestamp}.pdf")
    
    doc = SimpleDocTemplate(report_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#1B5E20"),
        alignment=1,
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor("#2E7D32"),
        spaceBefore=15,
        spaceAfter=10
    )

    story = []

    # 1. Header
    story.append(Paragraph("🏥 AgroVision AI Diagnostic Report", title_style))
    story.append(Paragraph(f"<b>Generated on:</b> {time.ctime()}", styles['Normal']))
    story.append(Spacer(1, 20))

    # 2. Diagnostic Summary
    story.append(Paragraph("🧪 Diagnostic Summary", subtitle_style))
    summary_data = [
        ["Disease Identified:", data.get("disease", "Unknown")],
        ["AI Confidence:", data.get("confidence", "0%")]
    ]
    summary_table = Table(summary_data, colWidths=[150, 300])
    summary_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # 3. Dual-Vision Evidence (Original vs Heatmap)
    orig_path = data.get("original_image_path")
    heatmap_path = data.get("heatmap_path")
    
    if (orig_path and os.path.exists(orig_path)) or (heatmap_path and os.path.exists(heatmap_path)):
        story.append(Paragraph("🔬 Dual-Vision Evidence", subtitle_style))
        # Create a table for side-by-side images
        img_table_data = []
        row_images = []
        row_captions = []
        
        if orig_path and os.path.exists(orig_path):
            img_orig = Image(orig_path, width=220, height=180)
            row_images.append(img_orig)
            row_captions.append(Paragraph("<center>Original Leaf</center>", styles['Italic']))
        else:
            row_images.append("")
            row_captions.append("")

        if heatmap_path and os.path.exists(heatmap_path):
            img_heat = Image(heatmap_path, width=220, height=180)
            row_images.append(img_heat)
            row_captions.append(Paragraph("<center>AI Activation Map</center>", styles['Italic']))
        else:
            row_images.append("")
            row_captions.append("")

        img_table_data.append(row_images)
        img_table_data.append(row_captions)
        
        img_table = Table(img_table_data, colWidths=[240, 240])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(img_table)
        story.append(Spacer(1, 20))

    # 4. Expert Action Plan (10-Point Plan)
    # Expert Action Plan (10-Point Plan & NPK)
    story.append(Paragraph("📋 Expert Action Plan", subtitle_style))
    
    if "npk" in data:
        npk = data["npk"]
        story.append(Paragraph(f"<b>Recommended NPK Ratio:</b> {npk.get('ratio', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Fertilizer:</b> {npk.get('fertilizer', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Reason:</b> {npk.get('reason', 'N/A')}", styles['Normal']))
    
    story.append(Paragraph(f"<b>Crop Rotation:</b> {data.get('next_crop', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Detailed Treatment Strategy:</b>", styles['Normal']))
    
    # Simple markdown-like to XML converter for Paragraph
    raw_treatment = data.get("treatment", "AI recommendation unavailable")
    
    # Replace markdown bold/italic with Paragraph tags
    # This is a basic approach, handling pairs of ** and __
    import re
    formatted_text = raw_treatment
    # Replace **text** with <b>text</b>
    formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', formatted_text)
    # Replace __text__ with <i>text</i>
    formatted_text = re.sub(r'__(.*?)__', r'<i>\1</i>', formatted_text)
    # Replace newlines with <br/>
    formatted_text = formatted_text.replace("\n", "<br/>")
    
    story.append(Paragraph(formatted_text, styles['Normal']))
    story.append(Spacer(1, 20))

    # 5. Disease Severity
    if "severity" in data:
        story.append(Paragraph("📉 Disease Severity", subtitle_style))
        sev = data["severity"]
        story.append(Paragraph(f"<b>Severity Level:</b> {sev.get('severity', 'Unknown')}", styles['Normal']))
        story.append(Paragraph(f"<b>Infected Area Percentage:</b> {sev.get('infected_area', 0)} %", styles['Normal']))
        story.append(Spacer(1, 20))

    # 6. Environmental & Spread Intelligence
    story.append(Paragraph("☁️ Environmental & Spread Intelligence", subtitle_style))
    story.append(Paragraph(f"<b>Temperature:</b> {data.get('temperature', 'N/A')} °C", styles['Normal']))
    story.append(Paragraph(f"<b>Humidity:</b> {data.get('humidity', 'N/A')}%", styles['Normal']))
    story.append(Paragraph(f"<b>Risk Level:</b> {data.get('risk_level', 'Unknown')}", styles['Normal']))
    
    if "spread_prediction" in data:
        spread = data["spread_prediction"]
        story.append(Paragraph(f"<b>Disease Spread Risk:</b> {spread.get('spread_risk', 'Unknown')}", styles['Normal']))
        if "explanation" in spread:
            story.append(Paragraph(f"<i>{spread['explanation']}</i>", styles['Normal']))
    story.append(Spacer(1, 20))

    # Optional Page Break for layout and length requirement
    story.append(PageBreak())

    # 7. Farmer Advice
    if "farmer_advice" in data:
        story.append(Paragraph("👨‍🌾 Immediate Farmer Advice", subtitle_style))
        advice = data["farmer_advice"]
        story.append(Paragraph(f"<b>Action:</b> {advice.get('action', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Monitoring:</b> {advice.get('monitoring', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Prevention:</b> {advice.get('prevention', 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 20))

    # Build PDF
    try:
        doc.build(story)
        return {"report_path": report_path}
    except Exception as e:
        print(f"[!] Error building PDF: {e}")
        return {"report_path": None}

if __name__ == "__main__":
    # Test with new keys
    test_data = {
        "disease": "Tomato Early blight",
        "confidence": "92.45%",
        "npk": {
            "ratio": "12-6-6",
            "fertilizer": "Urea + compost mix",
            "reason": "Boost nitrogen to recover leaf damage"
        },
        "temperature": 28,
        "humidity": 82,
        "risk_level": "MODERATE",
        "explanation": "Elevated humidity levels increase the likelihood of plant diseases.",
        "treatment": "**Explanation:** Early blight is a common tomato disease. \n\n**Organic Methods:** Neem oil spray. \n\n**Chemical:** Copper fungicides.",
        "next_crop": "Maize (2–3 season rotation)",
        "severity": {
            "severity": "Moderate Infection",
            "infected_area": 32.5
        },
        "spread_prediction": {
            "spread_risk": "HIGH spread risk within 3–5 days",
            "explanation": "Hot and highly humid conditions are optimal for rapid fungal spread."
        },
        "farmer_advice": {
            "action": "Apply copper fungicide. Carefully prune and burn infected foliage.",
            "monitoring": "Inspect plants every 48 hours.",
            "prevention": "Improve air circulation through pruning."
        }
    }
    print(generate_report(test_data))
