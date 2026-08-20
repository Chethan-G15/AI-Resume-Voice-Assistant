from app.services.ollama_service import understand_query


query = "What are CHETHAN G's skills?"

result = understand_query(query)

print("Ollama result:")
print(result)
