
STRAUSSIAN DOCUMENTARY MEMORY

RELATIONSHIP SPECIFICATION
Version 1.0

Document Number: 000003
Classification: Foundational Constitutional Specification
Status: Provisional Constitutional Baseline (Predicate Register Incomplete)
Authority: Defines canonical predicates and relationship assertions in the Straussian Documentary Memory


## PREAMBLE

The Relationship Specification answers: **How are entities related to one another?**

This Specification:
- Defines what constitutes a canonical Relationship Assertion
- Establishes identity and immutability rules for Relationship Assertions
- Defines cardinality and status rules
- Integrates Evidence Types (from Controlled Vocabulary Specification)
- Establishes governance authority for predicates

This Specification does NOT:
- Define entity classes (Documentary Ontology v1.1)
- Assign identifier families (Identifier Specification v1.0)
- Govern controlled vocabulary (Controlled Vocabulary Specification v1.0)

**NOTE ON COMPLETENESS (Principle 9):**

The complete Canonical Predicate Register has NOT been fully audited and validated.

This Specification establishes the constitutional framework for relationships.

Full predicate register validation is required before certification.

---

## I. RELATIONSHIP ASSERTION FUNDAMENTALS

### I.1 Definition

A Relationship Assertion is a formal statement that Subject is related to Object through Predicate.

```
Relationship Assertion (REL-xxxxxxx):
  Subject: [Entity identifier from Ontology v1.1]
  Predicate: [Canonical predicate from Predicate Register]
  Object: [Entity identifier from Ontology v1.1]
  Evidence Type: Primary [DOCUMENTARY|PROCEDURAL|COMPARATIVE|STRUCTURAL|REPOSITORY]
  Additional Evidence Types: [zero or more]
  Epistemic Status: [from Epistemic Classification family]
  Lifecycle Status: [ACTIVE|SUPERSEDED|WITHDRAWN|TOMBSTONED]
  Version History: [complete record of changes]
  Audit Trail: [authority, date, decisions]
```

### I.2 REL Identifiers (Principle 2)

Every documented Relationship Assertion receives a permanent REL identifier.

**Immutability Rule:**

If the **subject, predicate, object, or propositional meaning** changes, create a **new REL identifier** and mark the original as **SUPERSEDED** or **WITHDRAWN**.

```
Original REL-000000100:
  Subject: WK-000000001
  Predicate: PRD-000000013 (SUPPORTS)
  Object: CLM-000000042
  Meaning: Work directly supports Claim

Discovery: The relationship is weaker; provides context, not direct support.

Action:
  Create REL-000000101:
    Subject: WK-000000001
    Predicate: PRD-000000017 (CONTEXTUALIZES)
    Object: CLM-000000042
    Meaning: Work contextualizes Claim
  
  Mark REL-000000100 as SUPERSEDED
  COR-xxxxxx documents the change

Result:
  REL-000000100 preserved in history, marked SUPERSEDED
  REL-000000101 is current assertion
  No silent reinterpretation
  Complete audit trail
```

### I.3 Status Changes Without Creating New REL (Principle 2)

Status changes (review, dispute, confirmation, revision notes) may occur without creating a new REL identifier:

```
REL-000000100: WK-000000001 --supports--> CLM-000000042

Status evolution:
  Initial:  Lifecycle: ACTIVE,  Review: (none),     Revision: (none)
  Week 1:   Lifecycle: ACTIVE,  Review: DISPUTED,   Revision: (none)
  Week 2:   Lifecycle: ACTIVE,  Review: CONFIRMED,  Revision: (none)
  Week 3:   Lifecycle: ACTIVE,  Review: CONFIRMED,  Revision: CLARIFIED

All changes appended to REL-000000100's audit trail with timestamps and authority.
Status changes do NOT create new REL identifiers.
```

---

## II. DOCUMENTED VS. INFERRED RELATIONSHIPS (Principle 3)

### II.1 Documented Relationships Receive REL Identifiers

Relationship Assertions that are explicitly created through governance decisions or documentary evidence receive REL identifiers.

These are the primary assertions recorded in the Canonical Relationship Register.

