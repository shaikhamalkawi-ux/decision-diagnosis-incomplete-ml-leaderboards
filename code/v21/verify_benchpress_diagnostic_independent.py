#!/usr/bin/env python3
"""Verification without importing BenchPress diagnosis/producer code.

Exact rank-pair integer supports; verifies opposite completion arrays and
all constant-decision upper/lower-box certificates for 72 prespecified states.
"""
from pathlib import Path
from fractions import Fraction
import pandas as pd,numpy as np,json,collections,csv
ROOT=Path(__file__).resolve().parent.parent.parent
DATA=ROOT/'inputs/benchpress_primary_complete_case_scores.csv'
if not DATA.exists():
    import zipfile,io
    Z='/mnt/data/CERT_Bench_v0_8_ReleaseIntegrityWitnessClosure_Package.zip'
    p='CERT_Bench_v0_8_ReleaseIntegrityWitnessClosure/baseline_v041/results/benchpress_primary_complete_case_scores.csv'
    with zipfile.ZipFile(Z) as z:src=z.read(p)
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_bytes(src)
DATAFRAME=pd.read_csv(DATA).set_index('benchmark_id')
BENCH=list(DATAFRAME.index);MODEL=list(DATAFRAME.columns);D=len(BENCH);M=len(MODEL)
assert D==11 and M==10 and np.isfinite(DATAFRAME.to_numpy()).all()

def rankhi(row):
    return np.array([sum((2 if y>x else 1 if y==x else 0) for y in row)-1 for x in row],dtype=int)
truth=np.stack([rankhi(x) for x in DATAFRAME.to_numpy(float)])

def max_integer_support(g,k):
    a=sorted(int(v) for v in g)
    return sum(a)+k*a[-1]-sum(a[:k])

def semantic_decision(grid,k):
    commons=[]
    for i in range(M):
        mx=max(max_integer_support(grid[:,i]-grid[:,j],k) for j in range(M) if i!=j)
        if mx<=0:commons.append(i)
    return int(len(commons)==0)

def rank_orders_to_grid(order_map,known_rows):
    rr=truth.copy()
    for key,seq in order_map.items():
        t=BENCH.index(key)
        assert t not in known_rows
        assert len(seq)==M and sorted(seq)==list(range(M))
        r=np.zeros(M,dtype=int)
        for at,j in enumerate(seq):r[j]=2*at
        rr[t]=r
    return rr

rows=list(csv.DictReader(open(ROOT/'results/V20_BENCHPRESS_EXTERNAL_DIAGNOSTIC.csv')))
pairs=json.load(open(ROOT/'results/V20_BENCHPRESS_OPPOSITE_COMPLETIONS.json'))
pairmap={(r['order'],int(r['k']),int(r['q'])):r for r in pairs}
assert len(rows)==72
stat=collections.Counter()
for a in rows:
    order,k,q=a['order'],int(a['k_over_11']),int(a['observed_rows_q'])
    known={BENCH.index(t) for t in a['observed_benchmarks'].split(';') if t}
    assert len(known)==q
    status=a['status'];stat[status]+=1
    if status=='INFORMATION_LIMITED':
        pp=pairmap[(order,k,q)]['opposite_completions']
        assert len(pp)==2
        assert pp[0]['kind']=='archived_full' and pp[0]['D']==semantic_decision(truth,k)
        alt=pp[1];r=rank_orders_to_grid(alt['rank_orders'],known)
        assert alt['D']==semantic_decision(r,k)
        assert alt['D']!=pp[0]['D']
        assert all(np.array_equal(r[t],truth[t]) for t in known)
    else:
        assert (order,k,q) not in pairmap
        # Every hidden rank-difference lies within [-18,18].
        lower=[]; upper=[]
        for i in range(M):
            low_i=[];upper_i=[]
            for j in range(M):
                if i==j:continue
                gl=np.array([int(truth[t,i]-truth[t,j]) if t in known else -18 for t in range(D)],int)
                gu=np.array([int(truth[t,i]-truth[t,j]) if t in known else 18 for t in range(D)],int)
                low_i.append(max_integer_support(gl,k))
                upper_i.append(max_integer_support(gu,k))
            lower.append(max(low_i));upper.append(max(upper_i))
        if status=='CERTIFIED_D1':
            assert min(lower)>0
            assert semantic_decision(truth,k)==1
        elif status=='CERTIFIED_D0':
            assert min(upper)<=0
            assert semantic_decision(truth,k)==0
        else:raise AssertionError(status)
summary={'verification':'PASS','states_verified':len(rows),'opposite_pairs_verified':len(pairs),
         'certified_states_verified':stat['CERTIFIED_D1']+stat['CERTIFIED_D0'],
         'status_counts':dict(stat),'source_matrix_sha256':__import__('hashlib').sha256(DATA.read_bytes()).hexdigest(),
         'scope':'Benchmark-level row masking, not fold-level; exact observed rank and hypothetical strict-order checks.'}
(ROOT/'results/V21_BENCHPRESS_INDEPENDENT_REPLAY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
