#!/usr/bin/env python3
import os
import json
from pathlib import Path

class Config:
    def __init__(self):
        # Define config directory and file
        self.config_dir = os.path.expanduser("~/.config/docs-grabber")
        self.config_file = os.path.join(self.config_dir, "settings.json")
        
        # Default settings
        self.default_settings = {
            "base_repo_path": "",
            "filter_mode": "none"  # none, markdown_only, exclude_code, light_filter
        }
        
        # Current settings
        self.settings = self.default_settings.copy()
        
        # Ensure config directory exists
        self._ensure_config_dir()
        
        # Load settings if they exist
        self.load_settings()
    
    def _ensure_config_dir(self):
        """Ensure the config directory exists"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
    
    def load_settings(self):
        """Load settings from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Update settings with loaded values
                    self.settings.update(loaded_settings)
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save current settings to config file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
    
    def reset(self):
        """Reset settings to default"""
        self.settings = self.default_settings.copy()
        self.save_settings()


# File filtering functions
def is_markdown_file(filename):
    """Check if a file is a markdown file"""
    extensions = ['.md', '.mdx']
    return any(filename.lower().endswith(ext) for ext in extensions)

def is_code_file(filename):
    """Check if a file is likely a code file"""
    code_extensions = [
        # Programming languages
        '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.c', '.cpp', '.cs', '.go', '.rb', '.php',
        '.swift', '.kt', '.rs', '.scala', '.sh', '.bash', '.ps1', '.pl', '.lua', '.r',
        # Web development
        '.html', '.htm', '.css', '.scss', '.sass', '.less',
        # Data formats that might contain code
        '.json', '.xml', '.yaml', '.yml', 
        # Build and config files
        '.gradle', '.sbt', '.make', '.cmake', '.toml', '.ini', '.conf',
        # Compiled files
        '.class', '.jar', '.war', '.dll', '.exe', '.so', '.o', '.obj', '.pyc',
        # Docker and container files
        '.dockerfile', '.containerfile',
        # Database files
        '.sql', '.db', '.sqlite'
    ]
    return any(filename.lower().endswith(ext) for ext in code_extensions)

def is_binary_or_generated_file(filename):
    """Check if a file is likely a binary or generated file that should be excluded in light filtering"""
    binary_extensions = [
        # Binary files
        '.bin', '.dat', '.exe', '.dll', '.so', '.dylib', '.class', '.jar', '.war', '.ear',
        '.zip', '.tar', '.gz', '.bz2', '.xz', '.7z', '.rar',
        # Image files
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico', '.svg',
        # Audio/Video files
        '.mp3', '.mp4', '.wav', '.flac', '.ogg', '.avi', '.mov', '.mkv', '.webm',
        # Document formats (non-text)
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        # Database files
        '.db', '.sqlite', '.mdb',
        # Compiled code
        '.pyc', '.pyo', '.o', '.obj', '.a', '.lib',
        # Lock files and package management
        '.lock', '.yarn-integrity', 'package-lock.json', 'yarn.lock',
        # Cache files
        '.cache', '.DS_Store', 'Thumbs.db'
    ]
    
    # Also check for common generated file patterns
    generated_patterns = [
        'node_modules', '__pycache__', '.git', '.svn', '.hg', '.idea', '.vscode',
        'build', 'dist', 'target', 'out', 'bin', 'obj'
    ]
    
    # Check if the file has a binary extension
    is_binary = any(filename.lower().endswith(ext) for ext in binary_extensions)
    
    # Check if the file path contains a generated pattern
    is_generated = any(pattern in filename for pattern in generated_patterns)
    
    return is_binary or is_generated

def filter_files(source_dir, target_dir, filter_mode):
    """
    Filter files based on the selected mode
    
    Args:
        source_dir: Source directory containing files to filter
        target_dir: Target directory to copy filtered files to
        filter_mode: Filtering mode (none, markdown_only, exclude_code, light_filter)
    
    Returns:
        List of files that were copied
    """
    copied_files = []
    
    for root, dirs, files in os.walk(source_dir):
        # Create relative path
        rel_path = os.path.relpath(root, source_dir)
        target_path = os.path.join(target_dir, rel_path)
        
        # Create target directory if it doesn't exist
        os.makedirs(target_path, exist_ok=True)
        
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_path, file)
            
            # Apply filtering based on mode
            should_copy = True
            
            if filter_mode == "markdown_only":
                should_copy = is_markdown_file(file)
            elif filter_mode == "exclude_code":
                should_copy = not is_code_file(file)
            elif filter_mode == "light_filter":
                should_copy = not is_binary_or_generated_file(source_file)
            
            if should_copy:
                try:
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                    if os.path.isfile(source_file):
                        with open(source_file, 'rb') as src, open(target_file, 'wb') as dst:
                            dst.write(src.read())
                        copied_files.append(target_file)
                except Exception as e:
                    print(f"Error copying {source_file}: {e}")
    
    return copied_files
