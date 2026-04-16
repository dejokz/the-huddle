"""
Bengaluru Birth/Death Certificate Data Module
Structured data for BBMP certificate procedures, documents, affidavits, and offices.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class ProcedureStep:
    step_id: str
    title: str
    description: str
    timeline_days: str
    applicable_to: str
    fees: str
    penalties: str


@dataclass
class DocumentRequirement:
    doc_id: str
    name: str
    purpose: str
    alternatives: str
    when_required: str


@dataclass
class AffidavitTemplate:
    template_id: str
    template_type: str
    purpose: str
    draft_text: str
    notary_fee_range: str
    stamp_paper_requirement: str


@dataclass
class BbmpOffice:
    office_id: str
    zone_name: str
    address: str
    timing: str
    contact: str
    services: str


# ------------------------------------------------------------------
# BBMP Birth Certificate Procedures
# ------------------------------------------------------------------
_BIRTH_PROCEDURES = [
    ProcedureStep(
        step_id="birth_hospital_21_days",
        title="Standard Hospital Birth Registration (Within 21 Days)",
        description="For births in registered hospitals within BBMP limits. Hospital submits digital registration via eJanMa portal. Parents receive SMS confirmation. Certificate can be downloaded online or collected from BBMP zonal office.",
        timeline_days="7 days under SAKALA Act",
        applicable_to="Hospital births within 21 days of birth date",
        fees="No fee",
        penalties="None"
    ),
    ProcedureStep(
        step_id="birth_home_21_days",
        title="Home Birth Registration (Within 21 Days)",
        description="Parents must visit BBMP zonal office with parents' Aadhaar cards, address proof from birth time period, and two witness declarations from neighbors or relatives who knew about the birth. Medical attendant certificate if available.",
        timeline_days="7 days under SAKALA Act",
        applicable_to="Home births within 21 days",
        fees="No fee",
        penalties="None"
    ),
    ProcedureStep(
        step_id="birth_delayed_21_to_30_days",
        title="Delayed Hospital Birth Registration (21 to 30 Days)",
        description="Hospital can still submit digitally but late fee of Rs 2 applies. Parents should follow up with hospital administration to ensure submission.",
        timeline_days="7 to 14 days",
        applicable_to="Hospital births between 21 and 30 days after birth",
        fees="Rs 2 late fee",
        penalties="Minor delay, small penalty"
    ),
    ProcedureStep(
        step_id="birth_delayed_30_days_to_1_year",
        title="Late Birth Registration (30 Days to 1 Year)",
        description="Requires late registration affidavit, witness documentation, and payment of Rs 5 penalty. Application submitted at BBMP zonal office with supporting evidence.",
        timeline_days="21 days under SAKALA Act for delayed cases",
        applicable_to="Births registered between 30 days and 1 year after birth",
        fees="Rs 5 penalty",
        penalties="Additional affidavit and witness documents required"
    ),
    ProcedureStep(
        step_id="birth_late_beyond_1_year",
        title="Very Late Birth Registration (Beyond 1 Year)",
        description="Requires magistrate approval, additional affidavits, witness documentation, and potentially judicial orders. Timeline extends to 6 to 12 months. Fee is Rs 10 plus court-related costs.",
        timeline_days="6 to 12 months",
        applicable_to="Births registered more than 1 year after birth date",
        fees="Rs 10 plus magistrate approval costs",
        penalties="Magistrate order required; complex documentation"
    ),
    ProcedureStep(
        step_id="birth_correction_minor",
        title="Minor Birth Certificate Correction",
        description="Spelling variations, missing initials, or typographical errors can be corrected through notarized affidavit and supporting ID submitted directly to BBMP office. Examples: Aanand to Anand, missing middle initial.",
        timeline_days="15 to 30 days",
        applicable_to="Spelling errors, missing initials, typos",
        fees="Notary fee Rs 50 to 200",
        penalties="Only ONE correction allowed per certificate"
    ),
    ProcedureStep(
        step_id="birth_correction_major",
        title="Major Birth Certificate Correction",
        description="Complete name alterations, surname additions, or fundamental identity changes require Gazette notification, newspaper publications in both Kannada and English, and potentially court-level approval for individuals over 15 years.",
        timeline_days="Weeks to months",
        applicable_to="Complete name changes, surname additions, identity modifications",
        fees="Rs 3000 to 8000 including Gazette and newspaper costs",
        penalties="Only ONE correction allowed; irreversible if misclassified"
    ),
    ProcedureStep(
        step_id="birth_name_inclusion",
        title="Name Inclusion on Initially Blank Birth Certificate",
        description="Birth certificates can be registered initially as Male Child or Female Child without a name. Parents have one year to add the name without additional burden. After one year, formal correction process with Gazette notification is required.",
        timeline_days="Same as registration if within 1 year",
        applicable_to="Certificates registered without infant name",
        fees="No fee if within 1 year; Gazette costs if beyond 1 year",
        penalties="After 1 year, escalates to major correction procedure"
    ),
    ProcedureStep(
        step_id="birth_duplicate",
        title="Duplicate Birth Certificate Request",
        description="If original certificate is lost or damaged, apply for duplicate through eJanMa portal online verification or visit BBMP zonal office with ID proof and application letter.",
        timeline_days="7 to 14 days",
        applicable_to="Lost or damaged certificates",
        fees="Nominal fee Rs 10 to 50",
        penalties="None"
    ),
]

# ------------------------------------------------------------------
# Document Requirements
# ------------------------------------------------------------------
_DOCUMENTS = [
    DocumentRequirement(
        doc_id="doc_parents_aadhaar",
        name="Parents' Aadhaar Cards",
        purpose="Identity and address verification for birth registration",
        alternatives="Passport, Voter ID, or Ration Card with photo",
        when_required="All new registrations"
    ),
    DocumentRequirement(
        doc_id="doc_hospital_discharge",
        name="Hospital Discharge Summary",
        purpose="Proof of institutional birth for hospital registration pathway",
        alternatives="Hospital birth certificate or medical records from delivery",
        when_required="Hospital births"
    ),
    DocumentRequirement(
        doc_id="doc_witness_declarations",
        name="Two Witness Declarations",
        purpose="Attestation of birth circumstances for home births",
        alternatives="Neighbors, relatives, or community members who knew about the birth. They do not need to be government officials.",
        when_required="Home births and late registrations"
    ),
    DocumentRequirement(
        doc_id="doc_medical_attendant",
        name="Medical Attendant Certificate",
        purpose="Confirmation by doctor, nurse, or midwife who attended the birth",
        alternatives="If unavailable, additional witness declarations or pregnancy records",
        when_required="Home births when available"
    ),
    DocumentRequirement(
        doc_id="doc_address_proof_birth_time",
        name="Address Proof from Birth Time Period",
        purpose="Establishing jurisdictional location for zonal office assignment",
        alternatives="Rental agreement, utility bill, or employer letter from that period",
        when_required="Home births and some delayed registrations"
    ),
    DocumentRequirement(
        doc_id="doc_late_affidavit",
        name="Late Registration Affidavit",
        purpose="Legal declaration explaining delay in registration with penalty calculation",
        alternatives="Prescribed format available at BBMP offices or through agent assistance",
        when_required="Delayed registrations beyond 21 days"
    ),
    DocumentRequirement(
        doc_id="doc_notarized_affidavit_correction",
        name="Notarized Affidavit for Correction",
        purpose="Legal declaration requesting minor correction on birth certificate",
        alternatives="Drafted on non-judicial stamp paper and signed before notary",
        when_required="Minor corrections"
    ),
    DocumentRequirement(
        doc_id="doc_gazette_notification",
        name="Gazette Notification",
        purpose="Official government publication for major name or identity changes",
        alternatives="Required for all major corrections; cannot be substituted",
        when_required="Major corrections and name inclusion beyond 1 year"
    ),
    DocumentRequirement(
        doc_id="doc_newspaper_publication",
        name="Newspaper Publications",
        purpose="Public notice of name change in both Kannada and English newspapers",
        alternatives="Two newspaper clippings required as proof",
        when_required="Major corrections"
    ),
]

# ------------------------------------------------------------------
# Affidavit Templates
# ------------------------------------------------------------------
_AFFIDAVITS = [
    AffidavitTemplate(
        template_id="aff_minor_correction",
        template_type="Minor Name Correction",
        purpose="Correcting spelling error or missing initial on birth certificate",
        draft_text="I, [parent name], residing at [address], do hereby solemnly declare that my child's name was registered as [incorrect name] in birth certificate number [registration number] dated [date], whereas the correct name is [correct name]. This error occurred due to [reason: typographical error/clerical mistake]. I request correction of the same.",
        notary_fee_range="Rs 50 to 200",
        stamp_paper_requirement="Non-judicial stamp paper of Rs 20 value"
    ),
    AffidavitTemplate(
        template_id="aff_late_registration",
        template_type="Late Birth Registration",
        purpose="Explaining delay in registering birth beyond 21 days",
        draft_text="I, [parent name], son/daughter of [grandparent name], residing at [address], do hereby solemnly declare that my child [child name] was born on [date] at [place of birth: hospital name or home address]. Due to [reason for delay: illness/migration/lack of awareness], the birth could not be registered within the statutory period of 21 days. I request you to kindly register the birth and issue the birth certificate.",
        notary_fee_range="Rs 50 to 200",
        stamp_paper_requirement="Non-judicial stamp paper of Rs 20 value"
    ),
    AffidavitTemplate(
        template_id="aff_name_inclusion",
        template_type="Name Inclusion on Birth Certificate",
        purpose="Adding infant name to certificate initially registered as Male/Female Child",
        draft_text="I, [parent name], residing at [address], do hereby solemnly declare that my child was born on [date] and registered under birth certificate number [registration number] dated [date of registration] as [Male Child/Female Child]. The name of the child is [child name]. I request you to kindly include the name in the birth certificate.",
        notary_fee_range="Rs 50 to 200",
        stamp_paper_requirement="Non-judicial stamp paper of Rs 20 value"
    ),
]

# ------------------------------------------------------------------
# BBMP Zonal Offices (sample key zones for Bengaluru)
# ------------------------------------------------------------------
_OFFICES = [
    BbmpOffice(
        office_id="bbmp_nr_square",
        zone_name="Head Office N.R. Square",
        address="N.R. Square, Bengaluru, Karnataka 560002",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2222-1234",
        services="Central reference, record verification, complex corrections"
    ),
    BbmpOffice(
        office_id="bbmp_east_zone",
        zone_name="East Zone Office",
        address="CV Raman Nagar, Bengaluru, Karnataka 560093",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2530-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
    BbmpOffice(
        office_id="bbmp_west_zone",
        zone_name="West Zone Office",
        address="Rajajinagar, Bengaluru, Karnataka 560010",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2332-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
    BbmpOffice(
        office_id="bbmp_south_zone",
        zone_name="South Zone Office",
        address="Jayanagar, Bengaluru, Karnataka 560041",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2663-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
    BbmpOffice(
        office_id="bbmp_north_zone",
        zone_name="North Zone Office",
        address="Yelahanka, Bengaluru, Karnataka 560064",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2846-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
    BbmpOffice(
        office_id="bbmp_bommanahalli",
        zone_name="Bommanahalli Zone Office",
        address="Bommanahalli, Bengaluru, Karnataka 560068",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2572-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
    BbmpOffice(
        office_id="bbmp_yelahanka",
        zone_name="Yelahanka Zone Office",
        address="Yelahanka New Town, Bengaluru, Karnataka 560064",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2845-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
    BbmpOffice(
        office_id="bbmp_dasarahalli",
        zone_name="Dasarahalli Zone Office",
        address="Dasarahalli, Bengaluru, Karnataka 560057",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2839-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
    BbmpOffice(
        office_id="bbmp_mahadevapura",
        zone_name="Mahadevapura Zone Office",
        address="Mahadevapura, Bengaluru, Karnataka 560048",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2851-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
    BbmpOffice(
        office_id="bbmp_rajrajeshwari",
        zone_name="Rajarajeshwari Nagar Zone Office",
        address="Rajarajeshwari Nagar, Bengaluru, Karnataka 560098",
        timing="10:00 AM to 5:30 PM, Monday to Saturday",
        contact="080-2860-XXXX",
        services="Birth and death registration, corrections, duplicate certificates"
    ),
]

# ------------------------------------------------------------------
# Getters for embedding generation
# ------------------------------------------------------------------
def get_all_procedures() -> List[Dict]:
    return [asdict(p) for p in _BIRTH_PROCEDURES]


def get_all_documents() -> List[Dict]:
    return [asdict(d) for d in _DOCUMENTS]


def get_all_affidavits() -> List[Dict]:
    return [asdict(a) for a in _AFFIDAVITS]


def get_all_offices() -> List[Dict]:
    return [asdict(o) for o in _OFFICES]


# Convenience lookup helpers for handler
def get_procedure_by_id(step_id: str) -> Optional[Dict]:
    for p in _BIRTH_PROCEDURES:
        if p.step_id == step_id:
            return asdict(p)
    return None


def get_document_by_id(doc_id: str) -> Optional[Dict]:
    for d in _DOCUMENTS:
        if d.doc_id == doc_id:
            return asdict(d)
    return None


def get_office_by_zone(zone_name: str) -> Optional[Dict]:
    for o in _OFFICES:
        if zone_name.lower() in o.zone_name.lower():
            return asdict(o)
    return None
