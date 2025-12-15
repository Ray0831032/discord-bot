import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
TOKEN = os.environ["DISCORD_TOKEN"]
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    await asyncio.sleep(0.1)
    role = discord.utils.get(member.guild.roles, name="未驗證")
    if role:
        await member.add_roles(role)
@bot.event
async def on_ready():
    print("bot 已啟動（Persistent Views 已註冊）")

    bot.add_view(ServiceView())   # 下拉選單
    bot.add_view(CloseTicketView())  # 關閉按鈕
    bot.add_view(SetbutView())

class SetbutView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="獲取身分組", style=discord.ButtonStyle.green, custom_id="get_roles")
        async def button_callback(interaction):
            guild = interaction.guild
            role = discord.utils.get(guild.roles, name="客戶") or discord.utils.get(guild.roles, name="成員")
            unrole = discord.utils.get(guild.roles, name="未驗證")
            if role:
                await interaction.user.add_roles(role)
                await interaction.user.remove_roles(unrole)
                await interaction.response.send_message("你已成功獲取身分組！", ephemeral=True)
            else:
                await interaction.response.send_message("找不到指定的身分組。", ephemeral=True)
        button.callback = button_callback
        self.add_item(button)
@bot.command()
async def setupbutton(ctx):
    embed = discord.Embed(
        title="歡迎來到伺服器！",
        description="請點擊下方按鈕以獲取身分組。",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=SetbutView())

class ServiceMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="克服除錯", description="需要輔助方面的幫助", emoji="🛠️"),
            discord.SelectOption(label="買前詢問", description="購買前的相關問題", emoji="❓"),
            discord.SelectOption(label="成為夥伴", description="想與我們一起合作", emoji="🤝"),
            discord.SelectOption(label="沒收到貨", description="索取帳號/未收到商品", emoji="📦"),
        ]
        super().__init__(placeholder="選擇一個服務選項...", max_values=1, options=options, custom_id="menu")
    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        guild = interaction.guild
        overwrite = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        safe_name = "".join(c for c in interaction.user.name if c.isalnum())
        channel = await guild.create_text_channel(f"服務-{safe_name}", overwrites=overwrite)
        await channel.send(f"{interaction.user.mention}，感謝你選擇了「{selected_option}」服務，我們將盡快為你提供協助。",
                           view=CloseTicketView()
                          )


class ServiceView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ServiceMenu())


@bot.command()
async def services(ctx):
    embed = discord.Embed(
        title="**📩  UCHEAT | 除錯服務**",
        description="【**<:uc:1442544293460836544>開客服單須知**】\n\n- **服務時間 : 12:00～23:00**\n\n- **我們提供即時圖文協助，如果想要遠端服務請下單服務[點我購買](https://uc666.xyz/product/anydeskforu/)**\n\n 【**<:uc:1442544293460836544>輔助資訊快捷**】\n\n **🚥輔助狀態(內存):<#1415736109408849991>**\n\n **📚 使用教學(內存):<#1415737076187660508>**\n\n -------------------------------------------\n\n " \
        "**📩 UCHEAT | 解機服務**\n\n 【**<:uc:1442544293460836544>遠端解機**】\n\n- **單次收費:[人工服務](https://uc666.xyz/product/anydeskforu/)**\n\n 【**<:uc:1442544293460836544>自備服務**】\n\n- **需自備:[解機碼卡號](https://uc666.xyz/product-category/hwid-spoofer/)**\n\n- **[ USB隨身碟 - 至少8GB空間 ]**\n\n【**<:uc:1442544293460836544>遠端程序**】\n\n- **下載連結:[連連控遠端](https://www.asklink.com/zh-tw)**\n\n- **服務時間 : 18:00～23:00**",
        color=discord.Color.yellow(),
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1142488059326238750/1450142677671870555/UC-4.webp?ex=6941761c&is=6940249c&hm=21cf7885ce126c46cc8d9c0f9857d08406efe3497d1d44507c4af832fb889093&"
    )
    await ctx.send(embed=embed, view=ServiceView())

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="關閉服務單", style=discord.ButtonStyle.red, custom_id="close_ticket")

        async def button_callback(interaction):
            await interaction.response.send_message(
                "服務單已關閉，頻道將在 1 秒後刪除。",
                ephemeral=True
            )
            await asyncio.sleep(1)
            await interaction.channel.delete()

        button.callback = button_callback
        self.add_item(button)


@bot.command()
async def closeticket(ctx):
    embed = discord.Embed(
        title="關閉服務單",
        description="點擊下方按鈕以關閉此服務單。",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed, view=CloseTicketView())
    

bot.run(TOKEN)
