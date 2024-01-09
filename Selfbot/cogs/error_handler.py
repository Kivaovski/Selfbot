import traceback
import sys

from discord.ext import commands
import discord


class CommandErrorHandler(commands.Cog):

    """
    Handling de erros bem feitinho
    https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """
        The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return
            except discord.HTTPException:
                pass
        
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'```Falta o argumento {error.param.name}```', delete_after=5)

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            # if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                # await ctx.send('I could not find that member. Please try again.')
            pass
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

async def setup(bot: commands.Bot):
    await bot.add_cog(CommandErrorHandler(bot))