```
Example Documented Assertions:
- REL-000000100: WORK-A --cites--> WITNESS-B
- REL-000000101: CLAIM-1 --supports--> CLAIM-2
- REL-000000102: INTERPRETATION-X --based_on--> HERMENEUTIC_OBJECT-Y
```

### II.2 Query-Time Inferred Relationships (No REL Identifier)

Some relationships are derived through logical operations (transitive closure, rule application) at query time.

These derived relationships do NOT receive REL identifiers unless explicitly materialized.

```
Documented Assertions:
- REL-000000200: WORK-A --derives_from--> MANUSCRIPT-X
- REL-000000201: MANUSCRIPT-X --derives_from--> ORIGINAL

Derived Relationship (computed at query time, no new REL):
  WORK-A --derives_from--> ORIGINAL
  
This is inferred through transitive closure, not a new documented assertion.
```

### II.3 Materialized Inferred Relationships (Explicit Definition Needed)

If an inferred relationship must be formally recorded, materialization must be explicitly decided:

```
Policy Decision: "Transitive derives_from chains must be materialized for audit."

Then:
- REL-000000202: WORK-A --derives_from--> ORIGINAL
  (materialized inferred relationship)
  Marked as: "inferred through transitive closure of REL-200 and REL-201"
  Preserves provenance: links back to REL-200 and REL-201

Result: Inferred relationship has explicit identity and full audit trail.
```

### II.4 Provenance Preservation (Principle 3)

Every inferred relationship must be traceable back to the documented assertions that generated it:

```
Derived from: REL-000000200 + REL-000000201 → REL-000000202
             (source assertions)   (source assertions)  (derived)

Query for provenance of REL-000000202 returns:
  - Derivation rule: "Transitive closure on DERIVES_FROM"
  - Source assertions: REL-000000200, REL-000000201
  - Complete audit trail

Users can verify the derivation and trace back to original documented evidence.
```

---

## III. RELATIONSHIP ASSERTION PROPERTIES

### III.1 Subject and Object Classes

A Relationship Assertion's subject and object must be entity classes defined in Documentary Ontology v1.1.

Subject and object may also be:
- Navigational references to Work or Witness Components (WK-xxxxxxx:book:2, WIT-xxxxxxx:page:87)
- Passages identified by PSG identifier

All subject and object classes must be validated against the Ontology.

### III.2 Cardinality

Relationship Assertions may be:
- **One-to-one:** Subject relates to one Object (and vice versa)
- **One-to-many:** Subject relates to multiple Objects
- **Many-to-one:** Multiple Subjects relate to one Object
- **Many-to-many:** Multiple Subjects relate to multiple Objects

Cardinality is determined by the predicate definition and the specific entities involved.

### III.3 Reflexivity

A Relationship Assertion may have the same entity as subject and object (reflexive):

```
Example: CLAIM-A --contradicts--> CLAIM-A
(A claim may contradict itself — internal inconsistency)

Reflexivity is permitted if:
- The predicate permits reflexivity (defined in predicate entry)
- The relationship is semantically meaningful
- The relationship is explicitly documented

Reflexivity is prohibited if:
- The predicate forbids reflexivity (e.g., DERIVES_FROM cannot be reflexive; no cyclic derivation)
- The predicate definition specifies no reflexive use
```

---

## IV. EVIDENCE AND EVIDENCE TYPES (Principle 6)

### IV.1 Evidence Type Authority and Location

**Constitutional Source:**

Evidence Types are defined in **Controlled Vocabulary Specification v1.0** as five canonical constants.

**Assignment to Relationship Assertions:**

This Specification (Relationship Specification v1.0) defines how Evidence Types are assigned to Relationship Assertions.

### IV.2 The Five Canonical Evidence Types

From Controlled Vocabulary Specification v1.0:

- **DOCUMENTARY**: Evidence recoverable from Witnesses, sources, archival materials
- **PROCEDURAL**: Evidence documented through formal Repository Artifacts (DDR, etc.)
- **COMPARATIVE**: Evidence resulting from explicit comparison of entities
- **STRUCTURAL**: Evidence observable in structure or composition of entities
- **REPOSITORY**: Evidence from Repository investigation, judgment, or curation

