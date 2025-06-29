from typing import Dict, Optional
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
        
        db.session.add(template)
        db.session.commit()
        return template
        
    def get_template(self, template_id: int) -> Optional[ContentTemplate]:
        return ContentTemplate.query.get(template_id)
        
    def list_templates(self) -> List[ContentTemplate]:
        return ContentTemplate.query.all()
        
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
        template = ContentTemplate.query.get(template_id)
        if template:
            db.session.delete(template)
            db.session.commit()
            return True
        return False