
STRAUSSIAN DOCUMENTARY MEMORY

IDENTIFIER SPECIFICATION
Version 1.0

Document Number: 000002
Classification: Foundational Constitutional Specification
Status: Provisional Constitutional Baseline
Authority: Defines permanent, unique, immutable identities for all entities in the Straussian Documentary Memory


## PREAMBLE

The Identifier Specification answers: **How are entities permanently and uniquely identified?**

This Specification:
- Defines 16 identifier families for entity classes from Documentary Ontology v1.1
- Establishes 11 identifier families for predicates and controlled concepts
- Establishes permanent, immutable, non-reusable identifier rules
- Establishes administrative prefix standards

This Specification does NOT:
- Define what entities exist (Documentary Ontology v1.1)
- Define predicates (Relationship Specification v1.0)
- Define or govern controlled vocabularies (Controlled Vocabulary Specification v1.0)

---

## I. IDENTIFIER PRINCIPLES

### I.1 Permanence

Every identifier assigned to an entity is permanent.

Once assigned, an identifier:
- Is never changed
- Is never reassigned
- Is never reused
- Remains valid for the entity's entire history

### I.2 Uniqueness

No two entities within the same identifier family share an identifier.

Across families, identifiers are universally unique (no prefix reuse across families).

### I.3 Immutability

An identifier identifies a specific entity at a specific moment.

If an entity changes substantively, the identifier does not change; a Version Record documents the change.

If an entity must be replaced (not just corrected), a new identifier is created and the original is marked SUPERSEDED.

### I.4 Non-Reusability

If an identifier is abandoned, deprecated, or assigned to a replaced entity, the identifier number is never assigned to any other entity.

Gaps in identifier sequences are permitted and meaningful (they indicate abandoned or superseded identifiers).

---

## II. IDENTIFIER FAMILIES

### II.1 Entity Class Identifier Families

Every entity class from Documentary Ontology v1.1 receives a permanent identifier family:

| Entity Class | Family | Capacity | Purpose |
|---|---|---|---|
| **Core Documentary** | | | |
| Work | WK | 999M | Intellectual composition |
| Expression | EXP | 999M | Manifestation of Work |
| Witness | WIT | 999M | Documentary source |
| Passage | PSG | 999M | Textual/structural unit |
| **Interpretive/Analytical** | | | |
| Claim | CLM | 999M | Propositional assertion |
| Interpretation | INT | 999M | Scholarly reading |
| Hermeneutic Object | HOB | 999M | Formal analysis |
| Comparative Reconstruction | CPR | 999M | Comparative analysis |
| Inquiry | INQ | 999M | Research investigation |
| Inquiry Architecture Record | IAR | 999M | Inquiry structure |
| **Governance Artifacts** | | | |
| Documentary Decision Record | DDR | 999M | Governance decision |
| Derivation Record | DER | 999M | Transformation record |
| Evidence Record | EVR | 999M | Evidence documentation |
| Correction Record | COR | 999M | Correction documentation |
| Certification Record | CER | 999M | Verification record |
| **Administrative** | | | |
| Repository Register | RRG | 999M | Curated collection |

### II.2 Relationship and Controlled Concept Identifier Families

| Family | Purpose | Capacity |
|---|---|---|
| REL | Relationship Assertions | 999M |
| PRD | Canonical Predicates | 999M |
| THM | Themes (conceptual domains) | 999M |
| EPC | Epistemic Classifications | 999M |
| STS | Status (lifecycle, review, revision, allocation) | 999M |
| ROL | Roles (functions, positions) | 999M |
| LNG | Languages (natural language designations) | 999M |
| OPM | Operation Modes (operational states) | 999M |
| HCO | Hermeneutic Completeness (interpretation sufficiency) | 999M |
| QSS | Question Status (question lifecycle) | 999M |
| VOC | Vocabulary (meta-vocabulary governance) | 999M |

---

## III. IDENTIFIER SYNTAX

### III.1 Standard Format

