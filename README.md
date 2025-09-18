# AI MCP Framework: Building Authentic, Proactive AI Systems

A comprehensive framework for developing AI systems that automatically utilize MCP (Model Context Protocol) tools while maintaining authenticity and preventing behavioral drift.

## Overview

This framework emerged from a practical experiment: "How do we get AI systems to actually use the tools available to them?" Instead of waiting for explicit instructions, this system creates proactive AI behavior that automatically leverages MCP servers while maintaining safety and authenticity.

## Key Problems Solved

- **Tool Adoption Gap**: AIs often ignore available MCP tools unless explicitly prompted
- **Performative Behavior**: AI systems that claim capabilities without actual verification
- **Behavioral Drift**: Gradual degradation from helpful to sycophantic or potentially harmful
- **Learning Without Safety**: How to improve AI behavior without compromising core directives

## Framework Components

### 1. Enhanced MCP Server Exploration Prime Directive
The core behavioral directive that creates automatic MCP tool usage:
- **Initialization Phase**: Load authenticity framework + test tool availability
- **Execution Phase**: Proactive tool utilization + authenticity validation
- **Validation Phase**: Pre-response checks + continuous learning

### 2. Hierarchical Learning System
Safe learning architecture that prevents directive drift:
- **Prime Directive** (immutable): Core behavioral rules
- **Secondary Rules** (proven): Validated behavioral improvements
- **Tertiary Rules** (contextual): User-validated adaptations  
- **Quaternary Rules** (experimental): Require explicit approval

### 3. Authenticity Controls
Prevents performative behavior through:
- **Self-Audit Questions**: "Have I verified this claim?"
- **External Verification**: Grounding in actual tests/evidence
- **Observable Metrics**: Tracking prediction accuracy and decision quality
- **Safety Boundaries**: Hard limits on experimental changes

### 4. Safety Governance
Human-in-the-loop safeguards:
- **Experimental Rule Safety Protocol**: Prevents automatic override
- **Auto-Correction Protocol**: Immediate violation recovery
- **User Correction Integration**: Learning from human feedback

## Repository Structure

```
ai-mcp-framework/
├── README.md                          # This file
├── docs/
│   ├── architecture.md               # System architecture overview
│   ├── implementation-guide.md       # Step-by-step setup
│   └── research-background.md        # Supporting research
├── framework/
│   ├── prime-directive-v2.txt        # Enhanced MCP Prime Directive
│   ├── authenticity-controls.json    # Self-audit questions & metrics
│   ├── hierarchical-learning.json    # Learning governance rules
│   └── safety-protocols.json         # Safety governance system
├── examples/
│   ├── claude-preferences.txt        # Example preference implementation
│   ├── knowledge-graph-export.json   # Sample knowledge graph data
│   └── mcp-config-example.json       # Sample MCP server configuration
└── tools/
    ├── framework-installer.py        # Automated framework setup
    └── knowledge-graph-importer.py   # Import framework into memory systems
```

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Node.js**: 18 or higher (for MCP servers)
- **npm**: 8.19 or higher
- **Operating System**: macOS, Linux, or Windows with WSL

### Required MCP Servers
The framework requires these MCP servers to function properly:

- **Memory Server**: `@modelcontextprotocol/server-memory` - Stores framework rules and learning data
- **Filesystem Server**: `@modelcontextprotocol/server-filesystem` - File operations and repository access
- **Web Search Server**: `@modelcontextprotocol/server-web-search` or `@modelcontextprotocol/server-ddg-search`
- **Fetch Server**: `@modelcontextprotocol/server-fetch` - HTTP requests and external validation

### AI Platform Requirements
- **Claude Desktop**: Version 0.7.0 or higher with MCP support enabled
- **Claude API**: Access to Claude with MCP configuration capability
- **Other MCP-compatible AI platforms**: Any AI system supporting Model Context Protocol

### Installation Commands
```bash
# Install required MCP servers
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-web-search
npm install -g @modelcontextprotocol/server-fetch

# Optional but recommended servers
npm install -g @modelcontextprotocol/server-ddg-search
npm install -g @modelcontextprotocol/server-arxiv
npm install -g @modelcontextprotocol/server-wikipedia
```

## Quick Start

1. **Verify Prerequisites**
   ```bash
   python3 --version  # Should be 3.8+
   node --version     # Should be 18+
   npm --version      # Should be 8.19+
   ```

2. **Install MCP Memory Server**
   ```bash
   # Ensure you have an MCP memory server configured
   # This framework stores rules in persistent knowledge graphs
   ```

2. **Load the Framework**
   ```bash
   python tools/framework-installer.py
   ```

3. **Configure Your AI System**
   - Copy `framework/prime-directive-v2.txt` to your AI preferences
   - Import knowledge graph components using your MCP memory server
   - Configure MCP servers according to `examples/mcp-config-example.json`

4. **Verify Installation**
   - AI should automatically begin using MCP tools
   - Look for authenticity markers (🔍 VERIFIED vs ⚠️ ASSUMED)
   - Observe automatic tool testing at interaction start

## Key Features

### Automatic Tool Usage
- AI proactively uses memory, filesystem, web, and analysis tools
- No explicit user prompting required
- Tools become "force multipliers" for problem-solving

### Authenticity Validation
- Claims marked as verified or assumed
- Self-audit questions prevent overconfident responses
- External verification for technical claims

### Safe Learning
- Hierarchical rule system prevents core directive corruption
- User approval required for experimental behaviors
- Automatic rollback of harmful changes

### Continuous Improvement
- Learns from user corrections and mistakes
- Builds predictive error prevention
- Maintains simplification bias against complexity creep

## Real-World Results

From our experiment (September 17, 2025):
- **Immediate Tool Adoption**: AI began automatically using MCP tools without prompting
- **Authenticity Improvement**: Claims properly marked as verified vs. assumed
- **Safety Validation**: Successfully prevented potentially harmful experimental rules
- **Learning Integration**: User corrections automatically became behavioral improvements

## Research Foundation

This framework builds on:
- **Behavioral Psychology**: Preference simplification and habit formation
- **Safety Research**: Human-in-the-loop governance and fail-safe design
- **AI Alignment**: External observation for authenticity validation
- **Systems Thinking**: Hierarchical rule structures and feedback loops

## Use Cases

- **Personal AI Assistants**: Proactive tool usage with safety boundaries
- **Development Environments**: Automatic integration with development tools
- **Research Applications**: Systematic use of research and analysis tools
- **Content Creation**: Automatic fact-checking and verification
- **Business Intelligence**: Proactive data analysis and reporting

## Contributing

This framework is the result of practical experimentation with AI behavior modification. Contributions welcome for:
- Additional safety protocols
- Integration with other MCP servers
- Performance optimizations
- Documentation improvements

## License

MIT License - See LICENSE file for details

## Citation

If you use this framework in research or production:

```
AI MCP Framework: Building Authentic, Proactive AI Systems
GitHub: https://github.com/simplemindedbot/ai-mcp-framework
Date: September 2025
```

## Related Work

- [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
- [Anthropic's Constitutional AI](https://arxiv.org/abs/2212.08073)
- [AI Safety via Debate](https://arxiv.org/abs/1805.00899)

---

**Status**: Production-ready framework validated through real-world experimentation.
**Last Updated**: September 17, 2025