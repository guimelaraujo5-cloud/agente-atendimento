# guimel-assist

Implementação MVP do agente comercial omnichannel **Assistente Guimel** (WhatsApp + Instagram), focado em qualificação e conversão para simulação/digitação.

## O que já está implementado
- API FastAPI com webhooks, mensageria, endpoints admin e privacidade.
- FSM de atendimento (`S0..S6`).
- Orquestrador LLM com prompt de sistema e fallback seguro.
- Base de conhecimento versionada por produto.
- Templates de mensagens (abertura, objeções, follow-up, fechamento).
- Migração SQL inicial com as tabelas obrigatórias.

## Subir localmente (rápido)
```bash
./scripts/bootstrap.sh
./scripts/run_api.sh
```

API disponível em `http://localhost:8000`.

## Testes
```bash
python -m unittest discover -s tests
```

## Próximos passos para produção
1. Trocar storage in-memory por repositórios PostgreSQL.
2. Integrar Redis + Celery para follow-up agendado.
3. Integrar Meta Cloud API real (assinatura webhook, envio real e retries).
4. Implementar autenticação RBAC no painel admin.
5. Ativar criptografia de dados sensíveis em `lead_data`.

## Documentação
- Blueprint técnico: `docs/blueprint-guimel-assist.md`
- Guia de implementação operacional: `docs/como-implementar-e-rodar.md`
