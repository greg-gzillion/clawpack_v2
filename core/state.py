"""Two-tier state: infrastructure (mutable) + UI (reactive)"""

# TIER 1: Infrastructure state - mutable singleton, no reactivity
class InfrastructureState:
    """~80 fields: session config, cost tracking, telemetry"""
    def __init__(self):
        self.session_id = None
        self.working_dir = None
        self.model = "llama3.2:3b"
        self.provider = "ollama"
        self.cost_total = 0.0
        self.tokens_used = 0
        self.telemetry = {}
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

STATE = InfrastructureState()  # Global singleton, mutated directly

# TIER 2: UI state - reactive (Zustand-like)
class ReactiveStore:
    """Minimal reactive store for UI state"""
    def __init__(self):
        self._listeners = []
        self._state = {
            'messages': [],
            'input_mode': 'command',
            'tool_approvals': [],
            'progress': None,
            'is_processing': False
        }
    
    def get(self, key):
        return self._state.get(key)
    
    def set(self, key, value):
        self._state[key] = value
        self._notify(key, value)
    
    def subscribe(self, callback):
        self._listeners.append(callback)
    
    def _notify(self, key, value):
        for listener in self._listeners:
            listener(key, value)

UI_STATE = ReactiveStore()
