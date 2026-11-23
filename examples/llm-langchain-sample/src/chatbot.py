"""Hyper-personalized chatbot using Dozer + LangChain + Chroma + OpenAI."""

import os
from dotenv import load_dotenv

from dozer_client import DozerClient
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

DOZER_URL = os.getenv("DOZER_URL", "http://localhost:8080")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def build_context(customer_id: int):
    client = DozerClient(DOZER_URL)
    profile = client.get_customer_profile(customer_id)
    transactions = client.get_transactions(customer_id)
    cards = client.get_credit_cards()

    docs = []
    if profile:
        docs.append(Document(
            page_content=f"Customer profile: {profile}",
            metadata={"source": "dozer", "type": "profile"},
        ))
    for t in transactions:
        docs.append(Document(
            page_content=f"Transaction: {t}",
            metadata={"source": "dozer", "type": "transaction"},
        ))
    for c in cards:
        docs.append(Document(
            page_content=f"Credit card product: {c}",
            metadata={"source": "dozer", "type": "credit_card"},
        ))
    return docs, profile


def main():
    customer_id = int(os.getenv("CUSTOMER_ID", "1"))
    docs, profile = build_context(customer_id)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = Chroma.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.3)

    prompt = ChatPromptTemplate.from_template(
        "You are a helpful bank assistant. Use the following context about the "
        "customer and available credit card products to answer the question.\n\n"
        "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

    chain = (
        {"context": retriever, "question": lambda x: x}
        | prompt
        | llm
        | StrOutputParser()
    )

    question = "Which credit card product best fits this customer and why?"
    print("Customer:", profile.get("name") if profile else "unknown")
    print("Answer:", chain.invoke(question))


if __name__ == "__main__":
    main()
