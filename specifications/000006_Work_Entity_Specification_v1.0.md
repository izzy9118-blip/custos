STRAUSSIAN DOCUMENTARY MEMORY
WORK ENTITY SPECIFICATION

Version: 1.0
Document Number: 000006
Classification: Entity-Family Specification
Status: Certified
Authority: Defines recognition, identity, minimum record, validation, and lifecycle requirements for Work entities

PURPOSE

The Straussian Documentary Memory exists to preserve the documentary conditions under which disciplined inquiry into Leo Strauss and the sources he investigates can accumulate without losing its object.

The Work entity provides the stable documentary identity toward which successive inquiries converge.

This Specification answers:

What must the Repository preserve when it recognizes a distinct intellectual creation as a Work?

I. CONSTITUTIONAL BASIS

1. This Specification is subordinate to:
   - Documentary Ontology v1.1;
   - Identifier Specification v1.0;
   - Relationship Specification v1.0;
   - Controlled Vocabulary Specification v1.0;
   - Constitutional Admission Protocol v1.0.
2. The Documentary Ontology defines a Work as a distinct intellectual creation independent of any particular language, edition, transcription, or embodiment.
3. The Identifier Specification assigns the WK family to Works and establishes that canonical identity is independent of titles, versions, storage systems, and representations.
4. This Specification does not redefine Expression, Witness, Passage, Claim, Interpretation, Hermeneutic Object, or Comparative Reconstruction.

II. DEFINITION

A Work is a distinct intellectual creation recognized as the stable documentary object toward which successive inquiries may be directed.

A Work is not:
- a particular edition;
- a translation;
- a transcription;
- a manuscript;
- a printed volume;
- a digital file;
- an OCR product;
- a Passage;
- an interpretation of the text.

III. CONSTITUTIONAL FUNCTION

The Work has one primary constitutional function:

To preserve the identity of the intellectual creation toward which documentary inquiry converges.

The Work permits different readers, investigations, Citation Objects, Hermeneutic Objects, Comparative Reconstructions, and future AI systems to return to the same documentary object without confusing that object with a particular realization, embodiment, segment, or interpretation.

The Work does not determine:
- the author's teaching;
- the governing question of the text;
- the correct interpretation;
- Strauss's use of the Work;
- the relationship between the Work and other Works.

Those matters belong to inquiry and must be represented through the appropriate documentary, analytical, relational, and interpretive entities.

IV. CONDITIONS OF RECOGNITION

A candidate may be recognized as a Work only when all applicable conditions are satisfied.

1. Distinct Intellectual Creation
   The candidate represents an intellectual creation distinguishable from other recognized Works.

2. Documentary Basis
   Recognition rests on recoverable documentary evidence, documentary references, a recoverable textual tradition, an existing Expression, one or more Witnesses, or a documented Repository investigation.

3. Stability Sufficient for Inquiry
   The candidate possesses sufficient continuity for successive investigations to concern the same intellectual creation despite differences among Expressions, Witnesses, titles, or interpretations.

4. Duplicate Review
   The Repository confirms that the candidate has not already been admitted under another WK identifier.

5. Ontological Separation
   The candidate is distinguished from its Expressions, Witnesses, Work Components, Passages, and interpretations.

6. Preserved Uncertainty
   Where evidence does not establish whether one or several Works exist, uncertainty is preserved rather than resolved for administrative convenience.

V. WORK IDENTITY

1. Every admitted Work receives exactly one permanent canonical WK identifier.
2. The identifier is nonsemantic and shall not encode title, author, language, date, genre, theme, or interpretation.
3. Translation, edition, recension, transcription, OCR correction, normalization, pagination change, physical embodiment, and digital reproduction do not by themselves create a new Work.
4. A new Work identifier is justified only when documentary evidence establishes a distinct intellectual creation.
5. Disagreement about meaning does not create a new Work.
6. The Work identifier remains stable while documentary and interpretive understanding grows around it.

VI. DIFFERENCES DISCOVERED THROUGH TEXTUAL ANALYSIS

Textual analysis may disclose genuine differences. Each difference shall be preserved at the level where it arises.

A. Documentary Differences

1. Differences in exact wording, textual state, revision layer, cancellation, substitution, marginal addition, or alternate reading belong to Textual Variant records where constitutionally warranted.
2. A coherent editorial, linguistic, revised, or transcriptive realization may justify an Expression.
3. A specific manuscript, volume, scan, PDF, OCR file, or other recoverable embodiment is a Witness.
4. A bounded documentary segment is a Passage.
5. Textual Variants do not automatically create new Expressions.
6. Textual Variants and Expressions do not automatically create new Works.

B. Interpretive Differences

1. Differences concerning meaning, teaching, structure, intention, literary effect, or documentary operation belong to the inquiry layer.
2. They may be represented as Claims, Observations, Interpretations, Structural Patterns, Hypotheses, Hermeneutic Objects, or Comparative Reconstructions.
3. A new interpretation of unchanged documentary content does not create a new Passage or Work.

C. Governing Rule

Documentary difference shall be recorded without converting interpretive difference into documentary identity.

VII. REQUIRED WORK RECORD

Every admitted Work record shall contain:
- id;
- class;
- canonical_label;
- recognition_basis;
- lifecycle_status;
- responsible_authority_id;
- version_history;
- governing_specification_references.

The canonical class value shall be Work.

VIII. OPTIONAL WORK FIELDS

