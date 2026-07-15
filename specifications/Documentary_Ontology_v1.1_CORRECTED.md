STRAUSSIAN DOCUMENTARY MEMORY
DOCUMENTARY ONTOLOGY
Version 1.1
Document Number: 000001
Classification: Foundational Repository Specification
Status: Corrected Final Draft for Constitutional Re-Audit
Authority: Defines the canonical classes of entities recognized by the Straussian Documentary Memory

REVISION NOTICE

This corrected draft restores the full constitutional ontology and incorporates only the approved audit amendments. It preserves the distinction between source entities and Repository-created artifacts, restores previously recognized entity classes, preserves first-class component and passage identity, defines governance jurisdiction, and expands Correction Record semantics without importing implementation syntax.

No prior version is silently overwritten. Earlier repository versions remain historical records.

PURPOSE

The Documentary Ontology answers one question:

What exists in the Straussian Documentary Memory?

It defines the conceptual universe from which identifiers, relationship assertions, controlled vocabularies, registers, Citation Objects, validation records, graph projections, retrieval interfaces, and future AI access are derived.

It does not define identifier syntax, predicate inventories, URI schemes, file formats, folder structures, database labels, or software implementations.

I. CONSTITUTIONAL PRINCIPLES

1. Documentary fidelity precedes technical convenience.
2. Source entities and Repository-created artifacts are both first-class entities but remain ontologically distinct.
3. A Repository artifact never becomes primary documentary evidence merely because it is preserved.
4. Evidence, inference, interpretation, and hypothesis remain categorically distinct.
5. Identity is stable; versions and revisions record states of an entity.
6. Completed artifacts are never silently revised.
7. The full documentary artifact remains authoritative over every graph, index, database, or API projection.
8. Ontology governs implementations. Implementations do not govern ontology.
9. Roles do not create new identities where a role is sufficient.
10. New entity classes require formal ontology amendment.

II. ROOT CLASS

REPOSITORY ENTITY

Repository Entity is the universal root class. Every item represented in the Straussian Documentary Memory belongs to one most-specific canonical class and may inherit membership in parent classes.

III. SOURCE–ARTIFACT BOUNDARY

A. SOURCE ENTITY

A source entity originates in the documentary tradition under investigation. Source entities include Agents, Works, Expressions, Witnesses, Locations, Passages, Textual Variants, Citations, Quotations, and other recoverable documentary operations or structures.

B. REPOSITORY ARTIFACT

A Repository Artifact is produced by the Straussian Documentary Memory during inquiry, preservation, comparison, interpretation, governance, validation, certification, correction, administration, or technical formalization.

A Citation Object, Hermeneutic Object, Evidence Record, Register, Ledger, Catalog, or graph projection is not a primary source.

C. EVIDENTIARY STANDING

A source entity may bear the role of evidence.
A Repository Artifact may document evidence, reasoning, provenance, or governance.
A Repository Artifact does not acquire the evidentiary standing of the source entity it describes.

IV. CANONICAL ENTITY CLASSES

A. AGENTS

1. AGENT
An entity capable of documentary, intellectual, editorial, institutional, technical, or governance action.

2. PERSON
A natural person participating in the documentary tradition or Repository process.

3. COLLECTIVE AGENT
An organization, institution, publisher, archive, library, editorial body, project, or other organized body capable of action.

B. INTELLECTUAL ENTITIES

4. WORK
A distinct intellectual creation independent of any particular language, edition, transcription, or embodiment.

5. WORK COMPONENT
A bounded structural part of a Work or Expression, including a book, chapter, section, note, letter, lecture, paragraph, or appendix.

A Work Component is a first-class entity when independently addressable, cited, compared, or related. It receives its own stable identifier and retains a parent relationship to its Work or Expression.

6. EXPRESSION
A particular textual, linguistic, editorial, or transcriptive realization of a Work.

7. TRANSLATION
An Expression rendering a Work or another Expression into another language.

8. EDITION OR RECENSION
An Expression defined by a particular editorial, critical, or textual constitution.

9. TRANSCRIPTION
An Expression created by transcribing a Witness, including diplomatic, normalized, OCR, corrected OCR, or verified plain-text transcription.

C. DOCUMENTARY WITNESSES

10. WITNESS
A specific recoverable documentary embodiment consulted, preserved, cited, compared, or reconstructed.

11. SOURCE WITNESS
A Witness serving as the source of a documented derivation chain. Source Witness is provenance-relative.

12. DERIVED WITNESS
A Witness produced through reproduction, digitization, extraction, conversion, transcription, or another documented transformation.

13. WITNESS COMPONENT
A physically or digitally bounded component of a Witness, including a volume, page, folio, image, file segment, audio track, or transcript segment.

