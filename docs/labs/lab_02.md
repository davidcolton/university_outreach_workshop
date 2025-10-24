---
title: Workshop Lab 2
description: Instruct-Validate-Repair
logo: images/ibm-blue-background.png
---

# Lab 2: Instruct-Validate-Repair

Instruct-Validate-Repair is a design pattern for building robust automation using LLMs. The idea is simple:

1. Instruct the model to perform a task and specify requirements on the output of the task.
2. Validate that these requirements are satisfied by the model's output.
3. If any requirements fail, try to repair.



## Imports

In addition to importing `mellea` from `stdlib.requirements` we import `check`, `req` and `simple_validate`. These provide syntactic sugar for writing validation functions that operate over the last output from the model (interpreted as a string).

This is useful when your validation logic only depends upon the most recent model output.

```python
# Import necessary libraries
import mellea
from mellea.stdlib.requirement import check, req, simple_validate
from mellea.stdlib.sampling import RejectionSamplingStrategy
```



## Define Requirements

Defines a list of validation requirements for generated emails: require a salutation, enforce all-lowercase text via a validation function, and forbid mentioning "purple elephants."

```python
# Add a requirements list that can be used for validation and repair exercises
requirements = [
    req("The email should have a salutation"),
    req(
        "Use only lower-case letters",
        validation_fn=simple_validate(lambda x: x.lower() == x),
    ),
    check("Do not mention purple elephants."),
]
```



## Write email function

A function to generate a short email using the provided name and notes. This function instructs the Mellea session `m` to write an email using the global `requirements` list and a rejection-sampling strategy to try multiple candidates (loop_budget=5). If validation passes, the validated result is returned. If validation fails after sampling, the first sampled generation is returned as a fallback.

The function takes 3 arguments

* `m`: An active MelleaSession used to run the instruction.
* `name`: Recipient name to be interpolated into the prompt.
* `notes`: Notes to include in the body of the email.

Returns:

* A string containing the generated email text.

```python
def write_email(m: mellea.MelleaSession, name: str, notes: str) -> str:

    # Ask the model to write an email, passing validation requirements and
    # a sampling strategy that will retry up to 5 times if candidates fail.
    email_candidate = m.instruct(
        "Write an email to {{name}} using the notes following: {{notes}}.",
        requirements=requirements,
        strategy=RejectionSamplingStrategy(loop_budget=5),
        user_variables={"name": name, "notes": notes},
        return_sampling_results=True,
    )

    # If the instruction succeeded and a validated result is available,
    # return the validated result (preferred).
    if email_candidate.success:
        return str(email_candidate.result)

    # Otherwise, fall back to the first sampled generation (best-effort).
    # This ensures the function always returns some text even if validation failed.
    return email_candidate.sample_generations[0].value
```



## Sample usage

```python
# Create a Mellea model using the granite model and the ollama inference engine
m = mellea.start_session()

# Generate an email using the write_email function
email = write_email(
    m,
    "Olivia",
    """Olivia helped the lab over the last few weeks by organizing intern events, 
       advertising the speaker series, and handling issues with snack delivery.""",
)

# Display the generated email
display(Markdown(email))
```



## Summary

Most of this should look familiar by now, but the `validation_fn` and `check` should be new.

We created 3 requirements:

- First requirement, the salutation, will be validated by LLM-as-a-judge on the output of the instruction. This is the default behavior.
- Second requirement, lower case, uses a function that takes the output of a sampling step and returns a boolean value indicating successful or unsuccessful validation. While the validation_fn parameter requires to run validation on the full session context, Mellea provides a wrapper for simpler validation functions (simple_validate(fn: Callable[[str], bool])) that take the output string and return a boolean as seen in this case.
- Third requirement is a `check()`. Checks are only used for validation, not for generation. Checks aim to avoid the "do not think about B" effect that often prime models (and humans) to do the opposite and "think" about B.

We also saw in the `m = mellea.start_session()` how you can specify a different Ollama model, in case you want to try something other than Mellea's `ibm/granite4:micro` default.