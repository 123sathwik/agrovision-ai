"""
Contains templates for AI prompts used in Groq analysis.
Ensures consistent and structured output from the LLM.
"""

DISEASE_ANALYSIS_PROMPT = """
Analyze the following crop disease: {disease_name}.
Provide:
1. Symptoms
2. Causes
3. Immediate Treatment
4. Long-term Prevention
"""
