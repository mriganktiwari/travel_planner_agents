## Product Statement

The application helps users create an initial travel plan based on their origin, destination preferences, duration, budget, number of travellers, and interests.

It produces planning guidance only. It does not make bookings or guarantee live prices or availability.

## Supported User Inputs

The system should understand the following information when present:

- origin;
- destination;
- travel dates;
- trip duration;
- number of travellers;
- total budget;
- travel interests;
- pace preference;
- special constraints.

A user should not be required to provide every field in a structured form. The root agent should extract the information from natural language.

## Missing Information Policy

The system should ask a follow-up question only when missing information prevents a useful itinerary.

For the MVP:

- duration is required;
- origin is useful but may be marked as unknown;
- destination may be recommended by the system;
- exact dates are optional;
- budget is optional but strongly preferred;
- number of travellers defaults to one only when clearly stated as an assumption.

## Required Output Sections

Every complete trip plan should contain:

1. Request summary
2. Assumptions
3. Destination guidance
4. Day-by-day itinerary
5. Estimated budget
6. Practical notes
7. Price and availability disclaimer

## Output Quality Rules

The system should:

- preserve the stated duration;
- preserve the stated budget;
- avoid presenting estimates as confirmed prices;
- avoid claiming bookings have been made;
- group activities sensibly;
- avoid obviously unrealistic schedules;
- show assumptions explicitly;
- maintain context during follow-up messages.

## Follow-up Behaviour

The user should be able to say:

- make day two more relaxed;
- reduce the hotel budget;
- replace museums with food experiences;
- add one extra day;
- make the plan suitable for children.

The system should modify the existing trip rather than creating an unrelated plan.

## Out-of-Scope Behaviour

The system should not:

- complete payments;
- book flights or hotels;
- claim real-time availability without a live data source;
- provide visa or legal advice as guaranteed fact;
- hide uncertainty about prices;
- store sensitive payment information.

## Success Criteria

The MVP is successful when:

- a user can request a trip in natural language;
- the correct agents participate;
- the response contains the required sections;
- follow-up changes preserve the existing session;
- two separate sessions do not affect each other;
- the application works through Streamlit and FastAPI.
