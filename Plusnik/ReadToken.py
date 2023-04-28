# Autoplusnik Copyright (C) 2023 Igor Samsonov

import json
import gspread

def readStepikToken(path: str):
    try:
        with open(path, 'r') as f:
            text = f.read()
            f = json.load(text)
            
            return (f['Client-id'], f['Client-secret'])
    except Exception as e:
        raise ValueError(f"Token file corrupted: {path}")
    
def readGoogleToken(path: str):
    try:
        gc = gspread.service_account(path)
        
        return gc
    except Exception as e:
        raise ValueError(f"Token file corrupted: {path}")