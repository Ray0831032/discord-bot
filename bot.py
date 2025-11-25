import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
TOKEN = os.environ["DISCORD_TOKEN"]
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("bot已啟動")
@bot.command()
async def setupbutton(ctx):
    embed = discord.Embed(
        title = "歡迎來到伺服器！",
        description = "請點擊下方按鈕以獲取身分組。",
        color = discord.Color.blue()
    )
    view = discord.ui.View()
    button = discord.ui.Button(label="獲取身分組", style=discord.ButtonStyle.green, emoji="🎉")
    async def button_callback(interaction):
        role = discord.utils.get(ctx.guild.roles, name="客戶")
        unrole = discord.utils.get(ctx.guild.roles, name="未驗證")
        if role:
            await interaction.user.add_roles(role)
            await interaction.user.remove_roles(unrole)
            await interaction.response.send_message("你已成功獲取身分組！", ephemeral=True)
        else:
            await interaction.response.send_message("找不到指定的身分組。", ephemeral=True)
    button.callback = button_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

class ServiceMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="克服除錯", description="需要輔助方面的幫助", emoji="🛠️"),
            discord.SelectOption(label="買前詢問", description="購買前的相關問題", emoji="❓"),
            discord.SelectOption(label="成為夥伴", description="想與我們一起合作", emoji="🤝"),
            discord.SelectOption(label="沒收到貨", description="索取帳號/未收到商品", emoji="📦"),
        ]
        super().__init__(placeholder="選擇一個服務選項...", max_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        guild = interaction.guild
        overwrite = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        channel = await guild.create_text_channel(name=f"服務-{interaction.user.name}", overwrites=overwrite)
        await channel.send(f"{interaction.user.mention}，感謝你選擇了「{selected_option}」服務，我們將盡快為你提供協助。")
@bot.command()
async def services(ctx):
    embed = discord.Embed(
        title="服務選單",
        description="請從下拉選單中選擇你需要的服務類型。",
        color=discord.Color.purple()
    )
    view = discord.ui.View()
    view.add_item(ServiceMenu())
    await ctx.send(embed=embed, view=view)

@bot.command()
async def closeticket(ctx):
    embed = discord.Embed(
        title="關閉服務單",
        description="點擊下方按鈕以關閉此服務單。",
        color=discord.Color.red()
    )
    view = discord.ui.View()
    button = discord.ui.Button(label="關閉服務單", style=discord.ButtonStyle.red)
    async def button_callback(interaction):
        embed = discord.Embed(
            title="服務單已關閉",
            description="此服務單已被關閉，感謝你的使用！",
            color=discord.Color.green()
        )
        await interaction.response.send_message(
            "服務單已關閉，頻道將在 1 秒後刪除。",
            ephemeral=True
        )
        await asyncio.sleep(1)
        await interaction.channel.delete()
    
    button.callback = button_callback
    view.add_item(button)
    await ctx.send(embed=embed, view=view)
    

bot.run(TOKEN)
