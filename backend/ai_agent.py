import google.generativeai as genai
import json
import re

#  Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

#  Use a supported Gemini model
model = genai.GenerativeModel("models/gemini-3-flash-preview")


def extract_essential_data(text):
    """
    Fully autonomous AI Agent:
    - Reads document text
    - Determines document type
    - Decides what fields are essential
    - Outputs structured JSON dynamically
    """

    prompt = f"""
You are an intelligent document understanding AI agent.

Your job is to analyze the given document text and:

1. Identify the document type (for example: Invoice, Purchase Order, Bill of Entry, Receipt, etc.)
2. Decide which information in this document is essential and meaningful
3. Extract those essential fields automatically
4. Return the result in structured JSON format ONLY

Rules:
- Do NOT hardcode field names unless they are clearly present in the document
- Choose fields dynamically based on document content
- Use clear, descriptive field names
- If a value is missing or unclear, do not add them 
- Do NOT include explanations, markdown, or extra text
- Make sure only the essential fields are extracted
- let the heading be in capital letters
- make sure the result is properly structured

The JSON must follow this structure:

{{
  "document_type": "<detected document type>",
  "essential_data": {{
    "<field_name_1>": "<value>",
    "<field_name_2>": "<value>",
    "...": "..."
  }}
}}

DOCUMENT TEXT:
{text}
"""

    try:
        response = model.generate_content(prompt)
        raw_output = response.text.strip()

        # 🛡️ Extract JSON safely
        json_match = re.search(r"\{.*\}", raw_output, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            return {
                "error": "No valid JSON found in AI response",
                "raw_response": raw_output
            }

    except Exception as e:
        return {
            "error": "Gemini AI extraction failed",
            "reason": str(e)
        }