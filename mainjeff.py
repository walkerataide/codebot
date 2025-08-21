# -*- coding: utf-8 -*-

# ===================================================================================
# 1. IMPORTAÇÕES E CONFIGURAÇÃO INICIAL
# ===================================================================================

# Importações das bibliotecas necessárias.
import discord  # Biblioteca principal para interagir com a API do Discord.
from discord.ext import commands  # Módulo da biblioteca para criar comandos de forma fácil.
import random  # Módulo para gerar números aleatórios (usado no comando hug).
import os  # Para interagir com o sistema operacional (usado para ler variáveis de ambiente).
from dotenv import load_dotenv  # Para carregar variáveis de ambiente de um arquivo .env.

# Carrega as variáveis do arquivo .env para o ambiente do script.
load_dotenv()

# Configuração dos "Intents" (Intenções) do bot.
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.members = True

# Cria a instância do bot.
bot = commands.Bot(command_prefix='!', intents=intents)

# ===================================================================================
# 2. EVENTOS DO BOT
# ===================================================================================

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    print(f'Jeff está pronto para caçar em {len(bot.guilds)} servidores!')

@bot.event
async def on_member_join(member):
    # Substitua 'SEU_CANAL_ID_AQUI' pelo ID do seu canal de boas-vindas.
    # Certifique-se de que o ID seja um número inteiro (sem aspas).
    canal_id = SEU_CANAL_ID_AQUI

    canal = member.guild.get_channel(canal_id)

    if canal:
        await canal.send(f'Seja bem vindo {member.mention}, você foi promovido a recruta da torre.')
    else:
        print(f"AVISO: Canal de boas-vindas com ID {canal_id} não encontrado. Verifique a variável 'canal_id'.")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    reaction_rules = {
        "🔥": "Uau! Esse é quente!",
        "😂": "Haha, que engraçado!",
        "❤️": "Amor sentido!"
    }
    emoji = str(reaction.emoji)
    if emoji in reaction_rules:
        response = reaction_rules[emoji]
        await reaction.message.channel.send(f"{user.name} reagiu com {emoji}: {response}")

# ===================================================================================
# 3. COMANDOS DE DIVERSÃO
# ===================================================================================

@bot.command()
async def piada(ctx):
    await ctx.send('O que o tubarão faz no computador?')
    await ctx.send('Navega na rede.')

@bot.command()
async def dominio(ctx):
    await ctx.send('Calma paizão, você não é o sukuna')

hug_gifs = [
    "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
    "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
    "https://media.giphy.com/media/wnsgren9NtITS/giphy.gif"
]

@bot.command()
async def hug(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Você não pode se abraçar sozinho! 🤗")
        return
    gif = random.choice(hug_gifs)
    await ctx.send(f"{ctx.author.mention} abraçou {member.mention}! 🤗\n{gif}")

# ===================================================================================
# 4. SISTEMA DE PERFIS E RANKING
# ===================================================================================
perfis = {}

@bot.command()
async def criarperfil(ctx, *, nome: str):
    user_id = ctx.author.id
    perfis[user_id] = {"nome": nome, "pontos": perfis.get(user_id, {}).get("pontos", 0)}
    await ctx.send(f"✅ Perfil criado/editado para {ctx.author.mention}! Seu novo nome é: **{nome}**")

@bot.command()
async def perfil(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    user_id = membro.id

    if user_id not in perfis:
        await ctx.send(f"{membro.mention} ainda não tem perfil! Use `!criarperfil <nome>` para criar um.")
        return

    dados = perfis[user_id]
    await ctx.send(f"📜 **Perfil de {membro.mention}**\n"
                   f"👤 **Nome:** {dados['nome']}\n"
                   f"⭐ **Pontos:** {dados['pontos']}")

@bot.command()
async def rank(ctx):
    if not perfis:
        await ctx.send("📉 Não há perfis no rank ainda!")
        return

    ranking = sorted(perfis.items(), key=lambda item: item[1]["pontos"], reverse=True)

    msg = "🏆 **Ranking do Servidor** 🏆\n"
    for i, (user_id, dados) in enumerate(ranking, start=1):
        try:
            user = await bot.fetch_user(user_id)
            msg += f"`{i}.` {user.mention} — **{dados['pontos']}** pontos (Nome: {dados['nome']})\n"
        except discord.NotFound:
            msg += f"`{i}.` *Usuário Desconhecido* — **{dados['pontos']}** pontos (Nome: {dados['nome']})\n"

    await ctx.send(msg)

# ===================================================================================
# 5. COMANDOS DE ADMINISTRAÇÃO
# ===================================================================================

@bot.command()
@commands.has_permissions(administrator=True)
async def addpontos(ctx, membro: discord.Member, qtd: int):
    user_id = membro.id
    if user_id not in perfis:
        await ctx.send(f"{membro.mention} não tem perfil ainda! Peça para ele criar um com `!criarperfil`.")
        return

    perfis[user_id]["pontos"] += qtd
    await ctx.send(f"➕ **{qtd}** pontos foram adicionados a {membro.mention}! Total atual: **{perfis[user_id]['pontos']}**")

@bot.command()
@commands.has_permissions(administrator=True)
async def rempontos(ctx, membro: discord.Member, qtd: int):
    user_id = membro.id
    if user_id not in perfis:
        await ctx.send(f"{membro.mention} não tem perfil ainda!")
        return

    perfis[user_id]["pontos"] -= qtd
    await ctx.send(f"➖ **{qtd}** pontos foram removidos de {membro.mention}! Total atual: **{perfis[user_id]['pontos']}**")

# ===================================================================================
# 6. TRATAMENTO DE ERROS
# ===================================================================================

@hug.error
async def hug_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Você precisa mencionar alguém para abraçar! 😢 Exemplo: `!hug @amigo`")

@addpontos.error
@rempontos.error
async def admin_cmds_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 Você não tem permissão de Administrador para usar este comando!")

# ===================================================================================
# 7. INICIALIZAÇÃO DO BOT
# ===================================================================================

def main():
    """Função principal para iniciar o bot de forma segura."""
    # Busca o token do arquivo .env.
    TOKEN = os.getenv('DISCORD_TOKEN')

    if TOKEN is None:
        print("ERRO: A variável de ambiente DISCORD_TOKEN não foi encontrada.")
        print("Por favor, crie um arquivo .env e adicione DISCORD_TOKEN=SEU_TOKEN_AQUI")
        return

    bot.run(TOKEN)

if __name__ == "__main__":
    main()