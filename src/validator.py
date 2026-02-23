import re

def parse_indian_currency(value_str):
    """
    Parses a string like '₹1,50,000' or '₹34,54,136.30 Crores' into a float multiplier.
    Returns the raw numerical value.
    """
    if not isinstance(value_str, str):
        return None
        
    # Remove currency symbol and commas
    clean_str = re.sub(r'[₹$, ]', '', value_str).strip()
    
    # Handle multipliers
    multiplier = 1.0
    lower_str = clean_str.lower()
    if 'crores' in lower_str or 'crore' in lower_str:
        multiplier = 10000000.0  # 1 Crore = 10,000,000
        clean_str = re.sub(r'crores?', '', lower_str, flags=re.IGNORECASE).strip()
    elif 'lakhs' in lower_str or 'lakh' in lower_str:
        multiplier = 100000.0    # 1 Lakh = 100,000
        clean_str = re.sub(r'lakhs?', '', lower_str, flags=re.IGNORECASE).strip()
    elif 'millions' in lower_str or 'million' in lower_str or 'm' in lower_str:
        multiplier = 1000000.0 
        clean_str = re.sub(r'millions?|m', '', lower_str, flags=re.IGNORECASE).strip()
    elif 'billions' in lower_str or 'billion' in lower_str or 'b' in lower_str:
        multiplier = 1000000000.0 
        clean_str = re.sub(r'billions?|b', '', lower_str, flags=re.IGNORECASE).strip()
        
    try:
        val = float(clean_str)
        return val * multiplier
    except ValueError:
        return None
        
def audit_financials(data):
    """
    Audits the extracted financial data array.
    Injects a 'status' tracking key to each object based on basic math consistency.
    """
    if not isinstance(data, list):
        return data
        
    # First pass: map metrics to their 2025 numerical values for quick lookup
    metrics_map = {}
    for item in data:
        if isinstance(item, dict) and 'metric' in item and 'value_2025' in item:
            metric_name = item['metric'].lower()
            val = parse_indian_currency(str(item['value_2025']))
            if val is not None:
                metrics_map[metric_name] = val
                
    # Second pass: Apply Audit Rules and mark status
    for item in data:
        if not isinstance(item, dict):
            continue
            
        metric_name = item.get('metric', '').lower()
        item['status'] = 'Extracted' # Default status
        
        # Rule 1: Audit Sub-components
        # If the AI identified children components, verify their sum equals the parent.
        sub_components = item.get('sub_components', [])
        if isinstance(sub_components, list) and len(sub_components) > 0:
            parent_val = metrics_map.get(metric_name)
            
            if parent_val is not None:
                children_sum = 0
                all_children_found = True
                
                for child in sub_components:
                    child_val = metrics_map.get(str(child).lower())
                    if child_val is not None:
                        children_sum += child_val
                    else:
                        all_children_found = False
                        break
                        
                if all_children_found:
                    # Allow a small floating point margin of error (e.g., 1%)
                    if abs(parent_val - children_sum) <= max(abs(parent_val) * 0.01, 1.0):
                        item['status'] = 'Verified'
                    else:
                        item['status'] = 'Math Mismatch'
                        
        # Basic check: Total Assets = Total Liabilities + Total Shareholders' Equity
        elif 'total assets' in metric_name:
            liabilities = metrics_map.get('total liabilities')
            equity = metrics_map.get("total shareholders' equity") or metrics_map.get("total equity")
            
            if liabilities is not None and equity is not None:
                expected_assets = liabilities + equity
                actual_assets = metrics_map.get(metric_name)
                
                if actual_assets is not None and abs(expected_assets - actual_assets) <= max(abs(expected_assets) * 0.01, 1.0):
                    item['status'] = 'Verified'
                else:
                    item['status'] = 'Math Mismatch'
                    
    return data