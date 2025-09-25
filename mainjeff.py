# -*- coding: utf-8 -*-

# ===================================================================================
# 1. IMPORTAÇÕES E CONFIGURAÇÃO INICIAL
# ===================================================================================

import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import json

#carrega gifs de abraço
def setup_hub_gifs():
    #carrega os gifs de abraço
    config_path = "config.json"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        hug_gifs = config.get("hug_gifs", {})
    except Exception as e:
        print(f"⚠️ Erro ao carregar os gifs de {config_path}: {e}")
        reaction_rules = {}
    return list(hug_gifs.values())

HUG_GIFS = setup_hub_gifs()

def setup_bot():
    # Carrega variáveis do arquivo .env
    load_dotenv()
    # Configuração dos Intents (necessários para eventos e comandos)
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True
    intents.reactions = True
    intents.members = True

    # Criação da instância do bot
    return commands.Bot(command_prefix="!", intents=intents)

bot = setup_bot()

# ===================================================================================
# 2. EVENTOS DO BOT
# ===================================================================================

@bot.event
async def on_ready():
    """Evento disparado quando o bot é iniciado e conectado."""
    print(f"Bot conectado como {bot.user}")
    print(f"Jeff está pronto para caçar em {len(bot.guilds)} servidores!")

    # Sincronização dos comandos de barra
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos de barra sincronizados")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

@bot.event
async def on_member_join(member):
    """Mensagem de boas-vindas ao entrar no servidor."""
    # Carrega o ID do canal de boas-vindas de um arquivo JSON de configuração
    canal = member.guild.get_channel(os.getenv("1402964229430050846"))

    if canal:
        await canal.send(
            f"Seja bem-vindo {member.mention}, você foi promovido a recruta da torre."
        )
    else:
        print(f"⚠️ Canal de boas-vindas com ID {canal} não encontrado.")


@bot.event
async def on_reaction_add(reaction, user):
    """Reage automaticamente a certas reações."""
    if user.bot:
        return

    # Carrega as regras de reação do config.json
    config_path = "config.json"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        reaction_rules = config.get("reaction_rules", {})
    except Exception as e:
        print(f"⚠️ Erro ao carregar regras de reação de {config_path}: {e}")
        reaction_rules = {}

    emoji = str(reaction.emoji)

    if emoji in reaction_rules:
        await reaction.message.channel.send(
            f"{user.name} reagiu com {emoji}: {reaction_rules[emoji]}"
        )

# ENVIA UMA LISTA COM COMANDOS DE ADMIN PARA O DONO DO SERVIDOR

@bot.event
async def on_guild_join (guild):
 """Executado quando o bot entra em um novo servidor."""
    # Procura o dono do servidor
 dono = guild.owner
    # Manda a lista para o administrador/dono do server
 if dono:
        try:
            await dono.send(
                f"👋 Olá **{dono.display_name}**, obrigado por me adicionar ao servidor **{guild.name}**!\n\n"
                f"Aqui estão os comandos de administrador disponíveis:\n"
                f"```\n"
                f"!darmissao @membro <descrição>\n"
                f"!aprovar @membro\n"
                f"!revogar @membro\n"
                f"!addpontos @membro <quantidade>\n"
                f"!rempontos @membro <quantidade>\n"
                f"!cancelar @membro\n"
                f"!limpar <quantidade>\n"
                f"```"
            )
        except discord.Forbidden:
            print(f"⚠️ Não consegui enviar DM para o dono do servidor {guild.name}.")

# ========= Envia uma lista de comandos de admin para membros que possuem o cargo admin ==================================================
@bot.event
async def on_guild_join(guild):
    """Executado quando o bot entra em um novo servidor."""
    comandos_admin = (
        "📜 **Comandos de Administrador disponíveis:**\n"
        "```\n"
        "!darmissao @membro <descrição>\n"
        "!aprovar @membro\n"
        "!revogar @membro\n"
        "!addpontos @membro <quantidade>\n"
        "!rempontos @membro <quantidade>\n"
        "!cancelarmissao @membro\n"
        "!limpar <quantidade>\n"
        "```"
    )

    for membro in guild.members:
        if membro.guild_permissions.administrator:
            try:
                await membro.send(
                    f"👋 Olá **{membro.display_name}**, eu acabei de entrar no servidor **{guild.name}**!\n\n"
                    f"{comandos_admin}"
                )
            except discord.Forbidden:
                print(f"⚠️ Não consegui enviar DM para {membro.display_name}.")



# OBSERVAÇÃO!!!!  ele só envia para o DONO do servidor e não para quem tem cargo de admin

# ===================================================================================
# 3. COMANDOS DE DIVERSÃO
# ===================================================================================

@bot.command()
async def piada(ctx):
    await ctx.send("O que o tubarão faz no computador?")
    await ctx.send("Navega na rede.")


