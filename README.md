# AI Code Generation Prompts Examples (Python)

13-Mar-25

![alt text](banner.webp)

## Table of Contents

- [Introduction](#introduction)
- [Code Example](#code-example)
- [Projects](#projects)
- [Prompting Techniques](#prompting-techniques)
- [Favorite AI Code Generation Tools](#favorite-ai-code-generation-tools)

## Introduction

The purpose of this repository is to provide a few sample prompts used in order to create a simple Python GUI for the Linux desktop [project](https://github.com/danielrosehill/Docs-Grabber).

I created this repository and wrote these prompts on March 13th, 2025. The evolution of AI and the art of prompt engineering are both so fast that these techniques will likely be deprecated as agentic IDEs develop progressively better internal prompting structures and models get better at facilitating this kind of use. 

Nevertheless, I chose to share them because they represent a mode of prompting for GUI creation that I found particularly effective. 

## Code Example

You can find the actual code example for the Python GUI in the [docs_grabber.py](./code/docs_grabber.py) file located in the `code` folder.

## Projects

Here are the projects mentioned in this repository:

- [Docs-Grabber](https://github.com/danielrosehill/Docs-Grabber)
- [RooCode](https://example.com/roocode)
- [Windsurf](https://example.com/windsurf)
- [Cline](https://example.com/cline)

## Prompting Techniques

The key constituent elements are as follows:

# 1: Record your prompts!

Agentic IDE tools usually work by providing a convenient sidebar to model the experience of typing into a chat UI that countless people are familiar with.

This makes it extremely tempting to just write casual prompts into the chat bot and quickly forget about them. 

However, there is a lot of value in resisting this temptation and writing more detailed prompts and also recording them as artifacts in their repository itself:

1) Repository mobility: Detailed code generation prompts and debugging instructions take time and consideration to author effectively. If you're working in a collaborative coding environment, or you are simply using a number of development tools, writing out the prompts makes it much easier to move between different IDEs. Given the up and down state of many of the development tools at the moment, it makes sense to keep this portability in mind.

2) Prompt reuse and versioning: You'll frequently find that you reuse the same snippets in many prompts. This can be handled by using snippets.  A good way to speed up the population of an effective prompting library is to simply record your prompts in the individual repositories. Note: I will freely admit that I have very mixed feelings about the utility of formalizing prompt libraries. 

# 2: Name your files for semantic searchability

Large code bases provide inherent challenges to large language models, which are tasked with ingesting huge amounts of tokens in order to effectively understand the code base. 

I have seen abundant evidence that being very precise and detailed in how you label your files and folders actually makes it easy for the agents to find their way around the code. 

This doesn't only apply to the code parts of the repository, but also to the documentation - or in this case the instructions that you may version as documentation.

For that reason, I like to use, at a minimum, the following organisation structure:

- development-prompts 
- debugging 
- iterations 
- feature-additions 

# 3 - Drop in prompts as context

The very easy way to use prompts in chat UIs is to simply provide them as context in the UI itself. 

For example:

'We need to debug this Python app. See `your-file.md` for detailed instructions


# 4: Pair system prompts with user prompts for maximum efficiency 

Another hack of sorts that I have latched onto is using system prompting in order to streamline agents when using repositories that contain prompts written out as markdown documents. 

I've been able to implement this most effectively using Roo Code. 

For example, create modes for development from prompts, debugging from prompts, or. Editing from prompts. 

Then, write a mode prompt for each mode along these lines:

For initiation:

`You are a helpful programming sidekick whose purpose is to help me to generate a Python program from scratch. In the repository you will find a development prompt in the following folder: /docs/devprompt.md. Take this as your initial instruction and immediately begin developing the project. `

For debugging:

`You are a helpful programming assistant whose purpose is to help me to debug applications. In this repository you will find a folder of markdown files at the following location /docs/debugging. Find the highest numbered version in this folder. For example, if there is round1.md and round2.md, take round2.md to be your instruction. Proceed according to its directives.`

# 5 - Be modular, very modular

Using agentic code generation tools can at first feel a little bit like stepping into an exciting vision of the future in which AI is beginning to reach something like its full potential. 

Unfortunately, many will quickly discover that this is not quite the case. 

Although AI tools are fast maturing and incredibly impressive and powerful, they are nevertheless limited. 

At the time of writing, one of the main limitations for code generation and code editing projects is the sheer context load posed on large language models by the number of characters contained in your average code base. 

While technologies like caching and selective context injection can mitigate against these limitations to some extent, they remain imperfect solutions.

For now, those of us who use LLMs for this purpose frequently have to make do with our own hacks that we develop on the go. 

One of the most popular and effective of these is to be very modular in your tasks. 

I'm frequently tempted to write a long prompt which will ask a model to provide wide ranging fixes over a code base, tackling things from CSS through to actual code. Unfortunately, more often than not this results in poor results, deviated instructions and sometimes even destroyed files.

In practice, it's much more effective to limit your prompts to one or perhaps three very short tasks at a time. 

This prompting model pairs nicely with the default design of tools like Cline, Roo Code, and Windsurf which are built with precisely this kind of workflow in mind.

## Favorite AI Code Generation Tools

At the time of writing, these are the tools I'm using for AI code generation:

- **OpenHands**: A versatile tool for AI-driven development.
- **Windsurf IDE**: An integrated development environment tailored for AI projects.
- **Sonnet 3.7**: Known for its robust performance in AI applications.
- **Aider**: A tool that complements AI development with additional insights.

Additionally, I'm using **OpenRouter** for API access to a wide variety of models. Although it struggles with agentic capabilities, **Qwen's coder models** are some of my favorites for coding projects due to their efficiency and accuracy.