
STRAUSSIAN DOCUMENTARY MEMORY

DOCUMENTARY ONTOLOGY
Version 1.1

Document Number: 000001
Classification: Foundational Constitutional Specification
Status: Provisional Constitutional Baseline
Authority: Defines what entities exist in the Straussian Documentary Memory; constitutional precedent for all other specifications


## PREAMBLE

The Documentary Ontology answers the foundational question: **What is permitted to exist in the Repository?**

This Ontology:
- Defines 16 permanent entity classes
- Establishes that all entities are first-class with identical governance rights
- Clarifies compositional structures (Passages, Work Components, Witness Components)
- Establishes constitutional precedence over Identifier, Relationship, and Vocabulary specifications

This Ontology does NOT:
- Assign identifier prefixes (Identifier Specification v1.0)
- Define relationship predicates (Relationship Specification v1.0)
- Govern controlled vocabulary (Controlled Vocabulary Specification v1.0)
- Prescribe implementation, storage, or query mechanisms

---

## I. FOUNDATIONAL PRINCIPLES

### I.1 Ontological Closure

The Repository contains only what this Ontology defines.

New entity classes require formal amendment to this Ontology.

All entities defined here are first-class: they receive permanent identifiers, participate in relationships, have versioning and audit trails, and are governed under identical constitutional principles.

### I.2 No Metadata or Annotation Classes

All entity classes defined here are first-class Repository entities.

No entity is "metadata," "annotation," or "secondary."

Repository Artifacts (Documentary Decision Records, Derivation Records, Evidence Records, Correction Records, Certification Records) are not annotations; they are entities.

Administrative collections (Repository Registers) are not metadata; they are entities with identity and governance.

### I.3 Compositional Structure Principle

Some entities reference or contain other entities:
- Passages are units within Works or Witnesses
- Work Components are structural subdivisions of Works
- Witness Components are structural subdivisions of Witnesses

Compositional references are navigational only; they do not create separate entity classes.

---

## II. THE 16 ENTITY CLASSES

### II.1 Complete Enumeration

The Repository defines exactly 16 entity classes:

**Core Documentary Entities (4):**
1. Work
2. Expression
3. Witness
4. Passage

**Interpretive and Analytical Entities (6):**
5. Claim
6. Interpretation
7. Hermeneutic Object
8. Comparative Reconstruction
9. Inquiry
10. Inquiry Architecture Record

**Repository Governance Artifacts (5):**
11. Documentary Decision Record
12. Derivation Record
13. Evidence Record
14. Correction Record
15. Certification Record

**Administrative Infrastructure (1):**
16. Repository Register

No other entity classes exist unless formally added through amendment to this Ontology.

---

## III. CORE DOCUMENTARY ENTITIES

### III.1 Work

**Definition:**  
A Work is an intellectual composition or published material constituting a distinct, citable unit. A Work represents the intellectual and structural identity of a composition.

**Key Properties:**
- Title
- Creator/Author (referenced via Relationship Assertions, not a stored property)
- Date of composition or publication
- Original language
- Subject matter or genre classification

**Relationship to Expression:**
A Work may have multiple Expressions (editions, translations, versions). Different Expressions manifest the same Work.

**Lifecycle:**
- ACTIVE: Current canonical Work
- SUPERSEDED: Replaced by authoritative edition
- CORRECTED: Errors amended (same Work, improved version)
- REVISED: Substantially refined (same Work, better scholarship)
- WITHDRAWN: Determined fraudulent or inaccessible
- SPLIT: Determined to contain multiple distinct works
- MERGED: Unified with another Work (designating which is current)
- TOMBSTONED: Deprecated but preserved

**Uniqueness:**
A Work receives exactly one identifier (WK prefix) for its entire existence. If a Work is split into multiple distinct works, each receives a new identifier; the original is marked SPLIT.

---

### III.2 Expression

**Definition:**  
An Expression is a distinct textual or material manifestation of a Work. An Expression represents a specific version, edition, translation, or adaptation.

**Key Properties:**
- Language
- Date of creation or publication
- Medium or format (printed, manuscript, digital, oral recording, etc.)
- Relationship to base Work (edition, translation, adaptation, etc.)
- Scope (complete, abridged, supplemented, etc.)

**Relationship to Work:**
An Expression always derives from or represents a Work. The relationship is recorded through Relationship Assertions (DERIVES_FROM, TRANSLATES, etc.).

**Lifecycle:**
Expressions follow the same lifecycle states as Works.

---

### III.3 Witness

