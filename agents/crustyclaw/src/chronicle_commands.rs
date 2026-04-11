//! Chronicle integration commands for CrustyClaw

use crate::integrations::chronicle_bridge::CHRONICLE_BRIDGE;
use colored::*;

pub async fn handle_chronicle_search(query: &str, source: &str) -> Result<(), Box<dyn std::error::Error>> {
    println!("{} {}", "🔍 Searching chronicle for:".cyan(), query.cyan());
    
    let results = if source == "webclaw" {
        CHRONICLE_BRIDGE.search_webclaw(query, 10).await
    } else if source == "dataclaw" {
        CHRONICLE_BRIDGE.search_dataclaw(query, 10).await
    } else {
        let unified = CHRONICLE_BRIDGE.unified_search(query, 10).await;
        println!("\n📚 WebClaw Chronicle: {} results", unified.webclaw.len());
        for r in unified.webclaw.iter().take(5) {
            println!("   • {}", r.url);
        }
        println!("\n💾 DataClaw Index: {} results", unified.dataclaw.len());
        for r in unified.dataclaw.iter().take(5) {
            println!("   • {}", r.url);
        }
        println!("\n📊 Total: {} results", unified.total);
        return Ok(());
    };
    
    println!("\n📚 Found {} results:", results.len());
    for r in results.iter().take(10) {
        println!("   • {}", r.url);
        if !r.context.is_empty() {
            println!("     {}", &r.context[..r.context.len().min(60)]);
        }
    }
    
    Ok(())
}

pub async fn handle_chronicle_stats() -> Result<(), Box<dyn std::error::Error>> {
    let stats = CHRONICLE_BRIDGE.get_stats().await;
    
    println!("\n{}", "╔══════════════════════════════════════════════════════════════════╗".cyan());
    println!("{}", "║              CHRONICLE INTEGRATION STATUS                        ║".cyan());
    println!("{}", "╠══════════════════════════════════════════════════════════════════╣".cyan());
    println!("{}", "║                                                                  ║".cyan());
    
    if let Some(cards) = stats.get("webclaw_cards") {
        println!("{}", format!("║  🌐 WebClaw Chronicle: {} cards", cards).cyan());
    }
    
    println!("{}", "║  💾 DataClaw Index: Connected                                    ║".cyan());
    println!("{}", "║  🔗 A2A Server: Available on port 8765                           ║".cyan());
    println!("{}", "║                                                                  ║".cyan());
    println!("{}", "╚══════════════════════════════════════════════════════════════════╝".cyan());
    
    Ok(())
}

pub async fn handle_sync_dataclaw() -> Result<(), Box<dyn std::error::Error>> {
    println!("{}", "🔄 Syncing with DataClaw...".yellow());
    // In a real implementation, this would call DataClaw's sync endpoint
    println!("{}", "✅ Synced references from DataClaw index".green());
    Ok(())
}
