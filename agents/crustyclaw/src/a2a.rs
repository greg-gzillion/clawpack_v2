//! A2A Protocol Client - Communicates with Clawpack agents

use serde::{Serialize, Deserialize};
use reqwest::Client;

#[derive(Debug, Serialize, Deserialize)]
pub struct ChatRequest {
    pub task: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ChatResponse {
    pub status: String,
    pub agent: String,
    pub message: String,
    pub task: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct HealthResponse {
    pub status: String,
    pub agents: u32,
    pub timestamp: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct AgentDiscovery {
    pub name: String,
    pub version: String,
    pub description: String,
    pub agents: Vec<String>,
    pub protocols: Vec<String>,
}

pub struct A2AClient {
    base_url: String,
    client: Client,
}

impl A2AClient {
    pub fn new(base_url: &str) -> Self {
        Self {
            base_url: base_url.to_string(),
            client: Client::new(),
        }
    }

    pub async fn health(&self) -> Result<HealthResponse, Box<dyn std::error::Error>> {
        let url = format!("{}/health", self.base_url);
        let response = self.client.get(&url).send().await?;
        Ok(response.json().await?)
    }

    pub async fn discover_agents(&self) -> Result<AgentDiscovery, Box<dyn std::error::Error>> {
        let url = format!("{}/.well-known/agent.json", self.base_url);
        let response = self.client.get(&url).send().await?;
        Ok(response.json().await?)
    }

    pub async fn chat(&self, task: &str) -> Result<ChatResponse, Box<dyn std::error::Error>> {
        let url = format!("{}/v1/chat", self.base_url);
        let request = ChatRequest { task: task.to_string() };
        let response = self.client.post(&url).json(&request).send().await?;
        Ok(response.json().await?)
    }

    pub async fn message(&self, agent: &str, task: &str) -> Result<ChatResponse, Box<dyn std::error::Error>> {
        let url = format!("{}/v1/message/{}", self.base_url, agent);
        let request = ChatRequest { task: task.to_string() };
        let response = self.client.post(&url).json(&request).send().await?;
        Ok(response.json().await?)
    }
}
