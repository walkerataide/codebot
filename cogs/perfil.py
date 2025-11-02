import discord
from discord import app_commands
from discord.ext import commands
from data import perfis, missoes_ativas


class Perfis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando para criar ou editar perfil
    @app_commands.command(name="criarperfil", description="Cria ou edita seu perfil")
    @app_commands.describe(nome="O nome que deseja para seu perfil")
    async def criar_perfil(self, interaction: discord.Interaction, nome: str):
        user_id = interaction.user.id

        if user_id in perfis:
            await interaction.response.send_message(
                 "⚠️ Você já possui um perfil criado!",
                 ephemeral=True
            )
            return
        
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

    # Comando para exibir o perfil
    @app_commands.command(name="perfil", description="Mostra o perfil de um usuário")
    @app_commands.describe(membro="O usuário cujo perfil deseja ver (deixe vazio para ver o seu)")
    async def ver_perfil(self, interaction: discord.Interaction, membro: discord.Member = None):
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

    # Comando para exibir o ranking
    @app_commands.command(name="rank", description="Mostra o ranking dos perfis do servidor")
    async def rank(self, interaction: discord.Interaction):
        if not perfis:
            await interaction.response.send_message("📉 Não há perfis no rank ainda!")
            return

        ranking = sorted(perfis.items(), key=lambda item: item[1]["pontos"], reverse=True)
        embed = discord.Embed(title="🏆 Ranking do Servidor 🏆", color=discord.Color.gold())

        for i, (user_id, dados) in enumerate(ranking, start=1):
            try:
                user = await self.bot.fetch_user(user_id)
                nome = user.display_name
            except discord.NotFound:
                nome = "Usuário Desconhecido"

            embed.add_field(
                name=f"{i}. {nome}",
                value=f"**{dados['pontos']}** pontos\n(Nome: {dados['nome']})",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

    # Comando para mostrar missões
    @app_commands.command(name="missoes", description="Mostra as missões ativas de um usuário")
    @app_commands.describe(membro="O usuário cujas missões deseja ver (deixe vazio para ver as suas)")
    async def missoes(self, interaction: discord.Interaction, membro: discord.Member = None):
        membro = membro or interaction.user

        if membro.id not in missoes_ativas:
            await interaction.response.send_message(
                f"{membro.mention} não tem missões ativas no momento.", ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"🎯 Missão de {membro.mention}:\n**{missoes_ativas[membro.id]}**"
        )


# Função obrigatória para o bot carregar a Cog
async def setup(bot):
    await bot.add_cog(Perfis(bot))
