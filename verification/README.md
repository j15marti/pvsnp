# Reproducibility supplement: November 26, 2026

These are the three original Python verification programs distributed with [Exact Forest and Algebraic Interfaces for Satisfiability](../documents/PNP_Exact_Interfaces_Manuscript_2026-11-26.txt). The uploaded Git blobs were checked against the original source package.

## Run locally

Use Python 3.10 or later. No third-party dependencies, credentials, or network access are required by the scripts. Keep Python assertions enabled (do not use `-O` or set `PYTHONOPTIMIZE`).

```bash
git clone https://github.com/j15marti/pvsnp.git
cd pvsnp/verification
python3 forest_new_audit.py
python3 algebraic_interface_audit.py
python3 hybrid_rank_audit.py
```

Each script prints its results and generates its corresponding JSON file alongside the script. The forest audit also records the generated source instances and preferences. Runtime is machine-dependent.

## Expected results

All three original scripts were rerun successfully on November 26, 2026, with these counts:

| Script | Finite check | Count |
| --- | --- | ---: |
| [forest_new_audit.py](forest_new_audit.py) | Line-graph identities | 13,056 |
| | Nonempty crossing graphs (independent cover and matching comparisons) | 8,436 |
| | Coefficient-seven incidence checks | 4,384 |
| | Local extension queries compared to exhaustive search | 7,620 |
| [algebraic_interface_audit.py](algebraic_interface_audit.py) | Algebraic node-table comparisons | 292,756 |
| | Reconstructed nonzero-pair source witnesses | 47,955 |
| | Interval-family checks (up to 64 modules) | 63 |
| [hybrid_rank_audit.py](hybrid_rank_audit.py) | Joint 2-CNF/affine checks | 251,955 |

## Scope

- The forest audit deliberately uses an independent exact matching recurrence and cover branching for small controls; it is not an implementation of a polynomial-time blossom algorithm. It tests the structural inequalities underlying the coefficient-seven bound, not all implicit projected fractional LPs.
- The algebraic audit uses explicit small domains and supplied trees to compare dynamic-programming tables and witness reconstruction. It does not establish polynomial-time discovery of suitable trees for arbitrary instances.
- The hybrid audit exhausts the distinct nonempty 2-CNF relations and ordered independent affine systems on three variables. It tests variable seeds rather than independently auditing the sharper SCC enumeration bound.
- These are finite reproducibility checks, not a general SAT solver or a proof of the universal acquisition conjecture. The manuscript's implication to P = NP remains conditional.

## Original SHA-256 checksums

```text
2c44f29be7ed2270739d2993a1153c3dddcf4e02b0daad52f54f2410b6fffb53  forest_new_audit.py
8f7c2afeb4703551105ce31dfdb68eeb0f675768c192c3464c09b2d2c693a3bd  algebraic_interface_audit.py
944ea999d4d033973a34e80a9351256bc40202918eea9ce52676c34384a4060e  hybrid_rank_audit.py
```
