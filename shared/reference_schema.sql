-- Shared Reference Database for All Agents
-- All agents can query this unified reference system

CREATE TABLE IF NOT EXISTS references_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    title TEXT NOT NULL,
    content TEXT,
    file_path TEXT,
    tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cross_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_agent TEXT NOT NULL,
    target_agent TEXT NOT NULL,
    reference_id INTEGER,
    relation_type TEXT,
    FOREIGN KEY (reference_id) REFERENCES references_index(id)
);

CREATE TABLE IF NOT EXISTS agent_knowledge_sharing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_agent TEXT NOT NULL,
    to_agent TEXT NOT NULL,
    knowledge_topic TEXT,
    knowledge_content TEXT,
    shared_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT 0
);

CREATE INDEX idx_agent_category ON references_index(agent_name, category);
CREATE INDEX idx_tags ON references_index(tags);
CREATE INDEX idx_cross_ref ON cross_references(source_agent, target_agent);
