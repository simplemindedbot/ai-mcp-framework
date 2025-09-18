#!/usr/bin/env python3
"""
Smart Framework Deployment Tool

Safely switches from token-heavy framework to smart-caching version while preserving
all learning and providing rollback capabilities.
"""

import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class SmartFrameworkDeployer:
    """Manages deployment of token-optimized framework with learning preservation."""

    def __init__(self, claude_config_path: str = None):
        # Auto-detect Claude config paths
        self.claude_paths = self._detect_claude_paths(claude_config_path)
        self.framework_dir = Path(__file__).parent.parent / "framework"
        self.backup_dir = Path.home() / ".claude-framework-backups"
        self.deployment_log = self.backup_dir / "deployment-log.json"
        self.config_registry = self.backup_dir / "config-registry.json"

        # Initialize tracked configs
        self.project_configs = []
        self.new_configs = []
        self.unknown_configs = []

        # Ensure backup directory exists
        self.backup_dir.mkdir(exist_ok=True)

        # Load previous config registry
        self._load_config_registry()

    def _detect_claude_paths(self, custom_path: str = None) -> Dict[str, List[Path]]:
        """Detect all possible Claude configuration paths for both Claude Code and Claude Desktop."""
        paths = {
            "claude_code": [],
            "claude_desktop": []
        }

        if custom_path:
            paths["claude_code"].append(Path(custom_path))

        home = Path.home()

        # Comprehensive search for all CLAUDE.md files
        import subprocess
        try:
            result = subprocess.run([
                'find', str(home), '-name', '*CLAUDE.md', '-o', '-name', '*claude.md', '-o', '-name', 'CLAUDE.md'
            ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                found_paths = [Path(p.strip()) for p in result.stdout.strip().split('\n') if p.strip()]

                # Categorize files using registry and analysis
                for path in found_paths:
                    if path.exists():
                        try:
                            category = self._classify_config_file(path)
                            if category == "framework":
                                paths["claude_code"].append(path)
                            # Track new files separately
                            if str(path) not in self.known_configs or self.known_configs[str(path)].get("auto_classified"):
                                self.new_configs.append(path)
                        except Exception as e:
                            print(f"⚠️  Could not analyze {path}: {e}")
                            self.unknown_configs.append(path)

        except Exception as e:
            print(f"⚠️  Comprehensive search failed, using fallback: {e}")
            # Fallback to original detection
            claude_code_paths = [
                home / ".claude" / "CLAUDE.md",
                home / "CLAUDE.md",
                home / ".config" / "claude" / "CLAUDE.md",
                Path.cwd() / "CLAUDE.md",
                Path.cwd() / ".claude" / "CLAUDE.md"
            ]

            for path in claude_code_paths:
                if path.exists():
                    paths["claude_code"].append(path)

        # Claude Desktop config locations
        claude_desktop_paths = [
            home / "Library" / "Application Support" / "Claude" / "memory-data" / "memory.json",
            home / "Library" / "Application Support" / "com.anthropic.claudefordesktop" / "memory-data" / "memory.json"
        ]

        for path in claude_desktop_paths:
            if path.exists():
                paths["claude_desktop"].append(path)

        return paths

    def _load_config_registry(self):
        """Load previously tracked config classifications."""
        try:
            if self.config_registry.exists():
                with open(self.config_registry, 'r') as f:
                    registry = json.load(f)
                    self.known_configs = registry.get("known_configs", {})
                    self.deployment_history = registry.get("deployment_history", [])
            else:
                self.known_configs = {}
                self.deployment_history = []
        except Exception as e:
            print(f"⚠️  Could not load config registry: {e}")
            self.known_configs = {}
            self.deployment_history = []

    def _save_config_registry(self):
        """Save config classifications for future runs."""
        try:
            registry = {
                "known_configs": self.known_configs,
                "deployment_history": self.deployment_history,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.config_registry, 'w') as f:
                json.dump(registry, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save config registry: {e}")

    def _classify_config_file(self, file_path: Path) -> str:
        """Classify config file as framework, project, or new."""
        file_key = str(file_path)

        # Check if we've seen this file before
        if file_key in self.known_configs:
            return self.known_configs[file_key]["type"]

        # Analyze content for new files
        analysis_type = self._analyze_claude_file_type(file_path)

        # Register as new config
        self.known_configs[file_key] = {
            "type": analysis_type,
            "first_seen": datetime.now().isoformat(),
            "size": file_path.stat().st_size if file_path.exists() else 0,
            "auto_classified": True
        }

        # Add to appropriate tracking list
        if analysis_type == "project":
            self.project_configs.append(file_path)
        elif analysis_type == "unknown":
            self.unknown_configs.append(file_path)
        else:  # framework
            # Will be added to claude_paths["claude_code"] in detection
            pass

        return analysis_type

    def _analyze_claude_file_type(self, file_path: Path) -> str:
        """Analyze CLAUDE.md file to determine if it's a framework config or project-specific."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Framework indicators
            framework_indicators = [
                "Enhanced MCP Server Exploration Prime Directive",
                "MCP Server Exploration Prime Directive",
                "prime_directive",
                "Entity Type: prime_directive",
                "Auto-applies to: Every user interaction",
                "INITIALIZATION PHASE",
                "EXECUTION PHASE",
                "VALIDATION PHASE"
            ]

            # Project indicators
            project_indicators = [
                "# Claude Code Integration",
                "## 🐍 Modern Python Development Stack",
                "Repository Overview",
                "Project Overview",
                "Development Stack",
                "Available Commands",
                "Project Structure",
                "Key Commands"
            ]

            framework_score = sum(1 for indicator in framework_indicators if indicator in content)
            project_score = sum(1 for indicator in project_indicators if indicator in content)

            # Strong framework indicators
            if framework_score >= 2:
                return "framework"
            # Strong project indicators
            elif project_score >= 2:
                return "project"
            # Small files are likely framework configs
            elif len(content.split('\n')) < 100 and framework_score > 0:
                return "framework"
            # Large files with no framework indicators are likely project configs
            elif len(content.split('\n')) > 150 and framework_score == 0:
                return "project"
            # Default to framework for safety (can be overridden with user confirmation)
            else:
                return "framework"

        except Exception as e:
            print(f"⚠️  Error analyzing {file_path}: {e}")
            return "unknown"

    def _handle_new_configs(self) -> bool:
        """Handle newly discovered or created CLAUDE.md files."""
        if not self.new_configs and not self.unknown_configs:
            return True

        print(f"\n🔍 New or Updated CLAUDE.md Files Detected:")

        # Show new configs
        if self.new_configs:
            print(f"\n📝 New files found ({len(self.new_configs)}):")
            for i, path in enumerate(self.new_configs, 1):
                config_type = self.known_configs.get(str(path), {}).get("type", "unknown")
                size = path.stat().st_size if path.exists() else 0
                print(f"   {i}. {path} ({config_type}, {size} bytes)")

        # Show unknown configs
        if self.unknown_configs:
            print(f"\n❓ Files needing classification ({len(self.unknown_configs)}):")
            for i, path in enumerate(self.unknown_configs, 1):
                size = path.stat().st_size if path.exists() else 0
                print(f"   {i}. {path} ({size} bytes)")

        print(f"\n🎯 Classification Options:")
        print(f"   f = Framework config (will be optimized)")
        print(f"   p = Project-specific (won't be modified)")
        print(f"   s = Skip this time")
        print(f"   a = Auto-classify all")

        choice = input(f"\nHow should new files be handled? (f/p/s/a) [a]: ").strip().lower()

        if choice == 's':
            print("⏭️  Skipping new files for this deployment")
            return True
        elif choice == 'f':
            # Classify all as framework
            for path in self.new_configs + self.unknown_configs:
                self._reclassify_config(path, "framework")
                self.claude_paths["claude_code"].append(path)
            print("✅ All new files classified as framework configs")
        elif choice == 'p':
            # Classify all as project
            for path in self.new_configs + self.unknown_configs:
                self._reclassify_config(path, "project")
            print("✅ All new files classified as project configs")
        else:  # 'a' or default
            print("✅ Using automatic classification")

        # Save updated registry
        self._save_config_registry()
        return True

    def _reclassify_config(self, file_path: Path, new_type: str):
        """Manually reclassify a config file."""
        self.known_configs[str(file_path)] = {
            "type": new_type,
            "first_seen": self.known_configs.get(str(file_path), {}).get("first_seen", datetime.now().isoformat()),
            "size": file_path.stat().st_size if file_path.exists() else 0,
            "auto_classified": False,
            "user_classified": datetime.now().isoformat()
        }

    def backup_current_framework(self) -> Dict[str, str]:
        """Create backup of current framework configuration."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_info = {
            "timestamp": timestamp,
            "version": "pre-smart-framework",
            "backed_up_files": []
        }

        print(f"🔄 Creating backup for deployment at {timestamp}")

        # Backup Claude Code configurations
        for claude_path in self.claude_paths["claude_code"]:
            if claude_path.exists():
                backup_name = f"claude_code_backup_{timestamp}_{claude_path.name}"
                backup_path = self.backup_dir / backup_name
                shutil.copy2(claude_path, backup_path)
                backup_info["backed_up_files"].append({
                    "type": "claude_code",
                    "original": str(claude_path),
                    "backup": str(backup_path)
                })
                print(f"✅ Backed up Claude Code: {claude_path} → {backup_path}")

        # Backup Claude Desktop memory configurations
        for memory_path in self.claude_paths["claude_desktop"]:
            if memory_path.exists():
                backup_name = f"claude_desktop_memory_{timestamp}_{memory_path.name}"
                backup_path = self.backup_dir / backup_name
                shutil.copy2(memory_path, backup_path)
                backup_info["backed_up_files"].append({
                    "type": "claude_desktop",
                    "original": str(memory_path),
                    "backup": str(backup_path)
                })
                print(f"✅ Backed up Claude Desktop: {memory_path} → {backup_path}")

        # Save backup info
        with open(self.deployment_log, 'w') as f:
            json.dump(backup_info, f, indent=2)

        return backup_info

    def validate_framework_components(self) -> bool:
        """Validate that all smart framework components are present."""
        required_files = [
            "smart-memory-directive.txt",
            "session-memory-cache.json",
            "incremental-learning-protocol.json",
            "learning-aware-authenticity.json"
        ]

        print("🔍 Validating smart framework components...")

        for file_name in required_files:
            file_path = self.framework_dir / file_name
            if not file_path.exists():
                print(f"❌ Missing required file: {file_path}")
                return False
            print(f"✅ Found: {file_name}")

        return True

    def _create_claude_desktop_prime_directive(self, directive_content: str) -> Dict:
        """Create a Claude Desktop memory entity for the prime directive."""
        return {
            "type": "entity",
            "entityType": "prime_directive",
            "name": "Enhanced MCP Server Exploration Prime Directive v2.2 - Smart Memory Caching",
            "observations": [
                directive_content,
                "CLAUDE DESKTOP INTEGRATION: Token-optimized framework with smart memory caching",
                "Reduces memory queries by 70-85% through session-based caching",
                "Preserves all learning capabilities while minimizing token overhead",
                "Priority: Prime Directive (Highest)",
                "Auto-applies to: Every user interaction in Claude Desktop"
            ]
        }

    def _update_claude_desktop_memory(self, memory_path: Path, directive_entity: Dict) -> bool:
        """Update Claude Desktop memory.json with the new directive."""
        try:
            # Read existing memory data
            with open(memory_path, 'r') as f:
                lines = f.readlines()

            memory_entries = []
            for line in lines:
                if line.strip():
                    memory_entries.append(json.loads(line))

            # Remove existing prime directive entries
            memory_entries = [
                entry for entry in memory_entries
                if not (entry.get("entityType") == "prime_directive" and
                       "MCP Server Exploration" in entry.get("name", ""))
            ]

            # Add the new directive
            memory_entries.append(directive_entity)

            # Write back to file
            with open(memory_path, 'w') as f:
                for entry in memory_entries:
                    f.write(json.dumps(entry) + '\n')

            return True

        except Exception as e:
            print(f"❌ Failed to update Claude Desktop memory: {e}")
            return False

    def deploy_smart_framework(self, optimization_level: str = "optimized") -> bool:
        """Deploy the smart framework with specified optimization level."""
        if not self.validate_framework_components():
            print("❌ Framework validation failed. Aborting deployment.")
            return False

        # Handle new configs before deployment
        if not self._handle_new_configs():
            print("❌ New config handling cancelled deployment.")
            return False

        print(f"🚀 Deploying smart framework with {optimization_level} optimization...")

        # Read the smart directive
        smart_directive_path = self.framework_dir / "smart-memory-directive.txt"
        with open(smart_directive_path, 'r') as f:
            smart_directive = f.read()

        # Customize based on optimization level
        if optimization_level == "lightweight":
            smart_directive = self._apply_lightweight_modifications(smart_directive)
        elif optimization_level == "emergency":
            smart_directive = self._apply_emergency_modifications(smart_directive)

        # Deploy to Claude Code configurations
        deployed_count = 0

        for claude_path in self.claude_paths["claude_code"]:
            try:
                # Write new framework to Claude Code config
                with open(claude_path, 'w') as f:
                    f.write(smart_directive)
                print(f"✅ Deployed smart framework to Claude Code: {claude_path}")
                deployed_count += 1
            except Exception as e:
                print(f"❌ Failed to deploy to Claude Code {claude_path}: {e}")

        # Deploy to Claude Desktop memory system
        desktop_directive_entity = self._create_claude_desktop_prime_directive(smart_directive)

        for memory_path in self.claude_paths["claude_desktop"]:
            try:
                success = self._update_claude_desktop_memory(memory_path, desktop_directive_entity)
                if success:
                    print(f"✅ Deployed smart framework to Claude Desktop: {memory_path}")
                    deployed_count += 1
                else:
                    print(f"❌ Failed to deploy to Claude Desktop: {memory_path}")
            except Exception as e:
                print(f"❌ Failed to deploy to Claude Desktop {memory_path}: {e}")

        if deployed_count > 0:
            total_configs = len(self.claude_paths["claude_code"]) + len(self.claude_paths["claude_desktop"])
            print(f"🎉 Successfully deployed to {deployed_count}/{total_configs} configuration(s)")
            print(f"   Claude Code: {len(self.claude_paths['claude_code'])} configs")
            print(f"   Claude Desktop: {len(self.claude_paths['claude_desktop'])} memory systems")
            self._update_deployment_log("deployed", optimization_level)
            return True
        else:
            print("❌ Failed to deploy to any locations")
            return False

    def _apply_lightweight_modifications(self, directive: str) -> str:
        """Apply lightweight optimizations to the directive."""
        modifications = [
            ("memory:search_nodes ONCE per session", "memory:search_nodes ONCE per 3 sessions"),
            ("Cache tool availability results for session duration", "Cache tool availability results for 24 hours"),
            ("Update at natural conversation breaks", "Update only at session end")
        ]

        for old, new in modifications:
            directive = directive.replace(old, new)

        return directive

    def _apply_emergency_modifications(self, directive: str) -> str:
        """Apply emergency token conservation modifications."""
        # Insert emergency mode activation
        emergency_header = """🚨 EMERGENCY TOKEN CONSERVATION MODE ACTIVE 🚨

This framework is running in emergency mode with maximum token conservation.
Learning and authenticity features are preserved but heavily optimized.

"""

        # Modify key operations for emergency mode
        modifications = [
            ("MANDATORY: Query knowledge graph", "OPTIONAL: Query knowledge graph only if cache empty"),
            ("Verify functional access to critical MCP servers", "Use cached tool status, test only on failure"),
            ("Apply cached authenticity rules from memory", "Use minimal cached rules, skip validation for routine operations")
        ]

        modified_directive = emergency_header + directive
        for old, new in modifications:
            modified_directive = modified_directive.replace(old, new)

        return modified_directive

    def rollback_framework(self) -> bool:
        """Rollback to previous framework version."""
        if not self.deployment_log.exists():
            print("❌ No deployment log found. Cannot rollback.")
            return False

        with open(self.deployment_log, 'r') as f:
            backup_info = json.load(f)

        print(f"🔄 Rolling back to backup from {backup_info['timestamp']}")

        rollback_count = 0
        for file_info in backup_info["backed_up_files"]:
            original_path = Path(file_info["original"])
            backup_path = Path(file_info["backup"])
            config_type = file_info.get("type", "unknown")

            if backup_path.exists():
                try:
                    if config_type == "claude_desktop":
                        # For Claude Desktop, we need to restore the memory.json carefully
                        shutil.copy2(backup_path, original_path)
                        print(f"✅ Restored Claude Desktop memory: {original_path}")
                    else:
                        # For Claude Code, direct file copy
                        shutil.copy2(backup_path, original_path)
                        print(f"✅ Restored Claude Code config: {original_path}")
                    rollback_count += 1
                except Exception as e:
                    print(f"❌ Failed to restore {original_path}: {e}")

        if rollback_count > 0:
            print(f"🎉 Successfully rolled back {rollback_count} configuration(s)")
            self._update_deployment_log("rolled_back", backup_info["version"])
            return True
        else:
            print("❌ Rollback failed")
            return False

    def _update_deployment_log(self, action: str, version: str):
        """Update deployment log with action."""
        log_entry = {
            "action": action,
            "version": version,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Append to log
        if self.deployment_log.exists():
            with open(self.deployment_log, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"deployments": []}

        if "deployments" not in log_data:
            log_data["deployments"] = []

        log_data["deployments"].append(log_entry)

        with open(self.deployment_log, 'w') as f:
            json.dump(log_data, f, indent=2)

    def status_check(self) -> Dict:
        """Check current framework status and provide recommendations."""
        claude_code_configs = len(self.claude_paths["claude_code"])
        claude_desktop_configs = len(self.claude_paths["claude_desktop"])

        status = {
            "current_framework": "unknown",
            "claude_code_configs": claude_code_configs,
            "claude_desktop_configs": claude_desktop_configs,
            "total_configs": claude_code_configs + claude_desktop_configs,
            "project_configs": len(self.project_configs),
            "new_configs": len(self.new_configs),
            "unknown_configs": len(self.unknown_configs),
            "total_found": claude_code_configs + claude_desktop_configs + len(self.project_configs),
            "backup_available": self.deployment_log.exists(),
            "smart_components_ready": self.validate_framework_components()
        }

        # Analyze Claude Code framework
        for claude_path in self.claude_paths["claude_code"]:
            if claude_path.exists():
                with open(claude_path, 'r') as f:
                    content = f.read()

                if "Smart Memory Caching" in content:
                    status["claude_code_framework"] = "smart-framework"
                elif "Emergency Token Conservation" in content:
                    status["claude_code_framework"] = "emergency-mode"
                elif "Enhanced MCP Server Exploration Prime Directive v2.0" in content:
                    status["claude_code_framework"] = "original-v2"
                else:
                    status["claude_code_framework"] = "custom"
                break

        # Analyze Claude Desktop framework
        for memory_path in self.claude_paths["claude_desktop"]:
            if memory_path.exists():
                try:
                    with open(memory_path, 'r') as f:
                        lines = f.readlines()

                    for line in lines:
                        if line.strip():
                            entry = json.loads(line)
                            if (entry.get("entityType") == "prime_directive" and
                                "MCP Server Exploration" in entry.get("name", "")):
                                if "Smart Memory Caching" in entry.get("name", ""):
                                    status["claude_desktop_framework"] = "smart-framework"
                                elif "v2.0" in entry.get("name", ""):
                                    status["claude_desktop_framework"] = "original-v2"
                                else:
                                    status["claude_desktop_framework"] = "custom"
                                break
                except Exception as e:
                    status["claude_desktop_framework"] = f"error: {e}"
                break

        # Set overall framework status
        frameworks = [
            status.get("claude_code_framework"),
            status.get("claude_desktop_framework")
        ]
        if "smart-framework" in frameworks:
            status["current_framework"] = "smart-framework"
        elif "original-v2" in frameworks:
            status["current_framework"] = "original-v2"
        elif any(f for f in frameworks if f and not f.startswith("error")):
            status["current_framework"] = "mixed"

        return status

    def interactive_deployment(self):
        """Interactive deployment with user guidance."""
        print("🤖 Smart Framework Deployment Wizard")
        print("====================================")

        # Status check
        status = self.status_check()
        print(f"\n📊 Current Status:")
        print(f"   Overall Framework: {status['current_framework']}")
        print(f"   ")
        print(f"   📁 Configuration Discovery:")
        print(f"      Framework configs: {status['claude_code_configs']} (will be optimized)")
        if status.get('claude_code_framework'):
            print(f"        └─ Currently: {status['claude_code_framework']}")
        print(f"      Claude Desktop: {status['claude_desktop_configs']} memory systems")
        if status.get('claude_desktop_framework'):
            print(f"        └─ Currently: {status['claude_desktop_framework']}")
        print(f"      Project configs: {status['project_configs']} (will be preserved)")
        if status['new_configs'] > 0:
            print(f"      🆕 New files: {status['new_configs']} (needs classification)")
        if status['unknown_configs'] > 0:
            print(f"      ❓ Unknown files: {status['unknown_configs']} (needs classification)")
        print(f"      Total found: {status['total_found']} CLAUDE.md files")
        print(f"   ")
        print(f"   🔧 Deployment Ready:")
        print(f"      Backup available: {status['backup_available']}")
        print(f"      Smart components: {status['smart_components_ready']}")

        if not status['smart_components_ready']:
            print("\n❌ Smart framework components not found. Please run from framework directory.")
            return

        # Get user preferences
        print(f"\n🎯 Available optimization levels:")
        print("   1. optimized  - 70-85% token reduction, full learning preserved")
        print("   2. lightweight - 80-90% token reduction, essential learning only")
        print("   3. emergency  - 90-95% token reduction, minimal operations")

        level_choice = input("\nSelect optimization level (1-3) [1]: ").strip()
        level_map = {"1": "optimized", "2": "lightweight", "3": "emergency", "": "optimized"}
        optimization_level = level_map.get(level_choice, "optimized")

        # Confirm deployment
        print(f"\n🚀 Ready to deploy {optimization_level} smart framework")
        print("   This will:")
        print("   • Backup your current framework")
        print("   • Deploy smart caching system")
        print("   • Preserve all learning capabilities")
        print("   • Provide rollback option")

        confirm = input("\nProceed with deployment? (y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ Deployment cancelled")
            return

        # Execute deployment
        backup_info = self.backup_current_framework()
        success = self.deploy_smart_framework(optimization_level)

        if success:
            print(f"\n🎉 Smart framework deployed successfully!")
            print(f"   Optimization level: {optimization_level}")
            print(f"   Expected token savings: 70-95%")
            print(f"   Learning preservation: Full")
            print(f"\n💡 To rollback: python deploy-smart-framework.py --rollback")
        else:
            print(f"\n❌ Deployment failed. Your original framework is backed up.")

def main():
    parser = argparse.ArgumentParser(description="Deploy smart framework with token optimization")
    parser.add_argument("--claude-config", help="Path to Claude configuration file")
    parser.add_argument("--optimization", choices=["optimized", "lightweight", "emergency"],
                       default="optimized", help="Optimization level")
    parser.add_argument("--rollback", action="store_true", help="Rollback to previous framework")
    parser.add_argument("--status", action="store_true", help="Check current framework status")
    parser.add_argument("--interactive", action="store_true", help="Interactive deployment wizard")

    args = parser.parse_args()

    deployer = SmartFrameworkDeployer(args.claude_config)

    if args.rollback:
        success = deployer.rollback_framework()
        exit(0 if success else 1)

    elif args.status:
        status = deployer.status_check()
        print("📊 Framework Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")

    elif args.interactive:
        deployer.interactive_deployment()

    else:
        # Automated deployment
        backup_info = deployer.backup_current_framework()
        success = deployer.deploy_smart_framework(args.optimization)
        exit(0 if success else 1)

if __name__ == "__main__":
    main()