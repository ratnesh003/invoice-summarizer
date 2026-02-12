# Quick Start Guide

Get the Order Processing System up and running in under 5 minutes.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [First Steps](#first-steps)
- [Common Issues](#common-issues)
- [Next Steps](#next-steps)

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

- **Python 3.9 or higher**
  - Check your version: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/

- **pip** (Python package installer)
  - Usually comes with Python
  - Check: `pip --version` or `pip3 --version`

- **Modern Web Browser**
  - Chrome, Firefox, Safari, or Edge

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **RAM**: 512MB minimum (1GB recommended)
- **Disk Space**: 100MB for application + dependencies
- **Network**: Internet connection for initial dependency download

## Installation

### Step 1: Get the Code

**Option A: Clone with Git**
```bash
git clone <repository-url>
cd order-processing-system
```

**Option B: Download ZIP**
1. Download the project as a ZIP file
2. Extract to your desired location
3. Open terminal/command prompt in the extracted folder

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment keeps dependencies isolated:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 3: Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This installs:
- fastapi - Web framework
- uvicorn - ASGI server
- streamlit - Frontend framework
- pydantic - Data validation
- requests - HTTP library
- pandas - Data manipulation
- pytest - Testing framework
- tabulate - Table formatting

**Installation Time**: ~1-2 minutes depending on your connection

## Running the Application

You need to run **two** separate processes: the backend API and the frontend UI.

### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - Start Backend:**
```bash
uvicorn backend.main:app --reload
```

Expected output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Terminal 2 - Start Frontend:**

Open a new terminal in the same directory and run:
```bash
streamlit run frontend/app.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Your browser should automatically open to the application.

### Option 2: Automated Start (Windows Only)

Double-click `run_app.bat` in the project folder. This will:
1. Open a terminal for the backend
2. Open a terminal for the frontend
3. Launch your browser

### Verifying the Installation

1. **Check Backend API**: Visit http://127.0.0.1:8000
   - You should see: `{"message":"Order Processing API is running"}`

2. **Check API Documentation**: Visit http://127.0.0.1:8000/docs
   - You should see interactive Swagger UI

3. **Check Frontend**: Visit http://localhost:8501
   - You should see the Order Processing System interface

## First Steps

### 1. Upload Your First File

The application comes with sample data for testing:

1. Locate `sample_input.txt` in the project root
2. In the Streamlit UI, click **"Choose files"**
3. Select `sample_input.txt`
4. Click **"Process Files"**

### 2. View Results

After processing:
- The submission appears in the **History** sidebar
- The main area shows the **Output Report** with customer summaries
- Toggle to **Error Log** to see validation issues (if any)

### 3. Download Reports

Click the **"Download Output Report"** or **"Download Error Log"** button to save results locally.

### 4. Process Your Own Data

Create a text file with pipe-delimited order data:

```
OrderID|CustomerName|ProductName|Quantity|UnitPrice|OrderDate
ORD001|John Smith|Laptop|2|999.99|2024-03-15
ORD002|Jane Doe|Mouse|1|25.50|2024-03-16
```

**Important Format Rules:**
- Six fields separated by `|` (pipe character)
- Date format: `YYYY-MM-DD`
- Quantity and price must be non-negative numbers
- No header row (start with data)

## Common Issues

### Issue: "Port 8000 already in use"

**Cause**: Another application is using port 8000

**Solution**:
```bash
# Stop the process using the port
# On macOS/Linux:
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or start on a different port:
uvicorn backend.main:app --reload --port 8001
```

### Issue: "Port 8501 already in use"

**Cause**: Another Streamlit app is running

**Solution**:
```bash
# Kill existing Streamlit processes
pkill -f streamlit

# Or specify a different port:
streamlit run frontend/app.py --server.port 8502
```

### Issue: "Module not found" errors

**Cause**: Dependencies not installed or wrong Python environment

**Solution**:
```bash
# Ensure virtual environment is activated
# Look for (venv) in your prompt

# Reinstall dependencies
pip install -r requirements.txt

# Or install specific missing package:
pip install fastapi
```

### Issue: "Cannot connect to backend"

**Symptoms**: Frontend shows "Connection error" messages

**Solution**:
1. Verify backend is running: `curl http://localhost:8000`
2. Check for firewall blocking port 8000
3. Ensure `API_URL` in `frontend/app.py` matches backend URL
4. Restart both services

### Issue: "Permission denied" errors

**Cause**: Insufficient permissions to create directories or write files

**Solution**:
```bash
# Ensure write permissions in project directory
chmod -R 755 backend/data  # macOS/Linux

# Run as administrator (Windows)
```

### Issue: Python version too old

**Symptoms**: Syntax errors or "version 3.9 required"

**Solution**:
1. Check version: `python --version`
2. Install Python 3.9+ from https://www.python.org
3. Use `python3.9` explicitly if multiple versions installed

### Issue: Browser doesn't auto-open

**Solution**:
- Manually visit http://localhost:8501
- Check console output for actual URL
- Try: `streamlit run frontend/app.py --server.headless false`

## Troubleshooting Commands

**Check if services are running:**
```bash
# macOS/Linux
ps aux | grep uvicorn
ps aux | grep streamlit

# Windows
tasklist | findstr python
```

**View application logs:**
```bash
# Backend logs appear in the terminal running uvicorn
# Frontend logs appear in the terminal running streamlit
# Check backend/data/ for processed file outputs
```

**Reset application state:**
```bash
# Clear all processed data (use with caution)
rm -rf backend/data/uploads/*
rm -rf backend/data/outputs/*
rm -rf backend/data/errors/*
echo "[]" > backend/data/history.json
```

## Testing Your Installation

Run the test suite to verify everything is working:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=backend
```

Expected output: All tests should pass ✓

## Development Mode Features

When running with `--reload` flag, the backend automatically restarts when code changes:

```bash
uvicorn backend.main:app --reload
```

Streamlit also auto-reloads when files change.

## Production Deployment Notes

For production deployment:

1. **Don't use `--reload`**: Remove auto-reload in production
2. **Use a production server**: Consider Gunicorn or Hypercorn
3. **Set up HTTPS**: Use Nginx or Traefik as reverse proxy
4. **Configure CORS properly**: Don't use `allow_origins=["*"]`
5. **Add authentication**: Implement user authentication
6. **Use environment variables**: For configuration
7. **Set up monitoring**: Add logging and error tracking

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production setup instructions.

## Next Steps

Now that your application is running:

1. **Read the User Guide**: [USER_GUIDE.md](USER_GUIDE.md) for detailed usage
2. **Explore the API**: Visit http://127.0.0.1:8000/docs for interactive API docs
3. **Review Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
4. **Start Developing**: [DEVELOPMENT.md](DEVELOPMENT.md) for contribution guidelines

## Getting Help

If you encounter issues not covered here:

1. Check the [FAQ](USER_GUIDE.md#faq) in the User Guide
2. Review existing GitHub issues
3. Open a new issue with:
   - Your operating system and Python version
   - Complete error message
   - Steps to reproduce
   - Expected vs actual behavior

## Quick Reference

**Start Backend:**
```bash
uvicorn backend.main:app --reload
```

**Start Frontend:**
```bash
streamlit run frontend/app.py
```

**Run Tests:**
```bash
pytest
```

**Access Points:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

**🎉 Congratulations!** You're now ready to process orders!
