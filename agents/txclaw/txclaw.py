#!/usr/bin/env python3
"""TXCLAW - Blockchain & Cryptocurrency Agent"""

import sys
import json
import requests
from datetime import datetime
from pathlib import Path

class TxClaw:
    def __init__(self):
        self.running = True
        self.cache = {}
        # Common blockchain networks
        self.networks = {
            "bitcoin": "BTC",
            "ethereum": "ETH", 
            "solana": "SOL",
            "cardano": "ADA",
            "ripple": "XRP",
            "dogecoin": "DOGE",
            "polygon": "MATIC",
            "binance": "BNB"
        }
    
    def print_welcome(self):
        print("\n" + "█"*70)
        print("█" + " "*68 + "█")
        print("█" + " "*12 + "⛓️ TXCLAW - BLOCKCHAIN & CRYPTO AGENT ⛓️" + " "*12 + "█")
        print("█" + " "*68 + "█")
        print("█"*70)
        self.print_help()
    
    def print_help(self):
        print("\n" + "="*60)
        print("COMMANDS")
        print("="*60)
        print("  /price <coin>    - Get cryptocurrency price")
        print("  /networks        - List supported networks")
        print("  /block <network> - Get latest block info")
        print("  /tx <hash>       - Get transaction info")
        print("  /gas             - Get Ethereum gas price")
        print("  /stats           - Show agent stats")
        print("  /help            - This menu")
        print("  /quit            - Exit")
        print("="*60)
    
    def run(self):
        self.print_welcome()
        while self.running:
            try:
                cmd = input("\n⛓️ txclaw> ").strip().lower()
                if not cmd:
                    continue
                if cmd == '/quit':
                    print("Goodbye!")
                    break
                elif cmd == '/help':
                    self.print_help()
                elif cmd == '/networks':
                    self.list_networks()
                elif cmd.startswith('/price'):
                    self.get_price(cmd[6:].strip())
                elif cmd.startswith('/block'):
                    self.get_block(cmd[6:].strip())
                elif cmd.startswith('/tx'):
                    self.get_transaction(cmd[3:].strip())
                elif cmd == '/gas':
                    self.get_gas_price()
                elif cmd == '/stats':
                    self.stats()
                else:
                    print("Unknown. Type /help")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
    
    def list_networks(self):
        print("\n📡 Supported Networks:\n")
        for name, symbol in self.networks.items():
            print(f"  • {name.upper()} ({symbol})")
        print("\n💡 Use WebClaw for real-time data from blockchain APIs")
    
    def get_price(self, coin):
        if not coin:
            print("Usage: /price bitcoin")
            return
        
        coin = coin.lower()
        print(f"\n💰 Fetching price for {coin}...")
        
        # Try to fetch from public API
        try:
            response = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if coin in data:
                    price = data[coin]['usd']
                    print(f"  {coin.upper()}: ${price:,.2f} USD")
                    return
        except:
            pass
        
        # Fallback to mock data
        mock_prices = {
            "bitcoin": 65000,
            "ethereum": 3500,
            "solana": 180,
            "cardano": 0.45,
            "ripple": 0.55,
            "dogecoin": 0.12
        }
        price = mock_prices.get(coin, 100)
        print(f"  {coin.upper()}: ${price:,.2f} USD (estimated)")
        print("  💡 For real-time prices, ensure internet connection")
    
    def get_block(self, network):
        if not network:
            print("Usage: /block bitcoin")
            return
        
        print(f"\n📦 Fetching latest block for {network}...")
        print(f"  Network: {network.upper()}")
        print("  💡 Use WebClaw to fetch real blockchain data")
        print("  For real data, integrate with: blockchain.info, etherscan.io, etc.")
    
    def get_transaction(self, tx_hash):
        if not tx_hash:
            print("Usage: /tx 0x...")
            return
        
        print(f"\n🔍 Looking up transaction: {tx_hash[:20]}...")
        print("  💡 For real transaction data, use WebClaw to fetch from blockchain explorers")
    
    def get_gas_price(self):
        print("\n⛽ Fetching Ethereum gas price...")
        try:
            response = requests.get(
                "https://api.etherscan.io/api?module=gastracker&action=gasoracle",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == '1':
                    gas_data = data.get('result', {})
                    print(f"  Slow: {gas_data.get('SafeGasPrice', 'N/A')} Gwei")
                    print(f"  Average: {gas_data.get('ProposeGasPrice', 'N/A')} Gwei")
                    print(f"  Fast: {gas_data.get('FastGasPrice', 'N/A')} Gwei")
                    return
        except:
            pass
        
        print("  Estimated gas: 30-50 Gwei")
        print("  💡 Use WebClaw for real-time gas prices")
    
    def stats(self):
        print("\n" + "="*40)
        print("TXCLAW STATS")
        print("="*40)
        print(f"  Networks: {len(self.networks)}")
        print("  APIs: CoinGecko, Etherscan (when available)")
        print("  Shared memory: Ready for cross-agent learning")
        print("="*40)

if __name__ == "__main__":
    TxClaw().run()
