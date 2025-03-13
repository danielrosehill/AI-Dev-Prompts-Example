# Exploring AI Code Generation Prompts: A Journey with Python

**Date:** March 13, 2025

Welcome to a deep dive into the world of AI code generation prompts, where we explore the techniques and tools that have shaped my journey in developing a simple Python GUI for the Linux desktop.

## Introduction

The purpose of this exploration is to provide insights into the sample prompts used to create a Python GUI, as detailed in the [Docs-Grabber project](https://github.com/danielrosehill/Docs-Grabber). While the field of AI and prompt engineering evolves rapidly, these techniques represent a snapshot of effective prompting strategies at this time.

## Key Techniques in Prompting

### 1. Record Your Prompts Meticulously

I make it a point to meticulously record every single prompt, not just the development prompts but also all subsequent debugging prompts and UI editing prompts. I prefer to keep these organized in separate folders to maintain clarity and ease of access.

### 2. File and Folder Naming for RAG (Retrieval-Augmented Generation)

Naming files and folders with precision is crucial for retrieval-augmented generation (RAG). This practice enhances the ability of large language models to navigate and understand code bases efficiently. Here's a model folder structure that I find effective:

- **development-prompts/**: Contains development-related prompts.
- **debugging/**: Stores prompts used for debugging purposes.
- **ui-edits/**: Holds prompts for UI editing tasks.

### 3. Drop in Prompts as Context

Utilize chat UIs by providing prompts as context, streamlining the debugging and development process.

### 4. Pair System Prompts with User Prompts

Leveraging system prompting can streamline agentic interactions, especially when repositories contain markdown prompts. This approach has been effective in tools like Roo Code. Here are some examples:

- **UI Fixes**: "You are a helpful assistant tasked with improving the user interface. Refer to the `ui-edits` folder for guidance."
- **Security Review**: "Conduct a security review using the guidelines in `security-prompts.md`."

### 5. Be Modular

While AI tools are powerful, they have limitations. Being modular in task execution—focusing on one or a few tasks at a time—yields better results and aligns with the design of tools like Cline, Roo Code, and Windsurf. Here are some examples:

- **Effective Prompt**: "Refactor the login module to enhance security."
- **Ineffective Prompt**: "Refactor the entire application for security, UI, and performance optimizations."

## Favorite AI Code Generation Tools

At the time of writing, these are the tools I'm using for AI code generation:

- **OpenHands**: A versatile tool for AI-driven development.
- **Windsurf IDE**: An integrated development environment tailored for AI projects.
- **Sonnet 3.7**: Known for its robust performance in AI applications.
- **Aider**: A tool that complements AI development with additional insights.

Additionally, I'm using **OpenRouter** for API access to a wide variety of models. Although it struggles with agentic capabilities, **Qwen's coder models** are some of my favorites for coding projects due to their efficiency and accuracy.

## Conclusion

As the landscape of AI and prompt engineering continues to evolve, these insights and tools serve as a foundation for effective AI-driven development. Whether you're exploring new IDEs or refining your prompting techniques, the journey is as dynamic as the technology itself.
