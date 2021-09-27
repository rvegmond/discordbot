from discord.ext import commands, tasks
from loguru import logger


async def feedback(
    ctx: commands.Context = None,
    msg: str = "",
    delete_after: int = None,
    delete_message: bool = False,
) -> str:
    """
    Send feedback to the user after a message is posted.
    The original message can be deleted.
    The feedback will be sent to the original channel.

    paramters:
        msg:            the message to send
        delete_after:   how long to wait to delete the feedback message (default keep)
        delete_message: delete the original message (default keep)
    """
    if delete_message is not True and delete_message is not False:
        return f"Invallid option for delete_message {delete_message}"

    if ctx is None:
        return "context not spedified"

    await ctx.send(content=msg, delete_after=delete_after)
    if delete_message:
        try:
            await ctx.message.delete()
        except Exception as error:
            logger.info(f"message deletion failed {error}")
            return f"message deletion failed {error}"
    return "feedback sent successful"
