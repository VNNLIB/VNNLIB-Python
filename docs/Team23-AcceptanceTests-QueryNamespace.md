# Acceptance tests: Query namespace migration

**Component:** VNNLIB-Python query namespace  
**Date:** 1 October 2026  
**Reviewer:** Pending independent review

Three high-level tests check new API availability, legacy compatibility and warnings, and consistency between old and new usage.

## Environment

| Item | Reference |
|---|---|
| Remote repository | `VNNLIB/VNNLIB-Python` |
| Remote branch | `query-namespace-migration` at `ccb867d` |
| Remote main | `ccb867d` |
| Python package | `vnnlib` 1.1 |
| VNN-LIB language | 2.0 |
| Test dependencies | pytest and mypy |

The remote references above precede these test additions.

## Traceability

| Test | Sprint 1 criteria |
|---|---|
| AT-QN-1: New API availability | AT-1.1, AT-1.7 |
| AT-QN-2: Legacy API and warnings | AT-1.2, AT-1.3 |
| AT-QN-3: Functionality and consistency | AT-1.5, AT-1.6 |

**Note.** AT-1.8 will be assessed as part of the project's overall build, packaging and installation acceptance tests.

## AT-QN-1 — New API availability

**Requirement.** All 34 public symbols are accessible through `vnnlib.query`, retain their object identity, and remain available to Python type checking.

**Procedure.** Run the existing seven export-group tests and the namespace typing test. The typing test checks the stubs and typing marker, accesses all 34 symbols through both module paths, verifies compatible types, and checks that incorrect parser-result assignments are rejected.

**Expected.** All exports resolve to the original objects; correct types pass mypy and both incorrect assignments fail.

**Actual.** All **22/22 tests passed**, including the positive and negative typing checks.

**Result: PASS**

## AT-QN-2 — Legacy API and warnings

**Requirement.** Legacy exports remain usable and emit exactly one `DeprecationWarning` naming the replacement path. New-path access emits none.

**Procedure.** Check all 34 symbols through `vnnlib.<symbol>`, recording every warning with the `always` filter. Also check `vnnlib.query.<symbol>`, object identity, and invalid-name handling.

**Expected.** Each legacy access emits one correctly worded warning; new-path access emits none.

**Actual.** All **4/4 tests passed**. Direct root access preserves object identity and emits one correctly worded warning per symbol. New-path access emits no warnings.

**Result: PASS**

## AT-QN-3 — Functionality and consistency

**Requirement.** Existing functionality remains usable, and the README example produces identical results through old and new paths.

**Procedure.** Execute the README example unchanged with a valid specification, then execute its new-path equivalent with the same file. Compare query text and printed assertions, and inspect warnings. Run the existing compat suite unchanged.

**Expected.** Both examples produce identical, non-empty output; only the legacy example warns. Existing compat tests pass.

**Actual.** The README comparison passed. The legacy example emitted one warning and the new example emitted none. Existing compat tests passed **15/15**, giving **16/16 tests passed** for this acceptance test.

**Result: PASS**

## Evidence and overall result

```bash
python -m pytest test/test_query_namespace.py test/test_compat_transformer.py -q
python -m pytest test -q
```

| Check | Result |
|---|---|
| Namespace tests | 27 passed |
| Existing compat tests | 15 passed |
| Full pytest suite | 104 passed |
