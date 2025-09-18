# Complete Setup Tutorial

This tutorial provides step-by-step instructions for implementing the AI MCP Framework from scratch.

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [MCP Server Installation](#mcp-server-installation)
3. [Framework Installation](#framework-installation)
4. [AI Platform Configuration](#ai-platform-configuration)
5. [Testing and Validation](#testing-and-validation)
6. [Advanced Configuration](#advanced-configuration)

## Environment Setup

### Step 1: Verify System Requirements

```bash
# Check Python version (3.8+ required)
python3 --version

# Check Node.js version (18+ required)
node --version

# Check npm version (8.19+ required)
npm --version

# Check Git (for cloning repository)
git --version
```

If any requirements are missing:

**macOS (using Homebrew):**
```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install requirements
brew install python node git
```

**Linux (Ubuntu/Debian):**
```bash
# Update package list
sudo apt update

# Install requirements
sudo apt install python3 python3-pip nodejs npm git

# Install Node.js 18+ if needed
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Windows (using WSL2):**
```bash
# Install WSL2 with Ubuntu
wsl --install

# Follow Linux instructions above within WSL
```

### Step 2: Clone the Framework Repository

```bash
# Clone the repository
git clone https://github.com/simplemindedbot/ai-mcp-framework.git

# Navigate to the directory
cd ai-mcp-framework

# Verify contents
ls -la
```

## MCP Server Installation

### Step 3: Install Required MCP Servers

```bash
# Install core required servers
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-web-search
npm install -g @modelcontextprotocol/server-fetch

# Install recommended servers
npm install -g @modelcontextprotocol/server-ddg-search
npm install -g @modelcontextprotocol/server-arxiv
npm install -g @modelcontextprotocol/server-wikipedia

# Verify installations
npm list -g --depth=0 | grep modelcontextprotocol
```

### Step 4: Test MCP Server Functionality

```bash
# Test memory server
npx @modelcontextprotocol/server-memory --help

# Test filesystem server
npx @modelcontextprotocol/server-filesystem --help

# Test web search server
npx @modelcontextprotocol/server-web-search --help
```

## Framework Installation

### Step 5: Configure MCP Servers

Create your MCP configuration file:

```bash
# For Claude Desktop (macOS)
mkdir -p ~/Library/Application\ Support/Claude
cp examples/mcp-config-example.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# For other platforms, copy to appropriate location
```

Edit the configuration file to match your system:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "env": {
        "MEMORY_FILE_PATH": "~/Library/Application Support/Claude/memory-data/memory.json"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "~/Desktop", "~/Documents"],
      "description": "File system access for Desktop and Documents"
    }
  }
}
```

### Step 6: Run Framework Installer

```bash
# Run the framework installer
python tools/framework-installer.py

# If you have a custom MCP config location:
python tools/framework-installer.py --config-path /path/to/your/config.json
```

Expected output:
```
🚀 AI MCP Framework Installer
========================================
🔍 Validating MCP server configuration...
✅ Found 4 MCP servers configured
📚 Loading framework components...
✅ Loaded 4 framework components
📥 Importing framework components to memory system...
✅ Framework export created at: framework-export.json
🧪 Testing framework installation...
✅ Prime Directive Accessible
✅ Authenticity Controls Loaded
✅ Safety Protocols Active
✅ Mcp Tools Responsive
🎉 AI MCP Framework installation completed successfully!
```

### Step 7: Import Framework into Memory System

```bash
# Import the framework into your memory system
python tools/knowledge-graph-importer.py

# For specific memory server types:
python tools/knowledge-graph-importer.py --memory-server mcp_memory
```

## AI Platform Configuration

### Step 8A: Claude Desktop Configuration

1. **Restart Claude Desktop** to pick up the new MCP configuration
2. **Test MCP connection** by starting a new conversation
3. **Copy the Prime Directive** from `framework/prime-directive-v2.txt`
4. **Set as highest priority** in your Claude preferences

**Setting the Prime Directive:**

In Claude Desktop:
1. Go to Settings → Custom Instructions
2. Paste the entire content of `framework/prime-directive-v2.txt`
3. Set priority to "Highest"
4. Save settings

### Step 8B: Claude API Configuration

For API usage, include the framework components in your system prompt:

```python
import json

# Load framework components
with open('framework/prime-directive-v2.txt', 'r') as f:
    prime_directive = f.read()

# Include in your API call
system_prompt = f"""
{prime_directive}

[Additional instructions...]
"""
```

### Step 8C: Other AI Platforms

For other MCP-compatible AI platforms:
1. Configure MCP servers according to platform documentation
2. Import framework components using appropriate method
3. Set the Prime Directive as the highest priority behavioral rule

## Testing and Validation

### Step 9: Test Framework Functionality

**Test 1: Automatic Tool Testing**
Start a new conversation and observe:
- AI should automatically test MCP tool availability
- Should report functional vs. non-functional tools
- Should use 🔍 VERIFIED markers for tested capabilities

**Test 2: Proactive Tool Usage**
Ask a question that could benefit from web search:
```
What are the latest developments in AI safety research?
```

Expected behavior:
- AI should automatically use web search tools
- Should mark information as 🔍 VERIFIED (from search) vs ⚠️ ASSUMED (from training)
- Should not wait for explicit prompting

**Test 3: Authenticity Validation**
Ask for a status report:
```
Can you give me a status report on your current capabilities?
```

Expected behavior:
- AI should test actual capabilities before reporting
- Should include verification markers
- Should distinguish between verified and assumed capabilities

### Step 10: Verify Framework Components

```bash
# Verify all framework files are accessible
ls -la framework/
ls -la examples/
ls -la tools/

# Test installer functionality
python tools/framework-installer.py --help

# Test knowledge graph importer
python tools/knowledge-graph-importer.py --help
```

## Advanced Configuration

### Step 11: Customize for Your Use Case

**For Development Work:**
```json
{
  "filesystem": {
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "~/Code", "~/Projects"]
  }
}
```

**For Research:**
```json
{
  "arxiv": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-arxiv"],
    "env": {
      "ARXIV_STORAGE_PATH": "~/Research/papers"
    }
  }
}
```

**For Content Creation:**
```json
{
  "web-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-ddg-search"]
  }
}
```

### Step 12: Monitor Framework Performance

Create a simple monitoring script:

```python
#!/usr/bin/env python3
"""Monitor framework effectiveness"""

import json
from datetime import datetime

def log_interaction(used_tools, authenticity_markers, user_satisfaction):
    """Log framework performance metrics"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tools_used": used_tools,
        "authenticity_markers": authenticity_markers,
        "user_satisfaction": user_satisfaction
    }

    with open("framework_metrics.json", "a") as f:
        json.dump(log_entry, f)
        f.write("\n")

# Usage after each interaction
log_interaction(
    used_tools=["memory", "web_search"],
    authenticity_markers={"verified": 5, "assumed": 2},
    user_satisfaction=4.5
)
```

## Troubleshooting Common Issues

See the [Troubleshooting Guide](troubleshooting.md) for solutions to common setup problems.

## Next Steps

1. **Read the [Implementation Guide](implementation-guide.md)** for detailed framework usage
2. **Review [Architecture Documentation](architecture.md)** to understand system design
3. **Explore [Research Background](research-background.md)** for theoretical foundations
4. **Join the community** by contributing to the [GitHub repository](https://github.com/simplemindedbot/ai-mcp-framework)

## Support

If you encounter issues:
1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review existing [GitHub Issues](https://github.com/simplemindedbot/ai-mcp-framework/issues)
3. Create a new issue with detailed information about your setup and the problem

## Success Criteria

You'll know the framework is working correctly when:
- ✅ AI automatically uses MCP tools without prompting
- ✅ Responses include appropriate verification markers
- ✅ AI tests tool availability at conversation start
- ✅ Claims are backed by actual tool usage
- ✅ User experience feels more capable and authentic

Congratulations! You now have a fully functional AI MCP Framework implementation.