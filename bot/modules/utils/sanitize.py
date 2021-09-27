from discord.ext import commands, tasks
from loguru import logger


def sanitize(msg_in: str, maxlength: int = 200) -> str:
    """
    Sanitize the message in, remove forbidden characters.
    Truncate the message at maxlength (last bit will be replace with truncated)

    parameters:
        msg_in:    string to be sanitized
        maxlenght: maximum length of the string
    """
    forbidden = ["@", "#"]
    trunctext = " .. truncated"
    logger.info(f"msg_in: {msg_in}")
    if len(msg_in) > maxlength:
        tmplength = maxlength - len(trunctext)
        logger.info(f"tmplength {tmplength}")
        if tmplength < 0:
            msg_out = trunctext
        else:
            msg_out = msg_in[:tmplength]
            msg_out += trunctext
    else:
        msg_out = msg_in

    for nogo in forbidden:
        msg_out = msg_out.replace(nogo, "_")
    return msg_out
