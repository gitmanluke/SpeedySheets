import sqlite3
import tempfile
import os
from queryService.DBvalidator import DBvalidator

def _make_test_db():
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    conn = sqlite3.connect(path)
    conn.execute('CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT)')
    conn.execute('CREATE TABLE players (id INTEGER PRIMARY KEY, goals INTEGER)')
    conn.commit()
    conn.close()
    return path

_DB_PATH = _make_test_db()
_validator = DBvalidator(_DB_PATH)


def teardown_module(module):
    os.unlink(_DB_PATH)


def test_valid_select():
    assert _validator.valid_query("SELECT name FROM people") is True

def test_valid_select_star():
    assert _validator.valid_query("SELECT * FROM people WHERE id = 1") is True

def test_insert_blocked():
    assert _validator.valid_query("INSERT INTO people VALUES (1, 'x')") is False

def test_drop_blocked():
    assert _validator.valid_query("DROP TABLE people") is False

def test_update_blocked():
    assert _validator.valid_query("UPDATE people SET name='x'") is False

def test_delete_blocked():
    assert _validator.valid_query("DELETE FROM people") is False

def test_nonexistent_table():
    assert _validator.valid_query("SELECT * FROM ghost_table") is False

def test_nonexistent_column():
    assert _validator.valid_query("SELECT fake_col FROM people") is False

def test_empty_string():
    assert _validator.valid_query("") is False

def test_whitespace_only():
    assert _validator.valid_query("   ") is False

def test_non_string_int():
    assert _validator.valid_query(42) is False

def test_non_string_none():
    assert _validator.valid_query(None) is False

def test_semicolon_injection():
    assert _validator.valid_query("SELECT 1; DROP TABLE people") is False

def test_case_insensitive():
    assert _validator.valid_query("select name from people") is True

def test_pragma_blocked():
    assert _validator.valid_query("PRAGMA table_info(people)") is False