The following may be recorded when supported and useful:
- alternate_labels;
- identity_note;
- uncertainty_note;
- legacy_references;
- recognition_date;
- governing_record_ids;
- deprecation information.

Optional fields do not define Work identity.

IX. CANONICAL LABEL

1. canonical_label is required for retrieval, navigation, audit, and intelligibility.
2. canonical_label is not the source of Work identity.
3. The label may change through documented revision without changing the WK identifier.
4. The label does not claim to be the original title, the preferred scholarly title, the title of every Expression, or an immutable property of the Work.
5. Titles appearing in particular documentary realizations belong to the corresponding Expression or Witness records.

X. AUTHORSHIP

1. A primary creator is not required for Work recognition.
2. A Work may be anonymous, collective, pseudonymous, traditionally attributed, disputed, or of unknown authorship.
3. Authorship shall ordinarily be represented through explicit governed Relationship Assertions supported by evidence.
4. Absence of settled authorship does not prevent Work admission.
5. A change in attribution does not ordinarily change Work identity.

XI. WORK TYPE

1. work_type is not a required Work field.
2. Classification as poem, dialogue, treatise, history, letter, lecture, or another literary form does not establish Work identity.
3. Such classifications may later support retrieval or comparison through governed vocabulary or relationships.
4. No Work shall be denied recognition because it does not fit a settled genre.

XII. LANGUAGE

1. Language is not required for Work recognition.
2. Language may be recorded where useful and supported.
3. A translation changes the Expression, not the Work.
4. Uncertainty concerning original language shall be preserved.

XIII. WORK COMPONENTS

1. A bounded structural part of a Work may receive a WC identifier when it must be independently cited, compared, related, validated, versioned, retrieved, or preserved.
2. Parentage shall be represented through governed Relationship Assertions, not encoded into canonical identity.
3. A chapter, book, section, note, letter, or appendix does not automatically receive a WC identifier merely because it can be named.
4. Independent addressability must serve documentary fidelity or inquiry.

XIV. RELATIONSHIPS

1. Relationships concerning a Work shall be represented outside Work identity through canonical Relationship Assertions.
2. These may document authorship, realization, containment, citation, quotation, reference, interpretation, comparison, support, contradiction, correction, merger, split, or supersession.
3. Each Relationship Assertion must use a registered predicate and preserve evidence, provenance, responsibility, and lifecycle as constitutionally required.
4. A relationship does not alter Work identity merely because the relationship changes.

XV. PROHIBITED DETERMINANTS OF WORK IDENTITY

The following shall not determine Work identity:
- preferred title;
- uniform title;
- primary creator;
- work type;
- publisher;
- publication place;
- ISBN;
- edition statement;
- pagination;
- binding;
- manuscript shelfmark;
- file name;
- file format;
- storage path;
- checksum;
- OCR quality;
- graph node identifier;
- database key;
- theme;
- governing question;
- doctrinal summary;
- interpretive conclusion.

These may be valid elsewhere in the Repository. They are prohibited only as determinants of Work identity.

XVI. LIFECYCLE AND CORRECTION

1. A WK identifier never changes, expires, transfers, or is reused.
2. Labels, notes, evidence references, and descriptive metadata may be corrected through explicit versioned revision.
3. Where two WK identifiers are discovered to identify the same Work, neither is deleted; historical references remain intact and current resolution is governed by explicit documentary decision and lifecycle records.
4. Where one WK record is discovered to conflate distinct Works, the original record remains preserved, new identifiers are assigned where required, and relationships are reviewed rather than automatically propagated.
5. New Claims, Interpretations, Hermeneutic Objects, or Comparative Reconstructions do not alter Work lifecycle merely because understanding advances.

XVII. VALIDATION

A Work record is constitutionally valid only when:
1. id conforms to the authorized WK syntax;
2. the identifier is assigned in the Identifier Assignment Ledger;
3. the identifier is unique and assigned to no other entity;
4. class equals Work;
5. the candidate satisfies the distinct-intellectual-creation test;
6. at least one recoverable recognition basis is supplied;
7. duplicate review is complete;
8. Expression, Witness, Passage, and interpretive data are not collapsed into Work identity;
9. canonical_label is present and is not treated as canonical identity;
10. exactly one current lifecycle status is recorded;
11. a responsible authority is identified;
12. version history is present and append-only;
13. unresolved identity uncertainty is explicitly preserved;
14. governed relationships are represented as Relationship Assertions rather than implied by identity metadata.

Failure of any required rule returns the candidate for correction.

XVIII. WORK REGISTER

1. The Work Register is the canonical collection of admitted Work records.
2. It shall preserve every admitted WK identity, current lifecycle status, prior record versions, legacy references, and governing admission or correction records.
3. Register entries and counts shall remain consistent.
4. The Work Register shall never silently reinterpret a Work.
5. Substantive interpretations belong outside the Work Register.

XIX. IMPLEMENTATION INDEPENDENCE

A Work may be represented in GitHub, Neo4j, an MCP resource, an API response, a search index, RDF, JSON-LD, or a local database.

These are representations of one Work record, not additional Work identities.

No implementation may alter constitutional identity or silently add interpretive content to the Work record.

XX. FINAL DECLARATION

The Work is the stable documentary object around which inquiry accumulates.

The Work does not contain the inquiry.

Differences in wording are preserved as documentary differences.
Differences in understanding are preserved as inquiry and interpretation.
Neither kind of difference shall silently rewrite Work identity.

The Work remains stable so that disciplined inquiry may deepen without losing its object.

END OF DOCUMENT
