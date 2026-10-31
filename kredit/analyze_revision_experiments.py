"""Build revision tables, scientific figures, and local report after experiments finish."""
from pathlib import Path
import os,json,hashlib
B=Path(__file__).resolve().parent;O=B/'experiments/revision_v1';F=O/'figures';F.mkdir(exist_ok=True)
os.environ['MPLCONFIGDIR']=str(O/'mpl_cache')
import numpy as np,pandas as pd
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
m=json.loads((O/'manifest.json').read_text());assert m['status']=='PASS'
A=pd.read_csv(O/'attribution_summary.csv');P=pd.read_csv(O/'predictive_metrics.csv');C=pd.read_csv(O/'feature_comparison.csv');I=pd.read_csv(O/'source_importance.csv')
labels={'random_forest':'Random Forest','extra_trees':'Extra Trees','gradient_boosting':'Gradient Boosting','xgboost':'XGBoost'};families=list(labels)
plt.rcParams.update({'font.family':'Times New Roman','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':120})
def save(fig,name):
 fig.tight_layout();fig.savefig(F/(name+'.png'),dpi=220,bbox_inches='tight');fig.savefig(F/(name+'.pdf'),bbox_inches='tight');plt.close(fig)
def table(df):
 head='| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'
 return head+'\n'.join('| '+' | '.join('NA' if pd.isna(v) else f'{v:.4f}' if isinstance(v,(float,np.floating)) else str(v) for v in row)+' |' for row in df.itertuples(index=False,name=None))+'\n'
# Selected model performance, selection uses validation only.
primary=P[(P.seed==42)&(P.threshold_rule=='validation_f1')]
test=primary[primary.split=='test'].set_index('family');val=primary[primary.split=='validation'].set_index('family');winner=val.AP.idxmax()
fig,ax=plt.subplots(figsize=(8,4.5));x=np.arange(4);ax.bar(x-.18,val.loc[families,'AP'],.36,color='.3',label='Validation');ax.bar(x+.18,test.loc[families,'AP'],.36,color='.75',edgecolor='black',label='Test');ax.set_xticks(x,[labels[f] for f in families],rotation=12);ax.set_ylabel('Average precision');ax.set_ylim(0,.68);ax.legend(frameon=False,loc='upper left',ncol=2,fontsize=11);save(fig,'predictive_ap')
perf=pd.DataFrame({'Model':[labels[f] for f in families],'AP validation':[val.loc[f,'AP'] for f in families],'AP test':[test.loc[f,'AP'] for f in families],'ROC-AUC test':[test.loc[f,'ROC_AUC'] for f in families],'F1 test':[test.loc[f,'F1'] for f in families],'Recall test':[test.loc[f,'recall'] for f in families],'Brier test':[test.loc[f,'Brier'] for f in families]});perf.to_csv(O/'paper_predictive_table.csv',index=False)
# Separate axes preserve model-native units.
fig,axes=plt.subplots(2,2,figsize=(10,8))
for fam,ax in zip(families,axes.flat):
 d=C[(C.family==fam)&(C.seed==42)&(C.background_seed==20261021)&(C.group=='BILL_AMT')];xx=np.arange(6);factor=100 if fam in ['random_forest','extra_trees'] else 1
 ax.bar(xx-.19,d.mean_abs_interventional*factor,.38,color='.3',label='Interventional');ax.bar(xx+.19,d.mean_abs_path*factor,.38,color='.75',edgecolor='black',label='Path-dependent');ax.set_xticks(xx,[f'B{i}' for i in range(1,7)]);ax.set_title(labels[fam]);ax.set_ylabel('Probability percentage points' if factor==100 else 'Log-odds margin');ax.legend(frameon=False,fontsize=10)
save(fig,'billing_importance')
main=A[(A.seed==42)&(A.background_seed==20261021)&(A.group=='BILL_AMT')];fig,ax=plt.subplots(figsize=(8,4.5));xx=np.arange(4)
for j,(cutoff,color) in enumerate([(0.,'.3'),(.05,'.75')]):
 d=main[main.margin_cutoff==cutoff].set_index('family').loc[families];ax.bar(xx+(j-.5)*.36,d.disagreement_rate*100,.36,color=color,edgecolor='black',label='All unique maxima' if cutoff==0 else 'Both winner margins > 5%')
 for k,fam in enumerate(families):ax.text(k+(j-.5)*.36,d.loc[fam,'disagreement_rate']*100+.6,f'n={int(d.loc[fam,"n_valid"])}',ha='center',fontsize=8,rotation=0)