A Witness Component is a first-class entity when independently addressable, cited, compared, validated, or related. It receives its own stable identifier and retains a parent relationship to its Witness.

14. WITNESS COLLECTION
A governed grouping of Witnesses assembled for recovery, comparison, validation, or inquiry.

15. TEXTUAL VARIANT
A distinguishable reading or documentary state associated with one or more Locations in one or more Witnesses.

D. DOCUMENTARY ADDRESS AND SEGMENT ENTITIES

16. LOCATION
A recoverable address within a Witness or Witness Component.

17. PASSAGE
A bounded segment of documentary content recovered from one or more Locations.

Passage identity is determined by documentary scope and bounded content, not by interpretation. A new interpretation, Claim, or Hermeneutic Object concerning unchanged text does not create a new Passage identifier.

18. CONTEXT
A bounded documentary segment selected because it is necessary to understand another entity. Context must identify its focal entity, Witness, Location or Locations, and reason for inclusion.

E. DOCUMENTARY OPERATIONS AND APPARATUS

19. DOCUMENTARY OPERATION
A bounded act or event involving documentary entities.

20. CITATION
A Documentary Operation by which one documentary entity refers to another.

21. QUOTATION
A Documentary Operation in which wording from a source is reproduced within another documentary entity.

22. SELECTION
A Documentary Operation in which material is chosen for inclusion, citation, quotation, transcription, arrangement, or analysis.

23. OMISSION
A Documentary Operation in which demonstrably available or structurally expected material is absent from a later use, reproduction, or reconstruction.

24. PLACEMENT
A Documentary Operation concerning the documented position of an entity within a Work, Expression, or Witness.

25. SEQUENCE
A Documentary Operation concerning the documented ordering of passages, citations, quotations, variants, arguments, or inquiry stages.

F. INQUIRY ENTITIES

26. INQUIRY
A bounded, ordered process of documentary investigation.

27. QUESTION
A proposition posed for investigation rather than asserted as settled.

28. CLAIM
An atomic proposition recorded by the Repository.

29. OBSERVATION
A Claim restricted to something directly observable in the documentary record.

30. INTERPRETATION
A Claim or organized set of Claims concerning meaning, structure, teaching, function, documentary use, or inquiry.

31. STRUCTURAL PATTERN
An Interpretation identifying a recurrent arrangement or architecture across multiple documentary entities or operations.

32. HYPOTHESIS
A provisional Claim preserved for testing.

33. COMPARISON
An Inquiry Entity representing structured juxtaposition after independent reconstruction.

34. TASK
A defined future action required for recovery, verification, reconstruction, correction, expansion, or implementation.

G. EVIDENTIARY ENTITIES

35. EVIDENCE RECORD
An atomic Repository Artifact documenting how one evidence-bearing entity bears relevance to one Claim, Question, Comparison, Interpretation, Validation, or Certification.

36. EVIDENCE CHAIN
A composite Repository Artifact ordering multiple Evidence Records and preserving the path from documentary evidence to a Claim or conclusion.

H. INTERPRETIVE AND RECONSTRUCTION ARTIFACTS

37. HERMENEUTIC OBJECT
A governed Repository Artifact preserving a bounded interpretive analysis with explicit evidence, Claims, Questions, and provenance.

38. HERMENEUTIC OBJECT A
A Hermeneutic Object centered on a primary source passage or documentary object.

39. HERMENEUTIC OBJECT B
A Hermeneutic Object centered on a second author, comparison source, or intertextual object.

40. HERMENEUTIC OBJECT C
A Hermeneutic Object centered on Leo Strauss’s interpretive treatment.

41. COMPARATIVE RECONSTRUCTION
A Repository Artifact preserving the result of a documented Comparison.

42. INQUIRY ARCHITECTURE RECORD
A Repository Artifact preserving the ordered structure, stages, dependencies, and unresolved branches of an Inquiry.

43. REPOSITORY SYNTHESIS
A Repository Artifact combining multiple documented analyses while preserving their provenance and distinctions.

44. CITATION OBJECT
A governed composite Repository Artifact preserving a citation-centered inquiry package, including relevant Hermeneutic Objects, evidence, provenance, and certification state.

I. GOVERNANCE AND DOCUMENTARY DECISION ARTIFACTS

45. DOCUMENTARY DECISION RECORD
A Repository Artifact recording a formal decision concerning identity, inclusion, exclusion, merger, split, withdrawal, classification, or governance.

46. DERIVATION RECORD
A Repository Artifact documenting a transformation or derivation from one entity to another.

47. CORRECTION RECORD
A Repository Artifact documenting a correction to one or more canonical entities while preserving original state, corrected state, reason, authority, supporting evidence, effective date, and version relations.

