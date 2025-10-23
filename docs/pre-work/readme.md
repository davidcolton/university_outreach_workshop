---
title: Workshop Pre-work
description: Preparation for the Workshop
logo: images/ibm-blue-background.png
---


# Pre-work

The labs in this workshop are [Jupyter notebooks](https://jupyter.org/). Check out [Running the Granite Notebooks](#running-the-granite-notebooks) section on how to setup the way you want to run the notebooks.

- [Pre-work](#pre-work)
  - [Running the Granite Notebooks Locally](#running-the-granite-notebooks-locally)
  - [Local Prerequisites](#local-prerequisites)
    - [Git](#git)
    - [Uv](#uv)
  - [Clone the Granite Workshop Repository](#clone-the-granite-workshop-repository)
    - [Sync the Python Virtual Environment](#sync-the-python-virtual-environment)
    - [Serving the Granite AI Models](#serving-the-granite-ai-models)
      - [Replicate AI Cloud Platform](#replicate-ai-cloud-platform)
      - [Running Ollama Locally](#running-ollama-locally)
  - [Running the Granite Notebooks Remotely (Colab)](#running-the-granite-notebooks-remotely-colab)
    - [Colab Prerequisites](#colab-prerequisites)
    - [Serving the Granite AI Models for Colab](#serving-the-granite-ai-models-for-colab)
      - [Replicate AI Cloud Platform for Colab](#replicate-ai-cloud-platform-for-colab)


## Running the Granite Notebooks

It is recommended if you want to run the lab notebooks locally on your computer that you have:

- A computer or laptop
- Knowledge of [Git](https://git-scm.com/) and [Python](https://www.python.org/)

Running the lab notebooks locally on your computer requires the following steps:

## Local Prerequisites

- Git
- Uv

### Git

Git can be installed on most common operating systems like Windows,  Mac, and Linux. In fact, Git comes installed by default on most Mac and  Linux machines!

For comprehensive instructions on how to install `git` on your laptop please refer to the [Install Git](https://github.com/git-guides/install-git) page.

To confirm the you have `git` installed correctly you can open a terminal window and type `git version`. You should receive a response like the one shown below.

```shell
git version
git version 2.39.5 (Apple Git-154)
```

### Uv

`uv` is an extremely fast Python package and project manager, written in Rust.

For detailed instructions on how to install `uv` on your laptop please refer to the [Installing uv](https://docs.astral.sh/uv/getting-started/installation/#installing-uv) page where instructions for Mac, Windows and Linux machines can be found.

To confirm the you have `uv` installed correctly you can open a terminal window and type `uv --version`. You should receive a response like the one shown below.

```shell
uv --version
uv 0.6.12 (e4e03833f 2025-04-02)
```

## Clone the Granite Workshop Repository

Clone the workshop repository and cd into the repository directory.

```shell
git clone https://github.com/davidcolton/university_outreach_workshop
cd university_outreach_workshop
```

### Sync the Python Virtual Environment

The workshop repository uses a `pyproject.toml` file to define the version of Python to use and the required libraries to load. To sync your repository and setup Python and download the library dependancies run `uv sync` in a terminal. After syncing you have to activate your virtual environment.

**Note:**

If running on Windows it is suggested that you use the Windows Powershell running as administrator or, if you have it installed, the Windows Subsystem for Linux.

```shell
uv sync

# Mac & Linux
source .venv/bin/activate

# Windows Powershell
.venv\Scripts\activate
```

#### Running Ollama Locally

If you want to run the AI models locally on your computer, you can use [Ollama](https://ollama.com/download).

!!! note "Tested system"
    This was tested on a Macbook with an M1 processor and 32GB RAM. It maybe possible to serve models with a CPU and less memory.

Running Ollama locally on your computer requires the following steps:

1. [Download and install Ollama](https://github.com/ollama/ollama?tab=readme-ov-file#ollama), if you haven't already.

    On macOS, you can use Homebrew to install it with:

    ```shell
    brew install ollama
    ```

1. Start the Ollama server. You will leave this running during the workshop.

    ```shell
    ollama serve
    ```

1. In another terminal window, pull down the Granite models you will want to use in the workshop. Larger models take more memory to run but can give better results.

    ```shell
    ollama pull granite4:micro
    ```

## Running the Notebooks Remotely (Colab)

If you are having difficulties getting your environment setup, or the workshop examples are not running successfully you can always run the [Get Started with CoLab](https://github.com/generative-computing/mellea?tab=readme-ov-file#get-started-with-colab) examples from the Mellea repository. Some of the content and examples may be different but you can still see the concepts shown here at work.



!!! note "Notebook execution speed tip"
    The default execution runtime in Colab uses a CPU. Consider using a different Colab runtime to increase execution speed, especially in situations where you may have other constraints such as a slow network connection. From the navigation bar, select `Runtime -> Change runtime type`, then select either GPU- or TPU-based hardware acceleration.



### Colab Prerequisites

- [Google Colab](https://colab.research.google.com) requires a Google account that you're logged into
