#!/usr/bin/env python3
"""
AUTOPILOT Framework Deployment Tool

Deploys compiled AUTOPILOT rules to user configuration for immediate use.
Supports multiple AI systems and configuration formats.
"""

import os
import json
import shutil
import argparse
from datetime import datetime
from pathlib import Path

# Common configuration paths for different AI systems
CONFIG_PATHS = {
    "claude": [
        "~/.claude/CLAUDE.md",
        "~/.config/claude/preferences.txt",
        "CLAUDE.md"  # Project-specific
    ],
    "cursor": [
        "~/.cursor/preferences.txt",
        ".cursorrules"
    ],
    "chatgpt": [
        "~/.chatgpt/custom_instructions.txt"
    ],
    "generic": [
        "~/.ai_preferences.txt",
        ".ai_rules.json"
    ]
}

def find_existing_config(system="claude"):
    """Find existing configuration files for the specified AI system."""
    found_configs = []

    for config_path in CONFIG_PATHS.get(system, CONFIG_PATHS["generic"]):
        expanded_path = Path(config_path).expanduser()
        if expanded_path.exists():
            found_configs.append(expanded_path)

    return found_configs

def backup_existing_config(config_path):
    """Create a timestamped backup of existing configuration."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = config_path.with_suffix(f".backup_{timestamp}{config_path.suffix}")
    shutil.copy2(config_path, backup_path)
    return backup_path

def format_for_claude(compiled_rules):
    """Format compiled rules for Claude configuration."""
    output_lines = [
        "# AUTOPILOT Framework - Compiled AI Directives",
        "# Generated automatically - DO NOT EDIT MANUALLY",
        "",
        "Entity Type: autopilot_framework",
        "Priority: Prime Directive (Highest)",
        "Scope: All tasks and operations",
        "Auto-applies to: Every user interaction and task execution",
        f"Compiled: {datetime.now().isoformat()}",
        "",
        "## Core Directives",
        ""
    ]

    # Extract prime directive
    if "prime_directive" in compiled_rules:
        for directive in compiled_rules["prime_directive"]:
            output_lines.append(f"- {directive}")
        output_lines.append("")

    # Add key components as condensed format
    output_lines.extend([
        "## Token Optimization",
        "- Smart Memory Caching: 70-85% query reduction",
        "- Delta Updates: Store only changes, not full state",
        "- Batch Operations: Group memory operations when possible",
        "- Query Deduplication: Never repeat within session",
        "",
        "## Learning Integration",
        "- Immediate Updates: User corrections cached instantly",
        "- Deferred Updates: Batched at natural conversation breaks",
        "- Session Continuity: Cross-session pattern preservation",
        "",
        "## Authenticity Controls",
        "- Self-Audit Questions: Pre-response validation",
        "- Verification Markers: 🔍 VERIFIED vs ⚠️ ASSUMED",
        "- External Verification: For technical claims and assessments",
        "",
        "## Emergency Mode",
        "- Token Budget Critical: Use cached data exclusively",
        "- Defer Updates: Batch all learning updates to session end",
        "- Maintain Quality: Apply learned patterns without real-time validation",
        "",
        f"Framework compiled from {len(compiled_rules.get('_meta', {}).get('source_files', []))} source files"
    ])

    return "\n".join(output_lines)

def format_for_json_config(compiled_rules):
    """Format compiled rules for JSON-based configuration."""
    return {
        "autopilot_framework": {
            "version": compiled_rules.get("_meta", {}).get("compilation_version", "1.0"),
            "compiled_at": compiled_rules.get("_meta", {}).get("compiled_at"),
            "rules": {k: v for k, v in compiled_rules.items() if k != "_meta"},
            "deployment": {
                "priority": "highest",
                "auto_apply": True,
                "scope": "all_interactions"
            }
        }
    }

def deploy_to_config(compiled_rules_path, target_system="claude", target_path=None, format_type="auto"):
    """Deploy compiled rules to target AI system configuration."""

    # Load compiled rules
    with open(compiled_rules_path, 'r') as f:
        compiled_rules = json.load(f)

    # Determine target path
    if target_path:
        config_path = Path(target_path).expanduser()
    else:
        # Find existing config or use default
        existing_configs = find_existing_config(target_system)
        if existing_configs:
            config_path = existing_configs[0]
        else:
            # Use default path for system
            default_path = CONFIG_PATHS[target_system][0]
            config_path = Path(default_path).expanduser()

    # Create directories if needed
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Backup existing config
    backup_path = None
    if config_path.exists():
        backup_path = backup_existing_config(config_path)

    # Determine format
    if format_type == "auto":
        if config_path.suffix.lower() in ['.json']:
            format_type = "json"
        else:
            format_type = "markdown"

    # Format and write
    if format_type == "json":
        formatted_content = json.dumps(
            format_for_json_config(compiled_rules),
            indent=2
        )
    else:
        formatted_content = format_for_claude(compiled_rules)

    # Write to target
    with open(config_path, 'w') as f:
        f.write(formatted_content)

    return {
        "target_path": config_path,
        "backup_path": backup_path,
        "format": format_type,
        "rules_count": len([k for k in compiled_rules.keys() if k != "_meta"]),
        "source_files": compiled_rules.get("_meta", {}).get("source_files", [])
    }

def validate_deployment(config_path):
    """Validate that deployment was successful."""
    if not config_path.exists():
        return False, "Configuration file does not exist"

    try:
        content = config_path.read_text()
        if "autopilot" in content.lower() or "prime_directive" in content.lower():
            return True, "AUTOPILOT framework detected in configuration"
        else:
            return False, "AUTOPILOT framework not found in configuration"
    except Exception as e:
        return False, f"Error reading configuration: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Deploy compiled AUTOPILOT framework to AI system configuration"
    )

    parser.add_argument(
        "--compiled-rules",
        default="framework/autopilot-rules.json",
        help="Path to compiled AUTOPILOT rules"
    )

    parser.add_argument(
        "--system",
        choices=["claude", "cursor", "chatgpt", "generic"],
        default="claude",
        help="Target AI system"
    )

    parser.add_argument(
        "--target",
        help="Specific target configuration path"
    )

    parser.add_argument(
        "--format",
        choices=["auto", "markdown", "json"],
        default="auto",
        help="Output format"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deployed without making changes"
    )

    parser.add_argument(
        "--list-configs",
        action="store_true",
        help="List existing configuration files"
    )

    args = parser.parse_args()

    if args.list_configs:
        print(f"🔍 Searching for {args.system} configuration files...")
        configs = find_existing_config(args.system)
        if configs:
            for config in configs:
                print(f"  ✅ {config}")
        else:
            print(f"  ❌ No existing configurations found for {args.system}")
            print(f"  📝 Will create new config at: {CONFIG_PATHS[args.system][0]}")
        return

    # Check compiled rules exist
    compiled_path = Path(args.compiled_rules)
    if not compiled_path.exists():
        print(f"❌ Compiled rules not found: {compiled_path}")
        print("Run: python tools/framework_compiler.py")
        return 1

    print(f"🚀 Deploying AUTOPILOT framework to {args.system}")
    print(f"📦 Source: {compiled_path}")

    if args.dry_run:
        print("🔍 DRY RUN - No changes will be made")

        # Show what would be deployed
        with open(compiled_path, 'r') as f:
            compiled_rules = json.load(f)

        print(f"📊 Rules to deploy: {len([k for k in compiled_rules.keys() if k != '_meta'])}")
        print(f"📁 Source files: {len(compiled_rules.get('_meta', {}).get('source_files', []))}")

        # Show target path
        if args.target:
            target_path = Path(args.target).expanduser()
        else:
            existing_configs = find_existing_config(args.system)
            target_path = existing_configs[0] if existing_configs else Path(CONFIG_PATHS[args.system][0]).expanduser()

        print(f"🎯 Target: {target_path}")
        print(f"📝 Format: {args.format}")

        return 0

    try:
        result = deploy_to_config(
            compiled_path,
            args.system,
            args.target,
            args.format
        )

        print(f"✅ Successfully deployed to: {result['target_path']}")
        print(f"📦 Format: {result['format']}")
        print(f"🔧 Rules deployed: {result['rules_count']}")
        print(f"📁 Source files: {len(result['source_files'])}")

        if result['backup_path']:
            print(f"💾 Backup created: {result['backup_path']}")

        # Validate deployment
        is_valid, message = validate_deployment(result['target_path'])
        if is_valid:
            print(f"✅ Validation: {message}")
        else:
            print(f"⚠️  Validation: {message}")

        print(f"\n🎯 AUTOPILOT framework is now active!")
        print(f"🚀 Start your AI session to see token-optimized behavior")

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())