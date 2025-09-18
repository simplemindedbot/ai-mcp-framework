# Contributing to AI MCP Framework

Thank you for your interest in contributing to the AI MCP Framework! This project aims to solve the tool adoption problem in AI systems while maintaining safety and authenticity.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to creating a welcoming and inclusive environment for all contributors.

## Getting Started

### Prerequisites
- Read the [README.md](README.md) to understand the project
- Complete the [Setup Tutorial](docs/setup-tutorial.md) to get a working installation
- Familiarize yourself with the [Architecture](docs/architecture.md)

### Areas for Contribution
We welcome contributions in these areas:

1. **Framework Enhancement**
   - Additional safety protocols
   - New authenticity validation mechanisms
   - Performance optimizations
   - Cross-platform compatibility

2. **MCP Server Integration**
   - Support for new MCP servers
   - Improved server testing and validation
   - Configuration management tools

3. **Documentation**
   - Tutorial improvements
   - Use case examples
   - Troubleshooting guides
   - API documentation

4. **Testing and Quality Assurance**
   - Unit tests for framework components
   - Integration tests with real MCP servers
   - Performance benchmarks
   - User experience testing

5. **Tools and Utilities**
   - Installation and setup automation
   - Monitoring and debugging tools
   - Migration utilities
   - Configuration validators

## How to Contribute

