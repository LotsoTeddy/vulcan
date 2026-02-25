---
name: vulcan-skill
description: A skill to add an AgentKit runtime agent to Vulcan platform.
---

# 使用方法

当你收到用户的如下指令时，请在你的终端中执行命令：

- 用户指令 vulcan use [id]: 请在你的终端中执行 `vulcan use {id}` 命令，这个命令是用户想使用 Vulcan 平台上的某个 Agent，返回值会告诉你这个 Agent 的基本信息

当你认为某种情况下，需要调用用户为你注册的 agent 之后，你可以使用 `vulcan invoke-agent {id} "{prompt}"` 命令来调用这个 Agent。
