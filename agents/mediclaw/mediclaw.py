"""Mediclaw AI Agent - Entry Point"""

from cli.interface import MediclawCLI

if __name__ == "__main__":
    cli = MediclawCLI()
    cli.run()