### Reporting Issues
Before creating an issue:
1. Check [existing issues](https://github.com/simplemindedbot/ai-mcp-framework/issues)
2. Use the [troubleshooting guide](docs/troubleshooting.md)
3. Gather diagnostic information

When reporting issues, include:
- **Description**: Clear description of the problem
- **Environment**: OS, AI platform version, Node.js/Python versions
- **Steps to Reproduce**: Minimal steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Logs/Output**: Relevant error messages or logs
- **Additional Context**: Screenshots, configuration files, etc.

### Suggesting Enhancements
For feature requests or enhancements:
1. Check if similar suggestions exist in issues/discussions
2. Describe the motivation and use case
3. Provide detailed description of proposed changes
4. Consider implementation complexity and maintenance burden

### Submitting Code Changes

#### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ai-mcp-framework.git
cd ai-mcp-framework

# Add upstream remote
git remote add upstream https://github.com/simplemindedbot/ai-mcp-framework.git
```

#### 2. Create a Branch
```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or a bugfix branch
git checkout -b bugfix/issue-description
```

#### 3. Make Changes
Follow our [Contribution Guidelines](#contribution-guidelines) when making changes.

#### 4. Test Your Changes
```bash
# Run framework installer tests
python tools/framework-installer.py --help

# Test knowledge graph importer
python tools/knowledge-graph-importer.py --help

# Validate JSON configuration files
python -m json.tool framework/authenticity-controls.json
python -m json.tool framework/hierarchical-learning.json
python -m json.tool framework/safety-protocols.json
```

#### 5. Commit and Push
```bash
# Add your changes
git add .

# Commit with descriptive message
git commit -m "Add feature: brief description

- Detailed explanation of changes
- Why these changes are needed
- Any breaking changes or migration notes"

# Push to your fork
git push origin feature/your-feature-name
```

#### 6. Create Pull Request
1. Go to the GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template
5. Submit for review

## Development Setup

### Local Development Environment
```bash
# Clone repository
git clone https://github.com/simplemindedbot/ai-mcp-framework.git
cd ai-mcp-framework

# Install development dependencies
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-web-search

# Set up Python virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Test framework installation
python tools/framework-installer.py --help
```

### Testing Framework Changes
```bash
# Test with clean installation
rm -rf ~/.config/claude/memory-data/  # Clear previous data
python tools/framework-installer.py

# Test knowledge graph import
python tools/knowledge-graph-importer.py

# Validate configuration files
for file in framework/*.json; do
  echo "Validating $file"
  python -m json.tool "$file" > /dev/null
done
```

## Contribution Guidelines

### Code Style

#### Python Code
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use meaningful variable and function names
- Include docstrings for functions and classes
- Add type hints where appropriate

```python
def load_framework_components() -> Dict[str, Any]:
    """Load all framework JSON files from the framework directory.

    Returns:
        Dict mapping component names to their configuration data.
    """
    framework_dir = Path(__file__).parent.parent / "framework"
    # ... implementation
```

#### JSON Configuration
- Use consistent indentation (2 spaces)
- Include descriptions for complex configurations
- Validate JSON syntax before committing

```json
{
  "component_name": {
    "description": "Clear description of what this component does",
    "priority": "High",
    "settings": {
      "key": "value"
    }
  }
}
```

#### Documentation
- Use clear, concise language
- Include code examples where helpful
- Update relevant documentation when making changes
- Follow existing documentation structure

### Framework Design Principles

When contributing framework enhancements, follow these principles:

#### 1. Safety First
- All experimental features require human approval
- Implement fail-safe behaviors
- Preserve core safety boundaries
- Include rollback mechanisms

#### 2. Authenticity Over Performance
- Verify claims before making them
- Mark assumptions clearly
- Prefer honest "I don't know" over confident guessing
- Test actual capabilities, don't assume them

#### 3. Simplicity and Clarity
- Favor simple solutions over complex ones
- Make behaviors predictable and understandable
- Document the reasoning behind design decisions
- Avoid feature creep

#### 4. User Agency
- Maintain human oversight and control
- Provide transparency in AI decision-making
- Allow users to understand and modify behaviors
- Respect user preferences and boundaries

### Adding New Framework Components

When adding new components to the framework:

1. **Create in appropriate directory**:
   - `framework/` for core behavioral rules
   - `tools/` for installation and utility scripts
   - `examples/` for reference configurations
   - `docs/` for documentation

2. **Follow naming conventions**:
   - Use descriptive, hyphenated names
   - Include version numbers for major changes
   - Add clear file extensions

3. **Include proper metadata**:
   ```json
   {
     "component_name": "New Component",
     "version": "1.0",
     "description": "What this component does",
     "priority": "Medium",
     "scope": "Where this applies"
   }
   ```

4. **Update related files**:
   - Add to framework installer if needed
   - Update documentation
   - Include in examples if appropriate

### Adding MCP Server Support

When adding support for new MCP servers:

1. **Test server functionality** thoroughly
2. **Update configuration examples**
3. **Add to installation scripts** if appropriate
4. **Document setup requirements**
5. **Include troubleshooting guidance**

## Testing

### Manual Testing Checklist
Before submitting contributions, verify:

- [ ] Framework installer completes without errors
- [ ] All JSON configuration files are valid
- [ ] Documentation builds and renders correctly
- [ ] Examples work as described
- [ ] Changes don't break existing functionality
- [ ] New features work across different platforms

### Automated Testing
We encourage adding automated tests for new features:

```python
def test_framework_component_loading():
    """Test that framework components load correctly."""
    components = load_framework_components()
    assert 'authenticity-controls' in components
    assert 'hierarchical-learning' in components
    # ... additional assertions
```

### User Experience Testing
For UI/UX changes:
- Test with different AI platforms
- Verify accessibility
- Get feedback from other users
- Document any platform-specific considerations

## Documentation

### Documentation Standards
- Write for your audience (beginners vs. advanced users)
- Use clear headings and structure
- Include practical examples
- Keep language inclusive and welcoming
- Update related documentation when making changes

### Types of Documentation
1. **User Guides**: Help users accomplish specific tasks
2. **Reference Documentation**: Comprehensive coverage of features
3. **Tutorials**: Step-by-step learning experiences
4. **Architecture Docs**: Technical design and implementation details

### Building Documentation Locally
```bash
# Preview documentation changes
# (Add instructions for your documentation system)
```

## Community

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community chat
- **Pull Request Reviews**: Code discussion and feedback

### Getting Help
- Check the [troubleshooting guide](docs/troubleshooting.md)
- Search existing issues and discussions
- Ask questions in GitHub Discussions
- Reach out to maintainers for guidance

### Recognition
Contributors are recognized in:
- CONTRIBUTORS.md file (automatically updated)
- Release notes for significant contributions
- Project documentation acknowledgments

## Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers incremented
- [ ] Release notes prepared

## Questions?

If you have questions about contributing:
1. Check this guide and other documentation
2. Search existing issues and discussions
3. Ask in GitHub Discussions
4. Contact maintainers directly for sensitive questions

Thank you for contributing to the AI MCP Framework! Your help makes AI systems more capable, authentic, and trustworthy.