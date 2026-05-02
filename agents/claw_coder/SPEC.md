# ClawCoder Constitutional Payload Spec v1.0

> Law. Not suggestion. The contract between agents and the code engine.

## Canonical Payload

{
  "type": "code",
  "intent": "generate_code",
  "task_type": "code_generation",
  "confidence": 1.0,
  "source": "user",
  "language": "python",
  "query": "async web scraper with error handling",
  "flags": {
    "validate": true,
    "scan": false,
    "save": true
  }
}

## Command Types

code, explain, debug, review, tutorial, translate, run, test, scan, docs, project, deps, perf, delegate

## 39 Languages

python, rust, go, javascript, typescript, java, c, cpp, csharp, ruby, php, swift, kotlin, scala, r, julia, lua, perl, haskell, clojure, elixir, erlang, dart, bash, powershell, sql, html, css, yaml, json, xml, assembly, fortran, cobol, groovy, nim, zig, matlab, makefile

## Agent Integration

result = call_agent("claw_coder", {
    "type": "code",
    "language": "rust",
    "query": "async TCP server with tokio",
    "flags": {"validate": true, "save": true}
})

Version 1.0 - Frozen.