### IV.3 Evidence Type Cardinality (Principle 10)

Each Relationship Assertion has:

- **Exactly ONE Primary Evidence Type** (required): from the five canonical types
- **Zero or more Additional Evidence Types** (optional): from the five canonical types

```
Example:

REL-000000300: WORK-A --supports--> CLAIM-1

Primary Evidence Type: DOCUMENTARY
  (Primary basis: direct quote from source)

Additional Evidence Types: COMPARATIVE, STRUCTURAL
  (Also supported by: comparison with other works; structural pattern matching)

This assertion is grounded primarily in documentary evidence, 
but also supported by comparative and structural analysis.
```

### IV.4 Evidence Record vs. Relationship Assertion Evidence Type (Principle 6)

**Distinction:**

- **Evidence Record (EVR):** Documents **what evidence exists** (specific passages, analyses, proofs)
- **Relationship Assertion Evidence Type:** Indicates **the evidentiary basis** for this specific relationship

```
Example:

EVR-000000089:
  Documents: A comparative analysis of three manuscripts
  Content: Detailed side-by-side comparison
  
REL-000000300: WORK-A --supports--> CLAIM-1
  Primary Evidence Type: COMPARATIVE
  Evidence used: EVR-000000089 (among possibly others)

A single Evidence Record may support multiple Relationship Assertions 
with different Evidence Types.

A Relationship Assertion's Evidence Type indicates which kind of 
evidentiary basis the assertion rests on; the Evidence Record 
documents the detailed evidence.
```

---

## V. RELATIONSHIP ASSERTION STATUS AND LIFECYCLE (Principle 5)

### V.1 Lifecycle States for Relationship Assertions

Relationship Assertions use the following lifecycle states:

- **ACTIVE**: Assertion is currently canonical
- **SUPERSEDED**: Assertion replaced by another (reference successor)
- **WITHDRAWN**: Assertion determined invalid or no longer acceptable
- **TOMBSTONED**: Assertion deprecated but preserved

### V.2 Additional Status Dimensions (Not Lifecycle)

In addition to Lifecycle Status, Relationship Assertions may have:

- **Review/Dispute Status**: Whether validity is questioned (DISPUTED, CONFIRMED, CONTESTED, etc.)
- **Revision Status**: Whether wording has been refined (REVISED, CLARIFIED, etc.)

These are recorded in the assertion's audit trail and do not create new REL identifiers.

### V.3 SPLIT and MERGED States (Principle 5 — NOT Normally Used)

Relationship Assertions should **NOT** receive SPLIT or MERGED lifecycle states merely because their subject or object was split or merged.

Instead:

- The subject/object entity receives SPLIT or MERGED status
- The Relationship Assertion receives an **explicit separate decision**:
  - SUPERSEDED (replaced by new assertion involving successor entity)
  - WITHDRAWN (relationship no longer valid after split/merge)
  - ACTIVE with updated references (assertion continues with resolved identity)

```
Example:

Original: REL-000000400: WORK-A --supports--> CLAIM-1

Governance: WORK-A split_into [WORK-B, WORK-C]

Decision: Only WORK-B supports CLAIM-1; WORK-C does not inherit

Action:
  REL-000000401: WORK-B --supports--> CLAIM-1 (new, ACTIVE)
  REL-000000400 → SUPERSEDED (explicitly decided)
  DDR-xxxxxx documents the split decision and relationship outcome

Result: REL-000000400 does NOT receive SPLIT status.
        REL-000000400 receives SUPERSEDED status through explicit governance.
```

---

## VI. MERGER AND IDENTITY RESOLUTION (Principle 9)

### VI.1 Merger: MERGED_INTO Predicate

When two entities are merged, the relationship is formally recorded:

```
Predicate: MERGED_INTO
Direction: Asymmetric, directed
Definition: Subject has been formally merged into Object

Example: CLM-000000042 --merged_into--> CLM-000000043
(Claim 42 has been formally merged into Claim 43)

This is a DIRECTED, DATED governance event.
Recorded as: REL-xxxxxx with Evidence Type = PROCEDURAL
Documentary Decision Record (DDR) documents the merger decision.
```

### VI.2 Current Identity Resolution (Query-Time)

