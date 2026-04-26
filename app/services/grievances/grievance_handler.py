"""
Public Grievance Assistant Handler
Structured routing and escalation support for civic complaints in Bengaluru.
"""

import json
from typing import Dict, List


ISSUE_ROUTING = [
    {
        "keywords": ["water", "sewage", "drainage", "sanitation", "pipeline"],
        "category": "Water and drainage disruption",
        "primary_department": "BWSSB",
        "supporting_departments": ["BBMP", "KSPCB"],
        "typical_channels": ["Janaspandana 1902", "iPGRS portal", "ward office"],
        "expected_first_action": "Route complaint to water or drainage infrastructure team with location details.",
    },
    {
        "keywords": ["pothole", "road", "street", "asphalt", "dug up"],
        "category": "Road damage or pothole complaint",
        "primary_department": "BBMP Roads Department",
        "supporting_departments": ["BWSSB", "BDA", "NHAI"],
        "typical_channels": ["Janaspandana 1902", "iPGRS portal", "BBMP zonal office"],
        "expected_first_action": "Identify whether the road belongs to BBMP or another agency and tag the location.",
    },
    {
        "keywords": ["streetlight", "light", "dark", "lamp", "electric pole"],
        "category": "Streetlight malfunction",
        "primary_department": "BBMP Electrical Department",
        "supporting_departments": ["BESCOM"],
        "typical_channels": ["Janaspandana 1902", "ward office", "local electrical complaint channel"],
        "expected_first_action": "Capture pole or landmark details for field verification.",
    },
    {
        "keywords": ["illegal building", "violation", "extra floor", "construction", "setback"],
        "category": "Building violation complaint",
        "primary_department": "BBMP Town Planning",
        "supporting_departments": ["BDA", "Fire Department", "KSPCB"],
        "typical_channels": ["iPGRS portal", "BBMP Town Planning office", "written complaint with evidence"],
        "expected_first_action": "Route to planning enforcement with location, photos, and nature of violation.",
    },
]


class GrievanceQueryHandler:
    service = "grievances"

    def _format_response(self, data: Dict) -> str:
        return json.dumps(data, indent=2)

    def _classify_issue(self, query: str) -> Dict:
        q = (query or "").lower()
        matches = []
        for item in ISSUE_ROUTING:
            if any(keyword in q for keyword in item["keywords"]):
                matches.append(item)
        if len(matches) > 1:
            return {
                "category": "Multi-department civic complaint",
                "primary_department": matches[0]["primary_department"],
                "supporting_departments": sorted(
                    {dept for item in matches for dept in ([item["primary_department"]] + item["supporting_departments"])}
                ),
                "typical_channels": ["Janaspandana 1902", "iPGRS portal", "BBMP zonal office"],
                "expected_first_action": "Capture the exact location once, then route the issue to multiple departments instead of making the citizen repeat the complaint.",
                "matched_categories": [item["category"] for item in matches],
            }
        if matches:
            return matches[0]
        return {
            "category": "General civic grievance",
            "primary_department": "Janaspandana / iPGRS triage",
            "supporting_departments": ["BBMP"],
            "typical_channels": ["Janaspandana 1902", "iPGRS portal"],
            "expected_first_action": "Capture issue category, exact location, and citizen callback details before routing.",
        }

    def file_complaint(self, query: str = "") -> Dict:
        route = self._classify_issue(query)
        data = {
            "type": "grievance_routing",
            "query": query,
            "classified_issue": route["category"],
            "matched_categories": route.get("matched_categories", [route["category"]]),
            "routing": {
                "primary_department": route["primary_department"],
                "supporting_departments": route["supporting_departments"],
                "channels": route["typical_channels"],
            },
            "complaint_payload_checklist": [
                "Exact location with landmark, ward, or street name",
                "Short description of the issue",
                "How long the issue has been happening",
                "Photo or video evidence if available",
                "Callback number for follow-up",
            ],
            "first_action_expected": route["expected_first_action"],
            "citizen_friendly_next_step": "File the complaint with location details first. If it is misrouted, escalate with the complaint number instead of starting over.",
        }
        return {"success": True, "response": self._format_response(data), "data": data}

    def get_complaint_status(self, query: str = "") -> Dict:
        route = self._classify_issue(query)
        data = {
            "type": "grievance_status_guidance",
            "query": query,
            "likely_department": route["primary_department"],
            "status_flow": [
                "Complaint submitted and acknowledgement number generated",
                "Assigned to ward or departmental officer",
                "Field inspection or action initiated",
                "Citizen receives update or closure request",
            ],
            "escalation_path": [
                "Follow up using the complaint number",
                "Ask for assigned officer or department if no action is visible",
                "Escalate through Janaspandana or appellate grievance channel if closure is unsatisfactory",
            ],
            "transparency_message": "Citizens often get stuck after receiving only a reference number. The assistant keeps the next step clear and actionable.",
        }
        return {"success": True, "response": self._format_response(data), "data": data}

    def general_grievance_query(self, query: str = "") -> Dict:
        route = self._classify_issue(query)
        data = {
            "type": "general_grievance_guidance",
            "query": query,
            "classified_issue": route["category"],
            "recommended_department": route["primary_department"],
            "backup_departments": route["supporting_departments"],
            "channels": route["typical_channels"],
            "best_practices": [
                "State the issue in one sentence first, then add the location.",
                "Always save the complaint number.",
                "If photos exist, mention that during filing even if the first channel is voice-only.",
                "If the wrong department rejects it, reuse the same facts and complaint history to escalate.",
            ],
            "mentor_demo_hook": "The assistant reduces complaint drop-off by translating messy citizen language into structured routing and follow-up guidance.",
        }
        return {"success": True, "response": self._format_response(data), "data": data}
