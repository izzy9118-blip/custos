STRAUSSIAN DOCUMENTARY MEMORY
CONTROLLED VOCABULARY SPECIFICATION
Version 1.0
Document Number: 000004
Classification: Foundational Repository Specification
Status: Corrected Final Draft for Constitutional Re-Audit
Authority: Establishes constitutional governance of controlled terminology

PURPOSE

This Specification governs stable classificatory terminology. It does not define entity classes, identifier families, predicates, or Evidence Type constants.

Dependency order:

Documentary Ontology
→ Identifier Specification
→ Relationship Specification
→ Controlled Vocabulary Specification
→ Canonical Vocabulary Register
→ Implementations

I. ONTOLOGY–VOCABULARY BOUNDARY

1. Ontology determines what exists.
2. Vocabulary determines governed terminology used to classify or describe existing entities.
3. A controlled concept does not become an entity class merely because it is registered.
4. New entity classes require ontology amendment.
5. New controlled concepts within established families require Register governance.
6. Implementations may not use vocabulary additions to bypass ontology or predicate governance.

II. CONTROLLED IDENTIFIER FAMILIES

The following families are established by Identifier Specification v1.0:

THM — Theme
EPC — Epistemic Classification
STS — Status
ROL — Role
LNG — Language
OPM — Operation Mode
HCO — Hermeneutic Completeness
QSS — Question Status
VOC — Vocabulary Concept

No new family may be created by this Specification.

III. CANONICAL VOCABULARY REGISTER

The Specification defines rules.
The Canonical Vocabulary Register contains approved instances.

Ordinary Register additions do not amend this Specification.

An amendment is required only when:
- governance rules change;
- canonical record requirements change;
- approval procedures change;
- identifier-family architecture changes;
- constitutional boundaries change.

IV. CANONICAL VOCABULARY RECORD

Every approved concept shall include:

- identifier;
- identifier family;
- preferred English label;
- zero or more approved localizations;
- aliases;
- formal definition;
- scope note;
- usage guidance;
- cardinality and co-occurrence rules;
- related concepts;
- governed ontology classes;
- relationship integration;
- version history;
- deprecation status;
- date defined;
- date last revised;
- responsible authority;
- localization guidance;
- implementation notes.

Authoritative fields:
identifier, family, preferred label, approved localizations, formal definition, scope, usage, cardinality, governed classes, relationship integration, version history, deprecation status, dates, authority.

Advisory fields:
aliases, related concepts, localization guidance, implementation notes.

V. SEMANTIC STABILITY

1. One concept. One identity. One meaning.
2. Controlled identifiers are permanent.
3. Labels may change without changing identity if semantic meaning remains stable.
4. A fundamental semantic change requires a new identifier.
5. Deprecated concepts remain permanently recorded.
6. Identifiers are never reused.
7. Implementations must map local representations explicitly to canonical identifiers.

VI. STATUS DIMENSIONS

STS concepts must identify a Status Category.

A. LIFECYCLE STATUS
Exactly one current lifecycle status for each admitted entity.

Examples:
ACTIVE
SUPERSEDED
WITHDRAWN
MERGED
SPLIT
TOMBSTONED

B. REVIEW/DISPUTE STATUS
Zero or more.

Examples:
DISPUTED
CONTESTED
UNDER_REVIEW
CONFIRMED

C. REVISION STATUS
Zero or more.

Examples:
REVISED
CORRECTED
CLARIFIED

D. IDENTIFIER-ALLOCATION STATUS
Exactly one for an allocation record.

Examples:
RESERVED
ASSIGNED
VOID

VOID never applies to an admitted entity.

VII. EPISTEMIC CLASSIFICATION

The EPC family preserves the Repository Epistemic Hierarchy:

1. DOCUMENTED FINDING
Directly recoverable documentary evidence.

2. SUPPORTED INFERENCE
A reasoned conclusion derived from documented findings.

3. WORKING HYPOTHESIS
A provisional interpretation retained for testing.

4. UNRESOLVED QUESTION
An open matter lacking adequate evidence or resolution.

5. CONSTITUTIONAL PRINCIPLE
A foundational rule governing the Repository.

Anonymous and pseudonymous are not epistemic classifications. Attribution is represented through authorship relationships, Roles, Status where necessary, and documentary metadata.

VIII. ROLES

Roles describe functions and do not create entity classes.

Examples:
AUTHOR
EDITOR
TRANSLATOR
INVESTIGATOR
SECRETARY
CERTIFIER
VALIDATOR
PRIMARY_SOURCE
COMPARATIVE_SOURCE
CONTROL_WITNESS

Role assignments are relational and may be context-dependent.

IX. OPERATION MODE

Operation Mode distinguishes:
- RECOVERED;
- RESPONSIBLY_RECONSTRUCTED;
- HYPOTHETICAL_RECONSTRUCTION.

No reconstructed operation may be described as recovered.

X. LOCALIZATION GOVERNANCE

1. Every concept requires one preferred English label.
2. Additional localizations are optional at creation.
3. A localization may be proposed by a qualified language expert.
4. Vocabulary Governance reviews semantic equivalence and philosophical context.
5. Approved localizations are recorded in the Canonical Vocabulary Register.
6. Competing localizations trigger documented expert review.
7. Prior approved localizations remain in version history.
8. Machine translation may assist drafting but cannot create an approved canonical localization without human review.
9. Interface display labels are not canonical localizations.

XI. SYNONYM GOVERNANCE

1. Each concept has one preferred label per language.
2. Aliases do not receive separate identifiers.
3. A semantically equivalent label cannot create a duplicate concept.
4. Implementation aliases are technical mappings, not canonical vocabulary.

XII. VOCABULARY GOVERNANCE

Vocabulary Governance Authority may:
- approve concepts within existing families;
- revise definitions without changing identity where meaning remains stable;
- deprecate concepts;
- approve localizations;
- maintain the Canonical Vocabulary Register.

Vocabulary Governance may not:
- create ontology classes;
- create identifier families;
- define predicates;
- redefine Evidence Type constants;
- override higher constitutional specifications.

XIII. PROPOSAL AND REVISION PROCESS

A proposal must include:
- semantic necessity;
- uniqueness analysis;
- family assignment;
- formal definition;
- scope;
- usage;
- cardinality;
- governed classes;
- relationship integration;
- preferred label;
- localization status;
- responsible authority.

Revision classes:
- editorial clarification;
- expanded guidance;
- substantive semantic change.

A substantive semantic change that breaks historical compatibility requires a new identifier.

XIV. IMPLEMENTATION INDEPENDENCE

Software enum values, database keys, graph labels, RDF URIs, JSON-LD terms, API fields, search facets, and UI labels are implementation representations.

They must:
- map explicitly to canonical identifiers;
- preserve meaning;
- never silently redefine a concept;
- synchronize with the authoritative Register;
- preserve version and deprecation information.

XV. FINAL DECLARATION

The Controlled Vocabulary Specification governs classificatory meaning without replacing ontology, identifiers, predicates, or relationship evidence semantics.

The Specification establishes rules.
The Canonical Vocabulary Register implements those rules.

Semantic stability is constitutional law.

END OF DOCUMENT
