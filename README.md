# Bot de sorteio para Discord (Python)

Este exemplo cria um bot simples com comandos slash para:

- iniciar um sorteio (`/iniciar_sorteio`)
- entrar no sorteio (`/entrar_sorteio`)
- encerrar o sorteio e escolher o vencedor (`/encerrar_sorteio`)

## 1) Criar aplicação/bot no Discord

1. Acesse https://discord.com/developers/applications
2. Clique em **New Application** e dê um nome.
3. Em **Bot**, clique em **Add Bot**.
4. Copie o token do bot e guarde com segurança.
5. Em **Privileged Gateway Intents**, habilite **Server Members Intent**.

## 2) Configurar permissões e convidar o bot

Em **OAuth2 > URL Generator**:

- Scopes: `bot`, `applications.commands`
- Bot Permissions: pelo menos `Send Messages`, `Read Message History`, `View Channels`

Use a URL gerada para convidar o bot para o servidor.

## 3) Instalar dependências

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements-discord-bot.txt
```

## 4) Rodar o bot

```bash
export DISCORD_TOKEN="SEU_TOKEN_AQUI"
python discord_sorteio_bot.py
```

Quando o bot iniciar, os comandos slash serão sincronizados automaticamente.

## Observações

- Este exemplo mantém o sorteio em memória (reiniciar o processo limpa os dados).
- Para produção, use banco de dados (SQLite/PostgreSQL) e controle de permissões
  (por exemplo, permitir encerrar sorteio apenas para admins).
