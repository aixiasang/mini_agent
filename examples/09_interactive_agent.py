import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core._agent import Agent
from core._model import Memory, get_chater_cfg, ChaterPool
from core._tools import ToolKit
from core._utils import FileOperations, DirectoryOperations, SearchOperations
from datetime import datetime


async def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def calculate(expression: str) -> float:
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


async def ainput(prompt: str = "") -> str:
    return await asyncio.to_thread(input, prompt)


async def main():
    tools = ToolKit()
    tools.register(get_current_time, "get_current_time")
    tools.register(calculate, "calculate")
    tools.register(FileOperations.read_file, "read_file")
    tools.register(FileOperations.write_file, "write_file")
    tools.register(DirectoryOperations.list_directory, "list_directory")
    tools.register(SearchOperations.grep_in_file, "grep_in_file")

    agent = Agent(
        name="Assistant",
        chater=ChaterPool([
            get_chater_cfg("zhipuai"),
            get_chater_cfg("siliconflow"),
        ]),
        memory=Memory(max_messages=50),
        tools=tools,
        system_prompt="You are a helpful AI assistant with access to various tools.",
        max_iterations=5,
        tool_timeout=30,
        enable_logging=False
    )

    def response_formatter(self, response):
        if response.content and not response.tool_call and not response.tool_calls:
            response.content = f"💬 {response.content}"
        return response


    agent.add_post_reply_hook(response_formatter)

    print("=" * 60)
    print("Interactive Agent Demo")
    print("=" * 60)
    print(f"\nAgent: {repr(agent)}")
    print(f"Tools: {', '.join(tools._tools.keys())}")
    print(f"Memory: {'Unlimited' if agent.memory.max_messages is None else agent.memory.max_messages}")
    print(f"\nCommands:")
    print("  - 'quit' / 'exit'  : Exit")
    print("  - 'clear'          : Clear memory")
    print("  - 'memory'         : Show memory info")
    print("  - 'info'           : Show agent info")
    print("  - 'hooks'          : Show hook info")
    print("  - 'stream on/off'  : Toggle streaming")
    print("\n" + "=" * 60 + "\n")

    stream_mode = True

    while True:
        try:
            user_input = await ainput("You: ")

            if not user_input.strip():
                continue

            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break

            if user_input.lower() == "clear":
                agent.clear_memory()
                print("✓ Memory cleared\n")
                continue

            if user_input.lower() == "memory":
                print(f"\nMemory Statistics:")
                print(f"  Total: {len(agent.memory)}")
                print(f"  User: {len(agent.memory.get_by_role('user'))}")
                print(f"  Assistant: {len(agent.memory.get_by_role('assistant'))}")
                print(f"  Tool: {len(agent.memory.get_by_role('tool'))}")
                print()
                continue

            if user_input.lower() == "info":
                info = agent.to_dict()
                print(f"\nAgent Information:")
                for key, value in info.items():
                    print(f"  {key}: {value}")
                print()
                continue

            if user_input.lower() == "hooks":
                print(f"\nHook Information:")
                print(f"  Pre-reply: {len(agent._pre_reply_hooks)}")
                print(f"  Post-reply: {len(agent._post_reply_hooks)}")
                print(f"  Pre-observe: {len(agent._pre_observe_hooks)}")
                print(f"  Post-observe: {len(agent._post_observe_hooks)}")
                print()
                continue

            if user_input.lower().startswith("stream "):
                mode = user_input.lower().split()[1]
                if mode == "on":
                    stream_mode = True
                    print("✓ Streaming enabled\n")
                elif mode == "off":
                    stream_mode = False
                    print("✓ Streaming disabled\n")
                continue

            if stream_mode:
                print("Agent: ", end="", flush=True)
                async for _ in agent.reply(user_input, stream=True,auto_speak=True):
                    pass
                print("\n")
            else:
                async for _ in agent.reply(user_input, stream=False,auto_speak=True):
                    pass
                print()

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
