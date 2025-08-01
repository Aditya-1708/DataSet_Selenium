import json

# Load JSON data from a file
with open('grouped_jobs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get top-level keys
top_keys = list(data.keys())

print(top_keys)
