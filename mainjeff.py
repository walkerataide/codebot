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

    #confirmação de que está funcionando ou não os slash commands
    try:                            
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comandos de barra")
    except Exception as e:
        print(f"Erro ao sincronizar: {e}")

@bot.event
async def on_member_join(member):
    # Substitua 'SEU_CANAL_ID_AQUI' pelo ID do seu canal de boas-vindas.
    # Certifique-se de que o ID seja um número inteiro (sem aspas).
    canal_id = "https://discord.com/channels/1396868698739839028/1396868700132479037"

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
    

#aqui estarão os slash commands, são identicos aos comandos normais, porém mais organizados
#todos esses comandos aparecerão em uma lista ao digitar "/"
@bot.tree.command(name="piada", description="Conta uma piada")
async def slash_piada(interaction: discord.Interaction):
    await interaction.response.send_message("O que o tubarão faz no computador? Navega na rede.")

@bot.tree.command(name="dominio", description="Expande seu dominio")
async def slash_dominio(interaction: discord.Interaction):
    await interaction.response.send_message("Calma paizão, você não é o sukuna.")

@bot.tree.command(name="hug", description="Abraça um membro")
async def slash_hug(interaction: discord.Interaction, member: discord.Member):
    if member == interaction.user:
        await interaction.response.send_message("Você não pode se abraçar sozinho! 🤗")
        return
    
    gif = random.choice(hug_gifs)
    await interaction.response.send_message(
        f"{interaction.user.mention} abraçou {member.mention}! 🤗\n{gif}"
    )


# ===================================================================================
# 4. SISTEMA DE PERFIS E RANKING
# ===================================================================================
perfis = {}

@bot.command()
async def criarperfil(ctx, *, nome: str):
    user_id = ctx.author.id
    perfis[user_id] = {
        "nome": nome, 
        "pontos": perfis.get(user_id, {}).get("pontos", 0),
        "medalhas": perfis.get(user_id, {}).get("medalhas", None),
        "missoes": perfis.get(user_id, {}).get("missoes", 0),
        "rank": perfis.get(user_id, {}).get("rank", None),
        "moedas": perfis.get(user_id, {}).get("moedas", 0)
        }
    await ctx.send(f"✅ Perfil criado/editado para {ctx.author.mention}! Seu novo nome é: **{nome}**")

@bot.command()
async def perfil(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    user_id = membro.id

    if user_id not in perfis:
        await ctx.send(f"{membro.mention} ainda não tem perfil! Use `!criarperfil <nome>` para criar um.")
        return

    perfil = perfis[user_id]
    
    embed = discord.Embed(
        title=f"🎮 Perfil de {membro.mention}",
        color=discord.Color.blue()
    )
    embed.add_field(name="👤 Nome", value=perfil["nome"], inline=True)
    embed.add_field(name="⭐ Pontos", value=perfil["pontos"], inline=True)

    # Força quebra de linha (campo invisível)
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    
    embed.add_field(name="🏅 medalhas", value=perfil["medalhas"], inline=True)
    embed.add_field(name="📜 Missões", value=perfil["missoes"], inline=True)

    # Força quebra de linha (campo invisível)
    embed.add_field(name="\u200b", value="\u200b", inline=False)

    embed.add_field(name="📊 Rank", value=perfil["rank"], inline=True)
    embed.add_field(name="💰 Moedas", value=perfil["moedas"], inline=True)
    
    await ctx.reply(embed=embed)

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


missoes_ativas = {} # Armazena missões ativas por usuário

@bot.command()
async def missoes(ctx, membro: discord.Member = None):
    membro = membro or ctx.author
    if membro.id not in missoes_ativas:
        await ctx.send(f"{membro.mention} não tem missões ativas no momento.")
        return
    await ctx.send(f"🎯 Missão de {membro.mention}:\n**{missoes_ativas[membro.id]}**")



# ===================================================================================
# 5. COMANDOS DE ADMINISTRAÇÃO
# ===================================================================================

@bot.command()
#@commands.has_permissions(administrator=True)
async def darmissao(ctx, membro: discord.Member, *, descricao: str):
    if membro.id in missoes_ativas:
        await ctx.send(f"⚠️ {membro.display_name} já tem uma missão em andamento:\n**{missoes_ativas[membro.id]}**")
        return
    
    missoes_ativas[membro.id] = descricao
    await ctx.send(f"📜 Missão dada a {membro.mention}:\n**{descricao}**")

@bot.command(name="aprovar")
#@commands.has_permissions(manage_messages=True)  
async def aprovar(ctx, membro: discord.Member):
    if membro.id not in missoes_ativas:
        await ctx.send(f"⚠️ {membro.display_name} não tem nenhuma missão ativa.")
        return
    
    if membro.id not in perfis:
        await ctx.send(f"⚠️ {membro.mention} não tem perfil ainda! Peça para ele criar um com `!criarperfil`.")
        return
    
    perfis[membro.id]["pontos"] += 100
    perfis[membro.id]["moedas"] += 50
    perfis[membro.id]["missoes"] += 1

    missao_feita = missoes_ativas.pop(membro.id)
    await ctx.send(
        f"✅ Missão de **{membro.display_name}** aprovada!\n"
        f"Missão: *{missao_feita}*\n"
        f"+100 pontos | +50 Moedas 🎉"
    )

@bot.command()
@commands.has_permissions(administrator=True)
async def revogar(ctx, membro: discord.Member):
    if membro.id not in missoes_ativas:
        await ctx.send(f"⚠️ {membro.display_name} não tem nenhuma missão ativa.")
        return
    
    missao_revogada = missoes_ativas.pop(membro.id)
    await ctx.send(f"❌ Missão de **{membro.display_name}** revogada:\n*{missao_revogada}*")

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

@bot.command()
#@commands.has_permissions(manage_messages=True)  # só quem pode gerenciar mensagens pode usar
async def limpar(ctx, quantidade: int = 10):
    if quantidade < 1:
        await ctx.send("⚠️ A quantidade precisa ser pelo menos 1.")
        return

    # apagar o comando que chamou
    deletadas = await ctx.channel.purge(limit=quantidade + 1)

    await ctx.send(f"🧹 Limpei {len(deletadas)-1} mensagens!", delete_after=5)

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
