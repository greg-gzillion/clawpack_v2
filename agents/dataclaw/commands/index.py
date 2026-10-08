"""index command - Rebuild DataClaw local search index."""
name = "/reindex"


def run(args: str, agent=None) -> str:
    """Rebuild the DataClaw file index.

    Triggers a rebuild of agents/dataclaw/references/data_index.db.
    Takes ~30 seconds for the full corpus. Run after adding files to
    references/, docs/, data/, or exports/.
    """
    import subprocess
    from pathlib import Path

    project_root = Path(__file__).resolve().parent.parent.parent.parent
    script = project_root / "scripts" / "rebuild_data_index.py"

    if not script.exists():
        return (
            "Reindex: script not found at scripts/rebuild_data_index.py\n"
            "Expected a rebuild script at that path."
        )

    try:
        result = subprocess.run(
            ["python", str(script)],
            cwd=str(project_root),
            capture_output=True,
            text=True,
            timeout=600,
        )
        output = result.stdout[-2000:] if result.stdout else ""
        if result.returncode == 0:
            return f"Reindex complete.\n\n{output}"
        return f"Reindex failed (exit {result.returncode}).\n\n{output}"
    except subprocess.TimeoutExpired:
        return "Reindex timed out after 10 minutes."
    except Exception as e:
        return f"Reindex error: {e}"
