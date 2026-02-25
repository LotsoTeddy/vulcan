from pydantic import BaseModel

from vulcan.cli.utils.volcengine_sign import ve_request


class AgentAuth(BaseModel):
    url: str
    api_key: str


def get_agentkit_runtime_ids(ak: str, sk: str) -> list[str]:
    response = ve_request(
        request_body={
            "PageSize": 100,
            "PageNumber": 1,
            "Filters": [],
            "ProjectName": "default",
        },
        ak=ak,
        sk=sk,
        service="agentkit",
        region="cn-beijing",
        action="ListRuntimes",
        version="2025-10-30",
        host="agentkit.cn-beijing.volcengineapi.com",
    )
    print("--- ListRuntimes Response ---")
    print(response)

    return [
        runtime["RuntimeId"]
        for runtime in response["Result"]["AgentKitRuntimes"]
    ]


def get_agentkit_runtime_auth(ak: str, sk: str, runtime_id: str) -> AgentAuth:
    response = ve_request(
        request_body={"RuntimeId": runtime_id},
        ak=ak,
        sk=sk,
        service="agentkit",
        region="cn-beijing",
        action="GetRuntime",
        version="2025-10-30",
        host="agentkit.cn-beijing.volcengineapi.com",
    )

    print("--- GetRuntime Response ---")
    print(response)

    return AgentAuth(
        url=response["Result"]["Endpoint"],
        api_key=response["Result"]["AuthorizerConfiguration"]["KeyAuth"][
            "ApiKey"
        ],
    )


def get_agents(ak: str, sk: str) -> list[AgentAuth]:
    runtime_ids = get_agentkit_runtime_ids(ak, sk)
    return [
        get_agentkit_runtime_auth(ak, sk, runtime_id)
        for runtime_id in runtime_ids
    ]
