# Travel Agent MVP Plan

## 1. Project Goal

Build a small but complete multi-agent travel-planning application using:

- Google Agent Development Kit (ADK)
- Gemini through Vertex AI
- A single FastAPI backend
- A simple Streamlit interface
- SQLite for local development
- Optional containerization after the local MVP works

The MVP should allow a user to request a trip plan and refine it through follow-up messages.

Example:

> Plan a four-day trip to Goa from Delhi for two people under ₹40,000. We prefer beaches, local food, and a relaxed schedule.

The application should return:

- interpreted travel requirements;
- assumptions and missing-information notes;
- destination guidance;
- a day-by-day itinerary;
- an estimated budget breakdown;
- practical travel notes;
- a clear warning that prices are estimates.

---

# 2. MVP Scope

## Included

- One root travel agent
- One destination research agent
- One itinerary planning agent
- Basic deterministic tools
- Multi-turn session handling
- FastAPI backend
- Streamlit chat interface
- Local SQLite storage
- Local execution using Gemini through Vertex AI
- Basic testing and documentation

## Excluded

- Real booking
- Payments
- Authentication
- Live flight inventory
- Live hotel inventory
- Production-grade maps integration
- Complex agent-to-agent networking
- Multiple independently deployed agent services
- Production-grade observability
- GKE deployment during the first two-day build

---

# 3. Mental Model

```text
Streamlit UI
     |
     | HTTP
     v
FastAPI Backend
     |
     v
ADK Runner
     |
     v
Root Travel Agent
     |
     +-- Destination Research Agent
     |
     +-- Itinerary Planning Agent
     |
     +-- Deterministic Tools
     |
     v
Gemini through Vertex AI

SQLite stores local sessions and saved trip data.
```

Important distinction:

- An agent is a logical reasoning component.
- FastAPI is the application interface.
- A container packages the application.
- GKE runs and scales containers.
- These are separate architectural layers.

For the MVP, all agents should run inside one FastAPI backend process.

---

# 4. Recommended Project Structure

