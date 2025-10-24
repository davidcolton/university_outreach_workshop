---
title: Workshop Lab 3
description: Writing Compositional Code with Generative Stubs
logo: images/ibm-blue-background.png
---

# Lab 3 — Writing Compositional Code with Generative Stubs

This lab demonstrates how to use Mellea's `@generative` slots as compositional building blocks. It shows a small summarizer library, decision-aide functions, and compositionality checks that let LLM-powered functions be combined in predictable, testable ways.

In classical programming, pure (stateless) functions are a simple and powerful abstraction. A pure function takes inputs, computes outputs, and has no side effects. Generative programs can also use functions as abstraction boundaries, but in a generative program the meaning of the function can be given by an LLM instead of an interpreter or compiler. This is the idea behind a GenerativeSlot.

A GenerativeSlot is a function whose implementation is provided by an LLM. In Mellea, you define these using the `@generative` decorator. The function signature specifies the interface, and the docstring (or type annotations) guides the LLM in producing the output.

In this lab, we will see how **compositionality checks** can be used to combine libraries of generative functions.

## Goals
- Show how to define generative functions (GenerativeSlots) with clear signatures and docstrings.
- Build small, composable libraries: summarizers and decision aides.
- Use compositionality checks to gate downstream decisions.
- Demonstrate wiring these pieces together on a meeting transcript.

---

## Main code snippets of interest

### 1. Imports and setup
The notebook initialises Mellea and type hints. This cell sets the execution environment used by all generative calls.

Key items:
- `from mellea import generative`
- `from typing import Literal`

### 2. Summariser library
A small collection of generative slots that produce human-readable summaries.

Representative function signatures:
```python
@generative
def summarize_meeting(transcript: str) -> str: ...

@generative
def summarize_contract(contract_text: str) -> str: ...

@generative
def summarize_short_story(story: str) -> str: ...
```

Each function's docstring guides the LLM to produce outputs matching the annotated return type (here, `str`). Please view the lab notebook to see the full docstring.

Note:
   **`@generative`**: Converts a function into an AI-powered function. This decorator transforms a regular Python function into one that uses an LLM to generate outputs. The function's entire signature - including its name, parameters, docstring, and type hints - is used to instruct the LLM to imitate that function's behavior. The output is guaranteed to match the return type annotation using structured outputs and automatic validation.

### 3. Decision-aides library

Generative slots that turn structured summaries into actionable recommendations or mitigations.

Representative functions:

```python
@generative
def propose_business_decision(summary: str) -> str: ...

@generative
def generate_risk_mitigation(summary: str) -> str: ...

@generative
def generate_novel_recommendations(summary: str) -> str: ...
```

These are intended to be called only when upstream compositionality checks validate the summary.

### 4. Example: Summarize a meeting transcript

A long example transcript is provided and passed to the summarizer:

```python
m = mellea.start_session()
summary = summarize_meeting(m, transcript=transcript)
display(Markdown(f"# Summary of meeting:\n {summary}"))
```

This demonstrates end-to-end use of a generative slot and rendering results in a notebook.

### 5. Compositionality checks

Small generative validators that return `Literal["yes","no"]` and are used to control flow:

- `has_structured_conclusion(summary: str) -> Literal["yes","no"]`
- `contains_actionable_risks(summary: str) -> Literal["yes","no"]`
- `has_theme_and_plot(summary: str) -> Literal["yes","no"]`

These functions let the program ask LLMs whether an output satisfies a structural property before invoking downstream decision aides.

### 6. Applying decision aides conditionally

Example control flow that shows how compositionality checks gate downstream actions:

```python
if contains_actionable_risks(m, summary=summary) == "yes":
    mitigation = generate_risk_mitigation(m, summary=summary)
    display(Markdown(f"## Mitigation:\n{mitigation}"))
else:
    display(Markdown("Summary does not contain actionable risks."))
```

and

```python
if has_structured_conclusion(m, summary=summary) == "yes":
    decision = propose_business_decision(m, summary=summary)
    display(Markdown(f"# Decision:\n{decision}"))
else:
    display(Markdown("Summary lacks a structured conclusion."))
```

### Notes and best practices

- Keep generative slot docstrings precise: the function signature + docstring form the spec the LLM imitates.
- Prefer machine-friendly return types (lists, dicts, typed literals) to simplify downstream aggregation and validation.
- Use compositionality checks to reduce downstream hallucination and to make control flow auditable.