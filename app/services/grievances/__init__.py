"""
Grievance service exports for Vapi webhook dispatcher.
"""

from app.services.grievances.grievance_handler import GrievanceQueryHandler

_handler = GrievanceQueryHandler()

file_complaint = _handler.file_complaint
get_complaint_status = _handler.get_complaint_status
general_grievance_query = _handler.general_grievance_query
