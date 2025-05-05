import re

def extract_answer(text:str, 
                   partent:str = r"Answer:\s*(.*)"):
    
    match = re.search(partent, text)
    
    if match:
        answer_text = match.group(1).strip
        return answer_text
    else:
        return "Answer not found"