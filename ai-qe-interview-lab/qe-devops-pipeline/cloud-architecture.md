# Cloud Reference Architecture — AI QE Platform

How the lab projects map to managed cloud services at enterprise scale.
Patterns are cloud-agnostic; the tables map them to AWS (primary), Azure, GCP.

## AWS reference architecture

```
                            ┌─────────────────────────────────────────┐
                            │                 VPC                     │
 CI (GitHub Actions ─────▶  │  ┌──────────┐      ┌────────────────┐   │
 OIDC, no static keys)      │  │ ECS/     │      │ Step Functions │   │
                            │  │ Lambda   │◀────▶│ (agent         │   │
 Engineers (SSO/IAM) ────▶  │  │ (agents, │      │  orchestration)│   │
                            │  │  MCP srv)│      └────────────────┘   │
                            │  └────┬─────┘                           │
                            │       │ VPC endpoints (no public net)   │
                            │  ┌────▼─────┐  ┌───────────┐  ┌──────┐  │
                            │  │ Bedrock  │  │OpenSearch │  │ S3   │  │
                            │  │ (LLM +   │  │(vectors + │  │(docs,│  │
                            │  │ Titan    │  │ hybrid    │  │ arti-│  │
                            │  │ embed)   │  │ search)   │  │facts)│  │
                            │  └──────────┘  └───────────┘  └──────┘  │
                            │  Secrets Manager · CloudWatch · IAM     │
                            └─────────────────────────────────────────┘
```

| Lab component | AWS service | Why |
|---|---|---|
| LLM calls (qe-copilot llm_client) | Bedrock | Managed models, IAM auth, no keys in code, Guardrails |
| Embeddings + vector store (ChromaDB) | Bedrock Titan Embeddings + OpenSearch Serverless | Hybrid keyword+vector search, scales past local stores |
| Incident/doc corpus + artifacts | S3 (+ lifecycle policies) | Cheap, versioned, event-driven ingest triggers |
| Agent orchestration (LangGraph) | Step Functions + Lambda | Retries, timeouts, audit per state - LangGraph's ops story, managed |
| MCP servers | ECS Fargate (or Lambda for stdio-wrapped) | Long-lived tool endpoints with task-role IAM |
| ML training/registry (ml-qe-pipeline) | SageMaker (training jobs + Model Registry) | Same champion/challenger pattern, managed lineage |
| Scheduled retraining (retrain.py) | EventBridge Scheduler -> SageMaker Pipeline | The cron for the retraining workflow |
| Eval gates in CI | CodeBuild step or GitHub Actions OIDC role | Same exit-code contract |
| Secrets (API keys, tokens) | Secrets Manager | Rotation, audit, never in prompts or env files |
| Observability (token cost, latency, eval trends) | CloudWatch metrics + dashboards + alarms | Cost creep and quality decay become alerts |

## Azure / GCP mapping

| Capability | AWS | Azure | GCP |
|---|---|---|---|
| Managed LLM | Bedrock | Azure OpenAI | Vertex AI |
| Vector search | OpenSearch | AI Search | Vertex AI Vector Search |
| Object storage | S3 | Blob Storage | GCS |
| Workflow orchestration | Step Functions | Durable Functions / Logic Apps | Workflows |
| Containers | ECS Fargate | Container Apps | Cloud Run |
| ML platform | SageMaker | Azure ML | Vertex AI |
| Secrets | Secrets Manager | Key Vault | Secret Manager |
| CI/CD | CodePipeline / GH Actions | Azure DevOps | Cloud Build |
| Data warehouse (test telemetry) | Redshift/Athena | Synapse | BigQuery |

## Security & governance (the "scalable, secure, governed" bullet)

1. **Identity, not keys:** CI assumes an IAM role via GitHub OIDC - zero static
   credentials in the repo. Humans come through SSO. Agents get task roles.
2. **Least privilege per tool:** each MCP server's role can reach exactly its
   backing service (the BigQuery-reader role cannot touch S3).
3. **Network containment:** Bedrock/OpenSearch via VPC endpoints; AI traffic
   never crosses the public internet.
4. **Data governance:** PII redaction lambda in the ingest path (the
   embedding_pipeline.py stage 2 pattern); residency-sensitive workloads route
   to local models (the Ollama switch) or in-region endpoints.
5. **Cost governance:** Bedrock model-invocation logging + CloudWatch alarms on
   token spend per pipeline; batch/cached paths for bulk triage.
6. **Auditability:** every agent tool call logged (who/what/inputs hash);
   model registry + prompt versions in Git = full change lineage.

## Environment strategy

| Env | Purpose | AI posture |
|---|---|---|
| dev | Engineers + local Ollama | Anything goes, synthetic data only |
| staging | Full pipeline rehearsal | Cloud models, redacted data, all gates enforced |
| prod | Live QE platform | Advisory-only actions, human release authority, full audit |
