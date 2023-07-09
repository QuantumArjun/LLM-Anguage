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
    def __init__(self, model_name):
        # TODO: Add a "model verbosity" thing that can include an "explain your reasoning" in the prompt
        if model_name == "openai":
            os.environ["OPENAI_API_KEY"] = openai_key
            # self.model = OpenAI(model_name="gpt-3.5-turbo")
            self.model = OpenAI(model_name="text-davinci-003")
    
    def respond(self, user_text):
        
        template = ""
        input_variables = []
        chain_dict = {}
        
        template += "You are helping me learn Hindi by simulating a conversation I will have with a employee of a particular establishment. In this case, I am ordering food from an Indian restaurant, and you are simulating a Hindi speaking worker. I will input the English I am speaking, and you will respond to me with the Hindi response (using the english alphabet). First, you will provide me a few available dishes at an Indian restaurant. Here is my English phrase: {user_text}"
        
        chain_dict["user_text"] = user_text
        
        input_variables.append("user_text")

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
    

