# STRAUSSIAN DOCUMENTARY MEMORY
# RELATIONSHIP SPECIFICATION — INFERENCE CLARIFICATION AMENDMENT

**Amendment Version:** 1.0  
**Affected Document:** 000003 — Relationship Specification v1.0  
**Affected Section:** VIII. Inferability  
**Status:** Finalized Amendment Instrument — Awaiting Repository Admission  
**Purpose:** Replace the ungoverned marking “INFERRED” with a constitutionally explicit representation of materialized inference

## I. PRESERVATION

This amendment preserves Relationship Specification v1.0.

Upon admission, it shall create an explicit amendment relation to the prior specification, preserve the original text, and govern inference representation prospectively according to its effective-date decision.

All prior REL identifiers and historical assertions remain preserved.

## II. DEFECT CORRECTED

Relationship Specification v1.0 requires a materialized inference to be “explicitly marked INFERRED.”

The Controlled Vocabulary Specification does not establish INFERRED as:

- a Lifecycle Status;
- a Review/Dispute Status;
- a Revision Status;
- an Epistemic Classification;
- an Operation Mode;
- or another approved controlled value.

The requirement therefore cannot be implemented constitutionally without either:

1. registering a new governed concept in an authorized family; or
2. expressing inference through values and records already established.

This amendment adopts the second and narrower solution.

## III. REPLACEMENT TEXT FOR SECTION VIII

### VIII. INFERABILITY

#### A. Inferability Values

Each Predicate Register entry shall declare exactly one inferability value:

**NO**  
The relationship must be directly asserted and cannot be derived solely from other Relationship Assertions.

**YES**  
The relationship may be derived under the formal inference rule recorded in its Predicate Register entry.

**CONDITIONAL**  
The relationship may be derived only when every recorded precondition is satisfied.

#### B. Required Predicate Inference Record

Every Predicate with inferability YES or CONDITIONAL shall state:

- formal inference rule;
- required source Relationship Assertions;
- required source classes and predicates;
- whether the result is direct or indirect;
- provenance requirements;
- evidence-record requirements;
- cycle policy;
- failure conditions;
- whether query-time derivation is permitted;
- whether materialization is permitted.

#### C. Query-Time Derived Result

A query-time derived result:

- is not a canonical Relationship Assertion unless separately materialized and admitted;
- receives no REL identifier merely because a graph query produced it;
- must be labeled in the query response as derived;
- must expose the source REL identifiers and governing rule;
- must not be presented as directly documented.

#### D. Materialized Inferred Relationship Assertion

A materialized inference is a canonical Relationship Assertion only when it passes the Constitutional Admission Protocol.

It shall:

1. receive a permanent REL identifier;
2. preserve canonical Subject, Predicate, and Object;
3. use **SUPPORTED INFERENCE** as its Epistemic Classification;
4. use **PROCEDURAL** as its Evidence Type because the asserted relation is established through an authorized formal inference procedure;
5. link every source REL identifier;
6. link the governing Predicate Register rule;
7. include an Evidence Record or Evidence Chain preserving the complete derivation;
8. identify the validating authority and validation procedure;
9. preserve lifecycle, version history, and audit trail;
10. state explicitly that it is not a directly documented Relationship Assertion.

The source Relationship Assertions retain their own Evidence Types and Epistemic Classifications.

The materialized inference does not inherit documentary standing from them merely because its derivation is valid.

#### E. No Free-Standing INFERRED Status

No free-standing value labeled INFERRED shall be used as a Lifecycle Status, Review Status, Revision Status, Epistemic Classification, or Operation Mode unless it is separately submitted, approved, and registered through the constitutionally proper vocabulary process.

The combination of:

- EPC SUPPORTED INFERENCE;
- Evidence Type PROCEDURAL;
- source REL links;
- governing inference rule;
- Evidence Record or Evidence Chain;

constitutes the required explicit marking of a materialized inference.

#### F. Direct and Derived Separation

A derived traversal or inferred result shall never be presented as a directly documented Relationship Assertion.

Interfaces, APIs, graph queries, exports, and reports shall preserve this distinction visibly.

#### G. Graph Projection

Neo4j may compute or materialize derivative traversal edges for performance.

Such edges:

- do not become canonical REL entities by graph existence alone;
- must resolve to either a canonical REL or a declared query-time inference rule;
- must be reproducibly regenerable from GitHub canonical artifacts;
- must not silently alter canonical Relationship Assertions.

#### H. Validation

A materialized inferred REL is invalid unless:

- the Predicate permits inference;
- every precondition is satisfied;
- every source REL resolves;
- the governing rule resolves;
- EPC SUPPORTED INFERENCE is assigned;
- Evidence Type PROCEDURAL is assigned;
- the derivation record is complete;
- prohibited cycles are absent;
- the result has passed constitutional admission.

Failed materialization attempts shall be preserved in an audit or Validation Record where required.

## IV. CONFORMING CLARIFICATIONS

Upon admission, the following sentence in the Final Declaration shall be read as clarified:

> The Specification preserves the distinction between documented and inferred relationships.

“Inferred relationship” means either:

- a noncanonical query-time derived result with complete provenance; or
- an admitted materialized Relationship Assertion classified as SUPPORTED INFERENCE and supported by procedural derivation evidence.

## V. NO OTHER CHANGE

This amendment does not alter:

- predicate identity;
- Subject/Object class rules;
- Evidence Type constants;
- lifecycle cardinality;
- merger or split semantics;
- correction semantics;
- identifier families;
- graph implementation choice.

**END OF AMENDMENT**
