from core.rag import ClinicalRAG

def test_rag_indexing_and_retrieval():
    rag = ClinicalRAG()
    
    # 1. Lập chỉ mục các tài liệu mẫu
    rag.index_document(
        "Hướng dẫn điều trị tăng huyết áp: Sử dụng Amlodipin 5mg hàng ngày.", 
        source="Phác đồ BYT"
    )
    rag.index_document(
        "Bệnh nhân đái tháo đường cần kiểm soát đường huyết dưới 7.0 mmol/L.", 
        source="Hướng dẫn ĐTĐ"
    )
    rag.index_document(
        "Triệu chứng viêm phổi bao gồm ho khan, sốt cao và khó thở.", 
        source="Sổ tay lâm sàng"
    )
    
    # 2. Truy hồi
    res = rag.retrieve_context("Bệnh nhân bị tăng huyết áp thì uống thuốc gì?", top_k=1)
    
    # 3. Kiểm tra kết quả
    citations = res["citations"]
    assert len(citations) == 1, "Phải tìm thấy 1 tài liệu tương ứng"
    assert citations[0]["source"] == "Phác đồ BYT", "Nguồn trích dẫn phải đúng là Phác đồ BYT"
    assert "Amlodipin" in res["combined_context"], "Context trả về phải chứa thông tin Amlodipin"

def test_rag_no_match():
    rag = ClinicalRAG()
    rag.index_document("Sốt xuất huyết truyền qua muỗi vằn.", source="Dịch tễ học")
    
    # Truy vấn từ khóa không có trong tài liệu
    res = rag.retrieve_context("Đau dạ dày", top_k=1)
    
    assert len(res["citations"]) == 0, "Không được trả về citation nếu không khớp"
    assert res["combined_context"] == "", "Context phải rỗng nếu không khớp"

if __name__ == "__main__":
    test_rag_indexing_and_retrieval()
    test_rag_no_match()
    print("All RAG tests passed!")

