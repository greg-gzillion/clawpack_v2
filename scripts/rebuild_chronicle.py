import os
import sys
sys.path.insert(0, r'C:\Users\greg\dev\clawpack_v2')

print('🦞 Rebuilding Chronicle Index...')
print('=' * 50)

# 1. Rebuild webclaw search index
try:
    from agents.webclaw.providers.webclaw_provider import WebclawProvider
    provider = WebclawProvider()
    provider.build_index()
    stats = provider.get_stats()
    print(f'✅ Webclaw index rebuilt: {stats}')
except Exception as e:
    print(f'⚠️ Webclaw index rebuild: {e}')

# 2. Initialize chronicle ledger
try:
    from agents.webclaw.core.chronicle_ledger import ChronicleLedger
    ledger = ChronicleLedger()
    print(f'✅ Chronicle ledger ready: {len(ledger.entries) if hasattr(ledger, "entries") else 0} entries')
except Exception as e:
    print(f'⚠️ Chronicle ledger: {e}')

# 3. Check Common Chronicle reference
chronicle_ref = r'C:\Users\greg\dev\clawpack_v2\references\common_chronicle'
if os.path.exists(chronicle_ref):
    print(f'✅ Common Chronicle reference available')
    sys.path.insert(0, chronicle_ref)
else:
    print('⚠️ Common Chronicle reference not found')

print('=' * 50)
print('🎉 Chronicle system ready!')
