"""
Property Tax Assistant Handler
Structured demo-friendly guidance for BBMP property tax queries.
"""

import json
import re
from typing import Dict, List


ZONE_RATES = {
    "A": 5.0,
    "B": 4.5,
    "C": 4.0,
    "D": 3.6,
    "E": 3.2,
    "F": 2.8,
}

KHATA_GUIDE = {
    "A-Khata": {
        "meaning": "Property with approved layout, sanctioned building plan, and compliant records.",
        "implications": "Eligible for standard payments, rebates, resale, and easier loan processing.",
    },
    "B-Khata": {
        "meaning": "Property appears in revenue records but planning approvals or documentation are incomplete.",
        "implications": "May face transaction friction, higher scrutiny, and weaker loan eligibility.",
    },
    "E-Khata": {
        "meaning": "Digitally linked property record with Aadhaar-based verification and online workflow support.",
        "implications": "Best suited for digital payments, verification, and future online transactions.",
    },
}

PAYMENT_CHANNELS = [
    "BBMP online portal",
    "Bengaluru One centres",
    "BBMP help centres and zonal offices",
    "Assisted digital payment through authorised kiosks",
]


class TaxQueryHandler:
    service = "tax"

    def _format_response(self, data: Dict) -> str:
        return json.dumps(data, indent=2)

    def _infer_zone(self, query: str) -> str:
        q = (query or "").lower()
        patterns = [
            r"\bzone\s*([a-f])\b",
            r"\b([a-f])\s*zone\b",
            r"\b([a-f])[- ]zone\b",
        ]
        for pattern in patterns:
            match = re.search(pattern, q)
            if match:
                return match.group(1).upper()
        return "B"

    def _infer_khata(self, query: str) -> str:
        q = (query or "").lower()
        if "e-khata" in q or "e khata" in q:
            return "E-Khata"
        if "b-khata" in q or "b khata" in q:
            return "B-Khata"
        return "A-Khata"

    def _infer_area_sqft(self, query: str) -> int:
        q = query or ""
        digits = []
        current = ""
        for ch in q:
            if ch.isdigit():
                current += ch
            elif current:
                digits.append(int(current))
                current = ""
        if current:
            digits.append(int(current))

        plausible = [n for n in digits if 300 <= n <= 10000]
        return plausible[0] if plausible else 1200

    def _make_estimate(self, query: str) -> Dict:
        zone = self._infer_zone(query)
        khata = self._infer_khata(query)
        area_sqft = self._infer_area_sqft(query)
        rate = ZONE_RATES[zone]

        annual_base = round(area_sqft * rate, 2)
        cesses = round(annual_base * 0.24, 2)
        gross_tax = round(annual_base + cesses, 2)
        early_discount = round(gross_tax * 0.10, 2)
        payable_if_early = round(gross_tax - early_discount, 2)

        return {
            "zone": zone,
            "khata_type": khata,
            "built_up_area_sqft": area_sqft,
            "illustrative_rate_per_sqft": rate,
            "base_tax_estimate": annual_base,
            "cesses_and_charges_estimate": cesses,
            "gross_annual_tax_estimate": gross_tax,
            "early_payment_discount": early_discount,
            "estimated_payable_if_paid_early": payable_if_early,
            "disclaimer": "This is a demo-friendly estimate using simplified zone-rate assumptions. Final BBMP demand depends on official property records, usage category, and assessment details.",
        }

    def get_tax_estimate(self, query: str = "") -> Dict:
        estimate = self._make_estimate(query)
        data = {
            "type": "tax_estimate",
            "query": query,
            "summary": "Illustrative BBMP property tax estimate with early-payment rebate.",
            "estimate": estimate,
            "explanation_steps": [
                f"Start with {estimate['built_up_area_sqft']} square feet in zone {estimate['zone']}.",
                f"Use an illustrative rate of Rs {estimate['illustrative_rate_per_sqft']} per square foot.",
                f"Add cesses and charges, then subtract the 10 percent early-payment discount if applicable.",
            ],
            "recommended_next_steps": [
                "Verify your official zone and built-up area on BBMP records.",
                "Check whether your property is A-Khata, B-Khata, or E-Khata before payment.",
                "Use the BBMP portal or Bengaluru One centre for the final payable amount.",
            ],
        }
        return {"success": True, "response": self._format_response(data), "data": data}

    def get_payment_options(self, query: str = "") -> Dict:
        khata = self._infer_khata(query)
        data = {
            "type": "payment_options",
            "query": query,
            "important_dates": {
                "financial_year_start": "April 1",
                "early_payment_discount_deadline": "April 30",
                "common_half_year_reference_point": "November 30",
            },
            "channels": PAYMENT_CHANNELS,
            "khata_context": {
                "selected_type": khata,
                "details": KHATA_GUIDE[khata],
            },
            "documents_to_keep_ready": [
                "Property ID or application number",
                "Khata details",
                "Owner identification proof",
                "Previous tax receipt if available",
            ],
            "escalation_guidance": [
                "If the tax demand looks inflated, compare area and zone classification first.",
                "If the payment is not reflected, keep the receipt and contact the BBMP zonal office.",
                "If Khata details are inconsistent, resolve that before assuming the tax engine is wrong.",
            ],
        }
        return {"success": True, "response": self._format_response(data), "data": data}

    def general_tax_query(self, query: str = "") -> Dict:
        estimate = self._make_estimate(query)
        khata = self._infer_khata(query)
        data = {
            "type": "general_tax_guidance",
            "query": query,
            "khata_guide": KHATA_GUIDE,
            "payment_channels": PAYMENT_CHANNELS,
            "illustrative_estimate": estimate,
            "common_citizen_questions": [
                "What is the difference between A-Khata, B-Khata, and E-Khata?",
                "How much rebate do I get if I pay early?",
                "What should I do if my built-up area is wrong in BBMP records?",
            ],
            "mentor_demo_hook": "The assistant can explain tax in plain language, estimate dues, and guide the citizen toward the right correction or payment channel.",
        }
        if "dispute" in (query or "").lower() or "wrong" in (query or "").lower():
            data["dispute_support"] = {
                "likely_issue": "Assessment mismatch or record inconsistency",
                "suggested_documents": [
                    "Latest tax receipt",
                    "Khata extract or e-Khata record",
                    "Built-up area proof",
                    "Sale deed or title record",
                ],
                "next_step": "Raise the issue at the BBMP zonal office or authorised grievance channel with the supporting documents.",
            }
        return {"success": True, "response": self._format_response(data), "data": data}
