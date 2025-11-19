
# Create .gitignore file
gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Data files (uncomment if you want to exclude large data files)
# *.csv
# *.xlsx

# OS
Thumbs.db
.DS_Store

# Temporary files
*.tmp
*.bak
*.log
'''

with open('.gitignore', 'w') as f:
    f.write(gitignore_content)

print("✓ Created: .gitignore")
print("\n" + "="*80)
print("ALL FILES SUCCESSFULLY CREATED!")
print("="*80)
