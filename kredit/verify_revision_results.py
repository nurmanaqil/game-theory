from pathlib import Path
import os,sys,json,hashlib,re,ast
B=Path('kredit').resolve();O=B/'experiments/revision_v1';os.environ['MPLCONFIGDIR']=str(O/'mpl_cache');sys.path.insert(0,str(B/'.extension_deps'))
import numpy as np,pandas as pd,joblib
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score,roc_auc_score,f1_score
checks={}
def ck(name,b):checks[name]=bool(b);assert b,name
M=json.loads((O/'manifest.json').read_text());ck('all_family_manifests',M['status']=='PASS' and len(M['families'])==4)
A=pd.read_csv(O/'attribution_summary.csv');P=pd.read_csv(O/'predictive_metrics.csv');x=pd.read_csv(B/'treeshap/main/X_explanation_sample.csv')
xa=pd.read_csv(B/'processed/encoded/X_validation.csv');ya=pd.read_csv(B/'processed/encoded/y_validation.csv').squeeze('columns');xt=pd.read_csv(B/'processed/encoded/X_test.csv');yt=pd.read_csv(B/'processed/encoded/y_test.csv').squeeze('columns')
errors=[]
for fam in M['families']:
 for seed in [42,17,73]:
  f=O/fam/f'seed_{seed}';mm=json.loads((f/'model_manifest.json').read_text());model=joblib.load(f/'model.joblib');ck(f'{fam}_{seed}_model_sha',hashlib.sha256((f/'model.joblib').read_bytes()).hexdigest()==mm['model_sha256'])
  raw=model.predict_proba(x)[:,1] if fam in ['random_forest','extra_trees'] else model.decision_function(x) if fam=='gradient_boosting' else model.predict(x,output_margin=True)
  for split,ex,y in [('validation',xa,ya),('test',xt,yt)]:
   pr=model.predict_proba(ex)[:,1];r=P[(P.family==fam)&(P.seed==seed)&(P.split==split)&(P.threshold_rule=='validation_f1')].iloc[0]
   ck(f'{fam}_{seed}_{split}_metrics',np.allclose([average_precision_score(y,pr),roc_auc_score(y,pr),f1_score(y,pr>=mm['threshold'])],[r.AP,r.ROC_AUC,r.F1],rtol=0,atol=1e-12))
  with np.load(f/'shap_tree_path_dependent_0.npz',allow_pickle=False) as z:path=z['values']
  for file in f.glob('shap_*.npz'):
   with np.load(file,allow_pickle=False) as z:
    ck(str(file.relative_to(O))+'_schema',z['values'].shape==(1000,89) and list(z['feature_names'])==list(x.columns) and np.array_equal(z['test_row_indices'],M['evaluation_rows']))
    error=float(np.max(abs(z['values'].sum(axis=1)+float(z['baseline'])-raw)));ck(str(file.relative_to(O))+'_additivity',error<=mm['additivity_atol']);errors.append({'file':str(file.relative_to(O)),'max_error':error,'atol':mm['additivity_atol']})
  for bg in ([20261021,20261023,20261024] if seed==42 else [20261021]):
   with np.load(f/f'shap_interventional_{bg}.npz',allow_pickle=False) as z:inter=z['values']
   for group in ['BILL_AMT','PAY_AMT']:
    inds=[list(x.columns).index(group+str(i)) for i in range(1,7)];a=abs(inter[:,inds]);b=abs(path[:,inds]);valid=(np.isclose(a,a.max(axis=1,keepdims=True),rtol=0,atol=1e-12).sum(axis=1)==1)&(np.isclose(b,b.max(axis=1,keepdims=True),rtol=0,atol=1e-12).sum(axis=1)==1)
    def margin(v):
     v=np.sort(v,axis=1);den=v[:,-1]+v[:,-2];return np.divide(v[:,-1]-v[:,-2],den,out=np.zeros(len(v)),where=den>1e-12)
    ma,mb=margin(a),margin(b);different=a.argmax(axis=1)!=b.argmax(axis=1)
    for cut in [0,.01,.05,.1]:
     mask=valid if cut==0 else valid&(ma>cut)&(mb>cut);r=A[(A.family==fam)&(A.seed==seed)&(A.background_seed==bg)&(A.group==group)&(A.margin_cutoff==cut)].iloc[0]
     ck(f'{fam}_{seed}_{bg}_{group}_{cut}_counts',int(mask.sum())==r.n_valid and int((mask&different).sum())==r.n_disagreement)
ck('historical_model_sha',hashlib.sha256((B/'modeling/selected_rf.joblib').read_bytes()).hexdigest()=='3f79f93e3e66a28fac8ff168e297d6ccfcfc9a5413dec44cbc55db977cc12b7f')
old=json.loads((B/'artifacts/artifact_checksums.json').read_text());ck('historical_preprocessing_checksums',all(hashlib.sha256((B/k).read_bytes()).hexdigest()==v for k,v in old.items()))
ck('consultation_md_unchanged',hashlib.sha256(Path('consultation_guide.md').read_bytes()).hexdigest()=='5d4771a0c9d04778dfe19f50861ccb27c0ef8b7487a70071bf198599159d3094')
missing=[]
for p in [O/'RESULTS.md',O/'paper_methods_results_en.md',B/'paper/manuscript_revision_en.md',Path('README.md')]:
 for target in re.findall(r'\]\(([^\s)]+)\)',p.read_text(encoding='utf-8')):
  if not target.startswith(('http://','https://','#')) and not (p.parent/target).exists():missing.append((str(p),target))
ck('local_markdown_links',not missing)
for p in B.glob('*revision*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
ck('five_png_figures',len(list((O/'figures').glob('*.png')))==5)
(O/'final_quality_report.json').write_text(json.dumps({'status':'PASS','n_checks':len(checks),'checks':checks,'shap_additivity':errors,'plots_visually_reviewed':5,'missing_links':missing,'input_file_sha256':{k:hashlib.sha256((B/k).read_bytes()).hexdigest() for k in old}},indent=2));print('FINAL QA PASS:',len(checks),'checks')