**Definition:**  
A Witness is a documentary source: a manuscript, printed book, archival record, artifact, physical object, or recorded material preserved in the Repository. A Witness is a primary source whose content is accessible (via digitization, transcription, preservation, or archival access).

**Key Properties:**
- Physical or digital location/access information
- Date of creation, publication, or observation
- Medium (manuscript, printed book, artifact, digital, audio, video, etc.)
- Provenance or custody history
- Preservation status and access control

**Scope:**
A Witness is a complete, bounded documentary object. Subdivisions (pages, folios, sections) are Witness Components, not separate Witnesses.

**Lifecycle:**
Witnesses follow the same lifecycle states as Works.

---

### III.4 Passage

**Definition:**  
A Passage is a textual or structural unit within a Work or Witness that is significant enough to receive separate identity and be addressed independently in Relationship Assertions.

**Key Property — Dual Identity Model:**

A Passage has two distinct identity dimensions:

**1. Permanent Entity Identity (PSG prefix):**
- PSG identifiers are permanent and versioned
- A Passage is a first-class Repository entity
- Passages are citable and participate in relationships
- A substantive change in Passage content requires a new PSG identifier
- Editorial corrections retain the same PSG with version history

**2. Navigational Location Reference:**
- Indicates where the Passage is located within a parent entity
- Examples: WK-000000042:pages:45-67, WIT-000000100:folio:12
- Parent-derived syntax is used in queries and navigation only
- Location reference is NOT the Passage identity

**Example:**

```
PSG-000000001 (Passage Identity)
  Title: "On Natural Right"
  Content: [quoted or paraphrased text]
  Located in: WK-000000042 (navigational reference)
  Pages: 45–67 (navigational metadata)
  Lifecycle: ACTIVE
  Version history: v1.0 (original), v1.1 (corrected typo, same PSG)

Query results:
  "Retrieve PSG-000000001" → returns canonical Passage entity
  "Navigate WK-000000042:pages:45-67" → returns location reference
  Both refer to same logical content; identity is PSG-000000001
```

**Substantive Changes Require New Identity:**

If the Passage content is substantially altered (not just corrected):

```
Original: PSG-000000001 ("On Natural Right" from pages 45–67)

Substantive change: A critical phrase is reinterpreted or a major section is relocated.

Action: Create PSG-000000002 (new Passage identity)
        Mark PSG-000000001 as SUPERSEDED
        Correction Record documents why the original is superseded

Result: Two distinct Passage entities with complete history
```

**Lifecycle:**
Passages follow the same lifecycle states as Works (ACTIVE, SUPERSEDED, CORRECTED, REVISED, WITHDRAWN, etc.).

---

## IV. INTERPRETIVE AND ANALYTICAL ENTITIES

### IV.1 Claim

**Definition:**  
A Claim is a propositional assertion made within Repository inquiry. A Claim states a proposition (factual, interpretive, or evaluative) and typically requires supporting evidence through Relationship Assertions.

**Key Properties:**
- Propositional content
- Epistemic Classification (certainty/acceptance status)
- Authority or agent making the Claim
- Evidence status and lifecycle

**Distinctness:**
A Claim is a proposition. An Interpretation is a scholarly rendering. A Claim may cite an Interpretation; an Interpretation may make Claims.

**Lifecycle:**
Claims follow standard entity lifecycle (ACTIVE, DISPUTED, CORRECTED, SUPERSEDED, WITHDRAWN, TOMBSTONED).

---

### IV.2 Interpretation

**Definition:**  
An Interpretation is a hermeneutic reading or analytical rendering of one or more entities (Works, Witnesses, prior Interpretations). An Interpretation represents scholarly judgment applied to source material.

**Key Properties:**
- Interpretive framework or methodology
- Source entities being interpreted
- Analytical judgment or finding
- Authority (interpreter)
- Scope and limitations

**Nesting:**
Interpretations may nest (Interpretation of Interpretation), creating chains of scholarly engagement.

**Lifecycle:**
Interpretations follow standard entity lifecycle.

---

### IV.3 Hermeneutic Object

**Definition:**  
A Hermeneutic Object is a formal analytical artifact: scholarly analysis, commentary, exegesis, critical apparatus, or systematic investigation. It differs from Interpretation by explicit methodology and systematic structure.

**Key Properties:**
- Analytical framework (explicit)
- Source materials analyzed
- Organizational structure
- Conclusions or findings
- Authority (analyst or editorial board)
- Critical apparatus, notes, references

**Lifecycle:**
Hermeneutic Objects follow standard entity lifecycle.

---

### IV.4 Comparative Reconstruction

