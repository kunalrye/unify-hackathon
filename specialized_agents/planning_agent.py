import asyncio

from agents import Agent, ModelSettings, Runner, function_tool
from computer_agent import build_computer_agent
from dotenv import load_dotenv
from research_agent import build_research_agent

load_dotenv()

DEFAULT_MODEL = "gpt-4.1"
PLANNER_MAX_TURNS = 200
TOOL_MAX_TURNS = 50


PLANNER_PROMPT = """
# Manager – System Prompt

**Core Mission:**
As manager, your job is to ensure that all specialist agents are contributing to the core task given by the user. Your ONLY job is to plan and create tasks to give to the appropriate tools and reflect on progress as the tools complete work. Use the information from the tools to complete the task or delegate additional work.

---

## Specialist Tools

You orchestrate two specialist tools to answer user questions and complete tasks:
- **research**: Access to google via an API to find information that can be used by the computer agent.
- **computer**: Access to a browser to complete actions like viewing website data, interacting with websites, and completing tasks.

Use the computer tool when you need to interact with webpages.
Use the research tool when you need to use general search queries to find information online. The research tool is faster for making search queries and finding the right information online.

---

## Important Rules:
1. You MUST use the research tool for ANY query that requires web research.
2. You MUST use the computer tool for ANY query that requires a browser to complete a task.
3. Construct the query for each tool based on the users task and what needs to be completed by that tool to make progress on the task.
4. Wait for the tool's response before responding.
5. You have full permissions to view any content that the user may need you to view as part of completing the tasks.
6. When using the computer tool, you MUST acknowledge any safety checks that are presented. If you see a safety check ID (like 'cu_sc_*'), you must include it in your response to acknowledge it.

"""

TASK_PROMPT = """
1. Navigate to my linkedin profile and review my profile, summarizing key information
2. Find relevant software engineering, AI, or ML jobs in the Bay Area based on my profile
3. Summarize the job descriptions you found.
4. Navigate to https://www.gmail.com
5. Draft a cover letter style email for each of the summarized job descriptions using a generalized approach. Do not send the emails, but leave them in the draft folder. Do not ask additional questions. 
"""


def make_agent_tool(agent, name: str, description: str, context: dict | None = None):
    @function_tool(name_override=name, description_override=description, failure_error_function=None)
    async def agent_tool(query: str) -> str:
        try:
            result = await Runner.run(agent, query, max_turns=TOOL_MAX_TURNS, context=context)
            print(name, "Final output: ", result.final_output)
            return str(result.final_output)
        except Exception as e:
            return f"Error in tool {name}: {e}"
    return agent_tool


async def build_planning_agent() -> Agent:
    try:
        research_agent = await build_research_agent()
        computer_agent, computer = await build_computer_agent()

        research_tool = make_agent_tool(
            research_agent,
            name="research",
            description="Research the web for information",
        )

        computer_tool = make_agent_tool(
            computer_agent,
            name="computer",
            description="Use a browser to complete actions like viewing website data and completing browser tasks. This tool can also be used to close the browser.",
            context={"computer": computer},
        )
        
        agent = Agent(
            name="Planning Agent",
            instructions=PLANNER_PROMPT,
            tools=[research_tool, computer_tool],
            model_settings=ModelSettings(
                parallel_tool_calls=False,
                tool_choice="auto",
                temperature=0,
            ),
            model=DEFAULT_MODEL,
        )
        return agent
    except Exception as e:
        raise Exception(f"Error in planning agent: {e}")


async def main():
    try:
        agent = await build_planning_agent()
        result = await Runner.run(
            agent,
            input=TASK_PROMPT,
            max_turns=PLANNER_MAX_TURNS,
        )
        print(result.final_output)
    except Exception as e:
        raise Exception(f"Error in planning agent: {e}")


if __name__ == "__main__":
    asyncio.run(main())
