"""
Certificate service exports for Vapi webhook dispatcher.
"""

from app.services.certificates.cert_handler import CertificateQueryHandler

_handler = CertificateQueryHandler()

assess_eligibility = _handler.assess_eligibility
generate_document_checklist = _handler.generate_document_checklist
get_procedure_steps = _handler.get_procedure_steps
get_affidavit_template = _handler.get_affidavit_template
get_office_info = _handler.get_office_info
general_cert_query = _handler.general_cert_query
