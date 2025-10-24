---
title: Workshop Lab 6
description: Information Extraction with Generative Slots
logo: images/ibm-blue-background.png
---

# Lab 6 — Information Extraction with Generative Slots

This lab demonstrates simple information extraction using Mellea generative slots. You will define a typed generative function to extract person names from text, run it against a sample document, and inspect the structured output.

## Goals
- Introduce a generative slot for information extraction.
- Show how to start a Mellea session and call generative functions.
- Provide a small, reproducible example for extracting person names from text.

## 1. Setup & imports

Use these imports to create the session and display results.

````python
# Import necessary libraries and display utilities
from mellea import generative, start_session
from mellea.backends import model_ids

from IPython.display import display, Markdown
````



## 2. Define the generative extractor

This generative slot defines the interface and docstring the LLM will follow. The return type is a list of strings (person names).

```python
# Define a generative function to extract person names
@generative
def extract_all_person_names(doc: str) -> list[str]:
    """
    Extract all person names mentioned in the given document text.

    This function analyzes the input text and identifies names of people,
    including full names, titles, and honorifics. It returns a list of unique
    person names found in the document.

    Args:
        doc (str): The input document text to analyze for person names.
                   Can contain paragraphs, quotes, or any text format.

    Returns:
        list[str]: A list of strings where each string is a person's name.
                   Names may include titles (e.g., "President Obama", "Dr. Smith").
                   Returns an empty list if no names are found.
    """
```



## 3. Example usage

Start a session, provide sample text, and call the generative extractor. The example shows how to pass the session and input and how to print results.

```python
# Start a Mellea session
m = start_session()

# Example document text
NYTimes_text = """CAMP DAVID, Md. — Leaders of the world's richest countries banded together on Saturday
to press Germany to back more pro-growth policies ... as President Obama ... cannot afford Chancellor Angela Merkel's ..."""

# Call the generative extractor
person_names = extract_all_person_names(m, doc=NYTimes_text)

# Display results
print(f"person_names = {person_names}")
# expected: person_names = ['President Obama', 'Angela Merkel']
```



## 4. Notes and tips

- Keep the function signature and docstring precise; they form the spec the LLM imitates.
- Use typed return values (lists, dicts, literals) to simplify validation and downstream processing.
- Test on varied documents (news, papers, transcripts) to evaluate extraction robustness.



## 5. Exercises

- Extend the extractor to include entity types (person, organization, location) and return structured records.
- Add a confidence field or provenance (text span) for each extracted name.
- Compose the extractor with a deduplication/normalization step (e.g., convert "B. Obama" → "Barack Obama").
