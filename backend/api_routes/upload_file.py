from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io

router = APIRouter()

@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    
    # Read the file bytes
    contents = await file.read()
    
    # ── Excel or CSV? ──────────────────────────────────────────
    if file.filename.endswith(".xlsx") or file.filename.endswith(".xls"):
        df = pd.read_excel(io.BytesIO(contents))
        
    elif file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))
        
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a .xlsx, .xls or .csv file."
        )
    
    # ── Find the email column (case-insensitive) ───────────────
    email_column = None
    for col in df.columns:
        if "email" in col.lower():
            email_column = col
            break
    
    if email_column is None:
        raise HTTPException(
            status_code=400,
            detail=f"No email column found. Columns in your file: {list(df.columns)}"
        )
    
    # ── Extract + clean emails ─────────────────────────────────
    emails = (
        df[email_column]
        .dropna()                        # remove empty rows
        .astype(str)                     # convert to string
        .str.strip()                     # remove whitespace
        .str.lower()                     # normalize to lowercase
        .tolist()
    )
    
    # ── Basic email validation ─────────────────────────────────
    valid_emails   = [e for e in emails if "@" in e and "." in e.split("@")[-1]]
    invalid_emails = [e for e in emails if e not in valid_emails]
    
    return {
        "total_found"    : len(emails),
        "valid_count"    : len(valid_emails),
        "invalid_count"  : len(invalid_emails),
        "valid_emails"   : valid_emails,
        "invalid_emails" : invalid_emails,
        "column_used"    : email_column,
    }