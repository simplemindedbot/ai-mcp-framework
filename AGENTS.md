# Repository Guidelines

## Project Structure & Module Organization
Core directives and safety runbooks sit in `framework/`, stored as versioned `.json` and `.txt` assets grouped by behavior. Automation lives in `tools/`; treat each script as a CLI entry point with explicit flags. `docs/` captures architecture and implementation guides, `examples/` contains MCP configs and knowledge graph exports for smoke tests, and `research-paper/` houses background material for deeper documentation work.

## Build, Test, and Development Commands
- `python tools/deploy-smart-framework.py --interactive` backs up discovered Claude configs, then installs the token-optimized directives.
- `python tools/framework-installer.py --dry-run` checks prerequisites and prints planned actions; drop the flag to apply changes.
- `python tools/knowledge-graph-importer.py --output tmp/framework-import.json` rebuilds MCP import packages so you can review them before uploading.
- `python -m json.tool framework/authenticity-controls.json` keeps configs valid; repeat for every JSON artifact you touch.

## Coding Style & Naming Conventions
Target Python 3.8+, keep four-space indentation, and write docstrings that describe behavior. Use type hints for public functions, snake_case for modules and functions, and CamelCase only for classes. JSON keys stay lowercase with underscores and files remain two-space indented.

## Testing Guidelines
Run touched CLIs with `--help` or `--dry-run` to confirm argument wiring before deployment. Regenerate knowledge graph exports and open them to verify serialization. When you add directives, place representative scenarios in `examples/` and note manual verification steps in `docs/implementation-guide.md`; integration runs against live MCP servers should include saved logs.

## Commit & Pull Request Guidelines
Follow the repository history: imperative subject line, blank line, then concise bullet points covering rationale and risk. Branches use prefixes like `feature/` or `bugfix/` plus a scoped description. Pull requests link issues, summarize testing evidence, attach screenshots or command output when workflows change, and call out any edits to Claude configuration files.

## Agent-Specific Tips
Keep authenticity markers (`🔍 VERIFIED`, `⚠️ ASSUMED`) aligned with `framework/authenticity-controls.json` so downstream agents render accurate cues. Update `CLAUDE.md` and `GEMINI.md` peers whenever directive semantics shift. Ensure automation scripts respect home-directory boundaries and document new flags in script-level help text.
