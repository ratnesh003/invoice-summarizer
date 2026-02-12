# Documentation Index

Welcome to the Order Processing System documentation. This directory contains comprehensive guides for users, developers, and contributors.

## 📖 Documentation Structure

### For Users

**[Quick Start Guide](QUICKSTART.md)** 🚀
- Get the system running in 5 minutes
- Installation steps
- First-time setup
- Common troubleshooting

**[User Guide](USER_GUIDE.md)** 📚
- Complete usage instructions
- Interface walkthrough
- Understanding reports
- Error handling
- Tips and best practices
- FAQ

### For Developers

**[Architecture Overview](ARCHITECTURE.md)** 🏗️
- System design and structure
- Component interactions
- Data flow diagrams
- Technology stack details
- Design patterns used
- Scalability considerations

**[API Documentation](API.md)** 🔌
- REST API reference
- Endpoint specifications
- Request/response examples
- Error codes
- Client examples in multiple languages

**[Development Guide](DEVELOPMENT.md)** 💻
- Development environment setup
- Coding standards
- Testing guidelines
- Git workflow
- Pull request process
- Common development tasks

### For Contributors

**[Contributing Guidelines](../CONTRIBUTING.md)** 🤝
- How to contribute
- Code of conduct
- Submission process
- Style guidelines
- Community resources

**[Changelog](../CHANGELOG.md)** 📝
- Version history
- Release notes
- Breaking changes
- Migration guides

## 📚 Quick Reference

### Getting Started (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
uvicorn backend.main:app --reload

# Start frontend (new terminal)
streamlit run frontend/app.py
```

Visit: http://localhost:8501

### Key Concepts

**Input Format**:
```
OrderID|CustomerName|ProductName|Quantity|UnitPrice|OrderDate
ORD001|John Smith|Laptop|2|999.99|2024-03-15
```

**Output Report**:
Customer-aggregated summary with orders, items, totals, and discounts

**Business Rule**:
10% discount on line items exceeding $500

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/upload` | Upload and process files |
| GET | `/api/history` | List all submissions |
| GET | `/api/file/{id}/output` | Get output report |
| GET | `/api/file/{id}/error` | Get error log |
| DELETE | `/api/history/{id}` | Delete submission |

### Tech Stack

- **Backend**: FastAPI, Pydantic, Tabulate
- **Frontend**: Streamlit, Pandas
- **Testing**: Pytest
- **Python**: 3.9+

## 🎯 Common Tasks

### First Time Setup

1. Read [QUICKSTART.md](QUICKSTART.md)
2. Follow installation steps
3. Run the sample file
4. Explore the interface

### Processing Orders

1. Prepare pipe-delimited file
2. Upload via Streamlit UI
3. View customer summary report
4. Check error log for issues
5. Download results

### Contributing Code

1. Read [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Set up development environment
3. Create feature branch
4. Make changes with tests
5. Submit pull request

### Understanding the System

1. Review [ARCHITECTURE.md](ARCHITECTURE.md)
2. Explore code structure
3. Check [API.md](API.md) for endpoints
4. Run tests to see examples

## 🔍 Finding What You Need

| I want to... | Read this... |
|--------------|--------------|
| Install and run the app | [QUICKSTART.md](QUICKSTART.md) |
| Learn how to use the interface | [USER_GUIDE.md](USER_GUIDE.md) |
| Understand the system design | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Use the API programmatically | [API.md](API.md) |
| Contribute code | [DEVELOPMENT.md](DEVELOPMENT.md) |
| Report a bug or request a feature | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| See what's changed | [CHANGELOG.md](../CHANGELOG.md) |

## 💡 Learning Path

### For Users

1. **Setup** → [QUICKSTART.md](QUICKSTART.md)
2. **Learn Interface** → [USER_GUIDE.md](USER_GUIDE.md)
3. **Process Data** → Try sample files
4. **Troubleshoot** → [USER_GUIDE.md#faq](USER_GUIDE.md#faq)

### For Developers

1. **Architecture** → [ARCHITECTURE.md](ARCHITECTURE.md)
2. **Setup Dev Environment** → [DEVELOPMENT.md](DEVELOPMENT.md)
3. **API Reference** → [API.md](API.md)
4. **Write Tests** → [DEVELOPMENT.md#testing](DEVELOPMENT.md#testing)
5. **Submit Changes** → [CONTRIBUTING.md](../CONTRIBUTING.md)

### For System Administrators

1. **Setup** → [QUICKSTART.md](QUICKSTART.md)
2. **Architecture** → [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Security** → [ARCHITECTURE.md#security-considerations](ARCHITECTURE.md#security-considerations)
4. **Deployment** → [ARCHITECTURE.md#scalability--performance](ARCHITECTURE.md#scalability--performance)

## 🛠️ Tools and Resources

### Development Tools

- **Python**: https://www.python.org/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Streamlit**: https://streamlit.io/
- **Pytest**: https://pytest.org/

### Related Documentation

- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Streamlit API**: https://docs.streamlit.io/library/api-reference
- **Pydantic Models**: https://docs.pydantic.dev/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

## 📧 Getting Help

### Questions?

1. Check the [FAQ](USER_GUIDE.md#faq)
2. Search existing GitHub issues
3. Open a new issue
4. Join community discussions

### Found a Bug?

1. Check if already reported
2. Gather reproduction steps
3. Include environment details
4. Submit issue with template

### Want a Feature?

1. Check if already requested
2. Explain the use case
3. Describe expected behavior
4. Submit feature request

## 🔄 Keeping Documentation Updated

Help us keep documentation accurate:

- Fix typos and errors
- Add missing examples
- Clarify confusing sections
- Update outdated information
- Add FAQs from common questions

See [CONTRIBUTING.md](../CONTRIBUTING.md) for how to submit documentation improvements.

## 📊 Documentation Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| README.md | ✅ Complete | 2024-03-15 |
| QUICKSTART.md | ✅ Complete | 2024-03-15 |
| USER_GUIDE.md | ✅ Complete | 2024-03-15 |
| ARCHITECTURE.md | ✅ Complete | 2024-03-15 |
| API.md | ✅ Complete | 2024-03-15 |
| DEVELOPMENT.md | ✅ Complete | 2024-03-15 |
| CONTRIBUTING.md | ✅ Complete | 2024-03-15 |
| CHANGELOG.md | ✅ Complete | 2024-03-15 |

## 🙏 Thank You

Thank you for using and contributing to the Order Processing System. Your feedback helps us improve!

---

**Need help?** Open an issue or start a discussion on GitHub.
