# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Anthropic API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
ANTHROPIC_API_KEY=""  # Enter your Anthropic API secret key
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv sync
```

This installs runtime dependencies and the `dev` group (pytest, pytest-asyncio).

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
pip install pytest pytest-asyncio  # optional, for running tests
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Document Retrieval

Use the @ symbol followed by a document ID to include document content in your query:

```
> Tell me about @deposition.md
```

### Commands

Use the / prefix to execute commands defined in the MCP server:

```
> /summarize deposition.md
```

Commands will auto-complete when you press Tab.

## MCP Server

The bundled `mcp_server.py` exposes the in-memory `docs` dictionary to MCP clients via:

- **Tools**
  - `read_doc_contents(doc_id)` — return the contents of a document.
  - `edit_document(doc_id, old_str, new_str)` — replace `old_str` with `new_str` in a document.
- **Resources**
  - `docs://documents` — JSON list of all document IDs.
  - `docs://documents/{doc_id}` — contents of a single document.
- **Prompts**
  - `format(doc_id)` — rewrite a document in markdown format.
  - `summarize(doc_id)` — produce a concise summary of a document.

## Development

### Adding New Documents

Edit the `mcp_server.py` file to add new documents to the `docs` dictionary.

### Testing

Tests live in `tests/` and use `pytest` with `pytest-asyncio` (auto mode).

- `tests/test_mcp_server.py` exercises the server in-process against the `FastMCP` instance.
- `tests/test_mcp_client.py` spawns the server as a subprocess and exercises `MCPClient` end-to-end.

Run the suite with:

```bash
uv run pytest
```

### Linting and Typing Check

There are no lint or type checks implemented.
