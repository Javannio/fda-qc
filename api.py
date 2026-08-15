from fastapi import FastAPI, UploadFile, File
from pydantic import ValidationError
from schema import RecallRecord
import pandas as pd
import io

app = FastAPI(title="FDA Recall Data QC API")

@app.get("/")
def root():
    return {"message": "FDA Recall Data QC API — POST a CSV to /validate"}

@app.post("/validate")
async def validate_csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents), dtype={
        'recall_number': str,
        'status': str,
        'classification': str,
        'state': str,
        'country': str,
        'recalling_firm': str,
        'product_description': str,
        'reason_for_recall': str,
        'voluntary_mandated': str,
        'recall_initiation_date': str,
        'report_date': str,
        'termination_date': str,
    })

    fields = ['recall_number', 'status', 'classification', 'state', 'country',
              'recalling_firm', 'product_description', 'reason_for_recall',
              'voluntary_mandated', 'recall_initiation_date', 'report_date',
              'termination_date']

    clean_records = []
    flagged_records = []

    for _, row in df.iterrows():
        record_dict = {f: (row[f] if f in row and pd.notna(row[f]) and row[f] != '' else None) for f in fields}
        try:
            validated = RecallRecord(**record_dict)
            clean_records.append(validated.model_dump())
        except ValidationError as e:
            flagged_records.append({
                **record_dict,
                "flag_reason": "; ".join(err["msg"] for err in e.errors())
            })

    total = len(df)
    passed = len(clean_records)
    failed = len(flagged_records)

    return {
        "total_records": total,
        "passed": passed,
        "flagged": failed,
        "pass_rate": f"{passed/total:.1%}" if total else "0%",
        "flagged_records": flagged_records
    }
