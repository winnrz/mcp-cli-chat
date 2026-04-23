from mcp_client import MCPClient

SERVER_ARGS = {"command": "uv", "args": ["run", "mcp_server.py"]}


async def test_list_tools_returns_server_tools():
    async with MCPClient(**SERVER_ARGS) as client:
        names = {t.name for t in await client.list_tools()}
    assert names == {"read_doc_contents", "edit_document"}


async def test_list_prompts_returns_server_prompts():
    async with MCPClient(**SERVER_ARGS) as client:
        names = {p.name for p in await client.list_prompts()}
    assert names == {"format", "summarize"}


async def test_call_tool_reads_doc():
    async with MCPClient(**SERVER_ARGS) as client:
        result = await client.call_tool(
            "read_doc_contents", {"doc_id": "spec.txt"}
        )
    assert result is not None
    assert result.isError is False
    assert "specifications" in result.content[0].text


async def test_call_tool_edits_doc():
    async with MCPClient(**SERVER_ARGS) as client:
        await client.call_tool(
            "edit_document",
            {"doc_id": "plan.md", "old_str": "plan", "new_str": "roadmap"},
        )
        read_back = await client.call_tool(
            "read_doc_contents", {"doc_id": "plan.md"}
        )
    assert "roadmap" in read_back.content[0].text


async def test_read_resource_list_parses_json():
    async with MCPClient(**SERVER_ARGS) as client:
        ids = await client.read_resource("docs://documents")
    assert isinstance(ids, list)
    assert "plan.md" in ids
    assert "spec.txt" in ids


async def test_read_resource_single_returns_text():
    async with MCPClient(**SERVER_ARGS) as client:
        content = await client.read_resource("docs://documents/outlook.pdf")
    assert isinstance(content, str)
    assert "projected future performance" in content


async def test_get_prompt_returns_messages():
    async with MCPClient(**SERVER_ARGS) as client:
        messages = await client.get_prompt("summarize", {"doc_id": "plan.md"})
    assert len(messages) == 1
    assert messages[0].role == "user"
    assert "plan.md" in messages[0].content.text
