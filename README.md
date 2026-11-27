# P versus NP: Exact Forest and Algebraic Interfaces

**Research status (26 November 2026): conditional constructive theorem; P versus NP remains open.**

This project investigates whether a uniform deterministic polynomial-time algorithm for an NP-complete satisfiability problem can be constructed through exact constraint transformations, cooperative solver tracks, and provably bounded aggregate computation.

## Current E/B model manuscript (27 November 2026)

**Signed Four-Port Equality–Balance Networks:** formal model, NP-completeness reduction, canonical contraction and cooperative certificate framework. The universal aggregate-contraction theorem and P versus NP remain open.

- [LaTeX manuscript and build instructions](documents/EB4_model_2026-11-27/README.md)
- [Exact LaTeX source](documents/EB4_model_2026-11-27/eb4_model.tex) and [bibliography](documents/EB4_model_2026-11-27/references.bib)
- [Shared E/B instance registry and SHA-256 fingerprints](https://github.com/j15marti/pnp/blob/0c14cdc57925788cf7a451dcd5aa171dce860f2c/research/coordination/shared-eb-2026-11-27/instance-registry-v1.json)
- [Public proof release and independent audit protocol](https://github.com/j15marti/pnp/blob/fc87c43ad1a247e4133b931911f7cfa4afeb17c0/research/coordination/2026-11-27_PUBLIC_PROOF_RELEASE_GATE.md)

The source and bibliography match the original locally compiled manuscript. The binary PDF upload is pending; it can be rebuilt using the documented LaTeX commands. These are model definitions, established scoped lemmas, and a conditional research framework, not a claimed resolution.

## Current manuscript

**Jeremy Martinez, _Exact Forest and Algebraic Interfaces for Satisfiability: A constructive framework and a conditional theorem for P = NP_, 26 November 2026.** Research manuscript prepared with AI assistance for mathematical review.

- [Full manuscript, text edition (21-page PDF extraction)](documents/PNP_Exact_Interfaces_Manuscript_2026-11-26.txt)
- The text edition includes the theorem statements, proofs, limitations, verification record and references. Mathematical notation and figures may be degraded by PDF extraction; the original typeset PDF is not yet stored in this repository.

## Constructive proof spine

The starting problem is proper, clause-distinct **Monotone 3-SAT-(2,2)**, with exactly two positive and two negative occurrences per variable. This NP-complete class is distinct from exact-two-of-four SAT. For $n$ variables there are $4n/3$ clauses. See [Döcker (2019)](https://arxiv.org/abs/1912.08032).

1. Compile the source into two clause multigraphs sharing the variable-edge labels. Matroid union constructs a simultaneous partition into forests in polynomial time.
2. Form exact activation-signal relations with disjoint private domains. The upper-bound signal projection preserves satisfiability and permits reconstruction of a source witness.
3. Solve admitted local and global interfaces through matching, fractional q-Horn backdoors, affine/binary compatibility, and algebraic-interface dynamic programming.
4. Permit multiple cooperating tracks to share certified information and execute bounded exponential local computations, provided the aggregate work is polynomial.
5. Verify reconstructed witnesses against the original input. A terminal that declines its structural promise does not certify UNSAT.

## Main results in the November 26 revision

| Result | Scope and significance |
| --- | --- |
| Simultaneous forest acquisition (Theorem 2.2) | Polynomial-time construction for the balanced source; certificates persist under pinning and clause deletion as stated in Proposition 2.3. |
| Exact upper-bound projection (Theorem 3.1) | Preserves existential feasibility, not model counts. |
| Optimal crossing covers (Theorems 4.1–4.2) | Each crossing graph is the line graph of a subcubic multigraph. Minimum vertex cover is acquired by maximum matching; local extension takes $2^{\tau_B(Q)}\operatorname{poly}(N)$ time. |
| Projected q-Horn terminal (Theorem 5.2; Corollary 5.3) | With exact local oracles and integer guard budget $k$, the combined terminal takes $2^{\tau_{\max}+6k}\operatorname{poly}(N)$ time or soundly declines. |
| Sharpened conservation inequality (Theorem 6.3) | The original representation satisfies $\rho_{\rm signal}+7\tau_\Sigma\ge n/3$, improving the previous coefficient of 15. This is a representation-specific obstruction, not a general complexity lower bound. |
| Algebraic-interface composition (Theorem 7.1) | Exact dynamic programming over shared linear spans, with explicit decomposition, query, join and reconstruction costs. |
| Infinite low-interface family (Theorem 7.5) | Strictly rank-expanding punctured-plane systems can have interface width at most two despite exponentially many witnesses. |
| Mixed 2-CNF/affine feasibility (Theorem 8.1) | Polynomial for fixed affine rank, with the stated enumeration bound. Logarithmic rank alone gives a quasipolynomial bound for this terminal. |
| Charged recursive computation | A strict polynomial-potential decrease bounds all executed child jobs when its hypotheses are met. |

For algebraic modules whose contributions satisfy a binary linear equation, let $V_S$ be the span of the contributions from a group $S$. The interface is

$$
\mathcal B_S=V_S\cap V_{\overline S}.
$$

After translating the target to zero as in the manuscript, two disjoint child groups $A,B$ compose via

$$
T_S=(T_A+T_B)\cap\mathcal B_S,\qquad S=A\dot\cup B.
$$

This avoids enumerating the Cartesian product of all local assignments at once, but requires affordable exact local queries and acquisition of a suitable decomposition.

A sufficient recursion-budget certificate is

$$
\sum_i \mu(R_i)^c \le \mu(R)^c-1,
$$

for a fixed exponent and positive integer measure, charging every executed child and the stated local overhead. Neither this inequality nor small interface width has been proved universally available.

## The remaining proof obligation

**Conjecture 11.2 (Universal affordable acquisition or contraction).** In the manuscript's authenticated state domain, a fixed uniform deterministic procedure must find, on every relevant satisfiable unfinished residual, a verified witness, an exact affordable terminal, or a sound witness-liftable reduction with strictly decreasing polynomially bounded global credit. All discovery, failed probes, preprocessing, compatibility, recursion, storage and reconstruction must fit fixed polynomial bounds in the original encoded input length.

**Theorem 11.3.** Conjecture 11.2 implies $P=NP$.

The conditional argument is to run the proposed witness finder with its hypothesized uniform polynomial clock and verify every returned source witness. Satisfiable inputs would yield a verified witness within that clock, and unsatisfiable inputs could not yield one. NP-completeness then supplies the class equality.

The universal acquisition or contraction conjecture is **not proved**. The repository therefore does not claim an unconditional proof of $P=NP$ or $P\ne NP$. In particular, inexpensive supplied interfaces, local correctness, successful finite tests, and restricted-model obstructions do not establish a uniform worst-case polynomial decision bound.

## Reproduce the computational audits

The [verification supplement](verification/README.md) includes all three original Python audit programs, their expected results, scope limitations, and SHA-256 checksums. Each uploaded file matches the original manuscript source package. All three audits were rerun successfully on November 26, 2026.

```bash
git clone https://github.com/j15marti/pvsnp.git
cd pvsnp/verification
python3 forest_new_audit.py
python3 algebraic_interface_audit.py
python3 hybrid_rank_audit.py
```

Python 3.10 or later is sufficient; no third-party packages are required. Keep assertions enabled. Each program generates its adjacent JSON results.

## Verification and research directions

The manuscript reports targeted finite audits, including 13,056 line-graph identities, 7,620 exhaustive-reference local extension queries, 292,756 algebraic interface-table comparisons, and 251,955 mixed 2-CNF/affine comparisons. These are reported computational controls, not independent peer review or a substitute for the missing universal theorem.

The research priorities are exact contextual compatibility, polynomial acquisition of algebraic interfaces, shared-hub and forest contractions, and a universal progress or obstruction theorem. Arithmetic complexity and formal polynomial identity techniques are useful analogies, but formal polynomial computation and Boolean decision computation are distinct; an arithmetic separation alone does not settle P versus NP.

See the manuscript for the detailed theorem hypotheses, counterexamples, proofs, citations and audit limitations. Mathematical criticism and independent verification are welcome.
