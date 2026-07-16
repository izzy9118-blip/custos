# Repository Operations Manual  
**Version:** 1.0  
**Status:** Operational Guidance

## Purpose

Provide the standard operating procedures required to execute the constitutional specifications consistently, reproducibly, and audibly.

This Manual derives all authority from the certified constitutional specifications.  
If any provision in this Manual conflicts with a constitutional specification, the constitutional specification prevails.

---

## 1. Purpose and Scope

This Manual defines operational procedures for repository work performed under the certified constitutional framework.

It covers operational execution of:
- constitutional admissions;
- register and ledger updates;
- referential-integrity maintenance;
- verification, commit, release, and rollback discipline;
- quality assurance and revision governance for operations guidance.

This Manual does **not**:
- amend constitutional specifications;
- create constitutional authority;
- define or redefine repository semantics;
- create identifier families;
- assign canonical identifiers by itself;
- create canonical repository objects by itself.

---

## 2. Constitutional Authority

### 2.1 Governing Constitutional Documents

Operations under this Manual are subordinate to and constrained by the certified constitutional specifications:

- **Document 000001** — Documentary Ontology  
- **Document 000002** — Identifier Specification  
- **Document 000003** — Relationship Specification  
- **Document 000004** — Controlled Vocabulary Specification  
- **Document 000005** — Constitutional Admission Protocol

### 2.2 Statement of Constitutional Subordination

This Manual is an operational instrument only.  
It implements constitutional requirements and does not alter constitutional meaning, jurisdiction, or hierarchy.

---

## 3. Repository Production Principles

1. **Minimal Modification**  
   Apply only the smallest set of changes required to execute the approved constitutional action.  
   No operational action shall modify unrelated repository content, even where such modifications appear beneficial.

2. **Append-Only Discipline**  
   Where constitutional records are append-only (e.g., ledger entry arrays, audit trails), preserve order and history; do not reorder or rewrite prior entries.

3. **Immutable Historical Record**  
   Preserve historical admissions, assignments, and audit history as immutable except through constitutionally permitted lifecycle mechanisms.

4. **Constitution-Guided Repository Reasoning**  
   Repository operations shall be guided first by the certified constitutional specifications and second by the current certified repository state.  
   Where an inconsistency is detected, constitutional requirements govern the required corrective action.

5. **Constitutional Fidelity**  
   Every operational action must be traceable to existing constitutional specifications or approved governance decisions already adopted under them.

---

## 4. Admission Workflow

### 4.1 Candidate Preparation
- Prepare candidate object content using the approved constitutional template for its object type.
- Limit candidate fields to constitutionally required and approved governance content.

### 4.2 Constitutional Validation
- Validate required fields and constraints against governing constitutional specifications.
- Confirm jurisdiction/responsible authority references are present where required.
- Confirm no unauthorized semantics are introduced.

### 4.3 Documentary Validation
- Confirm documentary basis requirements are present where required.
- Confirm governing references are traceable and recoverable.

### 4.4 Repository Validation
- Confirm identifier uniqueness.
- Confirm register/ledger consistency requirements.
- Confirm referential integrity status (assigned or explicitly planned-not-assigned where constitutionally permitted).

### 4.5 Repository Update Sequence
Execute updates in one coherent admission unit:
1. Create canonical object file.
2. Create identifier assignment file (if required).
3. Update relevant register file (append entry, update required count fields only).
4. Update identifier ledger index file (append-only).

### 4.6 Verification
- Verify expected created files exist.
- Verify expected modified files contain only intended changes.
- Verify no unrelated file modifications.

### 4.7 Admission Completion
Admission is operationally complete only when all required repository updates are present and committed.

---

## 5. Repository Update Rules

### 5.1 Register Updates
- Preserve existing fields.
- Apply minimal, targeted updates.
- Use append-only behavior for entry lists unless a governing specification explicitly permits otherwise.

### 5.2 Ledger Updates
- Preserve existing ledger structure and historical entries.
- Append only the new identifier/reference entries.
- Never remove or reorder historical ledger entries.

### 5.3 Append-Only Requirements
- Treat append-only declarations as strict operational constraints.
- Any correction must be additive or handled through constitutionally permitted lifecycle/revision mechanisms.

### 5.4 Identifier Discipline
- Use only constitutionally authorized identifier families.
- Do not allocate or use identifiers outside approved constitutional governance.
- Do not reuse identifiers.

