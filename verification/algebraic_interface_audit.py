#!/usr/bin/env python3
"""Exact, bounded verification of algebraic interface dynamic programming.

Uses only the Python standard library. Run this file to recreate the adjacent
JSON audit. The generic examples use tiny domains for independent truth-table
checks; the matrix tests reconstruct original nonzero-pair source witnesses.
This finite audit supports, but does not replace, the accompanying proof.
"""
from itertools import product
from random import Random
from pathlib import Path
import json

SEED = 20261126
RNG = Random(SEED)
COUNTS = dict(exhaustive_domain_instances=0, exhaustive_domain_targets=0,
              exhaustive_pair_matrices=0, exhaustive_pair_target_trees=0,
              random_instances=0, random_targets=0, node_table_checks=0,
              contribution_witness_checks=0, source_pair_witness_checks=0,
              interval_family_checks=0)


def basis(gens):
    pivots = {}
    for v in gens:
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                v ^= pivots[p]
            else:
                pivots[p] = v
                break
    return [pivots[p] for p in sorted(pivots, reverse=True)]


def member(v, bs):
    for b in bs:
        v = min(v, v ^ b)
    return v == 0


def span(bs):
    out = {0}
    for g in bs:
        out |= {x ^ g for x in list(out)}
    return out


def intersection_basis(a, b):
    """Polynomial Gaussian elimination with dependency provenance."""
    a, b = basis(a), basis(b)
    columns = a + b
    pivots, intersections = {}, []
    for j, g in enumerate(columns):
        v, provenance = g, 1 << j
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                w, old = pivots[p]
                v ^= w
                provenance ^= old
            else:
                pivots[p] = (v, provenance)
                break
        if not v:
            common = 0
            for k, w in enumerate(a):
                if (provenance >> k) & 1:
                    common ^= w
            intersections.append(common)
    return basis(intersections)


def sumset(a, b):
    return {x ^ y for x in a for y in b}


def target_parts(generators, t):
    flat = [(i, g) for i, gs in enumerate(generators) for g in gs]
    pivots = {}
    for j, (_, g) in enumerate(flat):
        v, provenance = g, 1 << j
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                w, old = pivots[p]
                v ^= w
                provenance ^= old
            else:
                pivots[p] = (v, provenance)
                break
    v, provenance = t, 0
    while v:
        p = v.bit_length() - 1
        if p not in pivots:
            return None
        w, old = pivots[p]
        v ^= w
        provenance ^= old
    parts = [0] * len(generators)
    for j, (i, g) in enumerate(flat):
        if (provenance >> j) & 1:
            parts[i] ^= g
    return parts


def random_tree(n):
    live = list(range(n))
    while len(live) > 1:
        a = live.pop(RNG.randrange(len(live)))
        b = live.pop(RNG.randrange(len(live)))
        live.append((a, b))
    return live[0]


def interval_tree(lo, hi):
    if hi - lo == 1:
        return lo
    mid = (lo + hi) // 2
    return interval_tree(lo, mid), interval_tree(mid, hi)


def verify(generators, domains, t, tree, reference=True):
    n = len(generators)
    global_domain = {0}
    if reference:
        for d in domains:
            global_domain = sumset(global_domain, d)
    parts = target_parts(generators, t)
    if parts is None:
        if reference:
            assert t not in global_domain
        return None, 0
    shifted = [{d ^ parts[i] for d in domains[i]} for i in range(n)]
    max_width = 0

    def walk(node):
        nonlocal max_width
        if isinstance(node, int):
            ids = {node}
            raw = shifted[node] if reference else None
            joined = {x: {node: x ^ parts[node]} for x in shifted[node]}
        else:
            li, ld, lt, lw = walk(node[0])
            ri, rd, rt, rw = walk(node[1])
            ids = li | ri
            raw = sumset(ld, rd) if reference else None
            joined = {x ^ y: lw[x] | rw[y] for x in lt for y in rt}
        inside = basis(g for i in ids for g in generators[i])
        outside = basis(g for i in range(n) if i not in ids for g in generators[i])
        interface_basis = intersection_basis(inside, outside)
        max_width = max(max_width, len(interface_basis))
        table = {s for s in joined if member(s, interface_basis)}
        if reference:
            explicit_interface = span(inside) & span(outside)
            assert span(interface_basis) == explicit_interface
            assert table == raw & explicit_interface
            COUNTS['node_table_checks'] += 1
        return ids, raw, table, {s: joined[s] for s in table}

    _, _, table, witnesses = walk(tree)
    if reference:
        assert (0 in table) == (t in global_domain)
    if 0 not in table:
        return None, max_width
    witness = witnesses[0]
    assert set(witness) == set(range(n))
    total = 0
    for i, d in witness.items():
        assert d in domains[i]
        total ^= d
    assert total == t
    COUNTS['contribution_witness_checks'] += 1
    return witness, max_width


