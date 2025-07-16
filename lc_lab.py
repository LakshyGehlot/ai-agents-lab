from config import geminiKey
from langchain.schema import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchResults
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


# Tools =========================================
def writeFile(content: tuple):
    content = eval(content)
    with open(f"./output/{content[0]}", "w") as file:
        file.write(content[1])
    return f"Content written to {content[0]}"


def readFile(filename: str):
    with open(f"./output/{filename}", "r") as file:
        return file.read()
    return f"Content read from {filename}"


def askFromUser(question: str):
    res = input(question + "\n").strip()
    return "user not responded" if res == "" else res


searchTool = DuckDuckGoSearchResults()

llm = ChatGoogleGenerativeAI(api_key=geminiKey, model="gemini-1.5-flash")

tools = [
    Tool(
        name="writeFile",
        func=writeFile,
        description="Write content to a file. Parameters, content: tuple(name_of_the_file_to_write, content_to_write)",
    ),
    Tool(
        name="readFile",
        func=readFile,
        description="Read content from a file. Parameter filename",
    ),
    Tool(
        name="DuckDuckGoSearchResults",
        func=searchTool,
        description="Search the internet using DuckDuckGo. Parameters, query",
    ),
    Tool(
        name="askFromUser",
        func=askFromUser,
        description="Ask question about the task and get a response. Parameters, question",
    ),
]

agent = initialize_agent(
    llm=llm,
    tools=tools,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=3,
)

messages = [
    SystemMessage(
        content="You are a goal-to-plan assistant. Break down high-level tasks into clear action steps. Respond in Markdown."
    ),
    HumanMessage(
        # content="test mode (dont ask question for this prompt) create a structured roadmap for learning machine learning with all the key concepts and important algroithms including topics from maths and stats don't include python fundamentals and write them in a markdown file."
        content="(test mode) use web search to find up to date syllabus and draft a study plan for JEE Mains exam 2026. Write the plan in  a markdown file. (don't ask questions for this task)"
    ),
]

response = agent.invoke(messages)
print(response)
