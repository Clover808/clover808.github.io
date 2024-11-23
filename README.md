# Clover Clothes - Bespoke Attire

A static e-commerce website for Clover Clothes, specializing in fabrics, fashion design, and tailoring services.

## Project Structure

```
CloverClothes-FastAPI/
├── build.py              # Static site generator script
├── docs/                 # Generated static site (for GitHub Pages)
├── static/              
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Image assets
├── templates/           
│   ├── base.html        # Base template
│   └── index.html       # Home page template
└── requirements.txt     # Python dependencies
```

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Clover808/Bespoke-attire.git
   cd Bespoke-attire
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Unix/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Local Development

1. Start the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

2. Visit `http://localhost:8000` in your browser

## Building for GitHub Pages

1. Make your changes in the `templates/` directory

2. Run the build script to generate static files:
   ```bash
   python build.py
   ```

3. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

4. GitHub Pages will automatically deploy from the `docs/` folder

## Important Notes for Maintainers

### Asset Paths
- All asset paths in templates must use `{{ BASE_URL }}` prefix
- Example: `{{ BASE_URL }}/static/css/style.css`
- The `BASE_URL` is set to `/Bespoke-attire` in `build.py`

### Navigation Links
- All internal links should use `{{ BASE_URL }}` prefix
- Example: `<a href="{{ BASE_URL }}/products">Products</a>`

### Adding New Pages
1. Create new template in `templates/`
2. Update `build.py` to generate the static version
3. Run `python build.py`
4. Commit and push changes

### Troubleshooting
- If styles don't match between local and GitHub Pages:
  1. Check asset paths in templates
  2. Ensure `build.py` ran successfully
  3. Verify all files are in `docs/` directory
  4. Check browser console for 404 errors

### Managing Python Processes
- To stop local development server:
  1. Press `Ctrl+C` in the terminal
  2. Or use Task Manager to end `python.exe` processes
- Always deactivate virtual environment when done:
  ```bash
  deactivate
  ```

## Contact

For questions or issues, please open a GitHub issue or contact the maintainers.

## License

[Add your license information here]
