//! Chronicle Bridge for CrustyClaw
//! Connects to WebClaw and DataClaw chronicle indexes

use std::collections::HashMap;
use serde::{Serialize, Deserialize};
use reqwest::Client;

#[derive(Debug, Serialize, Deserialize)]
pub struct ChronicleResult {
    pub url: String,
    pub context: String,
    pub source: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct UnifiedSearchResult {
    pub query: String,
    pub webclaw: Vec<ChronicleResult>,
    pub dataclaw: Vec<ChronicleResult>,
    pub total: usize,
}

pub struct ChronicleBridge {
    client: Client,
    webclaw_url: String,
    dataclaw_url: String,
}

impl ChronicleBridge {
    pub fn new() -> Self {
        Self {
            client: Client::new(),
            webclaw_url: "http://127.0.0.1:8765".to_string(),
            dataclaw_url: "http://127.0.0.1:8765".to_string(),
        }
    }

    pub async fn search_webclaw(&self, query: &str, limit: usize) -> Vec<ChronicleResult> {
        let url = format!("{}/v1/search?q={}&limit={}", self.webclaw_url, query, limit);
        
        match self.client.get(&url).send().await {
            Ok(response) => {
                if let Ok(results) = response.json::<Vec<ChronicleResult>>().await {
                    results
                } else {
                    vec![]
                }
            }
            Err(_) => vec![],
        }
    }

    pub async fn search_dataclaw(&self, query: &str, limit: usize) -> Vec<ChronicleResult> {
        let url = format!("{}/v1/dataclaw/search?q={}&limit={}", self.dataclaw_url, query, limit);
        
        match self.client.get(&url).send().await {
            Ok(response) => {
                if let Ok(results) = response.json::<Vec<ChronicleResult>>().await {
                    results
                } else {
                    vec![]
                }
            }
            Err(_) => vec![],
        }
    }

    pub async fn unified_search(&self, query: &str, limit: usize) -> UnifiedSearchResult {
        let webclaw = self.search_webclaw(query, limit).await;
        let dataclaw = self.search_dataclaw(query, limit).await;
        
        UnifiedSearchResult {
            query: query.to_string(),
            webclaw,
            dataclaw: dataclaw,
            total: webclaw.len() + dataclaw.len(),
        }
    }

    pub async fn index_code(&self, file_path: &str, content: &str, language: &str) -> bool {
        let url = format!("{}/v1/index", self.webclaw_url);
        
        let mut map = HashMap::new();
        map.insert("url", format!("file://{}", file_path));
        map.insert("context", format!("Code: {}\n{}", file_path, &content[..content.len().min(500)]));
        map.insert("source", format!("crustyclaw/{}", language));
        
        match self.client.post(&url).json(&map).send().await {
            Ok(response) => response.status().is_success(),
            Err(_) => false,
        }
    }

    pub async fn get_stats(&self) -> HashMap<String, usize> {
        let mut stats = HashMap::new();
        
        if let Ok(response) = self.client.get(&format!("{}/v1/stats", self.webclaw_url)).send().await {
            if let Ok(json) = response.json::<HashMap<String, usize>>().await {
                stats.insert("webclaw_cards".to_string(), json.get("total_cards").copied().unwrap_or(0));
            }
        }
        
        stats
    }
}

// Global instance
lazy_static::lazy_static! {
    pub static ref CHRONICLE_BRIDGE: ChronicleBridge = ChronicleBridge::new();
}
