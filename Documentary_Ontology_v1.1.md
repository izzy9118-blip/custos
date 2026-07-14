STRAUSSIAN DOCUMENTARY MEMORY
DOCUMENTARY ONTOLOGY
Version 1.1
Document Number: 000001
Classification: Foundational Repository Specification
Status: Revised Consolidated Release
Authority: Defines the canonical classes of entities recognized by the Straussian
Documentary Memory
REVISION NOTICE
Version 1.1 supersedes Version 1.0 without altering or invalidating the preserved Version
1.0 artifact.
This revision incorporates the first adversarial architectural review. It:
- distinguishes source and derived Witnesses while preserving Transcription as an
Expression;
- adds Textual Variant as an addressable documentary entity;
- distinguishes source apparatus from Repository-created intertextual apparatus
records;
- clarifies Comparison and Comparative Reconstruction;
- defines Evidence Record as atomic and Evidence Chain as composite;
- separates Validation from Certification;
- separates constitutional authority from technical formalization;
- narrows Reasoning Record into Documentary Decision Record;
- reclassifies Capacity as Capacity Record;
- adds Witness Collection and Relationship Assertion;
- introduces controlled concepts for Operation Mode, Hermeneutic Completeness, and
Question Status;
- preserves unresolved matters as statuses rather than unnecessary duplicate classes.
No prior certified artifact is silently revised.
PURPOSE
The Documentary Ontology defines what kinds of things may exist within the Straussian
Documentary Memory.
It establishes the conceptual universe from which all later repository structures shall be
derived, including:
- identifiers;
- registers;
- Citation Objects;
- manifests and ledgers;
- validation schemas;
- graph nodes and relationships;
- repository catalogs;
- retrieval interfaces;
- future AI access.
This document does not define identifiers, relationship predicates, file formats, folder
structures, database labels, or software implementations. Those shall be governed by
later specifications.
The ontology answers one question:
What exists in the Straussian Documentary Memory?
CONSTITUTIONAL BASIS
This ontology derives from the established architecture of the Straussian Reader and
Repository:
- The Reader reconstructs inquiry.
- The Repository preserves documentary memory.
- The Secretary preserves the path of inquiry without adding interpretation.
- Documentary evidence precedes interpretation.
- Primary sources take priority over secondary sources.
- Every author is reconstructed independently before comparison.
- Uncertainty is preserved where evidence is incomplete.
- Completed artifacts are never silently revised.
- The full documentary artifact remains authoritative over any database or graph
projection.
The ontology therefore serves documentary fidelity rather than technical convenience.
I. FOUNDATIONAL DISTINCTIONS
1. ENTITY AND ROLE
An entity is something recognized as possessing a stable documentary identity.
A role describes how an entity functions within a particular inquiry or relationship.
Roles do not create new identities.
Examples:
- A Person may bear the roles of author, editor, translator, investigator, secretary, or
certifier.
- A Work may bear the role of primary source in one inquiry and comparative source in
another.
- A Passage may bear the role of evidence for one Claim and context for another.
- A Witness may bear the role of cited witness, citing witness, authoritative witness, or
control witness.
The ontology shall not create separate entity classes where a role is sufficient.
2. IDENTITY AND VERSION
An entity retains one identity through time.
A version records a state of that entity or artifact at a particular stage.
A revision does not create a new identity unless the documentary object itself has
become a distinct entity.
Version numbers, dates, titles, storage locations, and file names are not identities.
3. WORK, EXPRESSION, AND WITNESS
A Work is an intellectual creation.
An Expression is a particular textual or linguistic realization of a Work.
A Witness is a specific recoverable documentary embodiment of a Work or Expression.
These classes shall never be collapsed.
Example:
- The Aeneid is a Work.
- A particular translation of the Aeneid is an Expression.
- A particular printed volume, scan, PDF, OCR transcript, or plain-text file is a Witness.
4. SOURCE AND REPOSITORY ARTIFACT
A source entity originates in the documentary tradition under investigation.
A Repository Artifact is produced by the Straussian Documentary Memory during
inquiry, preservation, certification, or administration.
A Citation Object is not a primary source.
A graph record is not a source.
A Repository interpretation is not documentary evidence merely because it has been
preserved.
5. EVIDENCE AND INFERENCE
Evidence is a role borne by a recoverable documentary entity in support of a Claim.
Evidence is not identical to the Claim it supports.
An Evidence Record is a Repository Artifact that documents the connection between
evidence-bearing entities and Claims.
Documented Findings, Supported Inferences, Working Hypotheses, and Unresolved
Questions shall remain categorically distinct.
Numerical confidence scores shall not replace epistemic classification.
6. ONTOLOGY AND IMPLEMENTATION
The ontology governs implementations.
Implementations do not govern the ontology.
GitHub files, Neo4j nodes, database rows, API objects, MCP resources, and search
indexes are representations of ontological entities. They are not additional entity
classes merely because a technology uses them.
7. RECOVERED AND RECONSTRUCTED OPERATIONS
A recovered operation is directly attested by documentary evidence.
A responsibly reconstructed operation is inferred from controlled documentary
comparison.
A hypothetical reconstruction is a provisional possibility preserved for testing.
These modes are epistemically distinct and shall be recorded through the controlled
concept Operation Mode.
No reconstructed operation shall be described as recovered.
8. EPISODIC OPERATION AND STRUCTURAL PATTERN
An episodic Documentary Operation is a bounded act or event involving identifiable
documentary entities.
A structural pattern is an Interpretation derived from multiple operations, passages, or
witnesses.
A structural pattern is not itself a Documentary Operation.
It must be recorded as an Interpretation or Claim and supported by multiple Evidence
Records where appropriate.
9. CONSTITUTIONAL AUTHORITY AND TECHNICAL FORMALIZATION
Constitutional entities govern mission, safeguards, and enduring documentary
principles.
Technical formalization entities implement those principles through specifications,
schemas, and controlled vocabularies.
Technical formalization may evolve within constitutional limits.
It may never override a Safeguard or Foundational Document.
II. ROOT CLASS
REPOSITORY ENTITY
Repository Entity is the universal root class.
Every item represented in the Straussian Documentary Memory shall belong to one
most-specific canonical class.
Membership in parent classes follows through inheritance.
An entity may bear multiple roles and classifications while retaining one primary
identity.
III. CANONICAL ENTITY CLASSES
A. AGENTS
1. AGENT
An entity capable of authorship, editorial action, translation, publication, preservation,
investigation, certification, or institutional action.
2. PERSON
A natural person participating in the documentary tradition or Repository process.
Examples include authors, translators, editors, commentators, investigators,
secretaries, and certifiers.
3. COLLECTIVE AGENT
An organization, institution, editorial body, publisher, archive, library, project, or other
organized body capable of documentary action.
Agent roles shall be recorded separately from Agent identity.
B. INTELLECTUAL ENTITIES
4. WORK
A distinct intellectual creation independent of any particular language, edition,
transcription, or physical embodiment.
Examples:
- The Aeneid
- The Prince
- Thoughts on Machiavelli
5. WORK COMPONENT
A bounded structural part of a Work or Expression.
Examples:
- book;
- chapter;
- section;
- note;
- letter;
- lecture;
- paragraph;
- appendix.
A Work Component possesses documentary boundaries but does not replace the
identity of the Work to which it belongs.
6. EXPRESSION
A particular textual, linguistic, editorial, or transcriptive realization of a Work.
Expressions preserve intellectual content while recording a distinguishable textual
state.
7. TRANSLATION
An Expression that renders a Work or another Expression into a different language.
A Translation is not a Witness. It may be embodied by one or more Witnesses.
8. EDITION OR RECENSION
An Expression defined by a particular editorial, critical, or textual constitution.
An edition as intellectual text is an Expression.
A particular printed or digital copy of that edition is a Witness.
9. TRANSCRIPTION
An Expression created by transcribing another Witness.
Subtypes may include:
- diplomatic transcription;
- normalized transcription;
- OCR transcription;
- corrected OCR transcription;
- verified plain-text transcription.
The transcription process and its source Witness shall be preserved through
provenance.
C. DOCUMENTARY WITNESSES
10. WITNESS
A specific, recoverable documentary embodiment consulted, preserved, cited,
compared, or reconstructed by the Repository.
Witnesses may include:
- manuscripts;
- printed volumes;
- facsimiles;
- scans;
- PDFs;
- digital editions;
- webpages;
- OCR files;
- plain-text files;
- audio or video records;
- archival images.
A Witness must be independently identifiable and recoverable.
The Repository reasons from Witnesses, not from abstract Works alone.
10.1 SOURCE WITNESS
A Witness serving as the source of a documented derivation chain.
Source Witness is a provenance-relative class. It does not mean that the Witness is the
original historical manuscript, the best textual authority, or a primary source in every
inquiry.
A printed edition may be a Source Witness for a scan.
A scan may be a Source Witness for an OCR file.
10.2 DERIVED WITNESS
A Witness created through a documented reproduction, digitization, transcription,
extraction, conversion, or other transformation of another Witness.
A Derived Witness shall point through provenance to the Witness or Witnesses from
which it was created.
Examples include:
- a scan made from a printed volume;
- a PDF assembled from page images;
- an OCR file created from a scan;
- a normalized plain-text file created from OCR;
- an audio transcript created from a recording.
Derived Witness status does not by itself determine textual reliability. Reliability must
be documented through validation and provenance.
11. WITNESS COMPONENT
A physically or digitally bounded component of a Witness.
Examples include:
- volume;
- page;
- folio;
- image;
- file segment;
- audio track;
- transcript segment.
A Witness Component may embody a Work Component but shall not be confused with
it.
11.1 TEXTUAL VARIANT
A distinguishable reading or documentary state associated with one or more Locations
in one or more Witnesses.
Textual Variants may include:
- cancellations;
- corrections;
- substitutions;
- interlinear additions;
- marginal additions;
- glosses;
- alternate readings;
- layers of revision;
- conflicting transcriptions.
A Textual Variant does not automatically constitute a separate Expression.
Where a coherent revised textual realization exists, it may also justify recognition as an
Expression.
Every Textual Variant shall preserve:
- the relevant Witness or Witnesses;
- the relevant Location or Locations;
- the variant reading or state;
- the basis for distinguishing it;
- the Agent or hand, when documented;
- sequence or dating, when documented;
- uncertainty, when unresolved.
D. DOCUMENTARY ADDRESS AND SEGMENT ENTITIES
12. LOCATION
A recoverable address within a Witness.
Examples:
- page number;
- line number;
- chapter and section;
- note number;
- paragraph number;
- image number;
- timestamp;
- character offset;
- stable fragment identifier.
A Location identifies where documentary content may be recovered.
13. PASSAGE
A bounded segment of documentary content recovered from one or more Locations
within a Witness.
A Passage may serve as source text, evidence, context, quotation source, comparison
object, or the site of a Textual Variant.
14. CONTEXT
A bounded documentary segment selected because it is necessary to understand
another documentary entity.
Context is always attached to:
- a focal entity;
- a Witness;
- one or more Locations;
- a documented reason for inclusion.
Context shall not be treated as free-floating interpretation.
14.1 SOURCE APPARATUS
A recoverable apparatus present within an external Work, Expression, or Witness that
connects documentary entities.
Examples include:
- a footnote;
- endnote;
- marginal citation;
- bibliography entry;
- critical apparatus entry;
- cross-reference;
- source list;
- parallel-passage notation.
A Source Apparatus is represented through the ordinary classes Work Component,
Witness Component, Passage, Citation, Quotation, Location, and Textual Variant as
appropriate.
The ontology does not create a separate external-source class merely because these
entities function together as apparatus.
E. DOCUMENTARY OPERATIONS AND EVENTS
15. DOCUMENTARY OPERATION
A bounded act or event involving documentary entities.
Every recorded Documentary Operation shall carry an Operation Mode:
- recovered;
- responsibly reconstructed;
- hypothetical reconstruction.
A recovered operation must be directly evidenced.
A responsibly reconstructed operation must be supported by controlled comparison.
A hypothetical reconstruction remains provisional.
Structural patterns inferred from multiple operations are Interpretations, not
Documentary Operations.
16. CITATION
A Documentary Operation by which one Work, Expression, Witness, Work Component,
Witness Component, Passage, or Source Apparatus refers to another documentary
entity.
A Citation may identify a source without reproducing its words.
A Citation is not identical to a Quotation.
17. QUOTATION
A Documentary Operation in which wording from a source is reproduced within another
Work, Expression, Witness, Work Component, Witness Component, Passage, or Source
Apparatus.
A Quotation may be accompanied by a Citation, but the two remain distinct.
18. SELECTION
A Documentary Operation in which particular documentary material is chosen for
inclusion, citation, quotation, transcription, arrangement, or analysis.
19. OMISSION
A Documentary Operation in which material that is demonstrably available or
structurally expected is absent from a later use, reproduction, or reconstruction.
Omission shall be recorded only when supported by recoverable comparison.
Its Operation Mode shall state whether the omission is recovered, responsibly
reconstructed, or hypothetical.
Omission shall not be inferred from speculation about authorial psychology.
20. PLACEMENT
A Documentary Operation concerning the documented position of a Citation,
Quotation, Passage, Note, Variant, or other unit within a Work, Expression, or Witness.
21. SEQUENCE
A Documentary Operation concerning the documented ordering of passages, citations,
quotations, variants, arguments, or inquiry stages.
Selection, Omission, Placement, and Sequence support reconstruction of Inquiry
Architecture when documentary evidence permits.
F. INQUIRY ENTITIES
22. INQUIRY
A bounded, ordered process of documentary investigation.
An Inquiry may contain:
- one or more Questions;
- documentary recovery;
- independent reconstruction;
- comparison;
- interpretation;
- validation;
- certification;
- unresolved matters.
An Inquiry is distinct from the artifacts produced during it.
23. QUESTION
A proposition posed for investigation rather than asserted as settled.
Question subtypes may include:
- Documentary Question;
- Comparative Question;
- Methodological Question;
- Future Repository Question.
A Question may remain unresolved indefinitely.
Whether it is unassigned, active, deferred, unresolved after investigation, or closed
shall be recorded through Question Status rather than through duplicate ontology
classes.
24. CLAIM
An atomic proposition recorded by the Repository.
Every Claim shall possess:
- a stable identity;
- a precise formulation;
- an epistemic classification;
- documentary support or an explicit statement of its absence;
- provenance;
- a location within a Repository Artifact.
Claims shall not be merged merely because they are similar.
25. OBSERVATION
A Claim restricted to something directly observable in the documentary record.
An Observation shall not include inferred intention or speculative motive.
26. INTERPRETATION
A Claim or organized set of Claims concerning meaning, structure, teaching, function,
documentary use, or inquiry.
Interpretation must remain distinguishable from the evidence on which it depends.
26.1 STRUCTURAL PATTERN
An Interpretation identifying a recurrent arrangement, tendency, or architecture across
multiple Documentary Operations, Passages, Witnesses, or Works.
A Structural Pattern shall not be treated as a recovered operation.
It must preserve:
- the compared entities;
- the recurring feature identified;
- the Evidence Records supporting the pattern;
- exceptions and counterevidence;
- its epistemic classification.
27. HYPOTHESIS
A provisional Claim preserved for future testing.
A Hypothesis shall remain explicitly provisional and shall not be silently promoted to a
Documented Finding.
28. COMPARISON
An Inquiry Entity representing the act or process of structured juxtaposition after
independent reconstruction.
A Comparison may be proposed, active, incomplete, or completed.
The recorded artifact produced from a documented Comparison is a Comparative
Reconstruction.
Comparison is the inquiry process.
Comparative Reconstruction is the preserved Repository Artifact.
29. TASK
A defined future action required for documentary recovery, verification, reconstruction,
correction, expansion, or implementation.
30. CAPACITY â RECLASSIFIED
Capacity is no longer an Inquiry Entity.
Version 1.1 reclassifies it as Capacity Record under Repository Production Artifacts.
This retained entry preserves reference continuity with Version 1.0.
G. EVIDENTIARY ENTITIES
31. EVIDENCE RECORD
An atomic Repository Artifact documenting how one evidence-bearing documentary
entity bears relevance to one Claim, Question, Comparison, Interpretation, Validation, or
Certification.
An Evidence Record preserves:
- the evidence-bearing entity;
- its Witness and Location;
- the proposition or requirement supported;
- the type of support;
- limitations;
- counterevidence, when known;
- provenance.
The Evidence Record does not replace the underlying evidence-bearing entity.
A single Evidence Record does not by itself constitute an Evidence Chain.
32. EVIDENCE CHAIN
A composite, ordered documentary structure composed of two or more Evidence
Records.
An Evidence Chain may link:
- source entities;
- Textual Variants;
- Citations;
- Quotations;
- intermediary uses;
- Straussian uses;
- Repository reconstructions;
- Validations;
- Certification.
Every component Evidence Record retains its own identity.
The Chain preserves order and documentary transformation without collapsing its
components.
32.1 INTERTEXTUAL APPARATUS RECORD
A Repository Artifact reconstructing the exact documentary apparatus by which one
entity refers to, quotes, locates, varies, or transmits another.
It may document:
- the citing entity;
- the cited entity;
- the Source Apparatus;
- edition and Witness information;
- Locations;
- Textual Variants;
- parallel passages;
- intermediary documentary layers;
- uncertainty or unresolved attribution.
An Intertextual Apparatus Record does not replace the external Source Apparatus.
It is the Repository's reproducible reconstruction of that apparatus.
H. REPOSITORY PRODUCTION ARTIFACTS
33. DOCUMENTARY REGISTER ENTRY
A pre-production record of a documentary event.
It records documentary discovery before full reconstruction.
It may contain:
- Location;
- Agent;
- cited source;
- immediate documentary context;
- preliminary documentary function.
It shall not contain premature philosophical interpretation.
34. CITATION OBJECT
The principal aggregate artifact produced by the Repository for a bounded
documentary inquiry.
A Citation Object preserves the complete, reproducible path of reconstruction.
It may contain or reference:
- Documentary Register Entries;
- source Witnesses and Locations;
- Hermeneutic Objects;
- Comparative Reconstruction;
- Claims;
- Questions;
- Evidence Records;
- Inquiry Architecture;
- Repository Synthesis;
- Certification Record;
- Manifest;
- provenance and version history.
The full Citation Object remains authoritative over any graph projection, search index,
summary, or database record.
35. HERMENEUTIC OBJECT A
A Repository Artifact that reconstructs the cited source author, Work, Expression,
Passage, or teaching according to its own integrity before the later citing author or
Strauss enters the analysis.
36. HERMENEUTIC OBJECT B
A Repository Artifact that reconstructs an intermediary citing author or Work according
to its own integrity, including its documentary use of the source reconstructed in
Hermeneutic Object A.
Hermeneutic Object B is used where an intermediary documentary layer exists.
37. HERMENEUTIC OBJECT C
A Repository Artifact that reconstructs Strauss's use of the documentary chain,
including his interpretation, selection, quotation, omission, placement, sequencing,
pedagogy, and transformation of the inquiry where the evidence permits.
38. COMPARATIVE RECONSTRUCTION
The preserved Repository Artifact produced by a documented Comparison.
It compares independently completed Hermeneutic Objects or other documentary
reconstructions without erasing their differences or allowing a later author to redefine
an earlier one.
A Comparative Reconstruction shall identify:
- the Comparison from which it was produced;
- the entities compared;
- the independent reconstructions on which it depends;
- agreements;
- differences;
- unresolved divergences;
- evidence for each comparative finding.
39. INQUIRY ARCHITECTURE RECORD
A Repository Artifact, or a formally bounded component of Hermeneutic Object C, that
records how documentary selection, omission, placement, quotation, and sequence
transform the structure of an Inquiry.
It may record:
- Documentary Selection;
- Documentary Placement;
- Immediate Documentary Effect;
- Inquiry Transformation;
- Remaining Open Question.
It concerns documented structure, not speculative psychology.
40. REPOSITORY SYNTHESIS
A Repository Artifact that records the outcome of a completed inquiry at two levels:
1. Documentary achievement:
What has been faithfully recovered?
2. Educational achievement:
What durable investigative Capacity has been acquired?
A Repository Synthesis does not supersede the underlying Citation Object.
41. CERTIFICATION RECORD
A holistic Repository Artifact attesting that an entire artifact or package satisfies the
defined conditions for preservation, reproducibility, documentary integrity, and archival
admission.
Certification shall identify the Validation Records on which it depends.
Certification follows validation.
Certification attests process and archival status.
Certification does not convert uncertainty into certainty and does not make an
interpretation true merely by certifying it.
42. DOCUMENTARY DECISION RECORD
A narrowly bounded Repository Artifact preserving an externally reviewable decision
that materially affects documentary interpretation, preservation, classification, or
production.
Every Documentary Decision Record shall identify:
- the decision made;
- the affected entities or artifacts;
- the documentary or constitutional basis;
- alternatives considered where necessary for reproducibility;
- the responsible Agent or process;
- the resulting action;
- unresolved limitations.
It shall not contain private chain-of-thought.
It shall not serve as a general reasoning log.
Interpretive claims belong in Interpretations and Claims. Technical runtime logs belong
outside the canonical Documentary Memory unless preserved as Validation or
Provenance Records.
43. CORRECTION RECORD
A Repository Artifact that documents an identified error, the affected artifact, the
correction, the reason for correction, and the relation between versions.
A Correction Record never silently alters the historical text of a prior certified artifact.
43.1 CAPACITY RECORD
A Repository Artifact documenting a durable investigative ability acquired through
repeated, certified documentary inquiry.
A Capacity Record identifies:
- the Capacity acquired;
- the inquiries and certified artifacts from which it arose;
- the documentary practices that constitute the Capacity;
- evidence that the Capacity has been demonstrated;
- limitations and conditions of application.
Examples include:
- reconstruction before interpretation;
- recognition of citation as documentary evidence;
- recovery of inquiry architecture;
- preservation of authorial independence.
A Capacity Record records what the Repository has become able to do.
It is not itself an Inquiry or a Claim about a historical source.
43.2 RELATIONSHIP ASSERTION
A Repository Artifact that records a formally asserted relationship between two or more
entities where the relationship itself requires identity, provenance, evidence, status, or
version history.
Relationship predicates shall be governed by the later Relationship Specification.
Relationship Assertions may document, among other things:
- dependency;
- contradiction;
- interpretive divergence;
- refinement;
- correction;
- extension;
- support;
- derivation;
- succession;
- supersession.
A Relationship Assertion shall preserve:
- subject entity;
- predicate;
- object entity;
- documentary basis;
- responsible Agent or process;
- epistemic or validation status;
- version and provenance.
The existence of Relationship Assertion as a class does not predetermine the permitted
relationship vocabulary.
I. STRUCTURAL AND ADMINISTRATIVE ARTIFACTS
44. MANIFEST
A machine-readable or human-readable Repository Artifact describing the identity,
class, components, provenance, version, status, completeness, and integrity
information of another artifact or package.
45. LEDGER
An ordered, appendable Repository Artifact preserving atomic records of one
controlled kind.
Ledger subtypes may include:
- Claim Ledger;
- Evidence Ledger;
- Relationship Ledger;
- Version Ledger;
- Validation Ledger.
46. REGISTER
A canonical collection maintaining recognized entities or controlled records of a defined
class.
Register subtypes may include:
- Authority Register;
- Work Register;
- Witness Register;
- Theme Register;
- Documentary Register;
- Hermeneutic Process Register;
- Hypothesis Register;
- Capacity History.
A Register preserves identity and status.
It does not silently reinterpret its contents.
47. CATALOG
A Repository Artifact indexing artifacts, entities, versions, Locations, statuses,
dependencies, and validation states across the Repository.
The Catalog supports discovery.
It does not replace the artifacts it indexes.
47.1 WITNESS COLLECTION
A curated Repository Artifact grouping Witnesses for a defined Work, Expression, Work
Component, Inquiry, or documentary purpose.
A Witness Collection is not itself a Witness.
It shall record:
- the Witnesses included;
- the principle of selection;
- relevant authority or comparative roles;
- coverage limits;
- known excluded or unavailable Witnesses;
- dependencies on particular inquiries or Citation Objects;
- provenance and version history.
Witness Collections support large-scale discovery and comparison without collapsing
Witness identities.
J. GOVERNANCE AND FORMALIZATION ENTITIES
47.2 CONSTITUTIONAL ENTITY
A Governance and Formalization Entity governing mission, documentary principles,
institutional limits, and safeguards.
Constitutional Entities possess priority over Technical Formalization Entities.
48. FOUNDATIONAL DOCUMENT
A Constitutional Entity defining the enduring mission, discipline, constitution, or
operating architecture of the Straussian Reader or Documentary Memory.
Examples include:
- Operating System;
- Learning System;
- Repository Safeguards.
49. SAFEGUARD
A binding Constitutional Entity protecting documentary fidelity, source priority, authorial
independence, uncertainty, reproducibility, version history, and mission integrity.
50. AMENDMENT
A versioned Constitutional Entity that supplements or revises an existing constitutional
rule without silently rewriting prior documentary history.
50.1 TECHNICAL FORMALIZATION ENTITY
A Governance and Formalization Entity defining implementation rules within
constitutional limits.
Technical Formalization Entities may evolve more readily than Constitutional Entities,
but they may never override them.
51. SPECIFICATION
A normative Technical Formalization Entity defining a structural or technical rule.
Specification subtypes include:
- Documentary Ontology;
- Identifier Specification;
- Relationship Specification;
- URI Specification;
- Packaging Specification;
- Graph Specification.
A Specification implements constitutional principles.
It does not revise them merely by technical necessity.
52. SCHEMA
A formal, machine-verifiable Technical Formalization Entity describing permitted
structure, properties, values, and validation requirements.
A Schema implements a Specification.
A Schema does not possess authority to revise the Specification or Constitutional Entity
it implements.
53. CONTROLLED VOCABULARY
A governed Technical Formalization Entity containing permitted terms used for
classification, status, roles, themes, operation modes, completeness states, or
relationship types.
Controlled terms shall not be invented ad hoc during production.
K. CONTROLLED CONCEPT ENTITIES
54. THEME
A registered conceptual term used to organize documentary inquiry without replacing
the language of the source.
Themes support retrieval and comparison.
A Theme is not itself a Claim or Interpretation.
55. EPISTEMIC CLASSIFICATION
A controlled category describing the documentary status of a Claim or Question.
The governing epistemic system may include:
- Documented Finding;
- Supported Inference;
- Working Hypothesis;
- Unresolved Question;
- Constitutional Principle.
Numerical confidence shall not substitute for these classifications.
56. STATUS
A controlled lifecycle category.
Examples may include:
- Draft;
- Under Review;
- Final;
- Certified;
- Superseded;
- Corrected;
- Archived.
57. ROLE
A controlled contextual function borne by an entity.
Examples may include:
- author;
- editor;
- translator;
- cited source;
- citing source;
- primary source;
- secondary source;
- authoritative witness;
- control witness;
- investigator;
- secretary;
- certifier.
Roles shall not be mistaken for entity classes.
58. LANGUAGE
A controlled concept identifying the language of a Work, Expression, Witness, Passage,
Quotation, or Translation.
58.1 OPERATION MODE
A controlled concept identifying the epistemic basis of a Documentary Operation.
Permitted values shall include:
- recovered;
- responsibly reconstructed;
- hypothetical reconstruction.
Additional values require versioned revision of the controlled vocabulary.
Operation Mode shall not be replaced by numerical confidence.
58.2 HERMENEUTIC COMPLETENESS
A controlled concept describing which required Hermeneutic Objects or stages are
present, complete, partial, pending, inapplicable, or absent within a Citation Object.
The exact vocabulary shall be defined in a later Specification.
It shall support distinctions such as:
- A complete;
- B complete;
- C complete;
- A and C complete;
- A, B, and C complete;
- partial;
- pending;
- inapplicable.
Hermeneutic Completeness is a status property, not a new ontology class.
58.3 QUESTION STATUS
A controlled concept describing the relation of a Question to Repository inquiry.
Permitted categories may include:
- unassigned;
- assigned;
- active;
- deferred;
- unresolved after investigation;
- closed;
- superseded.
An unassigned Question remains a Question.
It does not require a duplicate entity class.
L. PROVENANCE AND LIFECYCLE ENTITIES
59. VERSION RECORD
A Repository Artifact identifying a particular state of an entity or artifact without
changing its underlying identity.
60. REVISION RECORD
A Repository Artifact documenting what changed between versions, why it changed,
who or what authorized the change, and which prior version remains preserved.
61. PROVENANCE RECORD
A Repository Artifact documenting origin, custody, derivation, transformation,
authorship, acquisition, and processing history.
62. ACQUISITION RECORD
A Provenance Record documenting when, where, and how a Witness or other external
documentary entity entered the Repository.
63. VALIDATION RECORD
A Repository Artifact documenting one discrete check against defined structural,
documentary, procedural, or computational criteria.
A Validation Record shall identify:
- the entity or artifact checked;
- the criteria;
- the method;
- the result;
- the Agent or process;
- the date;
- limitations;
- any required correction or revalidation.
Validation reports the result of a check.
It does not by itself certify the whole artifact.
64. FIXITY RECORD
A Repository Artifact preserving checksums or equivalent integrity evidence for a
stored file or package.
Fixity proves file stability.
It does not prove documentary accuracy.
64.1 DERIVATION RECORD
A Provenance Record documenting the creation of one Witness, Expression, or
Repository Artifact from another.
It shall identify:
- source entity;
- derived entity;
- transformation process;
- responsible Agent or tool;
- date;
- software and version, where relevant;
- validation status;
- known loss, normalization, or uncertainty.
Derived Witnesses shall be supported by Derivation Records.
IV. REQUIRED ONTOLOGICAL SEPARATIONS
The following distinctions are mandatory:
1. Agent is not Work.
2. Work is not Expression.
3. Expression is not Witness.
4. Source Witness is not Derived Witness.
5. Transcription as Expression is not the file or embodiment that serves as its Derived
Witness.
6. Witness is not Witness Collection.
7. Witness is not Location.
8. Location is not Passage.
9. Passage is not Context.
10. Textual Variant is not automatically a separate Expression.
11. Source Apparatus is not Intertextual Apparatus Record.
12. Citation is not Quotation.
13. Episodic Documentary Operation is not Structural Pattern.
14. Recovered operation is not responsibly reconstructed operation.
15. Source entity is not Repository Artifact.
16. Claim is not Evidence.
17. Evidence Record is atomic; Evidence Chain is composite.
18. Observation is not Interpretation.
19. Hypothesis is not Documented Finding.
20. Comparison is the inquiry process; Comparative Reconstruction is the preserved
artifact.
21. Inquiry is not the artifact produced by the Inquiry.
22. Validation is not Certification.
23. Constitutional Entity is not Technical Formalization Entity.
24. Safeguard has priority over Specification and Schema.
25. Capacity Record is not Inquiry.
26. Theme is not Claim.
27. Role is not entity identity.
28. Status is not entity identity.
29. Version is not entity identity.
30. Certification is not proof of truth.
31. Relationship Assertion is not the entities it relates.
32. Graph node is not the authoritative artifact.
33. Storage location is not documentary identity.
34. Technical convenience is not ontological necessity.
V. SOURCE AND EVIDENCE ROLES
The following are roles rather than independent top-level classes:
- Primary Source
- Secondary Source
- Cited Source
- Citing Source
- Comparative Source
- Authoritative Witness
- Control Witness
- Evidence
- Contextual Evidence
- Corroborating Evidence
- Contradictory Evidence
- Source Witness in a particular derivation chain
- Target Witness in a validation process
These roles are inquiry-relative or process-relative.
The same entity may bear different roles in different inquiries or derivation chains
without changing identity.
Interpretive divergence, dependency, conflict, refinement, and extension are
relationship predicates or Relationship Assertion types to be defined in the Relationship
Specification. They are not separate source classes.
VI. AGGREGATE AND ATOMIC ENTITIES
ATOMIC ENTITIES
Atomic entities are intended to be independently addressable at the smallest useful
documentary scale.
Examples include:
- Location;
- Passage;
- Textual Variant;
- Citation;
- Quotation;
- Question;
- Claim;
- Evidence Record;
- Documentary Register Entry;
- Validation Record;
- Relationship Assertion, when individually asserted.
AGGREGATE ENTITIES
Aggregate entities contain or organize other entities while retaining their own identity.
Examples include:
- Work;
- Expression;
- Witness;
- Witness Collection;
- Inquiry;
- Evidence Chain;
- Intertextual Apparatus Record;
- Citation Object;
- Register;
- Catalog;
- Comparative Reconstruction;
- Repository Synthesis.
Aggregation never permits the loss of component identity or provenance.
An Evidence Chain is composed of Evidence Records.
A Witness Collection is composed of Witness references, not merged Witness
identities.
A Citation Object aggregates or references constituent artifacts while preserving their
separate identities.
VII. ONTOLOGICAL INVARIANTS
1. Every entity shall possess one stable identity independent of name, title, file path,
database key, or storage system.
2. Every entity shall have one most-specific canonical class.
3. Roles, statuses, classifications, and operation modes shall not silently create
duplicate identities.
4. Every Repository-produced artifact shall be explicitly distinguished from external
documentary sources.
5. Every Witness shall be recoverable through provenance and Location information
sufficient for verification.
6. Every Derived Witness shall identify its source Witness or Witnesses through a
Derivation Record.
7. Every Textual Variant shall identify the Witness and Location in which it occurs or
against which it is compared.
8. Every Claim shall preserve its epistemic classification.
9. Every Documentary Operation shall preserve its Operation Mode.
10. Every Evidence Record shall point back to recoverable documentary entities.
11. Every Evidence Chain shall preserve the identities and order of its component
Evidence Records.
12. Every Intertextual Apparatus Record shall preserve the external Source Apparatus
on which it depends.
13. Every aggregate artifact shall preserve the identities of its components.
14. Every Validation Record shall state the criteria, method, result, and limitations of the
check.
15. Every Certification Record shall identify the Validation Records and review on which
it depends.
16. Every revision shall preserve prior versions and the reason for change.
17. Every Constitutional Entity shall retain priority over Technical Formalization Entities.
18. Unknowns shall remain unknown until documentary evidence permits revision.
19. Unassigned, deferred, and unresolved Questions shall remain distinguishable
through Question Status.
20. The graph shall be derived from canonical artifacts and shall never replace them.
21. Technology-specific objects shall remain implementation representations unless a
genuine documentary class is demonstrated through production.
22. No ontology class shall encode speculative intention, hidden motive, reader
psychology, or unsupported authorial purpose.
23. The ontology shall remain small enough to govern production and complete enough
to preserve documentary distinctions.
VIII. NON-GOALS
The Documentary Ontology does not:
- define Strauss's philosophy;
- classify philosophical doctrines;
- infer hidden intentions;
- replace close reading;
- define the final relationship predicate vocabulary;
- assign permanent identifiers;
- prescribe GitHub folders;
- prescribe Neo4j labels;
- prescribe MCP tools;
- prescribe JSON, YAML, XML, RDF, or database syntax;
- define file naming conventions;
- authorize numerical confidence scores;
- treat transcription files as equivalent to source Witnesses without provenance;
- treat structural patterns as directly recovered operations;
- convert interpretation into evidence;
- convert Validation into Certification;
- allow Specification or Schema to override Safeguards;
- replace the Repository Safeguards.
Those matters belong to other specifications or to documentary inquiry itself.
IX. CLASS ADMISSION RULE
A new ontology class may be introduced only when all of the following conditions are
satisfied:
1. Production has demonstrated a recurring documentary need.
2. The proposed class possesses a stable identity distinguishable from existing classes.
3. The need cannot be represented adequately as:
- a role;
- a property;
- a status;
- a relationship;
- a controlled vocabulary term;
- a component of an existing class.
4. The class is required for documentary fidelity, reproducibility, provenance, or durable
retrieval.
5. The class is not being introduced merely because a storage system, programming
language, database, or user interface makes it convenient.
6. The change is issued through a versioned revision of this ontology.
7. The revision includes:
- reason for admission;
- affected classes;
- migration consequences;
- relation to prior versions;
- preservation of prior documentary history.
X. CANONICAL CLASS HIERARCHY
Repository Entity
1. Agent
1.1 Person
1.2 Collective Agent
2. Intellectual Entity
2.1 Work
2.2 Work Component
2.3 Expression
2.3.1 Translation
2.3.2 Edition or Recension
2.3.3 Transcription
3. Documentary Witness
3.1 Witness
3.1.1 Source Witness
3.1.2 Derived Witness
3.2 Witness Component
3.3 Textual Variant
4. Documentary Address and Segment
4.1 Location
4.2 Passage
4.3 Context
4.4 Source Apparatus as a functional configuration of existing source entities
5. Documentary Operation
5.1 Citation
5.2 Quotation
5.3 Selection
5.4 Omission
5.5 Placement
5.6 Sequence
6. Inquiry Entity
6.1 Inquiry
6.2 Question
6.3 Claim
6.3.1 Observation
6.3.2 Interpretation
6.3.2.1 Structural Pattern
6.3.3 Hypothesis
6.4 Comparison
6.5 Task
7. Evidentiary Entity
7.1 Evidence Record
7.2 Evidence Chain
7.3 Intertextual Apparatus Record
8. Repository Production Artifact
8.1 Documentary Register Entry
8.2 Citation Object
8.3 Hermeneutic Object A
8.4 Hermeneutic Object B
8.5 Hermeneutic Object C
8.6 Comparative Reconstruction
8.7 Inquiry Architecture Record
8.8 Repository Synthesis
8.9 Certification Record
8.10 Documentary Decision Record
8.11 Correction Record
8.12 Capacity Record
8.13 Relationship Assertion
9. Structural and Administrative Artifact
9.1 Manifest
9.2 Ledger
9.3 Register
9.4 Catalog
9.5 Witness Collection
10. Governance and Formalization Entity
10.1 Constitutional Entity
10.1.1 Foundational Document
10.1.2 Safeguard
10.1.3 Amendment
10.2 Technical Formalization Entity
10.2.1 Specification
10.2.2 Schema
10.2.3 Controlled Vocabulary
11. Controlled Concept
11.1 Theme
11.2 Epistemic Classification
11.3 Status
11.4 Role
11.5 Language
11.6 Operation Mode
11.7 Hermeneutic Completeness
11.8 Question Status
12. Provenance and Lifecycle Entity
12.1 Version Record
12.2 Revision Record
12.3 Provenance Record
12.4 Acquisition Record
12.5 Validation Record
12.6 Fixity Record
12.7 Derivation Record
XI. DEPENDENCY ORDER
The Repository shall proceed in the following architectural order:
Documentary Ontology
â
Identifier Specification
â
Relationship Specification
â
Canonical Registers
â
Repository Catalog and Manifests
â
Validation Schemas
â
Citation Object Conversion and Packaging
â
Knowledge Graph Projection
â
Retrieval Interface
â
Straussian Reader Integration
Ontology precedes identity.
Identity precedes storage.
Relationships precede retrieval.
Evidence precedes inference.
XII. FINAL DECLARATION
The Documentary Ontology establishes the permanent conceptual foundation of the
Straussian Documentary Memory.
Version 1.1 preserves and sharpens the distinction between:
- authors and works;
- works, Expressions, and Witnesses;
- source and Derived Witnesses;
- transcriptions as Expressions and transcription files as Witnesses;
- stable text and Textual Variants;
- Citations and Quotations;
- Source Apparatus and Intertextual Apparatus Records;
- episodic operations and Structural Patterns;
- recovered and reconstructed operations;
- sources and Repository artifacts;
- evidence, Evidence Records, Evidence Chains, and Claims;
- documentary findings and Interpretation;
- Comparison and Comparative Reconstruction;
- Validation and Certification;
- constitutional authority and technical formalization;
- Inquiry and Capacity Record;
- identity and version;
- ontology and implementation.
Every future specification, register, schema, graph projection, Citation Object package,
and retrieval tool shall conform to these distinctions.
No implementation may silently alter them.
No completed version may be overwritten.
Future revision requires explicit versioning, preserved history, and documented
necessity arising from Repository production.
REVISION HISTORY
Version 1.0
Initial release establishing the foundational entity classes and ontological separations.
Version 1.1
Revised consolidated release following adversarial architectural review. Version 1.0
remains preserved and unchanged.
END OF DOCUMENT
Document: Documentary Ontology
Version: 1.1
Document Number: 000001
Classification: Foundational Repository Specification