ax.set_xticks(xx,[labels[f] for f in families],rotation=12);ax.set_ylabel('Top billing disagreement (%)');ax.legend(frameon=False);save(fig,'winner_margin_disagreement')
fig,axes=plt.subplots(2,2,figsize=(10,7.5))
for fam,ax in zip(families,axes.flat):
 for group,marker,color in [('BILL_AMT','o','.2'),('PAY_AMT','s','.65')]:
  d=A[(A.family==fam)&(A.seed==42)&(A.margin_cutoff==0)&(A.group==group)].sort_values('background_seed');ax.plot(np.arange(len(d)),d.disagreement_rate*100,marker=marker,color=color,label=group)
 ax.set_xticks(range(3),['20261021','20261023','20261024'],rotation=20,fontsize=9);ax.set_title(labels[fam]);ax.set_ylim(0,50);ax.set_ylabel('Top-feature disagreement (%)');ax.legend(frameon=False,fontsize=10)
save(fig,'background_disagreement')
# Seed summaries include checks for effectively identical fitted functions.
seed_rows=[]
for fam in families:
 ref=pd.read_csv(O/f'{fam}/seed_42/predictions_test.csv').probability_default.to_numpy()
 for seed in [42,17,73]:
  pred=pd.read_csv(O/f'{fam}/seed_{seed}/predictions_test.csv').probability_default.to_numpy();d=A[(A.family==fam)&(A.seed==seed)&(A.group=='BILL_AMT')&(A.background_seed==20261021)&(A.margin_cutoff==0)].iloc[0]
  seed_rows.append({'family':fam,'seed':seed,'max_probability_difference_from_seed42':float(abs(pred-ref).max()),'test_predictions_equal_to_seed42_at_1e-12':bool(np.allclose(pred,ref,atol=1e-12,rtol=0)),'billing_disagreement':d.disagreement_rate,'billing_spearman':d.spearman})
seeds=pd.DataFrame(seed_rows);seeds.to_csv(O/'seed_sensitivity.csv',index=False)
robust=main[main.margin_cutoff.isin([0,.05])][['family','margin_cutoff','n_valid','n_disagreement','disagreement_rate']].copy();robust.family=robust.family.map(labels)
q=A[(A.seed==42)&(A.background_seed==20261021)&(A.margin_cutoff==0)][['family','group','spearman','n_valid','disagreement_rate','mean_L1_difference','relative_L1','units']].copy();q.family=q.family.map(labels)
# Source-feature top five, signed aggregation before absolute mean.
top=[]
for fam in families:
 for mode in ['interventional','tree_path_dependent']:
  d=I[(I.family==fam)&(I.seed==42)&(I['mode']==mode)&(I.background_seed==(20261021 if mode=='interventional' else 0))].nlargest(5,'mean_abs_shap')
  for rank,(_,r) in enumerate(d.iterrows(),1):top.append({'family':fam,'mode':mode,'rank':rank,'source_feature':r.source_feature,'mean_abs_shap':r.mean_abs_shap})
write=pd.DataFrame(top);write.to_csv(O/'top_source_features.csv',index=False)
# Magnitude diagnostics by agreement and prespecified margin subset.
magnitude_rows=[]
for fam in families:
 for seed in [42,17,73]:
  for bs in ([20261021,20261023,20261024] if seed==42 else [20261021]):
   for group in ['BILL_AMT','PAY_AMT']:
    loc=pd.read_csv(O/f'{fam}/seed_{seed}/local_{group}_{bs}.csv')
    for cut in [0.,.01,.05,.1]:
     valid=loc.unique_top_both if cut==0 else loc.unique_top_both & (loc.margin_interventional>cut) & (loc.margin_path>cut)
     for status in [False,True]:
      d=loc[valid & (loc.disagreement==status)]
      magnitude_rows.append({'family':fam,'seed':seed,'background_seed':bs,'group':group,'margin_cutoff':cut,'winner_changed':status,'n':len(d),'mean_L1':float(d.L1_difference.mean()) if len(d) else None,'median_L1':float(d.L1_difference.median()) if len(d) else None,'mean_abs_group_difference':float(d.abs_group_difference.mean()) if len(d) else None})