When entities are merged, historical Relationship Assertions preserve original identifiers:

```
Historical:
  REL-000000100: CLM-000000042 --supports--> WORK-A

After merge:
  CLM-000000042 merged_into CLM-000000043 (designated current)

Preserved in Audit Trail:
  REL-000000100 still points to CLM-000000042 (unchanged)

Query-Time Resolution:
  Query for "relationships of CLM-000000042" 
    → resolved via merger record
    → returns REL-000000100 with note: "subject resolved to CLM-000000043"
  
  Query for "relationships of CLM-000000043"
    → returns REL-000000100 (current identity)

Result: Historical accuracy preserved; current identity resolved transparently.
        No rewriting of historical assertions.
```

### VI.3 Reflexive Relationships from Merger (Principle 5)

If merger creates a reflexive relationship:

```
Original: REL-000000300: CLM-000000042 --cites--> CLM-000000043

After: CLM-000000042 merged_into CLM-000000043

Result: CLM-000000043 --cites--> CLM-000000043 (reflexive)

Validation:
  Check predicate (CITES): reflexivity permitted? NO
  
  Action Options:
  A) REL-000000300 → WITHDRAWN (merger invalidated relationship)
  B) REL-000000300 → SUPERSEDED by reflexive variant (if semantically valid)
  C) Preserve REL-000000300 with annotation: "merger created reflexive state"
  
  Decision recorded in DDR-xxxxxx (merger decision)
```

---

## VII. SPLIT AND RELATIONSHIP PROPAGATION (Principle 5, 7)

### VII.1 Split: SPLIT Predicate

When an entity is split, the governance decision is recorded:

```
Predicate: SPLIT_INTO
Direction: One-to-many (asymmetric)
Definition: Subject is determined to contain multiple distinct entities

Example: WORK-A --split_into--> [WORK-B, WORK-C]
(Work A was determined to contain two distinct works)

Entity Lifecycle: WORK-A receives SPLIT status
Successor Lifecycle: WORK-B and WORK-C receive ACTIVE status

Recorded as: REL-xxxxxx with Evidence Type = PROCEDURAL
Documentary Decision Record (DDR) documents split decision.
```

### VII.2 Relationship Propagation on Split (Principle 5 — Not Automatic)

When an entity is split, Relationship Assertions involving that entity are NOT automatically propagated.

Instead, explicit governance decisions are made:

```
Original: REL-000000500: WORK-A --supports--> CLAIM-1

Governance: WORK-A split_into [WORK-B, WORK-C]

Decision Options:

Option A: Both successors inherit relationship
  Create REL-000000501: WORK-B --supports--> CLAIM-1 (ACTIVE)
  Create REL-000000502: WORK-C --supports--> CLAIM-1 (ACTIVE)
  REL-000000500 → SUPERSEDED
  DDR-xxxxxx documents: both successors support claim

Option B: One successor inherits
  Create REL-000000501: WORK-B --supports--> CLAIM-1 (ACTIVE)
  REL-000000500 → SUPERSEDED
  DDR-xxxxxx documents: only WORK-B inherits

Option C: Neither successor inherits
  REL-000000500 → WITHDRAWN
  DDR-xxxxxx documents: relationship applies only to pre-split entity

Implementation:
  New assertions (REL-501, 502) must be explicitly created with evidence.
  Original assertion (REL-500) receives explicit lifecycle decision.
  No silent copying or automatic propagation.
```

### VII.3 Split and Predicate Inference (Principle 7)

**Important Distinction:**

- **Split operation:** Governance event, dated, creates new entities
- **Predicate inference:** Logical operation, applies to explicitly asserted relationships

These operate **independently**:

```
Original Assertions:
  REL-000000600: WORK-A --derives_from--> MANUSCRIPT-X
  REL-000000601: MANUSCRIPT-X --derives_from--> ORIGINAL

Inferred:
  WORK-A --derives_from--> ORIGINAL (transitive, no new REL)

Governance Event:
  WORK-A split_into [WORK-B, WORK-C]
  Decision: Both WORK-B and WORK-C derived from MANUSCRIPT-X

New Assertions Created:
  REL-000000602: WORK-B --derives_from--> MANUSCRIPT-X (new, explicit)
  REL-000000603: WORK-C --derives_from--> MANUSCRIPT-X (new, explicit)

Inference Then Applies:
  Transitive closure now derives:
    WORK-B --derives_from--> ORIGINAL
    WORK-C --derives_from--> ORIGINAL

Result: Split does not automatically extend inferred relationships.
        Inference operates on explicitly asserted relationships after split.
        Complete audit trail of every decision.
```

