# Next Round Script

## Exact Spoken Opening

Hello mentors, we are presenting **Bengaluru Sahayaka**, a voice-first AI assistant for Bengaluru local government services.

The problem we are solving is simple: citizens should not need to understand government structure, legal jargon, or department routing just to complete basic civic tasks.

Our system handles three high-friction journeys:

1. Birth and death certificates
2. Property tax guidance
3. Public grievance routing and follow-up

Instead of forms and confusion, the citizen speaks naturally, and the assistant guides them to the right next step.

## Exact Demo Flow

### Host

I’ll start with the host assistant.

> "I need help with a birth certificate."

This shows the host acting as the entry point and routing the citizen to the right specialist.

### Certificates

Now I’ll show a late registration use case.

> "My baby was born at home 45 days ago. What do I need to do?"

Then:

> "What documents do I need?"

Then:

> "Can you help me with the affidavit?"

Say this after the output:

This is important because citizens usually miss deadlines, don’t know the correct process, and often rely on middlemen for affidavit drafting and documentation.

### Property Tax

Now I’ll switch to property tax.

> "I have a 1200 square foot property in B zone with A-Khata. Can you estimate my tax and tell me the payment options?"

Say this after the output:

Here the assistant converts a confusing tax problem into a plain-language estimate, explains rebate logic, and tells the citizen what to keep ready before payment.

### Grievances

Now I’ll show a complaint-routing flow.

> "There is a pothole and drainage issue near my street in Jayanagar. Where should I complain and how do I track it?"

Say this after the output:

This is where the assistant is especially useful because real complaints often span multiple departments. Instead of making the citizen guess, we classify, route, and explain the escalation path.

## Exact Closing

To summarize, Bengaluru Sahayaka turns fragmented civic workflows into guided voice journeys.

It helps citizens understand what applies to them, what documents they need, where they should go, and what they should do next.

Our goal is not just answering questions. Our goal is reducing friction, repeat visits, and confusion in public service delivery.

## If They Ask Why This Can Win

Say:

We focused on a problem with real public impact, high usability value, and a clear path to deployment. The same architecture can support multiple government services while staying accessible to users who are not comfortable with portals or forms.

## If Live Demo Breaks

Say:

I’ll quickly show the backend demo scenarios endpoint and the structured outputs that power the same voice flow.

Then open:

- `/health`
- `/demo/scenarios`

And say:

These are the service journeys and structured outputs that the voice orchestration layer uses during the live call flow.
