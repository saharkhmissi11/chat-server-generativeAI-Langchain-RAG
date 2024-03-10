from langchain.embeddings.openai import OpenAIEmbeddings

model_name = "text-embedding-ada-002"

def create_embedding_model():
    """
    Creates and returns an OpenAI embedding model.

    Returns:
        OpenAIEmbeddings: An OpenAI embedding model instance.
    """

    try:
        return OpenAIEmbeddings(model_name=model_name)
    except Exception as e:
        print(f"Error creating embedding model: {e}")
        raise


def generate_embedding(text: str, model):
    """
    Generates an embedding for the given text using the provided model.

    Args:
        text: The text to generate an embedding for.
        model: The OpenAI embedding model instance.

    Returns:
        list: A list representing the generated embedding.
    """

    try:
        embedding = model.embed_text(text)
        return embedding.tolist()
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise
