"""
Tax service exports for Vapi webhook dispatcher.
"""

from app.services.tax.tax_handler import TaxQueryHandler

_handler = TaxQueryHandler()

get_tax_estimate = _handler.get_tax_estimate
get_payment_options = _handler.get_payment_options
general_tax_query = _handler.general_tax_query
