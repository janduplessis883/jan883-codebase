import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool,
    DirectoryReadTool,
    FileReadTool,
)

import openai

from datetime import datetime

current_date = datetime.now()


from llm_agents.select_model import *

# Initialize tools
serper_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()


# Create the agent--------------------------------------------
researcher = Agent(
    role="Researcher",
    goal="Conduct research by searching the internet for topic: {topic}. Used the scrape_tool to scape relevant web artiles you find to collaborate your findings. Always scrape at least 2 sites.",
    verbose=True,
    memory=True,
    backstory=(
        """You are expert in conducting internet research. You have a knack for finding the most appropriate information online and
        scrape the content to write a short synopsys of the most relevant links, you the present this information to the writer agent
        to conclude the write-up"""
    ),
    tools=[serper_tool, scrape_tool],
    allow_delegation=True,
    cache=True,
    allow_code_execution=True,
)

writer = Agent(
    role="Writer",
    goal="Write a comprehensive piece on {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a senior writer with years of experienc and is able to tell a story, enging your audience"
        " Your mission is to take information gathered by the researcher and distill it into a well thought out piece of written text."
        " write a detailed report of the subject matter including references to source of information."
    ),
    tools=[serper_tool, scrape_tool],
    allow_delegation=True,
    cache=True,
    allow_code_execution=True,
)

# Create the task
research_task = Task(
    description=(
        "Research the specified topic using the provided tools."
        " Your findings should include a summary of the key points, relevant data, and"
        " any noteworthy insights."
    ),
    expected_output="A comprehensive report summarizing the research on {topic}. Write a blog article fomratted in markdown.",
    # tools=[serper_tool, scrape_tool],
    agent=researcher,
)

write_task = Task(
    description=(
        "Review the information gathered by the researcher."
        " Review all the data and evidenc collected and craft a well written report, of 8 paragraphs, in markdown format."
    ),
    expected_output="""# {topic}
    write 5 paragraphs citing the source of information
    .""",
    # tools=[serper_tool, scrape_tool],
    agent=writer,
)

# Initialize the crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Default is sequential, can be omitted
)
user_input = input("Ask a question: ")
# Kick off the crew with a specified topic
result = crew.kickoff(inputs={"topic": f"{user_input}"})
print(result)
ouput = str(result)
