from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
import getpass
import os
import qdrant_client
from qdrant_client.http import models
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from langchain.vectorstores import qdrant
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
import getpass
import os
import qdrant_client
from qdrant_client.http import models
from qdrant_client import QdrantClient



load_dotenv()


qdrant_client = QdrantClient(
    url=os.getenv('Qdrant_url'),
    api_key=os.getenv("Qdrant_api_key")
)


api_key= os.environ["OpenAI_API_Key"]
embeddings = OpenAIEmbeddings(api_key=api_key)
vector_store = Qdrant(
    client=qdrant_client, collection_name="Teesney_collection", 
    embeddings=embeddings,
)


#Converting to CHUNKS
# def get_chunks(text):
#     text_splitter = CharacterTextSplitter(
#         separator = ">>>",
#         chunk_size=2100, 
#         chunk_overlap= 200,
#         length_function=len
#         )
#     chunks = text_splitter.split_text(text)
#     return chunks

# with open('story.txt','r', encoding='utf-8') as f:
#     raw_text = f.read()

# texts=get_chunks(raw_text)
# vector_store.add_texts(texts)

qa = RetrievalQA.from_chain_type( llm=OpenAI(), chain_type = "stuff",
                                 retriever= vector_store.as_retriever()
                                )

querry = "Can you please suggest me gift for a date"
response = qa.invoke(querry)
print(response['result'])