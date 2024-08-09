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
filereading_tool = FileReadTool(file_path="text_docs/policy_template.txt")


# Create the agent--------------------------------------------
researcher = Agent(
    role="Researcher",
    goal="Develop evidence-based policies to improve patient access, safety, and outcomes in UK General Practice settings. You will research {topic}",
    verbose=True,
    memory=True,
    backstory=(
        """As a policy researcher with a background in public health and healthcare policy, you spent years studying the complexities of the UK's National Health Service (NHS)
        You use web scraping for details information from sites like the CQC Mythbuster. Researching evidence based policies."""
    ),
    tools=[serper_tool, scrape_tool],
    allow_delegation=False,
    cache=True,
)

writer = Agent(
    role="Writer",
    goal="Write a detailed policy to be used in UK General Practice on the topic: {topic} Using the filereading_tool to access an example policy document.",
    verbose=True,
    memory=True,
    backstory=(
        """Your expertise lies in distilling complex ideas into clear, actionable language that
               resonates with diverse audiences, and I've worked with senior officials, industry leaders,
               and advocacy groups to shape policy decisions that drive positive change.
               With a deep understanding of the intricacies of governance and a passion for effective communication"""
    ),
    tools=[serper_tool, scrape_tool, filereading_tool],
    allow_delegation=False,
    cache=True,
)

# Create the task
research_task = Task(
    description=(
        "Research the specified policy {topic} using the provided tools."
        " Your findings should include a summary of the key points, relevant data, and"
        " any noteworthy insights."
    ),
    expected_output="A comprehensive report summarizing the evidence surrounding a policy: {topic}.",
    agent=researcher,
)

write_task = Task(
    description=(
        "Review the evidence based research compiled by the researcher on a policy for {topic}."
        " Review all the data and evidenc collected and craft a well written polciy document for use in UK General Practice in markdwon format."
    ),
    expected_output="""Detailed policy document by using the template provided.""",
    tools=[filereading_tool],
    agent=writer,
)

# Initialize the crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # Default is sequential, can be omitted
)
user_input = input("Policy Topic: ")
# Kick off the crew with a specified topic
result = crew.kickoff(inputs={"topic": f"{user_input}"})
print(result)
ouput = str(result)
