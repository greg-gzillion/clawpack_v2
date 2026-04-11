//! CrustyClaw - Main CLI Entry Point

use clap::{Parser, Subcommand};
use crustyclaw::{A2AClient, ProceduralMemory, TraumaGuard, OllamaClient};

#[derive(Parser)]
#[command(name = "crustyclaw")]
#[command(version = "2.0.0")]
#[command(about = "🦞 Fast, memory-safe Rust AI assistant for Clawpack v2", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Connect to Clawpack A2A server
    A2a {
        #[arg(short, long, default_value = "http://127.0.0.1:8765")]
        url: String,
        #[command(subcommand)]
        action: A2aAction,
    },
    /// Manage procedural memory
    Memory {
        #[command(subcommand)]
        action: MemoryAction,
    },
    /// Check command safety
    Safety {
        command: String,
    },
    /// Ask AI a question
    Ask {
        question: String,
    },
    /// Interactive shell
    Shell,
    /// Show system status
    Status,
}

#[derive(Subcommand)]
enum A2aAction {
    Health,
    Agents,
    Chat { task: String },
    Message { agent: String, task: String },
}

#[derive(Subcommand)]
enum MemoryAction {
    Add { content: String, category: String },
    List,
    Feedback { id: String, helpful: bool },
    Relevant { task: String, limit: Option<usize> },
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();
    let cli = Cli::parse();

    match cli.command {
        Commands::A2a { url, action } => {
            let client = A2AClient::new(&url);
            match action {
                A2aAction::Health => {
                    match client.health().await {
                        Ok(health) => println!("✅ Clawpack A2A: {}", health.status),
                        Err(e) => println!("❌ Error: {}", e),
                    }
                }
                A2aAction::Agents => {
                    match client.discover_agents().await {
                        Ok(discovery) => {
                            println!("🤖 Available agents: {:?}", discovery.agents);
                        }
                        Err(e) => println!("❌ Error: {}", e),
                    }
                }
                A2aAction::Chat { task } => {
                    match client.chat(&task).await {
                        Ok(resp) => println!("🦞 Routed to {}: {}", resp.agent, resp.message),
                        Err(e) => println!("❌ Error: {}", e),
                    }
                }
                A2aAction::Message { agent, task } => {
                    match client.message(&agent, &task).await {
                        Ok(resp) => println!("📨 {} response: {}", resp.agent, resp.message),
                        Err(e) => println!("❌ Error: {}", e),
                    }
                }
            }
        }
        Commands::Memory { action } => {
            let mut memory = ProceduralMemory::new(".crustyclaw");
            match action {
                MemoryAction::Add { content, category } => {
                    let id = memory.add_rule(content, category);
                    println!("✅ Added rule: {}", id);
                }
                MemoryAction::List => {
                    println!("📚 Memory rules:");
                    // List implementation
                }
                MemoryAction::Feedback { id, helpful } => {
                    memory.record_feedback(&id, helpful);
                    println!("✅ Feedback recorded for {}", id);
                }
                MemoryAction::Relevant { task, limit } => {
                    let limit = limit.unwrap_or(5);
                    let rules = memory.get_relevant_rules(&task, limit);
                    println!("📋 Relevant rules for '{}':", task);
                    for rule in rules {
                        println!("  • {} (maturity: {:?})", rule.content, rule.maturity);
                    }
                }
            }
        }
        Commands::Safety { command } => {
            let mut guard = TraumaGuard::new();
            guard.enable();
            let result = guard.check(&command);
            if result.blocked {
                println!("⛔ BLOCKED: {}", result.reason.unwrap());
                println!("   Severity: {}", result.severity.unwrap());
            } else {
                println!("✅ Safe command");
            }
        }
        Commands::Ask { question } => {
            println!("🤔 Asking: {}", question);
            println!("💡 (Ollama integration coming soon)");
        }
        Commands::Shell => {
            println!("🦞 CrustyClaw Interactive Shell");
            println!("Type 'help' for commands, 'exit' to quit");
            // Shell implementation
        }
        Commands::Status => {
            println!("🦞 CrustyClaw v2.0.0");
            println!("Features:");
            println!("  ✅ A2A Client");
            println!("  ✅ Procedural Memory");
            println!("  ✅ Trauma Guard");
            println!("  ⏳ Ollama Integration (coming)");
        }
    }

    Ok(())
}

mod chronicle_commands;
use chronicle_commands::{handle_chronicle_search, handle_chronicle_stats, handle_sync_dataclaw};

// Add to existing match statement
// In the command matching section, add:

// chronicle search <query> [source]
// chronicle stats
// sync-dataclaw