```text
travel-agent-mvp/
|
|-- plan.md
|-- README.md
|-- .env.example
|-- .gitignore
|
|-- docs/
|   |-- product-contract.md
|   |-- architecture.md
|   |-- decisions.md
|   `-- sample-conversations.md
|
|-- backend/
|   |-- api/
|   |   |-- main.py
|   |   `-- schemas.py
|   |
|   |-- travel_agent/
|   |   |-- root_agent.py
|   |   |-- destination_agent.py
|   |   |-- itinerary_agent.py
|   |   `-- prompts/
|   |
|   |-- tools/
|   |   |-- budget.py
|   |   |-- duration.py
|   |   `-- destination_data.py
|   |
|   |-- services/
|   |   |-- agent_runner.py
|   |   `-- session_manager.py
|   |
|   |-- storage/
|   |   |-- database.py
|   |   `-- models.py
|   |
|   `-- tests/
|       |-- evaluation_cases.md
|       `-- test_sessions.py
|
|-- frontend/
|   `-- streamlit_app.py
|
|-- data/
|   |-- travel_agent.db
|   `-- destinations.json
|
`-- requirements.txt
```

The filenames are recommendations. They can be simplified while learning.

---

# 5. Where to Add the Step 1 Product Contract

The main product contract should be created here:

```text
docs/product-contract.md
```

This file should define the expected behavior of the application without depending on implementation details.

It becomes the reference for:

- agent prompts;
- API request and response models;
- test cases;
- Streamlit input fields;
- expected output quality;
- decisions about what is inside or outside the MVP.

Do not place the product contract only inside an agent prompt. Agent prompts are implementation files and may change. The contract should remain a stable, human-readable product document.

## Supporting Contract Files

Use the following progression:

### 1. Human-readable product contract

```text
docs/product-contract.md
```

Defines what the application accepts, returns, and guarantees.

### 2. Golden evaluation examples

```text
backend/tests/evaluation_cases.md
```

Contains representative user prompts and the expected characteristics of good answers.

### 3. API-level contract

```text
backend/api/schemas.py
```

Added later when FastAPI is introduced. It converts the product contract into request and response data structures.

### 4. Agent-level instructions

```text
backend/travel_agent/prompts/
```

Added after the product contract is stable. Each agent prompt should implement only its assigned responsibility.

The product contract should be the source of truth. API schemas and agent prompts should reflect it.

---

# 6. Starting Template for `docs/product-contract.md`

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

---

# 7. Five Good Starting Evaluation Prompts

Add these to:

```text
backend/tests/evaluation_cases.md
```

## Case 1: Fully specified request

> Plan a four-day Goa trip from Delhi for two people under ₹40,000. We like beaches, local food, and a relaxed pace.

Expected behaviour:

- no unnecessary clarification;
- four-day itinerary;
- estimated transport, stay, food, and activities;
- relaxed schedule;
- budget-aware recommendations.

## Case 2: Destination not specified

> Suggest and plan a three-day trip from Bengaluru under ₹25,000 for one person. I enjoy nature and quiet places.

Expected behaviour:

- destination agent recommends a suitable destination;
- assumptions are shown;
- itinerary agent uses the selected destination;
- estimated budget stays close to the limit.

## Case 3: Missing essential information

> Plan a trip to Jaipur.

Expected behaviour:

- ask for duration;
- optionally ask for origin or budget;
- do not fabricate a complete detailed itinerary immediately.

## Case 4: Unrealistic budget

> Plan a seven-day international trip from Mumbai for two people under ₹20,000.

Expected behaviour:

- identify the constraint as unrealistic;
- avoid pretending the trip is feasible;
- suggest reducing duration, changing destination, or increasing budget.

## Case 5: Follow-up modification

Initial request:

> Plan a five-day Kerala trip for a family of four.

Follow-up:

> Make day three less tiring and reduce expensive activities.

Expected behaviour:

- preserve the existing trip;
- modify day three;
- update the estimated budget;
- avoid regenerating an unrelated itinerary.

---

# 8. Two-Day Build Plan

## Day 1: Agentic System

### Step 1 — Define the Product Contract

Create:

```text
docs/product-contract.md
backend/tests/evaluation_cases.md
```

Tasks:

- write the input expectations;
- define required output sections;
- define assumptions and clarification rules;
- define out-of-scope behaviour;
- add five evaluation prompts.

Completion criteria:

- you can judge whether an answer is acceptable without looking at the implementation;
- each evaluation prompt has an expected behaviour;
- scope is narrow enough for two days.

### Step 2 — Set Up the Local Environment

Tasks:

- create the repository and folder structure;
- create a Python virtual environment;
- configure the GCP project;
- enable Vertex AI;
- authenticate locally;
- configure the Gemini model;
- verify that ADK can call Gemini.

Initial test:

```text
User prompt -> one basic ADK agent -> Gemini response
```

Do not add FastAPI or Streamlit yet.

Completion criteria:

- one basic travel-related prompt returns successfully;
- no service-account key is committed;
- model and project configuration are read from environment settings.

### Step 3 — Build the Destination Agent

Responsibilities:

- recommend a destination when one is missing;
- explain destination suitability;
- identify key attractions;
- identify broad seasonal or logistical considerations;
- produce a destination brief for another agent.

It should not create the full day-by-day itinerary.

Completion criteria:

- the agent produces a concise destination brief;
- it does not attempt booking;
- it distinguishes assumptions from facts;
- it stays within its assigned role.

### Step 4 — Build the Itinerary Agent

Responsibilities:

- consume the travel requirements;
- consume the destination brief;
- create the correct number of days;
- group activities logically;
- respect interests and pace;
- provide estimated daily costs.

Completion criteria:

- trip duration is correct;
- the itinerary is not overcrowded;
- estimates are labelled clearly;
- the budget is considered.

### Step 5 — Build the Root Travel Agent

Responsibilities:

1. interpret the user request;
2. extract constraints;
3. identify missing information;
4. delegate destination work;
5. delegate itinerary work;
6. combine the outputs;
7. present one coherent answer.

Recommended design:

- root agent as the single entry point;
- destination and itinerary agents as sub-agents;
- controlled parent-child delegation;
- no separate network services.

Completion criteria:

- one user request triggers the appropriate agents;
- the final answer follows the product contract;
- the user sees one coherent response, not raw agent outputs.

### Step 6 — Add Essential Tools

Start only with deterministic tools:

- trip duration validation;
- basic budget allocation;
- currency formatting;
- a small local destination dataset.

Possible budget categories:

- transport;
- accommodation;
- food;
- local transport;
- activities;
- contingency.

Do not add live flight or hotel APIs.

Completion criteria:

- calculations are repeatable;
- agents do not invent basic arithmetic;
- tool failures are handled gracefully.

### End-of-Day-1 Checkpoint

The following should work locally:

```text
User prompt
   ->
Root agent
   ->
Destination agent
   ->
Itinerary agent
   ->
