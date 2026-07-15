STRAUSSIAN DOCUMENTARY MEMORY
RELATIONSHIP SPECIFICATION
Version 1.0
Document Number: 000003
Classification: Foundational Repository Specification
Status: Corrected Final Draft for Constitutional Re-Audit
Authority: Defines canonical predicates, reified Relationship Assertions, evidence requirements, inference, lifecycle, merger, split, and validation semantics

PURPOSE

This Specification answers:

How are identity-bearing entities related to one another?

I. RELATIONSHIP ASSERTION MODEL

Every canonical Relationship Assertion is a reified entity with a permanent REL identifier.

Required fields:
- relationship_id;
- subject_id;
- predicate_id;
- object_id;
- evidence_type;
- epistemic_classification;
- lifecycle_status;
- zero or more review/dispute statuses;
- zero or more revision statuses;
- supporting Evidence Record identifiers;
- authority;
- creation date;
- version history;
- audit trail.

Subject and Object must be canonical identifiers for classes defined in Documentary Ontology v1.1.

Navigational strings, unregistered labels, offsets, or parent-derived component references cannot serve as canonical Subject or Object identifiers.

II. IMMUTABILITY

1. Subject, Predicate, Object, and propositional meaning are immutable for a REL identifier.
2. A change to any of those creates a new REL identifier.
3. The prior REL is preserved and marked SUPERSEDED or WITHDRAWN.
4. Status changes that do not change the proposition remain attached to the same REL and are appended to its audit history.

III. STATUS CARDINALITY

A Relationship Assertion is a reified Repository Entity and has:
- exactly one current Lifecycle Status;
- zero or more Review/Dispute Statuses;
- zero or more Revision Statuses.

It may therefore be ACTIVE, DISPUTED, and CORRECTED simultaneously, provided each belongs to the proper status dimension.

Lifecycle examples:
ACTIVE, SUPERSEDED, WITHDRAWN, TOMBSTONED.

IV. EVIDENCE TYPES

Evidence Types are closed constitutional constants governed by this Relationship Specification:

1. DOCUMENTARY — recoverable from Witnesses, Passages, Citations, Quotations, or archival materials.
2. PROCEDURAL — established by formal Repository governance or validation artifacts.
3. COMPARATIVE — established through explicit documented comparison.
4. STRUCTURAL — observable in documented organization or composition.
5. REPOSITORY — established through a documented Repository investigation or curatorial judgment.

Rules:
- Every Relationship Assertion has exactly one Evidence Type.
- Evidence Type is distinct from Epistemic Classification and Operation Mode.
- Implementations may not add, remove, or redefine Evidence Types.
- Any change requires formal amendment to this Specification.
- Multiple evidence bases are represented by multiple Evidence Records or multiple Relationship Assertions, not by silently multiplying the Evidence Type field.

V. PREDICATE REGISTER REQUIREMENTS

Every Predicate receives a PRD identifier and a Canonical Predicate Register entry containing:
- preferred label;
- formal definition;
- inverse predicate, if any;
- permitted subject classes;
- permitted object classes;
- cardinality;
- symmetry;
- asymmetry;
- transitivity;
- reflexivity;
- inferability;
- inference conditions;
- cycle rule;
- evidence requirements;
- lifecycle and governance notes;
- version history;
- deprecation state.

No predicate may use a Subject or Object class absent from Documentary Ontology v1.1.

VI. CANONICAL PREDICATE CORE

The following predicate families form the minimum constitutional core. Exact PRD allocations belong in the Canonical Predicate Register.

A. DOCUMENTARY REFERENCE
CITES
IS_CITED_BY
QUOTES
IS_QUOTED_BY
REFERS_TO
IS_REFERRED_TO_BY

B. STRUCTURE AND EMBODIMENT
HAS_COMPONENT
COMPONENT_OF
EMBODIES
EMBODIED_BY
LOCATED_AT
LOCATION_OF
CONTAINS
CONTAINED_IN

C. PROVENANCE AND DERIVATION
DERIVES_FROM
SOURCE_OF
TRANSCRIBED_FROM
TRANSCRIPTION_OF
TRANSLATES
TRANSLATION_OF
NORMALIZES
NORMALIZED_FROM
PRODUCED_FROM
PRODUCES

D. EVIDENCE AND INQUIRY
SUPPORTS
SUPPORTED_BY
CONTRADICTS
CONTRADICTED_BY
CONTEXTUALIZES
CONTEXTUALIZED_BY
RAISES
RAISED_BY
ANSWERS
ANSWERED_BY
TESTS
TESTED_BY
INTERPRETS
INTERPRETED_BY
COMPARES
COMPARED_IN

E. AUTHORSHIP AND RESPONSIBILITY
AUTHORED_BY
AUTHOR_OF
EDITED_BY
EDITOR_OF
TRANSLATED_BY
TRANSLATOR_OF
CERTIFIED_BY
CERTIFIER_OF
VALIDATED_BY
VALIDATOR_OF

