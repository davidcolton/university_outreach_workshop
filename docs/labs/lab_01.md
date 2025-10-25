---
title: Workshop Lab 1
description: Hello Mellea
logo: images/ibm-blue-background.png
---

# What is Generative Computing?

A generative program is any computer program that contains calls to an LLM. As we will see throughout the documentation, LLMs can be incorporated into software in a wide variety of ways. Some ways of incorporating LLMs into programs tend to result in robust and performant systems, while others result in software that is brittle and error-prone.

Generative programs are distinguished from classical programs by their use of functions that invoke generative models. These generative calls can produce many different data types — strings, booleans, structured data, code, images/video, and so on. The model(s) and software underlying generative calls can be combined and composed in certain situations and in certain ways (e.g., LoRA adapters as a special case). In addition to invoking generative calls, generative programs can invoke other functions, written in languages that do not have an LLM in their base, so that we can, for example, pass the output of a generative function into a DB retrieval system and feed the output of that into another generator. Writing generative programs is difficult because generative programs interleave deterministic and stochastic operations.

If you would like to read more about this, please don't hesitate to take a look [here](https://docs.mellea.ai/overview/project-mellea).

## Mellea

[Mellea](https://github.com/generative-computing/mellea) is a library for writing generative programs. Generative programming replaces flaky agents and brittle prompts with structured, maintainable, robust, and efficient AI workflows.

## Features

- A standard library of opinionated prompting patterns.
- Sampling strategies for inference-time scaling.
- Clean integration between verifiers and samplers.
- Batteries-included library of verifiers.
- Support for efficient checking of specialized requirements using activated LoRAs.
- Train your own verifiers on proprietary classifier data.
- Compatible with many inference services and model families. Control cost and quality by easily lifting and shifting workloads between:
  - inference providers
  - model families
  - model sizes
- Easily integrate the power of LLMs into legacy code-bases (mify).
- Sketch applications by writing specifications and letting `mellea` fill in the details (generative slots).
- Get started by decomposing your large unwieldy prompts into structured and maintainable Mellea problems.



## Lab 1: Hello Mellea

Running `mellea.start_session()` initialize a new `MelleaSession`. The session holds three things:

1. The model to use for this session.
2. An inference engine; i.e., the code that actually calls our model. We will be using ollama, but you can also use Huggingface or any OpenAI-compatible endpoint.
3. A `Context`, which tells Mellea how to remember context between requests. This is sometimes called the "Message History" in other frameworks. Throughout these early tutoriala, we will be using a `SimpleContext`. In `SimpleContext`, **every request starts with a fresh context**. There is no preserved chat history between requests. Mellea provides other types of context, but for now we will not be using those features. See the [Mellea Tutorials](https://github.com/generative-computing/mellea) for further details.



## Prerequisites

This lab is a [Jupyter notebook](https://jupyter.org/). Please follow the instructions in [pre-work](../labs/pre_work.md) to configure the environment for the lab.




## Loading the Lab

To run the notebook from command line in Jupyter using the activated virtual environment from the [pre-work](../labs/pre_work.md), run:

```shell
jupyter-lab
```

When Jupyter Lab opens the path to the `labs/lab_01.ipynb` notebook file is relative to the root folder from the git clone in the  [pre-work](../labs/pre_work.md). The folder navigation pane on the left-hand side can be used to navigate to the file. Once the notebook has been found it can be double clicked and it will open to the pane on the right.

Alternatively, if you already have it configured and setup on you laptop, VSCode could be used either (don't forget to select the virtual environment).



!!! Note
    All notebooks in this set of examples can be opened in this manner apart from `lab_07` which is a python script and is run from the command line.



### Imports

```python
# Import necessary libraries
import mellea

# Display utilities
from IPython.display import display, Markdown

# Format code cells with black
import jupyter_black
jupyter_black.load() 
```

To use Mellea we import the `mellea` library. The other imports are only for displaying output and for formatting the notebook cells and can be ignored.

!!! Note
    If you see something about the Rust compiler, please confirm you are using python3.11, or python3.12 anything above that has a Rust dependency.

### Chat with Mellea

We can have a simple chat with a `mellea` session by starting a session, `m`, and then using the `chat` function. We can then display the answer by displaying the answer objects content.

```python
# Create a Mellea model using the granite3.3:8b model and the ollama inference engine
m = mellea.start_session()

# Send a chat message to the model
# In this example, we are asking for fun trivia about IBM and the early history of AI.
# Since we are using a SimpleContext, there is no preserved chat history between requests.
# Each request starts fresh.
answer = m.chat(
    "tell me some fun trivia about IBM and the early history of AI."
)

# Display the answer in markdown format
display(Markdown(answer.content))
```



## Start a Session with LinearContext

In the first example we have used SimpleContext, a context manager that resets the chat message history on each model call. That is, the model's context is entirely determined by the current Component.

Mellea also provides a LinearContext, which behaves like a chat history. We can use the ChatContext to interact with chat models

```python
from mellea import start_session
from mellea.stdlib.base import ChatContext

# Create a session with chat context
m = start_session(ctx=ChatContext())

# Generate and store responses
problem = m.chat("Make up a math problem.")
solution = m.chat("Solve your math problem.")

# Display the problem and solution using the content attribute
display(Markdown(f"Problem:\n{problem.content}\nSolution:\n{solution.content}"))
```

