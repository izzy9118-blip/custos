CANONICAL_PATH_QUERY = """
MATCH (n {canonical_id: $canonical_id})
RETURN n.canonical_id AS canonical_id,
       n.canonical_class AS canonical_class,
       n.github_path AS github_path,
       n.git_commit AS git_commit
""".strip()

REL_BACKED_NEIGHBORHOOD_QUERY = """
MATCH (subject {canonical_id: $canonical_id})-[r]->(object)
WHERE r.rel_id IS NOT NULL
RETURN subject.canonical_id AS subject_id,
       r.rel_id AS rel_id,
       type(r) AS predicate,
       object.canonical_id AS object_id
ORDER BY rel_id, object_id
""".strip()
