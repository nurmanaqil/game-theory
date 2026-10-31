from pathlib import Path
import json,hashlib
import pandas as pd
O=Path('kredit/experiments/revision_v1');families=['random_forest','extra_trees','gradient_boosting','xgboost'];ms=[]
for f in families:
 m=json.loads((O/f/'family_manifest.json').read_text());assert m['status']=='PASS';assert m['families']==[f];ms.append(m)
for file in ['selection_validation.csv','predictive_metrics.csv','pilot_checks.csv','attribution_summary.csv','feature_comparison.csv','source_importance.csv','timing.csv']:
 dfs=[pd.read_csv(O/f/'worker_tables'/file) for f in families];pd.concat(dfs,ignore_index=True).to_csv(O/file,index=False)
for key in ['protocol_sha256','script_sha256','versions','evaluation_rows','source_features']:
 assert all(m[key]==ms[0][key] for m in ms),key
merged=dict(ms[0]);merged['families']=families;merged['worker_elapsed_seconds']={f:m['elapsed_seconds'] for f,m in zip(families,ms)};merged['elapsed_seconds']=max(m['elapsed_seconds'] for m in ms);merged['elapsed_note']='maximum worker duration, not total end-to-end wall time; excludes earlier cached computation';merged['parallel_workers']=4
(O/'manifest.json').write_text(json.dumps(merged,indent=2));print('All four family manifests merged')
