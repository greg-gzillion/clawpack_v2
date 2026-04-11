//! CrustyClaw - Modular Rust AI Assistant for Clawpack v2
//!
//! Features:
//! - A2A protocol client for agent communication
//! - Procedural memory with confidence decay
//! - Trauma guard for safety
//! - Ollama integration for local AI

pub mod a2a;
pub mod memory;
pub mod security;
pub mod llm;
pub mod commands;
pub mod core;

pub use a2a::A2AClient;
pub use memory::ProceduralMemory;
pub use security::TraumaGuard;
pub use llm::OllamaClient;

/// Version of CrustyClaw
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
