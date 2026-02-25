from pydantic import BaseModel


class AddAgentRequest(BaseModel):
    url: str
    api_key: str


class AddAgentResponse(BaseModel):
    id: str


class UseResponse(BaseModel):
    instruction: str


class InvokeAgentRequest(BaseModel):
    id: str
    prompt: str


class InvokeAgentResponse(BaseModel):
    response: str
