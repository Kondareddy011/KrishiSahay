# Installing Pillow - Troubleshooting Guide

## Issue: `pip` command not recognized

This happens when Python/pip is not in your system PATH or virtual environment is not activated.

## Solution Options:

### Option 1: Use `python -m pip` (Recommended)

Instead of `pip`, use:
```powershell
python -m pip install Pillow==10.1.0
```

### Option 2: Activate Virtual Environment First

If you created a virtual environment:

**Windows PowerShell:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install Pillow==10.1.0
```

**Windows Command Prompt:**
```cmd
cd backend
venv\Scripts\activate
pip install Pillow==10.1.0
```

**macOS/Linux:**
```bash
cd backend
source venv/bin/activate
pip install Pillow==10.1.0
```

### Option 3: Install All Requirements at Once

```powershell
cd backend
python -m pip install -r requirements.txt
```

This will install Pillow along with all other dependencies including:
- FastAPI
- Uvicorn
- Supabase client
- And other backend dependencies

### Option 4: Check Python Installation

1. Check if Python is installed:
   ```powershell
   python --version
   ```

2. If Python is not found, try:
   ```powershell
   py --version
   ```
   Then use `py -m pip` instead of `pip`

3. If neither works, install Python from [python.org](https://www.python.org/downloads/)
   - **Recommended**: Python 3.8+ for full ML features
   - **Minimum**: Python 3.7+ (some features may be limited)

## Quick Fix Commands:

**In PowerShell (from project root):**
```powershell
cd backend
python -m pip install Pillow==10.1.0
```

**Or install all requirements:**
```powershell
cd backend
python -m pip install -r requirements.txt
```

## Verify Installation:

After installing, verify:
```powershell
python -m pip show Pillow
```

You should see Pillow version 10.1.0 installed.

## Pillow Usage in Project

Pillow is used for:
- Image processing in `backend/image_analyzer.py`
- Image analysis for crop/pest/disease detection
- Image format conversion
- Image property analysis (size, colors, etc.)

## If Still Having Issues:

1. Make sure you're in the `backend` directory
2. Try `python3` instead of `python` (on some systems)
3. Try `py` instead of `python` (Windows Python Launcher)
4. Check if Python is added to PATH:
   - Open System Properties → Environment Variables
   - Add Python installation directory to PATH if needed
5. Use virtual environment (recommended):
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Alternative: Skip Pillow (Limited Functionality)

If Pillow installation fails, the backend will still work but:
- Image analysis will use basic fallback
- Some image features may be limited
- ML image classification won't work

The app will still function for text-based queries.

## Related Dependencies

Pillow is part of the image analysis stack:
- **Pillow** - Basic image processing
- **torch/torchvision** - ML models (optional)
- **transformers** - Vision models (optional)

For basic functionality, only Pillow is required.
