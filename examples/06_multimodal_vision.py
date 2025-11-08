import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core._agent import Agent
from core._model import Memory, get_chater_cfg, ChaterPool, ChatResponse, ImageBlock, MultimodalContent
from core._utils import image_to_base64


async def main():
    agent = Agent(
        name="VisionAgent",
        chater=ChaterPool([
            get_chater_cfg("siliconflow"),
            get_chater_cfg("zhipuai")
        ]),
        memory=Memory(),
        system_prompt="You are a vision AI that describes images in detail."
    )

    image_path = "../data/ikun1.png"
    
    content = MultimodalContent()
    content.add_text("What do you see in this image?")
    content.add_image(url=f"file://{image_path}")

    user_msg = ChatResponse(
        role="user",
        content=content
    )

    agent.observe(user_msg)

    print("Vision Analysis Demo\n")
    print("=" * 60)
    print(f"Image: {image_path}\n")

    async for response in agent.reply("", stream=False):
        agent.speak(response)
    print()

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
