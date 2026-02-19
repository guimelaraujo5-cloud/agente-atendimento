# guimel-assist

Blueprint e esqueleto de MVP para agente comercial omnichannel (WhatsApp + Instagram) do correspondente bancário Guimel.

## Estrutura
- `apps/api`: FastAPI + FSM + orquestrador LLM.
- `apps/admin`: reservado para painel Next.js.
- `packages/knowledge`: regras versionadas por produto.
- `packages/templates`: templates de conversa e follow-up.
- `infra`: docker-compose, env, migrações SQL.
- `docs`: blueprint técnico completo.
- `tests`: suíte unitária e contratos de integração/e2e.

## Quick start
```bash
cd infra && docker compose up -d
python -m unittest discover -s tests
```
