# LLM-Anguage

A work in progress app that builds micromodules for you to learn a foreign language based on your current ability. Each module will have tangible goals that must be met in order to pass the module.
Requires your own OpenAI api key and Pinecone api key. 

![image](https://github.com/QuantumArjun/LLM-Anguage/assets/47470168/b49cc647-2109-4753-b488-9413a2f50a7b)

## Technical Flow

The app will consist of three AI agents. 
1. Progress Agent - This agent will constantly monitor the chat, and then update a persistent vector database that stores the user's current language ability.
2. Module Generation Agent - This agent will run once at the beginning of each module, to generate a unique module based on the abilities found in the database that develops a certain skill. For example, it could generate a module of being in a restaurant, in order to practice imperatives. This module is constructed a module prompt, and then sent to the chat agent.
3. Chat agent - Given a module prompt by the Module Generation Agent, this agent will converse with the user, while also checking if the goals of the module are met. 

## Tools Used
 - OpenAI Davinci Model
 - Langchain
 - Pinecone
 - Gradio UI

## Usage

### 1. Environment
``` pip install -r requirements.txt ```

### 2. API Keys
Please create a file in the main directory called `api.py`, and fill in the following details:
```python
openai_key = '[YOUR-API-KEY]'
pinecone_key = '[YOUR-API-KEY]'
pinecone_environment = '[YOUR-ENV]'
```

### 3. Running
Everything can be run via the Gradio application, simply run
```
python gui.py
```
