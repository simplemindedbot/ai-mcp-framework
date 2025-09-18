# AUTOPILOT Framework: Compiled AI Directives

## Overview

The AUTOPILOT Framework is an optimization layer built on top of the core AI-MCP Framework. It addresses the challenge of token efficiency when providing complex behavioral rules to a Large Language Model (LLM).

While the source files in the `/framework` directory are designed to be human-readable for auditability and development, they are not optimized for an LLM's context window. Passing verbose, descriptive rules on every interaction is token-intensive and costly.

The AUTOPILOT framework introduces a "compilation" step that transforms these human-readable rules into a compact, machine-optimized format.

## The Compilation Process

A dedicated script, `tools/framework_compiler.py`, performs this transformation. The process involves:

1.  **Ingestion:** The compiler reads the source `.txt` and `.json` rule files.
2.  **Abstraction & Compaction:**
    *   For narrative directives (e.g., `prime-directive-v2.txt`), it extracts the core, actionable commands and strips the descriptive prose.
    *   For configuration files (e.g., `authenticity-controls.json`), it removes descriptive metadata and flattens the data structure into its most essential form.
3.  **Serialization:** The compiler merges all the compacted rules into a single JSON object.
4.  **Output:** The final, token-efficient ruleset is saved as `framework/autopilot-rules.json`.

## Benefits

-   **Token Efficiency:** Drastically reduces the number of tokens required to load the framework's rules into the LLM's context, leading to lower operational costs and faster processing.
-   **Separation of Concerns:** Maintains a clear distinction between the human-readable "source" rules and the machine-readable "compiled" rules.
-   **Performance:** A smaller context allows the model to process instructions more quickly.

This compiled `autopilot-rules.json` file is the payload that the AI system loads at runtime, giving it the complete set of behavioral instructions in the most efficient way possible.
