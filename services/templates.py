<<<<<<< HEAD
from typing import Dict, Optional, List, List
=======
from typing import Dict, Optional, List
>>>>>>> bda3689dc620783c47fe4eefc69ce623bbc8cc42
from database import SessionLocal
from models import ContentTemplate

class TemplateManager:
    def __init__(self):
        self.templates = {}
        
    def create_template(
        self,
        name: str,
        content: str,
        variables: Optional[Dict[str, str]] = None
    ) -> ContentTemplate:
        template = ContentTemplate(
            name=name,
            content=content,
            variables=variables or {}
        )
        session = SessionLocal()
        try:
            session.add(template)
            session.commit()
            session.refresh(template)
        finally:
            session.close()
        return template
        
    def get_template(self, template_id: int) -> Optional[ContentTemplate]:
        session = SessionLocal()
        try:
            return session.query(ContentTemplate).get(template_id)
        finally:
            session.close()
        
    def list_templates(self) -> List[ContentTemplate]:
        session = SessionLocal()
        try:
            return session.query(ContentTemplate).all()
        finally:
            session.close()
        
    def apply_template(
        self,
        template_id: int,
        variables: Dict[str, str]
    ) -> str:
        template = self.get_template(template_id)
        if not template:
            raise ValueError("Template not found")
            
        content = template.content
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", value)
        return content
        
    def delete_template(self, template_id: int) -> bool:
        session = SessionLocal()
        try:
            template = session.query(ContentTemplate).get(template_id)
            if template:
                session.delete(template)
                session.commit()
                return True
            return False
        finally:
            session.close()