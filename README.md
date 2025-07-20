# Equivalent Soil Mass (ESM) Web App

This Flask-based web application lets users upload a CSV of initial and new bulk density (bd) and SOC values to compute corrected SOC stock via two methods:

- **Fixed-depth**: single-depth mineral mass correction  
- **Profile-based**: full depth-profile correction

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## CSV Format

| bd_i | soc_i | bd_n | soc_n | depth |
|------|-------|------|-------|-------|
| 1.5  | 0.014 | 1.1  | 0.016 | 30    |
