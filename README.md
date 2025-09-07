flowchart TD
    A[Slack Channel: sre-lending-alerts] -->|Alert Message| B[Slack Bot: Chillbot]
    B -->|User mentions /chart| C[Bot Server]

    C -->|Send alert + query + metadata| D[LLM - Groq API]
    D -->|Dashboard UID + Panel ID| C

    C -->|Fetch chart| E[Grafana Server]
    E -->|Chart Image| C

    C -->|Post chart in thread| A
