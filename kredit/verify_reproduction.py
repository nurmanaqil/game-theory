"""Verify historical results in an isolated output folder; never overwrite originals."""
from pathlib import Path
import os,sys,json,time,hashlib,platform
BASE=Path(__file__).resolve().parent
OUT=BASE/'reproduction'/'20261023'
OUT.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(OUT/'mpl_cache')
(OUT/'mpl_cache').mkdir(exist_ok=True)
import numpy as np
import pandas as pd
import sklearn,shap,scipy,joblib
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import average_precision_score,roc_auc_score,accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,precision_recall_curve
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import spearmanr,kendalltau
checks={};timing={};start=time.perf_counter()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,passed,detail=None):
 checks[name]={'passed':bool(passed),'detail':detail}
 print(name, 'PASS' if passed else 'FAIL',flush=True)
 assert passed,name
# Hash old experiment artifacts before reading anything.
protected={str(p.relative_to(BASE)):digest(p) for folder in ['raw','processed','artifacts','modeling','treeshap'] for p in (BASE/folder).rglob('*') if p.is_file()}
try:
 raw=pd.read_csv(BASE/'raw/UCI_Credit_Card.csv');target='default.payment.next.month'
 check('raw_checksum',digest(BASE/'raw/UCI_Credit_Card.csv')==json.loads((BASE/'raw/manifest.json').read_text())['sha256'])
 recorded=json.loads((BASE/'artifacts/artifact_checksums.json').read_text())
 check('preprocessing_file_checksums',all(digest(BASE/k)==v for k,v in recorded.items()),len(recorded))
 X=raw.drop(columns=['ID',target]).copy();X.loc[X.EDUCATION.isin([0,5,6]),'EDUCATION']=0
 groups=X.groupby(X.columns.tolist(),sort=True,dropna=False).ngroup();fold=np.full(len(X),-1)
 for k,(_,idx) in enumerate(StratifiedGroupKFold(n_splits=5,shuffle=True,random_state=20261020).split(X,raw[target],groups)):fold[idx]=k
 pre=joblib.load(BASE/'artifacts/preprocessor.joblib');tr=json.loads((BASE/'modeling/selected_threshold.json').read_text())
 data={}
 for name,mask in [('train',fold>=2),('validation',fold==1),('test',fold==0)]:
  idx=np.flatnonzero(mask);meta=pd.read_csv(BASE/f'processed/metadata/metadata_{name}.csv')
  check(name+'_split_membership',np.array_equal(idx,meta.raw_row_index_0based))
  ex=pd.read_csv(BASE/f'processed/encoded/X_{name}.csv');y=pd.read_csv(BASE/f'processed/encoded/y_{name}.csv').squeeze('columns')
  check(name+'_encoding',np.allclose(pre.transform(X.iloc[idx]),ex,rtol=0,atol=1e-9))
  check(name+'_labels',np.array_equal(raw[target].iloc[idx],y))
  data[name]=(ex,y)
 from sklearn.base import clone
 fitted_pre=clone(pre).fit(pd.read_csv(BASE/'processed/semantic/X_train.csv'))
 for name in ['train','validation','test']:
  semantic=pd.read_csv(BASE/f'processed/semantic/X_{name}.csv')
  check(name+'_encoder_refit',np.allclose(fitted_pre.transform(semantic),data[name][0],rtol=0,atol=1e-9) and list(fitted_pre.get_feature_names_out())==list(data[name][0].columns))
 joblib.dump(fitted_pre,OUT/'refitted_preprocessor.joblib')
 model=joblib.load(BASE/'modeling/selected_rf.joblib');config=json.loads((BASE/'modeling/selected_rf_config.json').read_text())
 check('model_checksum',digest(BASE/'modeling/selected_rf.joblib')==tr['model_sha256'])
 for name in ['validation','test']:
  ex,y=data[name];prob=model.predict_proba(ex)[:,list(model.classes_).index(1)]
  saved=pd.read_csv(BASE/f'modeling/predictions_{name}.csv')
  check(name+'_probabilities',np.allclose(prob,saved.probability_default,rtol=1e-7,atol=1e-9),float(np.max(np.abs(prob-saved.probability_default))))
  pd.DataFrame({'probability_default':prob}).to_csv(OUT/f'predictions_{name}.csv',index=False)
  if name=='validation':
   p,r,thresholds=precision_recall_curve(y,prob);f=np.divide(2*p[:-1]*r[:-1],p[:-1]+r[:-1],out=np.zeros_like(thresholds),where=(p[:-1]+r[:-1])!=0)
   chosen=thresholds[np.flatnonzero(f==f.max())[-1]]
   check('selected_threshold',np.isclose(chosen,tr['threshold'],rtol=0,atol=1e-12),float(chosen))
  else:
   original=pd.read_csv(BASE/'modeling/test_metrics.csv')
   for i,thr in enumerate([.5,tr['threshold']]):
    pred=prob>=thr
    actual=[accuracy_score(y,pred),precision_score(y,pred),recall_score(y,pred),f1_score(y,pred),roc_auc_score(y,prob),average_precision_score(y,prob)]
    check('test_metrics_'+str(i),np.allclose(actual,original.iloc[i][['Accuracy','Precision','Recall','F1','ROC_AUC','Average_precision']].astype(float),atol=1e-12,rtol=0))
    check('test_confusion_'+str(i),np.array_equal(confusion_matrix(y,pred).ravel(),original.iloc[i][['TN','FP','FN','TP']].astype(int)))
 t=time.perf_counter();refit=RandomForestClassifier(**config['parameters']);refit.fit(*data['train']);timing['refit_seconds']=time.perf_counter()-t
 refit_prob=refit.predict_proba(data['test'][0])[:,1];ref_prob=model.predict_proba(data['test'][0])[:,1]
 check('selected_forest_refit_predictions',np.allclose(refit_prob,ref_prob,rtol=1e-7,atol=1e-9),float(np.max(np.abs(refit_prob-ref_prob))))
 joblib.dump(refit,OUT/'refitted_rf.joblib')
 train=data['train'][0];test=data['test'][0]
 manifest=json.loads((BASE/'treeshap/main/main_manifest.json').read_text())
 idx=np.sort(np.random.default_rng(20261022).choice(len(test),1000,replace=False));sample=test.iloc[idx]
 check('explanation_membership',np.array_equal(idx,manifest['evaluation_rows']))
 check('explanation_inputs',np.allclose(sample,pd.read_csv(BASE/'treeshap/main/X_explanation_sample.csv'),rtol=0,atol=1e-9))
 prob=model.predict_proba(sample)[:,1];values={}
 for seed in [20261021,20261023,20261024]:
  bgidx=np.sort(np.random.default_rng(seed).choice(len(train),100,replace=False));bg=train.iloc[bgidx]
  modes=['interventional','tree_path_dependent'] if seed==20261021 else ['interventional']
  for mode in modes:
   print('Computing',mode,'background',seed,flush=True);t=time.perf_counter()
   exp=shap.TreeExplainer(model,data=bg if mode=='interventional' else None,feature_perturbation=mode,model_output='raw')
   phi=np.asarray(exp.shap_values(sample,approximate=False,check_additivity=True))[:,:,1];baseline=float(np.asarray(exp.expected_value)[1])
   timing[f'{mode}_{seed}_seconds']=time.perf_counter()-t
   old=(BASE/f'treeshap/main/shap_{mode}.npz') if seed==20261021 else BASE/f'treeshap/background_check/shap_interventional_{seed}.npz'
   with np.load(old,allow_pickle=False) as z:
    check(f'{mode}_{seed}_attributions',np.allclose(phi,z['values'],rtol=1e-7,atol=1e-9),float(np.max(np.abs(phi-z['values']))))
    check(f'{mode}_{seed}_baseline',np.isclose(baseline,float(z['baseline']),rtol=0,atol=1e-10))
   check(f'{mode}_{seed}_additivity',np.max(np.abs(phi.sum(axis=1)+baseline-prob))<=1e-6)
   np.savez_compressed(OUT/f'shap_{mode}_{seed}.npz',values=phi,baseline=baseline,test_row_indices=idx)
   values[(mode,seed)]=phi
 bills=[sample.columns.get_loc('BILL_AMT'+str(i)) for i in range(1,7)]
 rows=[]
 for seed in [20261021,20261023,20261024]:
  a=values[('interventional',seed)][:,bills];b=values[('tree_path_dependent',20261021)][:,bills]
  valid=(np.isclose(abs(a),abs(a).max(axis=1,keepdims=True),atol=1e-12,rtol=0).sum(axis=1)==1)&(np.isclose(abs(b),abs(b).max(axis=1,keepdims=True),atol=1e-12,rtol=0).sum(axis=1)==1)
  n=int(((abs(a).argmax(axis=1)!=abs(b).argmax(axis=1))&valid).sum());rho=float(spearmanr(abs(a).mean(axis=0),abs(b).mean(axis=0)).statistic)
  old=pd.read_csv(BASE/'treeshap/background_check/background_comparison.csv').set_index('background_seed').loc[seed]
  check('background_summary_'+str(seed),n==old.n_disagreement_vs_path and np.isclose(rho,old.spearman_vs_path))
  rows.append({'background_seed':seed,'disagreement_count':n,'spearman':rho})
 pd.DataFrame(rows).to_csv(OUT/'background_summary.csv',index=False)
finally:
 unchanged=all(digest(BASE/k)==v for k,v in protected.items());checks['historical_artifacts_unchanged']={'passed':unchanged,'detail':len(protected)}
 report={'status':'PASS' if checks and all(c['passed'] for c in checks.values()) and len(checks)>30 else 'INCOMPLETE_OR_FAILED','versions':{m.__name__:m.__version__ for m in [np,pd,sklearn,scipy,shap,joblib]},'python':platform.python_version(),'python_executable':sys.executable,'dependency_strategy':'new local venv, reused copied cp314 site-packages via .pth; no pip install','checks':checks,'timing':timing,'elapsed_seconds':time.perf_counter()-start,'scope':'recomputed split; loaded preprocessor transform; saved model predictions; threshold and test metrics; refit selected RF only; full main SHAP and two extra backgrounds. Encoder refit train-only is checked on subsequent runs; initial run has separate encoder_refit_report.json. No full candidate search.'}
 (OUT/'verification_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({'status':report['status'],'elapsed':report['elapsed_seconds'],'checks':len(checks),'output':str(OUT)},indent=2),flush=True)