Structured trip response
```

Run all five evaluation prompts manually.

---

## Day 2: Application Layer

### Step 7 — Add Sessions and SQLite

Store:

- session ID;
- conversation events;
- session state;
- optionally saved itinerary output.

Use SQLite only for local development.

Tasks:

- create a new session;
- retrieve an existing session;
- preserve context across messages;
- keep sessions isolated.

Completion criteria:

- “make day two cheaper” updates the same trip;
- two users or browser sessions do not share context;
- restarting the application does not unexpectedly mix sessions.

### Step 8 — Add FastAPI

FastAPI should be a thin interface around the agent system.

Minimum endpoints:

```text
GET  /health
POST /sessions
POST /chat
```

Conceptual request for `/chat`:

- session ID;
- user message.

Conceptual response:

- session ID;
- assistant response;
- success or error status.

Do not add streaming initially.

Completion criteria:

- an API client can create a session;
- multiple messages can be sent to the session;
- the backend returns useful errors;
- the API does not contain agent business logic.

### Step 9 — Add Streamlit

Streamlit responsibilities:

- create or retain a session ID;
- display the conversation;
- send user messages to FastAPI;
- show loading state;
- show errors clearly;
- provide sample prompts;
- allow a new conversation.

Streamlit should not call Gemini or ADK directly.

Completion criteria:

- the full flow works from the browser;
- a friend can understand how to use it;
- follow-up messages maintain context.

### Step 10 — Test the Full MVP

Test:

- fully specified request;
- missing destination;
- missing duration;
- unrealistic budget;
- follow-up modification;
- model or tool failure;
- two independent sessions;
- application restart.

Evaluate:

- correct agent responsibility;
- constraint preservation;
- output consistency;
- session continuity;
- clear uncertainty;
- acceptable response time.

### Step 11 — Add Basic Documentation

Update `README.md` with:

- project purpose;
- architecture;
- local setup;
- required GCP configuration;
- how to run the backend;
- how to run Streamlit;
- known limitations;
- example prompts.

Add a simple architecture diagram to:

```text
docs/architecture.md
```

### End-of-Day-2 Checkpoint

A user should be able to:

1. open the Streamlit application;
2. request a trip;
3. receive a structured itinerary;
4. ask a follow-up question;
5. retain the conversation context;
6. start a new independent session.

---

# 9. Recommended Data Storage

## During Development

| Data | Storage |
|---|---|
| ADK sessions | SQLite |
| Saved itineraries | SQLite |
| Destination reference data | JSON |
| Temporary intermediate values | Session state or process memory |
| Configuration | Environment variables |
| Secrets | Local `.env`, excluded from Git |
| Uploaded files | Not supported initially |

## Later on GKE

| Local MVP | GKE Version |
|---|---|
| SQLite | Cloud SQL PostgreSQL |
| Local JSON | Container image or Cloud Storage |
| `.env` | Secret Manager |
| Local authentication | Workload Identity |
| Local Streamlit | Separate GKE Deployment |
| Local FastAPI | Separate GKE Deployment |

Do not use a pod's local filesystem for important production data.

---

# 10. Suggested Implementation Order

Follow this order strictly:

1. Product contract
2. Evaluation prompts
3. One basic ADK agent
4. Destination agent
5. Itinerary agent
6. Root-agent orchestration
7. Deterministic tools
8. Session persistence
9. FastAPI
10. Streamlit
11. Docker
12. GKE

Avoid beginning with Kubernetes, containers, or UI. They can hide problems in the core agent design.

---

# 11. Definition of Done

The MVP is complete when:

- the root travel agent is the single entry point;
- at least two specialist agents participate;
- the response follows the product contract;
- duration, budget, travellers, and interests are preserved;
- estimates are labelled;
- follow-up messages update the existing plan;
- SQLite keeps sessions separate;
- FastAPI exposes the system;
- Streamlit provides a usable interface;
- all five evaluation prompts have been tested;
- the README explains how to run the application.

---

# 12. Recommended First Action

Create only these files first:

```text
travel-agent-mvp/
|-- plan.md
|-- docs/
|   `-- product-contract.md
`-- backend/
    `-- tests/
        `-- evaluation_cases.md
```

Then:

1. copy the contract template from this plan into `docs/product-contract.md`;
2. copy the five evaluation prompts into `backend/tests/evaluation_cases.md`;
3. edit them until they match the exact travel assistant you want to build;
4. do not write agent code until these documents feel clear.

The best initial milestone is not “the agent responds.”

It is:

> Given a sample user request, I can clearly state what information the application should extract, which agent should handle each responsibility, and what a successful final response must contain.
