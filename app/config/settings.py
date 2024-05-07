# settings.py

# List of file extensions to include in analysis
INCLUDE_EXTENSIONS = {
    '.py', '.js', '.java', '.cpp', '.c', '.cs', '.tsx', '.ts', '.php', '.rb', '.swift', 
    '.go', '.scala', '.kt', '.rs', '.lua', '.groovy', '.perl', '.sh', '.bat', '.ps1',
    '.html', '.css', '.scss', '.less', '.sql', '.pl', '.r', '.m', '.mm', '.vue', 
    '.yaml', '.yml', '.xml', '.json', '.toml', '.config', '.conf'
}

# New set of extensions specifically for document files used in documentation summarizer
DOCUMENT_EXTENSIONS = {
    '.md', '.rst', '.tex', '.htm', '.markdown', '.mdown', '.mkdn', '.mkd', 
    '.asciidoc', '.adoc', '.ad', '.docx', '.pdf', '.txt'
}

# List of file extensions to exclude from analysis
EXCLUDE_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.bmp', '.tiff', '.psd', 
    '.mp3', '.wav', '.m4a', '.flac', '.mp4', '.avi', '.mov', '.wmv', '.flv', 
    '.exe', '.dll', '.so', '.dylib', '.bin', '.lib', '.dmg', '.iso', '.img', 
    '.msi', '.zip', '.tar', '.gz', '.rar', '.7z', '.bz2', '.log', '.out', '.tmp',
    '.cache', '.bak', '.swp', '.lock', '.sublime-project', '.sublime-workspace',
    '.jar', '.war', '.ear', '.apk', '.aab'
}

# List of directories to exclude from analysis
EXCLUDE_DIRECTORIES = {
    '__pycache__', '.venv', 'venv', '.env', 'env', 'node_modules', '.git', '.github', '.gitlab',
    'dist', 'build', 'bin', 'obj', 'lib', 'libs', 'vendor', '.vscode', '.idea', 'nbproject',
    '.settings', 'logs', 'temp', 'tmp', 'cache', 'backups', 'deployments', 'uploads', 'download',
    'node_modules', 'jspm_packages', '.npm', '.bower_cache', '.mypy_cache', '.pytest_cache', '.sass-cache',
    'coverage', 'docker', 'dockerfiles', '.dockerignore', 'volumes', '__MACOSX'
}