mag=pd.DataFrame(magnitude_rows);mag.to_csv(O/'magnitude_by_agreement.csv',index=False)
fig,axes=plt.subplots(2,2,figsize=(10,8))
for fam,ax in zip(families,axes.flat):
 loc=pd.read_csv(O/f'{fam}/seed_42/local_BILL_AMT_20261021.csv');factor=100 if fam in ['random_forest','extra_trees'] else 1
 data=[loc.loc[loc.unique_top_both & (loc.disagreement==status),'L1_difference'].values*factor for status in [False,True]]
 ax.boxplot(data,tick_labels=['Same top feature','Different top feature'],showfliers=False,medianprops={'color':'black'});ax.set_ylim(bottom=0);ax.set_title(labels[fam]);ax.set_ylabel('L1 difference (probability pp)' if factor==100 else 'L1 difference (log-odds)')
save(fig,'difference_magnitude_by_winner')
report='# Hasil eksperimen revisi empat model\n\n'
report+='Dataset UCI Credit Card Default dan split lama dipertahankan. Protokol ditetapkan sebelum hasil revisi, tetapi test sudah pernah dilihat; hasil ini analisis pengembangan, bukan konfirmasi pada holdout baru.\n\n'
report+='## 1. Cakupan yang selesai\n\nEmpat keluarga, tiga konfigurasi per keluarga, tiga seed training (42/17/73), 1.000 observasi test tetap. Seed 42 memakai tiga background 100 train; dua seed lain memakai background awal tetap. Pilot dan additivity diperiksa setiap model. Hasil lama tidak ditimpa. Dua background tambahan RF seed 42 menggunakan artefak yang sudah direproduksi; lihat reuse_provenance.json.\n\n'
report+='## 2. Performa prediksi\n\n'+table(perf)+'\n'
report+=f'Model utama menurut AP validation adalah **{labels[winner]}**. Model utama tidak dipilih dari AP test. Threshold tiap model berasal dari F1 validation; Brier bukan ukuran kalibrasi murni. Semua model tetap disertakan pada analisis atribusi.\n\n![Average precision](figures/predictive_ap.png)\n\n'
report+='## 3. Dua mode pada setiap model\n\n'+table(q)+'\n'
report+='Raw Random Forest/Extra Trees berupa probabilitas; raw kedua boosting berupa log-odds/margin. Selisih mentah tidak sebanding lintas satuan. Relative L1 memakai mean abs(raw output - baseline path) sebagai penyebut per fitted model, tetapi tetap tidak invariant terhadap link nonlinear. Ranking dan persentase ketidaksepakatan juga bergantung pada model/fungsi output.\n\n![Importance tagihan](figures/billing_importance.png)\n\n'
report+='B1-B6 pada grafik berarti BILL_AMT1-BILL_AMT6. Skala setiap panel mengikuti unit modelnya.\n\n'
report+='## 4. Kasus hampir seri\n\nMargin = (atribusi absolut pertama - kedua)/(pertama + kedua). Subset robust mensyaratkan margin >0,05 pada kedua mode. Ambang ditetapkan sebelum analisis; hasil 0,01 dan 0,10 tetap tersedia di tabel lengkap. Denominator subset berubah sehingga angka subset tidak boleh dianggap langsung sebagai pengurangan error pada seluruh nasabah.\n\n'+table(robust)+'\n![Ketidaksepakatan dan margin](figures/winner_margin_disagreement.png)\n\n'
report+='Besar perbedaan juga dibandingkan antara kasus dengan pemenang sama dan berbeda. Seluruh ambang margin tersedia di magnitude_by_agreement.csv; plot berikut menampilkan baseline utama, tanpa outlier pada tampilan boxplot (data tidak dihapus).\n\n![Magnitudo perubahan dan pemenang](figures/difference_magnitude_by_winner.png)\n\n'
qr=q.set_index(['family','group'])
rf_l1=float(qr.loc[('Random Forest','BILL_AMT'),'mean_L1_difference'])*100
et_l1=float(qr.loc[('Extra Trees','BILL_AMT'),'mean_L1_difference'])*100
report+=f'RF dan Extra Trees sama-sama menunjukkan ketidaksepakatan sekitar 42%, tetapi mean L1 enam tagihannya masing-masing {rf_l1:.4f} dan {et_l1:.4f} poin persentase probabilitas. Kesamaan tingkat pergantian pemenang tidak berarti besar perubahan atribusinya sama. Pada kedua boosting, distribusi L1 kasus dengan pemenang sama/berbeda juga dapat tumpang tindih; perubahan ranking bukan pengganti ukuran magnitudo.\n\n'
report+='## 5. Background dan seed\n\n![Sensitivitas background](figures/background_disagreement.png)\n\n'+table(seeds)+'\n'
report+='Tiga seed adalah pemeriksaan deskriptif, bukan 100 replikasi independen. Gradient Boosting dengan subsample=1 dan semua fitur dapat menghasilkan fungsi yang sama pada seed berbeda; kolom kesamaan prediksi test di atas harus dibaca sebelum menyebutnya variasi model yang independen. Kesamaan pada test saja tidak membuktikan fungsi sama pada seluruh input. Tidak mengklaim menangkap distribusi ketidakpastian populasi.\n\n'
report+='## 6. Kelompok fitur dan batas interpretasi\n\n'+table(pd.read_csv(O/'correlation_summary.csv'))+'\n'
report+='PAY_AMT memiliki korelasi Pearson lebih rendah pada train, tetapi Spearman tetap sekitar 0,46-0,55. Perbandingan kelompok tidak mengisolasi efek korelasi karena distribusi, relevansi prediktif, dan penggunaan split juga berbeda. Pemain TreeSHAP tetap kolom encoded; penjumlahan signed indikator untuk laporan source-level bukan permainan grouped Shapley baru. Masking kategori dapat membentuk kombinasi indikator yang tidak terjadi secara alami.\n\n'
report+='## 7. Posisi terhadap paper 2025\n\nEmpat model dan analisis margin memperluas dimensi pemeriksaan, tetapi tidak berarti penelitian secara keseluruhan mengungguli jurnal. Lin-Wang meneliti 100 seed XGBoost; kita hanya tiga. García-Céspedes dkk. sudah membahas dua mode dan distribusi portfolio; detail full text belum dapat diaudit lengkap. Lihat literature_positioning.md untuk bukti dan batas akses. Studi kita diposisikan sebagai pengembangan empiris terfokus; klaim novelty belum final.\n\n'
report+='## 8. Keterbatasan dan pekerjaan naskah\n\nSatu dataset, satu split, test pernah dilihat, pencarian konfigurasi terbatas, hanya tiga seed dan ukuran background 100, tanpa klaim kausal maupun uji signifikansi populasi. Kalibrasi tidak diuji dengan reliability curve. Background adalah sampel dari train yang sama; belum ada uji pergeseran portfolio/populasi. Tidak ada eksperimen manipulasi korelasi atau enumerasi Shapley acuan. Google Docs dan panduan konsultasi historis belum diubah.\n\n'
report+='Tabel lengkap: selection_validation.csv, predictive_metrics.csv, attribution_summary.csv, feature_comparison.csv, source_importance.csv, seed_sensitivity.csv, pilot_checks.csv. Unit, membership, baseline, checksum, dan versi ada pada manifest serta model_manifest masing-masing run.\n'
(O/'RESULTS.md').write_text(report,encoding='utf-8')
# Independent consistency checks of generated summaries.
assert len(P)==48 and len(A)==160 and len(pd.read_csv(O/'pilot_checks.csv'))==24
assert len(list(O.glob('*/seed_*/shap_*.npz')))==32
for fam in families:
 sel=pd.read_csv(O/'selection_validation.csv');d=sel[sel.family==fam];selected=json.loads((O/fam/'selection.json').read_text());assert selected['candidate']==int(d.loc[d.validation_AP.idxmax(),'candidate'])
assert len(I.source_feature.unique())==23 and len(I)==736 and len(C)==240
(O/'analysis_checks.json').write_text(json.dumps({'status':'PASS','prediction_metric_rows':len(P),'attribution_summary_rows':len(A),'pilot_rows':24,'shap_files':32,'source_features':23,'plots':5,'selection_validation_only':True},indent=2))
print('ANALYSIS PASS; validation winner:',winner)
