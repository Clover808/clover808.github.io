# Clover Clothes - Bespoke Attire

## Day 2: Managing and Updating the Site

This guide is for maintainers who need to update the Clover Clothes website. Our site is hosted on GitHub Pages and uses a static site generator for deployment.

### Quick Start Guide

1. **Clone the Repository** (First time only)
   ```bash
   git clone https://github.com/Clover808/Bespoke-attire.git
   cd Bespoke-attire
   ```

2. **Set Up Python Environment** (First time only)
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

### Making Updates to the Site

1. **Activate the Environment**
   ```bash
   .\venv\Scripts\activate  # Windows
   ```

2. **Make Your Changes**
   - Edit files in `templates/` directory
   - Update static assets in `static/` directory
   - Test locally if needed: `uvicorn main:app --reload`

3. **Build the Site**
   ```bash
   python build.py
   ```
   This generates static files in the `docs/` directory for GitHub Pages.

4. **Review Your Changes**
   - Check the generated files in `docs/`
   - Ensure all links use `{{ BASE_URL }}` prefix
   - Verify all assets are included

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Description of your changes"
   git push
   ```

6. **Clean Up**
   ```bash
   deactivate  # Exit virtual environment
   # Use Task Manager to close any remaining python.exe processes if needed
   ```

### Important Notes

#### URL Structure
- All internal links must use `{{ BASE_URL }}` prefix
- Example: `{{ BASE_URL }}/static/css/style.css`
- The `BASE_URL` is set to `/Bespoke-attire` in `build.py`

#### Common Issues
1. **Missing Assets on GitHub Pages**
   - Ensure files are in `docs/` directory
   - Check all paths use `{{ BASE_URL }}`
   - Run `build.py` before committing

2. **Python Processes**
   - Close all terminals when done
   - Use Task Manager to end lingering `python.exe` processes

### File Structure
```
CloverClothes-FastAPI/
├── build.py              # Static site generator
├── docs/                 # Generated site (DO NOT edit directly)
├── static/              
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript
│   └── images/          # Images
└── templates/           
    ├── base.html        # Main template
    └── index.html       # Home page
```

### Need Help?
- Check GitHub Issues for known problems
- Create a new issue if you encounter problems
- Contact the main maintainers through GitHub

Remember: Always build and test locally before pushing to GitHub Pages!
