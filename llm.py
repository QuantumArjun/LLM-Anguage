import langchain
import os
from langchain.llms import OpenAI
from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from api import *
import pyttsx3
from gtts import gTTS
import os

class LLM:
    def __init__(self, model_name, language_enum):
        # TODO: Add a "model verbosity" thing that can include an "explain your reasoning" in the prompt
        if model_name == "openai":
            os.environ["OPENAI_API_KEY"] = openai_key
            # self.model = OpenAI(model_name="gpt-3.5-turbo")
            self.model = OpenAI(model_name="text-davinci-003")

        self.language = language_enum['name']
    
    def respond(self, user_text, history=None):
        template = ""
        input_variables = []
        chain_dict = {}
        
        template += f"You are helping me learn {self.language} by simulating a conversation I will have with a employee of a particular establishment. In this case, I am ordering food from an Indian restaurant, and you are simulating a {self.language} speaking worker. You will respond to me in the language {self.language}. Here is what I say to you:{{user_text}}"
        if history is not None:
            template += ". The conversation history is structured as a list of lists, in the following format. [[my response, your response],[my response, your response], [my response, your response]]. Here is the conversation so far:{{history}}"
        template += f". Given the conversation history and my most recent response, please respond to me in the language {self.language}. Your response: "
        

        chain_dict["user_text"] = user_text
        chain_dict["history"] = str(history)
        
        input_variables.append("user_text")
        input_variables.append("history")

        prompt = PromptTemplate(
            input_variables=input_variables,
            template=template,
        )

        chain = LLMChain(llm=self.model, prompt=prompt)

        result = chain.run(chain_dict)
        return result


if __name__ == "__main__":
    llm = LLM(model_name="openai")
    result = llm.respond("Hello, I would like to order some food.")
    print(result)

    tts = gTTS(result)
    tts.save("output.mp3")

    # Play the generated speech
    os.system("afplay output.mp3")  # macOS
    

