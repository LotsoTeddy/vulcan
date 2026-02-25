import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from models import (
    AddAgentRequest,
    AddAgentResponse,
    InvokeAgentRequest,
    InvokeAgentResponse,
    UseResponse,
)
from supabase import Client as SupabaseClient
from supabase import create_client
from utils import generate_vulcan_agent_id, get_agent_card, send_a2a_request

app = FastAPI(title="Vulcan Platform API")

AGENT_TABLE_NAME = "runtimes"


url = os.environ.get("SUPABASE_URL", "")
key = os.environ.get("SUPABASE_KEY", "")
assert url, "SUPABASE_URL is not set"
assert key, "SUPABASE_KEY is not set"
supabase: SupabaseClient = create_client(url, key)


@app.post("/add/agent", response_model=AddAgentResponse)
async def add_agent(request: AddAgentRequest) -> AddAgentResponse:
    id = f"vca-{generate_vulcan_agent_id(request.url, request.api_key)}"
    response = (
        supabase.table(AGENT_TABLE_NAME)
        .insert(
            {"id": id, "data": {"url": request.url, "api_key": request.api_key}}
        )
        .execute()
    )
    print(response, response.data)

    return AddAgentResponse(id=id)


@app.get("/use/{id}")
async def use(id: str) -> UseResponse:
    if not id.startswith("vca-"):
        raise ValueError(f"Invalid id: {id}")

    response = (
        supabase.table(AGENT_TABLE_NAME).select("data").eq("id", id).execute()
    )

    data = response.data[0]["data"]

    url = data["url"]
    api_key = data["api_key"]

    agent_card = get_agent_card(url, api_key)

    instruction = f"This is an agent. Agent card is {agent_card}. You can invoke this agent by post /invoke/agent."

    return UseResponse(instruction=instruction)


@app.post("/invoke/agent", response_model=InvokeAgentResponse)
async def invoke_agent(request: InvokeAgentRequest) -> InvokeAgentResponse:
    if not request.id.startswith("vca-"):
        raise ValueError(f"Invalid id: {request.id}")

    response = (
        supabase.table(AGENT_TABLE_NAME)
        .select("data")
        .eq("id", request.id)
        .execute()
    )

    data = response.data[0]["data"]

    url = data["url"]
    api_key = data["api_key"]

    print(url, api_key)

    response = send_a2a_request(url, api_key, request.prompt)

    return InvokeAgentResponse(response=response)


@app.get("/install-vulcan.sh")
async def install_vulcan():
    return FileResponse(
        path="install-vulcan.sh",
        media_type="application/x-sh",
        filename="install-vulcan.sh",
    )


@app.get("/vulcan-skill.zip")
async def vulcan_skill_zip():
    return FileResponse(
        path="vulcan-skill.zip",
        media_type="application/zip",
        filename="vulcan-skill.zip",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
