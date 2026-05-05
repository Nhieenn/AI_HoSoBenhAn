import re
import uuid
from typing import List, Dict, Any, Optional

class Document:
    def __init__(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        self.id = str(uuid.uuid4())
        self.content = content
        self.metadata = metadata or {}

class RetrievalResult:
    def __init__(self, document: Document, score: float):
        self.document = document
        self.score = score
        self.citation = f"[{self.document.metadata.get('source', 'Unknown')}]: {self.document.content[:50]}..."

class BaseRetriever:
    """
    Interface cơ sở cho Retriever.
    Kiến trúc này giúp dễ dàng thay thế MockRetriever bằng VectorDB thật (như ChromaDB) sau này.
    """
    def add_documents(self, documents: List[Document]) -> None:
        raise NotImplementedError

    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        raise NotImplementedError


class MockRetriever(BaseRetriever):
    """
    Mô phỏng Retriever sử dụng keyword matching đơn giản, không cần model ML.
    """
    def __init__(self):
        self.documents: List[Document] = []
        
    def add_documents(self, documents: List[Document]) -> None:
        self.documents.extend(documents)
        
    def _tokenize(self, text: str) -> set:
        """Tokenize đơn giản dựa trên từ ngữ."""
        words = re.findall(r'\b\w+\b', text.lower())
        return set(words)
        
    def retrieve(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []
            
        results = []
        for doc in self.documents:
            doc_tokens = self._tokenize(doc.content)
            # Tính điểm tương đồng dựa trên sự giao nhau của từ khóa (Jaccard-like score)
            intersection = query_tokens.intersection(doc_tokens)
            score = len(intersection) / (len(query_tokens) + 0.001)  # Tránh chia cho 0
            
            if score > 0:
                results.append(RetrievalResult(doc, score))
                
        # Sắp xếp theo score giảm dần
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]


class ClinicalRAG:
    """
    Module 5: Truy hồi và Neo đầu ra (RAG)
    """
    def __init__(self, retriever: Optional[BaseRetriever] = None):
        # Cho phép Dependency Injection. Mặc định dùng MockRetriever nếu không truyền.
        self.retriever = retriever or MockRetriever()
        
    def index_document(self, content: str, source: str = "Tài liệu Y khoa", metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        UC-RAG-01: Quản lý kho tri thức y khoa.
        Lập chỉ mục tài liệu.
        """
        meta = metadata or {}
        meta["source"] = source
        doc = Document(content=content, metadata=meta)
        self.retriever.add_documents([doc])
        return doc.id
        
    def retrieve_context(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        UC-RAG-02: Truy hồi và Citation.
        Tìm kiếm ngữ cảnh liên quan và trả về cùng thông tin trích dẫn.
        """
        results = self.retriever.retrieve(query, top_k=top_k)
        
        contexts = []
        citations = []
        for res in results:
            contexts.append(res.document.content)
            citations.append({
                "id": res.document.id,
                "source": res.document.metadata.get("source"),
                "text_snippet": res.document.content[:100],
                "score": res.score
            })
            
        return {
            "query": query,
            "combined_context": "\n\n".join(contexts),
            "citations": citations
        }
