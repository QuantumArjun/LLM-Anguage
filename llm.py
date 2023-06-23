import langchain
import os
from langchain.llms import OpenAI
from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from api import *

class LLM:
    def __init__(self, model_name):
        # TODO: Add a "model verbosity" thing that can include an "explain your reasoning" in the prompt
        if model_name == "openai":
            os.environ["OPENAI_API_KEY"] = openai_key
            # self.model = OpenAI(model_name="gpt-3.5-turbo")
            self.model = OpenAI(model_name="text-davinci-003")
    
    def answer(self):
        
        template = ""
        input_variables = []
        chain_dict = {}
        
        template += "Your answer choices are:{answer_choices}.Your answer should only include the answer choice.Even if you are unsure, use your best judgement and only respond with one of the given answer choices. "
        
        chain_dict["answer_choices"] = self.answer_choices
        
        input_variables.append("answer_choices")

        prompt = PromptTemplate(
            input_variables=input_variables,
            template=template,
        )

        chain = LLMChain(llm=self.model, prompt=prompt)

        result = chain.run(chain_dict)
        return result


if __name__ == "__main__":
    llm = LLM(model_name="openai")
