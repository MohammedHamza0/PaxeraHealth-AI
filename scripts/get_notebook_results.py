import json

notebook_path = r'f:/Work/PaxeraHealth-AI/notebooks/02_AI_Candidate_Test_Solution.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell.get('source', []))
        if "FINAL MODEL COMPARISON" in source or "print(\"FINAL MODEL COMPARISON\")" in source:
            print("Found comparison cell:")
            outputs = cell.get('outputs', [])
            for out in outputs:
                if 'text' in out:
                    print("".join(out['text']))
                if 'data' in out and 'text/plain' in out['data']:
                    print("".join(out['data']['text/plain']))
