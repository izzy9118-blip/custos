STRAUSSIAN DOCUMENTARY MEMORY
IDENTIFIER SPECIFICATION
Version 1.0
Document Number: 000002
Classification: Foundational Repository Specification
Status: Initial Release
Authority: Governs the assignment, preservation, validation, and resolution of canonical
entity identifiers throughout the Straussian Documentary Memory
PURPOSE
The Identifier Specification defines how stable identities are assigned to entities
recognized by Documentary Ontology v1.1.
It establishes:
- the syntax of canonical identifiers;
- the identifier families assigned to ontology classes;
- the distinction between identity, version, reference, locator, and hash;
- the canonical assignment record;
- the assignment and reservation protocol;
- duplicate prevention;
- treatment of correction, merger, split, supersession, withdrawal, and tombstoning;
- transcription and Derived Witness identity;
- controlled vocabulary identity;
- concurrency and distributed-authority boundaries;
- migration and scalability invariants.
This document does not define:
- relationship predicates;
- version-number semantics;
- URI schemes;
- GitHub paths;
- Neo4j labels;
- MCP resource formats;
- file naming conventions;
- storage engines;
- search ranking;
- fixity algorithms.
Those matters belong to later specifications.
The Identifier Specification answers one question:
How does every identity-bearing entity receive one permanent, unambiguous,
implementation-independent designation?
I. GOVERNING PRINCIPLES
1. STABLE IDENTITY
Every identity-bearing entity shall receive one canonical identifier.
The identifier remains stable through:
- correction;
- revision;
- reformatting;
- migration;
- relocation;
- reindexing;
- database replacement;
- graph projection;
- changes in file name or repository path;
- changes in descriptive metadata;
- changes in title or conventional name;
- changes in storage technology.
2. IMMUTABILITY
A canonical identifier, once assigned, shall never be changed, reassigned, recycled, or
silently replaced.
An identifier may acquire lifecycle events, including:
- disputed;
- corrected;
- merged;
- split;
- superseded;
- withdrawn;
- tombstoned.
Those events alter the entityâs recorded status, not the identifier itself.
3. CONTENT INDEPENDENCE
Canonical identifiers shall not encode:
- title;
- author;
- subject;
- theme;
- language;
- date;
- version;
- file format;
- repository path;
- storage location;
- checksum;
- inferred meaning;
- interpretive conclusion.
The prefix identifies only the governed identifier family.
The numeric component is nonsemantic.
4. ONTOLOGICAL CONFORMITY
Every canonical identifier shall correspond to an entity class admitted by Documentary
Ontology v1.1.
The Identifier Specification shall not create new ontology classes.
Where the Ontology defines a role, status, property, or functional configuration rather
than an independent entity, this Specification shall not manufacture a new canonical
identity merely for technical convenience.
5. ONE ENTITY, ONE CANONICAL IDENTIFIER
The Repository shall seek to assign one canonical identifier to one entity.
Before assignment, the allocation authority shall test whether the candidate entity
already exists.
Duplicate identifiers for one entity and one identifier for multiple entities are both
errors.
If duplicate identities are discovered after assignment, neither identifier is deleted or
reassigned. The correction is documented through lifecycle events and Relationship
Assertions.
6. IDENTITY BEFORE STORAGE
Canonical identity is independent of physical and technical representation.
A GitHub path, database key, Neo4j internal node number, URI, MCP resource address,
search index key, UUID, checksum, or file name may locate or represent an entity.
None of those operational values replaces the canonical identifier.
7. PRESERVED HISTORY
Historical references retain the identifier that was used when the record was created.
No later merger, correction, or supersession silently rewrites prior certified references.
Current-resolution services may report a later active identity, but the original reference
remains visible and auditable.
II. IDENTITY-BEARING ENTITIES
1. CONCRETE ENTITIES
Every concrete instance of an ontology class receives a canonical identifier when it
must be independently:
- cited;
- versioned;
- validated;
- certified;
- related;
- retrieved;
- governed;
- preserved;
- tracked through provenance.
Abstract grouping classes, including Repository Entity, Intellectual Entity, Inquiry Entity,
and similar parent classes, do not receive identifiers merely because they exist in the
hierarchy.
2. COMPONENT IDENTITY TEST
A component receives its own canonical identifier only when at least one of the
following applies:
- it has an independent lifecycle;
- it may be cited outside its parent;
- it may be versioned independently;
- it has distinct provenance;
- it may be validated or certified independently;
- it participates directly in Relationship Assertions;
- it must survive extraction from its parent;
- documentary fidelity requires independent addressability.
Otherwise the component is addressed through a noncanonical component reference
within its parent.
3. LEDGER ENTRIES
A Ledger is an ontology entity and receives a Ledger identifier.
An entry within a Ledger receives the canonical identifier appropriate to the entity it
records when the entry represents an independent entity.
Examples:
- a Claim Ledger entry representing a Claim uses a CLM identifier;
- an Evidence Ledger entry representing an Evidence Record uses an EVR identifier;
- a Relationship Ledger entry representing a Relationship Assertion uses a REL
identifier.
Purely administrative line events that do not constitute ontology entities use local
ledger record addresses, not new canonical entity identifiers.
4. SOURCE APPARATUS
Source Apparatus is a functional configuration of existing source entities under
Documentary Ontology v1.1.
It does not receive a separate identifier merely as a configuration.
A Repository-created Intertextual Apparatus Record is an independent entity and
receives its own identifier.
III. CANONICAL IDENTIFIER SYNTAX
1. FORM
A canonical identifier consists of:
PREFIX + HYPHEN + NINE-DIGIT SEQUENCE
Examples:
WK-000000001
WIT-000000037
CLM-000014582
CO-000000001
2. FORMAL PATTERN
Canonical identifiers shall conform to:
^[A-Z]{2,3}-[0-9]{9}$
Only prefixes listed in the Canonical Prefix Table are valid.
The numeric sequence:
- begins at 000000001;
- is zero-padded to nine digits;
- is unique within its prefix family;
- contains no meaning;
- is never reused.
The value 000000000 is reserved and shall never be assigned.
3. CASE AND CHARACTER SET
Canonical identifiers use:
- uppercase ASCII letters;
- one ASCII hyphen;
- ASCII decimal digits.
Whitespace, lowercase letters, punctuation beyond the one delimiter, diacritics,
slashes, colons, and embedded version strings are prohibited.
4. CAPACITY
Nine digits permit 999,999,999 identifiers in each family.
This capacity is selected because the Repository may eventually contain:
- at least one million Citation Objects;
- tens of millions of Claims;
- tens or hundreds of millions of Passages and Evidence Records;
- large numbers of Derived Witnesses, validation events, provenance records, and
relationships.
Capacity exhaustion shall not be solved by rewriting existing identifiers.
Any future expansion must be additive, versioned, and preserve every Version 1.0
identifier unchanged.
IV. CANONICAL PREFIX TABLE
A. AGENTS AND INTELLECTUAL ENTITIES
AGN â Person or Collective Agent
WK â Work
WCM â Work Component
EXP â Expression, including Translation, Edition or Recension, and Transcription
B. WITNESSES AND DOCUMENTARY SEGMENTS
WIT â Witness, including Source Witness and Derived Witness
WCW â Witness Component
VAR â Textual Variant
LOC â Location
PSG â Passage
CTX â Context
C. DOCUMENTARY OPERATIONS
DOP â Documentary Operation, including Citation, Quotation, Selection, Omission,
Placement, and Sequence
D. INQUIRY ENTITIES
INQ â Inquiry
QST â Question
CLM â Claim, including Observation, Interpretation, Structural Pattern, and Hypothesis
CMP â Comparison
TSK â Task
E. EVIDENTIARY ENTITIES
EVR â Evidence Record
EVC â Evidence Chain
ITA â Intertextual Apparatus Record
F. REPOSITORY PRODUCTION ARTIFACTS
DRE â Documentary Register Entry
CO â Citation Object
HOA â Hermeneutic Object A
HOB â Hermeneutic Object B
HOC â Hermeneutic Object C
CPR â Comparative Reconstruction
IAR â Inquiry Architecture Record
SYN â Repository Synthesis
CER â Certification Record
DDR â Documentary Decision Record
COR â Correction Record
CAP â Capacity Record
REL â Relationship Assertion
G. STRUCTURAL AND ADMINISTRATIVE ARTIFACTS
MAN â Manifest
LDG â Ledger
REG â Register
CAT â Catalog
WCL â Witness Collection
H. CONSTITUTIONAL AND TECHNICAL FORMALIZATION ENTITIES
FND â Foundational Document
SFG â Safeguard
AMD â Amendment
SPC â Specification
SCH â Schema
VOC â Controlled Vocabulary
I. CONTROLLED CONCEPTS
THM â Theme
EPC â Epistemic Classification
STS â Status
ROL â Role
LNG â Language
OPM â Operation Mode
HCO â Hermeneutic Completeness
QSS â Question Status
J. PROVENANCE AND LIFECYCLE ENTITIES
VER â Version Record
REV â Revision Record
PRV â Provenance Record
ACQ â Acquisition Record
VAL â Validation Record
FIX â Fixity Record
DER â Derivation Record
V. PREFIX GOVERNANCE
1. PREFIXES ARE CLOSED
Only prefixes listed in this Specification may be used for canonical assignment.
New prefixes require a versioned revision of the Identifier Specification.
2. PREFIXES IDENTIFY FAMILIES, NOT FULL MEANING
A prefix identifies the broad identity family assigned at minting.
Subtypes are stored as ontology-class properties.
Examples:
- Translation, Edition, and Transcription all use EXP;
- Source Witness and Derived Witness both use WIT;
- Observation, Interpretation, Structural Pattern, and Hypothesis all use CLM;
- Citation and Quotation both use DOP.
3. NO SEMANTIC SUBENCODING
The numeric portion shall not be partitioned to encode:
- author;
- project;
- source;
- date;
- language;
- work;
- repository;
- institutional origin.
Range allocation is operational only. It carries no documentary meaning.
4. RELATIONSHIP ASSERTIONS
A Relationship Assertion receives one REL identifier.
Its predicate, subject, object, evidence, status, and provenance are properties, not
parts of the identifier.
If the asserted predicate changes materially, a new Relationship Assertion receives a
new REL identifier.
The earlier assertion remains preserved and receives an appropriate lifecycle event.
VI. CONTROLLED CONCEPT IDENTITY
1. CONTROLLED TERMS ARE ENTITIES
Every governed Controlled Concept receives a canonical identifier.
Strings such as âDocumented Finding,â âDraft,â ârecovered,â or âTranslatorâ are
labels, not identities.
Examples:
EPC-000000001
STS-000000001
OPM-000000001
ROL-000000001
2. DEFINITION REVISION
A Controlled Concept retains its identifier when its definition is clarified without
changing its essential meaning.
The changed definition is recorded through Version and Revision Records.
If the meaning changes materially, a new Controlled Concept receives a new identifier
and the relation between the terms is documented.
3. THEMES
Themes receive THM identifiers.
A Theme may change label while retaining identity if the governed concept remains the
same.
A materially different concept receives a new THM identifier.
4. VOCABULARIES AND TERMS
A Controlled Vocabulary as a governed collection receives a VOC identifier.
Each identity-bearing term within it receives the prefix appropriate to its Controlled
Concept class.
The vocabulary and its terms are separate entities.
VII. TRANSCRIPTION, EXPRESSION, AND WITNESS IDENTITY
1. THREE-TIER MODEL
A source documentary object, a transcriptional realization, and each embodiment of
that realization are distinct.
Example:
Source Witness:
WIT-000000001
Diplomatic Transcription as Expression:
EXP-000000001
UTF-8 file embodying the Expression:
WIT-000000002
TEI-XML file embodying the same Expression:
WIT-000000003
2. DERIVATION
Every Derived Witness shall be connected to:
- the Expression it embodies;
- its immediate source Witness where applicable;
- its ultimate source Witness where applicable;
- one or more Derivation Records.
Derivation Records receive DER identifiers.
3. CORRECTION VERSUS NEW IDENTITY
A Witness retains its identifier through corrections that preserve the identity of the
same documentary embodiment.
Examples that ordinarily preserve the Witness identifier:
- correcting a transcription error;
- repairing encoding corruption;
- replacing a damaged file with a verified byte-equivalent restoration;
- correcting metadata without changing the embodied text.
These changes require:
- a new Version Record;
- a Revision or Derivation Record as appropriate;
- new Fixity Records for changed files;
- preservation of earlier versions.
4. NEW EXPRESSION OR WITNESS
A new Expression identifier is required when a transformation intentionally produces a
distinct textual realization.
Examples:
- normalization;
- translation;
- abridgment;
- modernization;
- editorial reconstruction;
- removal of diacritics as a substantive textual policy;
- a new critical constitution of the text.
Each independent embodiment of the new Expression receives its own Witness
identifier.
5. FORMAT CONVERSION
A format conversion may create a new Derived Witness while embodying the same
Expression.
Whether it receives a new Witness identifier depends on whether it is independently
preserved, cited, validated, or versioned.
A temporary conversion used only during processing need not enter the canonical
Repository as an identity-bearing Witness.
VIII. IDENTIFIER ASSIGNMENT AUTHORITY
1. IDENTIFIER ASSIGNMENT LEDGER
The canonical record of identifier allocation is the Identifier Assignment Ledger.
It is:
- append-only;
- immutable in historical form;
- authoritative for assignment history;
- independent of any one storage technology;
- capable of physical partitioning without logical fragmentation.
The Identifier Assignment Ledger is itself a Ledger entity and receives an LDG identifier.
2. IDENTIFIER REGISTRY
The Identifier Registry is a derived, queryable index built from the Identifier Assignment
Ledger and current lifecycle events.
It may be implemented through:
- a database;
- a search index;
- a graph;
- a cache;
- generated files.
The Identifier Registry is not independently authoritative.
If the Registry conflicts with the certified Identifier Assignment Ledger, the Ledger
governs.
3. AUTHORITY REGISTER
The Authority Register governs Agents and authority records.
It shall not be used as the universal identifier-allocation ledger.
This separation prevents Agent authority records from being confused with Repository-
wide identity assignment.
4. ASSIGNMENT AUTHORITY
Canonical identifiers may be assigned only by:
- the central Repository allocation authority; or
- an explicitly delegated allocator operating within recorded limits.
The precise software mechanism belongs to a later Technical Specification.
IX. ASSIGNMENT PROTOCOL
1. CANDIDATE PREPARATION
Before assignment, a candidate entity shall have:
- a proposed ontology class;
- sufficient descriptive metadata for disambiguation;
- provenance adequate to explain why the entity is being admitted;
- a provisional local key or UUID if needed operationally;
- an identity comparison against existing Registry records.
2. DUPLICATE CHECK
The allocation authority shall check for:
- exact existing identity;
- likely duplicate identity;
- prior legacy reference;
- conflicting classification;
- existing merge or supersession history.
Hashes, titles, names, and similarity scores may assist this check.
They do not determine identity automatically.
3. RESERVATION
The allocator reserves the next available number in the appropriate prefix family.
The reservation event records:
- prefix;
- numeric value;
- timestamp;
- allocator;
- transaction or batch identifier;
- provisional entity key;
- reservation status.
4. ASSIGNMENT
Assignment is complete only when the reservation and entity admission are committed
atomically by the allocation authority.
The assignment event records:
- canonical identifier;
- ontology class;
- assignment timestamp;
- responsible authority;
- admission provenance;
- initial lifecycle status;
- provisional or legacy references, where applicable.
5. FAILED ASSIGNMENT
If a reservation cannot be completed, the number is marked VOID.
Voided numbers are never reused.
Sequence gaps are permitted and carry no meaning.
6. BATCH ASSIGNMENT
Contiguous or noncontiguous ranges may be reserved for controlled batch ingestion.
Every number in the range must end as:
- ASSIGNED; or
- VOID.
No unrecorded number may disappear from a reserved range.
7. OFFLINE WORK
Offline canonical assignment is prohibited unless a range was reserved in advance by
the canonical allocator.
Local systems may use provisional UUIDs or local namespace keys until canonical
assignment occurs.
X. CONCURRENCY AND DUPLICATE PREVENTION
1. SERIALIZATION
Assignment shall be serialized within each prefix family.
No two transactions may successfully assign the same prefix and numeric value.
2. ATOMICITY
Reservation, uniqueness validation, and final assignment shall be transactional.
A partial failure must not produce two valid assignments or an unrecorded canonical
identifier.
3. IMPLEMENTATION-NEUTRAL REQUIREMENT
The allocation mechanism may use:
- transactional database locks;
- a single-writer service;
- compare-and-swap operations;
- distributed consensus;
- another mechanism proven to preserve the invariants.
The Identifier Specification governs the invariants, not the technology.
4. RECONCILIATION
Operational allocation records shall be reconciled against certified ledger segments.
A mismatch blocks certification until resolved.
5. NO REUSE AFTER EXPOSURE
Once a number has been reserved, displayed, transmitted, written to a file, or included
in a log, it shall never be assigned to another entity.
Abandoned numbers become VOID.
XI. LIFECYCLE EVENTS
1. APPEND-ONLY HISTORY
The original assignment event is never edited.
Later changes are expressed through appended lifecycle events.
2. PERMITTED LIFECYCLE STATES
The controlled Status vocabulary may include:
- active;
- disputed;
- withdrawn;
- superseded;
- merged;
- split;
- tombstoned;
- void.
The Status identifiers themselves are governed Controlled Concepts.
3. TOMBSTONING
Tombstoning does not delete an identifier or erase the entityâs historical existence.
A tombstone lifecycle event records:
- affected identifier;
- status;
- date;
- responsible authority;
- reason;
- supporting Documentary Decision Record or Correction Record;
- replacement identifier, if any.
No new Tombstone ontology class is created by this Specification.
4. MERGER
When two assigned identifiers are determined to designate one entity:
- both identifiers remain preserved;
- one may be designated the current canonical identity;
- the other receives a merged lifecycle state;
- a Relationship Assertion documents the merger;
- all prior references remain unchanged;
- a reference audit identifies dependent artifacts requiring review.
5. SPLIT
When one assigned identity is determined to contain multiple entities:
- the original identifier remains historically valid;
- each newly distinguished entity receives a new identifier;
- the original receives a split lifecycle state;
- Relationship Assertions document the resulting identities;
- prior references remain unchanged pending explicit review.
6. SUPERSESSION
Supersession preserves both identifiers.
A supersession event never causes automatic rewriting of certified historical
references.
7. RECLASSIFICATION WITHIN A FAMILY
If an entity is reclassified within the same prefix family while remaining the same entity,
the identifier is retained and the class correction is documented.
Examples:
- Hypothesis to Interpretation within CLM;
- Source Witness to Derived Witness within WIT where the same Witness was
misclassified.
8. CROSS-FAMILY MISIDENTIFICATION
If correction shows that the originally assigned entity belongs to a fundamentally
different identity family, the original identifier is not mutated.
A new identifier is assigned in the correct family.
A Correction Record and Relationship Assertion document the misidentification and
relation between the records.
XII. REFERENCE PRESERVATION AND RESOLUTION
1. HISTORICAL REFERENCES
Certified artifacts retain the identifier originally cited.
No resolver may conceal that historical reference.
2. CURRENT RESOLUTION
A current-resolution service may follow:
- supersession;
- merger;
- split guidance;
- tombstone status.
It must return:
- the requested identifier;
- its lifecycle status;
- the current target or targets, if any;
- the complete direct chain;
- a warning where resolution is disputed or nonunique.
3. NO SILENT ALIASING
Resolution does not make two identifiers textually interchangeable in the canonical
record.
Aliases, legacy references, and current targets are explicit mappings.
4. CHAIN INTEGRITY
Resolution chains shall:
- preserve direct events;
- prevent cycles;
- expose intermediate identifiers;
- avoid inventing a single current target where a split creates several;
- retain documentary reasons and provenance.
XIII. CANONICAL IDENTIFIER VERSUS OTHER VALUES
1. VERSION
Version is stored separately from canonical identity.
Correct:
entity_
id: CO-000000001
version: 2.3.1
The string CO-000000001@2.3.1 may be used as a human-readable reference
shorthand only if a later Versioning Specification authorizes it.
It is not a canonical identifier.
2. LOCATION
A Passage and Location remain separate identified entities.
Correct structured reference:
passage_
id: PSG-000000001
location
id: LOC-000000042
_
Composite strings do not create new canonical identifiers.
3. URI
URI design is deferred to the URI Specification.
A URI is a locator or resource name.
It is not the canonical entity identifier governed here.
4. STORAGE PATH
A file path may contain the identifier for convenience.
Changing the path does not change identity.
5. DATABASE KEY
Internal database keys may be integers, UUIDs, hashes, or engine-specific values.
Every representation must retain the canonical identifier as a distinct property.
6. HASH OR CHECKSUM
Hashes support:
- fixity;
- duplicate detection;
- content comparison;
- migration verification.
A changed hash does not automatically create a new entity.
A matching hash does not automatically prove that two documentary entities are
identical.
7. SEARCH IDENTIFIER
Search engines may generate internal document identifiers and relevance scores.
Those values are operational and noncanonical.
8. LEGACY REFERENCE
A pre-Specification document number, file name, or informal code may be preserved as
a legacy reference.
Legacy references are mapped explicitly to canonical identifiers and are never silently
treated as canonical.
XIV. BOOTSTRAP AND LEGACY MATERIAL
1. BOOTSTRAP
The first Identifier Assignment Ledger shall record its own genesis assignment and the
assignment of identifiers to foundational Repository entities.
The bootstrap sequence shall include, at minimum:
- the Identifier Assignment Ledger;
- Documentary Ontology as a Specification entity;
- Identifier Specification as a Specification entity;
- existing Foundational Documents and Safeguards;
- existing Citation Objects and associated artifacts admitted to the canonical
Repository.
2. SPECIFICATION VERSIONS
Documentary Ontology v1.0 and v1.1 are versions of one Specification entity unless a
constitutional decision determines otherwise.
They therefore share one SPC identifier and have distinct Version Records.
3. DOCUMENT NUMBERS
Document Number 000001 and Document Number 000002 are historical local
designations.
They are not canonical entity identifiers.
4. EXISTING CITATION OBJECT NUMBERS
An existing label such as Citation_Object_000001 is a legacy reference until the
Identifier Assignment Ledger formally assigns a CO identifier.
A legacy number does not automatically determine the numeric portion of the canonical
identifier.
5. LEGACY MAPPING
Every adopted legacy artifact shall preserve:
- legacy reference;
- canonical identifier;
- source file name;
- admission date;
- responsible authority;
- ambiguity notes;
- related prior versions.
XV. DISTRIBUTED AND FORKED REPOSITORIES
1. SINGLE CANONICAL AUTHORITY
Version 1.0 assumes one canonical allocation authority for the Straussian Documentary
Memory.
2. FORKS
A fork shall not mint identifiers using canonical prefix sequences unless it has received
a recorded delegation.
Independent forks use provisional, explicitly namespaced local identifiers.
Those identifiers are not canonical identifiers under this Specification.
3. MERGE FROM A FORK
When fork material enters the canonical Repository:
- candidate entities undergo duplicate review;
- canonical identifiers are assigned by the central authority;
- local identifiers are preserved as provenance and legacy references;
- mappings are recorded explicitly.
4. DELEGATED RANGES
A delegated allocator may receive recorded numeric ranges.
Delegation records shall specify:
- prefix family;
- allocated range;
- authority;
- start and end dates;
- reconciliation obligations;
- unused-range treatment.
Unused delegated numbers become VOID when delegation closes.
XVI. SCALABILITY AND PHYSICAL PARTITIONING
1. LOGICAL UNITY
The Identifier Assignment Ledger is logically unified even when physically partitioned.
2. PERMITTED PARTITIONING
Ledger segments may be partitioned by:
- prefix family;
- numeric range;
- time period;
- certified batch.
Partitioning shall not change identifier meaning.
3. CERTIFIED SEGMENTS
Certified ledger segments are immutable.
Corrections are appended in later segments.
4. DERIVED INDEXES
Implementations should maintain derived indexes for:
- identifier lookup;
- prefix lookup;
- lifecycle status;
- current resolution;
- legacy references;
- assigned ranges;
- voided numbers;
- merge and supersession chains.
Indexes are rebuildable from canonical ledger and lifecycle artifacts.
5. PERFORMANCE
No production service should require a sequential scan of the entire canonical ledger
for ordinary validation.
Performance mechanisms remain subordinate to the canonical record.
XVII. VALIDATION RULES
A canonical identifier is structurally valid only when:
1. its prefix appears in the Canonical Prefix Table;
2. its syntax matches the formal pattern;
3. its numeric portion is not 000000000;
4. its assignment appears in the Identifier Assignment Ledger;
5. the identifier is assigned to only one entity;
6. its ontology class is compatible with its prefix family;
7. it has not been recorded solely as a reservation or VOID event;
8. all lifecycle events form a valid, acyclic history;
9. Registry results reconcile with the canonical ledger.
XVIII. MIGRATION AND CHANGE CONTROL
1. NO REFORMATTING OF EXISTING IDENTIFIERS
No future version shall pad, truncate, renumber, or rewrite an existing Version 1.0
identifier.
2. ADDITIVE EXPANSION
If a family approaches exhaustion, a future specification shall add an expansion
mechanism before capacity is reached.
The expansion must preserve every earlier identifier exactly.
3. NO MASS ALIAS MIGRATION
The Repository shall not create replacement identifiers merely to impose a new visual
format.
Mappings are reserved for genuine identity correction, integration of external systems,
or unavoidable architectural change.
4. SPECIFICATION REVISION
Changes to:
- prefix families;
- syntax;
- sequence capacity;
- assignment authority;
- lifecycle semantics;
- distributed allocation;
require a versioned revision of this Specification.
5. PRESERVED HISTORY
Every revision shall state:
- what changed;
- why it changed;
- affected identifier families;
- compatibility consequences;
- migration requirements;
- preservation guarantees.
XIX. RELATIONSHIP TO LATER SPECIFICATIONS
1. RELATIONSHIP SPECIFICATION
The Relationship Specification shall define:
- permitted predicates;
- subject and object constraints;
- evidentiary requirements;
- contradiction;
- merger;
- split;
- supersession;
- dependency;
- derivation;
- refinement.
This Identifier Specification assigns identity to Relationship Assertions but does not
define their semantics.
2. VERSIONING SPECIFICATION
A later Versioning Specification shall define:
- version-number syntax;
- major, minor, and patch meaning;
- release states;
- version references;
- compatibility rules.
3. URI SPECIFICATION
A later URI Specification shall map canonical identifiers to resolvable resources without
altering canonical identity.
4. TECHNICAL ALLOCATION SPECIFICATION
A later Technical Allocation Specification shall define:
- transaction mechanism;
- locks;
- database or service architecture;
- Git synchronization;
- batch reservation;
- ledger segment format;
- cryptographic integrity;
- disaster recovery.
XX. GOVERNING MAXIMS
Ontology before identity.
Identity before storage.
Canonical identifier before locator.
Version is not identity.
Hash is not identity.
Prefix is family, not meaning.
Reservation is never reuse.
Correction is not erasure.
Resolution is not silent rewriting.
The ledger governs the index.
Evidence precedes inference.
XXI. FINAL DECLARATION
The Identifier Specification establishes the permanent identity system of the Straussian
Documentary Memory.
Every admitted entity shall receive one stable canonical identifier appropriate to its
ontology family.
Canonical identifiers are:
- unique;
- immutable;
- nonsemantic;
- implementation-independent;
- version-independent;
- storage-independent;
- permanently auditable.
The Identifier Assignment Ledger preserves every reservation, assignment, void,
correction, merger, split, supersession, withdrawal, and tombstone event.
The Identifier Registry is derived from that record and remains subordinate to it.
No file path, URI, graph key, database number, hash, title, date, version string, or
search identifier may replace canonical identity.
Existing history shall not be rewritten.
Identifiers shall not be reused.
Identity shall remain stable.
END OF DOCUMENT
Document: Identifier Specification
Version: 1.0
Document Number: 000002
Classification: Foundational Repository Specification
