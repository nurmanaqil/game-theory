from pathlib import Path
import subprocess,sys,time,json
B=Path('kredit').resolve();O=B/'experiments/revision_v1';families=['random_forest','extra_trees','gradient_boosting','xgboost']
expected=[]
for seed in [42,17,73]:
 expected.append(O/f'extra_trees/seed_{seed}/shap_tree_path_dependent_0.npz')
 for bg in ([20261021,20261023,20261024] if seed==42 else [20261021]):expected.append(O/f'extra_trees/seed_{seed}/shap_interventional_{bg}.npz')
start=time.monotonic()
while not all(p.exists() for p in expected):
 if time.monotonic()-start>1800:raise TimeoutError('Extra Trees checkpoints incomplete after bounded wait')
 print('Waiting for ET checkpoints',sum(p.exists() for p in expected),'/',len(expected),flush=True);time.sleep(20)
for name,args in [('extra_trees_finalize',['run_revision_experiments.py','extra_trees']),('merge',['merge_revision_experiments.py']),('analysis',['analyze_revision_experiments.py']),('manuscript',['write_revision_sections.py'])]:
 print('STAGE',name,flush=True)
 with (O/f'{name}_final.log').open('w',encoding='utf-8') as log:subprocess.run([sys.executable,str(B/args[0]),*args[1:]],check=True,stdout=log,stderr=subprocess.STDOUT)
checks=json.loads((O/'analysis_checks.json').read_text());assert checks['status']=='PASS'
(O/'completion.json').write_text(json.dumps({'status':'PASS','analysis':checks,'local_manuscript':str(B/'paper/manuscript_revision_en.md'),'google_docs_modified':False},indent=2));print('REVISION COMPLETE',flush=True)
