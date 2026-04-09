"""Emergency Medicine Protocols"""

EMERGENCY_PROTOCOLS = {
    "cardiac_arrest": ["call_emergency", "cpr", "defibrillation", "advanced_cardiac_life_support"],
    "stroke": ["fast_test", "call_emergency", "time_of_onset", "do_not_give_aspirin"],
    "anaphylaxis": ["epinephrine", "call_emergency", "lay_flat", "elevate_legs"],
    "seizure": ["protect_from_injury", "time_seizure", "recovery_position", "call_if_prolonged"],
    "bleeding": ["direct_pressure", "elevate", "tourniquet_if_severe", "call_emergency"],
    "choking": ["heimlich_maneuver", "back_blows", "chest_thrusts", "call_emergency"],
    "burns": ["cool_water", "cover_burn", "do_not_apply_ice", "seek_care"],
    "fracture": ["immobilize", "ice", "elevate", "pain_management"]
}

class EmergencyProtocols:
    @staticmethod
    def get_protocol(emergency: str):
        return EMERGENCY_PROTOCOLS.get(emergency.lower().replace(" ", "_"), [])
    
    @staticmethod
    def list_emergencies():
        return list(EMERGENCY_PROTOCOLS.keys())
