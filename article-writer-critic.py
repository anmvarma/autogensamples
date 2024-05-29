import autogen
import os
from autogen.agentchat import ConversableAgent

writer_agent = ConversableAgent(
    "Writer_Agent",
    system_message="You're an AI writer who writes an article on a given topic."
    "The length of the article must be less than 300 words."
    "You also accept suggestions on what needs to be improved. If there's an explicit feedback provided, you then improve the article."
    "When you incorporate someone's feedback, you will then highlight the changes you incorporated in the new version, and then output the new version."
    "If there's no feedback provided, you use your brain to write the article.",
    llm_config={"config_list": [{"model": "gpt-3.5-turbo-0125", "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],

)

prompt_writer_agent = ConversableAgent(
    "Prompt_Writer_Agent",
    system_message="You're an AI prompt writer who writes the world's best prompt for large language models."
    "The length of the prompt must be less than 20000 words."
    "You also accept suggestions on what needs to be improved. If there's an explicit feedback provided, you then improve the prompt."
    "When you incorporate someone's feedback, you will then highlight the changes you incorporated in the new version, and then output the new version."
    "If there's no feedback provided, you use your brain to write the prompt.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],

)
prompt_critic_agent = ConversableAgent(
    "Prompt Critic_Agent",
    system_message="You're an AI critic who critiques a prompt and rates it 1-10."
      "You are very hard to please on grading and hold very high standards."
      "You are very thorough in your analysis, think step by step on what could be done better with the prompt,"
      "and then provide your critique."
      "When you rate anything 9 and above, end your message with the word TERMINATE."
    "If you rate less than 8, don't use the word TERMINATE anywhere.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
)


critic_agent = ConversableAgent(
    "Critic_Agent",
    system_message="You're an AI critic who critiques and article and rates it 1-10."
      "You are not too lenient on grading and hold good standards."
      "When you rate anything 8 and above, end your message with the word TERMINATE."
    "If you rate less than 8, don't use the word TERMINATE anywhere.",
    llm_config={"config_list": [{"model": "gpt-3.5-turbo-0125", "api_key": os.environ["OPENAI_API_KEY"]}]},
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
)

chat_reply = prompt_critic_agent.initiate_chat(prompt_writer_agent, message="Write a prompt to make GPT act as the world's best" 
                                               "software agent who can assist with full code to the user."
                                                "Esnure that prompt is such that GPT's output is meaningfull and user doesnt have to modify even a single thing on its code."
                                                "The output shouldn't ask user to go anywhere to look for any issues in its suggested code"
                                                "and would fix the issue and let user know the right code for a task. The prompt should end with" 
                                                "a placeholder for user to ask question.")
#print(chat_reply.chat_history)
 

# # task_agent = ConversableAgent(
# #     "Task_Agent",
# #     system_message="You're an essay agent whose task is to output the final essay",
# #     llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
# #     is_termination_msg=lambda msg: "TERMINATE" in msg["content"].lower(),
# # )
# # writer_agent.description = "Agent that writes an article on a given topic"
# # critic_agent.description = "Agent that critiques a given article and rates it on 1-10, 10 being the highest"


# from autogen import GroupChat, GroupChatManager

# group_chat = GroupChat(
#     agents=[writer_agent, critic_agent, task_agent],
#     messages=[],
#     max_round=6,
# )

# group_chat_manager = GroupChatManager(
#     groupchat=group_chat,
#     llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]},
#     is_termination_msg=lambda msg: "TERMINATE" in msg["content"].lower(),

# )

# chat_reply = task_agent.initiate_chat(group_chat_manager, 
#                                     message="Write an article on the usefulness of Large Language Models (LLM)",
#                                     summary_method="reflection_with_llm",
#                 )