# Troubleshooting Guide

This guide covers common issues encountered when implementing the AI MCP Framework and their solutions.

## Quick Diagnostics

### Check Framework Status
```bash
# Test framework installer
python tools/framework-installer.py --help

# Verify MCP servers are installed
npm list -g --depth=0 | grep modelcontextprotocol

# Check Node.js and Python versions
node --version && python3 --version
```

## Common Installation Issues

### Issue: MCP Servers Not Found
**Symptoms:**
- `npm install -g @modelcontextprotocol/server-*` fails
- Framework installer reports missing servers

**Solutions:**
```bash
# Update npm to latest version
npm install -g npm@latest

# Clear npm cache
npm cache clean --force

# Reinstall MCP servers with specific registry
npm install -g @modelcontextprotocol/server-memory --registry https://registry.npmjs.org/

# For corporate networks, check proxy settings
npm config get proxy
npm config get https-proxy
```

### Issue: Permission Errors During Installation
**Symptoms:**
- `EACCES` permission denied errors
- Cannot install global npm packages

**Solutions:**
```bash
# Option 1: Use node version manager (recommended)
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install node
nvm use node

# Option 2: Configure npm to use different directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
source ~/.profile

# Option 3: Fix npm permissions (macOS/Linux)
sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}
```

### Issue: Python Path Problems
**Symptoms:**
- `python3 not found` errors
- Framework installer fails to run

**Solutions:**
```bash
# Check available Python versions
which python3
ls -la /usr/bin/python*

# Create symlink if needed (Linux)
sudo ln -s /usr/bin/python3.x /usr/bin/python3

# Use virtual environment (recommended)
python3 -m venv framework-env
source framework-env/bin/activate  # Linux/macOS
# framework-env\Scripts\activate  # Windows

# Install in virtual environment
pip install -r requirements.txt  # if requirements.txt exists
```

## MCP Configuration Issues

### Issue: AI Platform Doesn't Recognize MCP Servers
**Symptoms:**
- AI doesn't use tools automatically
- No MCP server testing at conversation start
- Tools appear unavailable

**Solutions:**

**For Claude Desktop:**
```bash
# Verify config file location
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Check config file format
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool

# Restart Claude Desktop completely
killall "Claude" && open /Applications/Claude.app

# Check Claude Desktop version (0.7.0+ required)
# In Claude Desktop: Help → About Claude
```

**For other platforms:**
```bash
# Verify MCP config syntax
python3 -c "import json; json.load(open('path/to/config.json'))"

# Test individual MCP servers
npx @modelcontextprotocol/server-memory --help
npx @modelcontextprotocol/server-filesystem ~/Documents --help
```

### Issue: Memory Server Cannot Store Data
**Symptoms:**
- Framework components not persistent across sessions
- Knowledge graph import fails
- Memory server errors in logs

**Solutions:**
```bash
# Create memory data directory
mkdir -p ~/Library/Application\ Support/Claude/memory-data

# Check permissions
ls -la ~/Library/Application\ Support/Claude/
chmod 755 ~/Library/Application\ Support/Claude/memory-data

# Test memory server directly
npx @modelcontextprotocol/server-memory

# Alternative memory file location
export MEMORY_FILE_PATH=~/Documents/claude-memory.json
```

### Issue: Filesystem Server Access Denied
**Symptoms:**
- Cannot access files or directories
- Filesystem operations fail
- Permission errors in AI responses

**Solutions:**
```bash
# Check directory permissions
ls -la ~/Desktop ~/Documents

# Grant Claude access (macOS)
# System Preferences → Privacy & Security → Files and Folders → Claude

# Update MCP config with accessible directories
{
  "filesystem": {
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/allowed-dir"]
  }
}

# Test filesystem server
npx @modelcontextprotocol/server-filesystem ~/Desktop
```

## Framework Behavior Issues

### Issue: AI Not Using Tools Automatically
**Symptoms:**
- AI gives generic responses instead of using tools
- No tool testing at conversation start
- Manual prompting required for tool usage

**Diagnostic Steps:**
```bash
# Verify Prime Directive is loaded
grep -n "INITIALIZATION PHASE" framework/prime-directive-v2.txt

# Check if framework was imported to memory
python tools/knowledge-graph-importer.py --help

# Test memory system access
# In AI conversation: "Can you search your memory for MCP directives?"
```

**Solutions:**
1. **Ensure Prime Directive has highest priority** in AI preferences
2. **Restart AI platform** after configuration changes
3. **Clear AI conversation history** to start fresh
4. **Verify MCP servers are responsive:**
   ```bash
   # Test each server individually
   npx @modelcontextprotocol/server-memory &
   npx @modelcontextprotocol/server-filesystem ~/Documents &
   ```

### Issue: Missing Verification Markers
**Symptoms:**
- No 🔍 VERIFIED or ⚠️ ASSUMED markers in responses
- Claims not distinguished by verification status

