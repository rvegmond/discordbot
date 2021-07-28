from discord.ext import commands, tasks
from loguru import logger
from datetime import timedelta, datetime


def normalize_time(intime: str) -> str:
    """
    Translate the intime to a normal "clock" time.
    The input can be hours from now, clock time or hours + hours/10

    paramters:
        intime:     The time to normalize
    Output:
        intime:     The normalized time
    """
    logger.info(f"intime: {intime}")
    now = datetime.now()
    logger.info(f"now: {now}")
    if "." in intime or "," in intime:
        logger.info(f"found . {intime}")
        (hours, minutes) = intime.split(".")
        logger.info(f"hours: {hours}, minutes: {minutes}")
        intime = now + timedelta(hours=int(hours), minutes=int(minutes) * 6)
    elif "u" in intime:
        logger.info(f"found u {intime}")
        intime = intime.replace("u", "")
        (hours, minutes) = intime.split(":")
        intime = datetime.datetime(
            now.year, now.month, now.day, int(hours), int(minutes), 0
        )
        if intime < now:
            intime = intime + timedelta(days=1)
    elif ":" in intime:
        logger.info(f"found : {intime}")
        (hours, minutes) = intime.split(":")
        logger.info(f"hours: {hours}, minutes: {minutes}")
        intime = now + timedelta(hours=int(hours), minutes=int(minutes))
        logger.info(f"intime: {intime}")
    intime = intime.strftime("%Y-%m-%d %H:%M")
    logger.info(f"return {intime}")
    return intime
