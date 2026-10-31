# Precompute independent validation candidates while SHAP for the first family runs.
from pathlib import Path
import ast,sys,time,os,json
B=Path('kredit').resolve();O=B/'experiments/revision_v1';os.environ['MPLCONFIGDIR']=str(O/'mpl_cache');sys.path.insert(0,str(B/'.extension_deps'))
import pandas as pd,joblib,xgboost
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier,GradientBoostingClassifier
source=ast.parse((B/'run_revision_experiments.py').read_text(encoding='utf-8-sig'))
for node in source.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['candidate_specs','make']:exec(compile(ast.Module(body=[node],type_ignores=[]),'candidate_specs','exec'))
x=pd.read_csv(B/'processed/encoded/X_train.csv');y=pd.read_csv(B/'processed/encoded/y_train.csv').squeeze('columns');times=[]
for fam in ['extra_trees','gradient_boosting','xgboost']:
 f=O/fam;f.mkdir(exist_ok=True)
 for i,p in enumerate(candidate_specs(fam)):
  path=f/f'candidate_{i}.joblib'
  if path.exists():continue
  t=time.perf_counter();m=make(fam,p,42);m.fit(x,y);tmp=f/f'candidate_{i}.partial';joblib.dump(m,tmp);tmp.replace(path)
  times.append({'family':fam,'candidate':i,'fit_seconds':time.perf_counter()-t});print(times[-1],flush=True)
  (O/'prefit_timing.json').write_text(json.dumps(times,indent=2))
