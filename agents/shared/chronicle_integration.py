# chronicle_integration.py
# Bridge between Clawpack and Common Chronicle

import sys
from pathlib import Path

# Path to Common Chronicle submodule
CHRONICLE_PATH = Path(__file__).parent.parent / 'references' / 'common_chronicle'

def init_chronicle():
    '''Initialize Common Chronicle features if available'''
    if CHRONICLE_PATH.exists():
        sys.path.insert(0, str(CHRONICLE_PATH))
        
        try:
            # Try different possible import paths
            from app.services import timeline_service
            from app.services import event_service
            
            return {
                'available': True,
                'timeline_service': timeline_service,
                'event_service': event_service,
                'path': str(CHRONICLE_PATH)
            }
        except ImportError as e:
            return {'available': False, 'error': str(e)}
    
    return {'available': False, 'error': 'Common Chronicle not found'}

if __name__ == '__main__':
    result = init_chronicle()
    if result['available']:
        print(f"✅ Common Chronicle loaded from {result['path']}")
    else:
        print(f"⚠️ Common Chronicle not available: {result.get('error')}")
