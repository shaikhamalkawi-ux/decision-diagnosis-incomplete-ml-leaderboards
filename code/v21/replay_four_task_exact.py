from fractions import Fraction as F
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent.parent
ROWS=[(F(1),F(0),F(1,3),F(2,3)),(F(1),F(1,3),F(0),F(2,3)),(F(1),F(1,6),F(1,6),F(2,3)),(F(1),F(0),F(1,2),F(1,2)),(F(1),F(1,2),F(0),F(1,2)),(F(1),F(1,3),F(1,3),F(1,3))]
KNOWN=[(F(0),F(1,3),F(2,3),F(1)),(F(1,2),F(1),F(1,2),F(0)),(F(0),F(2,3),F(2,3),F(2,3))]
P=[F(21,68),F(21,68),F(21,68),F(5,68)];E=F(13,400)
def support(g):
    assert min(P)>E
    return sum(w*x for w,x in zip(P,g))+E*(max(g)-min(g))
res=[]
for ii,u in enumerate(ROWS):
    task=[u]+KNOWN
    gaps={}
    for i in range(4):
        rival={str(j):str(support([row[i]-row[j] for row in task])) for j in range(4) if j!=i}
        bound=max(F(t) for t in rival.values())
        assert bound>0
        gaps[str(i)]={'rival_supports':rival,'max_margin':str(bound)}
    res.append({'row_type':ii+1,'all_candidate_excluded':True,'gaps':gaps})
mid=tuple((x+y)/2 for x,y in zip(ROWS[0],ROWS[-1]))
final={str(j):str(support([row[0]-row[j] for row in ([mid]+KNOWN)])) for j in (1,2,3)}
assert final=={'1':'-11/40800','2':'-29/5100','3':'-11/40800'},final
out={'six_full_rank_rows_all_excluded':True,'min_candidate_margin':str(min(F(v['max_margin']) for r in res for v in r['gaps'].values())),
     'nonexistence_fixed_joint_mixture_average_supports':final,'details':res}
(ROOT/'results/V20_FOUR_TASK_EXACT_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='details'},indent=2))