@bot.command()
async def dominio(ctx):
    await ctx.send("Calma paizão, você não é o sukuna.")


#Dá abraço no membro indicado
@bot.command()
async def hug(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Você não pode se abraçar sozinho! 🤗")
        return

    gif = random.choice(HUG_GIFS)
    await ctx.send(f"{ctx.author.mention} abraçou {member.mention}! 🤗\n{gif}")


# ==== Versões em Slash Commands ====

@bot.tree.command(name="piada", description="Conta uma piada")
async def slash_piada(interaction: discord.Interaction):
    await interaction.response.send_message("O que o tubarão faz no computador? Navega na rede.")


@bot.tree.command(name="dominio", description="Expande seu domínio")
async def slash_dominio(interaction: discord.Interaction):
    await interaction.response.send_message("Calma paizão, você não é o sukuna.")


@bot.tree.command(name="hug", description="Abraça um membro")
async def slash_hug(interaction: discord.Interaction, member: discord.Member):
    if member == interaction.user:
        await interaction.response.send_message("Você não pode se abraçar sozinho! 🤗")
        return

    gif = random.choice(HUG_GIFS)
    await interaction.response.send_message(
        f"{interaction.user.mention} abraçou {member.mention}! 🤗\n{gif}"
    )

# =============== Comando para atribuir missões a membros (texto, imagens, links, arquivos)==========================

# Slash command para enviar missão
@bot.tree.command(name="enviar_missao", description="Envia uma missão para um membro.")
@app_commands.describe(
    membro="Membro que receberá a missão",
    descricao="Descrição da missão",
    link="Um link opcional para a missão",
    imagem="URL de uma imagem opcional",
    arquivo="Um arquivo opcional (PDF, TXT, imagem, etc.)"
)
async def enviar_missao(
    interaction: discord.Interaction,
    membro: discord.Member,
    descricao: str,
    link: str = None,
    imagem: str = None,
    arquivo: discord.Attachment = None
):
    try:
        # Cria um embed bonitinho
        embed = discord.Embed(
            title="🎯 Nova Missão Recebida!",
            description=descricao,
            color=discord.Color.red()
        )
        if link:
            embed.add_field(name="🔗 Link de Referência", value=f"[Clique aqui]({link})", inline=False)
        if imagem:
            embed.set_image(url=imagem)

        # Envia DM para o membro
        files = []
        if arquivo:
            files.append(await arquivo.to_file())

        await membro.send(
            content=f"📌 {membro.mention}, você recebeu uma nova missão!",
            embed=embed,
            files=files
        )

        await interaction.response.send_message(
            f"✅ Missão enviada com sucesso para {membro.mention}.",
            ephemeral=True
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            f"🚫 Não consegui enviar DM para {membro.mention} (talvez ele bloqueou mensagens diretas).",
            ephemeral=True
        )

# ===================================================================================
# 4. SISTEMA DE PERFIS E RANKING
# ===================================================================================

perfis = {}
missoes_ativas = {}  # Armazena missões ativas por usuário


@bot.tree.command(name="criarperfil", description="Cria ou edita seu perfil")
@app_commands.describe(nome="O nome que deseja para seu perfil")
async def slash_criarperfil(interaction: discord.Interaction, nome: str):
    user_id = interaction.user.id
    perfis[user_id] = {
        "nome": nome,
        "pontos": perfis.get(user_id, {}).get("pontos", 0),
        "medalhas": perfis.get(user_id, {}).get("medalhas", None),
        "missoes": perfis.get(user_id, {}).get("missoes", 0),
        "rank": perfis.get(user_id, {}).get("rank", None),
        "moedas": perfis.get(user_id, {}).get("moedas", 0),
    }

    await interaction.response.send_message(
        f"✅ Perfil criado/editado para {interaction.user.mention}! Seu novo nome é: **{nome}**"
    )


@bot.tree.command(name="perfil", description="Mostra o perfil de um usuário")
@app_commands.describe(membro="O usuário cujo perfil deseja ver (deixe vazio para ver o seu)")
async def slash_perfil(interaction: discord.Interaction, membro: discord.Member = None):
    membro = membro or interaction.user
    user_id = membro.id

    if user_id not in perfis:
        await interaction.response.send_message(
            f"{membro.mention} ainda não tem perfil! Use `/criarperfil <nome>` para criar um.",
            ephemeral=True,
        )
        return

    perfil = perfis[user_id]

    embed = discord.Embed(
        title=f"🎮 Perfil de {membro.display_name}", color=discord.Color.blue()
    )
    embed.set_thumbnail(url=membro.avatar.url if membro.avatar else membro.default_avatar.url)

    embed.add_field(name="👤 Nome", value=perfil["nome"], inline=True)
    embed.add_field(name="⭐ Pontos", value=perfil["pontos"], inline=True)
    embed.add_field(name="🏅 Medalhas", value=perfil["medalhas"], inline=True)
    embed.add_field(name="📜 Missões", value=perfil["missoes"], inline=True)
    embed.add_field(name="📊 Rank", value=perfil["rank"], inline=True)
    embed.add_field(name="💰 Moedas", value=perfil["moedas"], inline=True)

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="rank", description="Mostra o ranking dos perfis do servidor")
async def slash_rank(interaction: discord.Interaction):
    if not perfis:
        await interaction.response.send_message("📉 Não há perfis no rank ainda!")
        return

    ranking = sorted(perfis.items(), key=lambda item: item[1]["pontos"], reverse=True)
    embed = discord.Embed(title="🏆 Ranking do Servidor 🏆", color=discord.Color.gold())

    for i, (user_id, dados) in enumerate(ranking, start=1):
        try:
            user = await bot.fetch_user(user_id)
            nome = user.display_name
        except discord.NotFound:
            nome = "Usuário Desconhecido"

        embed.add_field(
            name=f"{i}. {nome}",
            value=f"**{dados['pontos']}** pontos\n(Nome: {dados['nome']})",
            inline=False,
        )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="missoes", description="Mostra as missões ativas de um usuário")
