import json

import pytest

import mcp_server


@pytest.fixture(autouse=True)
def reset_docs():
    original = mcp_server.docs.copy()
    yield
    mcp_server.docs.clear()
    mcp_server.docs.update(original)


async def test_list_tools_exposes_read_and_edit():
    names = {t.name for t in await mcp_server.mcp.list_tools()}
    assert names == {"read_doc_contents", "edit_document"}


async def test_list_prompts_exposes_format_and_summarize():
    names = {p.name for p in await mcp_server.mcp.list_prompts()}
    assert names == {"format", "summarize"}


async def test_read_doc_contents_returns_text():
    content, _ = await mcp_server.mcp.call_tool(
        "read_doc_contents", {"doc_id": "plan.md"}
    )
    assert content[0].text == mcp_server.docs["plan.md"]


async def test_read_doc_contents_unknown_id_raises():
    with pytest.raises(Exception):
        await mcp_server.mcp.call_tool(
            "read_doc_contents", {"doc_id": "missing.md"}
        )


async def test_edit_document_replaces_substring():
    await mcp_server.mcp.call_tool(
        "edit_document",
        {"doc_id": "plan.md", "old_str": "plan", "new_str": "roadmap"},
    )
    assert "roadmap" in mcp_server.docs["plan.md"]
    assert "plan" not in mcp_server.docs["plan.md"]


async def test_edit_document_unknown_id_raises():
    with pytest.raises(Exception):
        await mcp_server.mcp.call_tool(
            "edit_document",
            {"doc_id": "missing.md", "old_str": "a", "new_str": "b"},
        )


async def test_documents_resource_lists_ids():
    result = await mcp_server.mcp.read_resource("docs://documents")
    assert result[0].mime_type == "application/json"
    assert set(json.loads(result[0].content)) == set(mcp_server.docs.keys())


async def test_document_resource_returns_content():
    result = await mcp_server.mcp.read_resource("docs://documents/spec.txt")
    assert result[0].mime_type == "text/plain"
    assert result[0].content == mcp_server.docs["spec.txt"]


async def test_format_prompt_returns_user_message_with_doc_id():
    result = await mcp_server.mcp.get_prompt("format", {"doc_id": "plan.md"})
    assert len(result.messages) == 1
    msg = result.messages[0]
    assert msg.role == "user"
    assert "plan.md" in msg.content.text


async def test_summarize_prompt_returns_user_message_with_doc_id():
    result = await mcp_server.mcp.get_prompt(
        "summarize", {"doc_id": "report.pdf"}
    )
    assert len(result.messages) == 1
    msg = result.messages[0]
    assert msg.role == "user"
    assert "report.pdf" in msg.content.text
