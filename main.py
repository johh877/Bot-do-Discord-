import os
import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# Configura as permissões do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler()

async def enviar_mensagem_agendada(channel_id, texto):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(texto)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado com sucesso como: {bot.user}")
    scheduler.start()

# Comando: !agendar DD/MM/AAAA HH:MM Sua mensagem aqui
@bot.command()
async def agendar(ctx, data_str: str, hora_str: str, *, texto: str):
    try:
        data_hora_str = f"{data_str} {hora_str}"
        data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
        
        if data_hora < datetime.now():
            await ctx.send("❌ Essa data e hora já passaram!")
            return

        scheduler.add_job(
            enviar_mensagem_agendada, 
            'date', 
            run_date=data_hora, 
            args=[ctx.channel.id, texto]
        )
        await ctx.send(f"✅ Mensagem agendada para **{data_hora_str}** neste canal!")
    except ValueError:
        await ctx.send("❌ Formato inválido! Use exatamente assim:\n`!agendar DD/MM/AAAA HH:MM Sua mensagem aqui`\nExemplo: `!agendar 25/12/2026 20:00 Feliz Natal galera!`")

# Puxa o Token de forma segura das configurações da Render
TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)
