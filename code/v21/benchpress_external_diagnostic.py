#!/usr/bin/env python3
"""Independent *benchmark-row* diagnostic transfer (not fold-level G2).

Inputs: 11x10 complete-case scores from frozen public BenchPress source archive.
No imputation, model retraining, synthetic benchmark observations or inferential
frequency claims. Alternative rank rows are explicitly hypothetical completions.
"""
from pathlib import Path
import zipfile,io,pandas as pd,numpy as np, hashlib,json,csv,random
ROOT=Path(__file__).resolve().parent.parent.parent; OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
ZIP=Path('/mnt/data/CERT_Bench_v0_8_ReleaseIntegrityWitnessClosure_Package.zip')  # optional historical fallback
LOCAL_SCORES=ROOT/'inputs/benchpress_primary_complete_case_scores.csv'
LOCAL_RANKS=ROOT/'inputs/benchpress_primary10__rank__equal__normalized_matrix.csv'
EXPECTED_LOCAL_SHA='b13854563618794e44dfa9d98e001765b0049cd023613b836964de3be631a605'
RECORDED_SOURCE_ARCHIVE_SHA='0a85ae39025ad7d8e4bbca031752964a18c1a5c012f246929ee8c92cc0205511'
ENTRY='CERT_Bench_v0_8_ReleaseIntegrityWitnessClosure/baseline_v041/results/benchpress_primary_complete_case_scores.csv'
RANKENTRY='CERT_Bench_v0_8_ReleaseIntegrityWitnessClosure/data/processed/benchpress_primary10__rank__equal__normalized_matrix.csv'
DENOM=2*9  # half-midrank diff denom across 10 models

def half_ranks_for_high_good(x):
    return np.array([2*sum(y>z for y in x)+sum(y==z for y in x)-1 for z in x],dtype=np.int16)

def support_num(g,k):
    q=sorted(int(v) for v in g)
    return sum(q)+k*max(q)-sum(q[:k]) # / (D*DENOM)

def full_decision(mat,k):
    d,m=mat.shape
    common=[];margins={}
    for i in range(m):
        v=max(support_num(mat[:,i]-mat[:,j],k) for j in range(m) if j!=i)
        margins[i]=v
        if v<=0:common.append(i)
    return int(len(common)==0),common,margins

def uniform_exclusion_certificate(observed,mask,k):
    # Adversarial rank difference on each entirely undisclosed task may be -DENOM.
    # This is a *sufficient* outer-box certificate of D=1; never invert its failure.
    d,m=observed.shape
    margins=[]
    for i in range(m):
        opts=[]
        for j in range(m):
            if i==j:continue
            gaps=np.where(mask,observed[:,i]-observed[:,j],-DENOM)
            opts.append(support_num(gaps,k))
        margins.append(max(opts))
    return bool(min(margins)>0),min(margins),margins

def uniform_D0_certificate(observed,mask,k):
    """Sufficient D=0: one candidate defeats all rivals even under
    *upper* completion gap +DENOM for each unobserved benchmark row.
    """
    d,m=observed.shape
    for i in range(m):
        supports=[]
        for j in range(m):
            if i==j:continue
            gap=np.where(mask,observed[:,i]-observed[:,j],DENOM)
            supports.append(support_num(gap,k))
        if max(supports)<=0:return True,i,max(supports)
    return False,None,None

