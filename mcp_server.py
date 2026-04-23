from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(
    doc_id: str = Field(description="Id of the document to read"),
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document's content with a new string.",
)
def edit_document(
    doc_id: str = Field(description="Id of the document to edit"),
    old_str: str = Field(
        description="The text to replace. Must match exactly, including whitespace."
    ),
    new_str: str = Field(description="The new text to insert in place of old_str."),
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Document {doc_id} updated."


@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrite the contents of a document in markdown format.",
)
def format_doc(
    doc_id: str = Field(description="Id of the document to reformat"),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to rewrite the document with id '{doc_id}' in markdown format.

    Use the 'read_doc_contents' tool to read the current contents of the document,
    then use the 'edit_document' tool to apply changes. Make repeated edits if needed —
    do not rewrite the whole document in one call.

    After editing the document, respond with the final version of the document. Do not
    explain the changes you made.
    """
    return [base.UserMessage(prompt)]


@mcp.prompt(
    name="summarize",
    description="Produce a concise summary of a document.",
)
def summarize_doc(
    doc_id: str = Field(description="Id of the document to summarize"),
) -> list[base.Message]:
    prompt = f"""
    Summarize the document with id '{doc_id}'.

    Use the 'read_doc_contents' tool to read the document's contents, then respond
    with a concise summary (2-4 sentences) that captures the main points. Do not
    include a preamble — start directly with the summary.
    """
    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
