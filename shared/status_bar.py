# shared/status_bar.py - Persistent accessibility status for all agents

def get_status_line():
    '''Returns a one-line status bar showing active accessibility toggles.'''
    try:
        from shared.voice_hook import is_active, is_braille_active, is_neuralink_active, is_eye_tracker_active
        parts = []
        if is_active():
            parts.append('VOICE ON')
        if is_braille_active():
            parts.append('BRAILLE ON')
        if is_neuralink_active():
            parts.append('NEURALINK ON')
        if is_eye_tracker_active():
            parts.append('EYE ON')
        if parts:
            return ' | '.join(parts)
        return ''
    except:
        return ''

def wrap_result_with_status(result_text):
    '''Append status bar to agent response if accessibility toggles are active.'''
    status = get_status_line()
    if status:
        return f"{result_text}\n\n{'='*40}\n{status}\n{'='*40}"
    return result_text

print('shared/status_bar.py created')