### 5.5 Cross-Reference Verification
- Verify references resolve to canonical identifiers where assigned.
- If unresolved references are constitutionally permitted, mark explicitly as planned/not-assigned.
- Do not silently convert unresolved to resolved references.

---

## 6. Resolution of Planned Canonical References

### 6.1 Rule

A planned canonical reference is permitted only where governing specifications allow forward reference to a not-yet-admitted canonical object, and the reference is explicitly marked as planned-not-assigned.

When the referenced canonical object is admitted and assigned, corresponding planned references shall be resolved at the next dependent admission action or within the same production cycle.

Resolution is limited to reference-state updates only, including:
- referenced identifier value (e.g., `null` to assigned identifier),
- reference assignment status (e.g., `PLANNED_NOT_ASSIGNED` to `ASSIGNED`),
- minimal auditable note of resolution event where audit recording is required.

Resolution shall not alter:
- predicate or object semantics,
- governance decisions,
- constitutional meaning,
- prior historical admission content.

Planned-reference resolution is **referential-integrity maintenance**, not a new constitutional admission.

---

## 7. Repository Verification

For each admission/update action, verify:

1. **Files Created**  
   Required new files exist at approved paths.

2. **Files Modified**  
   Only approved existing files changed; unchanged sections preserved where required.

3. **Register Consistency**  
   Register entries and required count fields remain consistent.

4. **Ledger Consistency**  
   Assignment records and ledger index entries remain consistent and append-only.

5. **Referential Integrity**  
   References are correctly resolved or explicitly and constitutionally marked as planned.

6. **No Unrelated Changes**  
   No collateral modifications outside approved operational scope.

---

## 8. Commit and Release Procedure

### 8.1 Commit Discipline
- Commit only approved scope changes.
- Use commit messages that clearly state constitutional action performed.
- Avoid mixed-purpose commits.

### 8.2 Verification After Commit
- Re-open modified/created files from repository state at commit.
- Confirm required changes are present and no unrelated files changed.
- Confirm append-only and ordering constraints are preserved.

### 8.3 Rollback Guidance
- If verification fails, apply targeted corrective commit or revert affected commit(s) according to repository policy.
- Preserve auditability of rollback actions.
- Do not rewrite history in ways that violate repository governance policy.

### 8.4 Documentation Requirements
- Record operational verification summary with:
  - files created;
  - files modified;
  - constitutional/documentary/repository validation outcomes;
  - final admission/maintenance status.

---

## 9. Quality Assurance Checklist

Before closing any operational action, confirm all items:

- [ ] Constitutional compliance checked against Documents 000001–000005.
- [ ] Documentary compliance checked where required.
- [ ] Identifier uniqueness and assignment integrity verified.
- [ ] Register updates correct and minimal.
- [ ] Ledger updates append-only and ordered.
- [ ] Referential integrity verified (resolved or explicitly planned).
- [ ] No unrelated repository changes.
- [ ] Audit trail/documentation complete.

---

## 10. Revision Policy

1. **Semantic Versioning**  
   Revisions use semantic version labels (e.g., 1.0, 1.1, 2.0).

2. **Changelog Required**  
   Every revision includes a clear changelog of operational changes.

3. **Constitutional Compatibility Statement Required**  
   Every revision includes an explicit statement confirming compatibility with Documents 000001–000005 and identifying any constraints.

4. **Operational Evolution Constraint**  
   This Manual may evolve operationally but shall never alter constitutional meaning or authority.

---

## Operational Principle

This Manual exists solely to ensure faithful execution of the constitutional specifications.

Operational convenience shall never take precedence over constitutional fidelity.

Where uncertainty exists, repository operators shall seek constitutional clarification rather than introducing operational assumptions.

## SELF-AUDIT

1. **Any section accidentally creating constitutional authority?**  
   No. All sections are operational and explicitly subordinate to constitutional specifications.

2. **Any section conflicting with Documents 000001–000005?**  
   No conflict identified. The Manual defers to constitutional documents in all cases.

3. **Any operational rule exceeding constitutional authority?**  
   No. Rules are implementation discipline for admitted constitutional structure and repository integrity.

4. **Does the Manual remain entirely subordinate to the Constitution?**  
   Yes. Subordination is explicit, repeated, and enforced throughout.

**READY FOR OPERATIONAL ADOPTION**
