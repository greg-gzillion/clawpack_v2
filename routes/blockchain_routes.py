"""Txclaw routing"""
class BlockchainRoutes:
    commands = ['tx', '/balance', '/send', '/contract']
    agent = 'txclaw'
    
    @staticmethod
    def get_help():
        return """
💰 BLOCKCHAIN:
  /balance <address>        - Check balance
  /send <to> <amount>       - Send transaction
  /contract <address>       - Contract info
"""
