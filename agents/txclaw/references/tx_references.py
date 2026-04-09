"""TX Blockchain Reference Data"""

# TX Blockchain official resources
TX_OFFICIAL_URLS = {
    "mainnet": "https://tx.org",
    "explorer": "https://explorer.tx.org",
    "docs": "https://docs.tx.org",
    "github": "https://github.com/tx-org",
    "status": "https://status.tx.org",
}

# TX Blockchain APIs
TX_API_URLS = {
    "rpc": "https://rpc.tx.org",
    "rest": "https://api.tx.org",
    "websocket": "wss://ws.tx.org",
}

# TX Ecosystem
TX_ECOSYSTEM_URLS = {
    "staking": "https://staking.tx.org",
    "governance": "https://gov.tx.org",
    "tokens": "https://tokens.tx.org",
    "dapps": "https://dapps.tx.org",
}

# TX Analytics
TX_ANALYTICS_URLS = {
    "stats": "https://stats.tx.org",
    "validators": "https://validators.tx.org",
    "transactions": "https://tx.tx.org",
}

# TX Community
TX_COMMUNITY_URLS = {
    "discord": "https://discord.gg/tx",
    "telegram": "https://t.me/tx_blockchain",
    "twitter": "https://twitter.com/tx_blockchain",
    "forum": "https://forum.tx.org",
}

# TX Development
TX_DEV_URLS = {
    "sdk": "https://docs.tx.org/sdk",
    "cli": "https://github.com/tx-org/cli",
    "testnet_faucet": "https://faucet.tx.org",
    "contract_verifier": "https://verify.tx.org",
}

def get_all_urls() -> dict:
    """Get all TX blockchain URLs"""
    return {
        **TX_OFFICIAL_URLS,
        **TX_API_URLS,
        **TX_ECOSYSTEM_URLS,
        **TX_ANALYTICS_URLS,
        **TX_COMMUNITY_URLS,
        **TX_DEV_URLS,
    }

def get_source_count() -> int:
    """Get total number of reference sources"""
    return len(get_all_urls())

def get_source_list() -> list:
    """Get list of all source names"""
    return list(get_all_urls().keys())
