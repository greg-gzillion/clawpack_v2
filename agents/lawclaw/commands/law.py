def run(args):
    """Get legal information - prioritizes case law and practical content"""
    if not args:
        return "Usage: /law <topic>\nExample: /law contract"
    
    import subprocess
    import sys
    from pathlib import Path
    
    topic = args.lower().strip()
    
    # Map to better sources
    topic_map = {
        'contract': 'contract',
        'contracts': 'contract',
        'breach': 'contract',
        'tort': 'torts',
        'property': 'property',
        'criminal': 'criminal',
        'family': 'family',
    }
    
    dir_name = topic_map.get(topic, topic)
    
    # Use webclaw to get content
    webclaw = Path(__file__).parent.parent.parent / "webclaw" / "webclaw.py"
    
    if not webclaw.exists():
        return "❌ Webclaw not found"
    
    # Get material from webclaw
    result = subprocess.run(
        [sys.executable, str(webclaw), "material", dir_name],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.stdout:
        # Clean up the output
        output = result.stdout.strip()
        # Remove excessive navigation text
        lines = output.split('\n')
        cleaned = []
        skip_next = False
        for line in lines:
            if 'Skip to content' in line or 'Search this site' in line:
                continue
            if len(line) > 200 and line.count(' ') > 30:
                continue
            cleaned.append(line)
        return '\n'.join(cleaned[:100])  # First 100 lines
    else:
        return f"Use AI: /ask What is {topic} law?"