def main():
    if LOCAL_SCORES.exists() and LOCAL_RANKS.exists():
        b=LOCAL_SCORES.read_bytes(); rb=LOCAL_RANKS.read_bytes()
        assert hashlib.sha256(b).hexdigest()==EXPECTED_LOCAL_SHA
    else:
        with zipfile.ZipFile(ZIP) as archive:
            b=archive.read(ENTRY); rb=archive.read(RANKENTRY)
        assert hashlib.sha256(b).hexdigest()==EXPECTED_LOCAL_SHA
    data=pd.read_csv(io.BytesIO(b)).set_index('benchmark_id')
    recorded=pd.read_csv(io.BytesIO(rb),index_col=0)
    data=data.loc[recorded.index,recorded.columns]
    assert data.shape==(11,10) and np.isfinite(data.to_numpy(float)).all()
    benchmark_ids=list(data.index);model_ids=list(data.columns)
    observed=np.stack([half_ranks_for_high_good(row) for row in data.to_numpy(float)])
    assert np.allclose(observed/18,recorded.to_numpy(float),rtol=0,atol=1e-12)
    d,m=observed.shape
    orders={'alphabetical':sorted(range(d),key=lambda i:benchmark_ids[i]),
            'reverse':sorted(range(d),key=lambda i:benchmark_ids[i],reverse=True),
            'sha256_seed930021':sorted(range(d),key=lambda i:hashlib.sha256((str(930021)+':'+benchmark_ids[i]).encode()).hexdigest())}
    rows=[];pairs=[]
    for order_name,order in orders.items():
      for k in (1,2):
        actualD,actualC,actualM=full_decision(observed,k)
        for q in range(d+1):
          hidden=set(order[q:]);mask=np.array([i not in hidden for i in range(d)])
          certified,min_num,candidate_num=uniform_exclusion_certificate(observed,mask,k)
          certified_zero, necessary_candidate, max_upper=uniform_D0_certificate(observed,mask,k)
          assert not (certified and certified_zero)
          if q==d:assert not hidden
          # truth is a first compatible completion, not a determined outcome if q<d.
          dset={actualD}; explicit=[{'kind':'archived_full','D':actualD,'common':actualC}]
          # structured alternatives, selected using only observed rows
          score=np.mean(np.where(mask[:,None],observed,np.nan),axis=0) if q==d else None
          rng=random.Random(930021 + k*1000 + 17*q + list(orders).index(order_name))
          alternatives=[]
          for favorite in range(m):
              others=[x for x in range(m) if x!=favorite]
              for setup in (0,1):
                  # Favor the selected model but vary the complete order among rivals
                  ps=others if setup==0 else list(reversed(others))
                  alternatives.append([favorite]+ps)
          for trial in range(32):
              alternatives.append(rng.sample(list(range(m)),m))
          for trial,ranking in enumerate(alternatives):
              tmp=observed.copy()
              for task in hidden:
                  if trial>=2*m:
                      rank_order=rng.sample(list(range(m)),m)
                  else:
                      rank_order=ranking
                  row=np.zeros(m,dtype=np.int16)
                  for rank,model in enumerate(rank_order):row[model]=2*rank
                  tmp[task]=row
              D,C,M=full_decision(tmp,k)
              if D not in dset:
                  explicit.append({'kind':'hypothetical_strict_rank_row','D':D,'common':C,'rank_orders':{benchmark_ids[t]:sorted(range(m),key=lambda j:tmp[t,j]) for t in hidden}})
              dset.add(D)
              if len(dset)==2:break
          status='INFORMATION_LIMITED' if len(dset)==2 else 'CERTIFIED_D1' if certified else 'CERTIFIED_D0' if certified_zero else 'INCONCLUSIVE'
          if certified:assert dset=={1},'unsound exclusion certificate'
          if certified_zero:assert dset=={0},'unsound necessary-winner certificate'
          rows.append({'order':order_name,'k_over_11':k,'observed_rows_q':q,'unseen_rows':len(hidden),
                       'realized_archive_D':actualD,'status':status,'certified_D1':certified,
                       'min_exclusion_margin_num':min_num,'certified_D0':certified_zero,'D0_candidate':necessary_candidate,'max_D0_upper':max_upper, 'opposing_pair_found':len(dset)==2,
                       'num_constructed_trials_at_most':len(alternatives), 'observed_benchmarks':';'.join(benchmark_ids[t] for t in order[:q])})
          if len(dset)==2:pairs.append({'order':order_name,'k':k,'q':q,'opposite_completions':explicit})
          print('BENCHPRESS',order_name,k,q,status,flush=True)
    with (OUT/'V20_BENCHPRESS_EXTERNAL_DIAGNOSTIC.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/'V20_BENCHPRESS_OPPOSITE_COMPLETIONS.json').write_text(json.dumps(pairs,indent=2)+'\n')
    from collections import Counter
    ct=Counter(x['status'] for x in rows)
    summ={'frozen_score_csv_sha256':hashlib.sha256(b).hexdigest(),'archive_sha256':RECORDED_SOURCE_ARCHIVE_SHA,
         'data_entry':ENTRY,'rows':d,'models':m,'state_count':len(rows),'state_status_counts':dict(ct),
         'true_full_decision':{str(k):full_decision(observed,k)[0] for k in (1,2)},
         'sampling':'three prespecified disclosure orders, k=1/11 and 2/11, all prefix counts 0..11',
         'rank_completions':'Each missing entire benchmark row replaced by a possible strict total order; no score magnitude or fold-level realizability claim',
         'no_inference':'This is a benchmark-row diagnostic transfer, not independent fold-level confirmation of the TabArena Q theorem',
         'source':'Microsoft BenchPress public 11x10 complete-case scope retained in CERT-Bench v0.8 evidence archive; verify against official HF CDLA release'}
    (OUT/'V20_BENCHPRESS_SUMMARY.json').write_text(json.dumps(summ,indent=2)+'\n')
    print(json.dumps(summ,indent=2))

if __name__=='__main__':main()
