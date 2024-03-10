import os
from dotenv import load_dotenv
import redis
from langchain.vectorstores.redis import Redis
from langchain_core.callbacks import CallbackManager

from langchainIntegration.DocumentLoaders import load_document
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import (
    ConversationalRetrievalChain,
    LLMChain
)
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.prompts.prompt import PromptTemplate


chat = ChatOpenAI()
load_dotenv()
url = os.getenv("REDIS_URL")
host = os.getenv("REDIS_HOST")
password = os.getenv("REDIS_PASSWORD")
port = os.getenv("REDIS_PORT")
embeddings = OpenAIEmbeddings()

r = redis.Redis(
    host=host,
    port=port,
    password=password)


def load(document_url):
    docs = load_document(document_url)
    vstore = Redis.from_documents(docs, embeddings, redis_url=url, index_name='chatserver')
    r.execute_command('FT._LIST')
    vstore.write_schema("redis_schema.yaml")
    return vstore, r


def similarity_search(query: str):
    vstore = Redis.from_existing_index(embeddings, index_name="chatserver", schema="redis_schema.yaml")
    results = vstore.similarity_search(query, k=1)
    return results


'''def retrieve():
    vstore = Redis.from_existing_index(embeddings, index_name="chatserver", schema="redis_schema.yaml")
    retriever = MultiQueryRetriever.from_llm(
        retriever=vstore.as_retriever(), llm=chat
    )
    question = "what is this dataset?"
    llm = ChatOpenAI()
    response = llm.(question, retriever=retriever)
    return response'''

def retrieve(question):
  vstore = Redis.from_existing_index(embeddings, index_name="chatserver", schema="redis_schema.yaml")
  template = """Given the following chat history and a follow up question, rephrase the follow up input question to be a standalone question.
  Or end the conversation if it seems like it's done.
  Chat History:\"""
  {chat_history}
  \"""
  Follow Up Input: \"""
  {question}
  \"""
  Standalone question:"""

  condense_question_prompt = PromptTemplate.from_template(template)

  template = """{question}

  It's ok if you don't know the answer.
  Context:\"""

  {context}
  \"""
  Question:\"""
  {question}
  \"""

  Helpful Answer:"""

  qa_prompt = PromptTemplate.from_template(template)
  llm = OpenAI(temperature=0)

  streaming_llm = OpenAI(
    streaming=True,
    callback_manager=CallbackManager([
      StreamingStdOutCallbackHandler()
    ]),
    verbose=True,
    max_tokens=150,
    temperature=0.2
  )

  # use the LLM Chain to create a question creation chain
  question_generator = LLMChain(
    llm=llm,
    prompt=condense_question_prompt
  )

  # use the streaming LLM to create a question answering chain
  doc_chain = load_qa_chain(
    llm=streaming_llm,
    chain_type="stuff",
    prompt=qa_prompt
  )
  chatbot = ConversationalRetrievalChain(
    retriever=vstore.as_retriever(),
    combine_docs_chain=doc_chain,
    question_generator=question_generator
  )
  # create a chat history buffer
  chat_history = []
  # gather user input for the first question to kick off the bot
  result = chatbot(
      {"question": question, "chat_history": chat_history}
  )

  return result





















