import os
import random
from dataclasses import dataclass, field

import discord
from discord import app_commands
from discord.ext import commands


@dataclass
class Sorteio:
    premio: str
    participantes: set[int] = field(default_factory=set)
    ativo: bool = True


intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
arvore = bot.tree
sorteio_atual: Sorteio | None = None


@bot.event
async def on_ready() -> None:
    synced = await arvore.sync()
    print(f"Bot conectado como {bot.user}.")
    print(f"{len(synced)} comando(s) slash sincronizado(s).")


@arvore.command(name="iniciar_sorteio", description="Inicia um novo sorteio")
@app_commands.describe(premio="Nome do prêmio")
async def iniciar_sorteio(interaction: discord.Interaction, premio: str) -> None:
    global sorteio_atual

    if sorteio_atual and sorteio_atual.ativo:
        await interaction.response.send_message(
            "Já existe um sorteio ativo. Use /encerrar_sorteio antes de iniciar outro.",
            ephemeral=True,
        )
        return

    sorteio_atual = Sorteio(premio=premio)
    await interaction.response.send_message(
        f"🎉 Sorteio iniciado!\nPrêmio: **{premio}**\n"
        "Use **/entrar_sorteio** para participar.",
    )


@arvore.command(name="entrar_sorteio", description="Entra no sorteio ativo")
async def entrar_sorteio(interaction: discord.Interaction) -> None:
    if not sorteio_atual or not sorteio_atual.ativo:
        await interaction.response.send_message(
            "Não há sorteio ativo no momento.",
            ephemeral=True,
        )
        return

    usuario_id = interaction.user.id
    if usuario_id in sorteio_atual.participantes:
        await interaction.response.send_message(
            "Você já está participando deste sorteio.",
            ephemeral=True,
        )
        return

    sorteio_atual.participantes.add(usuario_id)
    await interaction.response.send_message(
        f"✅ {interaction.user.mention} entrou no sorteio de **{sorteio_atual.premio}**!"
    )


@arvore.command(name="encerrar_sorteio", description="Encerra o sorteio e sorteia um vencedor")
async def encerrar_sorteio(interaction: discord.Interaction) -> None:
    global sorteio_atual

    if not sorteio_atual or not sorteio_atual.ativo:
        await interaction.response.send_message(
            "Não há sorteio ativo para encerrar.",
            ephemeral=True,
        )
        return

    if not sorteio_atual.participantes:
        sorteio_atual.ativo = False
        await interaction.response.send_message(
            "Sorteio encerrado sem participantes.",
            ephemeral=True,
        )
        return

    vencedor_id = random.choice(list(sorteio_atual.participantes))
    vencedor = interaction.guild.get_member(vencedor_id) if interaction.guild else None
    sorteio_atual.ativo = False

    if vencedor:
        mensagem_vencedor = vencedor.mention
    else:
        mensagem_vencedor = f"<@{vencedor_id}>"

    await interaction.response.send_message(
        f"🏆 Sorteio encerrado!\n"
        f"Prêmio: **{sorteio_atual.premio}**\n"
        f"Vencedor(a): {mensagem_vencedor}"
    )


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError(
            "Defina a variável de ambiente DISCORD_TOKEN antes de iniciar o bot."
        )
    bot.run(token)
