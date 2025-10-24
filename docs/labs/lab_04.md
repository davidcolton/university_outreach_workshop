---
title: Workshop Lab 4
description: Docling and Mellea
logo: images/ibm-blue-background.png
---

# Lab 4 — Docling and Mellea

This lab demonstrates how to combine Docling (document extraction) with Mellea (generative workflows) to extract structured content from PDFs and perform LLM-powered transformations on extracted objects.

Goals

- Load a PDF into a RichDocument using Docling.
- Extract table objects and inspect them.
- Use a Mellea session (with an Ollama backend) to transform Docling Table objects.
- Observe how Mellea-friendly Docling objects can be used directly with LLM transforms.



---

## 1. Setup and imports

Core imports for Docling, Mellea, the Ollama backend, and notebook display utilities.

```python
# Python imports for [lab_04.ipynb](http://_vscodecontentref_/0)
from pathlib import Path
import mellea
from mellea.backends.model_ids import META_LLAMA_3_2_3B
from mellea.backends.ollama import OllamaModelBackend
from mellea.backends.types import ModelOption
from mellea.stdlib.docs.richdocument import RichDocument
from mellea.stdlib.docs.richdocument import Table
```



## 2. Load a PDF and extract the first table

This snippet uses RichDocument.from_document_file to load a PDF (via URL or file path), then gets the first table and renders it as Markdown.

```python
# Load a document from a URL and extract the first table
rd = RichDocument.from_document_file("https://arxiv.org/pdf/1906.04043")

# Extract the first table from the document
first_table: Table = rd.get_tables()[0]

# Display the first table in markdown format
display(Markdown(first_table.to_markdown()))
```

Why it matters: RichDocument wraps Docling-extracted structure (text, tables, figures) into Mellea-friendly objects that can be inspected or passed to transforms.



## 3. Transform a Table with a Mellea session and Ollama backend

Demonstrates creating a MelleaSession configured for a specific model and calling transform repeatedly with different random seeds to see variability in LLM outputs. The transform instruction asks the model to add a "Model" column derived from the "Feature" column.

```python
# Create a Mellea session using an Ollama backend model
m_llama = mellea.MelleaSession(backend=OllamaModelBackend(model_id=META_LLAMA_3_2_3B))

for seed in [x * 12 for x in range(5)]:
    table2 = m_llama.transform(
        first_table,
        "Add a 'Model' column as the last column that extracts which model was used for that feature or 'None' if none.",
        model_options={ModelOption.SEED: seed},
    )
    if isinstance(table2, Table):
        display(Markdown(table2.to_markdown()))
    else:
        print("==== TRYING AGAIN after non-useful output.====")
```

Notes:

- model_options can control behavior (e.g., deterministic sampling via seed).
- The transform returns a new Table object when the LLM output conforms; otherwise you should handle retries or fallbacks.



## 4. Working with the Table object

The Table returned by RichDocument / transforms is an object with methods to export, inspect, or feed into other generative slots. Typical operations include converting to markdown, CSV, or passing into further transforms. Here we just connect to Markdown to display the table.

```python
# Render table as markdown for human inspection
display(Markdown(first_table.to_markdown()))
```



## Tips & best practices

- Keep transform instructions precise and scoped; ask for structured outputs when you expect objects back.
- Inspect the RichDocument structure before transforming (rd.get_tables(), rd.get_figures(), etc.).
- Use model options to control sampling behavior when debugging nondeterministic outputs.