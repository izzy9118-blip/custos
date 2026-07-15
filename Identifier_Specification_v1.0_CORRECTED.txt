STRAUSSIAN DOCUMENTARY MEMORY
IDENTIFIER SPECIFICATION
Version 1.0
Document Number: 000002
Classification: Foundational Repository Specification
Status: Corrected Final Draft for Constitutional Re-Audit
Authority: Defines permanent identity and identifier allocation for every identity-bearing class in Documentary Ontology v1.1

PURPOSE

This Specification defines stable, unique, immutable identifiers independent of titles, content hashes, versions, storage paths, software systems, and representations.

I. GOVERNING PRINCIPLES

1. One entity, one canonical identity.
2. An identifier is permanent and never reused.
3. Identity is independent of title, version, storage, URI, database key, and content hash.
4. Changes in representation do not change identity.
5. Substantive discovery of distinct identity requires a new identifier.
6. Merger, split, supersession, withdrawal, correction, and deprecation preserve historical identifiers.
7. Identifier assignment is append-only and auditable.
8. Prefixes identify governed families; numeric sequences carry no semantic meaning.
9. The reserved sequence 000000000 is never assigned.
10. All canonical identifiers use nine-digit zero-padded sequences unless a future amendment expands capacity.

II. GENERAL SYNTAX

[PREFIX]-[NINE-DIGIT SEQUENCE]

Examples:
AG-000000001
WK-000000001
WIT-000000001
REL-000000001

III. ENTITY CLASS–IDENTIFIER COVERAGE

A. AGENTS
Agent — AG
Person — PER
Collective Agent — CAG

B. INTELLECTUAL ENTITIES
Work — WK
Work Component — WC
Expression — EXP
Translation — TRL
Edition or Recension — EDN
Transcription — TRS

C. WITNESSES
Witness — WIT
Source Witness — uses WIT with controlled provenance classification
Derived Witness — uses WIT with controlled provenance classification
Witness Component — WCP
Witness Collection — WCL
Textual Variant — TVR

D. ADDRESS AND SEGMENT ENTITIES
Location — LOC
Passage — PSG
Context — CTX

E. DOCUMENTARY OPERATIONS
Documentary Operation — DOP
Citation — CIT
Quotation — QUO
Selection — SEL
Omission — OMI
Placement — PLC
Sequence — SEQ

F. INQUIRY ENTITIES
Inquiry — INQ
Question — QST
Claim — CLM
Observation — OBS
Interpretation — INT
Structural Pattern — SPT
Hypothesis — HYP
Comparison — CMP
Task — TSK

G. EVIDENTIARY ENTITIES
Evidence Record — EVR
Evidence Chain — EVC

H. INTERPRETIVE AND RECONSTRUCTION ARTIFACTS
Hermeneutic Object — HO
Hermeneutic Object A — HOA
Hermeneutic Object B — HOB
Hermeneutic Object C — HOC
Comparative Reconstruction — CR
Inquiry Architecture Record — IAR
Repository Synthesis — RSY
Citation Object — CO

I. GOVERNANCE AND DOCUMENTARY DECISION ARTIFACTS
Documentary Decision Record — DDR
Derivation Record — DER
Correction Record — COR
Certification Record — CER
Validation Record — VAL
Provenance Record — PRO
Fixity Record — FIX
Version Record — VER
Revision Record — REV

J. REGISTERS, LEDGERS, CATALOGS, MANIFESTS
Register — REG
Ledger — LDG
Catalog — CAT
Manifest — MAN
Authority Register — AUR
Canonical Predicate Register — CPRG
Canonical Vocabulary Register — CVRG

K. CONSTITUTIONAL AND TECHNICAL FORMALIZATION
Foundational Document — FND
Safeguard — SFG
Amendment — AMD
Specification — SPEC
Schema — SCH

L. RELATIONAL ENTITIES
Relationship Assertion — REL
Predicate — PRD

