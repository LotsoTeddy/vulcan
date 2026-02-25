import os

from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import Client as SupabaseClient
from supabase import create_client

from vulcan.platform.models import (
    AddAgentRequest,
    AddAgentResponse,
    InvokeAgentRequest,
    InvokeAgentResponse,
    UseResponse,
)
from vulcan.platform.types import AGENT_TABLE_NAME
from vulcan.platform.utils import (
    generate_vulcan_agent_id,
    get_agent_card,
    send_a2a_request,
)

load_dotenv()


app = FastAPI(title="Vulcan Platform API")


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
