# GEMINI.md: AI MCP Framework

## Directory Overview

This directory contains the AI MCP Framework, a system for developing proactive, authentic, and safe AI systems that leverage MCP (Model Context Protocol) tools. The framework is defined through a series of configuration files (`.json`) and directives (`.txt`) that guide the AI's behavior. The primary goal is to encourage AI systems to automatically and effectively use available tools without explicit user commands, while maintaining a strong sense of authenticity and avoiding behavioral drift.

The core of the project is the `framework` directory, which contains the files that define the AI's behavior. The `tools` directory contains Python scripts for installing, deploying, and managing the framework. The `docs` directory provides documentation, and the `examples` directory shows sample configurations and data.

## Project Goals

The AI MCP Framework aims to solve several key problems in AI development:

*   **Tool Adoption Gap:** Encourages AIs to use available MCP tools without needing explicit prompts.
*   **Performative Behavior:** Prevents AIs from making claims they cannot verify, ensuring authenticity.
*   **Behavioral Drift:** Mitigates the tendency of AI systems to degrade in performance or helpfulness over time.
*   **Safe Learning:** Provides a hierarchical structure for AI learning that prevents core directives from being compromised.
*   **Token Optimization:** Reduces the number of tokens used in interactions through smart caching and other efficiencies.

## Dependencies

### System Requirements
*   **Python**: 3.8 or higher
*   **Node.js**: 18 or higher
*   **npm**: 8.19 or higher

### Required MCP Servers
*   `@modelcontextprotocol/server-memory`
*   `@modelcontextprotocol/server-filesystem`
*   `@modelcontextprotocol/server-web-search` or `@modelcontextprotocol/server-ddg-search`
*   `@modelcontextprotocol/server-fetch`

## Getting Started Guide

1.  **Install MCP Servers:**
    ```bash
    npm install -g @modelcontextprotocol/server-memory
    npm install -g @modelcontextprotocol/server-filesystem
    npm install -g @modelcontextprotocol/server-web-search
    npm install -g @modelcontextprotocol/server-fetch
    ```
2.  **Deploy the Framework:**
    ```bash
    python tools/deploy-smart-framework.py --interactive
    ```
3.  **Verify Installation:**
    *   Observe the AI's behavior for proactive tool usage.
    *   Look for authenticity markers (🔍 VERIFIED vs ⚠️ ASSUMED) in the AI's responses.
    *   Confirm that the AI tests for tool availability at the start of an interaction.

## Key Files

*   `framework/prime-directive-v2.txt`: The central directive that governs the AI's behavior. It mandates proactive tool use, authenticity checks, and a continuous learning loop.
*   `framework/hierarchical-learning.json`: Defines a four-tiered learning system (Prime, Secondary, Tertiary, Quaternary) that allows for safe and controlled behavioral evolution. It prevents core directives from being overwritten by new learnings.
*   `framework/authenticity-controls.json`: A framework for ensuring the AI's claims are genuine and not "performative." It includes self-audit questions, verification markers, and metrics for tracking authenticity.
*   `framework/safety-protocols.json`: A set of protocols to ensure the safe operation of the AI, including human-in-the-loop safeguards and auto-correction mechanisms.
*   `tools/deploy-smart-framework.py`: A Python script for deploying the framework with token optimization.
*   `tools/framework-installer.py`: A Python script for manual installation of the framework.
*   `README.md`: Provides a comprehensive overview of the project, its goals, and how to use it.

## Customization and Extension

The framework is designed to be customizable. You can modify the AI's behavior by editing the files in the `framework` directory. For example, you could:

*   **Add new self-audit questions** to `authenticity-controls.json`.
*   **Define new contextual rules** in `hierarchical-learning.json`.
*   **Modify the core behavior** by editing `prime-directive-v2.txt`.

The hierarchical learning system allows for the safe integration of new behaviors. New learnings are classified and integrated according to the rules in `hierarchical-learning.json`, ensuring that the core directives are not compromised.

## Development Conventions

*   **Versioning:** Files are versioned using suffixes like `-v2` to track major changes.
*   **JSON Schema:** Configuration files use a consistent and well-documented JSON schema.
*   **Descriptive Naming:** Files and directories are named descriptively to make the project structure easy to understand.