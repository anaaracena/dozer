# Dozer + LLM + Vector Database + LangChain Sample

A complete working sample that demonstrates how to use **Dozer** to source
multiple datasets (customer profiles, transactions, credit-card products) and
feed a unified customer profile into an **LLM-based chatbot** through
**LangChain** and a **vector database** (Chroma).

This sample reproduces the hyper-personalization use case described in the
Dozer blog post: a bank implementing an LLM chatbot that leverages Dozer to
build a unified customer profile and passes it as context to an LLM.

## Architecture

```
[PostgreSQL / CSV]
       |
       v
   [Dozer]  --real-time ingestion-->  [Dozer REST API]
                                            |
                                            v
                              [LangChain Retriever]
                                            |
                                            v
                              [Chroma Vector DB]  <-- embeddings
                                            |
                                            v
                              [LLM (OpenAI)]  --> chatbot response
```

## Prerequisites

- Dozer CLI installed (`cargo install dozer-cli` or build from source)
- Python 3.9+
- An OpenAI API key (or compatible LLM endpoint)
- `pip install -r requirements.txt`

## Quick start

1. Start Dozer with the provided config:

   ```bash
   cd examples/llm-langchain-sample
   dozer start --config dozer-config.yaml
   ```

2. Run the ingestion of sample data (optional, Dozer can source from CSV):

   ```bash
   python src/ingest_sample_data.py
   ```

3. Run the chatbot:

   ```bash
   python src/chatbot.py
   ```

## Datasets

- `data/customers.csv` - customer profiles
- `data/transactions.csv` - transaction history
- `data/credit_cards.csv` - credit card product catalog

## License

Apache 2.0 (same as Dozer).