M. CONTROLLED CONCEPT FAMILIES
Theme — THM
Epistemic Classification — EPC
Status — STS
Role — ROL
Language — LNG
Operation Mode — OPM
Hermeneutic Completeness — HCO
Question Status — QSS
Vocabulary Concept — VOC

IV. IDENTITY RULES FOR SUBTYPES

A subtype may receive:
1. its own family where independent subtype identity is constitutionally useful; or
2. the parent family plus controlled classification where subtype identity does not require a separate sequence.

Source Witness and Derived Witness use the WIT family because provenance status may change relative to a derivation chain without changing Witness identity.

Hermeneutic Objects A, B, and C retain dedicated families because they are established archival artifact forms with distinct production and validation requirements.

V. COMPONENT AND PASSAGE IDENTITY

1. Work Components and Witness Components are first-class entities when independently addressable, cited, compared, validated, or related.
2. They receive WC and WCP identifiers.
3. Parentage is represented by Relationship Assertions, not encoded into canonical identity.
4. Parent-derived strings may later serve as navigational locators but are not canonical identifiers.
5. Passages receive PSG identifiers.
6. Passage identity is not changed by reinterpretation. A new Interpretation or Claim receives its own identifier.
7. A new Passage identifier is assigned only when the bounded documentary segment itself is newly constituted or materially distinct.

VI. VERSION, REVISION, AND CORRECTION

1. Version numbers never replace canonical identifiers.
2. A Version Record receives VER identity.
3. A Revision Record receives REV identity.
4. Ordinary correction preserves the entity identifier and creates COR and relevant VER/REV records.
5. A change in title, metadata, transcription accuracy, or classification does not automatically create a new entity.
6. A materially distinct documentary object receives a new identifier.
7. No identifier is reused after withdrawal, merger, split, or deprecation.

VII. MERGER, SPLIT, AND CURRENT RESOLUTION

A. MERGER
1. All original identifiers remain valid historical references.
2. A Documentary Decision Record identifies the current representative.
3. Historical assertions retain original identifiers.
4. Query-time current resolution may follow the merger record.
5. No silent rewriting occurs.

B. SPLIT
1. The original identifier remains preserved with SPLIT lifecycle status.
2. Each resulting entity receives a new identifier.
3. Relationships are not automatically propagated.
4. Explicit new Relationship Assertions and documentary decisions govern successor assignments.

VIII. IDENTIFIER ASSIGNMENT LEDGER

Every assignment, reservation, void, merger, split, withdrawal, and current-resolution decision shall be recorded in an append-only Identifier Assignment Ledger.

Minimum fields:
- identifier;
- family;
- assigned class;
- assignment status;
- assignment date;
- authority;
- source decision;
- lifecycle status;
- predecessor or successor identifiers where applicable;
- audit history.

Allocation statuses:
- RESERVED;
- ASSIGNED;
- VOID.

VOID applies only to abandoned identifier reservations, not admitted entities.

IX. GOVERNANCE JURISDICTION

1. Ontology Governance defines classes.
2. Identifier Governance creates identifier families and allocates identifiers.
3. Predicate Governance defines predicates.
4. Vocabulary Governance approves controlled concepts within established families.
5. Ordinary addition of a controlled concept does not require Identifier Governance approval.
6. A new identifier family requires formal amendment to this Specification.
7. Identifier Governance may not redefine ontology classes or predicate semantics.

X. VALIDATION

A canonical identifier is valid only when:
1. its syntax is valid;
2. its family exists;
3. it is present in the Identifier Assignment Ledger;
4. its assigned class is compatible with the family;
5. it has not been reused.

XI. FINAL DECLARATION

This Specification provides explicit identifier coverage for every identity-bearing class in Documentary Ontology v1.1 while preserving stable identity across versions, corrections, mergers, splits, migrations, and implementations.

END OF DOCUMENT
