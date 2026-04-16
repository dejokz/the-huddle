"""
Tax Guru Handler (Phase 1 Scaffold)
Property tax assistance - full implementation in Phase 2.
"""

from typing import Dict


class TaxQueryHandler:
    service = "tax"

    def get_tax_estimate(self, query: str = "") -> Dict:
        data = {
            "type": "phase_one_scaffold",
            "message": "Property tax assistance is coming soon in Phase 2. For now, I can answer basic questions about BBMP property tax, Khata types, and payment deadlines.",
            "basic_info": {
                "annual_due": "April 30 and November 30",
                "early_payment_discount": "10% if paid by April 30",
                "khata_types": "A-Khata (full documentation), B-Khata (revenue records incomplete), E-Khata (digital with Aadhaar)",
                "contact": "Visit your nearest BBMP zonal office or bbmp.gov.in"
            }
        }
        return {"success": True, "response": str(data), "data": data}

    def get_payment_options(self, query: str = "") -> Dict:
        return self.get_tax_estimate(query)

    def general_tax_query(self, query: str = "") -> Dict:
        return self.get_tax_estimate(query)
