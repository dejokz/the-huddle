# Demo Script

## Goal

Use this as your 5 to 7 minute mentoring-round script. It is designed for a working demo first, with a clean fallback if the live call flow becomes unstable.

## 30-Second Opening

Hi, we are presenting **Bengaluru Sahayaka**, a voice-first AI assistant for local government services in Bengaluru.  
Instead of forcing citizens to navigate forms, departments, and jargon, our system helps them through voice in simple language across three high-impact flows: **birth and death certificates, property tax, and public grievances**.

## Demo Flow

### 1. Host Routing

Say:

> "I need help with a birth certificate."

What to point out:

- the host identifies the service instead of making the user browse menus
- the experience is built for English or Kannada
- the host routes to a specialist assistant

### 2. Certificate Demo

Say:

> "My baby was born at home 45 days ago. What do I need to do?"

Then say:

> "Can you tell me the documents I need?"

Then say:

> "Can you help me with the affidavit?"

What to point out:

- the assistant identifies this as a late registration case
- it explains penalty and timeline clearly
- it generates a personalized checklist instead of generic instructions
- it helps with affidavit drafting, which is where many citizens depend on middlemen

### 3. Property Tax Demo

Say:

> "I have a 1200 square foot property in B zone. Can you estimate my tax and tell me the payment options?"

What to point out:

- the assistant explains tax in plain language
- it gives an illustrative estimate and early-payment rebate
- it guides the user on Khata context and payment channels
- this is useful for citizens who are confused by assessment logic

### 4. Grievance Demo

Say:

> "There is a pothole and drainage issue near my street. Where should I complain and how do I track it?"

What to point out:

- the assistant classifies the complaint from natural language
- it suggests the right department and backup channels
- it gives a structured payload checklist for filing the complaint
- it explains follow-up and escalation, not just initial routing

## If Live Voice Demo Fails

Fallback immediately to:

1. Show the backend health endpoint: `/health`
2. Show the demo scenarios endpoint: `/demo/scenarios`
3. Trigger one certificate webhook example and one grievance/tax example
4. Explain that the same structured outputs are what power the voice orchestration layer

## What To Say If Mentors Ask "What Is Novel Here?"

- We are not building a chatbot for information only. We are building a **voice-first public-service navigator**.
- The value is in **routing, simplification, and actionable next steps**, not just answering FAQs.
- We focused on **high-friction government workflows** where confusion creates missed deadlines, repeat visits, and dependence on agents.

## What To Say If Mentors Ask "Why Will This Matter?"

- It reduces unnecessary office visits.
- It supports low-digital-literacy and multilingual users.
- It can work as a front door to multiple departments instead of forcing citizens to understand government structure first.

## What To Say If They Ask "What Next?"

- stronger data integrations with live BBMP and grievance systems
- end-to-end status tracking and reminders
- richer Kannada-first voice optimization
- assisted submission workflows for common service centres

## Final Close

> "Bengaluru Sahayaka shows how voice AI can turn fragmented government services into guided citizen journeys. Instead of asking people to understand the system first, the system adapts to the citizen."
