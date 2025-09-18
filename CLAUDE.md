# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **AI MCP Framework** - a comprehensive system for building AI agents that automatically utilize MCP (Model Context Protocol) tools while maintaining authenticity and preventing behavioral drift. The framework creates proactive AI behavior that leverages MCP servers without explicit prompting.

## Key Commands

### Framework Installation
```bash
# Install the complete framework
python tools/framework-installer.py

# Import framework into knowledge graph/memory system
python tools/knowledge-graph-importer.py

# Generate framework export for MCP memory servers
python tools/framework-installer.py --config-path ~/.config/mcp/config.json
```

### Validation and Testing
```bash
# Test MCP server configuration
python tools/framework-installer.py --config-path /path/to/mcp/config.json

# Generate import for different memory server types
python tools/knowledge-graph-importer.py --memory-server mcp_memory
python tools/knowledge-graph-importer.py --memory-server generic
```

## Architecture Overview

The framework operates through a **multi-layered behavioral modification system**:

### Core Components
1. **Enhanced MCP Server Exploration Prime Directive** (`framework/prime-directive-v2.txt`)
   - Initialization Phase: Framework loading + tool testing
   - Execution Phase: Proactive tool utilization + authenticity validation
   - Validation Phase: Pre-response checks + continuous learning

2. **Hierarchical Learning System** (`framework/hierarchical-learning.json`)
   - Prime Directive (immutable) → Secondary Rules (proven) → Tertiary Rules (contextual) → Quaternary Rules (experimental)
   - Prevents directive drift through human-in-the-loop governance

3. **Authenticity Controls** (`framework/authenticity-controls.json`)
   - Self-audit questions prevent performative behavior
   - Verification markers: 🔍 VERIFIED vs ⚠️ ASSUMED
   - Observable metrics track prediction accuracy and decision quality

4. **Safety Protocols** (`framework/safety-protocols.json`)
   - Experimental rule safety protocol prevents automatic override
   - Auto-correction protocol for immediate violation recovery
   - User correction integration for learning from human feedback

### Framework Architecture Flow
```
User Input → Framework Loading → Tool Testing → Proactive Tool Usage →
Authenticity Validation → Pre-Response Check → Response Delivery
```

## MCP Server Configuration

The framework requires specific MCP servers to function properly:

### Critical Servers (Required)
- `memory`: Persistent knowledge graphs for framework rules
- `filesystem`: File operations and repo management
- `web_search`: Research and verification capabilities
- `fetch`: HTTP requests and external validation

### Recommended Servers
- `ddg-search`: DuckDuckGo search capabilities
- `arxiv-research`: Academic paper access
- `wikipedia`: Knowledge base access
- `markitdown`: Document conversion
- `mcp-sequentialthinking-tools`: Complex reasoning support

### Configuration File
Use `examples/mcp-config-example.json` as a template for MCP server setup. The configuration includes environment variables for data storage paths and server-specific settings.

## Key Development Patterns

### Framework Implementation
1. **Load Framework Components**: Query memory system for authenticity controls and safety protocols
2. **Test MCP Tool Availability**: Verify functional access to all configured MCP servers
3. **Proactive Tool Utilization**: Automatically leverage MCP tools based on task requirements
4. **Authenticity Validation**: Apply self-audit questions throughout execution
5. **Pre-Response Verification**: Mandatory validation with verification markers

### Safety Boundaries
- All experimental rules require explicit human approval
- Framework violations trigger immediate self-correction
- Hierarchical learning prevents core directive corruption
- External verification required for technical claims

### Learning Integration
- User corrections automatically become behavioral improvements
- Observable metrics track decision quality over time
- Mistake patterns become predictive error prevention
- Cross-session learning through persistent knowledge graphs

## File Structure Significance

```
framework/               # Core behavioral modification components
├── prime-directive-v2.txt      # Main behavioral directive (highest priority)
├── authenticity-controls.json  # Self-audit questions and verification
├── hierarchical-learning.json  # Safe learning architecture
└── safety-protocols.json       # Human-in-the-loop safeguards

tools/                   # Installation and import utilities
├── framework-installer.py      # Automated framework setup
└── knowledge-graph-importer.py # Memory system integration

examples/                # Reference implementations and configs
├── mcp-config-example.json     # MCP server configuration template
├── knowledge-graph-export.json # Sample knowledge graph data
└── claude-preferences.txt      # Example preference implementation

docs/                    # Architecture and implementation guides
├── architecture.md             # System architecture overview
└── implementation-guide.md     # Step-by-step setup instructions
```

## Framework Integration

### For AI Systems
1. Copy `framework/prime-directive-v2.txt` content to AI preferences (highest priority)
2. Import framework components using `tools/knowledge-graph-importer.py`
3. Configure MCP servers according to `examples/mcp-config-example.json`
4. Verify automatic tool usage and authenticity markers in responses

### For Developers
- The framework operates at the behavioral level - no code compilation needed
- Tools are Python scripts for setup and knowledge graph management
- Configuration is JSON-based for MCP server integration
- Framework effects are observable through AI behavior changes

## Success Indicators

When properly implemented, you should observe:
- **Automatic MCP tool usage** without explicit user prompting
- **Verification markers** (🔍 VERIFIED vs ⚠️ ASSUMED) in AI responses
- **Proactive tool testing** at the start of interactions
- **External verification** for technical claims and assessments
- **Learning from corrections** with behavioral improvements over time

## Safety Notes

- Framework modifications require human approval for experimental rules
- Core directives are immutable to prevent behavioral drift
- All learning happens through hierarchical rule promotion
- Safety protocols include automatic rollback capabilities
- External verification prevents performative behavior