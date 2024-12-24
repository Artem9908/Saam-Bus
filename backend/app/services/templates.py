from datetime import datetime
from typing import Dict
import logging
from ..exceptions import TemplateError, ValidationError

logger = logging.getLogger(__name__)

class DocumentTemplate:
    @staticmethod
    def _generate_receipt(data: Dict) -> str:
        """Generate receipt template"""
        return f"""RECEIPT

Date: {data['date']}
Customer: {data['name']}
Amount: ${data['amount']:.2f}

Thank you for your business!
"""

    @staticmethod
    def generate_receipt(data: Dict[str, any]) -> str:
        return f"""
RECEIPT
----------------------------------------

Document Number: {datetime.now().strftime('%Y%m%d%H%M%S')}
Issue Date: {data['date']}

RECIPIENT INFORMATION
----------------------------------------
Name: {data['name']}

PAYMENT DETAILS
----------------------------------------
Amount Paid: ${data['amount']:.2f}

CONFIRMATION
----------------------------------------
This document certifies that {data['name']} 
has paid the amount of ${data['amount']:.2f} 
on {data['date']}.

----------------------------------------
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Document ID: {datetime.now().strftime('%Y%m%d%H%M%S')}
"""

    @staticmethod
    def generate_invoice(data: Dict[str, any]) -> str:
        return f"""
INVOICE
----------------------------------------

Invoice Number: INV-{datetime.now().strftime('%Y%m%d%H%M%S')}
Issue Date: {data['date']}

BILL TO
----------------------------------------
Name: {data['name']}

AMOUNT DUE
----------------------------------------
Total Amount: ${data['amount']:.2f}

PAYMENT TERMS
----------------------------------------
Due upon receipt

----------------------------------------
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    @staticmethod
    def generate_contract(data: Dict[str, any]) -> str:
        return f"""
CONTRACT
----------------------------------------

Contract Number: CNT-{datetime.now().strftime('%Y%m%d%H%M%S')}
Date: {data['date']}

PARTIES
----------------------------------------
Client: {data['name']}

TERMS AND CONDITIONS
----------------------------------------
1. Payment Terms
   Amount: ${data['amount']:.2f}
   Due Date: {data['date']}

2. Services
   - Document generation services
   - Digital storage
   - Access to generated documents

3. Agreement
This contract is entered into by {data['name']} 
for the amount of ${data['amount']:.2f}
on {data['date']}.

----------------------------------------
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Document ID: {datetime.now().strftime('%Y%m%d%H%M%S')}
"""

    @staticmethod
    def _generate_contract(data: Dict) -> str:
        """Generate contract template"""
        return f"""CONTRACT

Contract Number: CNT-{datetime.now().strftime('%Y%m%d%H%M')}

PARTIES
1. Company Name
2. {data['name']}

TERMS AND CONDITIONS
1. Amount: ${data['amount']:.2f}
2. Date: {data['date']}

Signatures:
_________________
Company Representative

_________________
{data['name']}
"""

    @staticmethod
    def get_template(template_type: str, data: Dict[str, any]) -> str:
        templates = {
            'receipt': DocumentTemplate.generate_receipt,
            'invoice': DocumentTemplate.generate_invoice,
            'contract': DocumentTemplate.generate_contract,
        }
        
        template_func = templates.get(template_type.lower())
        if not template_func:
            raise ValueError(f"Unknown template type: {template_type}")
            
        return template_func(data) 

    @staticmethod
    def generate_template(template_type: str, data: Dict) -> str:
        """Generate document content from template"""
        valid_templates = ["receipt", "invoice", "contract"]
        if template_type not in valid_templates:
            raise TemplateError(f"Unknown template type: {template_type}")
        
        try:
            if template_type == "receipt":
                return DocumentTemplate.generate_receipt(data)
            elif template_type == "invoice":
                return DocumentTemplate.generate_invoice(data)
            elif template_type == "contract":
                return DocumentTemplate.generate_contract(data)
        except Exception as e:
            raise TemplateError(f"Failed to generate template: {str(e)}") 