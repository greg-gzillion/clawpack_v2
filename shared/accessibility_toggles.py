_braille_active = False

_neuralink_active = False

_eye_active = False



def toggle_braille():

    global _braille_active

    _braille_active = not _braille_active

    return _braille_active



def toggle_neuralink():

    global _neuralink_active

    _neuralink_active = not _neuralink_active

    return _neuralink_active



def toggle_eye():

    global _eye_active

    _eye_active = not _eye_active

    return _eye_active



def is_braille_active():

    return _braille_active

def is_neuralink_active():

    return _neuralink_active

def is_eye_active():

    return _eye_active



def get_active():

    active = []

    if _braille_active: active.append('BRAILLE')

    if _neuralink_active: active.append('NEURALINK')

    if _eye_active: active.append('EYE')

    return active



def status():

    parts = get_active()

    if not parts:

        return 'Accessibility toggles: none active. Use /access voice|braille|neuralink|eye on|off'

    return 'Active: ' + ' | '.join(parts)

