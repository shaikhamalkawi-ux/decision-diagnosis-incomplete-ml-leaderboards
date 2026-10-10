#!/usr/bin/env python3
"""Standalone pure-stdlib exact arithmetic verification of G2-KBS V22 rank-only proofs.

Does NOT establish source-score feasibility. That is a separate private source-gated audit.
"""
import json,itertools,argparse
from fractions import Fraction as F
from pathlib import Path
P=Path(__file__).resolve().parent

def support(g,eps):
 assert F(0)<=eps<=F(1,4)
 return sum(g,F(0))/4+eps*(max(g)-min(g))

def ranks_valid(row):
 if len(row)!=4:return False
 groups=sorted(set(row))
 pos=0
 for code in groups:
  count=sum(t==code for t in row)
  if code!=2*pos+count-1:return False
  pos+=count
 return pos==4

def actions(eps,i):
 for j in range(4):
  if i==j:continue
  for plus in range(4):
   for minus in range(4):
    if plus==minus:continue
    yield j,[F(1,4)+(eps if d==plus else -eps if d==minus else 0) for d in range(4)]

def payoff(rows,masked_pos,pat,i,action):
 j,w=action
 return sum(w[d]*F(((pat if d==masked_pos else rows[d])[i]-(pat if d==masked_pos else rows[d])[j]),6) for d in range(4))

def case_verify(case):
 rows=case['task_rank_codes_complete_data'];patterns=case['admissible_unknown_task_rank_rows']
 assert len(rows)==4 and all(ranks_valid(x) for x in rows)
 assert len(patterns) in (11,19) and len({tuple(p) for p in patterns})==len(patterns)
 assert all(ranks_valid(row) for row in patterns)
 h=case['task_names'].index(case['hidden_task']);i=case['affected_candidate_index'];eps=F(case['epsilon'])
 act=list(actions(eps,i))
 # Each method has some positive defeating weight/rival in every legal completion.
 v_all=[]
 for cand in range(4):
  ca=list(actions(eps,cand))
  v_all.append(min(max(payoff(rows,h,pat,cand,a) for a in ca) for pat in patterns))
 assert min(v_all)==F(1,48) and all(v>0 for v in v_all)
 alpha=min(max(payoff(rows,h,pat,i,a) for a in act) for pat in patterns)
 delta=max(min(payoff(rows,h,pat,i,a) for pat in patterns) for a in act)
 assert alpha==F(1,48) and delta==F(-1,24)
 # Adversary: two legal rank completions mixed equally, defeating all fixed actions.
 L=case['completion_mixture'];assert len(L)==2
 lambda_completions=[x['rank_row'] for x in L];lambda_probs=[F(x['probability']) for x in L]
 assert sum(lambda_probs)==1 and all(p in patterns for p in lambda_completions)
 max_dual=max(sum(prob*payoff(rows,h,pat,i,a) for prob,pat in zip(lambda_probs,lambda_completions)) for a in act)
 # Decision maker: two fixed joint actions mixed equally, not depending on completion.
 M=case['fixed_action_mixture'];assert len(M)==2
 mixes=[]
 for x in M:
  w=list(map(F,x['weight_vector']));assert sum(w)==1 and min(w)>=0
  assert sum(abs(y-F(1,4)) for y in w)/2<=eps
  j=x['rival_index'];assert j!=i
  mixes.append((F(x['probability']),(j,w)))
 assert sum(v for v,_ in mixes)==1
 min_primal=min(sum(prob*payoff(rows,h,pat,i,action) for prob,action in mixes) for pat in patterns)
 assert max_dual==min_primal==0
 # Role renaming and arbitrary task permutations preserve pure/mixture outcome in rank space.
 for order in itertools.permutations(range(4)):
  reorder=[rows[d] for d in order];newh=order.index(h)
  changed_actions=[(j,[w[d] for d in order]) for j,w in act]
  assert min(max(payoff(reorder,newh,pat,i,a) for a in changed_actions) for pat in patterns)==alpha
 for perm in itertools.permutations(range(4)):
  shifted=[[r[d] for d in perm] for r in rows]
  newpat=[[p[d] for d in perm] for p in patterns]
  newi=perm.index(i)
  ca=list(actions(eps,newi))
  assert min(max(payoff(shifted,h,pat,newi,a) for a in ca) for pat in newpat)==alpha
 return {'case_id':case['case_id'],'source_sha256':case['source_archive_hash'],'legal_rank_rows':len(patterns),
 'all_candidates_semantic_min':str(min(v_all)), 'affected_candidate_semantic_min':str(alpha),
 'best_fixed_single_action':str(delta), 'optimal_fixed_joint_mixture':'0',
 'dual_upper_bound':str(max_dual),'dual_lower_bound':str(min_primal),
 'task_permutation_assertions':24,'model_permutation_assertions':24,'status':'PASS'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificates',default=str(P/'V22_RANK_ONLY_SADDLE_CERTIFICATES.json'));args=ap.parse_args()
 o=json.load(open(args.certificates))
 assert len(o['cases'])==4 and all(x['source_archive_hash']==o['source_sha256'] for x in o['cases'])
 vals=[case_verify(c) for c in o['cases']]
 out={'verification':'PASS','cases':len(vals),'metamorphic_permutation_assertions':sum(x['task_permutation_assertions']+x['model_permutation_assertions'] for x in vals),
 'total_rank_patterns':sum(x['legal_rank_rows'] for x in vals),'details':vals,
 'boundary':'Source-realizability not independently established without restricted original fold-score CSV.'}
 (P/'V22_RANK_ONLY_VERIFICATION.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
