import sqlite3
from pathlib import Path
from contextlib import closing
SCHEMA = "CREATE TABLE IF NOT EXISTS api_notes (\n id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL,\n status TEXT NOT NULL CHECK(status IN ('draft','published')), version INTEGER NOT NULL DEFAULT 1,\n created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),\n updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')));\nCREATE TABLE IF NOT EXISTS api_idempotency (\n scope TEXT NOT NULL, key TEXT NOT NULL, fingerprint TEXT NOT NULL,\n response TEXT NOT NULL, PRIMARY KEY(scope,key));\nCREATE INDEX IF NOT EXISTS api_notes_status ON api_notes(status);"

def connect(path):
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    return db

def initialize(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with closing(connect(path)) as db:
        db.execute('PRAGMA journal_mode=WAL')
        db.executescript(SCHEMA)

def rows(cursor):
    return [dict(row) for row in cursor.fetchall()]
