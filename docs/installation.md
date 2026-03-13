# Installation

LoraCamp is a Python-based tool, but we recommend using **uv** to manage your environment. `uv` will automatically handle Python installation and dependency management for you.

## Prerequisites

1.  **uv**: Install `uv` using the official installer:

    ```bash
    # macOS / Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # On Windows
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

    Or, from PyPI:

    ```bash
    # With pip
    pip install uv
    ```
    For more installation options, see the [uv documentation](https://github.com/astral-sh/uv).

## Setup

Follow these steps to set up LoraCamp:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/scruffynerf/loracamp.git
    cd loracamp
    ```

2.  **Set Up Environment (Recommended)**:
    `uv` will automatically find or install the correct Python version (3.12+) and set up a virtual environment.

    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install -e .
    ```

    *Note: If you prefer standard tools, you can still use `python -m venv venv && pip install -r requirements.txt`, provided you have Python 3.10+ manually installed.*

## Verification

Run the help command to ensure everything is installed correctly:

```bash
uv run loracamp --help
```

You are now ready to [prepare your catalog](getting-started.md)!
