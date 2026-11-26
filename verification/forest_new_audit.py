#!/usr/bin/env python3
"""Exact finite audit of matching crossing covers and conservation coefficient seven.

Standard library only. Run with Python 3.10 or newer. This is finite evidence for
the stated constructions, not an asymptotic proof or a general SAT algorithm.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import random
import time

SEED = 20261126
CONTROL_POSITIVE = [
    (0, 1, 2), (0, 3, 4), (5, 6, 7), (6, 8, 9),
    (8, 10, 11), (3, 7, 10), (2, 4, 9), (1, 5, 11),
]
CONTROL_NEGATIVE = [
    (5, 6, 8), (0, 1, 11), (2, 3, 7), (4, 7, 8),
    (2, 5, 9), (1, 3, 10), (0, 4, 6), (9, 10, 11),
]


def validate_formula(n, clauses):
    assert len(clauses) == 4 * n // 3
    for sign in (0, 1):
        part = [tuple(sorted(c)) for s, c in clauses if s == sign]
        assert len(set(part)) == len(part)
        counts = Counter(v for c in part for v in c)
        assert counts == Counter({v: 2 for v in range(n)})
        assert all(len(c) == len(set(c)) == 3 for c in part)


def make_projection(n, clauses, preference):
    parent = list(range(n))

    def root(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    normalized = []
    for sign, clause in clauses:
        owners = tuple(v for v in clause if ((preference >> v) & 1) == sign)
        negative = tuple(v for v in clause if v not in owners)
        for v in owners[1:]:
            parent[root(v)] = root(owners[0])
        normalized.append((owners, negative))
    blocks = defaultdict(list)
    for v in range(n):
        blocks[root(v)].append(v)
    block_of = {v: b for b, vs in blocks.items() for v in vs}
    outputs = defaultdict(set)
    obligations = defaultdict(list)
    nonlinear_clause_sets = []
    for owners, negative in normalized:
        grouped = defaultdict(list)
        for v in negative:
            grouped[block_of[v]].append(v)
        signals = []
        nonlinear_in_clause = []
        for b, vs in grouped.items():
            group = tuple(sorted(vs))
            outputs[b].add(group)
            signals.append((b, group))
            if len(group) >= 2:
                nonlinear_in_clause.append(group)
        assert len(nonlinear_in_clause) <= 1
        nonlinear_clause_sets.append(nonlinear_in_clause)
        if owners:
            b = block_of[owners[0]]
            assert all(block_of[v] == b for v in owners)
            assert all(a != b for a, _ in signals)
            obligations[b].append((owners, tuple(signals)))
    return {
        "blocks": dict(blocks),
        "outputs": {b: sorted(outputs[b]) for b in blocks},
        "obligations": {b: obligations[b] for b in blocks},
        "nonlinear_clause_sets": nonlinear_clause_sets,
    }


def crossing_data(supports):
    supports = sorted(set(tuple(sorted(s)) for s in supports if len(s) >= 2))
    membership = defaultdict(list)
    crossing_edges = set()
    for i, group in enumerate(supports):
        for v in group:
            membership[v].append(i)
        crossing_edges.update(tuple(sorted(e)) for e in combinations(group, 2))
    assert all(len(js) <= 2 for js in membership.values())
    root_edges = {}
    next_dummy = len(supports)
    for v, js in sorted(membership.items()):
        if len(js) == 2:
            root_edges[v] = tuple(js)
        else:
            root_edges[v] = (js[0], next_dummy)
            next_dummy += 1
    degrees = Counter(a for e in root_edges.values() for a in e)
    assert max(degrees.values(), default=0) <= 3
    reconstructed = {
        (v, w) for v, w in combinations(sorted(root_edges), 2)
        if set(root_edges[v]) & set(root_edges[w])
    }
    assert crossing_edges == reconstructed
    return set(membership), crossing_edges, root_edges


def maximum_root_matching(root_edges):
    """Exact root-graph matching, using a vertex recurrence independent of cover DP."""
    pair_label = {}
    for label, (u, v) in sorted(root_edges.items()):
        pair_label.setdefault(tuple(sorted((u, v))), label)
    adjacency = defaultdict(set)
    for u, v in pair_label:
        adjacency[u].add(v)
        adjacency[v].add(u)
    all_vertices = frozenset(adjacency)

    @lru_cache(None)
    def solve(vertices):
        if not vertices:
            return ()
        u = min(vertices)
        best = solve(vertices - {u})
        for v in sorted(adjacency[u] & vertices):
            candidate = (pair_label[tuple(sorted((u, v)))],) + solve(vertices - {u, v})
            if len(candidate) > len(best):
                best = candidate
        return best

    answer = solve(all_vertices)
    used = [a for label in answer for a in root_edges[label]]
    assert len(set(used)) == len(used)
    return set(answer)


def minimum_crossing_cover(crossing_edges):
    """Independent exact cover calculation by branching on an uncovered edge."""
    @lru_cache(None)
    def solve(edges):
        if not edges:
            return ()
        u, v = edges[0]
        left = (u,) + solve(tuple(e for e in edges if u not in e))
        right = (v,) + solve(tuple(e for e in edges if v not in e))
        return left if len(left) <= len(right) else right

    return set(solve(tuple(sorted(crossing_edges))))


def audit_projection(n, clauses, preference, stats):
    data = make_projection(n, clauses, preference)
    nonlinear = set()
    cover = set()
    for b in data["blocks"]:
        support, crossing, root_edges = crossing_data(data["outputs"][b])
        matching = maximum_root_matching(root_edges)
        candidate = support - matching
        reference = minimum_crossing_cover(crossing)
        assert all(u in candidate or v in candidate for u, v in crossing)
        assert len(candidate) == len(reference)
        assert len(support) <= 3 * len(candidate)
        nonlinear.update(support)
        cover.update(candidate)
        stats["blocks_with_line_graph_checked"] += 1
        stats["nonempty_crossing_graphs"] += bool(support)
    d = len(nonlinear)
    k = len(cover)
    dirty = [c for _, c in clauses if any(v in nonlinear for v in c)]
    t = len(dirty)
    duplication = sum(len(set(c) & nonlinear) - 1 for c in dirty)
    assert duplication == 4 * d - t
    independent = nonlinear - cover
    selected_clauses = []
    for u in independent:
        chosen = next(
            i for i, groups in enumerate(data["nonlinear_clause_sets"])
            if any(u in group for group in groups)
        )
        selected_clauses.append(chosen)
    assert len(selected_clauses) == len(set(selected_clauses))
    assert len(independent) <= 2 * k
    assert duplication >= d - k
    assert t - d <= 2 * d + k <= 7 * k
    stats["preference_words_checked"] += 1
    stats["coefficient_seven_incidence_checks"] += 1
    stats["max_nonlinear_support"] = max(stats["max_nonlinear_support"], d)
    return data


def local_conditions(data, b, pins):
    positive = [
        owners for owners, incoming in data["obligations"][b]
        if all(pins.get(signal) == 1 for signal in incoming)
    ]
    capped = [group for group in data["outputs"][b] if pins.get((b, group)) == 0]
    return positive, capped


def satisfies_local(true_variables, positive, capped):
    return (
        all(any(v in true_variables for v in clause) for clause in positive)
        and all(not all(v in true_variables for v in group) for group in capped)
    )


def matching_local_oracle(variables, positive, capped):
    support, crossing, root_edges = crossing_data(capped)
    matching = maximum_root_matching(root_edges)
    cover = sorted(support - matching)
    for word in range(1 << len(cover)):
        fixed = {v: ((word >> i) & 1) for i, v in enumerate(cover)}
        forced_zero = set()
        contradiction = False
        for group in capped:
            if any(fixed.get(v) == 0 for v in group):
                continue
            live = [v for v in group if v not in fixed]
            assert len(live) <= 1
            if not live:
                contradiction = True
                break
            forced_zero.add(live[0])
        if contradiction:
            continue
        true_variables = {v for v in variables if fixed.get(v, 1) == 1 and v not in forced_zero}
        if satisfies_local(true_variables, positive, capped):
            return true_variables
    return None


def brute_local_oracle(variables, positive, capped):
    for word in range(1 << len(variables)):
        true_variables = {v for i, v in enumerate(variables) if (word >> i) & 1}
        if satisfies_local(true_variables, positive, capped):
            return true_variables
    return None


def audit_queries(data, rng, stats, queries_per_block=12):
    for b, variables in data["blocks"].items():
        signals = set((b, s) for s in data["outputs"][b])
        signals.update(s for _, incoming in data["obligations"][b] for s in incoming)
        signals = sorted(signals)
        for query in range(queries_per_block):
            if query == 0:
                pins = {}
            elif query == 1:
                pins = {s: 0 for s in signals}
            elif query == 2:
                pins = {s: 1 for s in signals}
            else:
                pins = {}
                for signal in signals:
                    value = rng.randrange(3)
                    if value < 2:
                        pins[signal] = value
            positive, capped = local_conditions(data, b, pins)
            actual = matching_local_oracle(variables, positive, capped)
            expected = brute_local_oracle(variables, positive, capped)
            assert (actual is None) == (expected is None)
            if actual is not None:
                assert satisfies_local(actual, positive, capped)
                stats["local_queries_sat"] += 1
            else:
                stats["local_queries_unsat"] += 1
            stats["local_queries_compared_to_exhaustive_search"] += 1
            stats["max_local_block_size_in_query_tests"] = max(
                stats["max_local_block_size_in_query_tests"], len(variables)
            )


def generate_formula(n, rng):
    clauses = []
    for sign in (0, 1):
        for _ in range(100000):
            stubs = list(range(n)) * 2
            rng.shuffle(stubs)
            triples = [tuple(sorted(stubs[i:i+3])) for i in range(0, 2*n, 3)]
            if all(len(set(c)) == 3 for c in triples) and len(set(triples)) == len(triples):
                clauses.extend((sign, c) for c in triples)
                break
        else:
            raise RuntimeError("failed to generate a proper balanced source")
    validate_formula(n, clauses)
    return clauses


def main():
    started = time.monotonic()
    rng = random.Random(SEED)
    stats = Counter()
    control = [(0, c) for c in CONTROL_POSITIVE] + [(1, c) for c in CONTROL_NEGATIVE]
    validate_formula(12, control)
    query_preferences = {0, (1 << 12) - 1} | set(rng.sample(range(1 << 12), 62))
    for preference in range(1 << 12):
        data = audit_projection(12, control, preference, stats)
        if preference in query_preferences:
            audit_queries(data, rng, stats)
    generated_manifest = []
    for n in (6, 9, 12):
        for trial in range(12):
            clauses = generate_formula(n, rng)
            preferences = [0, (1 << n) - 1] + [rng.randrange(1 << n) for _ in range(6)]
            for preference in preferences:
                data = audit_projection(n, clauses, preference, stats)
                audit_queries(data, rng, stats, queries_per_block=8)
            generated_manifest.append({"n": n, "trial": trial, "clauses": clauses, "preferences": preferences})
    stats["generated_balanced_formulas"] = len(generated_manifest)
    payload = {
        "status": "all_assertions_passed",
        "seed": SEED,
        "scope": "Finite exact construction audit; no asymptotic completeness claim.",
        "control": {"n": 12, "positive": CONTROL_POSITIVE, "negative": CONTROL_NEGATIVE},
        "control_preferences": 4096,
        "stats": dict(sorted(stats.items())),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "generated_cases": generated_manifest,
    }
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "generated_cases"}, indent=2))


if __name__ == "__main__":
    main()
