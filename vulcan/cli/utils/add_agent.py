import requests

from vulcan.cli.utils.get_agents import AgentAuth, get_agentkit_runtime_auth


def add_agent(
    id: str,
    vulcan_host: str,
    volcengine_access_key: str,
    volcengine_secret_key: str,
) -> str:
    """Add an AgentKit runtime agent to Vulcan platform.

    Args:
        id (str): AgentKit runtime ID of the agent to add.

    Returns:
        str: The unique ID of the added agent in Vulcan platform.
    """
    agent_auth: AgentAuth = get_agentkit_runtime_auth(
        ak=volcengine_access_key, sk=volcengine_secret_key, runtime_id=id
    )

    response = requests.post(
        f"{vulcan_host}/add/agent",
        json={"url": agent_auth.url, "api_key": agent_auth.api_key},
    )
    response.raise_for_status()

    return response.json()["id"]
