# Implementation Guide

## Overview

This guide walks you through implementing the AI MCP Framework step by step. The framework creates AI systems that automatically use MCP tools while maintaining authenticity and safety.

## Prerequisites

- MCP (Model Context Protocol) compatible AI system
- MCP memory server configured and accessible
- Basic understanding of AI preferences/prompting

## Step 1: MCP Server Setup

1. **Install Required MCP Servers**
   ```bash
   # Essential servers
   npm install -g @modelcontextprotocol/server-memory
   npm install -g @modelcontextprotocol/server-filesystem  
   npm install -g @modelcontextprotocol/server-web-search
   npm install -g @modelcontextprotocol/server-fetch
   
   # Recommended servers
   npm install -g @modelcontextprotocol/server-ddg-search
   npm install -g @modelcontextprotocol/server-arxiv
   npm install -g @modelcontextprotocol/server-wikipedia
   ```

2. **Configure MCP Servers**
   - Copy `examples/mcp-config-example.json` to your MCP configuration
   - Adjust file paths and environment variables as needed
   - Ensure memory server has write access to store framework data

## Step 2: Knowledge Graph Setup

1. **Import Framework Components**
   ```bash
   # Use your MCP memory server to import the framework
   python tools/knowledge-graph-importer.py
   ```

2. **Verify Knowledge Graph**
   - Confirm framework entities are accessible
   - Test memory server read/write operations
   - Validate relationships between components

## Step 3: Framework Deployment

### Option A: Automated Deployment (Recommended)

1. **Interactive Deployment**
   ```bash
   # Comprehensive deployment with file discovery
   python tools/deploy-smart-framework.py --interactive
   ```

   This will:
   - Discover all CLAUDE.md files (Claude Code + Claude Desktop)
   - Analyze and classify framework vs project configs
   - Deploy token-optimized framework to appropriate locations
   - Create automatic backups for rollback capability

2. **Quick Deployment**
   ```bash
   # Deploy specific optimization level
   python tools/deploy-smart-framework.py --optimization optimized    # 70-85% token savings
   python tools/deploy-smart-framework.py --optimization lightweight  # 80-90% token savings
   python tools/deploy-smart-framework.py --optimization emergency    # 90-95% token savings
   ```

3. **Verify Deployment**
   ```bash
   # Check deployment status
   python tools/deploy-smart-framework.py --status
   ```

### Option B: Manual Configuration

1. **Set Prime Directive**
   - Copy content from `framework/smart-memory-directive.txt` (token-optimized v2.2)
   - OR copy `framework/prime-directive-v2.txt` (full-featured v2.0)
   - Set as highest priority in your AI system preferences
   - Ensure it overrides other behavioral rules

2. **Configure Authenticity Controls**
   - Import `framework/authenticity-controls.json` into memory system
   - Verify self-audit questions are accessible
   - Test verification marker functionality

## Step 4: Safety Protocol Implementation

1. **Load Safety Governance**
   - Import `framework/safety-protocols.json`
   - Configure hierarchical learning system
   - Set up experimental rule approval process

2. **Test Safety Boundaries**
   - Verify experimental rules require approval
   - Test auto-correction protocol
   - Confirm user correction integration

## Step 5: Verification and Testing

1. **Token Optimization Test**
   - Monitor memory query frequency (should be once per session vs. per-interaction)
   - Observe tool testing caching (should use cached results)
   - Check session-based learning updates
   - Verify 70-85% reduction in framework-related token usage

2. **Automatic Tool Usage Test**
   - Start new AI interaction
   - Observe automatic MCP tool testing (smart/cached approach)
   - Verify proactive tool utilization
   - Check tool selection uses cached performance data

3. **Authenticity Validation Test**
   - Look for 🔍 VERIFIED vs ⚠️ ASSUMED markers
   - Test user-calibrated validation levels
   - Verify external verification triggers (selective application)
   - Check cached self-audit question usage

4. **Safety Protocol Test**
   - Attempt to create experimental rule
   - Confirm user approval requirement
   - Test auto-correction on framework violation

## Step 6: Monitoring and Optimization

1. **Track Success Metrics**
   - Monitor automatic MCP tool usage frequency
   - Measure token efficiency (target: 70-85% reduction)
   - Assess authenticity marker accuracy
   - Track user interaction quality improvements
   - Monitor session cache hit rates

2. **Learning Integration**
   - Observe user correction incorporation (immediate caching)
   - Monitor hierarchical rule progression
   - Track mistake learning effectiveness
   - Verify cross-session learning persistence

3. **Usage Analysis**
   ```bash
   # Analyze token usage patterns
   python tools/token-optimizer.py --analyze --daily-interactions 20 --tokens-per-interaction 2000 --daily-budget 50000

   # Generate optimization recommendations
   python tools/token-optimizer.py --generate-directive optimized --output custom-directive.txt
   ```

## Troubleshooting

### Deployment Issues
```bash
# Rollback to previous framework
python tools/deploy-smart-framework.py --rollback

# Check current status
python tools/deploy-smart-framework.py --status
```

### Token Usage Still High
- Verify smart memory directive (v2.2) is deployed, not v2.0
- Check session cache is functioning (memory queries should be once per session)
- Monitor tool testing frequency (should use cached results)
- Consider emergency mode for maximum savings

### MCP Tools Not Used Automatically
- Verify prime directive is set as highest priority
- Check MCP server accessibility and configuration
- Confirm memory server contains framework components
- Verify cached tool availability data

### Authenticity Markers Missing
- Check if user-calibrated validation is being applied
- Verify authenticity controls are loaded in memory
- Confirm selective validation triggers are working
- Check cached self-audit question accessibility

### Safety Protocols Not Working
- Verify safety governance rules are imported
- Check experimental rule flagging system
- Confirm user approval process configuration

### Learning Not Occurring
- Check session-based cache updates
- Verify user correction integration setup
- Confirm memory server write permissions
- Monitor batch learning updates at session end

## Advanced Configuration

### Custom MCP Servers
- Add your custom servers to MCP configuration
- Update prime directive to include new tools
- Test automatic utilization of custom capabilities

### Domain-Specific Rules
- Create tertiary rules for specific contexts
- Follow hierarchical learning promotion process
- Maintain alignment with core framework principles

### Integration with Existing Systems
- Map framework components to your existing AI architecture
- Maintain compatibility with current behavioral rules
- Gradually migrate to framework-based approach

## Support

For implementation questions or issues:
1. Check the troubleshooting section above
2. Review framework documentation in `/docs`
3. Examine working examples in `/examples`
4. Open an issue in the repository

## Next Steps

After successful implementation:
1. Monitor framework effectiveness over time
2. Contribute improvements back to the project
3. Share results and lessons learned
4. Explore advanced framework customizations