48. CERTIFICATION RECORD
A Repository Artifact formally attesting that specified requirements have been satisfied.

49. VALIDATION RECORD
A Repository Artifact documenting the result of a defined validation procedure without itself conferring constitutional certification.

50. PROVENANCE RECORD
A Repository Artifact documenting origin, custody, derivation, responsibility, and transformation history.

51. FIXITY RECORD
A Repository Artifact documenting checksums or other fixity evidence for an artifact or Witness.

52. VERSION RECORD
A Repository Artifact documenting a state of an entity at a particular stage.

53. REVISION RECORD
A Repository Artifact documenting a governed change between versions.

J. REGISTERS, LEDGERS, CATALOGS, AND MANIFESTS

54. REGISTER
A governed authoritative collection of recognized records or entities.

55. LEDGER
An ordered, append-oriented record of assignments, events, decisions, or transactions.

56. CATALOG
A discovery-oriented descriptive collection that supports finding and retrieval.

57. MANIFEST
A structured declaration of the contents, composition, dependencies, and fixity of an artifact or package.

These classes shall not be collapsed. A Register governs recognition; a Ledger preserves ordered events; a Catalog supports discovery; a Manifest describes composition.

58. AUTHORITY REGISTER
A Register governing authorized entities, identifier assignments, or recognized authorities as defined by later specifications.

59. CANONICAL PREDICATE REGISTER
A Register containing approved predicate definitions.

60. CANONICAL VOCABULARY REGISTER
A Register containing approved controlled concepts.

K. CONSTITUTIONAL AND TECHNICAL FORMALIZATION ENTITIES

61. FOUNDATIONAL DOCUMENT
A constitutional artifact stating mission, enduring principles, or governing commitments.

62. SAFEGUARD
A constitutional rule preventing drift, erasure, conflation, or unauthorized alteration.

63. AMENDMENT
A versioned constitutional change preserving the prior rule and its history.

64. SPECIFICATION
A normative technical or constitutional document defining a governed domain.

65. SCHEMA
A formal structure used to validate or represent entities under a Specification.

L. RELATIONAL AND CONTROLLED-CONCEPT ENTITIES

66. RELATIONSHIP ASSERTION
A reified, identity-bearing assertion connecting a Subject and Object through a canonical Predicate.

67. PREDICATE
A governed semantic relation type used by Relationship Assertions.

68. THEME
A controlled concept representing a conceptual domain or inquiry topic.

69. EPISTEMIC CLASSIFICATION
A controlled concept recording the evidentiary or epistemic standing of a Claim, Interpretation, or Relationship Assertion.

70. STATUS
A controlled concept recording lifecycle, review, revision, or allocation state.

71. ROLE
A controlled concept describing how an entity functions within a relationship or inquiry.

72. LANGUAGE
A controlled concept representing a natural language.

73. OPERATION MODE
A controlled concept distinguishing recovered, responsibly reconstructed, and hypothetical Documentary Operations.

74. HERMENEUTIC COMPLETENESS
A controlled concept recording the sufficiency or completion state of an interpretive artifact.

75. QUESTION STATUS
A controlled concept recording the lifecycle or resolution state of a Question.

76. VOCABULARY CONCEPT
A meta-level controlled concept governing vocabulary organization.

V. CORRECTION RECORD SEMANTICS

1. A Correction Record may affect one entity or an explicitly enumerated set of entities.
2. Ordinary correction preserves the corrected entity’s identifier.
3. The original state and every prior version remain preserved.
4. A Version Record and, where appropriate, a Revision Record document the corrected state.
5. A Correction Record may itself be corrected by another Correction Record.
6. A correction that reveals distinct identity, merger, split, fraud, or invalidity invokes the corresponding identity or lifecycle procedure rather than silently altering identity.
7. Correction types may be governed by controlled vocabulary or operational policy; the Ontology does not impose a closed taxonomy.

VI. GOVERNANCE JURISDICTION

1. Ontology Governance determines what entity classes exist and their essential boundaries.
2. Identifier Governance determines identifier families and allocation rules.
3. Predicate Governance determines canonical predicates and subject/object constraints.
4. Vocabulary Governance determines controlled concepts within approved identifier families.
5. Each authority is limited to its own domain.
6. A lower specification may not override a higher dependency.
7. Questions outside an authority’s jurisdiction are referred to the appropriate governing specification.

Dependency order:

Documentary Ontology
→ Identifier Specification
→ Relationship Specification
→ Controlled Vocabulary Specification
→ Registers and operational artifacts
→ Implementations

VII. FINAL DECLARATION

This Ontology preserves the full documentary architecture required to reconstruct inquiry without conflating source with artifact, evidence with inference, identity with version, or ontology with implementation.

END OF DOCUMENT
