# shared/constitutional_command.py
"""
Constitutional Command Wrapper — enforces lifecycle participation automatically.

Every command decorated with @constitutional_command gets:
  PRE:  recall_prior() — surface relevant memory
  POST: remember() — persist to UnifiedMemory
        learn_fact() — extract learnings
        auto_delegate() — offer cross-agent actions
        decision_ledger.record() — tamper-evident audit trail

Usage:
    from shared.constitutional_command import constitutional_command

    @constitutional_command(agent="lawclaw", source_type="web_verified")
    def run(args):
        ...
        return result_string

The wrapper handles all constitutional phases. The command function
only needs to implement its domain logic and return a result string.
"""
from functools import wraps
from typing import Callable, Optional


def constitutional_command(
    agent: str = "lawclaw",
    command_name: Optional[str] = None,
    source_type: str = "web_verified",
    confidence: float = 0.85,
):
    """
    Decorator that wraps a command function in the constitutional lifecycle.

    Args:
        agent: Agent name for logging and memory attribution
        command_name: Override for the command name (defaults to function's `name` variable)
        source_type: Source type for memory writes (web_verified, chronicle, memory)
        confidence: Confidence score for memory writes (must be >= 0.75 for memory_guard)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(args):
            # Resolve command name from the module if not provided
            cmd_name = command_name
            if cmd_name is None:
                cmd_name = getattr(func, '__module__', '').split('.')[-1] or func.__name__

            # ── PHASE 1: RECALL ────────────────────────────────────
            # Surface prior knowledge from unified memory before execution
            recalled = []
            try:
                from shared._agent_helpers import recall_memory
                recalled = recall_memory(agent, args, limit=3)
            except Exception:
                pass  # recall failure must not block execution

            # ── PHASE 2: REASON ────────────────────────────────────
            # Execute the actual command logic
            result = func(args)

            # ── POST-EXECUTION PHASES ──────────────────────────────
            if result and isinstance(result, str) and len(result) > 20:
                # ── PHASE 4: MEMORY WRITE ──────────────────────────
                try:
                    from agents.lawclaw.commands._memory import remember
                    remember(
                        command=f"/{cmd_name}",
                        query=args,
                        result_summary=result[:400],
                        source_type=source_type,
                        confidence=confidence,
                    )
                except Exception:
                    pass

                # ── PHASE 5: DELEGATION SURFACE ────────────────────
                # Note: auto_delegate modifies output in-place if passed a list
                # For the decorator pattern, we append delegation offers to the result
                try:
                    from shared._agent_helpers import delegate as _delegate_check
                    delegation_offers = []
                    if len(result) > 300:
                        delegation_offers.append(
                            f"  delegate docuclaw — export as document"
                        )
                    if "court" in args.lower() or "jurisdiction" in args.lower():
                        delegation_offers.append(
                            f"  delegate draftclaw — building permit lookup"
                        )
                    if delegation_offers:
                        result += "\n\n  Cross-agent actions (Ctrl+Click):\n"
                        result += "\n".join(delegation_offers)
                except Exception:
                    pass

                # ── PHASE 6: LEARNING ──────────────────────────────
                try:
                    from shared._agent_helpers import learn
                    learn(agent, args, result[:500], source_type, confidence)
                except Exception:
                    pass

                # ── PHASE 7: DECISION LEDGER ───────────────────────
                try:
                    from shared.decision_ledger import get_ledger
                    ledger = get_ledger()
                    ledger.record(
                        agent=agent,
                        action=f"/{cmd_name}",
                        query=args[:200],
                        result=result[:100],
                        source=source_type,
                    )
                except Exception:
                    pass

            return result

        return wrapper
    return decorator