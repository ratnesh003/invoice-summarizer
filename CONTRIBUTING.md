# Contributing to Order Processing System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Submission Guidelines](#submission-guidelines)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive Behavior**:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable Behavior**:
- Trolling, insulting/derogatory comments, personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Project maintainers have the right to remove, edit, or reject comments, commits, code, issues, and other contributions that don't align with this Code of Conduct.

Report unacceptable behavior to: [INSERT CONTACT EMAIL]

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- Python 3.9 or higher installed
- Git for version control
- Familiarity with FastAPI and Streamlit (helpful but not required)
- Read our [Development Guide](DEVELOPMENT.md)

### Setting Up Your Environment

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/order-processing-system.git
   cd order-processing-system
   ```

2. **Set up upstream remote**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/order-processing-system.git
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

5. **Run tests to verify setup**
   ```bash
   pytest
   ```

## How to Contribute

### Ways to Contribute

You don't need to write code to contribute! Here are many ways to help:

**🐛 Report Bugs**
- Check if the bug already exists in issues
- Use the bug report template
- Include reproduction steps and environment details

**✨ Suggest Features**
- Check if the feature is already requested
- Use the feature request template
- Explain the use case and benefits

**📝 Improve Documentation**
- Fix typos or unclear explanations
- Add examples or tutorials
- Translate documentation

**🧪 Write Tests**
- Improve test coverage
- Add edge case tests
- Write integration tests

**💻 Submit Code**
- Fix bugs
- Implement features
- Optimize performance

**👀 Review Pull Requests**
- Test changes locally
- Provide constructive feedback
- Help improve code quality

### First Time Contributors

Look for issues labeled:
- `good first issue` - Easy to tackle for newcomers
- `help wanted` - We need help with these
- `documentation` - Documentation improvements

**Not sure where to start?**
- Review open issues
- Ask in discussions
- Reach out to maintainers

## Development Process

### 1. Find or Create an Issue

Before writing code:
1. Check if an issue exists
2. If not, create one describing your proposal
3. Wait for feedback/approval from maintainers
4. Discuss approach if it's a significant change

### 2. Create a Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Write code following our [style guidelines](#style-guidelines)
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Commit Your Changes

Follow our commit message convention:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style/formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Example**:
```
feat(api): add customer filtering endpoint

Add /api/customers endpoint with filtering by name and date range.
Includes pagination and sorting support.

Closes #123
```

### 5. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create PR on GitHub
```

## Submission Guidelines

### Pull Request Process

1. **Before Submitting**:
   - [ ] All tests pass (`pytest`)
   - [ ] Code is formatted (`black`, `isort`)
   - [ ] No linting errors (`flake8`)
   - [ ] Documentation updated if needed
   - [ ] Branch is up to date with main

2. **PR Title**:
   - Use the same format as commit messages
   - Be descriptive and concise
   - Example: `feat(api): add customer filtering`

3. **PR Description**:
   Use the template provided:
   ```markdown
   ## Description
   What does this PR do?
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation
   
   ## How Has This Been Tested?
   Describe your testing approach
   
   ## Checklist
   - [ ] Tests pass
   - [ ] Code follows style guide
   - [ ] Documentation updated
   - [ ] No breaking changes
   
   ## Related Issues
   Closes #123
   ```

4. **Review Process**:
   - Automated checks run (tests, linting)
   - At least one maintainer review required
   - Address feedback promptly
   - Keep discussion professional and constructive

5. **After Approval**:
   - Maintainer will merge your PR
   - Your contribution will be credited
   - Thank you! 🎉

### Reporting Bugs

**Before Submitting**:
- Check if the bug already exists
- Test with the latest version
- Verify it's reproducible

**Bug Report Template**:
```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen?

**Actual Behavior**
What actually happens?

**Screenshots**
If applicable

**Environment**:
- OS: [e.g., Windows 10, macOS 12]
- Python Version: [e.g., 3.9.5]
- Browser: [e.g., Chrome 120]

**Additional Context**
Any other relevant information
```

### Suggesting Features

**Feature Request Template**:
```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
How should it work?

**Describe alternatives considered**
Other approaches you've thought about

**Additional Context**
Mockups, examples, or relevant info

**Would you be willing to implement this?**
Yes/No
```

## Style Guidelines

### Python Code Style

We follow **PEP 8** with these tools:

**Formatting**:
```bash
# Format with Black
black backend/ frontend/ tests/

# Sort imports
isort backend/ frontend/ tests/
```

**Linting**:
```bash
# Check with Flake8
flake8 backend/ frontend/ tests/

# Type checking
mypy backend/
```

### Code Quality

**Good Practices**:
- Use type hints
- Write descriptive variable names
- Keep functions small and focused
- Add docstrings to public functions
- Handle errors appropriately
- Write tests for new code

**Example**:
```python
from typing import Optional

def calculate_discount(amount: float, rate: float) -> float:
    """
    Calculate discount amount.
    
    Args:
        amount: The base amount
        rate: Discount rate (0.0 to 1.0)
        
    Returns:
        The discount amount
        
    Raises:
        ValueError: If rate is invalid
    """
    if not 0 <= rate <= 1:
        raise ValueError(f"Rate must be between 0 and 1, got {rate}")
    
    return amount * rate
```

### Documentation Style

**Docstrings**: Use Google style
**Comments**: Explain why, not what
**Markdown**: Follow standard markdown conventions

### Git Commit Guidelines

**Structure**:
```
type(scope): subject

body (optional)

footer (optional)
```

**Rules**:
- Use imperative mood: "add" not "added"
- First line ≤ 72 characters
- Capitalize first letter
- No period at end
- Reference issues in footer

### Testing Guidelines

**Test Structure**:
```python
def test_function_name_behavior():
    """Should describe expected behavior."""
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_value
```

**Coverage**:
- Aim for >80% coverage
- Test happy paths
- Test error cases
- Test edge cases

## Community

### Communication Channels

**GitHub**:
- Issues: Bug reports, feature requests
- Discussions: Questions, ideas, help
- Pull Requests: Code contributions

**Response Times**:
- Issues: Within 48 hours
- Pull Requests: Within 1 week
- Security Issues: Within 24 hours

### Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors list

Thank you for contributing! 💙

### Getting Help

**Stuck?** Don't hesitate to ask:
- Comment on the issue
- Open a discussion
- Tag maintainers if urgent

**Resources**:
- [Development Guide](DEVELOPMENT.md)
- [Architecture Docs](ARCHITECTURE.md)
- [API Reference](API.md)

## Additional Resources

### Learning Resources

**FastAPI**:
- Official Tutorial: https://fastapi.tiangolo.com/tutorial/
- Async Programming: https://fastapi.tiangolo.com/async/

**Streamlit**:
- Get Started: https://docs.streamlit.io/get-started
- API Reference: https://docs.streamlit.io/library/api-reference

**Testing**:
- Pytest Docs: https://docs.pytest.org/
- Testing Best Practices: https://docs.pytest.org/en/latest/goodpractices.html

**Python**:
- PEP 8 Style Guide: https://pep8.org/
- Type Hints: https://docs.python.org/3/library/typing.html

### Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

### Release Process

See [DEVELOPMENT.md](DEVELOPMENT.md) for release workflow.

---

## Questions?

Feel free to reach out if you have questions about contributing. We're here to help!

**Happy Contributing! 🚀**
