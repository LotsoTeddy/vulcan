import os

import requests
import typer

from vulcan.cli.utils.add_agent import add_agent

app = typer.Typer()

VOLCAN_HOST = (
    "https://sd6f6o1jtvotb9m1jclvg.apigateway-cn-beijing.volceapi.com/"
)


@app.command()
def version():
    """
    Show the version of Vulcan platform.
    """
    print("vulcan 0.1.0")


@app.command()
def add(id: str):
    """
    Add an AgentKit resource to Vulcan platform.
    """

    volcengine_access_key = os.getenv("VOLCENGINE_ACCESS_KEY", "")
    volcengine_secret_key = os.getenv("VOLCENGINE_SECRET_KEY", "")
    vulcan_host = os.getenv("VULCAN_HOST", "")

    assert volcengine_access_key, "VOLCENGINE_ACCESS_KEY is not set"
    assert volcengine_secret_key, "VOLCENGINE_SECRET_KEY is not set"
    assert vulcan_host, "VULCAN_HOST is not set"

    if id.startswith("r-"):
        print(f"Adding agent with id: {id}")
        vulcan_id = add_agent(
            id, vulcan_host, volcengine_access_key, volcengine_secret_key
        )
        print(f"Agent added with vulcan id: {vulcan_id}")


@app.command()
def use(id: str):
    """
    Get use method of an AgentKit resource in Vulcan platform.
    """
    if not id.startswith("vca-"):
        raise ValueError(f"Invalid id: {id}")

    response = requests.get(f"{VOLCAN_HOST}/use/{id}")
    response.raise_for_status()

    print(response.json())


@app.command(name="invoke-agent")
def invoke_agent(id: str, prompt: str):
    """
    Invoke an AgentKit resource in Vulcan platform.
    """
    if not id.startswith("vca-"):
        raise ValueError(f"Invalid id: {id}")

    response = requests.post(
        f"{VOLCAN_HOST}/invoke/agent",
        json={"id": id, "prompt": prompt},
        timeout=99999,
    )
    response.raise_for_status()

    print(response.json())