F. GOVERNANCE AND LIFECYCLE
SUPERSEDES
SUPERSEDED_BY
WITHDRAWS
WITHDRAWN_BY
CORRECTS
CORRECTED_BY
MERGED_INTO
HAS_MERGED_PREDECESSOR
SPLIT_INTO
RESULTS_FROM_SPLIT
DEPRECATES
DEPRECATED_BY

G. ARTIFACT COMPOSITION
DOCUMENTS
DOCUMENTED_BY
HAS_EVIDENCE_RECORD
EVIDENCE_RECORD_FOR
HAS_VERSION
VERSION_OF
HAS_REVISION
REVISION_OF
HAS_PROVENANCE
PROVENANCE_OF
HAS_FIXITY_RECORD
FIXITY_RECORD_FOR

VII. SUBJECT/OBJECT VALIDATION

Predicate constraints must use only canonical ontology classes.

Examples:
- CITES may connect Citation, Work, Work Component, Expression, Witness, Witness Component, or Passage to a documentary entity.
- QUOTES must involve a Quotation or the entity in which the Quotation occurs, and a quoted source Passage or Witness.
- SUPPORTS may connect Passage, Citation, Quotation, Evidence Record, Observation, Claim, Witness, or Hermeneutic Object to Claim, Interpretation, Hypothesis, Question, Validation Record, or Certification Record, as defined by the Predicate Register.
- CONTAINS may connect Work to Work Component, Witness to Witness Component, Register to records, Manifest to declared contents, Citation Object to contained artifacts, or Evidence Chain to Evidence Records.
- Undefined convenience labels such as “Historical Record” or “Source Witness” may only be used if they map to ontology classes or controlled classifications.

VIII. INFERABILITY

Inferability values:

NO
The relationship must be directly asserted and cannot be derived solely from other relationships.

YES
The relationship may be derived under the formal logical rule in its Predicate Register entry.

CONDITIONAL
The relationship may be derived only when the stated preconditions are satisfied.

Every inferable predicate must state:
- the formal inference rule;
- required source assertions;
- whether the result is direct or indirect;
- provenance requirements;
- cycle policy;
- whether query-time computation or materialization is permitted.

A derived traversal or inferred result must never be presented as a directly documented Relationship Assertion.

Implementations may compute inferred relationships dynamically or materialize them. A materialized inference receives a REL identifier, is explicitly marked INFERRED, and links to all source REL identifiers and the governing rule.

Storage strategy is not constitutional. Logical results and provenance are constitutional.

IX. TRANSITIVITY AND CYCLES

1. DERIVES_FROM must be acyclic.
2. CONTAINS and COMPONENT_OF must be acyclic.
3. SUPERSEDES and current-resolution chains must be acyclic.
4. MERGED_INTO is directed and must be acyclic as a current-resolution chain.
5. Symmetric identity-equivalence views derived from mergers may form an equivalence class and are not treated as invalid directed cycles.
6. Predicate validation must reject prohibited cycles.
7. The failed assertion attempt must be recorded in an audit log.
8. This Specification does not prescribe a cycle-detection algorithm.

X. MERGER SEMANTICS

1. Merger is represented by MERGED_INTO and a Documentary Decision Record.
2. All historical Relationship Assertions retain their original Subject and Object identifiers.
3. A current identity representative may be resolved at query time.
4. Historical assertions are never silently rewritten.
5. A relationship that becomes reflexive after current resolution is flagged for predicate-specific validation.
6. Reflexive invalidity does not retroactively erase the historical assertion; it triggers an explicit lifecycle decision.

XI. SPLIT SEMANTICS

1. Split is represented by SPLIT_INTO and a Documentary Decision Record.
2. The original entity is preserved with SPLIT lifecycle status.
3. Resulting entities receive new identifiers.
4. Existing Relationship Assertions are not automatically copied.
5. Each affected assertion is reviewed.
6. New successor assertions require explicit documentary or procedural evidence.
7. The original assertion receives an explicit lifecycle decision: ACTIVE as historical, SUPERSEDED, WITHDRAWN, or TOMBSTONED.

XII. CORRECTION SEMANTICS

1. A Correction Record may correct a Relationship Assertion’s metadata, status history, evidence link, or wording without changing its proposition.
2. If Subject, Predicate, Object, or propositional meaning changes, a new REL is required.
3. The original REL remains preserved.
4. Correction Records identify original state, corrected state, reason, authority, evidence, and effective date.
5. Correction Records may themselves be corrected.

XIII. GOVERNANCE JURISDICTION

1. Ontology Governance decides which classes may serve as Subject or Object.
2. Identifier Governance allocates REL and PRD identifiers.
3. Predicate Governance defines predicates and their constraints.
4. Vocabulary Governance governs controlled classifications used by Relationship Assertions, except the closed Evidence Type constants defined here.
5. Predicate Governance may not create ontology classes or identifier families.
6. New predicates require Predicate Register governance.
7. Changes to this constitutional framework require formal amendment.

XIV. FINAL DECLARATION

This Specification preserves the distinction between documented and inferred relationships, requires canonical entity identifiers at both ends of every assertion, preserves complete provenance, and prevents silent propagation during merger, split, correction, or inference.

END OF DOCUMENT
