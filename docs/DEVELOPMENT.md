# Development Guide

Guidelines for contributing to the Order Processing System.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Git Workflow](#git-workflow)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)
- [Common Development Tasks](#common-development-tasks)

## Getting Started

### Development Environment Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/order-processing-system.git
   cd order-processing-system
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

### Required Development Tools

- **Python 3.9+**: Core runtime
- **Git**: Version control
- **Code Editor**: VS Code, PyCharm, or similar
- **Postman/curl**: API testing
- **pytest**: Test runner

### Recommended VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "tamasfe.even-better-toml",
    "redhat.vscode-yaml"
  ]
}
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch Naming Conventions**:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/updates

### 2. Make Changes

Write your code following our [Code Standards](#code-standards).

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_processor.py

# Run specific test
pytest tests/test_processor.py::test_parse_order_line_valid
```

### 4. Check Code Quality

```bash
# Format code with Black
black backend/ frontend/ tests/

# Sort imports
isort backend/ frontend/ tests/

# Lint with Flake8
flake8 backend/ frontend/ tests/

# Type check with mypy
mypy backend/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add customer filtering feature"
```

**Commit Message Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build/tooling changes

**Examples**:
```
feat(api): add customer filtering endpoint

Add new /api/customers endpoint with name and date range filtering.
Includes pagination support and sorting options.

Closes #123
```

```
fix(processor): handle empty customer names correctly

Previously crashed when customer_name was empty string.
Now logs validation error and continues processing.

Fixes #456
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Line length: 100 characters (not 79)
# Use double quotes for strings
# Use type hints

from typing import List, Optional
from datetime import date


def process_orders(
    orders: List[str],
    validate: bool = True
) -> tuple[str, str]:
    """
    Process a list of order lines.
    
    Args:
        orders: List of pipe-delimited order strings
        validate: Whether to perform validation
        
    Returns:
        Tuple of (output_report, error_log)
        
    Raises:
        ValueError: If orders list is empty
    """
    if not orders:
        raise ValueError("Orders list cannot be empty")
    
    # Implementation here
    return output, errors
```

### Code Formatting

**Black Configuration** (pyproject.toml):
```toml
[tool.black]
line-length = 100
target-version = ['py39']
include = '\.pyi?$'
```

**isort Configuration**:
```toml
[tool.isort]
profile = "black"
line_length = 100
```

### Type Hints

Use type hints throughout:

```python
# Good
def calculate_discount(amount: float, rate: float) -> float:
    return amount * rate

# Avoid
def calculate_discount(amount, rate):
    return amount * rate
```

### Docstrings

Use Google-style docstrings:

```python
def parse_order_line(line: str) -> tuple[Optional[Order], Optional[str]]:
    """
    Parse a single order line into an Order object.
    
    Args:
        line: Pipe-delimited order string
        
    Returns:
        Tuple of (Order object, error message)
        Order is None if parsing fails
        Error message is None if parsing succeeds
        
    Example:
        >>> order, error = parse_order_line("ORD001|John|Laptop|2|999.99|2024-03-15")
        >>> print(order.customer_name)
        John
    """
    pass
```

### Error Handling

```python
# Good: Specific exceptions with clear messages
try:
    quantity = int(quantity_str)
    if quantity < 0:
        raise ValueError(f"Quantity must be non-negative, got {quantity}")
except ValueError as e:
    logger.error(f"Invalid quantity: {e}")
    return None, str(e)

# Avoid: Bare except or generic errors
try:
    quantity = int(quantity_str)
except:
    return None, "Error"
```

### Logging

Use Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)

# Good
logger.info(f"Processing file: {filename}")
logger.warning(f"Invalid order detected: {order_id}")
logger.error(f"Failed to parse line: {line}", exc_info=True)

# Avoid print statements in production code
print("Processing...")  # Don't do this
```

## Testing

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_processor.py     # Business logic tests
├── test_routes.py        # API endpoint tests
└── test_models.py        # Data model tests
```

### Writing Tests

```python
import pytest
from backend.core.processor import parse_order_line


class TestOrderParsing:
    """Tests for order line parsing."""
    
    def test_parse_valid_order(self):
        """Should parse a valid order line correctly."""
        line = "ORD001|John Smith|Laptop|2|999.99|2024-03-15"
        order, error = parse_order_line(line)
        
        assert error is None
        assert order is not None
        assert order.order_id == "ORD001"
        assert order.customer_name == "John Smith"
        assert order.quantity == 2
    
    def test_parse_invalid_quantity(self):
        """Should reject negative quantities."""
        line = "ORD001|John Smith|Laptop|-2|999.99|2024-03-15"
        order, error = parse_order_line(line)
        
        assert order is None
        assert error is not None
        assert "quantity" in error.lower()
    
    @pytest.mark.parametrize("line,expected_error", [
        ("ORD001|John|Laptop|abc|999.99|2024-03-15", "quantity format"),
        ("ORD001|John|Laptop|2|xyz|2024-03-15", "price format"),
        ("ORD001|John|Laptop|2|999.99|15-03-2024", "date format"),
    ])
    def test_parse_various_errors(self, line, expected_error):
        """Should handle various validation errors."""
        order, error = parse_order_line(line)
        
        assert order is None
        assert expected_error in error.lower()
```

### Test Coverage

Maintain >80% code coverage:

```bash
# Generate coverage report
pytest --cov=backend --cov-report=html

# View report
open htmlcov/index.html
```

### Fixtures

Use pytest fixtures for common test data:

```python
# conftest.py
import pytest
from datetime import date
from backend.core.models import Order


@pytest.fixture
def sample_order():
    """Sample order for testing."""
    return Order(
        order_id="ORD001",
        customer_name="John Smith",
        product_name="Laptop",
        quantity=2,
        unit_price=999.99,
        order_date=date(2024, 3, 15)
    )


@pytest.fixture
def sample_orders_file(tmp_path):
    """Create a temporary orders file."""
    file_path = tmp_path / "orders.txt"
    file_path.write_text(
        "ORD001|John Smith|Laptop|2|999.99|2024-03-15\n"
        "ORD002|Jane Doe|Mouse|1|25.50|2024-03-16\n"
    )
    return file_path
```

## Git Workflow

### Branch Strategy

```
main (protected)
  ├── develop (integration branch)
  │     ├── feature/add-filtering
  │     ├── feature/improve-validation
  │     └── fix/discount-calculation
  └── hotfix/critical-bug
```

### Commit Guidelines

**Good Commits**:
- Atomic: One logical change per commit
- Descriptive: Clear message explaining what and why
- Tested: All tests pass

**Bad Commits**:
- "WIP" or "fixes"
- Multiple unrelated changes
- Breaking tests

### Rebase vs Merge

**For feature branches**: Use rebase for clean history
```bash
git checkout feature/your-feature
git rebase develop
```

**For merging to main**: Use merge commits
```bash
git checkout develop
git merge --no-ff feature/your-feature
```

## Pull Request Process

### Before Creating PR

- [ ] All tests pass locally
- [ ] Code is formatted (black, isort)
- [ ] No linting errors (flake8)
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow convention

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested these changes

## Checklist
- [ ] Tests pass
- [ ] Code is formatted
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Fixes #123
Related to #456
```

### Review Process

1. **Automated Checks**: CI/CD runs tests
2. **Code Review**: At least one approval required
3. **Discussion**: Address reviewer comments
4. **Merge**: Squash and merge or rebase

## Project Structure

```
backend/
├── __init__.py
├── main.py                 # FastAPI app
├── api/
│   ├── __init__.py
│   └── routes.py          # Endpoint handlers
├── core/
│   ├── __init__.py
│   ├── models.py          # Pydantic models
│   ├── processor.py       # Business logic
│   └── utils.py           # Helper functions
└── data/                  # Data storage

frontend/
└── app.py                 # Streamlit UI

tests/
├── __init__.py
├── conftest.py
├── test_processor.py
├── test_routes.py
└── test_models.py
```

### Adding New Files

**Backend Module**:
```python
# backend/core/new_module.py
"""
Module for new functionality.

This module handles...
"""
from typing import List
import logging

logger = logging.getLogger(__name__)


def new_function() -> None:
    """Function description."""
    pass
```

**Test File**:
```python
# tests/test_new_module.py
"""Tests for new_module functionality."""
import pytest
from backend.core.new_module import new_function


class TestNewFunction:
    """Test suite for new_function."""
    
    def test_basic_functionality(self):
        """Should work correctly."""
        pass
```

## Common Development Tasks

### Adding a New API Endpoint

1. **Define route in routes.py**:
```python
@router.get("/customers")
async def get_customers(
    name: Optional[str] = None
) -> List[CustomerSummary]:
    """Get list of customers with optional filtering."""
    # Implementation
    pass
```

2. **Add tests**:
```python
def test_get_customers_endpoint(client):
    response = client.get("/api/customers")
    assert response.status_code == 200
```

3. **Update API documentation** in API.md

### Adding Business Logic

1. **Add function to processor.py**:
```python
def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax amount."""
    return amount * rate
```

2. **Add tests**:
```python
def test_calculate_tax():
    assert calculate_tax(100.0, 0.08) == 8.0
```

3. **Update documentation**

### Adding a Data Model

1. **Define in models.py**:
```python
class TaxInfo(BaseModel):
    rate: float
    amount: float
    total: float
```

2. **Add validation**:
```python
@validator('rate')
def rate_must_be_positive(cls, v):
    if v < 0:
        raise ValueError('Rate must be positive')
    return v
```

3. **Add tests** for validation

### Debugging Tips

**Backend**:
```python
# Add breakpoints
import pdb; pdb.set_trace()

# Or use built-in debugger
import ipdb; ipdb.set_trace()

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend**:
```python
# Streamlit debugging
st.write("Debug:", variable)
st.json(data_structure)

# Check session state
st.write(st.session_state)
```

### Performance Profiling

```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')
    stats.print_stats(10)
```

## Dependencies Management

### Adding Dependencies

```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Dependency Guidelines

- Use specific versions: `fastapi==0.100.0`
- Document why package is needed
- Check for security vulnerabilities
- Prefer well-maintained packages

## Documentation

### Code Documentation

- All public functions need docstrings
- Complex logic needs inline comments
- Update README.md for user-facing changes
- Update ARCHITECTURE.md for design changes

### API Documentation

FastAPI auto-generates docs, but:
- Add descriptions to endpoints
- Document request/response examples
- Note any breaking changes

## Release Process

1. Update version in `__version__.py`
2. Update CHANGELOG.md
3. Create release branch: `release/v1.2.0`
4. Final testing
5. Merge to main
6. Create GitHub release with tag
7. Deploy to production

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Bugs**: Create an issue with reproduction steps
- **Features**: Propose in discussions first
- **Urgent**: Tag maintainers in PR/issue

## Code of Conduct

Be respectful, inclusive, and professional. See CODE_OF_CONDUCT.md.

---

**Happy Coding! 🚀**
