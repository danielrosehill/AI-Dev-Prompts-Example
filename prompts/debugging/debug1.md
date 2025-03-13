# Feedback Prompt 1

## Introduction

This document outlines the necessary bug fixes for the first version of the doc grabber utility.

## Bug Fixes

- The utility clones the repository. It should either import the documents without cloning the repository or clone the repository and then delete the `.git` folder in the clone it creates.
- The presence of a second git folder could create problems for the user, as the utility is intended to import documentation into a Git repository.