---

## VIII. CORRECTION RECORDS AND RELATIONSHIP ASSERTIONS

### VIII.1 Immutable Propositions (Principle 2)

A Relationship Assertion's proposition (subject, predicate, object, meaning) is immutable once documented.

If the proposition must change, create a new REL and supersede the original.

### VIII.2 Status Changes Without Correction Record

Status or review changes (DISPUTED, CONFIRMED, REVISED wording) do not require a new REL or a Correction Record.

They are recorded in the assertion's audit trail with version history.

### VIII.3 Propositional Changes Require Correction Record

If a Relationship Assertion's proposition must change:

1. Create new REL with revised proposition
2. Mark original REL as SUPERSEDED
3. Create Correction Record (COR) documenting:
   - Original assertion (REL-xxxxxx)
   - Reason for supersession
   - New assertion (REL-yyyyyy)
   - Authority and date
   - Supporting evidence

---

## IX. CANONICAL PREDICATE REGISTER (INCOMPLETE)

### IX.1 Predicate Framework

The Canonical Predicate Register defines all canonical predicates (PRD identifiers).

Each predicate entry specifies:
- Definition
- Permitted Subject and Object classes
- Transitivity, reflexivity, symmetry properties
- Evidence Type constraints
- Cardinality rules
- Inferability (YES/NO/CONDITIONAL)
- Relationship integration notes

### IX.2 Note on Completeness (Principle 9)

**This Specification does NOT provide a complete, audited Canonical Predicate Register.**

The framework is established. The predicate catalog is incomplete.

Full predicate register development and validation is required before certification.

A complete Canonical Predicate Register must include:
- All 62+ canonical predicates (or however many are required)
- Validation of each predicate against Documentary Ontology v1.1
- Evidence Type and Inferability assignments
- Complete subject/object class validation
- Cross-audit against Relationship Specification constraints

---

## X. GOVERNANCE AUTHORITY AND JURISDICTION

### X.1 Predicate Governance Authority

The Predicate Governance Authority manages:
- Canonical Predicate Register creation and maintenance
- Predicate approval and deprecation
- Predicate subject/object class validation
- Evidence Type and Inferability assignment
- Liaison with other authorities

### X.2 Authority Boundaries

**Ontology Governance Authority:**
- Defines entity classes
- Predicate Authority constrains predicates to those classes

**Identifier Governance Authority:**
- Assigns PRD family
- Allocates predicate identifiers

**Vocabulary Governance Authority:**
- Governs Evidence Type terminology
- Predicate Authority applies those types

**Predicate Governance Authority:**
- Defines predicates within constraints set by Ontology
- Operates independently on predicate definition

---

## XI. FINAL DECLARATION

The Relationship Specification v1.0 establishes canonical relationships:

- **Immutable Relationship Assertions** (new REL for propositional changes; SUPERSEDED original)
- **Status changes without new REL** (review, dispute, revision noted in audit trail)
- **Documented vs. inferred distinction** (REL for documented; query-time derivation for inferred unless materialized)
- **Evidence Type integration** (one Primary + zero-or-more Additional; from Controlled Vocabulary)
- **Merger and split handling** (preserve history; resolve at query time; explicit governance)
- **Complete audit trail** (no silent rewriting; all changes recorded)

Every Relationship Assertion traces to documentary evidence or valid inference.

---

END OF RELATIONSHIP SPECIFICATION v1.0 — FINAL CONSOLIDATED

Document Number: 000003  
Classification: Foundational Constitutional Specification  
Status: **Provisional Constitutional Baseline** (Predicate Register Incomplete)  
Note: Complete Canonical Predicate Register required before certification.  
Next Phase: Production validation and Strauss corpus construction
