# LAB_NormalObjects_LangGraph

## Overview

This project implements Bloyce's Protocol using LangGraph. Complaints are processed through a structured workflow consisting of:

1. Intake
2. Validation
3. Investigation
4. Resolution
5. Closure

The workflow uses state management and conditional routing to handle both valid and invalid complaints.

## Files

* `normalobjects_langgraph.py` - Main LangGraph workflow implementation
* `lab_summary.md` - Comparison of LangGraph and LangChain approaches
* `README.md` - Project documentation

## Requirements

* Python 3.13+
* langgraph
* langchain
* langchain-openai
* python-dotenv

## Running the Project

Activate the virtual environment and run:

```bash
python normalobjects_langgraph.py
```

The script processes sample complaints and displays the workflow path for each complaint.
