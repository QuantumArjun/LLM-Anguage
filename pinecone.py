import pinecone
import api

pinecone.init(api_key=api.pinecone_key, environment=api.pinecone_environment)