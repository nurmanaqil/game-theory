"""Revision experiment. Outputs isolated; validation-only selection; paired raw-output SHAP."""
from pathlib import Path
import os,sys,json,time,hashlib,platform
B=Path(__file__).resolve().parent;O=B/'experiments/revision_v1';O.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(O/'mpl_cache');(O/'mpl_cache').mkdir(exist_ok=True)
sys.path.insert(0,str(B/'.extension_deps'))
import numpy as np,pandas as pd,joblib,sklearn,shap,scipy,xgboost
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier,GradientBoostingClassifier
from sklearn.metrics import average_precision_score,roc_auc_score,precision_recall_curve,accuracy_score,precision_score,recall_score,f1_score,brier_score_loss,log_loss,confusion_matrix
from scipy.stats import spearmanr,kendalltau
START=time.perf_counter();timings=[]
WORKER=sys.argv[1] if len(sys.argv)>1 else None
if WORKER:
 assert WORKER in ['random_forest','extra_trees','gradient_boosting','xgboost']
 (O/WORKER/'worker_tables').mkdir(parents=True,exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def savejson(p,d):p.write_text(json.dumps(d,indent=2,allow_nan=False),encoding='utf-8')
def clean(x):return None if not np.isfinite(x) else float(x)
def write_table(rows,p):
 if WORKER and p.parent==O:p=O/WORKER/'worker_tables'/p.name
 pd.DataFrame(rows).to_csv(p,index=False)
def say(*s):print(*s,flush=True)
protected={str(p.relative_to(B)):digest(p) for d in ['raw','processed','artifacts','modeling','treeshap'] for p in (B/d).rglob('*') if p.is_file()}
D={s:(pd.read_csv(B/f'processed/encoded/X_{s}.csv'),pd.read_csv(B/f'processed/encoded/y_{s}.csv').squeeze('columns')) for s in ['train','validation','test']}
features=list(D['train'][0].columns);assert all(list(x.columns)==features for x,y in D.values())
MAP=pd.read_csv(B/'artifacts/feature_map.csv');assert list(MAP.encoded_feature)==features
sources=list(dict.fromkeys(MAP.source_feature));groups={g:[features.index(f'{g}{i}') for i in range(1,7)] for g in ['BILL_AMT','PAY_AMT']}
seeds=[42,17,73];bgseeds=[20261021,20261023,20261024]
idx=np.sort(np.random.default_rng(20261022).choice(len(D['test'][0]),1000,replace=False));S=D['test'][0].iloc[idx]
assert np.allclose(S,pd.read_csv(B/'treeshap/main/X_explanation_sample.csv'))
if not (O/'evaluation_membership.csv').exists():pd.read_csv(B/'treeshap/main/evaluation_membership.csv').to_csv(O/'evaluation_membership.csv',index=False)
backgrounds={s:D['train'][0].iloc[np.sort(np.random.default_rng(s).choice(len(D['train'][0]),100,replace=False))] for s in bgseeds}
for s,bg in backgrounds.items():
 if not (O/f'background_{s}.csv').exists():bg.to_csv(O/f'background_{s}.csv',index=False)
# Only train data define correlation summaries.
cr=[]
for g in groups:
 cols=[f'{g}{i}' for i in range(1,7)]
 for method in ['pearson','spearman']:
  c=D['train'][0][cols].corr(method=method);
  if not (O/f'{g}_{method}_train.csv').exists():c.to_csv(O/f'{g}_{method}_train.csv')
  v=c.values[np.triu_indices(6,1)]
  cr.append({'group':g,'method':method,'min':v.min(),'max':v.max(),'mean':v.mean()})
write_table(cr,O/'correlation_summary.csv')

def candidate_specs(fam):
 if fam in ['random_forest','extra_trees']:
  return [dict(n_estimators=300,max_depth=d,min_samples_leaf=5,max_features='sqrt',bootstrap=fam=='random_forest',n_jobs=2) for d in [8,12,None]]
 if fam=='gradient_boosting':return [dict(n_estimators=200,learning_rate=.05,min_samples_leaf=5,max_depth=d,subsample=1.) for d in [2,3,4]]
 return [dict(n_estimators=300,learning_rate=.05,max_depth=d,subsample=.8,colsample_bytree=.8,reg_lambda=1.,objective='binary:logistic',eval_metric='logloss',tree_method='hist',n_jobs=2) for d in [2,3,4]]
def make(fam,params,seed):
 cls={'random_forest':RandomForestClassifier,'extra_trees':ExtraTreesClassifier,'gradient_boosting':GradientBoostingClassifier,'xgboost':xgboost.XGBClassifier}[fam]
 return cls(random_state=seed,**params)
def raw_predict(model,fam,x):
 if fam in ['random_forest','extra_trees']:return model.predict_proba(x)[:,list(model.classes_).index(1)]
 if fam=='gradient_boosting':return model.decision_function(x)
 return model.predict(x,output_margin=True)
def threshold(y,p):
 pr,re,th=precision_recall_curve(y,p);den=pr[:-1]+re[:-1];f=np.divide(2*pr[:-1]*re[:-1],den,out=np.zeros_like(th),where=den!=0);return float(th[np.flatnonzero(f==f.max())[-1]])
def explain(model,fam,x,mode,bg):
 expl=shap.TreeExplainer(model,data=bg if mode=='interventional' else None,feature_perturbation=mode,model_output='raw')
 v=np.asarray(expl.shap_values(x,approximate=False,check_additivity=True));base=np.asarray(expl.expected_value)
 if v.ndim==3:pos=list(model.classes_).index(1);v=v[:,:,pos];base=float(base[pos])
 else:base=float(base.reshape(-1)[0])
 assert v.shape==x.shape and np.isfinite(v).all()
 error=float(np.max(abs(v.sum(axis=1)+base-raw_predict(model,fam,x))));assert error<=(1e-5 if fam=='xgboost' else 1e-6),(fam,mode,error)
 if mode=='interventional':assert expl.data.shape[0]==100
 return v,base,error

families=[WORKER] if WORKER else ['random_forest','extra_trees','gradient_boosting','xgboost'];selection=[];metrics=[];pilot=[];summary=[];feature_rows=[];source_rows=[];locals_all=[]
for fam in families:
 folder=O/fam;folder.mkdir(exist_ok=True);best=None
 for ci,params in enumerate(candidate_specs(fam)):
  cp=folder/f'candidate_{ci}.joblib';t=time.perf_counter()
  if cp.exists():model=joblib.load(cp)
  else:model=make(fam,params,42);model.fit(*D['train']);joblib.dump(model,cp)
  pv=model.predict_proba(D['validation'][0])[:,1];ap=float(average_precision_score(D['validation'][1],pv))
  selection.append({'family':fam,'candidate':ci,'validation_AP':ap,'validation_ROC_AUC':roc_auc_score(D['validation'][1],pv),'parameters':json.dumps(params),'seconds_fit_or_load':time.perf_counter()-t})
  say('CANDIDATE',fam,ci,'AP',ap)
  if best is None or ap>best[0]:best=(ap,ci,params,model)
  write_table(selection,O/'selection_validation.csv')
 ap,ci,params,selected=best;savejson(folder/'selection.json',{'family':fam,'candidate':ci,'parameters':params,'validation_AP':ap,'selection_seed':42,'criterion':'highest validation AP; exact tie lower candidate index'})
 for seed in seeds:
  run=folder/f'seed_{seed}';run.mkdir(exist_ok=True);mp=run/'model.joblib';t=time.perf_counter()
  if mp.exists():model=joblib.load(mp)
  else:
   model=selected if seed==42 else make(fam,params,seed)
   if seed!=42:model.fit(*D['train'])
   joblib.dump(model,mp)
  timings.append({'family':fam,'seed':seed,'operation':'fit_or_load_selected','seconds':time.perf_counter()-t})
  pv=model.predict_proba(D['validation'][0])[:,1];thr=threshold(D['validation'][1],pv)
  savejson(run/'model_manifest.json',{'family':fam,'seed':seed,'selected_params':params,'threshold':thr,'model_sha256':digest(mp),'feature_order':features,'raw_units':'probability' if fam in ['random_forest','extra_trees'] else 'log_odds_margin','tuned_on_test':False,'additivity_atol':1e-5 if fam=='xgboost' else 1e-6})
  for split in ['validation','test']:
   x,y=D[split];pr=model.predict_proba(x)[:,1]
   pd.DataFrame({'y_true':y,'probability_default':pr,'prediction_selected':pr>=thr}).to_csv(run/f'predictions_{split}.csv',index=False)
   for label,tval in [('default',.5),('validation_f1',thr)]:
    pred=pr>=tval;tn,fp,fn,tp=confusion_matrix(y,pred).ravel()
    metrics.append({'family':fam,'seed':seed,'split':split,'threshold_rule':label,'threshold':tval,'AP':average_precision_score(y,pr),'ROC_AUC':roc_auc_score(y,pr),'Brier':brier_score_loss(y,pr),'log_loss':log_loss(y,pr),'accuracy':accuracy_score(y,pred),'precision':precision_score(y,pred,zero_division=0),'recall':recall_score(y,pred),'F1':f1_score(y,pred),'TN':tn,'FP':fp,'FN':fn,'TP':tp})
  write_table(metrics,O/'predictive_metrics.csv')
  # Technical pilot uses same first 20 fixed sample rows, no outcome selection.
  for mode in ['interventional','tree_path_dependent']:
   t=time.perf_counter();v,base,err=explain(model,fam,S.iloc[:20],mode,backgrounds[bgseeds[0]])
   pilot.append({'family':fam,'seed':seed,'mode':mode,'n':20,'error':err,'atol':1e-5 if fam=='xgboost' else 1e-6,'seconds':time.perf_counter()-t})
  write_table(pilot,O/'pilot_checks.csv')
  computed={};settings=[('tree_path_dependent',0)]+[('interventional',s) for s in (bgseeds if seed==42 else bgseeds[:1])]
  for mode,bs in settings:
   file=run/f'shap_{mode}_{bs}.npz';t=time.perf_counter()
   if file.exists():
    with np.load(file,allow_pickle=False) as z:v=z['values'];base=float(z['baseline']);assert np.array_equal(z['test_row_indices'],idx) and np.array_equal(z['feature_names'],np.array(features))
    err=float(np.max(abs(v.sum(axis=1)+base-raw_predict(model,fam,S))));assert err<=(1e-5 if fam=='xgboost' else 1e-6)
   else:
    say('SHAP START',fam,seed,mode,bs);v,base,err=explain(model,fam,S,mode,backgrounds[bs] if bs else None)
    np.savez_compressed(file,values=v,baseline=base,test_row_indices=idx,feature_names=np.array(features))
   elapsed=time.perf_counter()-t;timings.append({'family':fam,'seed':seed,'operation':f'{mode}_{bs}','seconds':elapsed});computed[(mode,bs)]=(v,base)
   say('SHAP PASS',fam,seed,mode,bs,'seconds',round(elapsed,1),'error',err)
   for src in sources:
    inds=np.flatnonzero(MAP.source_feature.to_numpy()==src);source_rows.append({'family':fam,'seed':seed,'mode':mode,'background_seed':bs,'source_feature':src,'mean_abs_shap':float(abs(v[:,inds].sum(axis=1)).mean())})
  path,pbase=computed[('tree_path_dependent',0)];raw=raw_predict(model,fam,S);normalizer=float(abs(raw-pbase).mean())
  for bs in (bgseeds if seed==42 else bgseeds[:1]):
   inter,ibase=computed[('interventional',bs)]
   for group,positions in groups.items():
    a,b=inter[:,positions],path[:,positions];aa,bb=abs(a),abs(b)
    topa=aa.argmax(axis=1);topb=bb.argmax(axis=1)
    valid=(np.isclose(aa,aa.max(axis=1,keepdims=True),atol=1e-12,rtol=0).sum(axis=1)==1)&(np.isclose(bb,bb.max(axis=1,keepdims=True),atol=1e-12,rtol=0).sum(axis=1)==1)
    def margin(x):
     s=np.sort(x,axis=1);den=s[:,-1]+s[:,-2];return np.divide(s[:,-1]-s[:,-2],den,out=np.zeros(len(x)),where=den>1e-12)
    ma,mb=margin(aa),margin(bb);different=topa!=topb
    l1=abs(a-b).sum(axis=1);gs=abs(a.sum(axis=1)-b.sum(axis=1))
    rho=clean(spearmanr(aa.mean(axis=0),bb.mean(axis=0)).statistic);tau=clean(kendalltau(aa.mean(axis=0),bb.mean(axis=0)).statistic)
    for cutoff in [0.,.01,.05,.1]:
     subset=valid if cutoff==0 else valid&(ma>cutoff)&(mb>cutoff);nv=int(subset.sum());nd=int((different&subset).sum())
     summary.append({'family':fam,'seed':seed,'background_seed':bs,'group':group,'margin_cutoff':cutoff,'units':'probability' if fam in ['random_forest','extra_trees'] else 'log_odds_margin','n_valid':nv,'n_disagreement':nd,'disagreement_rate':nd/nv if nv else None,'spearman':rho,'kendall_tau':tau,'baseline_interventional':ibase,'baseline_path':pbase,'mean_L1_difference':float(l1.mean()),'mean_absolute_group_sum_difference':float(gs.mean()),'relative_L1':float(l1.mean()/normalizer) if normalizer>1e-12 else None,'normalizer_path_centered_output':normalizer,'median_winner_margin_interventional':float(np.median(ma)),'median_winner_margin_path':float(np.median(mb))})
    ranksa=pd.Series(aa.mean(axis=0)).rank(ascending=False);ranksb=pd.Series(bb.mean(axis=0)).rank(ascending=False)
    for j,pos in enumerate(positions):feature_rows.append({'family':fam,'seed':seed,'background_seed':bs,'group':group,'feature':features[pos],'mean_abs_interventional':float(aa[:,j].mean()),'mean_abs_path':float(bb[:,j].mean()),'rank_interventional':float(ranksa[j]),'rank_path':float(ranksb[j]),'mean_abs_difference':float(abs(a[:,j]-b[:,j]).mean())})
    local=pd.DataFrame({'test_row_index':idx,'family':fam,'seed':seed,'background_seed':bs,'group':group,'unique_top_both':valid,'disagreement':different,'margin_interventional':ma,'margin_path':mb,'L1_difference':l1,'abs_group_difference':gs});local.to_csv(run/f'local_{group}_{bs}.csv',index=False)
  write_table(summary,O/'attribution_summary.csv');write_table(feature_rows,O/'feature_comparison.csv');write_table(source_rows,O/'source_importance.csv');write_table(timings,O/'timing.csv')
assert all(digest(B/p)==v for p,v in protected.items()),'Historical artifact changed'
versions={m.__name__:m.__version__ for m in [np,pd,sklearn,scipy,shap,xgboost,joblib]}
savejson(O/WORKER/'family_manifest.json' if WORKER else O/'manifest.json',{'status':'PASS','python':platform.python_version(),'versions':versions,'protocol_sha256':digest(O/'protocol.md'),'script_sha256':digest(Path(__file__)),'historical_files_unchanged':len(protected),'elapsed_seconds':time.perf_counter()-START,'families':families,'seeds':seeds,'background_seeds':bgseeds,'evaluation_rows':idx.tolist(),'n_tuning_candidates_per_family':3,'prior_test_exposure':True,'source_features':sources})
say('ALL EXPERIMENTS PASS',round(time.perf_counter()-START,1))
