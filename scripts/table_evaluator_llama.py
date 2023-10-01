import os

import openai
from dotenv import load_dotenv
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Prompt,
    get_response_synthesizer,
    StorageContext,
    load_index_from_storage
)
from llama_index.indices.vector_store import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine

from common.prompts import PROMPT_RETRIEVE_TABLES
from config import (
    INDEX_PATH,
    OUTPUT_PATH,
    SIMILARITY_TOP_K_VALUE
)
from common.utils import mkdir_if_not_exist

from common.question import QUESTION


def load_index_from_dir(path: str):
    if len(os.listdir(path)):
        storage_context = StorageContext.from_defaults(persist_dir=path)
        return load_index_from_storage(storage_context)


def create_and_save_index(data_dir: str, index_dir: str):
    documents = SimpleDirectoryReader(data_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=index_dir)
    return index


def main(question: str):
    mkdir_if_not_exist(INDEX_PATH)
    index = load_index_from_dir(INDEX_PATH)
    if not index:
        index = create_and_save_index(OUTPUT_PATH, INDEX_PATH)

    response_synthesizer = get_response_synthesizer(
        text_qa_template=Prompt(PROMPT_RETRIEVE_TABLES),
    )
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=SIMILARITY_TOP_K_VALUE,
    )

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )

    response = query_engine.query(question)

    return str(response)


if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print(main(QUESTION))