All identifiers follow a uniform format:

```
[FAMILY]-[SEQUENCE]

Where:
  FAMILY   = 2–4 uppercase letters (administrative prefix)
  HYPHEN   = separator
  SEQUENCE = 9-digit zero-padded number (000000001 to 999999999)
  
Examples:
  WK-000000001     (Work)
  PSG-000000042    (Passage)
  CLM-000000089    (Claim)
  DDR-000000015    (Documentary Decision Record)
  REL-000000200    (Relationship Assertion)
  PRD-000000007    (Predicate)
  THM-000000001    (Theme)
```

**Reserved:** The sequence 000000000 is reserved and never assigned.

### III.2 Prefix Standards (Principle 7)

**Prefix Length:**
- 2–4 uppercase alphabetic characters
- Unique within the Repository
- Never reused across families

**Prefix Semantics:**
- Prefixes are administrative designations
- Mnemonicity is permitted (WK for Work, PSG for Passage, DDR for Documentary Decision Record) but not required
- Prefixes encode NO ontological meaning
- Prefixes do NOT reflect entity properties, relationships, or hierarchies
- Semantics reside exclusively in entity class definitions (Ontology v1.1) and entity content

**Prefix Permanence:**
- Once assigned to a family, never changed or reassigned
- Prefix identifies family membership only

### III.3 Structural References (Navigational Only)

Work Components, Witness Components, and Passage locations are addressed through navigational syntax, NOT separate identifiers:

```
WK-000000001:book:2:chapter:5          (Chapter 5 of Book 2 in Work 1)
WIT-000000042:page:87                  (Page 87 of Witness 42)
PSG-000000001:location:WK:42:pages:45-67  (Location of Passage 1)
```

Navigational references:
- Do NOT create separate entity identifiers
- Are used only for location and navigation
- May change without affecting entity identity
- Are resolved to parent entity identifiers in governance and versioning

---

## IV. IDENTIFIER ALLOCATION AND VALIDATION

### IV.1 Assignment Process

New identifiers are assigned in sequence within each family by the Identifier Governance Authority:

1. Family is identified (e.g., WK for new Work)
2. Next available sequence number is allocated (e.g., 000000089)
3. Identifier is permanently recorded in the Identifier Assignment Ledger
4. Identifier is bound to entity at creation time
5. No reallocation or reassignment occurs

### IV.2 Identifier Assignment Ledger

The Identifier Assignment Ledger (RRG entity) maintains permanent record of:
- Every identifier assigned
- Entity identifier points to
- Date of assignment
- Authority granting assignment
- Status (ASSIGNED, VOID, SUPERSEDED, etc.)

The Ledger itself is a Repository Register (RRG) entity with governance and versioning.

---

## V. IDENTIFIER PERMANENCE AND LIFECYCLE

### V.1 Permanence Rules

An identifier is **never changed, never reassigned, never expired.**

If an entity's lifecycle state changes (ACTIVE → SUPERSEDED, CORRECTED, WITHDRAWN, etc.), the identifier remains unchanged.

If an entity's content changes (even substantially), the identifier may remain unchanged if corrected with Version Record. If a new entity is required, a new identifier is created.

### V.2 Superseded Identifiers

When an identifier is superseded:

1. The old identifier is marked SUPERSEDED in the Identifier Assignment Ledger
2. A new identifier is assigned to the replacement entity (if replacement exists)
3. A Correction Record or Documentary Decision Record documents the supersession
4. The old identifier sequence number is never reused
5. Historical queries can find both old and new identifiers with clear linkage

Example:

```
Original: WK-000000089 (Work: "City and Man")
Later: Determined to be two distinct works; split required

Action:
  WK-000000089 → SUPERSEDED (marked in Ledger)
  WK-000000090 created (first split work)
  WK-000000091 created (second split work)
  DDR-000000055 documents the split decision

Result: Identifier WK-000000089 is never reused.
        Queries can traverse: WK-000000089 → split_into → [WK-000000090, WK-000000091]
```

