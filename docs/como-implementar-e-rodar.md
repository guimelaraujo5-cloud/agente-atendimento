# Como implementar esse projeto e fazer funcionar

## 1) Pré-requisitos
- Python 3.10+
- Docker e Docker Compose
- Conta Meta Developer (WhatsApp Cloud API + Instagram Messaging)

## 2) Infra local
Suba PostgreSQL e Redis:

```bash
cd infra
docker compose up -d
cd ..
```

## 3) API local
```bash
./scripts/bootstrap.sh
./scripts/run_api.sh
```

Valide:
```bash
curl http://localhost:8000/health
```

## 4) Aplicar migração (manual no MVP)
Execute o SQL `infra/migrations/001_init.sql` no PostgreSQL.

## 5) Configurar webhooks Meta
- WhatsApp webhook: `POST /webhooks/whatsapp`
- Instagram webhook: `POST /webhooks/instagram`
- Verificação:
  - `GET /webhooks/whatsapp/verify`
  - `GET /webhooks/instagram/verify`

## 6) Fluxo funcional fim-a-fim (MVP)
1. Mensagem entra no webhook.
2. Conversa é contextualizada por `conversation_id + channel + user_id`.
3. FSM avança conforme triagem/consentimento/dados mínimos.
4. Orquestrador LLM gera resposta JSON válida.
5. Sistema responde via endpoint de envio e persiste histórico.
6. Quando pronto, gera `LeadHandoff` e envia para fila operacional.

## 7) Como evoluir do MVP para produção
- Persistência:
  - Repositórios SQL para `users`, `conversations`, `messages`, `leads`, `lead_data`, `handoffs`, `followups`, `audit_logs`.
- Segurança:
  - Criptografia de CPF/NIS/nascimento/nome.
  - Máscara de CPF nos logs.
  - Consentimento explícito antes de CPF.
  - Assinatura/verificação de webhook Meta.
- Escala:
  - Filas Celery para follow-up D+1/D+3/D+7.
  - Rate limiting por `user_id` e por `channel`.
- Operação:
  - Dashboard admin (inbox, detalhe, kanban, métricas).
  - Métricas de conversão por produto e abandono por estado FSM.

## 8) Comandos úteis
```bash
# testes unitários
python -m unittest discover -s tests

# health
curl http://localhost:8000/health

# métricas mvp
curl http://localhost:8000/admin/metrics
```
