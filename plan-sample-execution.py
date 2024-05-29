
import autogen
import os

research_task = """What are daily stock prices of NVDA and TESLA in the past month. Save the results in a .md file named 'stock_prices.md'."""
planner_task = """Come up with a plan to find daily stock prices for MSFT in the last one month?."""

def my_financial_task(sender, recipient, context):
    carryover = context.get("carryover", "")
    if isinstance(carryover, list):
        carryover = carryover[-1]
    # try:
    #     filename = context.get("work_dir", "") + "/stock_prices.md"
    #     with open(filename, "r") as file:
    #         data = file.read()
    # except Exception as e:
    #     data = f"An error occurred while reading the file: {e}"

    return (
        research_task
        + "\nContext:\n"
        + carryover
        
    )


def my_writing_task(sender, recipient, context):
    carryover = context.get("carryover", "")
    if isinstance(carryover, list):
        carryover = carryover[-2]


    return (
        """Develop an engaging blog post using any information provided. """
        + "\nContext:\n"
        + carryover
        
        
    )

planner = autogen.AssistantAgent(
    name="planner",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    # the default system message of the AssistantAgent is overwritten here
    system_message="You are a helpful AI assistant. You suggest coding and writing steps for other AI assistants to accomplish a task. Suggest exactly two tasks, one for coding and other for writing. Do not suggest concrete code. For any action beyond writing code or reasoning, convert it to a step that can be implemented by writing code. For example, browsing the web can be implemented by writing code that reads and prints the content of a web page. Finally, inspect the execution result. If the plan is not good, suggest a better plan. If the execution is wrong, analyze the error and suggest a fix. The example output could look like, Here's the plan: 1. Find out the stock prices for MSFT in the last one month. 2. Write report based of that.",
)

researcher = autogen.AssistantAgent(
    name="Financial_researcher",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
)
writer = autogen.AssistantAgent(
    name="Writer",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    system_message="""
        You are a professional writer, known for
        your insightful and engaging articles.
        You transform complex concepts into compelling narratives.
        Reply "TERMINATE" in the end when everything is done.
        """,
)

user_proxy_auto = autogen.UserProxyAgent(
    name="User_Proxy_Auto",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
)

chat_results = autogen.initiate_chats(
    [
         {
            "sender": user_proxy_auto,
            "recipient": planner,
            "message": planner_task,
            "clear_history": True,
            "silent": False,
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "sender": user_proxy_auto,
            "recipient": researcher,
            "message": my_financial_task,
            "clear_history": True,
            "silent": False,
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "sender": user_proxy_auto,
            "recipient": writer,
            "message": my_writing_task,
            "max_turns": 2,  # max number of turns for the conversation (added for demo purposes, generally not necessarily needed)
            "summary_method": "reflection_with_llm",
            "work_dir": "tasks",
        },
    ]
)