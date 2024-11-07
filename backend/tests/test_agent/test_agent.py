import sys

sys.path.append(".")

import unittest
from pprint import pprint

from app.agents.agent import AgentMessageModel, AgentRunner, OnStopInput
from app.agents.tools.agent_tool import RunResult
from app.agents.tools.internet_search import internet_search_tool
from app.bedrock import ConverseApiToolResult
from app.repositories.models.conversation import (
    MessageModel,
    TextContentModel,
    ToolUseContentModel,
)
from app.repositories.models.custom_bot import (
    AgentModel,
    BotModel,
    GenerationParamsModel,
    KnowledgeModel,
)
from app.routes.schemas.conversation import type_model_name


def on_thinking(agent_log: list[AgentMessageModel]):
    print("====================================")
    print("Thinking...")
    print("====================================")
    assert len(agent_log) > 0
    assert agent_log[-1].role == "assistant"
    to_send = dict()
    for c in agent_log[-1].content:
        assert type(c) == ToolUseContentModel
        to_send[c.body.tool_use_id] = {
            "name": c.body.name,
            "input": c.body.input,
        }
    pprint(to_send)


def on_tool_result(tool_result: ConverseApiToolResult):
    print("====================================")
    print("Tool Result...")
    print("====================================")
    to_send = {
        "toolUseId": tool_result["toolUseId"],
        "status": tool_result["status"],  # type: ignore
        "content": tool_result["content"]["text"][:10],  # type: ignore
    }
    pprint(to_send["toolUseId"])
    pprint(to_send["status"])


def on_stop(on_stop_input: OnStopInput):
    print("====================================")
    print("Stop...")
    print("====================================")
    pprint(on_stop_input)


class TestAgentRunner(unittest.TestCase):
    def setUp(self) -> None:
        bot = BotModel(
            id="dummy",
            title="Japanese Dishes",
            description="Japanese Delicious Dishes",
            instruction="",
            create_time=1627984879.9,
            last_used_time=1627984879.9,
            # Pinned
            is_pinned=True,
            public_bot_id=None,
            owner_user_id="dummy",
            generation_params=GenerationParamsModel(
                max_tokens=2000,
                top_k=250,
                top_p=0.999,
                temperature=0.6,
                stop_sequences=["Human: ", "Assistant: "],
            ),
            agent=AgentModel(tools=[]),
            knowledge=KnowledgeModel(
                source_urls=[""],
                sitemap_urls=[""],
                filenames=[
                    "Ramen.pdf",
                    "Sushi.pdf",
                    "Yakiniku.pdf",
                ],
                s3_urls=[],
            ),
            display_retrieved_chunks=True,
            sync_status="RUNNING",
            sync_status_reason="reason",
            sync_last_exec_id="",
            published_api_stack_name=None,
            published_api_datetime=None,
            published_api_codebuild_id=None,
            conversation_quick_starters=[],
            bedrock_knowledge_base=None,
            bedrock_guardrails=None,
        )
        tools = [internet_search_tool]
        model = "claude-v3-sonnet"
        self.runner = AgentRunner(
            bot=bot,
            tools=tools,
            model=model,
            on_thinking=on_thinking,
            on_tool_result=on_tool_result,
            on_stop=on_stop,
        )
        self.model: type_model_name = model

    def test_run(self):
        message = MessageModel(
            role="user",
            content=[
                TextContentModel(
                    content_type="text",
                    body="今日の東京の天気?あと宮崎の天気も。並列処理して",
                )
            ],
            model=self.model,
            children=[],
            parent=None,
            create_time=0,
            feedback=None,
            used_chunks=None,
            thinking_log=None,
        )
        res = self.runner.run(messages=[message])
        print("====================================")
        pprint(res)


if __name__ == "__main__":
    unittest.main()
