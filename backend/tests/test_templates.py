import pytest
from datetime import datetime
from app.services.templates import DocumentTemplate
from app.exceptions import TemplateError

def test_contract_template():
    """Test contract template generation"""
    data = {
        'name': 'Test Client',
        'date': '2024-01-01',
        'amount': 1500.00
    }
    
    content = DocumentTemplate.generate_contract(data)
    
    # Check contract structure
    assert 'CONTRACT' in content
    assert 'Contract Number: CNT-' in content
    assert 'PARTIES' in content
    assert 'TERMS AND CONDITIONS' in content
    
    # Check data insertion
    assert 'Test Client' in content
    assert '2024-01-01' in content
    assert '1500.00' in content
    assert 'Document ID:' in content

def test_template_selection():
    """Test template type selection"""
    data = {
        'name': 'Test User',
        'date': '2024-01-01',
        'amount': 100.00
    }
    
    # Test all template types
    templates = ['receipt', 'invoice', 'contract']
    for template_type in templates:
        content = DocumentTemplate.get_template(template_type, data)
        assert content is not None
        assert len(content) > 0
        assert data['name'] in content
        assert data['date'] in content
        assert str(data['amount']) in content

def test_invalid_template_type():
    """Test invalid template type handling"""
    with pytest.raises(ValueError, match="Unknown template type: invalid"):
        DocumentTemplate.get_template('invalid', {})

def test_template_error_handling():
    """Test template error handling"""
    test_data = {
        "name": "Test User",
        "date": "2024-01-01",
        "amount": 100.50
    }
    
    # Test invalid template type
    with pytest.raises(TemplateError, match="Unknown template type"):
        DocumentTemplate.generate_template("invalid_type", test_data)
    
    # Test missing required data
    with pytest.raises(TemplateError, match="Failed to generate template"):
        DocumentTemplate.generate_template("receipt", {})