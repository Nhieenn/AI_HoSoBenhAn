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


class BaseReranker:
    """
    Interface cơ sở cho Reranker (VD: Cross-Encoder).
    """
    def rerank(self, query: str, results: List[RetrievalResult]) -> List[RetrievalResult]:
        raise NotImplementedError

class MockReranker(BaseReranker):
    """
    Mô phỏng Reranker: Tăng điểm nếu document chứa cụm từ chính xác (exact phrase).
    """
    def rerank(self, query: str, results: List[RetrievalResult]) -> List[RetrievalResult]:
        query_lower = query.lower()
        for res in results:
            if query_lower in res.document.content.lower():
                res.score += 2.0  # Tăng điểm mạnh nếu khớp cả cụm
            
        results.sort(key=lambda x: x.score, reverse=True)
        return results
class ClinicalRAG:
    """
    Module 5: Truy hồi và Neo đầu ra (Modular RAG)
    """
    def __init__(self, retriever: Optional[BaseRetriever] = None, reranker: Optional[BaseReranker] = None):
        # Cho phép Dependency Injection. Mặc định dùng MockRetriever nếu không truyền.
        self.retriever = retriever or MockRetriever()
        self.reranker = reranker or MockReranker()
        
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
        UC-RAG-02: Truy hồi, Rerank và Citation.
        """
        # Retrieval Stage (lấy nhiều hơn để rerank)
        results = self.retriever.retrieve(query, top_k=top_k * 2)
        
        # Rerank Stage
        results = self.reranker.rerank(query, results)
        results = results[:top_k]
        
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

    def check_faithfulness(self, generated_text: str, context: str) -> Dict[str, Any]:
        """
        UC-RAG-03: Kiểm tra độ trung thực (Faithfulness Check).
        """
        unsupported_claims = []
        
        # Rule đơn giản: Trích xuất các thực thể In Hoa (VD: Paracetamol) hoặc 
        # số đi kèm đơn vị (VD: 39 độ, 500mg) từ generated_text. Dùng \w để hỗ trợ tiếng Việt.
        entities = re.findall(r'\b[A-ZĐ][\w]+\b|\b\d+(?:\.\d+)?\s*\w+\b', generated_text)
        
        context_lower = context.lower()
        for entity in entities:
            # Bỏ qua các từ thông thường như "HÀNH CHÍNH" (uppercase all) do regex trên chỉ bắt Title Case
            if entity.lower() not in context_lower:
                unsupported_claims.append(entity)
                
        is_faithful = len(unsupported_claims) == 0
        return {
            "is_faithful": is_faithful,
            "unsupported_claims": list(set(unsupported_claims))
        }
