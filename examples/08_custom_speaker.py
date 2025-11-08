import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core._agent import Agent
from core._model import ChaterPool, Memory, get_chater_cfg, ChatResponse
from core._speaker import Speaker, MarkdownSpeaker, SilentSpeaker


class EmojiSpeaker(Speaker):
    def speak_stream_start(self, agent_name: str) -> None:
        print(f"{agent_name}: ", end="", flush=True)
    
    def speak_chunk(self, chunk: ChatResponse) -> None:
        if chunk.reasoning_content:
            print(f"{chunk.reasoning_content}", end="", flush=True)
        if chunk.content:
            print(chunk.content, end="", flush=True)
    
    def speak_stream_end(self) -> None:
        print(" ✨\n")
    
    def speak_complete(self, response: ChatResponse, agent_name: str) -> None:
        if response.reasoning_content:
            print(f"[Thinking: {response.reasoning_content}]")
        if response.content:
            print(f"{agent_name}: {response.content}")


class ColorSpeaker(Speaker):
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    
    def speak_stream_start(self, agent_name: str) -> None:
        print(f"{self.BLUE}{agent_name}:{self.RESET} ", end="", flush=True)
    
    def speak_chunk(self, chunk: ChatResponse) -> None:
        if chunk.reasoning_content:
            print(f"{self.YELLOW}{chunk.reasoning_content}{self.RESET}", end="", flush=True)
        if chunk.content:
            print(f"{self.GREEN}{chunk.content}{self.RESET}", end="", flush=True)
    
    def speak_stream_end(self) -> None:
        print()
    
    def speak_complete(self, response: ChatResponse, agent_name: str) -> None:
        if response.reasoning_content:
            print(f"{self.YELLOW}[Thinking: {response.reasoning_content}]{self.RESET}")
        if response.content:
            print(f"{self.GREEN}{response.content}{self.RESET}")


async def main():
    print("=== Custom Speaker Demo ===\n")
    
    print("1️⃣ Default ConsoleSpeaker\n")
    agent1 = Agent(
        name="Agent1",
        chater=ChaterPool([get_chater_cfg("siliconflow")]),
        memory=Memory(),
        system_prompt="Be helpful and brief."
    )
    
    async for response in agent1.reply("Say hello", stream=False):
        agent1.speak(response)
    print()
    
    print("\n2️⃣ EmojiSpeaker (stream mode)\n")
    agent2 = Agent(
        name="Agent2",
        chater=ChaterPool([get_chater_cfg("zhipuai")]),
        memory=Memory(),
        system_prompt="Be helpful and brief.",
        speaker=EmojiSpeaker()
    )
    
    async for response in agent2.reply("Say hi", stream=True):
        agent2.speak(response, stream=True)
    
    print("\n3️⃣ MarkdownSpeaker\n")
    agent3 = Agent(
        name="Agent3",
        chater=ChaterPool([get_chater_cfg("siliconflow")]),
        memory=Memory(),
        system_prompt="Be helpful and brief.",
        speaker=MarkdownSpeaker()
    )
    
    async for response in agent3.reply("Introduce yourself", stream=False):
        agent3.speak(response)
    
    print("\n4️⃣ ColorSpeaker (stream mode)\n")
    agent4 = Agent(
        name="Agent4",
        chater=ChaterPool([get_chater_cfg("zhipuai")]),
        memory=Memory(),
        system_prompt="Be helpful and brief.",
        speaker=ColorSpeaker()
    )
    
    async for response in agent4.reply("What can you do?", stream=True):
        agent4.speak(response, stream=True)
    
    print("\n5️⃣ SilentSpeaker (no output)\n")
    agent5 = Agent(
        name="Agent5",
        chater=ChaterPool([get_chater_cfg("siliconflow")]),
        memory=Memory(),
        system_prompt="Be helpful and brief.",
        speaker=SilentSpeaker()
    )
    
    print("Agent5 is speaking (silently)...")
    async for response in agent5.reply("Test silent mode", stream=False):
        agent5.speak(response)
    print("Done (no output as expected)\n")
    
    print("\n6️⃣ Runtime speaker change\n")
    agent1.speaker = EmojiSpeaker()
    print("Changed agent1's speaker to EmojiSpeaker:")
    async for response in agent1.reply("Say goodbye", stream=False):
        agent1.speak(response)
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
