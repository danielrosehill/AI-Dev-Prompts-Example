# Development Prompt for Sonnet

## Introduction

Your task is to develop a basic GUI for the Linux desktop using PyQt5 or PyQt6. The purpose of this GUI is to facilitate the copying of documentation from a GitHub repository into a working repository, providing contextual information for AI tools like code generation utilities.

## Requirements

- Use PyQt5 or PyQt6 for the GUI.
- Provide a path selection field for the user to choose where the docs should be saved.
- Save the docs to a folder called `reference` within the selected path.
- Exclude the `.git` folder during the pull from GitHub to avoid conflicts.

## Example Links

- Docs folder structure: https://github.com/All-Hands-AI/OpenHands/tree/main/docs
- Contained docs repository: https://github.com/open-webui/docs

## Functionality

1. The user provides the link to the documentation route of a GitHub repository.
2. The user selects the path where the docs should be saved.
3. The program pulls the documents from GitHub and copies them to the selected save path.
4. A progress indicator shows the copy progress.
5. A success message is displayed when the documents have been copied.

## Instructions for Use

- Click the "Grab Docs" button to start the process.
- Ensure the path selection is correct before initiating the pull.

## Output Details

- Generate a file called `ai-instructions.md` at the root of the target folder with the following format:

# AI Instructions: Documentation Context Folder

This folder contains documentation for the following GitHub repository: {repo-name}.

It is intended to provide you with context on how this SDK or utility operates. Do not edit the documentation in this folder or its recursive paths.

It was imported from the internet on: {runtime}.

The original URL was {repourl}

Replace placeholders with actual values during runtime.
