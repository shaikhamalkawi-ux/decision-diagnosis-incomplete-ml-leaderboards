#!/usr/bin/env python3
"""Independent exact integer recreation of all 65,780 canonical states.

Reimplements 68-task TV support using the two-full-plus-one-partial donor
formula for uniform p and epsilon=13/400; no access to prior proof engine.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,hashlib,time
ROOT=Path(__file__).resolve().parent.parent
# Rank rows encoded in multiples of 1/6; A/B/C/D indices fixed.
UNKNOWN=[(6,0,2,4),(6,2,0,4),(6,1,1,4),(6,0,3,3),(6,3,0,3),(6,2,2,2)]
KNOWN=[((0,2,4,6),21),((3,6,3,0),21),((0,4,4,4),5)]

def count_vectors(total,n):
    if n==1:
        yield (total,)
    else:
        for i in range(total+1):
            for rest in count_vectors(total-i,n-1):
                yield (i,)+rest

def support_integer_numerator(buckets):
    """D=68 equal atoms, epsilon=13/400. Gap coords multiples of 1/6.
    Returns exact 68*400*6 times the maximum weighted normalized gap.
    """
    b=sorted((int(g),int(c)) for g,c in buckets if c>0)
    if sum(c for g,c in b)!=68:raise AssertionError('Counts not 68')
    mx=b[-1][0]
    total=sum(g*c for g,c in b)
    lows=[]
    for gap,count in b:
        lows.extend([gap]*min(count,3-len(lows)))
        if len(lows)==3:break
    low1,low2,low3=lows
    return 400*(total+2*mx-low1-low2) + 84*(mx-low3)

def main():
    tic=time.monotonic()
    count=0;comparisons=0;min_max_margins=[None]*4;zero_for_some=[]
    min_margin_over_all=None
    for vector in count_vectors(21,6):
        count+=1
        states=[]
        for row,c in zip(UNKNOWN,vector):
            if c:states.append((row,c))
        states+=KNOWN
        for i in range(4):
            max_num=None
            for j in range(4):
                if i==j:continue
                buckets=[(row[i]-row[j],c) for row,c in states]
                n=support_integer_numerator(buckets)
                comparisons+=1
                if max_num is None or n>max_num:max_num=n
            if max_num<=0:zero_for_some.append({'vector':vector,'candidate':i,'max_margin_num':max_num})
            if min_max_margins[i] is None or max_num<min_max_margins[i]:min_max_margins[i]=max_num
            if min_margin_over_all is None or max_num<min_margin_over_all:min_margin_over_all=max_num
    assert count==65780 and comparisons==789360
    assert not zero_for_some,zero_for_some[:4]
    # Average rank array of both special completions: uncertain types 1+6 /2,
    # use 12th-rank units to avoid halves.
    avg_unc=tuple(a+b for a,b in zip(UNKNOWN[0],UNKNOWN[5]))
    avg_known=[(tuple(2*x for x in row),count) for row,count in KNOWN]
    avg_buckets=[]
    for j in (1,2,3):
        b=[(avg_unc[0]-avg_unc[j],21)]+[(row[0]-row[j],n) for row,n in avg_known]
        # coords in 1/12 instead of 1/6 -> divide numerator by 68*400*12
        num=support_integer_numerator(b)
        avg_buckets.append({'rival':j,'support_num':num,'support_exact':str(F(num,68*400*12))})
    assert all(x['support_num']<0 for x in avg_buckets)
    summ={'canonical_states':count,'ordered_comparisons':comparisons,'all_candidates_excluded_all_completions':True,
         'smallest_worst_rival_support_per_candidate':[str(F(x,68*400*6)) for x in min_max_margins],
         'global_min_worst_rival_support':str(F(min_margin_over_all,68*400*6)),
         'average_two_special_completions_A_supports':avg_buckets,
         'proof_family':'completed 68-task independent product of 21 unknown ranks, 4 methods, uniform p, eps 13/400; exact integer TV transportation',
         'runtime_seconds':round(time.monotonic()-tic,2)}
    (ROOT/'results/V20_EXACT_68TASK_FULL_STATE_REPLAY.json').write_text(json.dumps(summ,indent=2)+'\n')
    print(json.dumps(summ,indent=2))
if __name__=='__main__':main()
