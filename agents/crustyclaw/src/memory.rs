//! Procedural Memory with confidence decay
//! Inspired by cass-memory

use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemoryRule {
    pub id: String,
    pub content: String,
    pub category: String,
    pub helpful_count: u32,
    pub harmful_count: u32,
    pub created_at: u64,
    pub last_used: Option<u64>,
    pub maturity: Maturity,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum Maturity {
    Candidate,
    Established,
    Proven,
    Deprecated,
}

pub struct ProceduralMemory {
    rules: HashMap<String, MemoryRule>,
    storage_path: std::path::PathBuf,
}

impl ProceduralMemory {
    pub fn new(storage_dir: &str) -> Self {
        let path = std::path::PathBuf::from(storage_dir).join("memory.json");
        let rules = if path.exists() {
            let data = std::fs::read_to_string(&path).unwrap_or_default();
            serde_json::from_str(&data).unwrap_or_default()
        } else {
            HashMap::new()
        };
        
        Self {
            rules,
            storage_path: path,
        }
    }

    pub fn add_rule(&mut self, content: String, category: String) -> String {
        let id = format!("rule_{}", self.rules.len() + 1);
        let now = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs();
        
        let rule = MemoryRule {
            id: id.clone(),
            content,
            category,
            helpful_count: 0,
            harmful_count: 0,
            created_at: now,
            last_used: None,
            maturity: Maturity::Candidate,
        };
        
        self.rules.insert(id.clone(), rule);
        self.save();
        id
    }

    pub fn record_feedback(&mut self, id: &str, helpful: bool) {
        if let Some(rule) = self.rules.get_mut(id) {
            if helpful {
                rule.helpful_count += 1;
            } else {
                rule.harmful_count += 1;
            }
            self.update_maturity(rule);
            self.save();
        }
    }

    fn update_maturity(&self, rule: &mut MemoryRule) {
        let total = rule.helpful_count + rule.harmful_count;
        let harmful_ratio = if total > 0 {
            rule.harmful_count as f32 / total as f32
        } else {
            0.0
        };
        
        rule.maturity = match (rule.helpful_count, harmful_ratio) {
            (h, _) if h >= 10 && harmful_ratio < 0.1 => Maturity::Proven,
            (h, _) if h >= 3 && harmful_ratio < 0.25 => Maturity::Established,
            (_, r) if r > 0.5 => Maturity::Deprecated,
            _ => Maturity::Candidate,
        };
    }

    pub fn get_relevant_rules(&self, task: &str, limit: usize) -> Vec<&MemoryRule> {
        let mut scored: Vec<(&MemoryRule, f32)> = self.rules.values()
            .filter(|r| r.maturity != Maturity::Deprecated)
            .map(|r| {
                let relevance = if task.to_lowercase().contains(&r.category.to_lowercase()) {
                    0.5
                } else {
                    0.0
                };
                let confidence = (r.helpful_count as f32) - (r.harmful_count as f32 * 4.0);
                (r, relevance + confidence.min(1.0).max(0.0))
            })
            .collect();
        
        scored.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        scored.into_iter().take(limit).map(|(r, _)| r).collect()
    }

    fn save(&self) {
        let data = serde_json::to_string_pretty(&self.rules).unwrap();
        std::fs::write(&self.storage_path, data).unwrap();
    }
}
