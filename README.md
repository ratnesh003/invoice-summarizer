# Order Processing System

A modern, full-stack web application for processing order data from text files, generating detailed invoice summaries, and managing data validation errors. Built with FastAPI backend and Streamlit frontend.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 Overview

The Order Processing System streamlines the workflow of parsing, validating, and reporting on order data. It provides an intuitive web interface for uploading order files, viewing processed results, and managing historical submissions.

### Key Features

- **📤 Multi-File Upload**: Process multiple order files simultaneously
- **✅ Robust Validation**: Comprehensive data validation with detailed error reporting
- **💰 Automated Discounts**: Applies 10% discount on line items exceeding $500
- **📊 Customer Summaries**: Generates aggregated reports grouped by customer
- **📜 History Management**: Browse and manage previously processed submissions
- **⬇️ Export Capability**: Download processed reports and error logs
- **🎨 Clean UI**: Modern, responsive interface built with Streamlit

## 🚀 Quick Start

Get the application running in minutes:

```bash
# Clone the repository
git clone <repository-url>
cd order-processing-system

# Install dependencies
pip install -r requirements.txt

# Start the backend
uvicorn backend.main:app --reload &

# Start the frontend
streamlit run frontend/app.py
```

Access the application at `http://localhost:8501`

For detailed setup instructions, see [QUICKSTART.md](docs/QUICKSTART.md)

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running quickly
- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design and structure
- **[API Documentation](docs/API.md)** - REST API endpoints and usage
- **[Development Guide](docs/DEVELOPMENT.md)** - Contributing and development workflow
- **[User Guide](docs/USER_GUIDE.md)** - How to use the application

## 🏗️ Architecture

The system follows a clean separation of concerns with a REST API backend and a web-based frontend:

```
┌─────────────┐      HTTP/REST      ┌──────────────┐
│  Streamlit  │ ◄──────────────────► │   FastAPI    │
│  Frontend   │                      │   Backend    │
└─────────────┘                      └──────────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │ File Storage │
                                     │   + JSON DB  │
                                     └──────────────┘
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed system design.

## 📋 Requirements

- Python 3.9 or higher
- pip package manager
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🔧 Tech Stack

**Backend:**
- FastAPI - Modern, high-performance web framework
- Pydantic - Data validation using Python type annotations
- Tabulate - Pretty-print tabular data

**Frontend:**
- Streamlit - Rapid web app development framework
- Requests - HTTP library for API communication
- Pandas - Data manipulation and analysis

**Testing:**
- Pytest - Testing framework

## 📁 Project Structure

```
order-processing-system/
├── backend/              # FastAPI backend application
│   ├── api/             # API route handlers
│   ├── core/            # Business logic and models
│   └── data/            # Data storage (uploads, outputs, errors)
├── frontend/            # Streamlit frontend application
├── tests/               # Unit and integration tests
├── docs/                # Documentation files
└── requirements.txt     # Python dependencies
```

## 🎮 Usage Example

1. **Upload Files**: Select one or more pipe-delimited text files
2. **Process**: Click "Process Files" to validate and compute summaries
3. **Review**: View the generated customer summary report
4. **Check Errors**: Switch to error log view to see any validation issues
5. **Download**: Export reports for record-keeping or further analysis

### Input Format

Orders should be in pipe-delimited format:

```
OrderID|CustomerName|ProductName|Quantity|UnitPrice|OrderDate
ORD001|John Smith|Laptop|2|999.99|2024-03-15
```

### Output Format

Customer-aggregated summary with totals:

```
Customer Name    | Orders | Items | Gross Total | Discount  | Net Total
------------------------------------------------------------------------
John Smith       | 3      | 4     | $2,529.97   | $200.00   | $2,329.97
...
GRAND TOTAL      |        |       | $7,881.37   | $589.89   | $7,291.48
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_processor.py
```

## 🤝 Contributing

Contributions are welcome! Please read [DEVELOPMENT.md](docs/DEVELOPMENT.md) for details on our development process and coding standards.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Business Rules

- **Discount Logic**: 10% discount applied to line items with total > $500
- **Date Format**: Orders must use YYYY-MM-DD date format
- **Validation**: Negative quantities and prices are rejected
- **Aggregation**: Reports grouped by customer name with order counts

## 🐛 Troubleshooting

**Backend won't start:**
- Ensure port 8000 is not in use
- Check Python version is 3.9+
- Verify all dependencies are installed

**Frontend connection errors:**
- Confirm backend is running at http://localhost:8000
- Check firewall settings

For more troubleshooting tips, see [QUICKSTART.md](docs/QUICKSTART.md#troubleshooting)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI team for the excellent web framework
- Streamlit team for making web app development accessible
- Contributors and testers who helped improve the system

## 📧 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review the FAQ section in [USER_GUIDE.md](docs/USER_GUIDE.md)

---

**Built with ❤️ using Python**