**Definition:**  
A Comparative Reconstruction is an explicit analysis comparing two or more entities, identifying similarities, differences, patterns, or structural parallels.

**Key Properties:**
- Entities compared (minimum two)
- Dimensions of comparison
- Findings or structural patterns identified
- Authority (analyst)
- Comparison framework or methodology

**Lifecycle:**
Comparative Reconstructions follow standard entity lifecycle.

---

### IV.5 Inquiry

**Definition:**  
An Inquiry is an organized investigation addressing a specific research question, gap in understanding, or documentary problem.

**Key Properties:**
- Research question or objective
- Scope and methodology
- Entities or materials investigated
- Investigation status (ongoing, resolved, abandoned, inconclusive)
- Authority (investigator or research group)

**Relationship to Findings:**
Inquiries are investigations; Interpretations are conclusions. An Inquiry may produce multiple Interpretations.

**Lifecycle:**
Inquiries follow standard entity lifecycle (ACTIVE = ongoing, RESOLVED = complete, WITHDRAWN = abandoned).

---

### IV.6 Inquiry Architecture Record

**Definition:**  
An Inquiry Architecture Record documents the structure, relationships, and organizational plan of a complex Inquiry. It records question decomposition, evidence chains, and findings organization.

**Key Properties:**
- Scope of overall inquiry
- Sub-questions or investigation branches
- Evidence structure or argument tree
- Relationship map (component relationships)
- Verification or completion status
- Authority (inquiry designer or lead investigator)

**Lifecycle:**
IAR follow standard entity lifecycle.

---

## V. REPOSITORY GOVERNANCE ARTIFACTS

### V.1 Documentary Decision Record

**Definition:**  
A Documentary Decision Record documents a formal Repository governance decision: merger of entities, splitting of entities, withdrawal of entities, supersession, or other governance action. A DDR reifies a governance event.

**Key Properties:**
- Decision type (merger, split, withdrawal, supersession, correction, validation, etc.)
- Affected entities and identifiers
- Rationale and supporting evidence
- Authority and approval
- Effective date
- Predecessor decision (if superseding a prior decision)
- Complete audit trail

**Integration with Assertions:**
Merger decisions create MERGED_INTO Relationship Assertions. Correction decisions create Correction Records. Withdrawal decisions change Lifecycle Status.

**Lifecycle:**
DDR follow standard entity lifecycle (ACTIVE, SUPERSEDED, WITHDRAWN, TOMBSTONED).

---

### V.2 Derivation Record

**Definition:**  
A Derivation Record documents a transformation or reproduction process: transcription, translation, normalization, OCR, digitization, or other systematic derivation. It preserves the lineage of derived entities.

**Key Properties:**
- Source entity (original)
- Derived entity (result)
- Transformation method (transcription, translation, OCR, normalization, digitization, etc.)
- Authority or tool employed
- Date of derivation
- Fidelity assessment (reversible, lossy, metadata-enriched, etc.)
- Information loss or enrichment (documented where applicable)

**Integration with Relationships:**
DERIVES_FROM and similar predicates create Relationship Assertions. Derivation Record provides detailed process documentation.

**Lifecycle:**
DER follow standard entity lifecycle.

---

### V.3 Evidence Record

**Definition:**  
An Evidence Record formally documents supporting evidence for a Claim, Interpretation, or Relationship Assertion. It makes explicit the evidentiary basis of a Repository judgment.

**Key Properties:**
- Evidence described (cited passage, comparative analysis, experimental result, etc.)
- Entity or assertion being supported
- Primary Evidence Type (canonical constants from Controlled Vocabulary Specification)
- Additional Evidence Types (zero or more)
- Authority or source
- Date of documentation
- Confidence or completeness assessment
- Reasoning or justification

**Distinction:** (Principle 6)
- Evidence Record documents **what evidence exists**
- Relationship Assertion assigns **which Evidence Type to this specific relationship**

A single Evidence Record may support multiple Relationship Assertions with different Evidence Types.

**Lifecycle:**
EVR follow standard entity lifecycle.

---

### V.4 Correction Record

**Definition:**  
A Correction Record documents a correction, revision, or amendment to one or more entities. It preserves original state, corrected state, reason, and authority.

**Key Properties:**
- Affected entities (one or more)
- Type of correction (typographical, factual, metadata, attribution, invalidation, etc.)
- Original state (prior version identifier or description)
- Corrected state (new version or replacement entity)
- Rationale for correction
- Supporting evidence or justification
- Authority making correction
- Effective date
- Relationship to Lifecycle Status change

**Correction Semantics (Principle 4):**