@app_commands.describe(membro="O usuário cujas missões deseja ver (deixe vazio para ver as suas)")
async def slash_missoes(interaction: discord.Interaction, membro: discord.Member = None):
    membro = membro or interaction.user

    if membro.id not in missoes_ativas:
        await interaction.response.send_message(
            f"{membro.mention} não tem missões ativas no momento.", ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"🎯 Missão de {membro.mention}:\n**{missoes_ativas[membro.id]}**"
    )

# ===================================================================================
# 5. COMANDOS DE ADMINISTRAÇÃO
# ===================================================================================


@bot.command(name="aprovar")
async def aprovar(ctx, membro: discord.Member):
    if membro.id not in missoes_ativas:
        await ctx.send(f"⚠️ {membro.display_name} não tem nenhuma missão ativa.")
        return

    if membro.id not in perfis:
        await ctx.send(f"⚠️ {membro.mention} não tem perfil ainda! Use `/criarperfil`.")
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
async def cancelar(ctx, membro: discord.Member):
    if membro.id not in missoes_ativas:
        await ctx.send(f"⚠️ {membro.display_name} não tem nenhuma missão ativa.")
        return

    missao_revogada = missoes_ativas.pop(membro.id)
    await ctx.send(f"❌ Missão de **{membro.display_name}** revogada:\n*{missao_revogada}*")

    try:
        await membro.send(
            f"❌ Sua missão foi **cancelada** pela staff do servidor **{ctx.guild.name}**.\n"
            f"Missão cancelada: *{missao_revogada}*"
        )
    except discord.Forbidden:
        await ctx.followup.send(
            f"⚠️ Não consegui enviar DM para {membro.mention}.", ephemeral=True
        )

@bot.command()
@commands.has_permissions(administrator=True)
async def addpontos(ctx, membro: discord.Member, qtd: int):
    user_id = membro.id
    if user_id not in perfis:
        await ctx.send(f"{membro.mention} não tem perfil ainda! Use `/criarperfil`.")
        return

    perfis[user_id]["pontos"] += qtd
    await ctx.send(
        f"➕ **{qtd}** pontos foram adicionados a {membro.mention}! "
        f"Total atual: **{perfis[user_id]['pontos']}**"
    )


@bot.command()
@commands.has_permissions(administrator=True)
async def rempontos(ctx, membro: discord.Member, qtd: int):
    user_id = membro.id
    if user_id not in perfis:
        await ctx.send(f"{membro.mention} não tem perfil ainda!")
        return

    perfis[user_id]["pontos"] -= qtd
    await ctx.send(
        f"➖ **{qtd}** pontos foram removidos de {membro.mention}! "
        f"Total atual: **{perfis[user_id]['pontos']}**"
    )


@bot.command()
async def limpar(ctx, quantidade: int = 10):
    """Apaga mensagens no chat (default = 10)."""
    if quantidade < 1:
        await ctx.send("⚠️ A quantidade precisa ser pelo menos 1.")
        return

    deletadas = await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f"🧹 Limpei {len(deletadas) - 1} mensagens!", delete_after=5)


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
    """Função principal para iniciar o bot."""
    TOKEN = os.getenv("DISCORD_TOKEN")

    if TOKEN is None:
        print("ERRO: A variável de ambiente DISCORD_TOKEN não foi encontrada.")
        print("Crie um arquivo .env e adicione: DISCORD_TOKEN=SEU_TOKEN_AQUI")
        return

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
