---
title: Workshop Lab 5
description: Generative Objects
logo: images/ibm-blue-background.png
---

# Lab 5 — Generative Objects

This lab demonstrates how to wrap structured data with domain methods and expose them to LLMs using Mellea's MObject pattern. You will learn how to convert a plain Python class into an MObject with `@mify`, parse CSV-style text into a DataFrame, and run LLM-driven queries and transforms against the object.

## Goals
- Introduce the MObject pattern and `@mify`.
- Show how to store structured data (CSV string) with helper methods.
- Demonstrate using a Mellea session to query and transform the object.

---

## 1. Setup & imports

Key imports required for this lab.

```python
# Python imports for 
import pandas as pd
import mellea
from mellea.stdlib.mify import mify
```



## 2. MyCompanyDatabase MObject

This class holds a CSV table as a string and exposes parsing and update helpers. The `@mify` decorator controls what is visible to the LLM and how the object is rendered.

```python
@mify(fields_include={"table"}, template="{{ table }}")
class MyCompanyDatabase:
    def __init__(self, *, table: str | None = None):
        if table is not None:
            self.table = table

    def _parse_table(self, table: str) -> pd.DataFrame:
        """
        Parse the CSV table string into a pandas DataFrame and coerce Sales to int.
        """
        df = pd.read_csv(StringIO(table), sep=",")
        if "Sales" in df.columns:
            df["Sales"] = pd.to_numeric(
              df["Sales"].astype(str).str.strip(), errors="coerce").fillna(0).astype(int)
        return df

    def update_sales(self, store: str, amount: int) -> "MyCompanyDatabase":
        """
        Update the sales for `store` to `amount` and return a new MyCompanyDatabase.
        """
        df = self._parse_table(self.table)
        mask = df["Store"].astype(str).str.strip().str.lower() == store.strip().lower()
        df.loc[mask, "Sales"] = int(amount)
        return MyCompanyDatabase(table=df.to_csv(sep=",", index=False, header=True))
```

Notes:

- `_parse_table` ensures the Sales column is numeric.
- `update_sales` returns a new instance (functional/immutable style) suitable for generative transformations.



## 3. Example usage: query & transform

Create a Mellea session, query the object, and apply a transform to update it.

```python
# Create a Mellea session
m = mellea.start_session()

# Construct the database and ask a question
db = MyCompanyDatabase()
print(m.query(db, "What were sales for the Northeast branch this month?"))

# Apply a transform (LLM-driven) to update data
db = m.transform(db, "Update the northeast sales to 1250.")
print(m.query(db, "What were sales for the Northeast branch this month?"))
```

Tips:

- Use `m.query` for read-only LLM queries and `m.transform` to request object updates.
- Keep transformation instructions narrow and structured so the LLM returns a valid object.



## Best practices

- Prefer machine-friendly return types and well-documented methods; docstrings become the LLM's spec.
- Expose only necessary fields/methods to the LLM via `@mify(fields_include=...)`.
- Use small, testable transforms and explicit validation to reduce hallucination and keep pipelines auditable.