# STRAUSSIAN DOCUMENTARY MEMORY
# CANDIDATE COGNITIVE COMPONENT REGISTER ADMISSION DECISION

**Canonical Decision Identifier:** DDR-000000007

**Decision Version:** 1.0

**Decision Outcome:** ADMITTED

**Candidate Identifier:** REG-000000003

**Candidate Class:** Register

**Responsible Admission Authority:** CAG-000000006 — Repository Admission Authority

**Effective Date:** 2026-07-20

**Governing Basis:** Documents 000001–000005; Document 000005 read with AMD-000000002; SPEC-000000002; SPEC-000000003; DDR-000000001

## I. DECISION

CAG-000000006 admits REG-000000003, the Candidate Cognitive Component
Register v1.0, as the active canonical register required by
SPEC-000000003.

The canonical register is recorded at:

`registers/candidate-cognitive-component-register/REG-000000003.yaml`

The complete candidate entry is stored once in the canonical register and
resolves to a separate candidacy decision. No duplicate candidate-record tree
is maintained.

## II. PRECONDITIONS

1. **Class legibility:** Register is canonical ontology class 54.
2. **Identifier legibility:** REG is the established identifier family for
   Register; REG-000000003 is newly allocated by CAG-000000002.
3. **Authority legibility:** CAG-000000006 is active and has final ordinary
   native-admission decision jurisdiction under AMD-000000002.
4. **Specification legibility:** SPEC-000000003 requires a Candidate Cognitive
   Component Register and defines its minimum entry fields, preservation rule,
   and separation from production authority.
5. **Dependency legibility:** SPEC-000000002 and SPEC-000000003 are admitted
   active specifications.
6. **Record legibility:** The canonical register, fixity, lifecycle, version,
   assignment, validation, decision, and audit records are recoverable.

## III. SPECIALIZED-AUTHORITY DETERMINATIONS

The following determinations are separately recorded and remain attributable to
their own authorities:

1. VAL-000000021 — Ontology conformity — CAG-000000001 — PASS.
2. VAL-000000022 — Identifier conformity and allocation — CAG-000000002 — PASS.
3. VAL-000000023 — Predicate and relationship conformity — CAG-000000003 — PASS.
4. VAL-000000024 — Controlled-vocabulary conformity — CAG-000000004 — PASS.

CAG-000000006 verifies their completeness and resolution but does not perform
or absorb those specialized determinations.

## IV. ADMISSION EFFECTS

1. REG-000000003 becomes the admitted, active Candidate Cognitive Component
   Register.
2. The register implements the complete candidacy and register-entry fields
   required by Sections IV and XI of SPEC-000000003.
3. Its entry list is append-preserving and deterministically ordered by
   `designation_date_then_component_identifier`.
4. Rejected or withdrawn candidates remain preserved in the register's audit
   history and are not silently deleted.
5. Its initial admitted state contains zero entries. Infrastructure admission
   is distinct from candidate designation.
6. The initial Version Record and Identifier Assignment Ledger update become
   active as part of this admission unit.

## V. FUTURE ENTRY GOVERNANCE

A future candidate entry must resolve to an already admitted native canonical
artifact and to a separate Documentary Decision Record. The entry must state
the documentary basis, candidacy reason, intended scope and use, limitations,
validation status, current outcome, and audit history.

CAG-000000006 governs only the native admission of this Register through this
decision. This decision does not grant CAG-000000006 or any other authority an
unstated candidacy, validation, certification, integration, Manifest-release,
or activation jurisdiction.

## VI. GOVERNANCE BOUNDARY

This decision creates the register infrastructure only. It does not enter
HOC-000000001 or any other artifact, change certification eligibility, issue a
cognitive-integration decision, release a Manifest, authorize production use,
or authorize Neo4j projection.

## VII. NEXT GOVERNED ACTION

Before HOC-000000001 can be designated and entered, the Repository must identify
or establish a jurisdictionally legible Responsible Authority for candidate
designation. The candidacy decision and register append shall then occur as one
separate governed unit.

**END OF DECISION**
