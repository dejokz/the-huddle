"""
Certificate Guru Handler
Handles BBMP birth/death certificate queries via Qdrant RAG.
"""

import os
import json
from typing import Dict, List
from qdrant_client import QdrantClient
from app.services.certificates.cert_data import (
    get_all_procedures,
    get_all_documents,
    get_all_affidavits,
    get_all_offices,
    get_procedure_by_id,
    get_document_by_id,
    get_office_by_zone,
)
from app.embeddings import LocalEmbedding

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")


class CertificateQueryHandler:
    """Handle certificate-related queries - returns data only for Vapi LLM"""
    service = "certificates"

    def __init__(self):
        self.qdrant = QdrantClient(url=QDRANT_URL)
        self.embeddings = LocalEmbedding()

    def _get_embedding(self, text: str) -> List[float]:
        return self.embeddings.encode(text)

    def _format_response(self, data: Dict) -> str:
        return json.dumps(data, indent=2)

    def _rag_search(self, collection_name: str, query: str, limit: int = 3) -> List[Dict]:
        """Generic RAG search against a Qdrant collection."""
        try:
            embedding = self._get_embedding(query)
            results = self.qdrant.query_points(
                collection_name=collection_name,
                query=embedding,
                limit=limit
            ).points
            return [r.payload for r in results]
        except Exception as e:
            print(f"[Error] RAG search {collection_name}: {e}")
            return []

    def assess_eligibility(self, birth_type: str = "", days_since_birth: int = -1, request_type: str = "", query: str = "") -> Dict:
        """Determine procedural pathway based on citizen circumstances."""
        try:
            # If explicit params missing, fall back to RAG on procedures
            if not birth_type or days_since_birth < 0:
                results = self._rag_search("cert_procedures", query or "eligibility assessment", limit=3)
                data = {
                    "query": query or "eligibility assessment",
                    "type": "eligibility",
                    "results_found": len(results),
                    "procedures": results,
                    "note": "Please tell me: Was the birth in a hospital or at home? How many days ago was the birth? Do you need a new certificate, a correction, or a duplicate?"
                }
                return {"success": True, "response": self._format_response(data), "data": data}

            pathway = ""
            timeline = ""
            fees = ""
            penalties = ""

            if request_type.lower() in ["correction", "fix", "name change"]:
                pathway = "correction"
            elif request_type.lower() in ["duplicate", "lost", "replacement"]:
                pathway = "duplicate"
            elif request_type.lower() in ["name inclusion", "add name"]:
                pathway = "name_inclusion"
            else:
                if birth_type.lower() in ["hospital"] and days_since_birth <= 21:
                    pathway = "standard_hospital"
                    timeline = "7 days under SAKALA Act"
                    fees = "No fee"
                    penalties = "None"
                elif birth_type.lower() in ["home"] and days_since_birth <= 21:
                    pathway = "standard_home"
                    timeline = "7 days under SAKALA Act"
                    fees = "No fee"
                    penalties = "None"
                elif days_since_birth <= 30:
                    pathway = "delayed_21_to_30_days"
                    timeline = "7 to 14 days"
                    fees = "Rs 2 late fee"
                    penalties = "Minor delay penalty"
                elif days_since_birth <= 365:
                    pathway = "delayed_30_days_to_1_year"
                    timeline = "21 days under SAKALA Act"
                    fees = "Rs 5 penalty"
                    penalties = "Additional affidavit and witness documents required"
                else:
                    pathway = "late_beyond_1_year"
                    timeline = "6 to 12 months"
                    fees = "Rs 10 plus magistrate approval costs"
                    penalties = "Magistrate order required; complex documentation"

            data = {
                "query": query or "eligibility assessment",
                "type": "eligibility",
                "birth_type": birth_type,
                "days_since_birth": days_since_birth,
                "request_type": request_type,
                "pathway": pathway,
                "timeline": timeline,
                "fees": fees,
                "penalties": penalties,
                "next_step": "I can now generate your personalized document checklist."
            }
            return {"success": True, "response": self._format_response(data), "data": data}
        except Exception as e:
            return {"success": False, "error": str(e), "response": "{\"error\": \"Could not assess eligibility\"}"}

    def generate_document_checklist(self, birth_type: str = "", days_since_birth: int = -1, request_type: str = "", query: str = "") -> Dict:
        """Return personalized document checklist."""
        try:
            checklist = []
            notes = []

            # Base documents
            if request_type.lower() not in ["correction", "fix", "name change"]:
                checklist.append({"document": "Parents' Aadhaar Cards", "purpose": "Identity and address verification", "alternatives": "Passport, Voter ID, or Ration Card with photo"})

            if birth_type.lower() == "hospital" and request_type.lower() in ["new", "registration", ""]:
                checklist.append({"document": "Hospital Discharge Summary", "purpose": "Proof of institutional birth", "alternatives": "Hospital birth certificate or medical records"})

            if birth_type.lower() == "home":
                checklist.append({"document": "Two Witness Declarations", "purpose": "Attestation of birth circumstances by neighbors or relatives", "alternatives": "Community members who knew about the birth. No government official required."})
                checklist.append({"document": "Medical Attendant Certificate", "purpose": "Confirmation by doctor, nurse, or midwife", "alternatives": "If unavailable, additional witness declarations or pregnancy records"})
                checklist.append({"document": "Address Proof from Birth Time Period", "purpose": "Establish jurisdiction for zonal office", "alternatives": "Rental agreement, utility bill, or employer letter from that period"})

            if days_since_birth > 21 and request_type.lower() in ["new", "registration", ""]:
                checklist.append({"document": "Late Registration Affidavit", "purpose": "Legal declaration explaining delay", "alternatives": "Prescribed format available at BBMP offices"})
                notes.append(f"Late registration fee applies: Rs 2 for 21-30 days, Rs 5 for 30 days to 1 year, Rs 10 plus magistrate costs beyond 1 year. Your case is {days_since_birth} days.")

            if request_type.lower() in ["correction", "fix", "name change"]:
                checklist.append({"document": "Notarized Affidavit for Correction", "purpose": "Legal declaration requesting correction", "alternatives": "Drafted on non-judicial stamp paper and signed before notary"})
                notes.append("Only ONE correction is allowed per birth certificate. Please verify all details before applying.")

            if request_type.lower() in ["name inclusion", "add name"]:
                checklist.append({"document": "Name Inclusion Affidavit", "purpose": "Request to add infant name to certificate", "alternatives": "Non-judicial stamp paper, notarized"})

            data = {
                "query": query or "document checklist",
                "type": "checklist",
                "birth_type": birth_type,
                "days_since_birth": days_since_birth if days_since_birth >= 0 else None,
                "request_type": request_type,
                "checklist": checklist,
                "notes": notes
            }
            return {"success": True, "response": self._format_response(data), "data": data}
        except Exception as e:
            return {"success": False, "error": str(e), "response": "{\"error\": \"Could not generate checklist\"}"}

    def get_procedure_steps(self, query: str) -> Dict:
        """Search procedure steps via RAG."""
        results = self._rag_search("certificates_procedures", query, limit=3)
        data = {
            "query": query,
            "type": "procedure_steps",
            "results_found": len(results),
            "procedures": results
        }
        return {"success": True, "response": self._format_response(data), "data": data}

    def get_affidavit_template(self, template_type: str = "", query: str = "") -> Dict:
        """Retrieve affidavit template via RAG or direct lookup."""
        if template_type:
            all_affs = get_all_affidavits()
            matches = [a for a in all_affs if template_type.lower() in a.get("template_type", "").lower()]
            if matches:
                data = {
                    "query": query or template_type,
                    "type": "affidavit_template",
                    "template": matches[0]
                }
                return {"success": True, "response": self._format_response(data), "data": data}

        results = self._rag_search("certificates_affidavits", query or template_type, limit=2)
        data = {
            "query": query or template_type,
            "type": "affidavit_template",
            "results_found": len(results),
            "templates": results
        }
        return {"success": True, "response": self._format_response(data), "data": data}

    def get_office_info(self, zone_name: str = "", query: str = "") -> Dict:
        """Find BBMP office info."""
        if zone_name:
            office = get_office_by_zone(zone_name)
            if office:
                data = {"query": query or zone_name, "type": "office_info", "office": office}
                return {"success": True, "response": self._format_response(data), "data": data}

        results = self._rag_search("certificates_offices", query or zone_name, limit=3)
        data = {
            "query": query or zone_name,
            "type": "office_info",
            "results_found": len(results),
            "offices": results
        }
        return {"success": True, "response": self._format_response(data), "data": data}

    def general_cert_query(self, query: str) -> Dict:
        """Fallback RAG across all certificate collections."""
        procedures = self._rag_search("certificates_procedures", query, limit=2)
        documents = self._rag_search("certificates_documents", query, limit=2)
        affidavits = self._rag_search("certificates_affidavits", query, limit=1)
        offices = self._rag_search("certificates_offices", query, limit=1)

        data = {
            "query": query,
            "type": "general_search",
            "procedures": procedures,
            "documents": documents,
            "affidavits": affidavits,
            "offices": offices
        }
        return {"success": True, "response": self._format_response(data), "data": data}