**Solutions:**
1. **Check authenticity controls are loaded:**
   ```bash
   cat framework/authenticity-controls.json
   ```

2. **Verify self-audit questions are accessible:**
   - In AI conversation: "Can you show me your self-audit questions?"

3. **Test verification markers explicitly:**
   - Ask: "Please test a tool and mark your response with verification status"

### Issue: Framework Violations Not Self-Correcting
**Symptoms:**
- AI makes claims without verification
- No immediate self-correction when framework rules are violated
- Authenticity protocols not applied

**Solutions:**
1. **Verify safety protocols are loaded:**
   ```bash
   cat framework/safety-protocols.json
   ```

2. **Test auto-correction explicitly:**
   - Ask AI to make a status report without testing tools
   - Should trigger self-correction behavior

3. **Check hierarchical learning system:**
   ```bash
   cat framework/hierarchical-learning.json
   ```

## Platform-Specific Issues

### Claude Desktop Issues

**Issue: Config Changes Not Taking Effect**
```bash
# Force restart Claude Desktop
killall "Claude"
sleep 2
open /Applications/Claude.app

# Verify config location
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Check for syntax errors
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool
```

**Issue: MCP Servers Not Starting**
```bash
# Check Claude Desktop logs (macOS)
tail -f ~/Library/Logs/Claude/claude-desktop.log

# Look for MCP server startup errors
grep -i "mcp\|server\|error" ~/Library/Logs/Claude/claude-desktop.log
```

### API Integration Issues

**Issue: Framework Not Working with API Calls**
```python
# Ensure Prime Directive is included in system prompt
import json

with open('framework/prime-directive-v2.txt', 'r') as f:
    prime_directive = f.read()

# Include in API call
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    system=prime_directive,  # Include framework here
    messages=[{"role": "user", "content": "Your question"}]
)
```

## Performance Issues

### Issue: Slow Tool Response Times
**Symptoms:**
- Long delays when AI uses tools
- Timeouts in tool operations
- Poor user experience

**Solutions:**
```bash
# Check network connectivity
ping google.com

# Test individual MCP servers for responsiveness
time npx @modelcontextprotocol/server-web-search
time npx @modelcontextprotocol/server-memory

# Optimize MCP server configuration
{
  "memory": {
    "timeout": 10000,  # Increase timeout
    "retryAttempts": 2  # Reduce retries
  }
}
```

### Issue: High Memory Usage
**Solutions:**
```bash
# Monitor memory usage
top -p $(pgrep -f "mcp-server")

# Limit memory server cache size
export MEMORY_MAX_SIZE=100MB

# Restart MCP servers periodically
# Add to cron job:
# 0 3 * * * killall node && sleep 5 && restart-claude
```

## Debugging and Logging

### Enable Debug Logging
```bash
# For framework installer
python tools/framework-installer.py --verbose

# For Node.js MCP servers
DEBUG=mcp* npx @modelcontextprotocol/server-memory

# For Claude Desktop (macOS)
tail -f ~/Library/Logs/Claude/claude-desktop.log
```

### Collect Diagnostic Information
```bash
#!/bin/bash
# diagnostic-collector.sh

echo "=== System Information ==="
uname -a
python3 --version
node --version
npm --version

echo "=== MCP Servers ==="
npm list -g --depth=0 | grep modelcontextprotocol

echo "=== Framework Files ==="
ls -la framework/
ls -la tools/

echo "=== MCP Configuration ==="
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

echo "=== Recent Logs ==="
tail -20 ~/Library/Logs/Claude/claude-desktop.log
```

## Getting Help

### Before Reporting Issues
1. **Run diagnostic collector** (script above)
2. **Try minimal reproduction** with fresh conversation
3. **Check existing issues** at [GitHub Issues](https://github.com/simplemindedbot/ai-mcp-framework/issues)

### Reporting Issues
When creating a GitHub issue, include:
- **Operating system and version**
- **AI platform and version** (Claude Desktop, API, etc.)
- **Framework version** (git commit hash)
- **Complete error messages**
- **Steps to reproduce**
- **Diagnostic output**

### Community Support
- **GitHub Discussions**: General questions and community help
- **GitHub Issues**: Bug reports and feature requests
- **Framework Documentation**: Comprehensive guides and references

## Validation Checklist

Use this checklist to verify your framework is working correctly:

- [ ] MCP servers install without errors
- [ ] Framework installer completes successfully
- [ ] AI platform recognizes MCP configuration
- [ ] AI automatically tests tools at conversation start
- [ ] AI uses tools proactively without prompting
- [ ] Responses include verification markers (🔍/⚠️)
- [ ] Status reports trigger actual tool testing
- [ ] Framework violations trigger self-correction
- [ ] Memory system persists framework components
- [ ] User corrections integrate into learning system

If all items are checked, your framework is properly configured and functional!