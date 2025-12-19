# Contributing to ConsoleMod

## Overview

ConsoleMod is a hobby project from 404Development LLC. While we don't accept external contributions through traditional means, we welcome feedback, suggestions, and bug reports.

## Code of Conduct

- Be respectful and constructive
- Focus on the code, not the person
- Maintain professional communication
- Respect the project's license and restrictions

## Reporting Issues

### Bug Reports

When reporting bugs, include:

1. **Python version** - `python --version`
2. **Operating system** - Windows, macOS, Linux
3. **ConsoleMod version** - Check `__version__.py`
4. **Steps to reproduce** - Clear, minimal steps
5. **Expected behavior** - What should happen
6. **Actual behavior** - What actually happens
7. **Traceback** - Full error stack if applicable
8. **Minimal reproducible example** - Small code snippet

### Feature Requests

For feature suggestions:

1. **Clear title** - Concise description
2. **Use case** - Why is this feature needed?
3. **Example usage** - How would it be used?
4. **Implementation ideas** - Optional suggestions
5. **Alternatives** - Any workarounds?

### Contact

Email: consolemod@404development.dev

## Code Style

### Python Style Guide

Follow PEP 8 with these modifications:

- **Line length**: 100 characters (see pyproject.toml)
- **Type hints**: Use for all public functions
- **Docstrings**: Google-style docstrings

### Type Hints Example

```python
async def awrite(self, message: str, style: Optional[str] = None) -> None:
    """Write message to pane asynchronously.
    
    Args:
        message: Text to write
        style: Optional Rich style string
    """
    pass
```

### Docstring Format

```python
def method(self, param1: str, param2: int) -> bool:
    """Brief one-line description.
    
    Longer multi-line description if needed.
    More details about behavior and side effects.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When this condition occurs
        RuntimeError: When that condition occurs
    """
```

## Code Organization

### Module Structure

Maintain the existing module structure:

```
consolemod/
├── core/          # Core UI components
├── ui/            # Visual components
├── input/         # Input handling
├── logging/       # Logging utilities
├── monitoring/    # Performance monitoring
└── utils/         # Helper utilities
```

### File Organization

- One class per file when possible
- Related utilities in module files
- Keep files under 500 lines
- Clear separation of concerns

## Testing Requirements

### Test Coverage

New code should have:

- 90%+ line coverage
- Tests for all public methods
- Tests for error conditions
- Integration tests where applicable

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=consolemod

# Run specific test file
pytest tests/test_core.py -v
```

### Writing Tests

Example test:

```python
def test_feature(self):
    """Test description."""
    # Arrange
    obj = Object()
    
    # Act
    result = obj.method()
    
    # Assert
    assert result is not None
```

## Git Workflow

### Branch Naming

- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`

### Commit Messages

```
[TYPE] Brief description (50 chars max)

Longer explanation of changes and why they're needed.
Include references to related issues.

Refs: #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`

### Pull Request Process

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Ensure tests pass
5. Submit PR with description
6. Address review comments

## Development Setup

### Installation

```bash
# Clone repository
git clone https://github.com/ConnerAdamsMaine/ConsoleMod.git
cd ConsoleMod

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Development Tools

```bash
# Code formatting
black src/ tests/ --line-length=100

# Linting
flake8 src/ tests/ --max-line-length=100

# Type checking
mypy src/ --ignore-missing-imports

# Testing
pytest tests/ -v
```

### Pre-commit Checks

```bash
# Format code
black src/ tests/ --line-length=100

# Check format
black --check src/ tests/ --line-length=100

# Lint
flake8 src/ tests/

# Type check
mypy src/

# Test
pytest tests/
```

## Documentation

### Docstring Standards

- Use Google-style docstrings
- Include type information
- Document exceptions
- Provide examples for complex functions

### Examples

```python
def complex_operation(param: str) -> Dict[str, Any]:
    """Perform complex operation.
    
    This function demonstrates the expected documentation
    format with clear explanation of what it does.
    
    Args:
        param: Input parameter description
        
    Returns:
        Dictionary with results. Keys:
            - 'status': Operation status (str)
            - 'data': Operation result (Any)
            
    Raises:
        ValueError: If param is empty
        RuntimeError: If operation fails
        
    Example:
        >>> result = complex_operation("input")
        >>> print(result['status'])
        'success'
    """
```

### README Updates

If your changes affect:

- Installation process
- API usage
- Features
- Requirements

Update the README.md accordingly.

## Performance Considerations

### Optimization Guidelines

1. **Profile first** - Measure before optimizing
2. **Benchmark changes** - Compare before/after
3. **Document performance** - Note optimization rationale
4. **Thread safety** - Don't sacrifice for speed

### Memory Management

- Respect pane max_lines setting
- Use circular buffers for bounded memory
- Clean up resources properly
- Test with large datasets

## Debugging

### Enable Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Print Debugging

```python
import sys
print("Debug info", file=sys.stderr)
```

### Debug Utilities

```bash
# Run with pdb
pytest tests/test_core.py -v --pdb

# Show local variables
pytest tests/test_core.py -v -l
```

## Release Process

### Version Numbering

Uses semantic versioning: MAJOR.MINOR.PATCH

- MAJOR: Breaking changes
- MINOR: New features
- PATCH: Bug fixes

### Release Checklist

1. Update version in `__version__.py`
2. Update version in `pyproject.toml`
3. Update CHANGELOG
4. Run full test suite
5. Tag release in git
6. Build distribution
7. Upload to PyPI

## License

All contributions are under the 404_CM-v1.0 license. By contributing, you agree to license your contributions under this license.

### License Restrictions

ConsoleMod is **NOT** authorized for:

- AI/ML training or deployment
- Commercial use
- Profit-generating use

See [OPTOUT.md](OPTOUT.md) and [LICENSE](LICENSE) for full details.

## Resources

### Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [TESTING.md](TESTING.md) - Testing guide
- [README.md](README.md) - Usage guide
- [STRUCTURE.md](src/Docs/STRUCTURE.md) - Module structure

### External Resources

- [PEP 8](https://www.python.org/dev/peps/pep-0008/) - Style guide
- [PEP 484](https://www.python.org/dev/peps/pep-0484/) - Type hints
- [pytest docs](https://docs.pytest.org/)
- [asyncio docs](https://docs.python.org/3/library/asyncio.html)

## Questions?

Contact: consolemod@404development.dev

We appreciate your interest in ConsoleMod!
