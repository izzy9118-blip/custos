CANONICAL_PATH_QUERY = """
MATCH (n:CanonicalEntity {
  projection_id: $projection_id,
  canonical_id: $canonical_id
})
RETURN n.canonical_id AS canonical_id,
       n.canonical_class AS canonical_class,
       n.github_path AS github_path,
       n.git_commit AS git_commit,
       n.source_fixity_sha256 AS source_fixity_sha256,
       n.source_role AS source_role,
       n.title AS title
""".strip()

REL_BACKED_NEIGHBORHOOD_QUERY = """
MATCH (subject:CanonicalEntity {
  projection_id: $projection_id,
  canonical_id: $canonical_id
})-[r:REFERENCES]->(object:CanonicalEntity {projection_id: $projection_id})
RETURN subject.canonical_id AS subject_id,
       r.rel_id AS rel_id,
       r.relationship_type AS predicate,
       object.canonical_id AS object_id
ORDER BY predicate, object_id
""".strip()

PROJECTION_CONSTRAINT_QUERY = """
CREATE CONSTRAINT canonical_entity_projection_identity IF NOT EXISTS
FOR (n:CanonicalEntity)
REQUIRE (n.projection_id, n.canonical_id) IS UNIQUE
""".strip()

CLEAR_PROJECTION_QUERY = """
MATCH (n {projection_id: $projection_id})
WHERE n:CanonicalEntity OR n:ProjectionSnapshot
DETACH DELETE n
""".strip()

WRITE_NODES_QUERY = """
UNWIND $nodes AS row
CREATE (n:CanonicalEntity)
SET n = row
""".strip()

WRITE_EDGES_QUERY = """
UNWIND $edges AS row
MATCH (subject:CanonicalEntity {
  projection_id: $projection_id,
  canonical_id: row.subject_id
})
MATCH (object:CanonicalEntity {
  projection_id: $projection_id,
  canonical_id: row.object_id
})
CREATE (subject)-[r:REFERENCES]->(object)
SET r = row.properties
""".strip()

WRITE_PROJECTION_METADATA_QUERY = """
CREATE (snapshot:ProjectionSnapshot)
SET snapshot = $metadata
""".strip()

PROJECTION_METADATA_QUERY = """
MATCH (snapshot:ProjectionSnapshot {projection_id: $projection_id})
RETURN snapshot.projection_id AS projection_id,
       snapshot.repository_full_name AS repository_full_name,
       snapshot.git_commit AS git_commit,
       snapshot.cognitive_memory_manifest_id AS cognitive_memory_manifest_id,
       snapshot.integrity_sha256 AS integrity_sha256,
       snapshot.projector_version AS projector_version
""".strip()

DOCUMENTARY_NODES_QUERY = """
UNWIND $canonical_ids AS requested_id
OPTIONAL MATCH (n:CanonicalEntity {
  projection_id: $projection_id,
  canonical_id: requested_id
})
RETURN requested_id,
       n.canonical_id AS canonical_id,
       n.canonical_class AS canonical_class,
       n.github_path AS github_path,
       n.git_commit AS git_commit,
       n.cognitive_memory_manifest_id AS cognitive_memory_manifest_id,
       n.source_fixity_sha256 AS source_fixity_sha256,
       n.source_role AS source_role,
       n.title AS title
ORDER BY requested_id
""".strip()

RELATED_DOCUMENTARY_NODES_QUERY = """
UNWIND $canonical_ids AS seed_id
MATCH (subject:CanonicalEntity {
  projection_id: $projection_id,
  canonical_id: seed_id
})-[r:REFERENCES]->(object:CanonicalEntity {projection_id: $projection_id})
WHERE r.relationship_type IN $relationship_types
RETURN seed_id,
       r.relationship_type AS relationship_type,
       r.source_field AS source_field,
       object.canonical_id AS canonical_id
ORDER BY seed_id, relationship_type, canonical_id
LIMIT $limit
""".strip()
