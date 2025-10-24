# Lab 07: MiniResearcher Pipeline

## Introduction

This lab demonstrates a structured generative programming pipeline using the Mellea framework and Ollama model backend. The goal is to generate a professional report based on a subtopic and main topic using a set of source documents. The pipeline includes safety validation, summarization, outline generation, and final report synthesis. It leverages Mellea's `MelleaSession` for model interaction, `Requirement` objects for constraint validation, and `RejectionSamplingStrategy` to ensure outputs meet defined standards.

The main highlights are given below.

---

## Session Initialization

```python
@cache
def get_session():
    return MelleaSession(backend=OllamaModelBackend(model_ids.IBM_GRANITE_4_MICRO_3B))

@cache
def get_guardian_session():
    return MelleaSession(
        backend=OllamaModelBackend(model_ids.IBM_GRANITE_GUARDIAN_3_0_2B)
    )
```

These functions initialize and cache two model sessions:

- `get_session()` sets up the main model used for summarization and report generation.
- `get_guardian_session()` initializes a safety-focused model to validate document content.

**Highlights:**

- Uses `OllamaModelBackend` to run local LLMs.
- Caching avoids repeated initialization.
- Supports modular backend switching.

---

## Input Safety Check

```python
def step_is_input_safe(guardian_session: MelleaSession, docs: list[str]) -> bool:
    is_safe = True
    for i_doc, doc in enumerate(docs):
        inspect = guardian_session.chat(doc)
        if str(inspect).upper().startswith("YES"):
            is_safe = False
            break
    return is_safe
```

This function checks each document for harmful content using the guardian model.

**Highlights:**

- Iterates through all documents.
- Uses `chat()` to query the guardian model.
- Flags unsafe content based on model response.

---

## Document Summarization

```python
def step_summarize_docs(s: MelleaSession, docs: list[str], user_args: dict) -> list[str]:
    summaries = []
    for doc in docs:
        summary = s.instruct(
            f"Summarize the following document to answer the question: 'How {{current_subtopic}} impacts {{main_topic}}?' 
 Document: {doc}",
            requirements=["Use maximal 3 sentences."],
            user_variables=user_args,
        )
        summaries.append(str(summary))
    return summaries
```

This function summarizes each document with a task-specific prompt.

**Highlights:**

- Uses `instruct()` to generate summaries.
- Applies a sentence limit constraint.
- Injects user-defined variables for context.

---

## Outline Generation

```python
def step_generate_outline(s: MelleaSession, user_args: dict, context: list[RAGDocument]) -> list[str]:
    class SectionTitles(BaseModel):
        section_titles: list[str]

    def must_have_sections(out: str) -> bool:
        stt = SectionTitles.model_validate_json(out)
        return is_a_true_subset_of_b(["Introduction", "Conclusion", "References"], stt.section_titles)

    def max_sub_sections(out: str) -> bool:
        stt = SectionTitles.model_validate_json(out)
        return len(stt.section_titles) <= 3 + user_args["max_subsections"]

    req_outline = Requirement("Include Introduction, Conclusion, and References", validation_fn=simple_validate(must_have_sections))
    req_num_sections = Requirement(f"Limit subsections to {user_args['max_subsections']}", validation_fn=simple_validate(max_sub_sections))

    outline_result = s.instruct(
        description="Create an outline for a report...",
        requirements=[req_outline, req_num_sections],
        user_variables=user_args,
        grounding_context={f"Document {i+1}": f"## Title: {d.title}, ## Source: {d.source}" for i, d in enumerate(context)},
        strategy=RejectionSamplingStrategy(loop_budget=2),
        return_sampling_results=True,
        format=SectionTitles,
    )
    return SectionTitles.model_validate_json(outline_result.value).section_titles
```

This function generates a structured outline for the report.

**Highlights:**

- Uses Pydantic `BaseModel` for structured output.
- Validates outline using `Requirement` and `simple_validate`.
- Applies `RejectionSamplingStrategy` to enforce constraints.

---

## Report Writing

```python
def step_write_full_report(m: MelleaSession, max_words: int, user_args: dict, summaries: list[str], outline: list[str]) -> str:
    req_focus = Requirement("Stay focused on the topic.")
    req_language = Requirement(f"Write in {user_args['language']}.")
    req_tone = Requirement("Use a {{tone}} tone.")
    req_length = Requirement(
        f"Max length {max_words} words.",
        validation_fn=simple_validate(create_check_word_count(max_words))
    )

    user_args.update({
        "context": "
".join(summaries),
        "outline": "
".join([f"* {o}" for o in outline]),
    })

    report_result = m.instruct(
        description="Context:
{{context}}
Summarize into a detailed report...",
        requirements=[req_focus, req_length, req_language, req_tone],
        user_variables=user_args,
        strategy=RejectionSamplingStrategy(loop_budget=2, requirements=[req_length]),
        return_sampling_results=True,
    )
    return report_result.value
```

This function composes the final report using summaries and outline.

**Highlights:**

- Enforces multiple constraints: tone, language, length.
- Uses `RejectionSamplingStrategy` to retry until valid output.
- Combines structured context and outline for coherent generation.

---

## `lab_07_context.py`

This file defines the `RAGDocument` dataclass and provides a list of documents used in the pipeline.

```python
@dataclass
class RAGDocument:
    title: str
    source: str
    content: str
```

**Highlights:**

- Encapsulates metadata and content.
- Used for grounding context in outline generation.
- Enables structured document handling.

---

## How to Run the Script

1. Install dependencies (if run in Workshop folder and virtual environment is activated this is not required as dependencies are already resolved):

```bash
pip install mellea openai pydantic
```

2. Run the script:

```bash
python lab_07.py
```

3. Output includes:

- Safety validation results
- Summaries of documents
- Generated outline
- Final report

---
