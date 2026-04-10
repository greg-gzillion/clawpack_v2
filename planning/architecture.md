# Clawpack V2 Architecture

## Core Loop
`clawpack.py` → routes/ → agents/ → shared/ → output

## Agent Structure
- Each agent in `agents/{name}/{name}.py`
- Commands in `agents/{name}/commands/*.py`
- Routes in `routes/{name}_routes.py`

## Shared Services
- `shared/memory/` - Persistent memory
- `shared/hooks/` - Lifecycle hooks
- `shared/permissions.py` - Security
