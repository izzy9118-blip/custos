from __future__ import annotations

from typing import Any


class Neo4jUnavailable(RuntimeError):
    pass


class Neo4jClient:
    """Optional adapter. Importing the package does not require neo4j."""

    def __init__(self, uri: str, username: str, password: str) -> None:
        try:
            from neo4j import GraphDatabase
        except ImportError as exc:
            raise Neo4jUnavailable(
                "Install the optional neo4j dependency: pip install -e '.[neo4j]'"
            ) from exc
        self._driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self) -> None:
        self._driver.close()

    def execute_write(self, query: str, parameters: dict[str, Any]) -> None:
        with self._driver.session() as session:
            session.execute_write(lambda tx: tx.run(query, parameters).consume())

    def execute_read(
        self, query: str, parameters: dict[str, Any]
    ) -> list[dict[str, Any]]:
        with self._driver.session() as session:
            records = session.execute_read(
                lambda tx: list(tx.run(query, parameters))
            )
        return [record.data() for record in records]
