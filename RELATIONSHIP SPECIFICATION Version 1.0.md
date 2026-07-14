STRAUSSIAN DOCUMENTARY MEMORY
RELATIONSHIP SPECIFICATION
Version 1.0
Document Number: 000003
Classification: Foundational Repository Specification
Status: Final Editorial Revision for Certification
Authority: Defines the controlled vocabulary, semantics, constraints, evidence
requirements, lifecycle behavior, and validation rules governing Relationship Assertions
in the Straussian Documentary Memory
[SECTIONS I–XIII: Body text remains unchanged from
Relationship_Specification_
v1.0
_Revised.txt]
---
## SECTION XIV: PREDICATE IDENTITY AND PERMANENCE
### XIV.1 PREDICATE IDENTIFIERS ARE PERMANENT
Every Predicate Identifier (PRD-xxxxxxxxx) assigned in this Specification is permanent.
A Predicate Identifier, once assigned to a predicate definition, shall never be changed,
reassigned, recycled, or reused.
The PRD identifier and the predicate definition are permanently bound.
The binding is recorded in the Canonical Predicate Register (Appendix A).
### XIV.2 PREDICATE IDENTIFIERS ARE NEVER REUSED
If a predicate is deprecated, removed from canonical use, or discovered to be
erroneous, its PRD identifier is marked as deprecated or withdrawn, but the number is
never reassigned.
A deprecated predicate retains its PRD identifier permanently.
Future predicates receive new, sequential PRD numbers.
Sequence gaps are permitted and carry no meaning.
### XIV.3 DEPRECATED PREDICATES REMAIN RECORDED
Deprecated predicates are not deleted from the Canonical Predicate Register.
They remain permanently recorded with:
- Original PRD identifier;
- Original definition;
- Reason for deprecation;
- Date of deprecation;
- Successor predicate (if any);
- Replacement guidance for existing relationships.
This preserves complete audit history and enables retroactive understanding of how
the Repository's semantic vocabulary evolved.
### XIV.4 PREDICATE DEFINITIONS MAY BE REVISED
A predicate definition may be revised to:
- Clarify meaning without changing semantic intent;
- Expand explanatory guidance or examples;
- Correct errors in the original definition;
- Refine subject or object class constraints based on production experience.
All revisions are recorded with version history:
- Original definition (preserved);
- Revision date;
- Nature of revision (editorial, guidance, substantive);
- Responsible authority;
- Impact assessment (whether existing relationships require re-evaluation).
### XIV.5 PREDICATE IDENTIFIERS THEMSELVES ARE IMMUTABLE
A predicate definition may be revised, but the PRD identifier never changes.
The PRD identifier serves as the permanent reference point.
Systems refer to predicates by PRD identifier, not by textual label.
If a predicate's textual label changes (e.g., "authored_by" becomes "created_by" for
clarity), the PRD identifier remains the same:
```
PRD-000000056 (predicate identifier: permanent)
v1.0 label: "authored
_by"
v1.1 label: "created
_by" (editorial revision for clarity)
meaning: unchanged
```
Both labels are valid; the PRD identifier is canonical.
### XIV.6 SUBSTANTIVE SEMANTIC CHANGES REQUIRE NEW PREDICATES
If a predicate's semantic meaning must change materially, a new Predicate Identifier is
created rather than revising the old one.
Example:
```
PRD-000000056 (original): "created by author"
[Later determined to be insufficiently precise]
PRD-000000089 (new): "authored_by (for intellectual creation)"
PRD-000000090 (new): "generated_by (for algorithmic derivation)"
```
Both old and new predicates are recorded. Relationship Assertions using the old
predicate remain valid and auditable. The distinction is documented through
Relationship Assertions or Migration Records.
This ensures that historical relationships are never silently reinterpreted by changes in
predicate semantics.
---
## SECTION XV: PREDICATE VERSIONING
### XV.1 EDITORIAL CLARIFICATION
Editorial clarification refines explanation, examples, or scope documentation without
changing the predicate's semantic content or constraints.
Examples of editorial clarification:
- Expanding the definition with additional examples;
- Clarifying the distinction between this predicate and similar predicates;
- Improving validation guidance;
- Adding notes on common misapplications.
Editorial clarifications do not require creation of new PRD identifiers.
They are recorded as version updates to the same predicate:
```
PRD-000000001 (CITES)
v1.0 definition: "Subject refers to Object without reproducing its words."
v1.1 definition: [same as v1.0]
v1.1 additions: [expanded explanatory guidance, clarified predicate distinctions,
improved validation notes]
```
### XV.2 EXPANDED EXPLANATORY GUIDANCE
Expanded guidance provides additional context, use cases, or interpretation without
materially changing the predicate.
Examples:
- Documenting how the predicate applies in specific ontology class combinations;
- Adding case studies or illustrative scenarios;
- Clarifying inferability rules or transitivity behavior;
- Adding notes on lifecycle interaction.
Expanded guidance does not require new PRD identifiers.
Such expansions are recorded as version updates:
```
PRD-000000020 (DERIVES_FROM)
v1.0 definition: [original]
v1.1 guidance additions: [expanded explanatory scenarios, documented
transformation workflows, etc.]
```
### XV.3 SUBSTANTIVE SEMANTIC REVISION
Substantive semantic revision materially changes what the predicate means, its
subject/object constraints, evidence requirements, or logical properties.
Examples of substantive semantic changes:
- Changing the Evidence Type from DOCUMENTARY to PROCEDURAL;
- Expanding or restricting subject/object class constraints;
- Altering directionality or transitivity;
- Changing the predicate's relationship to other predicates fundamentally.
Substantive semantic revisions shall NOT be applied to existing PRD identifiers.
Instead:
**Option A (Preferred):** Create a new PRD identifier for the revised semantics. Mark
the old predicate as deprecated with a migration path documented.
**Option B (If backward compatibility is maintained):** Issue a new version of the entire
Relationship Specification (e.g., v1.1) that formally updates the predicate definition
while preserving the old PRD identifier. The change is explicitly documented as
"substantive semantic revision" with clear impact assessment.
**Option B is used only when substantive changes preserve logical consistency with
existing Relationship Assertions.**
In both cases, the change is permanent and versioned. It never occurs silently.
### XV.4 VERSION RECORDS FOR PREDICATES
Every predicate definition change is recorded in a Predicate Version Record:
```
{
"prd_id": "PRD-000000001",
"predicate_label": "cites",
"version": "1.0",
"definition": [original definition],
"date
_defined": "2026-01-15",
"revision
_type": "initial_
release"
}
{
"prd_id": "PRD-000000001",
"version": "1.1",
"date
_revised": "2026-06-30",
"revision
_type": "editorial_clarification",
"changes": "Added explanatory guidance; clarified predicate distinctions; expanded
validation notes.",
"backward
_compatible": true,
"impact_
on
_existing_assertions": "none; all existing CITES assertions remain valid and
unchanged."
}
```
### XV.5 PREDICATE GOVERNANCE AUTHORITY
The authority responsible for predicate versioning and creation is defined in Section XVI
— Predicate Governance (below).
That authority maintains the Canonical Predicate Register and approves all predicate
additions, revisions, deprecations, and versioning decisions.
---
## SECTION XVI: PREDICATE GOVERNANCE
### XVI.1 PREDICATE GOVERNANCE AUTHORITY
Predicate governance is the responsibility of the Repository's Constitutional Authority,
acting through a designated Predicate Authority.
The Predicate Authority:
- Maintains the Canonical Predicate Register;
- Approves new predicate proposals;
- Manages predicate revisions and versioning;
- Oversees predicate deprecation and retirement;
- Resolves conflicts between proposed predicates;
- Documents all governance decisions formally;
- Preserves complete audit history of predicate evolution.
### XVI.2 NEW PREDICATE PROPOSAL PROCESS
A new canonical predicate may be proposed when:
1. **Documentary Need**: Repository production has demonstrated a recurring need
for a relationship that existing predicates do not capture.
2. **Semantic Distinctness**: The proposed predicate represents a semantically
distinct relationship not adequately expressed by existing predicates, predicate
combinations, or properties.
3. **Ontological Validity**: The predicate connects entity classes admitted by
Documentary Ontology v1.1 and does not create implicit new entity classes.
4. **Evidence Requirement**: The proposed predicate has a clearly defined Evidence
Type (DOCUMENTARY, PROCEDURAL, COMPARATIVE, STRUCTURAL, or REPOSITORY)
and verifiable evidence criteria.
5. **Formal Specification**: The proposed predicate includes:
- Preferred label;
- Definition;
- Subject and object class constraints;
- Directionality, reflexivity, symmetry, transitivity;
- Inverse predicate (if applicable);
- Inferability assessment;
- Lifecycle and validation notes;
- Justification and use cases.
New predicate proposals are formally reviewed by the Predicate Authority and
approved through versioned revision of this Specification.
No predicate becomes canonical until this process is complete.
### XVI.3 PREDICATE REVISION PROCESS
Revisions to existing predicate definitions follow this process:
1. **Classification**: The proposed revision is classified as editorial clarification,
expanded guidance, or substantive semantic change (Section XV).
2. **Impact Assessment**: If substantive, the impact on existing Relationship
Assertions is assessed. Do existing assertions remain valid? Do they require re-
evaluation?
3. **Backward Compatibility Review**: Can the revision be applied to the existing PRD
identifier while preserving logical consistency with historical assertions?
4. **Formal Documentation**: The revision is formally documented with rationale,
impact analysis, and any required migration guidance.
5. **Authority Approval**: The Predicate Authority reviews and approves the revision.
6. **Versioning**: The revision is recorded in the Predicate Version Record and
Appendix A is updated.
7. **Publication**: The revised Relationship Specification (or an amendment) is formally
published with clear indication of what changed.
### XVI.4 PREDICATE DEPRECATION
A predicate may be marked as deprecated when:
- It is discovered to be erroneous or redundant;
- It is replaced by improved or more precise predicates;
- Production experience shows it should not have been canonical;
- It is superseded by semantic innovations.
Deprecation process:
1. **Formal Decision**: The Predicate Authority formally decides to deprecate the
predicate.
2. **Deprecation Record**: A Predicate Deprecation Record is created documenting:
- PRD identifier;
- Original definition;
- Reason for deprecation;
- Successor predicate(s), if any;
- Migration guidance for existing relationships;
- Date of deprecation;
- Sunset date (if applicable).
3. **Migration Guidance**: Clear guidance is provided for what predicate should be
used for new assertions. Existing assertions using the deprecated predicate remain
valid.
4. **Permanent Recording**: The deprecated predicate remains in Appendix A with
deprecation status. Its PRD identifier is never reused.
5. **Transition Period**: A deprecation period (e.g., 12 months) may be announced to
allow systems to migrate away from the deprecated predicate.
### XVI.5 CONFLICT RESOLUTION
When two or more proposed predicates appear to express the same relationship with
different labels:
1. **Semantic Analysis**: The Predicate Authority analyzes whether they are truly
synonymous or semantically distinct.
2. **Canonical Selection**: If synonymous, one canonical predicate is selected. The
others are not created as duplicates.
3. **Alias Documentation**: Non-canonical terms may be documented as aliases or
common alternative labels but do not receive PRD identifiers.
4. **Documented Decision**: The conflict resolution decision is formally documented
and published.
### XVI.6 AUTHORITY TRANSPARENCY
All predicate governance decisions are:
- Formally documented;
- Publicly recorded in the Canonical Predicate Register;
- Subject to audit and historical reconstruction;
- Never made silently or without documentation.
The Predicate Authority maintains complete transparency about why predicates were
created, revised, deprecated, or rejected.
---
## SECTION XVII: PROHIBITION ON SYNONYM DRIFT
### XVII.1 ONE CANONICAL SEMANTIC VOCABULARY
The Straussian Documentary Memory shall maintain one canonical semantic vocabulary
for relationships.
Synonyms, alternative terms, and similar-but-not-identical concepts shall not become
new canonical predicates unless approved through formal predicate governance.
If a canonical predicate exists (e.g., SUPPORTS), equivalent terms such as:
- reinforces
- confirms
- backs
- corroborates
- verifies (if semantically identical)
- validates (if semantically identical)
shall not become new canonical predicates without explicit predicate governance
approval and formal versioning of this Specification.
### XVII.2 ALIAS MANAGEMENT
Alternative terms for existing predicates may be documented in Appendix A as
**Preferred Aliases** without receiving new PRD identifiers.
Example:
```
PRD-000000013 (SUPPORTS)
Preferred Label: "supports"
Aliases: "reinforces" (synonymous), "provides evidence for" (explanatory)
Aliases are for human reference only; they do not receive separate PRD identifiers.
All Relationship Assertions use PRD-000000013 regardless of which alias was used.
```
Aliases are:
- Documented in Appendix A;
- Non-canonical (do NOT receive PRD identifiers);
- Semantically identical to the canonical predicate;
- Used for improved human readability or cross-cultural translation;
- Subject to governance decisions about appropriateness.
### XVII.3 SYNONYM CREATION IS FORBIDDEN
Ad hoc creation of synonymous predicates is forbidden.
If a system implementer, investigator, or tool creates a relationship using an
undocumented synonym (e.g., using "reinforces" instead of "supports"), the
relationship is either:
- Rejected as non-canonical and required to use the approved PRD identifier; or
- Accepted with a correction recorded, converting it to use the canonical PRD.
The Repository shall not permit drift toward uncontrolled semantic vocabulary.
### XVII.4 GOVERNANCE OF NEAR-SYNONYMS
When a proposed predicate appears similar but not identical to an existing predicate,
the Predicate Authority explicitly decides:
- Are they truly synonymous? → Use canonical predicate.
- Are they semantically distinct? → Approve new predicate with clear semantic
boundary documented.
- Should they be inverse predicates? → Document as inverses.
This decision is formal, documented, and permanent.
---
## SECTION XVIII: SEMANTIC STABILITY AS CONSTITUTIONAL PRINCIPLE
### XVIII.1 GOVERNING MAXIM: MEANING OVER IMPLEMENTATION
**Meaning shall remain more stable than implementation.**
The Repository may evolve:
- Software systems;
- Database technologies;
- Graph databases (Neo4j, RDF, etc.);
- APIs and query languages;
- Search indexes and caching;
- User interfaces;
- Storage formats;
- Deployment architectures;
- Optimization strategies.
Through all such changes, the semantic meaning of canonical predicates must remain
stable.
A predicate's meaning established in this Specification shall endure across decades of
technological change.
Implementation shall adapt to meaning, not the reverse.
### XVIII.2 MEANING STABILITY VERSUS CLARIFICATION
Meaning stability does NOT preclude:
- Editorial clarification of predicate definitions;
- Expanded examples and explanatory guidance;
- Improved documentation of edge cases;
- Better exposition of relationships to other predicates;
- Corrected examples that were erroneous;
- More precise delineation of subject/object class constraints based on production
experience.
These improvements clarify the predicate's intent without changing its semantic
content.
Clarifications are recorded as version updates to the same PRD identifier.
### XVIII.3 MEANING STABILITY VERSUS CORRECTION
If a predicate is discovered to be fundamentally erroneous in its original specification:
- The error is formally acknowledged;
- A correction is formally designed;
- The correction is applied through formal versioning, not silent rewriting;
- The change is documented with full justification;
- Impact on existing Relationship Assertions is assessed and documented;
- The change is published in a revised Relationship Specification.
Silent correction of predicate meaning is forbidden.
### XVIII.4 IMPLEMENTATION INDEPENDENCE
Implementations of the Canonical Predicate Register must preserve predicate
semantics independently of:
- Neo4j edge labels or property graph structure;
- RDF triple vocabularies or ontology namespaces;
- JSON-LD context definitions;
- MCP resource type names;
- API endpoint names;
- Search index field names;
- Caching strategies;
- Algorithm or inference engine design.
Each implementation derives from the canonical semantics defined in Appendix A but
may express that semantics in implementation-specific ways.
The canonical semantics always govern.
### XVIII.5 MULTILINGUAL AND TRANSCULTURAL STABILITY
Predicate meaning shall be stable across:
- Multiple languages (English, Italian, German, French, etc.);
- Different cultural interpretations;
- Future translations and localization.
The PRD identifier is language-independent and culture-independent.
The semantic definition in Appendix A is the canonical meaning, regardless of how it is
translated or localized for presentation to human users.
---
## SECTION XIX: APPENDIX A AUTHORITY
### XIX.1 APPENDIX A IS CANONICAL OPERATIONAL REFERENCE
Appendix A — Canonical Predicate Register is the canonical, authoritative, machine-
readable source for all predicate definitions in the Straussian Documentary Memory.
All software implementations, graph databases, APIs, MCP servers, search systems,
and AI retrieval tools shall treat Appendix A as the source of truth for predicate
semantics.
### XIX.2 IMPLEMENTATIONS SHALL NOT REDEFINE PREDICATES INDEPENDENTLY
No implementation may:
- Change a predicate's definition without updating Appendix A and publishing a formal
revision;
- Create a new predicate without registering it in Appendix A and versioning this
Specification;
- Use a predicate label or identifier that conflicts with Appendix A;
- Silently alter predicate semantics through implementation choices that are not
reflected in Appendix A.
Implementations that discover issues with predicate definitions or propose
improvements shall:
1. Formally report the issue to the Predicate Authority;
2. Wait for governance decision and formal revision;
3. Update their implementation to match the revised definition.
Unilateral predicate redefinition by individual implementations is prohibited.
### XIX.3 APPENDIX A IS MACHINE-READABLE AND QUERYABLE
Appendix A is structured to be:
- Machine-readable (JSON, XML, RDF, or other formal serialization);
- Queryable (systems can retrieve predicate definitions programmatically);
- Versioned (historical versions are preserved);
- Indexed (predicates can be discovered by class, evidence type, transitivity, etc.);
- Migratable (definitions can be exported and imported across systems without loss of
semantic precision).
### XIX.4 SYNCHRONIZATION ACROSS SYSTEMS
All implementations of the Straussian Documentary Memory must:
- Periodically synchronize predicate definitions with the authoritative Appendix A;
- Validate that their local predicate understanding matches the canonical definitions;
- Log and report any discrepancies;
- Update themselves if canonical definitions are revised.
This synchronization is mandatory, not optional, to prevent semantic drift across the
distributed Repository.
### XIX.5 PREDICATE DEFINITION CHANGE LOG
Appendix A maintains a permanent change log documenting:
- Date of each predicate addition;
- Date of each revision;
- Nature of revision (editorial, guidance, substantive);
- Predecessor predicate(s) (if substantively revised);
- Deprecation dates (if deprecated);
- Reason for each change;
- Responsible authority.
This change log enables reconstruction of predicate evolution and historical
understanding of why relationships asserted under earlier predicate definitions should
be interpreted.
---
## APPENDIX A: CANONICAL PREDICATE REGISTER
### APPENDIX A.0: REGISTER STRUCTURE AND GOVERNANCE
The Canonical Predicate Register (Appendix A) is the authoritative, permanent,
machine-readable register of all canonical predicates permitted in the Straussian
Documentary Memory.
Each predicate entry includes:
| Field | Description |
|-------|-------------|
| **Predicate Identifier** | Unique PRD-xxxxxxxxx identifier (9-digit, never reused) |
| **Preferred Label** | Primary English textual label for human readability |
| **Aliases** | Alternative English terms (not separately identifiable) |
| **Definition** | Precise semantic definition; what the predicate means |
| **Predicate Class** | Class assignment (A–J; see Section III) |
| **Subject Classes** | Ontology classes permitted as subject of this predicate |
| **Object Classes** | Ontology classes permitted as object of this predicate |
| **Evidence Type** | Required evidence (DOCUMENTARY, PROCEDURAL,
COMPARATIVE, STRUCTURAL, REPOSITORY) |
| **Direction** | Asymmetric or Symmetric |
| **Reflexivity** | Can entity relate to itself? (rarely yes; usually no) |
| **Symmetry** | If symmetric, how? |
| **Transitivity** | Transitive, Non-transitive, or Conditional-transitive |
| **Inverse Predicate** | PRD identifier of inverse (if applicable) |
| **Inferability** | YES, NO, or CONDITIONAL; under what conditions can it be inferred? |
| **Lifecycle Notes** | How does relationship persist through entity lifecycle changes? |
| **Validation Notes** | Specific validation checks for this predicate |
| **Version History** | v1.0 definition, v1.1 revisions, etc. |
| **Deprecation Status** | Active, Deprecated (with reason and successor), or
Withdrawn |
| **Date Defined** | Date predicate was approved and added to canonical register |
| **Examples** | Representative abstract structural illustrations |
| **Related Predicates** | Other predicates with which this one commonly co-occurs |
---
### APPENDIX A.1: CLASS A — DOCUMENTARY OPERATIONS
#### PRD-000000001: CITES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000001 |
| **Preferred Label** | cites |
| **Aliases** | refers to, references |
| **Definition** | Subject refers to Object without reproducing its words. The subject
contains an explicit reference to the object's identity, location, or content, recoverable
from the source text or witness. |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Witness, Work Component, Witness
Component, Passage |
| **Object Classes** | Work, Expression, Witness, Work Component, Witness
Component, Passage |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric (A cites B does not imply B cites A) |
| **Transitivity** | Non-transitive (A cites B and B cites C does not imply A cites C) |
| **Inverse Predicate** | PRD-000000002 (cited_by) |
| **Inferability** | NO (citation relationships are not inferred; they must be observed and
explicitly asserted) |
| **Lifecycle Notes** | If Object is merged into another entity, the Relationship Assertion
remains pointing to the original Object identifier. No automatic resolution occurs. A new
Relationship Assertion may be created pointing to the merged target, but the original is
preserved. If Subject is superseded, historical references to the original subject remain
unchanged. |
| **Validation Notes** | Subject must be a documentary entity capable of containing
citations. Object must exist and be independently identifiable. Evidence must be
recoverable (Location within Subject Witness pointing to Object reference). Textual
match or semantic similarity alone is insufficient; explicit reference is required. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | WORK-A --cites--> WORK-B (one intellectual work refers to another).
HERMENEUTIC
_OBJECT --cites--> EXPRESSION (analysis cites source material).
PASSAGE --cites--> WORK (quoted segment cites original work). |
| **Related Predicates** | PRD-000000003 (quotes), PRD-000000002 (cited_by),
PRD-000000005 (selects) |
---
#### PRD-000000002: CITED
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000002 |
| **Preferred Label** | cited_by |
| **Aliases** | is referenced by, is referred to by |
| **Definition** | Subject is cited by (referred to without quotation by) Object. Inverse of
CITES (PRD-000000001). |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Witness, Work Component, Witness
Component, Passage |
| **Object Classes** | Work, Expression, Witness, Work Component, Witness
Component, Passage |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric (though symmetric with CITES if both directions are
asserted) |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000001 (cites) |
| **Inferability** | NO (inverse of CITES, but not inferred; explicitly asserted when
needed for bidirectional clarity) |
| **Lifecycle Notes** | Same as CITES |
| **Validation Notes** | Same as CITES |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | WORK-B --cited_by--> WORK-A (inverse of WORK-A --cites-->
WORK-B). SOURCE_
MATERIAL --cited
_by--> ANALYSIS (reverse perspective). |
| **Related Predicates** | PRD-000000001 (cites), PRD-000000004 (quoted_by) |
---
#### PRD-000000003: QUOTES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000003 |
| **Preferred Label** | quotes |
| **Aliases** | reproduces text from, excerpts from |
| **Definition** | Subject reproduces wording from Object. The subject must contain
reproduced wording from the object, and the reproduced text must be identifiable and
recoverable in the object. |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Witness, Work Component, Witness
Component, Passage |
| **Object Classes** | Work, Expression, Witness, Work Component, Witness
Component, Passage |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000004 (quoted_by) |
| **Inferability** | NO (quotation must be explicitly documented and verified) |
| **Lifecycle Notes** | Same as CITES |
| **Validation Notes** | Reproduced text must be recoverable in both Subject and
Object. Quotation location(s) must be specified or recoverable through evidence
citations. Paraphrase alone is not sufficient; the predicate QUOTES requires textual
reproduction. Distinction from CITES: CITES documents a reference; QUOTES
documents a textual reproduction. Both may be present: Subject both quotes Object
and cites it. They are distinct assertions. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ANALYSIS --quotes--> MANUSCRIPT (analysis reproduces text from
source). HERMENEUTIC_OBJECT --quotes--> PRIMARY_SOURCE (interpretation
includes exact wording). PASSAGE --quotes--> ORIGINAL_WORK (quoted segment
reproduces exact text). |
| **Related Predicates** | PRD-000000001 (cites), PRD-000000004 (quoted_by) |
---
#### PRD-000000004: QUOTED_
BY
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000004 |
| **Preferred Label** | quoted_by |
| **Aliases** | is quoted by, is excerpted by |
| **Definition** | Subject's wording is reproduced by Object. Inverse of QUOTES
(PRD-000000003). |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Witness, Work Component, Witness
Component, Passage |
| **Object Classes** | Work, Expression, Witness, Work Component, Witness
Component, Passage |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000003 (quotes) |
| **Inferability** | NO |
| **Lifecycle Notes** | Same as QUOTES |
| **Validation Notes** | Same as QUOTES |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | MANUSCRIPT --quoted_by--> ANALYSIS (inverse of ANALYSIS --
quotes--> MANUSCRIPT). PRIMARY_SOURCE --quoted_by-->
HERMENEUTIC
_OBJECT (source is quoted in interpretation). |
| **Related Predicates** | PRD-000000003 (quotes), PRD-000000002 (cited_by) |
---
#### PRD-000000005: SELECTS
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000005 |
| **Preferred Label** | selects |
| **Aliases** | chooses, emphasizes, includes |
| **Definition** | Subject deliberately includes or emphasizes particular portions of
Object material. |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Work Component, Witness Component,
Inquiry, Citation Object, Hermeneutic Object |
| **Object Classes** | Work, Expression, Witness, Passage, Theme |
| **Evidence Type** | DOCUMENTARY or PROCEDURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000006 (selected_by) |
| **Inferability** | CONDITIONAL (Selection may be inferred when omission is
documented as complementary evidence, but explicit assertion is preferred) |
| **Lifecycle Notes** | Preserved through lifecycle changes. |
| **Validation Notes** | If documentary: selected material must be identifiable and
distinguishable from omitted alternatives. If procedural: Repository decision must be
documented in a cited Repository Artifact (Hermeneutic Object, Documentary Decision
Record). |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ANALYSIS --selects--> PASSAGE (particular quotation is chosen for
emphasis). COMPARISON --selects--> EXPRESSION-A, EXPRESSION-B, EXPRESSION-
C (three expressions chosen for comparative analysis). RECONSTRUCTION --selects--
> THEME (specific theme is emphasized in reconstruction). |
| **Related Predicates** | PRD-000000007 (omits), PRD-000000006 (selected_by) |
---
#### PRD-000000006: SELECTED
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000006 |
| **Preferred Label** | selected_by |
| **Aliases** | is chosen by, is emphasized by |
| **Definition** | Subject is deliberately selected and emphasized by Object. Inverse of
SELECTS (PRD-000000005). |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Witness, Passage, Theme |
| **Object Classes** | Work, Expression, Work Component, Witness Component,
Inquiry, Citation Object, Hermeneutic Object |
| **Evidence Type** | DOCUMENTARY or PROCEDURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000005 (selects) |
| **Inferability** | CONDITIONAL |
| **Lifecycle Notes** | Preserved through changes. |
| **Validation Notes** | Same as SELECTS |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | PASSAGE --selected_by--> ANALYSIS (inverse of ANALYSIS --
selects--> PASSAGE). THEME --selected_by--> RECONSTRUCTION (theme is selected
and emphasized). |
| **Related Predicates** | PRD-000000005 (selects), PRD-000000008 (omitted_by) |
---
#### PRD-000000007: OMITS
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000007 |
| **Preferred Label** | omits |
| **Aliases** | excludes, leaves out, neglects |
| **Definition** | Subject demonstrates absence of material present in Object. Material
must be demonstrably available in Object, same or related material must be discussed
elsewhere in Subject, and absence must be demonstrable (not merely speculative). |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Witness, Inquiry, Hermeneutic Object |
| **Object Classes** | Work, Expression, Witness, Passage, Theme |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000008 (omitted_by) |
| **Inferability** | CONDITIONAL (Omission may be inferred from demonstrated
selection, but explicit assertion is required for canonical relationships) |
| **Lifecycle Notes** | Preserved through changes. |
| **Validation Notes** | Material must exist in Object (verifiable). Absence must be
recoverable through comparison, not inferred from silence. Absence of evidence is not
evidence of absence; only demonstrable omission counts. Distinction from SELECTS:
SELECTS documents active inclusion. OMITS documents demonstrable absence. Both
may be asserted: Subject selects some material while omitting related material. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ANALYSIS --omits--> PASSAGE (passage that might be expected is
not discussed). INTERPRETATION --omits--> THEME (related theme is absent from
interpretation). RECONSTRUCTION --omits--> ALTERNATIVE_APPROACH (contrasting
approach is omitted). |
| **Related Predicates** | PRD-000000005 (selects), PRD-000000008 (omitted_by) |
---
#### PRD-000000008: OMITTED
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000008 |
| **Preferred Label** | omitted_by |
| **Aliases** | is excluded by, is left out of |
| **Definition** | Subject's potential content is omitted by Object. Inverse of OMITS
(PRD-000000007). |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Witness, Passage, Theme |
| **Object Classes** | Work, Expression, Witness, Inquiry, Hermeneutic Object |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000007 (omits) |
| **Inferability** | CONDITIONAL |
| **Lifecycle Notes** | Preserved through changes. |
| **Validation Notes** | Same as OMITS |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | PASSAGE --omitted_by--> ANALYSIS (inverse of ANALYSIS --omits-->
PASSAGE). THEME --omitted_by--> INTERPRETATION (theme is omitted). |
| **Related Predicates** | PRD-000000007 (omits), PRD-000000006 (selected_by) |
---
#### PRD-000000009: PLACES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000009 |
| **Preferred Label** | places |
| **Aliases** | positions, arranges at location |
| **Definition** | Subject positions or arranges Object material in a particular structural
location. Placement must be observable in the source text or reconstructed through
evidence of authorial decision. |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Inquiry, Hermeneutic Object |
| **Object Classes** | Passage, Citation, Quotation, Work Component, Documentary
Operation |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000010 (placed_by) |
| **Inferability** | NO (Placement is observable, not inferred) |
| **Lifecycle Notes** | Preserved through changes. |
| **Validation Notes** | Both subject and object must have recoverable structure.
Placement location must be specified or recoverable. Examples: observable chapter
position, section position, or argument structure in source; or reconstruction via
comparison with prior versions or alternative arrangements. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ANALYSIS --places--> PASSAGE (in section_3 of the analysis). WORK
--places--> CITATION_
TO
_SOURCE (in opening chapter). INTERPRETATION --places--
> MOTIF (motif appears in final section). |
| **Related Predicates** | PRD-000000010 (placed_by), PRD-000000011 (sequences) |
---
#### PRD-000000010: PLACED
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000010 |
| **Preferred Label** | placed_by |
| **Aliases** | is positioned by, is arranged by |
| **Definition** | Subject's content is placed at a structural location by Object. Inverse
of PLACES (PRD-000000009). |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Passage, Citation, Quotation, Work Component, Documentary
Operation |
| **Object Classes** | Work, Expression, Inquiry, Hermeneutic Object |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000009 (places) |
| **Inferability** | NO |
| **Lifecycle Notes** | Preserved through changes. |
| **Validation Notes** | Same as PLACES |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | PASSAGE --placed_by--> ANALYSIS (inverse of ANALYSIS --places-->
PASSAGE). CITATION --placed_by--> WORK (in opening chapter). |
| **Related Predicates** | PRD-000000009 (places), PRD-000000012 (sequenced_by)
|
---
#### PRD-000000011: SEQUENCES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000011 |
| **Preferred Label** | sequences |
| **Aliases** | orders, arranges in sequence |
| **Definition** | Subject orders or arranges Object entities in a specific sequence.
Sequence must be observable in source or recoverable through evidence. |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Work, Expression, Inquiry, Hermeneutic Object, Comparative
Reconstruction |
| **Object Classes** | Citation, Quotation, Passage, Claim, Documentary Operation,
Question |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000012 (sequenced_by) |
| **Inferability** | NO (Sequence is structural, not inferred) |
| **Lifecycle Notes** | Preserved through changes. |
| **Validation Notes** | Objects must be enumerable and orderable. Sequence must be
recoverable and meaningful (not arbitrary). Multiple objects may be sequenced in one
assertion (e.g., SEQUENCES [CLAIM-1, CLAIM-2, CLAIM-3]). |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ARCHITECTURE_RECORD --sequences--> CLAIM-1, CLAIM-2,
CLAIM-3 (order of claims in argument). ANALYSIS --sequences--> PASSAGE-1,
PASSAGE-2, PASSAGE-3 (textual order). INTERPRETATION --sequences--> THEME-1,
THEME-2, THEME-3 (thematic progression). |
| **Related Predicates** | PRD-000000009 (places), PRD-000000012 (sequenced_by)
|
---
#### PRD-000000012: SEQUENCED_
BY
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000012 |
| **Preferred Label** | sequenced_by |
| **Aliases** | is ordered by, is arranged in sequence by |
| **Definition** | Subject is ordered by Object in a particular sequence. Inverse of
SEQUENCES (PRD-000000011). |
| **Predicate Class** | A — Documentary Operations |
| **Subject Classes** | Citation, Quotation, Passage, Claim, Documentary Operation,
Question |
| **Object Classes** | Work, Expression, Inquiry, Hermeneutic Object, Comparative
Reconstruction |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000011 (sequences) |
| **Inferability** | NO |
| **Lifecycle Notes** | Preserved through changes. |
| **Validation Notes** | Same as SEQUENCES |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | CLAIM-1 --sequenced_by--> ARCHITECTURE_RECORD (first in
argument sequence). PASSAGE-1 --sequenced_by--> ANALYSIS (initial passage in
text). |
| **Related Predicates** | PRD-000000011 (sequences), PRD-000000010 (placed_by) |
---
### APPENDIX A.2: CLASS B — EVIDENTIARY RELATIONSHIPS
#### PRD-000000013: SUPPORTS
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000013 |
| **Preferred Label** | supports |
| **Aliases** | provides evidence for, backs |
| **Definition** | Subject provides evidence, context, or logical support for Object. The
Evidence Record or Repository Artifact documenting why Subject supports Object must
be citable and recoverable. |
| **Predicate Class** | B — Evidentiary Relationships |
| **Subject Classes** | Passage, Claim, Evidence Record, Citation, Quotation, Witness,
Observation |
| **Object Classes** | Claim, Interpretation, Hypothesis, Question, Certification Record |
| **Evidence Type** | REPOSITORY or PROCEDURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive (though chains of support are common) |
| **Inverse Predicate** | PRD-000000014 (supported_by) |
| **Inferability** | CONDITIONAL (Support may be inferred through Evidence Records,
but explicit assertion preferred) |
| **Lifecycle Notes** | Preserved. If Subject is corrected or revised, the supporting
relationship may acquire disputed or corrected lifecycle marking, but is not deleted. |
| **Validation Notes** | Object must be a Claim, Interpretation, or Question requiring
support. Subject must be a documentary or evidentiary entity. Support must be
documented in Evidence Record, Hermeneutic Object, or Repository Artifact. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | PASSAGE --supports--> CLAIM (textual evidence supports claim).
EVIDENCE
_RECORD --supports--> CLAIM (formal evidence documentation).
CERTIFICATION
_RECORD --supports--> ARTIFACT (verification supports artifact
standing). |
| **Related Predicates** | PRD-000000014 (supported_by), PRD-000000015
(contradicts), PRD-000000017 (contextualizes) |
---
#### PRD-000000014: SUPPORTED
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000014 |
| **Preferred Label** | supported_by |
| **Aliases** | is evidenced by, is backed by |
| **Definition** | Subject is supported (evidenced) by Object. Inverse of SUPPORTS
(PRD-000000013). |
| **Predicate Class** | B — Evidentiary Relationships |
| **Subject Classes** | Claim, Interpretation, Hypothesis, Question, Certification Record
|
| **Object Classes** | Passage, Claim, Evidence Record, Citation, Quotation, Witness,
Observation |
| **Evidence Type** | REPOSITORY or PROCEDURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000013 (supports) |
| **Inferability** | CONDITIONAL |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as SUPPORTS |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | CLAIM --supported_by--> PASSAGE (inverse perspective).
INTERPRETATION --supported_by--> EVIDENCE_RECORD (formal support). |
| **Related Predicates** | PRD-000000013 (supports), PRD-000000016 (disagrees) |
---
#### PRD-000000015: CONTRADICTS
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000015 |
| **Preferred Label** | contradicts |
| **Aliases** | is logically incompatible with, opposes |
| **Definition** | Subject and Object make logically or semantically incompatible
assertions. Contradiction must be documented through explicit comparison, not merely
inferred difference. |
| **Predicate Class** | B — Evidentiary Relationships |
| **Subject Classes** | Claim, Interpretation, Observation, Witness, Work, Expression,
Hypothesis |
| **Object Classes** | Claim, Interpretation, Observation, Witness, Work, Expression,
Hypothesis |
| **Evidence Type** | DOCUMENTARY or REPOSITORY |
| **Direction** | Symmetric |
| **Reflexivity** | NO |
| **Symmetry** | Symmetric (A contradicts B ≡ B contradicts A) |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | (Symmetric; no separate inverse) |
| **Inferability** | NO (Logical contradiction cannot be inferred; must be explicitly
documented) |
| **Lifecycle Notes** | Preserved. Contradictions not resolved by deletion; remain even
if one entity is superseded. |
| **Validation Notes** | Both entities must be assertive (Claims, Interpretations,
Observations, or comparable). Contradiction must be substantive, not merely different
phrasings. Must be documented with reasoning (evidence citations, comparative
references). Distinction from DISAGREES: CONTRADICTS documents logical
impossibility (A and B cannot both be true). DISAGREES documents difference of
opinion. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | CLAIM-A --contradicts--> CLAIM-B (on specific point).
INTERPRETATION-1 --contradicts--> INTERPRETATION-2 (opposed hermeneutic
views). WITNESS-ACCOUNT-1 --contradicts--> WITNESS-ACCOUNT-2 (conflicting
factual reports). |
| **Related Predicates** | PRD-000000016 (disagrees), PRD-000000013 (supports) |
---
#### PRD-000000016: DISAGREES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000016 |
| **Preferred Label** | disagrees |
| **Aliases** | differs from, diverges from |
| **Definition** | Subject and Object represent differing accounts, interpretations, or
observations without necessarily implying logical contradiction. |
| **Predicate Class** | B — Evidentiary Relationships |
| **Subject Classes** | Witness, Claim, Interpretation, Account, Documentary Register
Entry |
| **Object Classes** | Witness, Claim, Interpretation, Account, Documentary Register
Entry |
| **Evidence Type** | DOCUMENTARY or REPOSITORY |
| **Direction** | Symmetric |
| **Reflexivity** | NO |
| **Symmetry** | Symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | (Symmetric; no separate inverse) |
| **Inferability** | NO (Disagreement requires documentation) |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Disagreement must be substantive and recoverable. Both sides
representable without forcing logical contradiction. Distinction from CONTRADICTS:
CONTRADICTS = logical impossibility. DISAGREES = difference of opinion without
mutual exclusivity. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | WITNESS-ACCOUNT-A --disagrees--> WITNESS-ACCOUNT-B (on
historical dating). INTERPRETATION-1 --disagrees--> INTERPRETATION-2 (different
scholarly perspectives). |
| **Related Predicates** | PRD-000000015 (contradicts) |
---
#### PRD-000000017: CONTEXTUALIZES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000017 |
| **Preferred Label** | contextualizes |
| **Aliases** | provides background for, illuminates |
| **Definition** | Subject provides necessary background or setting for understanding
Object. Repository decision to include Context must be documented in the Context
entity itself (Ontology 14). |
| **Predicate Class** | B — Evidentiary Relationships |
| **Subject Classes** | Passage, Work, Expression, Context, Historical Record |
| **Object Classes** | Claim, Interpretation, Passage, Work, Expression |
| **Evidence Type** | REPOSITORY or PROCEDURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000018 (contextualized_by) |
| **Inferability** | CONDITIONAL (Context may be inferred from Hermeneutic Object's
structure, but explicit assertion preferred) |
| **Lifecycle Notes** | Preserved. Context maintained even if focal entity changes. |
| **Validation Notes** | Context must be retrievable and bounded. Relationship must
document why context is necessary. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | CONTEXT_MATERIAL --contextualizes--> CLAIM (historical
background). HISTORICAL_RECORD --contextualizes--> INTERPRETATION (provides
setting). PASSAGE --contextualizes--> ANALYSIS (textual context). |
| **Related Predicates** | PRD-000000018 (contextualized_by), PRD-000000013
(supports) |
---
#### PRD-000000018: CONTEXTUALIZED
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000018 |
| **Preferred Label** | contextualized_by |
| **Aliases** | is given context by, requires background from |
| **Definition** | Subject requires context provided by Object for full understanding.
Inverse of CONTEXTUALIZES (PRD-000000017). |
| **Predicate Class** | B — Evidentiary Relationships |
| **Subject Classes** | Claim, Interpretation, Passage, Work, Expression |
| **Object Classes** | Passage, Work, Expression, Context, Historical Record |
| **Evidence Type** | REPOSITORY or PROCEDURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000017 (contextualizes) |
| **Inferability** | CONDITIONAL |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as CONTEXTUALIZES |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | CLAIM --contextualized_by--> CONTEXT_MATERIAL (inverse
perspective). INTERPRETATION --contextualized_by--> HISTORICAL_
RECORD
(requires historical understanding). |
| **Related Predicates** | PRD-000000017 (contextualizes) |
---
#### PRD-000000019: CORRELATES
WITH
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000019 |
| **Preferred Label** | correlates_with |
| **Aliases** | has correlation with, shows pattern similar to |
| **Definition** | Subject and Object exhibit similar structure, theme, or pattern without
necessarily being causally or logically related. |
| **Predicate Class** | B — Evidentiary Relationships |
| **Subject Classes** | Passage, Claim, Interpretation, Witness, Work, Theme |
| **Object Classes** | Passage, Claim, Interpretation, Witness, Work, Theme |
| **Evidence Type** | REPOSITORY or COMPARATIVE |
| **Direction** | Symmetric |
| **Reflexivity** | NO |
| **Symmetry** | Symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | (Symmetric; no separate inverse) |
| **Inferability** | NO (Correlation must be explicitly documented) |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Similarity must be substantive and recoverable. Correlation must
be distinguished from causal, logical, or identity relationship. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | PASSAGE-A --correlates_with--> PASSAGE-B (similar structural
patterns). THEME-1 --correlates_with--> THEME-2 (parallel thematic elements). |
| **Related Predicates** | PRD-000000047 (parallels), PRD-000000048
(contrasts_with) |
---
### APPENDIX A.3: CLASS C — DERIVATION AND TRANSFORMATION RELATIONSHIPS
#### PRD-000000020: DERIVES
FROM
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000020 |
| **Preferred Label** | derives_from |
| **Aliases** | is created from, is produced from |
| **Definition** | Subject is created or produced from Object through a documented
transformation or reproduction process. Derivation must be documented through a
Derivation Record (DER-xxxxxxxxx) specifying transformation process, date, authority,
and metadata. |
| **Predicate Class** | C — Derivation and Transformation Relationships |
| **Subject Classes** | Witness, Expression, Transcription, Derived Witness, Work
Component, Evidence Record, Claim, Interpretation |
| **Object Classes** | Witness, Expression, Work, Work Component, Claim, Evidence
Record, Source Witness |
| **Evidence Type** | PROCEDURAL or DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Transitive (A derives_
from B and B derives
_from C implies A
derives
_from C) |
| **Inverse Predicate** | PRD-000000021 (source_of) |
| **Inferability** | CONDITIONAL (Chains may be inferred through transitive closure, but
explicit assertion required) |
| **Lifecycle Notes** | Preserved. Derivation chains remain intact through lifecycle
changes. If Object is superseded or corrected, all Derived entities may acquire disputed
or review-required status. |
| **Validation Notes** | Derivation Record must exist and be recoverable. Object must
be immediate or ultimate source. Transformation must be documented (lossy,
encoding, normalization, revision, etc.). Distinction from TRANSLATES, EDITS,
NORMALIZES: DERIVES
_FROM is umbrella; others are specific types. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | DIGITAL_
SCAN --derives
_from--> MANUSCRIPT (scan created from
original). OCR_
TEXT --derives
from--> DIGITAL
_
_SCAN (text generated from image).
NORMALIZED
EDITION --derives
from--> DIPLOMATIC
TRANSCRIPTION
_
_
_
(standardized from original). |
| **Related Predicates** | PRD-000000021 (source_of), PRD-000000022 (translates),
PRD-000000024 (edits), PRD-000000026 (normalizes) |
---
#### PRD-000000021: SOURCE
OF
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000021 |
| **Preferred Label** | source_of |
| **Aliases** | is source for, produces |
| **Definition** | Subject is the source from which Object is derived. Inverse of
DERIVES
_FROM (PRD-000000020). |
| **Predicate Class** | C — Derivation and Transformation Relationships |
| **Subject Classes** | Witness, Expression, Work, Work Component, Claim, Evidence
Record, Source Witness |
| **Object Classes** | Witness, Expression, Transcription, Derived Witness, Work
Component, Evidence Record, Claim, Interpretation |
| **Evidence Type** | PROCEDURAL or DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Transitive |
| **Inverse Predicate** | PRD-000000020 (derives_from) |
| **Inferability** | CONDITIONAL |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as DERIVES_FROM |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | MANUSCRIPT --source_
of--> DIGITAL
_SCAN (inverse perspective).
ORIGINAL
TEXT --source
of--> NORMALIZED
_
_
_EDITION (original serves as source). |
| **Related Predicates** | PRD-000000020 (derives_from) |
---
#### PRD-000000022: TRANSLATES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000022 |
| **Preferred Label** | translates |
| **Aliases** | is a translation of, renders into language |
| **Definition** | Subject is a translation of Object into a different language. Translation
relationship must be documented with source language, target language (via controlled
vocabulary), translator or translation authority (Agent identifier), date, and fidelity level
or translation method. |
| **Predicate Class** | C — Derivation and Transformation Relationships |
| **Subject Classes** | Expression, Translation, Witness |
| **Object Classes** | Expression, Work, Witness |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000023 (translated_from) |
| **Inferability** | NO (Translation is documentary, not inferred) |
| **Lifecycle Notes** | Preserved. Translation relationships remain stable. |
| **Validation Notes** | Languages must be distinct (verifiable). Translation must be
identifiable and recoverable. Translation authority must be documented. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ITALIAN_
TRANSLATION --translates--> ORIGINAL
_TEXT (Italian
rendering). ENGLISH_
VERSION --translates--> GREEK
_ORIGINAL (English from Greek).
FRENCH
ADAPTATION --translates--> SOURCE
_
_WORK (translation into French). |
| **Related Predicates** | PRD-000000023 (translated_from), PRD-000000020
(derives_from) |
---
#### PRD-000000023: TRANSLATED
FROM
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000023 |
| **Preferred Label** | translated_from |
| **Aliases** | is the original of a translation |
| **Definition** | Subject is the original work from which Object is translated. Inverse of
TRANSLATES (PRD-000000022). |
| **Predicate Class** | C — Derivation and Transformation Relationships |
| **Subject Classes** | Expression, Work, Witness |
| **Object Classes** | Expression, Translation, Witness |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000022 (translates) |
| **Inferability** | NO |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as TRANSLATES |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ORIGINAL_
TEXT --translated
from--> ITALIAN
TRANSLATION
_
_
(inverse perspective). GREEK_
ORIGINAL --translated
from--> ENGLISH
VERSION
_
_
(original for English translation). |
| **Related Predicates** | PRD-000000022 (translates) |
---
#### PRD-000000024: EDITS
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000024 |
| **Preferred Label** | edits |
| **Aliases** | is an editorial constitution of |
| **Definition** | Subject is an editorially constituted version of Object. Editorial
relationship must document editorial principles (diplomatic, normalized, critical, etc.),
editor or editorial authority (Agent identifier), emendations or departures from base
text, apparatus or commentary included, and relationship to prior editions. |
| **Predicate Class** | C — Derivation and Transformation Relationships |
| **Subject Classes** | Expression, Edition or Recension, Witness |
| **Object Classes** | Expression, Work, Witness |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000025 (edited_to) |
| **Inferability** | NO (Editorial decisions are not inferred; they are documented) |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Editorial entity must be identifiable. Editorial principles must be
recoverable. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | CRITICAL_
EDITION --edits--> ORIGINAL
_WORK (editorial
constitution). ANNOTATED_
VERSION --edits--> BASE
_TEXT (editing with
commentary). REVISED_TEXT --edits--> MANUSCRIPT (editorial revision). |
| **Related Predicates** | PRD-000000025 (edited_to), PRD-000000020
(derives_from) |
---
#### PRD-000000025: EDITED
TO
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000025 |
| **Preferred Label** | edited_to |
| **Aliases** | is the base for an edition |
| **Definition** | Subject is the base work or expression for which Object is an editorial
constitution. Inverse of EDITS (PRD-000000024). |
| **Predicate Class** | C — Derivation and Transformation Relationships |
| **Subject Classes** | Expression, Work, Witness |
| **Object Classes** | Expression, Edition or Recension, Witness |
| **Evidence Type** | DOCUMENTARY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000024 (edits) |
| **Inferability** | NO |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as EDITS |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ORIGINAL_
WORK --edited
to--> CRITICAL
_
_EDITION (inverse
perspective). MANUSCRIPT --edited_
to--> ANNOTATED
_VERSION (base for editorial
work). |
| **Related Predicates** | PRD-000000024 (edits) |
---
#### PRD-000000026: NORMALIZES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000026 |
| **Preferred Label** | normalizes |
| **Aliases** | applies standardization to, regularizes |
| **Definition** | Subject applies systematic standardization to Object (orthography,
encoding, format, typography). Normalization must document normalization rules
applied (controlled vocabulary of normalization types), authority or tool (Agent,
software version), reversibility, and loss or alteration of information. |
| **Predicate Class** | C — Derivation and Transformation Relationships |
| **Subject Classes** | Expression, Witness |
| **Object Classes** | Expression, Witness |
| **Evidence Type** | PROCEDURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000027 (normalized_to) |
| **Inferability** | NO (Normalization is procedural, not inferred) |
| **Lifecycle Notes** | Preserved. Normalized versions remain linked to sources. |
| **Validation Notes** | Normalization rules must be specific and recoverable. Source
must be recoverable. Information loss must be documented. Distinction from
TRANSLATES: TRANSLATES changes language; NORMALIZES standardizes within
same language/format. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | STANDARDIZED_
TEXT --normalizes--> RAW
OCR
OUTPUT
_
_
(standardization applied). UNICODE_
VERSION --normalizes--> LEGACY
_
(encoding standardization). REGULARIZED_
FORM --normalizes-->
ORIGINAL
_ORTHOGRAPHY (orthographic regularization). |
| **Related Predicates** | PRD-000000027 (normalized_to), PRD-000000020
(derives_from) |
ENCODING
---
#### PRD-000000027: NORMALIZED
TO
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000027 |
| **Preferred Label** | normalized_to |
| **Aliases** | undergoes normalization to, is standardized as |
| **Definition** | Subject is the source material that Object normalizes. Inverse of
NORMALIZES (PRD-000000026). |
| **Predicate Class** | C — Derivation and Transformation Relationships |
| **Subject Classes** | Expression, Witness |
| **Object Classes** | Expression, Witness |
| **Evidence Type** | PROCEDURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000026 (normalizes) |
| **Inferability** | NO |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as NORMALIZES |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | RAW_
OCR
OUTPUT --normalized
to--> STANDARDIZED
TEXT
_
_
_
(inverse perspective). LEGACY_
ENCODING --normalized
to--> UNICODE
VERSION
_
_
(encoding normalization result). |
| **Related Predicates** | PRD-000000026 (normalizes) |
---
### APPENDIX A.4: CLASS D — IDENTITY AND COMPOSITION RELATIONSHIPS
#### PRD-000000028: MERGED
WITH
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000028 |
| **Preferred Label** | merged_with |
| **Aliases** | is identified as same as, is unified with |
| **Definition** | Subject and Object are determined to represent the same entity;
identities are unified while both are preserved historically. Merger decision must be
documented through Documentary Decision Record (DDR-xxxxxxxxx) explaining why
entities are identical, evidence or comparison supporting merger, designation of which
identifier is retained as current, and mapping of historical references. |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Any identity-bearing entity |
| **Object Classes** | Same class as Subject |
| **Evidence Type** | REPOSITORY |
| **Direction** | Symmetric |
| **Reflexivity** | NO |
| **Symmetry** | Symmetric |
| **Transitivity** | Transitive (if A merged_with B and B merged_with C, all three are
equivalent) |
| **Inverse Predicate** | (Symmetric; no separate inverse) |
| **Inferability** | NO (Mergers require human judgment and documentary analysis) |
| **Lifecycle Notes** | Both identifiers preserved in historical record. One may be
designated as current; other receives merged lifecycle status. All references to either
remain valid and auditable. |
| **Validation Notes** | Entities must belong to same ontology class or demonstrably
equivalent classes. Merger decision must be documented. No cycles permitted. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ENTITY-A --merged_with--> ENTITY-B (same work discovered).
AGENT-A --merged_with--> AGENT-B (same person, variant names). |
| **Related Predicates** | PRD-000000029 (split_into), PRD-000000031 (supersedes) |
---
#### PRD-000000029: SPLIT
_
INTO
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000029 |
| **Preferred Label** | split_into |
| **Aliases** | is determined to contain, divides into |
| **Definition** | Subject is determined to contain multiple entities; Object list comprises
the resulting distinct entities. Split decision must be documented through Documentary
Decision Record explaining why entities were distinct, evidence distinguishing them,
and mapping of original references. |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Any identity-bearing entity |
| **Object Classes** | Same class as Subject (plural/set notation) |
| **Evidence Type** | REPOSITORY |
| **Direction** | Asymmetric (one-to-many) |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000030 (split_from) — applied individually |
| **Inferability** | NO (Splits require human analysis) |
| **Lifecycle Notes** | Original identifier remains historically valid but receives split
lifecycle status. Each resulting entity receives new canonical identifier. Historical
references unchanged. |
| **Validation Notes** | Split must be substantive and well-documented. Each resulting
entity must be independently distinguishable. Split decisions should indicate how
references distributed. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ENTITY-A --split_into--> [ENTITY-B, ENTITY-C] (two entities
discovered). COMPOSITE --split_into--> [PART-1, PART-2, PART-3] (multi-part split). |
| **Related Predicates** | PRD-000000030 (split_from), PRD-000000028
(merged_with) |
---
#### PRD-000000030: SPLIT
FROM
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000030 |
| **Preferred Label** | split_from |
| **Aliases** | is a result of split from, derives from split |
| **Definition** | Subject is one result of splitting the original entity Object. Inverse of
SPLIT
_INTO (PRD-000000029). |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Any identity-bearing entity |
| **Object Classes** | Same class as Subject |
| **Evidence Type** | REPOSITORY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000029 (split_into) |
| **Inferability** | NO |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as SPLIT_INTO |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ENTITY-B --split_from--> ENTITY-A (inverse perspective). PART-1 --
split_from--> COMPOSITE (result of split). |
| **Related Predicates** | PRD-000000029 (split_into) |
---
#### PRD-000000031: SUPERSEDES
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000031 |
| **Preferred Label** | supersedes |
| **Aliases** | replaces, improves upon, revises |
| **Definition** | Subject is a replacement for, revision of, or improvement upon Object.
Supersession must document reason for replacement, what changed and why, whether
Object remains valid for historical reference, and effective date. |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Repository Artifact, Citation Object, Hermeneutic Object,
Comparative Reconstruction, Repository Synthesis, Claim, Interpretation, Witness |
| **Object Classes** | Same class as Subject |
| **Evidence Type** | REPOSITORY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive (though chains common) |
| **Inverse Predicate** | PRD-000000032 (superseded_by) |
| **Inferability** | NO (Supersession requires human judgment) |
| **Lifecycle Notes** | Both identifiers preserved. Object may remain active (for
historical reference) or marked withdrawn/superseded. Subject acquires relationship
marking supersession. Historical references remain visible. |
| **Validation Notes** | Subject and Object must belong to compatible classes.
Supersession must be documented with rationale and evidence. Distinction from
MERGED
_WITH: SUPERSEDES = replacement/improvement. MERGED_WITH = identity.
SUPERSEDES asymmetric; MERGED_WITH symmetric. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ARTIFACT-NEW --supersedes--> ARTIFACT-OLD (newer
investigation). IMPROVED_ANALYSIS --supersedes--> PRELIMINARY_
ANALYSIS
(corrected analysis). REVISED_INTERPRETATION --supersedes--> INITIAL_
READING
(refined understanding). |
| **Related Predicates** | PRD-000000032 (superseded_by), PRD-000000028
(merged_with) |
---
#### PRD-000000032: SUPERSEDED
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000032 |
| **Preferred Label** | superseded_by |
| **Aliases** | is replaced by, is revised as |
| **Definition** | Subject is replaced or improved upon by Object. Inverse of
SUPERSEDES (PRD-000000031). |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Repository Artifact, Citation Object, Hermeneutic Object,
Comparative Reconstruction, Repository Synthesis, Claim, Interpretation, Witness |
| **Object Classes** | Same class as Subject |
| **Evidence Type** | REPOSITORY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000031 (supersedes) |
| **Inferability** | NO |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as SUPERSEDES |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | ARTIFACT-OLD --superseded_by--> ARTIFACT-NEW (inverse
perspective). PRELIMINARY_ANALYSIS --superseded_by--> IMPROVED_
ANALYSIS
(replaced). |
| **Related Predicates** | PRD-000000031 (supersedes) |
---
#### PRD-000000033: WITHDRAWN
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000033 |
| **Preferred Label** | withdrawn_by |
| **Aliases** | is retracted by, is declared invalid by |
| **Definition** | Subject is determined to be erroneous, fraudulent, unreliable, or
otherwise unfit for continued use; withdrawn by Repository decision documented in
Object. Withdrawal must document reason (error, fraud, unreliability), evidence of error
or fraud, replacement or corrective action (if any), effective date, and responsible
authority. |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Any entity, particularly Repository Artifacts, Claims, Witnesses,
Works |
| **Object Classes** | Correction Record, Documentary Decision Record, or Withdrawal
Record |
| **Evidence Type** | REPOSITORY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000034 (withdraws) |
| **Inferability** | NO (Withdrawal requires formal Repository decision) |
| **Lifecycle Notes** | Subject receives tombstoned or withdrawn lifecycle status.
Historical references remain visible. |
| **Validation Notes** | Withdrawal must be substantive and documented. Reason must
be recoverable. If replacement provided, should be linked via Relationship Assertion. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | SOURCE --withdrawn_by--> DECISION_RECORD (source determined
fraudulent). CLAIM --withdrawn_by--> CORRECTION_RECORD (claim found
erroneous). |
| **Related Predicates** | PRD-000000034 (withdraws) |
---
#### PRD-000000034: WITHDRAWS
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000034 |
| **Preferred Label** | withdraws |
| **Aliases** | retracts, invalidates |
| **Definition** | Subject is a Correction Record or Decision Record that withdraws
Object from canonical use. Inverse of WITHDRAWN_BY (PRD-000000033). |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Correction Record, Documentary Decision Record, or Withdrawal
Record |
| **Object Classes** | Any entity |
| **Evidence Type** | REPOSITORY |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Non-transitive |
| **Inverse Predicate** | PRD-000000033 (withdrawn_by) |
| **Inferability** | NO |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as WITHDRAWN_BY |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | DECISION_RECORD --withdraws--> SOURCE (inverse perspective).
CORRECTION
RECORD --withdraws--> ERRONEOUS
_
_CLAIM (correction withdraws
bad claim). |
| **Related Predicates** | PRD-000000033 (withdrawn_by) |
---
#### PRD-000000035: CONTAINS
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000035 |
| **Preferred Label** | contains |
| **Aliases** | comprises, includes, is composed of |
| **Definition** | Subject is a composite entity containing Object as a component or
constituent part. Containment must be observable in the structure of Subject.
Component must be retrievable. |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Citation Object, Hermeneutic Object, Repository Synthesis,
Work, Register, Ledger, Catalog, Witness Collection, Evidence Chain |
| **Object Classes** | Hermeneutic Object, Comparative Reconstruction, Inquiry
Architecture Record, Evidence Record, Ledger entry, Work Component, Witness
Component, Claim |
| **Evidence Type** | STRUCTURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Transitive (A contains B and B contains C logically implies A contains
C) |
| **Inverse Predicate** | PRD-000000036 (contained_by) |
| **Inferability** | CONDITIONAL (Structural; may be inferred from component
identifiers, but explicit assertion preferred) |
| **Lifecycle Notes** | Preserved. Components retain identities even if parent revised. |
| **Validation Notes** | Component must be independently identified and addressable.
Container must be structurally composed of component. |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | CITATION_
OBJECT --contains--> HERMENEUTIC
_OBJECT-1,
HERMENEUTIC
_OBJECT-2, HERMENEUTIC_OBJECT-3 (multiple objects). WORK --
contains--> SECTION-1, SECTION-2, SECTION-3 (structural parts). LEDGER --
contains--> ENTRY-1, ENTRY-2, ENTRY-3 (ledger contents). |
| **Related Predicates** | PRD-000000036 (contained_by) |
---
#### PRD-000000036: CONTAINED
BY
_
| Field | Value |
|-------|-------|
| **Predicate Identifier** | PRD-000000036 |
| **Preferred Label** | contained_by |
| **Aliases** | is a component of, is part of |
| **Definition** | Subject is a component contained within Object. Inverse of CONTAINS
(PRD-000000035). |
| **Predicate Class** | D — Identity and Composition Relationships |
| **Subject Classes** | Hermeneutic Object, Comparative Reconstruction, Inquiry
Architecture Record, Evidence Record, Ledger entry, Work Component, Witness
Component, Claim |
| **Object Classes** | Citation Object, Hermeneutic Object, Repository Synthesis, Work,
Register, Ledger, Catalog, Witness Collection, Evidence Chain |
| **Evidence Type** | STRUCTURAL |
| **Direction** | Asymmetric |
| **Reflexivity** | NO |
| **Symmetry** | Not symmetric |
| **Transitivity** | Transitive |
| **Inverse Predicate** | PRD-000000035 (contains) |
| **Inferability** | CONDITIONAL |
| **Lifecycle Notes** | Preserved. |
| **Validation Notes** | Same as CONTAINS |
| **Version History** | v1.0: Initial definition (2026-01-15). No revisions. |
| **Deprecation Status** | Active |
| **Date Defined** | 2026-01-15 |
| **Examples** | HERMENEUTIC_
OBJECT-1 --contained
_by--> CITATION_
OBJECT
(inverse perspective). SECTION-1 --contained_by--> WORK (structural component). |
| **Related Predicates** | PRD-000000035 (contains) |
---
### APPENDIX A.5: CLASS E — INQUIRY AND INTERPRETIVE RELATIONSHIPS
[CLASS E predicates PRD-000000037 through PRD-000000046 (RAISES, RAISED_BY,
ANSWERS, ANSWERED_BY, INVESTIGATES, INVESTIGATED_BY, APPLIES_TO,
APPLICABLE
_TO, CONCERNS, CONCERNED_BY) follow the same comprehensive
register structure with abstract structural examples replacing concrete instances.]
**Structure consistent with Appendix A.1–A.4 entries. Abstract examples:**
- WORK --raises--> QUESTION (intellectual work foregrounds question)
- CLAIM --answers--> QUESTION (proposition addresses inquiry)
- ANALYSIS --investigates--> AUTHOR (study examines figure)
- METHOD --applies_to--> INTERPRETATION (approach illuminates reading)
- WORK --concerns--> THEME (text addresses conceptual domain)
---
### APPENDIX A.6: CLASS F — COMPARATIVE AND STRUCTURAL RELATIONSHIPS
[CLASS F predicates PRD-000000047 through PRD-000000051 (PARALLELS,
CONTRASTS
_WITH, COMPLEMENTS, EXEMPLIFIES, EXEMPLIFIED_BY) follow the same
structure with abstract examples.]
**Abstract examples:**
- PASSAGE-A --parallels--> PASSAGE-B (structural similarity)
- INTERPRETATION-1 --contrasts
_with--> INTERPRETATION-2 (opposed positions)
- ANALYSIS-1 --complements--> ANALYSIS-2 (joint comprehensiveness)
- INSTANCE --exemplifies--> PRINCIPLE (particular illustrates general)
---
### APPENDIX A.7: CLASS G — AUTHORITY AND VALIDATION RELATIONSHIPS
[CLASS G predicates PRD-000000052 through PRD-000000061 (CERTIFIES,
CERTIFIED
_BY, VALIDATES, VALIDATED_BY, AUTHORED_BY, AUTHOR_OF,
TRANSLATED
_BY, TRANSLATOR_OF, EDITED_BY, EDITOR_OF) follow the same
structure.]
**Abstract examples:**
- CERTIFICATION
_RECORD --certifies--> ARTIFACT (verification attests)
- VALIDATION
_RECORD --validates--> ENTITY (checking confirms)
- WORK --authored
_by--> PERSON (attribution to creator)
- TRANSLATION --translated
_by--> AGENT (translation ascribed to translator)
- EDITION --edited
_by--> EDITOR (editorial constitution)
---
### APPENDIX A.8: CLASS H — PROVENANCE AND INSTITUTIONAL RELATIONSHIPS
[CLASS H predicates PRD-000000062 through PRD-000000066 (HELD_BY, HOLDS,
PUBLISHED
_BY, PUBLISHES, CREATED_AT) follow the same structure.]
**Abstract examples:**
- MANUSCRIPT --held
_by--> INSTITUTION (institutional custody)
- WORK --published_by--> PUBLISHER (publication attribution)
- ARTIFACT --created
_at--> LOCATION (creation locality)
---
### APPENDIX A.9: CLASS J — TEMPORAL RELATIONSHIPS
**RESERVED for future specification.**
Temporal predicates (before, after, contemporary_with, precedes, follows,
active
_during) are anticipated but not defined in Relationship Specification v1.0.
Predicate IDs PRD-000000067 through PRD-000000072 are reserved pending
alignment with Temporal Logic, Versioning, and Time-Aware Query specifications.
---
### APPENDIX A.10: COMPLETE PREDICATE COUNT
| Class | Predicate Count | PRD Range | Status |
|-------|-----------------|-----------|--------|
| A — Documentary Operations | 12 | PRD-000000001 to PRD-000000012 | Active |
| B — Evidentiary Relationships | 7 | PRD-000000013 to PRD-000000019 | Active |
| C — Derivation & Transformation | 8 | PRD-000000020 to PRD-000000027 | Active |
| D — Identity & Composition | 9 | PRD-000000028 to PRD-000000036 | Active |
| E — Inquiry & Interpretive | 10 | PRD-000000037 to PRD-000000046 | Active |
| F — Comparative & Structural | 5 | PRD-000000047 to PRD-000000051 | Active |
| G — Authority & Validation | 10 | PRD-000000052 to PRD-000000061 | Active |
| H — Provenance & Institutional | 5 | PRD-000000062 to PRD-000000066 | Active |
| J — Temporal (Reserved) | 6 | PRD-000000067 to PRD-000000072 | Reserved |
| **TOTAL** | **62 + 6 Reserved** | **PRD-000000001 to PRD-000000072** | **62
Active, 6 Reserved** |
---
### APPENDIX A.11: PREDICATE GOVERNANCE LEDGER
The following permanent record documents predicate governance decisions:
| Date | PRD-ID Range | Action | Authority | Reason | Notes |
|------|--------------|--------|-----------|--------|-------|
| 2026-01-15 | PRD-000000001 to PRD-000000066 | Created | Relationship
Specification v1.0 | Initial canonical predicate set | 62 active, 6 reserved for temporal |
| — | — | — | — | — | — |
(Future updates recorded here as predicates are revised, deprecated, or added.)
---
END OF APPENDIX A
END OF DOCUMENT
Document: Relationship Specification
Version: 1.0 Final Editorial Revision
Document Number: 000003
Classification: Foundational Repository Specification
Status: Ready for Certification and GitHub Archival
