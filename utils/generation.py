from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEndpoint

from dotenv import load_dotenv
import os

load_dotenv()

huggingface_token = os.environ['HuggingFace_token']



template = """ Answer the question of user by using provided question, context and Thought, action, and observation process as mention below:

            Example:
                Thought: I need to answer the user's query about the impact of climate change on agriculture. First, I should clarify what specific aspects of agriculture they are interested in, such as crop yields, livestock health, or farming practices.

                Action: I will retrieve relevant information from my internal knowledge base regarding climate change effects on crop yields. Additionally, I will search for recent studies or data that provide insights into these effects.

                Observation: After retrieving the information, I found that climate change has led to altered rainfall patterns and increased temperatures, which can significantly affect crop yields across various regions. 

                Final Response: Based on the retrieved information and my internal knowledge, climate change is impacting agriculture by causing shifts in growing seasons and increasing the likelihood of extreme weather events.
                                    For instance, some regions may experience reduced yields due to droughts, while others might see changes in crop viability due to warmer temperatures.

            context: {context}
            Question: {question}
"""


def model():
    model_kwargs={
            "max_new_tokens": 512,
            "top_k": 2,
            "temperature": 0.1,
            "repetition_penalty": 1.03,
        }
    llm = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        task="text-generation",
        input_type=model_kwargs,
        huggingfacehub_api_token= huggingface_token,
    )
    return llm


def Naive_retriever(llm, retriever, query, template = template):
    

    prompt = ChatPromptTemplate.from_template(template)

    

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain.invoke(query)


