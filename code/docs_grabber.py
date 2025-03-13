#!/usr/bin/env python3
import sys
import os
import subprocess
import datetime
import shutil
import re
import tempfile
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QFileDialog, QProgressBar, QMessageBox, QComboBox,
                            QDialog, QGroupBox, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

# Import the configuration module
from config import Config, filter_files


class DocsGrabberThread(QThread):
    progress_signal = pyqtSignal(int)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str, str)
    
    def __init__(self, repo_url, target_path, filter_mode="none"):
        super().__init__()
        self.repo_url = repo_url
        self.target_path = target_path
        self.filter_mode = filter_mode
        
    def run(self):
        try:
            # Create a temporary directory for cloning
            temp_dir = tempfile.mkdtemp()
            
            self.status_signal.emit("Cloning repository...")
            self.progress_signal.emit(10)
            
            # Extract the repository URL and path components
            repo_path_match = re.search(r'github\.com/([^/]+)/([^/]+)(?:/tree/([^/]+)/(.+))?', self.repo_url)
            
            if not repo_path_match:
                self.finished_signal.emit(False, "Invalid GitHub URL format", "")
                return
                
            owner = repo_path_match.group(1)
            repo_name = repo_path_match.group(2)
            branch = repo_path_match.group(3) if repo_path_match.group(3) else "main"
            subdir_path = repo_path_match.group(4) if repo_path_match.group(4) else ""
            
            # Construct the raw GitHub URL for the specific directory
            if subdir_path:
                # If a specific subdirectory is specified, we'll clone only that part
                clone_url = f"https://github.com/{owner}/{repo_name}.git"
                specific_path = subdir_path
            else:
                # If the entire repo is specified, clone the whole thing
                clone_url = f"https://github.com/{owner}/{repo_name}.git"
                specific_path = ""
            
            # Clone the repository to the temp directory
            result = subprocess.run(
                ["git", "clone", "--branch", branch, clone_url, temp_dir],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.finished_signal.emit(False, f"Git clone failed: {result.stderr}", "")
                return
                
            self.progress_signal.emit(40)
            self.status_signal.emit("Processing files...")
            
            # Determine the source directory based on the specific path
            source_dir = temp_dir
            if specific_path:
                source_dir = os.path.join(temp_dir, specific_path)
                if not os.path.exists(source_dir):
                    self.finished_signal.emit(False, f"Specified path '{specific_path}' not found in repository", "")
                    return
            
            # Create the reference directory
            reference_dir = os.path.join(self.target_path, "reference")
            if os.path.exists(reference_dir):
                shutil.rmtree(reference_dir)
            os.makedirs(reference_dir, exist_ok=True)
            
            self.progress_signal.emit(60)
            
            # Apply file filtering based on the selected mode
            if self.filter_mode == "none":
                self.status_signal.emit("Copying all documentation files...")
                # Copy all files from the source directory to the reference directory (excluding .git)
                for item in os.listdir(source_dir):
                    if item != ".git":  # Skip .git directory
                        source = os.path.join(source_dir, item)
                        destination = os.path.join(reference_dir, item)
                        if os.path.isdir(source):
                            shutil.copytree(source, destination, ignore=shutil.ignore_patterns('.git'))
                        else:
                            shutil.copy2(source, destination)
            else:
                filter_description = {
                    "markdown_only": "markdown files only",
                    "exclude_code": "non-code files",
                    "light_filter": "documentation files (excluding binaries)"
                }.get(self.filter_mode, "files")
                
                self.status_signal.emit(f"Filtering and copying {filter_description}...")
                filter_files(source_dir, reference_dir, self.filter_mode)
            
            self.progress_signal.emit(80)
            self.status_signal.emit("Creating AI instructions file...")
            
            # Format the repository name for display
            display_repo_name = f"{owner}/{repo_name}"
            if specific_path:
                display_repo_name += f" (path: {specific_path})"
            
            # Generate AI instructions file
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ai_instructions = f"""# AI Instructions: Documentation Context Folder

This folder contains documentation for the following Github repository: {display_repo_name}.

It is intended to provide you with context on how this SDK or utility operates. Do not edit the documentation in this folder or its recursive paths.

It was imported from the internet on: {current_time}.

The original URL was {self.repo_url}
"""
            
            ai_instructions_path = os.path.join(self.target_path, "ai-instructions.md")
            with open(ai_instructions_path, "w") as f:
                f.write(ai_instructions)
            
            # Clean up temp directory
            shutil.rmtree(temp_dir)
            
            self.progress_signal.emit(100)
            self.status_signal.emit("Documentation successfully grabbed!")
            self.finished_signal.emit(True, "Documentation successfully grabbed!", reference_dir)
            
        except Exception as e:
            self.finished_signal.emit(False, f"Error: {str(e)}", "")


class SettingsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Base repository path
        repo_group = QGroupBox("Default Repository Path")
        repo_layout = QVBoxLayout()
        
        path_layout = QHBoxLayout()
        path_label = QLabel("Base Repository Path:")
        self.path_input = QLineEdit()
        self.path_input.setText(self.config.get("base_repo_path", ""))
        self.path_input.setPlaceholderText("Select default repository path")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)
        repo_layout.addLayout(path_layout)
        repo_group.setLayout(repo_layout)
        layout.addWidget(repo_group)
        
        # Filtering options
        filter_group = QGroupBox("Default Filtering Mode")
        filter_layout = QVBoxLayout()
        
        self.filter_none = QRadioButton("No filtering (copy all files)")
        self.filter_markdown = QRadioButton("Copy Markdown documents only (.md, .mdx)")
        self.filter_exclude_code = QRadioButton("Exclude code files")
        self.filter_light = QRadioButton("Light filtering (exclude binaries and generated files)")
        
        filter_layout.addWidget(self.filter_none)
        filter_layout.addWidget(self.filter_markdown)
        filter_layout.addWidget(self.filter_exclude_code)
        filter_layout.addWidget(self.filter_light)
        
        # Set the current filter mode
        current_filter = self.config.get("filter_mode", "none")
        if current_filter == "none":
            self.filter_none.setChecked(True)
        elif current_filter == "markdown_only":
            self.filter_markdown.setChecked(True)
        elif current_filter == "exclude_code":
            self.filter_exclude_code.setChecked(True)
        elif current_filter == "light_filter":
            self.filter_light.setChecked(True)
        else:
            self.filter_none.setChecked(True)
            
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Base Repository Path")
        if directory:
            self.path_input.setText(directory)
            
    def save_settings(self):
        # Save base repository path
        self.config.set("base_repo_path", self.path_input.text())
        
        # Save filter mode
        if self.filter_none.isChecked():
            self.config.set("filter_mode", "none")
        elif self.filter_markdown.isChecked():
            self.config.set("filter_mode", "markdown_only")
        elif self.filter_exclude_code.isChecked():
            self.config.set("filter_mode", "exclude_code")
        elif self.filter_light.isChecked():
            self.config.set("filter_mode", "light_filter")
        
        # Save settings to file
        if self.config.save_settings():
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to save settings.")


class DocsGrabberApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docs Grabber")
        self.setMinimumSize(600, 350)
        self.docs_path = ""
        
        # Initialize configuration
        self.config = Config()
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Repository URL input
        repo_layout = QHBoxLayout()
        repo_label = QLabel("GitHub Docs URL:")
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("https://github.com/username/repo/tree/main/docs")
        repo_layout.addWidget(repo_label)
        repo_layout.addWidget(self.repo_input)
        main_layout.addLayout(repo_layout)
        
        # Target path selection
        path_layout = QHBoxLayout()
        path_label = QLabel("Save Path:")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select target repository path")
        
        # Set default path from config if available
        default_path = self.config.get("base_repo_path")
        if default_path and os.path.isdir(default_path):
            self.path_input.setText(default_path)
            
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)
        main_layout.addLayout(path_layout)
        
        # Filtering options
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filtering Mode:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("No filtering (copy all files)", "none")
        self.filter_combo.addItem("Copy Markdown documents only (.md, .mdx)", "markdown_only")
        self.filter_combo.addItem("Exclude code files", "exclude_code")
        self.filter_combo.addItem("Light filtering (exclude binaries)", "light_filter")
        
        # Set default filter mode from config
        default_filter = self.config.get("filter_mode", "none")
        index = self.filter_combo.findData(default_filter)
        if index >= 0:
            self.filter_combo.setCurrentIndex(index)
            
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        main_layout.addLayout(filter_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Start button
        self.start_button = QPushButton("Grab Docs")
        self.start_button.clicked.connect(self.start_grabbing)
        buttons_layout.addWidget(self.start_button)
        
        # Open docs button (initially hidden)
        self.open_docs_button = QPushButton("Open Docs")
        self.open_docs_button.clicked.connect(self.open_docs)
        self.open_docs_button.setVisible(False)
        buttons_layout.addWidget(self.open_docs_button)
        
        # Settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        buttons_layout.addWidget(self.settings_button)
        
        # Quit button
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.quit_application)
        buttons_layout.addWidget(self.quit_button)
        
        main_layout.addLayout(buttons_layout)
            
    def quit_application(self):
        QApplication.quit()
        
    def browse_directory(self):
        # Start from the base repository path if configured
        start_dir = self.config.get("base_repo_path", "")
        if not start_dir or not os.path.isdir(start_dir):
            start_dir = os.path.expanduser("~")
            
        directory = QFileDialog.getExistingDirectory(self, "Select Target Repository", start_dir)
        if directory:
            self.path_input.setText(directory)
    
    def open_settings(self):
        dialog = SettingsDialog(self.config, self)
        if dialog.exec():
            # Refresh UI with updated settings
            default_path = self.config.get("base_repo_path")
            if default_path and os.path.isdir(default_path):
                self.path_input.setText(default_path)
                
            default_filter = self.config.get("filter_mode", "none")
            index = self.filter_combo.findData(default_filter)
            if index >= 0:
                self.filter_combo.setCurrentIndex(index)
    
    def start_grabbing(self):
        repo_url = self.repo_input.text().strip()
        target_path = self.path_input.text().strip()
        filter_mode = self.filter_combo.currentData()
        
        # Validate inputs
        if not repo_url:
            QMessageBox.warning(self, "Input Error", "Please enter a GitHub repository URL.")
            return
        
        if not target_path:
            QMessageBox.warning(self, "Input Error", "Please select a target repository path.")
            return
        
        if not os.path.isdir(target_path):
            QMessageBox.warning(self, "Path Error", "The selected path is not a valid directory.")
            return
        
        # Validate GitHub URL format
        if not (repo_url.startswith("https://github.com/") or repo_url.startswith("http://github.com/")):
            QMessageBox.warning(self, "URL Error", "Please enter a valid GitHub URL.")
            return
        
        # Disable UI elements during operation
        self.repo_input.setEnabled(False)
        self.path_input.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.start_button.setEnabled(False)
        self.settings_button.setEnabled(False)
        self.filter_combo.setEnabled(False)
        self.quit_button.setEnabled(False)
        self.open_docs_button.setVisible(False)
        
        # Start the clone thread
        self.docs_thread = DocsGrabberThread(repo_url, target_path, filter_mode)
        self.docs_thread.progress_signal.connect(self.update_progress)
        self.docs_thread.status_signal.connect(self.update_status)
        self.docs_thread.finished_signal.connect(self.process_finished)
        self.docs_thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def update_status(self, message):
        self.status_label.setText(message)
    
    def process_finished(self, success, message, docs_path):
        # Re-enable UI elements
        self.repo_input.setEnabled(True)
        self.path_input.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.start_button.setEnabled(True)
        self.settings_button.setEnabled(True)
        self.filter_combo.setEnabled(True)
        self.quit_button.setEnabled(True)
        
        if success:
            self.docs_path = docs_path
            self.open_docs_button.setVisible(True)
            QMessageBox.information(self, "Success", message)
        else:
            self.open_docs_button.setVisible(False)
            QMessageBox.critical(self, "Error", message)
            self.progress_bar.setValue(0)
            self.status_label.setText("Ready")
    
    def open_docs(self):
        if self.docs_path and os.path.exists(self.docs_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.docs_path))
        else:
            QMessageBox.warning(self, "Error", "Documentation path not found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DocsGrabberApp()
    window.show()
    sys.exit(app.exec())