def main():
    # Every subspace and every local subset in F_2^2, paired in every way.
    subspaces = [([], {0}), ([1], {0, 1}), ([2], {0, 2}),
                 ([3], {0, 3}), ([1, 2], {0, 1, 2, 3})]
    modules = []
    for gs, sp in subspaces:
        words = sorted(sp)
        for mask in range(1 << len(words)):
            modules.append((gs, {x for j, x in enumerate(words) if (mask >> j) & 1}))
    assert len(modules) == 30
    for left, right in product(modules, repeat=2):
        COUNTS['exhaustive_domain_instances'] += 1
        gs, ds = [left[0], right[0]], [left[1], right[1]]
        for t in range(4):
            verify(gs, ds, t, (0, 1))
            COUNTS['exhaustive_domain_targets'] += 1

    # Every three-block 2 by 2 binary source matrix, every target, every binary
    # tree on the three labeled leaves. Actual z_i in {01,10,11} are recovered.
    columns = list(product(range(4), repeat=2))
    trees = [(0, (1, 2)), (1, (0, 2)), (2, (0, 1))]
    for matrices in product(columns, repeat=3):
        COUNTS['exhaustive_pair_matrices'] += 1
        gs = [list(x) for x in matrices]
        maps = [{1: a, 2: b, 3: a ^ b} for a, b in matrices]
        ds = [set(mp.values()) for mp in maps]
        brute_targets = set()
        for zs in product((1, 2, 3), repeat=3):
            brute_targets.add(maps[0][zs[0]] ^ maps[1][zs[1]] ^ maps[2][zs[2]])
        for t in range(4):
            for tree in trees:
                witness, _ = verify(gs, ds, t, tree)
                assert (witness is not None) == (t in brute_targets)
                if witness is not None:
                    zs = [next(z for z, d in maps[i].items() if d == witness[i]) for i in range(3)]
                    assert all(z in (1, 2, 3) for z in zs)
                    assert maps[0][zs[0]] ^ maps[1][zs[1]] ^ maps[2][zs[2]] == t
                    COUNTS['source_pair_witness_checks'] += 1
                COUNTS['exhaustive_pair_target_trees'] += 1

    # Higher ambient dimensions and arbitrary local subsets/random trees.
    for _ in range(2500):
        ambient = RNG.randrange(1, 7)
        n = RNG.randrange(1, 8)
        gs = [[RNG.randrange(1 << ambient) for _ in range(RNG.randrange(1, 4))]
              for _ in range(n)]
        ds = [{x for x in span(g) if RNG.randrange(5) != 0} for g in gs]
        tree = random_tree(n)
        COUNTS['random_instances'] += 1
        for t in {0, RNG.randrange(1 << ambient), RNG.randrange(1 << ambient)}:
            verify(gs, ds, t, tree)
            COUNTS['random_targets'] += 1

    # Interval plane family: width at most 2, Fibonacci number of target-zero
    # source witnesses. Count by a separate two-state recurrence, and enumerate
    # the no-adjacent-zeros characterization for m up to 16.
    fib = [0, 1]
    for _ in range(65):
        fib.append(fib[-1] + fib[-2])
    for m in range(2, 65):
        gs = [[1 << i, 1 << (i+1)] for i in range(m)]
        ds = [{a, b, a ^ b} for a, b in gs]
        witness, width = verify(gs, ds, 0, interval_tree(0, m), reference=(m <= 7))
        assert witness is not None and width <= 2
        states = {0: 1, 1: 0}
        for _ in range(m):
            states = {0: states[1], 1: states[0] + states[1]}
        assert states[0] == fib[m-1]
        if m <= 16:
            direct = 0
            for inner in product((0, 1), repeat=m-1):
                seq = (0,) + inner + (0,)
                direct += all(seq[i] or seq[i+1] for i in range(m))
            assert direct == fib[m-1]
        COUNTS['interval_family_checks'] += 1
    result = dict(seed=SEED, all_checks_passed=True, **COUNTS,
                  interval_family_max_m=64, interval_family_max_width=2,
                  family_witnesses_at_m_64=fib[63])
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
