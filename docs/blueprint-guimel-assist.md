# guimel-assist — Blueprint técnico e funcional (MVP+)

## 1) Especificação funcional
- **Nome público:** Assistente Guimel.
- **Nome interno:** `guimel-assist`.
- **Missão:** qualificar leads de WhatsApp/Instagram para simulação/digitação, sem concluir análise final de crédito.
- **Objetivos comerciais por conversa:**
  1. Identificar intenção/produto.
  2. Triar elegibilidade com perguntas curtas.
  3. Explicar em 1–2 mensagens, sem promessas indevidas.
  4. Solicitar consentimento e coletar dados mínimos.
  5. Gerar `LeadHandoff` estruturado.
  6. Encerrar com próximo passo claro (simular/agendar/retorno).

### Regras mandatórias de conversa
- Tom humano, acolhedor e direto.
- Máximo 1 pergunta por mensagem (2 só se muito simples).
- Confirmar entendimento antes de pedir dado sensível.
- Proibido pedir senha, token, código, gov.br, CVV, credenciais bancárias.
- Proibido pedir foto de documento/cartão no pré-atendimento.
- Se recusa CPF: explicar sem CPF e pedir novamente apenas para simulação.

## 2) Arquitetura front-end e back-end
### Stack escolhida
- **Back-end:** FastAPI + PostgreSQL + Redis + Celery.
- **Front-end:** Next.js (admin panel).
- **Mensageria:** Meta APIs (WhatsApp Cloud API / Instagram Messaging).

### Componentes
- `webhooks`: entrada e verificação Meta.
- `conversations`: contexto, estado e histórico.
- `llm_orchestrator`: prompt, contexto, validação de schema JSON, fallback seguro.
- `leads/handoffs`: qualificação, handoff e fila operacional.
- `followups`: agendamento D+1/D+3/D+7 via Celery + Redis.
- `privacy`: anonimização/exclusão LGPD.
- `audit`: trilha imutável de eventos.
- `admin`: APIs para inbox, detalhe lead, kanban e métricas.

## 3) Modelo de dados
Implementado em `infra/migrations/001_init.sql` com tabelas:
- `users`
- `conversations`
- `messages`
- `leads`
- `lead_data`
- `handoffs`
- `followups`
- `audit_logs`

### Segurança do dado
- `lead_data` separado de `leads`.
- Campos sensíveis armazenados criptografados (`BYTEA`): nome, CPF, nascimento, NIS.
- CPF mascarado em logs e UI (somente final visível).

## 4) Máquina de estados (FSM)
Estados persistidos por conversa:
- `S0_GREETING`
- `S1_PRODUCT_SELECT`
- `S2_QUALIFY`
- `S3_EXPLAIN`
- `S4_CONSENT_AND_MIN_DATA`
- `S5_HANDOFF`
- `S6_FOLLOWUP`

Transições implementadas em `apps/api/app/core/fsm.py`.
- Retomada de conversa mantém estado atual.
- Inatividade D+1/D+3/D+7 envia para `S6_FOLLOWUP`.

## 5) Endpoints/API/Webhooks
### Webhooks
- `POST /webhooks/whatsapp`
- `GET /webhooks/whatsapp/verify`
- `POST /webhooks/instagram`
- `GET /webhooks/instagram/verify`

### Mensageria
- `POST /messages/send`
- `POST /messages/send/batch` (opcional)

### Admin
- `GET /admin/leads`
- `GET /admin/leads/{id}`
- `PATCH /admin/leads/{id}/status`
- `PATCH /admin/leads/{id}/assign`
- `POST /admin/handoffs/{id}/export`
- `GET /admin/conversations/{id}`
- `GET /admin/metrics`

### Privacidade
- `DELETE /privacy/user/{user_id}`
- `POST /privacy/export/{user_id}`

## 6) Painel administrativo
MVP com 5 telas:
1. Inbox/Leads (filtros por produto/canal/status/período + busca nome/CPF mascarado)
2. Detalhe do Lead (timeline, triagem, dados mascarados, copiar handoff)
3. Kanban Comercial (New, Qualified, Waiting Data, Handoff Sent, Closed)
4. Configurações (templates, horários, consentimento, produtos ativos, canais)
5. Métricas (leads por canal/produto, taxa qualificação/handoff, tempo de resposta)

## 7) Prompt e regras de segurança do LLM
- Prompt de sistema implementado em `app/services/llm_orchestrator.py`.
- Resposta obrigatoriamente JSON validada com Pydantic (`LLMResponse`).
- Em JSON inválido: fallback seguro + auditoria + retry controlado.
- Guardrails:
  - bloqueio de pedidos proibidos;
  - sem promessa de aprovação/liberação/taxa fixa;
  - coleta de CPF somente com consentimento explícito.

## 8) Logs, auditoria e LGPD
### Logs
- Estruturados JSON com `correlation_id`, `conversation_id`, `channel`, `state`.
- Eventos: inbound/outbound, latência LLM, handoff, follow-up.

### Auditoria
- Registrar alterações de status, handoff, edição manual, anonimização.
- Tabela dedicada: `audit_logs`.

### LGPD
- Consentimento versionado (`consent_given`, `consent_timestamp`).
- Endpoint de anonimização por `user_id`.
- Retenção configurável e exclusão sob solicitação titular.

---

## Regras de produto (base versionada)
Arquivos em `packages/knowledge/products/*.v1.json` contendo:
- `summary`
- `eligibility_rules`
- `triage_questions`
- `explanation_templates`
- `min_data_fields`
- `handoff_fields`
- `forbidden_asks`
- `objection_templates`

## Templates de mensagens
- Arquivo: `packages/templates/message_templates.v1.json`.
- Inclui abertura, objeções, follow-ups D+1/D+3/D+7 e fechamento comercial.

## Seeds/Demos de conversa
Recomendado criar `infra/seeds/demo_conversations.sql` com 5 leads (INSS, FGTS, CLT, CARTAO, AUXILIO_BRASIL) e objeções de CPF/golpe/liberação.

## Estrutura de projeto
- `/apps/api`
- `/apps/admin`
- `/packages/shared`
- `/packages/knowledge`
- `/packages/templates`
- `/infra`
- `/docs`

## Checklist de MVP executável
1. Subir Postgres/Redis via `docker-compose`.
2. Rodar migração `001_init.sql`.
3. Iniciar API FastAPI.
4. Configurar webhooks Meta e segredo de assinatura.
5. Habilitar worker Celery para follow-ups.
6. Testar fluxo E2E por produto e validar geração de `LeadHandoff`.
