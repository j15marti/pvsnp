#!/usr/bin/env python3
"""Finite audit of the bounded-rank 2-CNF/affine generator conclusion.

Python 3.10 or newer; standard library only. Run without -O so assertions remain
active. This checks all 2-CNF relations on three variables against all ordered
independent affine systems on those variables. It enumerates variable seeds,
which may be redundant within an implication SCC; it does not separately audit
the sharper SCC candidate-count bound. The empty relation is immediate and is
excluded from the counted comparisons. This is finite evidence, not a proof of
the general theorem or an unrestricted polynomial-time SAT solver.
"""

from itertools import combinations, product
from pathlib import Path
import json

def rank(rows):
    basis={}
    for v in rows:
        while v:
            k=v.bit_length()-1
            if k in basis: v ^= basis[k]
            else:
                basis[k]=v
                break
    return len(basis)

def parity(x):
    return x.bit_count() & 1

n=3
words=range(1<<n)
literals=[(i,b) for i in range(n) for b in (0,1)]
clauses=[(l,) for l in literals]+[(a,b) for a,b in combinations(literals,2) if a[0]!=b[0]]
masks=[]
for C in clauses:
    masks.append(sum(1<<x for x in words if any(((x>>i)&1)==b for i,b in C)))
relations={(1<<(1<<n))-1:()}
for j,cm in enumerate(masks):
    for rel,cs in list(relations.items()):
        relations.setdefault(rel&cm,cs+(j,))

systems=[]
for k in range(n+1):
    for rows in product(range(1<<n),repeat=k):
        if rank(rows)!=k: continue
        for rhs in range(1<<k):
            sol=sum(1<<x for x in words if all(parity(row&x)==((rhs>>j)&1) for j,row in enumerate(rows)))
            systems.append((rows,rhs,sol))

checks=0
for rel,clause_ids in relations.items():
    if not rel: continue
    a=next(x for x in words if rel>>x&1)
    implications=[set() for _ in range(n)]
    forbidden=[]
    for j in clause_ids:
        gauged=tuple((i,b^((a>>i)&1)) for i,b in clauses[j])
        assert any(b==0 for i,b in gauged)
        if len(gauged)==1: forbidden.append(1<<gauged[0][0])
        elif all(b==0 for i,b in gauged): forbidden.append(sum(1<<i for i,b in gauged))
        else:
            u=next(i for i,b in gauged if b==0)
            v=next(i for i,b in gauged if b==1)
            implications[u].add(v)
    reach=[]
    for i in range(n):
        seen={i}; todo=[i]
        while todo:
            u=todo.pop()
            for v in implications[u]-seen:
                seen.add(v);todo.append(v)
        reach.append(sum(1<<j for j in seen))
    seed_images={}
    for r in range(n+1):
        images=set()
        for k in range(r+1):
            for S in combinations(range(n),k):
                d=0
                for i in S: d|=reach[i]
                if not any((d&f)==f for f in forbidden):images.add(a^d)
        seed_images[r]=images
    for rows,rhs,sol in systems:
        brute=bool(rel&sol)
        got=any((sol>>x)&1 for x in seed_images[len(rows)])
        assert got==brute,(rel,clause_ids,rows,rhs,a,seed_images)
        checks+=1
result={"n":n,"distinct_2cnf_relations":len(relations),"nonempty_2cnf_relations":len(relations)-1,"independent_affine_systems_with_ordered_rows":len(systems),"joint_checks":checks,"failures":0,"scope":"Exhaustive for every distinct 2-CNF Boolean relation on three variables and every independent ordered GF2 row system on those variables. Rank theorem is symbolic; this is a finite control."}
print(json.dumps(result,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
