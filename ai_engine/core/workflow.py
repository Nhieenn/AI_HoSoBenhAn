import difflib
import uuid
import time
from typing import Dict, Any, List, Callable

class WorkflowEngine:
    def __init__(self):
        # In-memory storage for drafts (for demonstration/mocking)
        # In a real app, this should be backed by a DB.
        self.drafts = {}
        self.feedbacks = []

    def create_draft(self, generated_text: str, metadata: Dict[str, Any] = None) -> str:
        """Create a new draft in the workflow."""
        draft_id = str(uuid.uuid4())
        self.drafts[draft_id] = {
            "id": draft_id,
            "original_text": generated_text,
            "current_text": generated_text,
            "status": "DRAFT",
            "metadata": metadata or {},
            "created_at": time.time()
        }
        return draft_id
        
    def review_draft(self, draft_id: str, status: str, updated_text: str = None) -> Dict[str, Any]:
        """
        UC-WF-01: Review và Phê duyệt
        Bác sĩ duyệt (APPROVED), từ chối (REJECTED), hoặc cập nhật nháp.
        """
        if draft_id not in self.drafts:
            raise ValueError(f"Draft {draft_id} not found.")
            
        valid_statuses = ["DRAFT", "APPROVED", "REJECTED"]
        status = status.upper()
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            
        draft = self.drafts[draft_id]
        
        if updated_text is not None:
            draft["current_text"] = updated_text
            
        draft["status"] = status
        draft["updated_at"] = time.time()
        
        return draft

    def record_feedback(self, original_text: str, approved_text: str) -> Dict[str, Any]:
        """
        UC-WF-02: Active Learning từ phản hồi bác sĩ.
        Ghi lại sự khác biệt (diff) giữa nháp gốc và bản duyệt để cải thiện mô hình.
        """
        diff = list(difflib.ndiff(original_text.splitlines(keepends=True), approved_text.splitlines(keepends=True)))
        
        # Chỉ trích xuất những dòng có thay đổi (+ hoặc -)
        changes = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]
        
        feedback_record = {
            "id": str(uuid.uuid4()),
            "original_text": original_text,
            "approved_text": approved_text,
            "changes": changes,
            "timestamp": time.time()
        }
        
        self.feedbacks.append(feedback_record)
        return feedback_record

    def process_approved_draft(self, draft_id: str) -> Dict[str, Any]:
        """
        Xử lý khi draft được approved, tự động extract diff.
        """
        if draft_id not in self.drafts:
            raise ValueError(f"Draft {draft_id} not found.")
            
        draft = self.drafts[draft_id]
        if draft["status"] != "APPROVED":
            raise ValueError(f"Draft {draft_id} must be APPROVED to process feedback.")
            
        if draft["original_text"] != draft["current_text"]:
            feedback = self.record_feedback(draft["original_text"], draft["current_text"])
            return {"draft": draft, "feedback_recorded": True, "feedback": feedback}
            
        return {"draft": draft, "feedback_recorded": False}

    def generate_silent(self, generator_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        UC-WF-03: Chế độ chạy ngầm (Silent Mode).
        Sinh nháp ngầm không hiển thị trong workflow thật để đánh giá chất lượng.
        """
        start_time = time.time()
        generated_tuple = generator_func(*args, **kwargs)
        if isinstance(generated_tuple, tuple) and len(generated_tuple) == 2:
            generated_text, evidence_map = generated_tuple
        else:
            generated_text = generated_tuple
            evidence_map = None
            
        execution_time = time.time() - start_time
        
        return {
            "generated_text": generated_text,
            "evidence_map": evidence_map,
            "is_silent": True,
            "execution_time_seconds": execution_time,
            "status": "SILENT_LOGGED"
        }