### V.3 Abandoned Identifiers (VOID Status)

If an identifier is reserved but never assigned (e.g., allocation transaction fails):

1. The identifier is marked VOID in the Identifier Assignment Ledger
2. The number is never reassigned to another entity
3. The void gap is preserved in the sequence

Void identifiers prevent accidental reuse of abandoned numbers.

---

## VI. IDENTIFIER VERSIONING

### VI.1 Entity Versioning Preserves Identifier

An entity may have multiple versions:

```
WK-000000001 (Work)
  v1.0: Original entity (created 2026-01-15)
  v1.1: Corrected typo (2026-03-20)
  v1.2: Enhanced metadata (2026-05-10)
```

All versions are bound to the same identifier (WK-000000001).

Version history is preserved in the entity's Version Record.

### VI.2 Substantial Revision Creates New Identifier

If an entity undergoes substantial revision (not just correction), a new identifier may be created:

```
Original: CLM-000000042 (Claim: "Natural Right is...")
Later: Major reinterpretation of the Claim's meaning

Options:

A) Editorial Correction (same CLM):
   CLM-000000042
     v1.0: Original Claim
     v1.1: Refined wording (same meaning, clearer expression)
     v1.2: Corrected typo
   Result: Same identifier, multiple versions

B) Substantive Revision (new CLM):
   CLM-000000042 (original, marked SUPERSEDED)
     v1.0: Original Claim interpretation
   
   CLM-000000089 (new, marked ACTIVE)
     v1.0: Substantially revised interpretation
   
   COR-xxxxxx documents why CLM-000000042 is superseded
   Result: Two distinct Claim entities, complete history
```

---

## VII. GOVERNANCE AUTHORITY AND JURISDICTION

### VII.1 Identifier Governance Authority

The Identifier Governance Authority manages:
- Identifier family creation and assignment to entity classes
- Identifier allocation procedures
- Identifier Assignment Ledger maintenance
- Prefix administration
- Liaison with Ontology, Predicate, and Vocabulary authorities

### VII.2 Coordination with Other Authorities

**Ontology Governance Authority:**
- When new entity classes are defined in Ontology v1.1, Identifier Authority assigns identifier families
- When entity classes are amended, Identifier Authority assesses whether new families are needed

**Predicate Governance Authority:**
- Predicates use PRD family (already defined)
- Identifier Authority ensures no conflicts

**Vocabulary Governance Authority:**
- Controlled concepts use existing families (THM, EPC, STS, ROL, LNG, OPM, HCO, QSS, VOC)
- If new vocabulary family needed, Vocabulary Authority proposes; Identifier Authority approves through amendment

### VII.3 Independence Within Jurisdiction

Each authority operates independently within its domain while respecting other authorities:

- Ontology Authority determines what exists (precedent)
- Identifier Authority assigns identifiers (derived)
- Predicate Authority defines relationships (derived)
- Vocabulary Authority governs terminology (derived)

No authority may contradict another authority's domain; all must work within constraints set by upstream authorities.

---

## VIII. FINAL DECLARATION

The Identifier Specification v1.1 establishes permanent and unique identities:

- **27 permanent identifier families** (16 entity classes + 11 controlled concept families)
- **Uniform immutable syntax** ([FAMILY]-[9-DIGIT SEQUENCE])
- **Administrative prefix standards** (2–4 uppercase letters, no semantic encoding)
- **Permanence guarantees** (never changed, never reused, gap preserved)
- **Versioning and supersession rules** (Version Record preserves history)
- **Governance authority** with jurisdiction boundaries

Every entity in the Repository has a permanent, unique, immutable identity.

---

END OF IDENTIFIER SPECIFICATION v1.0 — FINAL CONSOLIDATED

Document Number: 000002  
Classification: Foundational Constitutional Specification  
Status: **Provisional Constitutional Baseline**  
Next Phase: Production validation and Strauss corpus construction
