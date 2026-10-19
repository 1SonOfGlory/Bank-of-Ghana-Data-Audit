import argparse
import json
import collections
parser = argparse.ArgumentParser(description='Inspect selected cross-frequency relationships.')
parser.add_argument('--profile', default='bog_profile.json')
args = parser.parse_args()
with open(args.profile, encoding='utf-8') as stream:
    p = json.load(stream)
a, m, q = [{r['id']: r for r in p[key]} for key in ('annual', 'monthly', 'quarterly')]
def vals(d,k):return d[k]['values']
for name,d in [('A',a),('M',m),('Q',q)]:
 groups=collections.defaultdict(list)
 for k,r in d.items():
  if r['n']:groups[tuple(r['values'].items())].append(k)
 print(name,'EXACT_DUPLICATES',[v for v in groups.values() if len(v)>1])
print('SELECTED SNAPSHOTS')
for k in ['GHA_HIN_1','GHA_INR_1','GHA_FSI_2','GHA_FSI_1','GHA_INT_3','GHA_INT_4','GHA_GIR_07','GHA_PSI_6','GHA_PSI_7','GHA_PSI_8','GHA_EXR_1']:
 print(k,list(vals(m,k).items())[:2],list(vals(m,k).items())[-4:])
print('CPI reconciliation')
dates=list(vals(m,'GH_PRI_1')); c=vals(m,'GH_PRI_1'); h=vals(m,'GHA_HIN_1');err=[]
for i in range(12,len(dates)):
 t=dates[i]
 if t in h:err.append((abs((c[t]/c[dates[i-12]]-1)*100-h[t]),t))
print('n',len(err),'errors > .2pp',sum(e>.2 for e,t in err),'largest',sorted(err,reverse=True)[:5])
print('ANNUAL QUARTERLY comparisons')
for ak,qk in [('GHA_NAT_AGDP1','GHA_NAT_27'),('GHA_NAT_RGDP20','GHA_NAT_14'),('GHA_NAT_RGDP10','GHA_NAT_8'),('GHA_NAT_RGPD01','GHA_NAT_3')]:
 dif=[]
 for y,v in vals(a,ak).items():
  ds=[f'{y}Q{i}' for i in range(1,5)]
  if all(z in vals(q,qk) for z in ds):
   s=sum(vals(q,qk)[z] for z in ds);dif.append((y,round(v-s,3),round((v/s-1)*100,3)))
 print(ak,qk,'years',len(dif),'last',dif[-5:],'discrepant >1pct',sum(abs(z[2])>1 for z in dif))
print('BOP SIGN CHECK',[(k,[(t,v) for t,v in vals(q,k).items() if v>0][-6:]) for k in ['GHA_BOP_7','GHA_BOP_10','GHA_BOP_4']])
print('MONTHLY QUARTERLY trade reconciliation')
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for mk,qk in [('GHA_TRA_2','GHA_BOP_3'),('GHA_TRA_3','GHA_BOP_4'),('GHA_TRA_0','GHA_BOP_2')]:
 dif=[]
 for t,v in vals(q,qk).items():
  y,qq=t.split('Q'); ds=[f'{s}-{y[-2:]}' for s in months[(int(qq)-1)*3:int(qq)*3]]
  if all(z in vals(m,mk) for z in ds):
   s=sum(vals(m,mk)[z] for z in ds); dif.append((t,round(v-s,2)))
 print(mk,'n',len(dif),'abs difference >1million',sum(abs(z[1])>1 for z in dif),'last',dif[-5:])
print('TARGET COMMON WINDOWS')
for ks in [['GHA_HIN_1','GH_PRI_1_1','GH_PRI_1_2','GHA_EXR_1','GHA_CMP_03','GHA_MAG_9','GHA_INR_1'],['GHA_FSI_2','GHA_FSI_1','GHA_FSI_7','GHA_COA_14','GHA_INR_36','GHA_HIN_1','GHA_EXR_1'],['GHA_INT_4','GHA_GIR_07','GHA_TRA_2','GHA_TRA_3','GHA_EXR_1','GHA_CMP_05','GHA_CMP_01','GHA_CMP_03']]:
 common=set.intersection(*(set(vals(m,k)) for k in ks)); ordered=[t for t in vals(m,ks[0]) if t in common];print(ks,len(common),ordered[0],ordered[-1])

