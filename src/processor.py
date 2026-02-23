import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def process_financials(text):
    if not text.strip():
        return [{"metric": "Error", "value": "No text extracted from PDF.", "page": "-", "snippet": "-"}]

    prompt = (
        "You are an expert financial auditor specializing in Indian financial reporting. "
        "Extract key financial metrics from the provided text, which includes page number markers (e.g., --- PAGE 1 ---). "
        "Return a strictly formatted JSON array of objects. "
        "Each object MUST have EXACTLY these keys:\n"
        "1. 'metric': The name of the financial metric.\n"
        "2. 'value_2024': The exact extracted value for the year 2024 (as a string with currency, or '-' if missing).\n"
        "3. 'value_2025': The exact extracted value for the year 2025 (as a string with currency, or '-' if missing).\n"
        "4. 'sub_components': An array of strings listing the names of any child metrics that sum up to this metric (e.g. ['Product Revenue', 'Service Revenue']). Leave empty [] if none.\n"
        "5. 'page': The absolute page number where you found this metric.\n"
        "6. 'snippet': A short, exact 5-8 word quote from the text surrounding the metric to prove its source.\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "1. Look for side-by-side columns representing the current year (2025) and previous year (2024).\n"
        "2. Always format financial values exactly as written (e.g. '₹ 100 Lakhs', '(15.5)%').\n"
        "3. Extract fundamental metrics like Revenue, Gross Margin, Net Income.\n\n"
        "Text to strictly analyze:\n"
        f"{text[:30000]}"
    )
    
    try:
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        
        response = model.generate_content([
            "You output strict JSON. Output an array of objects like [{\"metric\": \"Revenue\", \"value_2024\": \"₹100M\", \"value_2025\": \"₹110M\", \"sub_components\": [\"Product Sales\"], \"page\": 1, \"snippet\": \"Total revenue reached\"}].",
            prompt
        ])
        
        content = response.text
        data = json.loads(content)
        
        if isinstance(data, dict):
            for key, val in data.items():
                if isinstance(val, list):
                    data = val # Extract list
                    break
            else:
                return [{"metric": "Result", "value_2025": json.dumps(data), "page": "-", "snippet": "Data parsed contextually."}]
             
        if isinstance(data, list):
            # Calculate Percentage Change
            from src.validator import parse_indian_currency # Import here to avoid circular dependencies
            
            for item in data:
                if not isinstance(item, dict): continue
                
                # Check for percentage change fields
                item['percentage_change'] = None
                
                v24_raw = item.get('value_2024', '')
                v25_raw = item.get('value_2025', '')
                
                v24 = parse_indian_currency(str(v24_raw))
                v25 = parse_indian_currency(str(v25_raw))
                
                if v24 is not None and v25 is not None and v24 != 0:
                    change = ((v25 - v24) / abs(v24)) * 100
                    item['percentage_change'] = round(change, 2)
                    
            return data
            
        return [{"metric": "Error", "value_2025": "Unexpected JSON structure returned from Gemini.", "page": "-", "snippet": "-"}]
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return [{"metric": "Error", "value_2025": str(e), "page": "-", "snippet": "-"}]