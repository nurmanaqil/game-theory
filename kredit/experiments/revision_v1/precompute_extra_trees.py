from pathlib import Path
import os,sys,json,time
B=Path('kredit').resolve();O=B/'experiments/revision_v1';seed=int(sys.argv[1]);assert seed in [42,17,73]
os.environ['MPLCONFIGDIR']=str(O/'mpl_cache')
import pandas as pd,numpy as np,joblib,shap
from sklearn.ensemble import ExtraTreesClassifier
params=json.loads((O/'extra_trees/selection.json').read_text())['parameters'];folder=O/f'extra_trees/seed_{seed}';folder.mkdir(exist_ok=True)
x=pd.read_csv(B/'processed/encoded/X_train.csv');y=pd.read_csv(B/'processed/encoded/y_train.csv').squeeze('columns');test=pd.read_csv(B/'processed/encoded/X_test.csv');idx=np.sort(np.random.default_rng(20261022).choice(len(test),1000,replace=False));s=test.iloc[idx];bg=pd.read_csv(O/'background_20261021.csv');mp=folder/'model.joblib'
if mp.exists():m=joblib.load(mp)
else:
 m=ExtraTreesClassifier(random_state=seed,**params);m.fit(x,y);temp=folder/'model.partial';joblib.dump(m,temp);temp.replace(mp)
records=[]
settings=[('interventional',int(sys.argv[2]))] if len(sys.argv)>2 else [('tree_path_dependent',0),('interventional',20261021)]
for mode,bs in settings:
 file=folder/f'shap_{mode}_{bs}.npz'
 if file.exists():continue
 if bs:bg=pd.read_csv(O/f'background_{bs}.csv')
 print('START',seed,mode,bs,flush=True);t=time.perf_counter();e=shap.TreeExplainer(m,data=bg if bs else None,feature_perturbation=mode,model_output='raw');v=np.asarray(e.shap_values(s,approximate=False,check_additivity=True))[:,:,1];base=float(np.asarray(e.expected_value)[1]);error=float(np.max(abs(v.sum(axis=1)+base-m.predict_proba(s)[:,1])));assert error<=1e-6
 temp=file.with_suffix('.partial.npz');np.savez_compressed(temp,values=v,baseline=base,test_row_indices=idx,feature_names=np.asarray(list(s.columns),dtype=str));temp.replace(file)
 records.append({'seed':seed,'mode':mode,'seconds':time.perf_counter()-t,'error':error});print(records[-1],flush=True);(folder/f'precompute_timing_{sys.argv[2] if len(sys.argv)>2 else seed}.json').write_text(json.dumps(records,indent=2))
print('PRECOMPUTE PASS',seed,flush=True)
