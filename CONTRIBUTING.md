# 🤝 Contributing to Margadarsaka

Thank you for your interest in contributing to Margadarsaka! This guide will help you get started.

## 🚀 Quick Start for Contributors

### 1. Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/Margadarsaka.git
cd Margadarsaka

# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac
# or
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Install dependencies
uv sync --dev

# Set up environment variables (choose one):
# Option 1: Use .env file (recommended for new contributors)
cp .env.example .env
# Edit .env with your API keys

# Option 2: Use Doppler (optional)
uv run python setup_doppler.py
```

### 2. Run the Application

```bash
# Start the complete application
uv run margadarsaka

# Or run components individually
uv run uvicorn src.margadarsaka.api:app --reload  # API only
uv run streamlit run src/margadarsaka/ui.py       # UI only
```

### 3. Run Tests

```bash
# Quick tests
uv run python -m pytest tests/ -v

# Full test suite
./test.sh full          # Linux/Mac
.\test.ps1 -TestType full  # Windows

# Code quality checks
uv run black src/ tests/
uv run ruff check src/ tests/
```

## 🧑‍💻 Development Guidelines

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **Documentation**: Update docstrings and README as needed
- **Testing**: Add tests for new features
- **Type Hints**: Use type hints where applicable

### Commit Convention

```text
type(scope): description

Examples:
feat(api): add new career recommendation endpoint
fix(ui): resolve RIASEC assessment scoring bug
docs(readme): update installation instructions
test(doppler): add integration tests for secrets
```

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes  
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

## 🎯 Areas for Contribution

### 🔴 High Priority

- **UI/UX Improvements**: Better Streamlit components
- **AI Model Enhancements**: Improve career recommendations
- **Language Support**: Expand Hindi translation coverage
- **Resume Analysis**: Enhanced ATS scoring algorithms

### 🟡 Medium Priority

- **Database Integration**: Move from SQLite to PostgreSQL
- **Authentication**: User account system
- **API Optimization**: Performance improvements
- **Mobile Responsiveness**: Better mobile UI

### 🟢 Good First Issues

- **Documentation**: Improve inline documentation
- **Test Coverage**: Add more unit tests
- **Error Handling**: Better error messages
- **Configuration**: Environment variable validation

## 🔍 Testing Your Changes

### Before Submitting

1. **Run all tests**: `uv run python -m pytest tests/ -v`
2. **Check code quality**: `uv run black . && uv run ruff check .`
3. **Test both environments**: Test with both Doppler and .env setups
4. **Manual testing**: Run the full application and test your changes

### Test Categories

- **Unit Tests**: Core functionality
- **Integration Tests**: External services (Doppler, APIs)
- **UI Tests**: Streamlit interface validation
- **API Tests**: FastAPI endpoint testing

## 📋 Pull Request Process

### 1. Create Pull Request

- **Base branch**: `main` (for hotfixes) or `dev` (for features)
- **Title**: Clear, descriptive title
- **Description**: Explain what changes were made and why

### 2. PR Checklist

- [ ] Tests pass locally
- [ ] Code follows project style guidelines
- [ ] Documentation updated (if applicable)
- [ ] No breaking changes (or clearly documented)
- [ ] Screenshots included (for UI changes)

### 3. Review Process

- Code review by maintainers
- Automated tests run via GitHub Actions
- Address feedback and update PR
- Merge when approved

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues
2. Test with latest version
3. Try both Doppler and .env configurations

### Bug Report Template

```markdown
**Describe the bug**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. Windows 11, macOS 14, Ubuntu 22.04]
- Python version: [e.g. 3.12.2]
- UV version: [e.g. 0.1.45]
- Secrets method: [Doppler/env file]

**Additional context**
Any other context about the problem.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Clear description of what the problem is.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've considered.

**Additional context**
Any other context or screenshots.
```

## 🤔 Questions & Support

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Code Comments**: Implementation questions

## 🙏 Recognition

Contributors will be:

- Listed in the main README
- Tagged in release notes for significant contributions
- Invited to join the maintainer team (for regular contributors)

---

Happy coding! 🎉
