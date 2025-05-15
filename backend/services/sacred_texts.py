from typing import List, Dict, Optional
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, PDFLoader
import os

class SacredTextService:
    def __init__(self, persist_directory: str = "./data/embeddings"):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def add_sacred_text(self, text: str, source: str, metadata: Dict):
        """
        Adiciona um novo texto sagrado ao banco de dados
        """
        texts = self.text_splitter.split_text(text)
        self.vector_store.add_texts(
            texts=texts,
            metadatas=[{**metadata, "source": source} for _ in texts]
        )

    async def search_sacred_texts(self, query: str, k: int = 5) -> List[Dict]:
        """
        Busca textos sagrados relevantes para uma consulta
        """
        docs = self.vector_store.similarity_search(query, k=k)
        return [
            {
                "text": doc.page_content,
                "source": doc.metadata.get("source"),
                "metadata": doc.metadata
            }
            for doc in docs
        ]

    async def get_text_by_source(self, source: str) -> List[Dict]:
        """
        Recupera todos os textos de uma fonte específica
        """
        # Implementar filtro por fonte
        pass

    async def process_file(self, file_path: str, source: str):
        """
        Processa um arquivo de texto ou PDF
        """
        if file_path.endswith('.pdf'):
            loader = PDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        documents = loader.load()
        texts = self.text_splitter.split_documents(documents)
        
        self.vector_store.add_documents(
            documents=texts,
            metadatas=[{"source": source} for _ in texts]
        ) 