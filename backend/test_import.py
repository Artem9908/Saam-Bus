import sys
import os
from pathlib import Path

print('Current working directory:', os.getcwd())
print('Python path:', sys.path)
print('Directory contents:', os.listdir())
print('App directory contents:', os.listdir('app'))

try:
    from app.database import Base, get_db
    print('Successfully imported app.database')
except ImportError as e:
    print('Failed to import app.database:', str(e))

try:
    import app
    print('Successfully imported app')
    print('app.__file__:', app.__file__)
except ImportError as e:
    print('Failed to import app:', str(e))