**Editorial/Typographical Corrections:**
- Retain the same entity identifier
- Record change in Version Record
- Entity lifecycle may receive CORRECTED or REVISED status
- Example: "Strauss" corrected to "Strauß" in PSG-000000001 remains PSG-000000001

**Substantive Changes:**
- Create new entity identifier
- Mark original as SUPERSEDED or WITHDRAWN
- Correction Record documents why original is superseded
- Both entities preserved in history
- Example: Major reinterpretation of a Claim requires CLM-000000042 → SUPERSEDED, new CLM-000000089 created

**Lifecycle:**
COR follow standard entity lifecycle (a Correction Record may itself be corrected — nested corrections permitted).

---

### V.5 Certification Record

**Definition:**  
A Certification Record formally attests that an entity meets specified criteria (accuracy, completeness, authenticity, preservation status, scholarly review, access control, etc.).

**Key Properties:**
- Entity certified
- Certification criteria or standard applied
- Verification method or assessment procedure
- Authority (certifying agent or body)
- Date of certification
- Expiration or review date (if applicable)
- Conditions or limitations (if any)

**Integration:**
CERTIFIES and CERTIFIED_BY predicates create Relationship Assertions. Certification Record provides detailed documentation.

**Lifecycle:**
CER follow standard entity lifecycle.

---

## VI. ADMINISTRATIVE INFRASTRUCTURE

### VI.1 Repository Register

**Definition:**  
A Repository Register is a governed, versioned collection of entities or relationship assertions maintained for administrative, curatorial, or operational purposes. A Register may serve as an authoritative ledger, catalog, inventory, or administrative list.

**Key Properties:**
- Scope (what does this register contain?)
- Curation or governance authority
- Versioning and audit history
- Append-only or modifiable status
- Access control (if applicable)
- Relationship to registered entities

**Examples:**
- Canonical Predicate Register (contains all PRD entries)
- Identifier Assignment Ledger (log of all identifier allocations)
- Documentary Decision Ledger (audit trail of all governance decisions)
- Witness Catalog (curated inventory of archived witnesses)
- Theme Index (organized taxonomy of research themes)

**First-Class Status:**
Registers are first-class entities with identity, versioning, and governance. They are not metadata annotations.

**Lifecycle:**
RRG follow standard entity lifecycle.

---

## VII. COMPOSITIONAL STRUCTURE (DETAILED)

### VII.1 Passages and Location References

**Dual Identity:**

A Passage receives a first-class identifier (PSG) indicating entity identity.

A Passage also has a location within a parent entity, indicated by navigational reference syntax.

```
PSG-000000001 (entity identity)
  Located at: WK-000000042:pages:45-67 (navigational reference)
  
Query for "PSG-000000001" → returns Passage entity
Query for "WK-000000042:pages:45-67" → returns location reference
Navigate to location → finds PSG-000000001 at that location

If location changes (e.g., renumbering in new edition):
  PSG-000000001 identity unchanged
  Location reference updated to new coordinates
  Version Record documents the relocation
```

**Substantive Content Changes:**

If Passage content fundamentally changes:

```
Original: PSG-000000001 ("On Natural Right", pages 45–67 of WK-000000042)
  Content: [original text]
  Lifecycle: ACTIVE

Substantive reinterpretation: Major phrase reanalyzed; core meaning changed.

Action: Create PSG-000000002 (new Passage)
        Mark PSG-000000001 as SUPERSEDED
        Correction Record documents the reinterpretation

Result: Two distinct Passage entities; complete history preserved
```

---

### VII.2 Work Components

**Definition:**  
A Work Component is a structural subdivision of a Work significant enough to be independently addressed: book, part, chapter, section, act, etc.

**Identity Model:**
Work Components do NOT receive independent identifiers. They are addressed through parent-derived structural reference.

**Navigational Reference Syntax:**

```
WK-000000001:book:2:chapter:5        (Chapter 5 of Book 2 in Work 1)
WK-000000001:part:3                  (Part 3 of Work 1)
WK-000000001:section:12:subsection:3 (nested structure)
```

**In Relationship Assertions:**

A Relationship Assertion may reference a Work Component:

```
WK-000000001:book:2:chapter:3 --cites--> WIT-000000042

(Chapter 3 of Book 2 in Work 1 cites Witness 42)
```

The component reference is navigational; it does not create a separate entity identity.

**Immutability:**
If a Work Component is renumbered or relocated (e.g., due to edition changes), the reference syntax is updated in the relationship. The relationship assertion itself (if the reference changes substantially) may require a new REL identifier.

---

