import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core._agent import Agent
from core._model import Memory, get_chater_cfg, ChaterPool


async def main():
    def global_logger(agent, message):
        print(f"[GLOBAL] {agent.name} received: {message[:40]}...")
        return message

    def global_formatter(agent, response):
        if response.content:
            response.content = f"🤖 {response.content}"
        return response

    Agent.register_class_hook("pre_reply", "logger", global_logger)
    Agent.register_class_hook("post_reply", "formatter", global_formatter)

    print("Class-level hooks affect ALL agents\n")
    print("=" * 60)

    agent1 = Agent(
        name="Agent1",
        chater=ChaterPool([
            get_chater_cfg("siliconflow"),
            get_chater_cfg("zhipuai")
        ]),
        memory=Memory(),
        system_prompt="You are helpful."
    )

    agent2 = Agent(
        name="Agent2",
        chater=ChaterPool([
            get_chater_cfg("siliconflow"),
            get_chater_cfg("zhipuai")
        ]),
        memory=Memory(),
        system_prompt="You are friendly."
    )

    for agent in [agent1, agent2]:
        print(f"\n{agent.name}:")
        async for response in agent.reply("Say hello", stream=False):
            agent.speak(response)
        print()

    Agent.clear_class_hooks()
    print("\n" + "=" * 60)
    print("Class hooks cleared")


if __name__ == "__main__":
    asyncio.run(main())
