)
async def verify(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    image: discord.Attachment
):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ Bạn cần quyền Administrator.",
            ephemeral=True
        )
        return

    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ Lệnh này chỉ dùng trong server.",
            ephemeral=True
        )
        return

    if not image.content_type or not image.content_type.startswith("image/"):
        await interaction.response.send_message(
            "❌ Vui lòng chọn một tệp ảnh.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="Verify • BirthdayTime",
        description=(
            "> Hãy bấm nút \"Verify\" để được xác minh.\n"
            "> Sau khi bấm, hãy nhập đúng mã xác minh được cung cấp cho bạn."
        ),
        color=discord.Color.blue()
    )
    embed.set_footer(text="by ph.huyy.")
    embed.set_image(url=image.url)

    try:
        await channel.send(embed=embed, view=VerifyView())
    except discord.Forbidden:
        await interaction.response.send_message(
            f"❌ Bot không có quyền gửi tin nhắn tại {channel.mention}.",
            ephemeral=True
        )
        return
    except discord.HTTPException:
        await interaction.response.send_message(
            "❌ Không thể gửi bảng Verify vào kênh này.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"✅ Đã thiết lập bảng Verify tại {channel.mention}.",
        ephemeral=True
    )


@bot.event
async def on_member_join(member: discord.Member):
    # Chỉ gửi DM cho thành viên mới trong server được phép.
    if member.guild.id not in ALLOWED_GUILD_IDS:
        return

    VERIFY_LINK = "https://discord.gg/Nvmh4D7VCX"

    try:
        join_embed = discord.Embed(
            title="Chào mừng bạn đến server!",
            description=(
                f"Bạn hãy vào kênh verify của **{member.guild.name}** để xác minh."
                f"🔗 [Vào kênh Verify]({VERIFY_LINK})"
            ),
            color=discord.Color.blurple()
        )
        join_embed.set_footer(text="by ph.huyy.")

        # Nút bấm mở trực tiếp link Verify.
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="Vào Verify",
                style=discord.ButtonStyle.link,
                url=VERIFY_LINK
            )
        )

        await member.send(embed=join_embed, view=view)
    except (discord.Forbidden, discord.HTTPException):
        # Người dùng có thể đã tắt DM.
        pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bạn không có quyền sử dụng lệnh này.", delete_after=30)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Thiếu tham số. Hãy kiểm tra cú pháp lệnh.", delete_after=30)
        return
    if isinstance(error, commands.BadArgument):
        await ctx.send("❌ Tham số không hợp lệ. Hãy kiểm tra lại.", delete_after=30)
        return
    print(f"Command error: {type(error).__name__}: {error}")


bot.run(TOKEN)
