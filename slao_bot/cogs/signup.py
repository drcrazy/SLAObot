from discord import Colour, DMChannel, Embed, Member, Message
from discord.ext import commands
from discord.ext.commands import Context
from utils.config import settings


class SignUp(commands.Cog):
    def __init__(self, bot):
        """
        Cog to greet newcomers and give them some basic questionnaire.

        :param bot: Bot instance
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        if member.bot:
            return
        dm_channel = await member.create_dm()
        intro_message = (f'Привет, {format(member.mention)}! \r\n'
                         'Приветствуем тебя на Discord сервере гильдии <Адепты Катаклизма>! \r\n'
                         'Мы играем в The Burning Crusade Classic за Альянс на Пламегоре. \r\n'
                         'Если хочешь вступить к нам в гильдию, то напиши мне + в ответ. \r\n'
                         'Удачного времяпрепровождения!')

        await dm_channel.send(content=intro_message)

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not isinstance(message.channel, DMChannel):
            return
        if message.author.bot:
            return

        if message.content == '+':
            signup_form = (
                'Для получения доступа к гильдейским каналам мы бы хотели узнать тебя поближе. \r\n'
                'Пришли мне, пожалуйста, следующую информацию: \r\n '
                '1. Твоё имя \r\n'
                '2. Имя персонажа \r\n'
                '3. Класс, специализация \r\n'
                '4. Профессии, специализация \r\n'
                '5. Имена персонажей твинков'
            )

            await message.channel.send(signup_form)
        elif len(message.content) > 5:
            await message.channel.send('Спасибо! Офицеры в скором времени выдадут права в Discord')
            signup_channel = self.bot.get_channel(settings.signup_channel_id)
            if signup_channel:
                signup_embed = Embed(title='Новая заявка',
                                     description=message.content,
                                     colour=Colour.light_gray())
                signup_embed.add_field(name='Пользователь', value=format(message.author.mention))
                signup_embed.set_thumbnail(url=message.author.avatar_url)
                await signup_channel.send(embed=signup_embed)

    @commands.command(hidden=True)
    async def emit_join(self, ctx: Context) -> None:
        """Emit member_join event."""
        self.bot.dispatch('member_join', ctx.author)


def setup(bot):
    bot.add_cog(SignUp(bot))
