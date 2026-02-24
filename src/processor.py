import os
import json
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def process_financials(text):
    if not text.strip():
        return [{"metric": "Error", "value": "No text extracted from PDF.", "page": "-", "snippet": "-"}]

    prompt = (
        "You are an expert data analyst. The provided text contains highly structured reports or tabular data (e.g., Financial Statements, Stock Data, User Stats). "
        "Regardless of the input data shape, your task is to summarize it into a Comparative Dashboard. "
        "First, identify the TWO most recent or relevant periods being compared (e.g., '2021' and '2022', or 'Jan 09' and 'Jan 10'). "
        "Then, extract the core metrics and return a JSON array of objects representing these metrics. "
        "Each metric object MUST have exactly these keys:\n"
        "1. 'metric': Name of the metric (e.g. 'Products (Net sales)', 'Stock Open Price').\n"
        "2. 'value_2024': The formatted value for the OLDER of the two periods (e.g. '$294,866' or '191.00').\n"
        "3. 'value_2025': The formatted value for the NEWER of the two periods (e.g. '$307,003' or '194.50').\n"
        "4. 'percentage_change': A float representing the calculated percentage change from the older to the newer value (e.g. 4.12).\n"
        "5. 'status': A string, strictly either 'VERIFIED' if the math perfectly checks out, or 'EXTRACTED' if it is a raw value.\n"
        "6. 'sub_components': An optional array of strings listing sub-metrics that roll up into this metric, if clearly stated.\n"
        "7. 'page': The absolute page number where this was found.\n"
        "8. 'snippet': A short 5-8 word exact quote to prove its source.\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. We use 'value_2024' and 'value_2025' as schema keys regardless of what the actual periods are. Just map the older period to 'value_2024' and newer to 'value_2025'.\n"
        "2. Do not hallucinate metrics. Map the data precisely.\n"
        "3. FORMATTING: Return clean numbers (e.g., '14,20,00,000' or '$14,20,00,000'). ABSOLUTELY DO NOT prefix numbers with arbitrary letters like 'n' (e.g., 'n14,20,00,000' is strictly invalid).\n"
        "4. Output strictly valid JSON and nothing else.\n\n"
        "Text to strictly analyze:\n"
        f"{text[:30000]}"
    )
    
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                "You output strict JSON. Output an array of objects like [{\"metric\": \"Revenue\", \"value_2024\": \"100M\", \"value_2025\": \"110M\", \"percentage_change\": 10.0, \"status\": \"VERIFIED\", \"sub_components\": [\"Product sales\"], \"page\": 1, \"snippet\": \"Total revenue reached\"}].",
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        content = response.text
        data = json.loads(content)
        
        # Fallback Sanitization: Remove stray leading letters (like 'n') before digits
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    for key in ['value_2024', 'value_2025']:
                        if key in item and isinstance(item[key], str):
                            # e.g., 'n14,200' -> '14,200'
                            item[key] = re.sub(r'^[a-z]+(?=[\$]?\d)', '', item[key])
                            
        if isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, list):
                    data = val # Extract list
                    break
            else:
                return [{"metric": "Result", "value_2024": "-", "value_2025": json.dumps(data), "percentage_change": 0.0, "status": "EXTRACTED", "page": "-", "snippet": "Data parsed contextually."}]
             
        if isinstance(data, list):
            # Normalization fallback for old cache if needed, mostly trust AI
            return data
            
        return [{"metric": "Error", "value_2024": "-", "value_2025": "Unexpected JSON structure returned from Gemini.", "percentage_change": 0.0, "status": "EXTRACTED", "page": "-", "snippet": "-"}]
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return [{"metric": "Error", "value_2025": str(e), "page": "-", "snippet": "-"}]