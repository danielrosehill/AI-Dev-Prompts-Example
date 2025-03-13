# Edit Prompt 2

## Introduction

We're making good progress on the development of the GUI.

I can confirm that the cloning functionality now works as expected with the correct level of recursion.

## Feature Addition 1: Persistent Memory

- Allow users to set basic parameters that retain in persistent memory.
- Create a simple memory file in the user's config directory (~/.config) with a unique name.
- In the settings menu, enable users to choose the base path for their Github repositories.
- Provide a save button to memorize the base path for future runs, saving user time.

## Feature Addition 2: Selective Copying

- Integrate a feature for selective copying to avoid extraneous non-docs.
- Decide whether to implement filtering at the copying level or apply targeted deletions afterward.

### Filtering Rules

1. **Copy Markdown Documents Only**: Copy only markdown files using the extension filtering pattern: md, mdx. Delete non-matching files.
2. **Second Filtering Rule**: Develop a rule to exclude code from repositories containing a mix of documentation and code.
3. **Third Filtering Rule**: Implement a light filtering rule to exclude files that are definitely code, not intended as code samples.