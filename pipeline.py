import os, json
from datetime import datetime
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT = """
You are a data extraction agent. Your task is to find the latest information about TSMC's manufacturing expansion pipeline.

Question: How many manufacturing sites confirmed, under construction, or just about to come online does TSMC have in their pipeline to increase capacity? 
Break this down into >=12nm and <12nm manufacturing sites.

Rules:
1. Return results ONLY in valid JSON matching the schema:
   {
     "company": "TSMC",
     "kpi": "Manufacturing Sites by Process Node",
     "records": [
       {
         "estimated_completion_date": "YYYY-MM-DD or 'Unknown'",
         "gte_12nm_sites": int,
         "lt_12nm_sites": int,
         "source": "URL"
       }
     ],
     "last_updated": "YYYY-MM-DD"
   }
2. Do not add explanations outside of JSON.
3. Always include sources (URLs) you used.
"""

try:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PROMPT}],
        response_format={"type": "json_object"}
    )
    
    # Print the raw response for debugging
    print("DEBUG: Raw GPT response:")
    print(response)

    data = json.loads(response["choices"][0]["message"]["content"])

    out_file = f"kpi_data_{datetime.utcnow().strftime('%Y%m%d')}.json"
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Saved KPI data to {out_file}")
    print("DEBUG: Extracted JSON:")
    print(json.dumps(data, indent=2))

except Exception as e:
    print("❌ ERROR while running pipeline.py:")
    print(str(e))
