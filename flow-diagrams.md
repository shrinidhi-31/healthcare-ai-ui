# MedVerify Flow Diagrams

---

## 1. High-Level System Architecture

```mermaid
graph TD
    User["👤 User (WhatsApp / Web)"]
    API["FastAPI Layer\n(api/)"]
    Orch["Orchestrator\n(services/orchestrator.py)"]
    SM["Session Manager\n(services/session_manager.py)"]
    Redis[("Redis\nsession:{user_id}")]
    FR["Flow Registry\n(services/flow_registry.py)"]
    SF["Start Flow"]
    SyF["Symptom Flow"]
    RF["Report Flow"]
    DF["Doctor Flow"]
    EF["Emergency Flow"]
    Bot["Bot Response"]
    Alert["Alert Service\n(services/alert_service.py)"]
    Dash["Admin Dashboard"]

    User -->|Incoming message| API
    API --> Orch
    Orch --> SM
    SM <-->|Read / Write| Redis
    SM --> FR
    FR --> SF
    FR --> SyF
    FR --> RF
    FR --> DF
    FR --> EF
    EF --> Alert
    Alert --> Dash
    SF & SyF & RF & DF & EF --> Bot
    Bot -->|Reply| User
```

---

## 2. Orchestrator Processing Pipeline

```mermaid
sequenceDiagram
    participant W as WhatsApp Webhook
    participant O as Orchestrator
    participant SM as Session Manager
    participant Redis
    participant FR as Flow Registry
    participant F as Active Flow

    W->>O: Incoming message (user_id, text)
    O->>SM: get_session(user_id)
    SM->>Redis: GET session:{user_id}
    Redis-->>SM: SessionState (or None)
    SM-->>O: SessionState

    O->>FR: resolve_flow(session.flow)
    FR-->>O: Flow instance

    O->>F: execute(session, message)
    F-->>O: (updated_session, reply_text)

    O->>SM: save_session(updated_session)
    SM->>Redis: SET session:{user_id} EX 3600

    O-->>W: BotResponse(reply_text)
```

---

## 3. Start Flow

```mermaid
flowchart TD
    Start([User sends any message])
    Menu["Send main menu:\n1. Symptom Assessment\n2. Upload Report\n3. Find Doctor"]
    Choice{User selects option}
    ToSymptom["Set flow = symptoms\nstep = 0"]
    ToReport["Set flow = report\nstep = 0"]
    ToDoctor["Set flow = doctor\nstep = 0"]
    Invalid["Re-send menu\n(invalid input)"]

    Start --> Menu
    Menu --> Choice
    Choice -->|"1"| ToSymptom
    Choice -->|"2"| ToReport
    Choice -->|"3"| ToDoctor
    Choice -->|other| Invalid
    Invalid --> Choice
```

---

## 4. Symptom Flow

```mermaid
flowchart TD
    S0["Step 0: Ask main symptom"]
    S1["Step 1: Ask duration"]
    S2["Step 2: Ask age"]
    RF{"Red flag\ndetected?"}
    EF["Trigger Emergency Flow"]
    S3["Step 3: Ask additional symptoms"]
    S4["Step 4: Generate summary\n& recommendations"]
    Done([End — return to menu])

    S0 --> S1
    S1 --> S2
    S2 --> RF
    RF -->|Yes — chest pain, seizure\nstroke, unconsciousness\nshortness of breath\nheavy bleeding| EF
    RF -->|No| S3
    S3 --> S4
    S4 --> Done
```

**Red Flag Keywords**

| Keyword | Severity |
|---------|----------|
| chest pain | HIGH |
| shortness of breath | HIGH |
| seizure | HIGH |
| unconsciousness | HIGH |
| heavy bleeding | HIGH |
| stroke symptoms | HIGH |

---

## 5. Emergency Flow

```mermaid
flowchart TD
    Trigger([Red flag detected in Symptom Flow])
    Create["Create Alert\n(alert_service.create_alert)"]
    Store["Store alert in Redis / DB"]
    Notify["Push alert to Admin Dashboard"]
    Advice["Send emergency advice to user:\n• Call 112 immediately\n• Do not be alone\n• First aid tips"]
    Done([Session ends / reset to start])

    Trigger --> Create
    Create --> Store
    Store --> Notify
    Notify --> Advice
    Advice --> Done
```

```mermaid
sequenceDiagram
    participant SyF as Symptom Flow
    participant EF as Emergency Flow
    participant AS as Alert Service
    participant Redis
    participant Dash as Admin Dashboard
    participant User

    SyF->>EF: trigger(user_id, symptoms)
    EF->>AS: create_alert(user_id, severity=HIGH, reason, symptoms)
    AS->>Redis: LPUSH alerts:{user_id}
    AS-->>EF: Alert created
    EF->>Dash: WebSocket / SSE push (new alert)
    EF->>User: Emergency guidance message
```

---

## 6. Report Flow

```mermaid
flowchart TD
    S0["Step 0: Ask user to upload report\n(PDF or image)"]
    Recv["Receive media message\n(WhatsApp media URL)"]
    OCR["OCR Service:\nextract text from image/PDF"]
    Sum["Summarizer Service:\nAI-generated patient-friendly summary"]
    Reply["Send summary to user"]
    Done([End — return to menu])

    S0 --> Recv
    Recv --> OCR
    OCR --> Sum
    Sum --> Reply
    Reply --> Done
```

> **Note:** OCR and Summarizer services are planned as future AI modules. The flow is stubbed pending implementation.

---

## 7. Doctor Flow

```mermaid
flowchart TD
    S0["Step 0: Ask for city"]
    S1["Step 1: Ask for specialization"]
    Search["Query doctor registry\n(city + specialization)"]
    Found{"Results found?"}
    Send["Send doctor list:\n• Name\n• Hospital\n• Contact"]
    NoResult["Notify: No doctors found\nSuggest alternative city"]
    Done([End — return to menu])

    S0 --> S1
    S1 --> Search
    Search --> Found
    Found -->|Yes| Send
    Found -->|No| NoResult
    NoResult --> S0
    Send --> Done
```

---

## 8. Session State Machine

```mermaid
stateDiagram-v2
    [*] --> start : New user / no session
    start --> symptoms : User selects 1
    start --> report : User selects 2
    start --> doctor : User selects 3

    symptoms --> emergency : Red flag detected
    symptoms --> start : Flow complete

    emergency --> start : Advice sent

    report --> start : Summary delivered

    doctor --> start : Results sent
    doctor --> doctor : No results → retry city

    start --> start : Invalid input (re-show menu)
```

---

## 9. Alert Lifecycle

```mermaid
stateDiagram-v2
    [*] --> open : Emergency flow creates alert
    open --> acknowledged : Admin sees & acknowledges
    acknowledged --> resolved : Admin marks resolved
    open --> resolved : Direct resolution (skip ack)
    resolved --> [*]
```
