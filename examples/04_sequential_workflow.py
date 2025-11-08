import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core._agent import Agent
from core._model import Memory, get_chater_cfg, ChaterPool, ChatResponse
from core._pipeline import sequential_pipeline


async def main():
    planner = Agent(
        name="Planner",
        chater=ChaterPool([
            get_chater_cfg("siliconflow"),
            get_chater_cfg("zhipuai")
        ]),
        memory=Memory(),
        system_prompt="You create brief outlines. Output only 3 bullet points."
    )

    writer = Agent(
        name="Writer",
        chater=ChaterPool([
            get_chater_cfg("siliconflow"),
            get_chater_cfg("zhipuai")
        ]),
        memory=Memory(),
        system_prompt="You expand outlines into paragraphs. Keep it under 100 words."
    )

    reviewer = Agent(
        name="Reviewer",
        chater=ChaterPool([
            get_chater_cfg("siliconflow"),
            get_chater_cfg("zhipuai")
        ]),
        memory=Memory(),
        system_prompt="You review and improve text. Suggest 2 improvements."
    )

    print("Sequential Workflow: Article Writing\n")
    print("=" * 60)

    initial = ChatResponse(
        role="user",
        content="Topic: Benefits of morning exercise"
    )

    result = await sequential_pipeline(
        agents=[planner, writer, reviewer],
        initial_message=initial
    )

    print(f"\nFinal output:\n{result.content}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
