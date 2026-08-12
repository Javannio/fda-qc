import json
import pandas as pd
from pydantic import ValidationError
from schema import RecallRecord

with open('raw_data/fda_recalls_raw.json') as f:
    data = json.load(f)

df = pd.json_normalize(data['results'])

clean_records = []
flagged_records = []

fields = ['recall_number', 'status', 'classification', 'state', 'country',
          'recalling_firm', 'product_description', 'reason_for_recall',
          'voluntary_mandated', 'recall_initiation_date', 'report_date',
          'termination_date']

for _, row in df.iterrows():
    record_dict = {f: (row[f] if pd.notna(row[f]) and row[f] != '' else None) for f in fields}
    try:
        validated = RecallRecord(**record_dict)
        clean_records.append(validated.model_dump())
    except ValidationError as e:
        flagged_records.append({
            **record_dict,
            'flag_reason': '; '.join(err['msg'] for err in e.errors())
        })

clean_df = pd.DataFrame(clean_records)
flagged_df = pd.DataFrame(flagged_records)

clean_df.to_csv('results/clean_data.csv', index=False)
flagged_df.to_csv('results/flagged_data.csv', index=False)

total = len(df)
passed = len(clean_df)
failed = len(flagged_df)

with open('results/summary_report.md', 'w') as f:
    f.write(f"# QC Summary Report\n\n")
    f.write(f"- Total records processed: {total}\n")
    f.write(f"- Passed: {passed} ({passed/total:.1%})\n")
    f.write(f"- Flagged: {failed} ({failed/total:.1%})\n\n")
    if failed > 0:
        f.write(f"## Failure breakdown\n\n")
        f.write(flagged_df['flag_reason'].value_counts().to_string())

print(f"Done. {passed} clean, {failed} flagged. See results/summary_report.md")
