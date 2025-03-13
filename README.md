# AI Code Generation Prompts Examples (Python)

*13-Mar-25*

![alt text](banner.webp)

---

## Table of Contents

- [Introduction](#introduction)
- [Code Example](#code-example)
- [Projects](#projects)
- [Prompting Techniques](#prompting-techniques)
- [Favorite AI Code Generation Tools](#favorite-ai-code-generation-tools)

---

## Introduction

The purpose of this repository is to provide a few sample prompts used in order to create a simple Python GUI for the Linux desktop [project](https://github.com/danielrosehill/Docs-Grabber).

I created this repository and wrote these prompts on March 13th, 2025. The evolution of AI and the art of prompt engineering are both so fast that these techniques will likely be deprecated as agentic IDEs develop progressively better internal prompting structures and models get better at facilitating this kind of use.

Nevertheless, I chose to share them because they represent a mode of prompting for GUI creation that I found particularly effective.

---

## Code Example

You can find the actual code example for the Python GUI in the [docs_grabber.py](./code/docs_grabber.py) file located in the `code` folder.

---

## Projects

Here are the projects mentioned in this repository:

- [Docs-Grabber](https://github.com/danielrosehill/Docs-Grabber)
- [RooCode](https://example.com/roocode)
- [Windsurf](https://example.com/windsurf)
- [Cline](https://example.com/cline)

---

## Prompting Techniques

### Record Your Prompts Meticulously

I make it a point to meticulously record every single prompt, not just the development prompts but also all subsequent debugging prompts and UI editing prompts. I prefer to keep these organized in separate folders to maintain clarity and ease of access.

---

### File and Folder Naming for RAG (Retrieval-Augmented Generation)

Naming files and folders with precision is crucial for retrieval-augmented generation (RAG). This practice enhances the ability of large language models to navigate and understand code bases efficiently. Here's a model folder structure that I find effective:

- **development-prompts/**: Contains development-related prompts.
- **debugging/**: Stores prompts used for debugging purposes.
- **ui-edits/**: Holds prompts for UI editing tasks.

---

### Pair System Prompts with User Prompts

Leveraging system prompting can streamline agentic interactions, especially when repositories contain markdown prompts. This approach has been effective in tools like Roo Code. For example, create modes for development from prompts, debugging from prompts, or editing from prompts. Then, write a mode prompt for each mode along these lines:

- **For initiation**: "You are a helpful programming sidekick whose purpose is to help me to generate a Python program from scratch. In the repository, you will find a development prompt in the following folder: /docs/devprompt.md. Take this as your initial instruction and immediately begin developing the project."

- **For debugging**: "You are a helpful programming assistant whose purpose is to help me to debug applications. In this repository, you will find a folder of markdown files at the following location /docs/debugging. Find the highest numbered version in this folder. For example, if there is round1.md and round2.md, take round2.md to be your instruction. Proceed according to its directives."

- **UI Fixes**: "You are a helpful assistant tasked with improving the user interface. Refer to the `ui-edits` folder for guidance."

- **Security Review**: "Conduct a security review using the guidelines in `security-prompts.md`."

---

### Be Modular

While AI tools are powerful, they have limitations. Being modular in task execution—focusing on one or a few tasks at a time—yields better results and aligns with the design of tools like Cline, Roo Code, and Windsurf. Here are some examples:

- **Effective Prompt**: "Refactor the login module to enhance security."
- **Ineffective Prompt**: "Refactor the entire application for security, UI, and performance optimizations."

---

## Favorite AI Code Generation Tools

At the time of writing, these are the tools I'm using for AI code generation:

- **OpenHands**: A versatile tool for AI-driven development.
- **Windsurf IDE**: An integrated development environment tailored for AI projects.
- **Sonnet 3.7**: Known for its robust performance in AI applications.
- **Aider**: A tool that complements AI development with additional insights.

Additionally, I'm using **OpenRouter** for API access to a wide variety of models. Although it struggles with agentic capabilities, **Qwen's coder models** are some of my favorites for coding projects due to their efficiency and accuracy.

---

## Conclusion

As the landscape of AI and prompt engineering continues to evolve, these insights and tools serve as a foundation for effective AI-driven development. Whether you're exploring new IDEs or refining your prompting techniques, the journey is as dynamic as the technology itself.

---