### VII.3 Witness Components

**Definition:**  
A Witness Component is a structural subdivision of a Witness: page, folio, section, item, etc.

**Identity Model:**
Witness Components do NOT receive independent identifiers. They are addressed through parent-derived structural reference.

**Navigational Reference Syntax:**

```
WIT-000000042:page:87                (Page 87 of Witness 42)
WIT-000000042:folio:12               (Folio 12 of Witness 42)
WIT-000000042:section:3:subsection:2 (nested structure)
```

**In Relationship Assertions:**

```
WIT-000000042:page:87 --cited_by--> PSG-000000001

(Page 87 of Witness 42 is cited by Passage 1)
```

---

## VIII. STANDARD LIFECYCLE STATES

All entities (Works, Expressions, Witnesses, Passages, Claims, Interpretations, Hermeneutic Objects, Comparative Reconstructions, Inquiries, IAR, all Repository Artifacts, Registers) follow the same lifecycle states:

- **ACTIVE**: Current canonical entity; in use
- **SUPERSEDED**: Replaced by another entity (designating successor)
- **CORRECTED**: Errors amended (same entity, improved)
- **REVISED**: Substantially refined (same entity, better version)
- **WITHDRAWN**: Determined invalid, erroneous, fraudulent, or inaccessible
- **TOMBSTONED**: Deprecated but preserved for historical reference
- **SPLIT**: Entity determined to contain multiple distinct entities (original marked SPLIT; successors receive new identifiers)
- **MERGED**: Entity unified with another (if multiple merge, designate which is current)

**Note on Relationship Assertions:**

Relationship Assertions (reified in Relationship Specification v1.0) typically use only:
- ACTIVE
- SUPERSEDED
- WITHDRAWN
- TOMBSTONED

SPLIT and MERGED states are normally reserved for the entities themselves, not for assertions. See Principle 5 and Relationship Specification v1.0 for detailed rules.

---

## IX. ONTOLOGY GOVERNANCE

### IX.1 Constitutional Precedence

The Documentary Ontology has constitutional precedence over Identifier, Relationship, and Vocabulary specifications only on the question: **What entity classes exist?**

Other authorities (Identifier Governance, Predicate Governance, Vocabulary Governance) operate independently within their own jurisdictions while respecting the Ontology.

### IX.2 Authority Boundaries

**Ontology Governance Authority:**
- Defines what entity classes exist
- Establishes entity properties and structural boundaries
- Has precedence on questions of existence

**Identifier Governance Authority:**
- Assigns identifier prefixes to entity classes defined by the Ontology
- Manages identifier allocation
- Does NOT define what entities are

**Predicate Governance Authority:**
- Defines canonical relationship predicates
- Constrains predicates to entity classes defined by the Ontology
- Does NOT define entity classes

**Vocabulary Governance Authority:**
- Governs controlled terminology
- Does NOT define entity classes or predicates

### IX.3 Amendment Process

Amendment to the Ontology requires formal governance decision and documentation of:
- Reason for new entity class
- Properties and boundaries
- Relationship to existing classes
- Impact on Identifier, Relationship, and Vocabulary specifications

---

## X. WHAT THIS ONTOLOGY DOES NOT SPECIFY

This Ontology does NOT:
- Assign identifier prefixes (Identifier Specification v1.0)
- Define relationship predicates (Relationship Specification v1.0)
- Govern controlled vocabulary (Controlled Vocabulary Specification v1.0)
- Prescribe implementation, storage, database design, or query mechanisms
- Define user interface presentations
- Specify computational efficiency or optimization strategies

Those matters belong to other specifications, implementations, or operational guidelines.

---

## XI. FINAL DECLARATION

The Documentary Ontology v1.1 establishes constitutional definition of what exists:

- **16 permanent entity classes** (core documentary, interpretive, governance artifacts, administrative infrastructure)
- **Dual identity for Passages** (permanent PSG + navigational location reference)
- **Compositional structures** (Work and Witness Components as structural references, not entities)
- **Uniform lifecycle and versioning** applied to all entities
- **First-class governance** for all entities (no metadata or annotation classes)
- **Constitutional precedence** for Ontology on questions of existence only

All other specifications derive from and respect this Ontology while remaining independent in their own domains.

**Existence is constitutional. All other governance derives from existence.**

---

END OF DOCUMENTARY ONTOLOGY v1.1 — FINAL CONSOLIDATED

Document Number: 000001  
Classification: Foundational Constitutional Specification  
Status: **Provisional Constitutional Baseline**  
Next Phase: Production validation and Strauss corpus construction
