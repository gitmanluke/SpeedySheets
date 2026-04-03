import sqlite3
import re
import os

_BLOCKED_KEYWORDS = frozenset({
    'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE',
    'REPLACE', 'TRUNCATE', 'ATTACH', 'DETACH', 'PRAGMA',
    'VACUUM', 'EXEC', 'EXECUTE',
})

class DBvalidator:
    def __init__(self, database_path: str):
        self._database_path = database_path

    def valid_query(self, query: str) -> bool:
        if not isinstance(query, str) or not query.strip():
            return False
        query = query.strip()
        if not self._is_select_only(query):
            return False
        if self._contains_blocked_keywords(query):
            return False
        return self._validate_against_db(query)

    def _is_select_only(self, query: str) -> bool:
        match = re.match(r'\s*(\w+)', query)
        return bool(match) and match.group(1).upper() == 'SELECT'

    def _contains_blocked_keywords(self, query: str) -> bool:
        tokens = set(re.findall(r'\b\w+\b', query.upper()))
        return bool(tokens & _BLOCKED_KEYWORDS)

    def _validate_against_db(self, query: str) -> bool:
        abs_path = os.path.abspath(self._database_path)
        uri = f"file:{abs_path}?mode=ro"
        conn = None
        try:
            conn = sqlite3.connect(uri, uri=True)
            conn.execute(f"EXPLAIN {query}")
            return True
        except (sqlite3.OperationalError, sqlite3.ProgrammingError, sqlite3.DatabaseError):
            return False
        finally:
            if conn:
                conn.close()
