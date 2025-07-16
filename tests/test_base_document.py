from datetime import datetime
from shared.libraries.company_os_core.models import BaseDocument

def test_base_document_validation():
    doc = BaseDocument(
        title="Test Document",
        status="Draft",
        owner="Test User",
        last_updated=datetime.now(),
    )
    assert doc.title == "Test Document"
