"""
File that contains the tech related functions and classes
Tech are the modules for a user, tehere are stored in a google sheet
"""
import os
from discord.ext import commands
from loguru import logger
import gspread

from ..robin import Robin
from ..utils import feedback

SHEET_CONFIG = [
    {"column": 1, "spec": "div", "long_name": "influence", "short_name": "infl"},
    {"column": 2, "spec": "div", "long_name": "Naam", "short_name": ""},
    {"column": 3, "spec": "div", "long_name": "Bijgewerkt", "short_name": ""},
    {"column": 4, "spec": "div", "long_name": "Cred.cap.", "short_name": ""},
    {"column": 5, "spec": "div", "long_name": "taakstelling", "short_name": ""},
    {"column": 6, "spec": "div", "long_name": "ws-count", "short_name": ""},
    {"column": 7, "spec": "ship", "long_name": "Transport", "short_name": ""},
    {"column": 8, "spec": "ship", "long_name": "Total Cargo Slots", "short_name": ""},
    {"column": 9, "spec": "ship", "long_name": "Miner", "short_name": ""},
    {"column": 10, "spec": "ship", "long_name": "Hydrogen Capacity", "short_name": ""},
    {"column": 11, "spec": "ship", "long_name": "Battleship", "short_name": ""},
    {
        "column": 12,
        "spec": "trade",
        "long_name": "Cargo bay extension",
        "short_name": "cbe",
    },
    {
        "column": 13,
        "spec": "trade",
        "long_name": "Shipment Computer",
        "short_name": "sc",
    },
    {"column": 14, "spec": "trade", "long_name": "Trade boost", "short_name": "tboost"},
    {"column": 15, "spec": "trade", "long_name": "Rush", "short_name": "rush"},
    {"column": 16, "spec": "trade", "long_name": "Trade burst", "short_name": "burst"},
    {
        "column": 17,
        "spec": "trade",
        "long_name": "Shipment Drone",
        "short_name": "sdrone",
    },
    {"column": 18, "spec": "trade", "long_name": "Offload", "short_name": "offl"},
    {"column": 19, "spec": "trade", "long_name": "Shipment Beam", "short_name": "sb"},
    {"column": 20, "spec": "trade", "long_name": "Entrust", "short_name": "entr"},
    {"column": 21, "spec": "trade", "long_name": "Dispatch", "short_name": "disp"},
    {"column": 22, "spec": "trade", "long_name": "Recall", "short_name": "rec"},
    {"column": 23, "spec": "trade", "long_name": "Relic Drone", "short_name": "rdrone"},
    {
        "column": 24,
        "spec": "mining",
        "long_name": "Mining Boost",
        "short_name": "mboost",
    },
    {
        "column": 25,
        "spec": "mining",
        "long_name": "Hydrogen bay extension",
        "short_name": "hbe",
    },
    {"column": 26, "spec": "mining", "long_name": "Enrich", "short_name": "enr"},
    {"column": 27, "spec": "mining", "long_name": "Remote mining", "short_name": "rm"},
    {
        "column": 28,
        "spec": "mining",
        "long_name": "Hydrogen upload",
        "short_name": "hu",
    },
    {"column": 29, "spec": "mining", "long_name": "Mining Unity", "short_name": "mu"},
    {"column": 30, "spec": "mining", "long_name": "Crunch", "short_name": "cr"},
    {"column": 31, "spec": "mining", "long_name": "Genesis", "short_name": "gen"},
    {
        "column": 32,
        "spec": "mining",
        "long_name": "Hydrogen Rocket",
        "short_name": "hr",
    },
    {
        "column": 33,
        "spec": "mining",
        "long_name": "Mining Drone",
        "short_name": "mdrone",
    },
    {
        "column": 34,
        "spec": "weapons",
        "long_name": "Weak Battery",
        "short_name": "wbat",
    },
    {"column": 35, "spec": "weapons", "long_name": "Battery", "short_name": "bat"},
    {"column": 36, "spec": "weapons", "long_name": "Laser", "short_name": "las"},
    {
        "column": 37,
        "spec": "weapons",
        "long_name": "Mass battery",
        "short_name": "mbat",
    },
    {"column": 38, "spec": "weapons", "long_name": "Dual laser", "short_name": "dlas"},
    {"column": 39, "spec": "weapons", "long_name": "Barrage", "short_name": "barrage"},
    {
        "column": 40,
        "spec": "weapons",
        "long_name": "Dart Launcher",
        "short_name": "dart",
    },
    {"column": 41, "spec": "shields", "long_name": "Alpha Shield", "short_name": "as"},
    {
        "column": 42,
        "spec": "shields",
        "long_name": "Delta shield",
        "short_name": "delta",
    },
    {
        "column": 43,
        "spec": "shields",
        "long_name": "Passive shield",
        "short_name": "pass",
    },
    {
        "column": 44,
        "spec": "shields",
        "long_name": "Omega shield",
        "short_name": "omega",
    },
    {
        "column": 45,
        "spec": "shields",
        "long_name": "Mirror shield",
        "short_name": "mirror",
    },
    {
        "column": 46,
        "spec": "shields",
        "long_name": "Blast Shield",
        "short_name": "blast",
    },
    {"column": 47, "spec": "shields", "long_name": "Area shield", "short_name": "area"},
    {"column": 48, "spec": "support", "long_name": "EMP", "short_name": "emp"},
    {"column": 49, "spec": "support", "long_name": "Teleport", "short_name": "tp"},
    {
        "column": 50,
        "spec": "support",
        "long_name": "Red star life extender",
        "short_name": "rse",
    },
    {"column": 51, "spec": "support", "long_name": "Remote Repair", "short_name": "rr"},
    {"column": 52, "spec": "support", "long_name": "Time warp", "short_name": "tw"},
    {"column": 53, "spec": "support", "long_name": "Unity", "short_name": "unit"},
    {"column": 54, "spec": "support", "long_name": "Sanctuary", "short_name": "sanc"},
    {"column": 55, "spec": "support", "long_name": "Stealth", "short_name": "stealth"},
    {"column": 56, "spec": "support", "long_name": "Fortify", "short_name": "fort"},
    {"column": 57, "spec": "support", "long_name": "Impulse", "short_name": "imp"},
    {"column": 58, "spec": "support", "long_name": "Alpha Rocket", "short_name": "ar "},
    {"column": 59, "spec": "support", "long_name": "Salvage", "short_name": "salv"},
    {"column": 60, "spec": "support", "long_name": "Suppress", "short_name": "supp"},
    {"column": 61, "spec": "support", "long_name": "Destiny", "short_name": "dest"},
    {"column": 62, "spec": "support", "long_name": "Barrier", "short_name": "barr"},
    {"column": 63, "spec": "support", "long_name": "Vengeance", "short_name": "veng"},
    {"column": 64, "spec": "support", "long_name": "Delta Rocket", "short_name": "dr"},
    {"column": 65, "spec": "support", "long_name": "Leap", "short_name": "leap"},
    {"column": 66, "spec": "support", "long_name": "Bond", "short_name": "bond"},
    {"column": 67, "spec": "support", "long_name": "Laser Turret", "short_name": "lt"},
    {"column": 68, "spec": "support", "long_name": "Alpha Drone", "short_name": "ad"},
    {"column": 69, "spec": "support", "long_name": "Suspend", "short_name": "susp"},
    {"column": 70, "spec": "support", "long_name": "Omega Rocket", "short_name": "or"},
    {"column": 71, "spec": "support", "long_name": "Remote Bomb", "short_name": "rb"},
]

short_to_long = {}
for item in SHEET_CONFIG:
    short_to_long[item["short_name"]] = item["long_name"]

long_to_short = {}
for item in SHEET_CONFIG:
    long_to_short[item["long_name"]] = item["short_name"]

specialty = {}

for item in SHEET_CONFIG:
    if item["spec"] not in specialty:
        specialty[item["spec"]] = []
    specialty[item["spec"]].append(item["long_name"])


def _tech_get_module(worksheet, user, module):
    """
    Get a specific module level
    """
    list_of_lists = worksheet.get_all_records()
    for item in list_of_lists:
        if item["Naam"] == user:
            mod_config = item
    return f"{short_to_long[module]} ({module}): {mod_config[short_to_long[module]]}"


def _tech_get_specialty(worksheet, user, spec):
    """
    get all levels in a specific specialty
    """
    list_of_lists = worksheet.get_all_records()
    for item in list_of_lists:
        if item["Naam"] == user:
            mod_config = item
    msg = f"**{spec}** for **{user}**, laatst bijgewerkt: **{mod_config['Bijgewerkt']}**\n"
    for item in specialty[spec]:
        short = long_to_short[str(item)]
        msg = msg + f"{item} ({short}): {mod_config[item]}\n"
    return msg


def _tech_get_all(worksheet, user):
    """
    Just get all tech for a user
    """
    list_of_lists = worksheet.get_all_records()
    for item in list_of_lists:
        if item["Naam"] == user:
            mod_config = item
    msg = (
        f"**Tech** for **{user}**, laatst bijgewerkt: **{mod_config['Bijgewerkt']}**\n"
    )
    i = 0
    for item in mod_config:
        if i > 6 or i == 0:
            msg = msg + f"{item} ({long_to_short[str(item)]}): {mod_config[item]}\n"
        i = i + 1
    return msg


class Tech(Robin):
    """
    The class that gets tech info
    """

    # def _tech_get_ws(self, worksheet, ws):
    #     list_of_lists = worksheet.get_all_records()
    #     for item in list_of_lists:
    #         if item['ws-count'] == ws:
    #             mod_config = item
    #     msg = f"**Tech** for **{ws}**, laatst bijgewerkt: **{mod_config['Bijgewerkt']}**\n"
    #     i = 0
    #     for item in mod_config:
    #         if i > 6 or i == 0:
    #             msg = msg + f"{item}: {mod_config[item]}\n"
    #         i = i + 1
    #     return msg

    @commands.command(
        name="tech",
        brief=("Geeft info over tech mods"),
        help=(
            "Met het tech commando vraag je de modules op van een speler zoals bekend in de google sheet\n"
            f"**tech get discordnaam** all         - geeft alle modules van een speler\n"
            f"**tech get discordnaam** modulenaam  - geeft het modulelevel van een speler\n"
            f"**tech get discordnaam** tech        - geeft de modules voor een bepaalde tech van een speler\n"
            f"     waar waar tech = [{specialty.keys()}]]"
            "\n"
            "\n"
        ),
    )
    async def tech(
        self,
        ctx,
        requested_action="not_defined",
        requested_for="not_defined",
        requested_type="all",
    ):
        """
        Get and display the tech levels for a user/group
        tech [get|set] [player|ws#] [mining|modulename|all]
        """
        if (requested_action == "not_defined") or (requested_for == "not_defined"):
            await ctx.send_help(ctx.command)
            return None
        logger.info(f"long_to_short {long_to_short}")
        logger.info(f"user {requested_for}")
        usermap = self._getusermap_by_alias(requested_for)
        gc = gspread.service_account()
        wks = gc.open_by_key(os.getenv("GSHEET_ID"))
        worksheet = wks.worksheet("Modules")
        if requested_type == "all":
            msg = _tech_get_all(worksheet, usermap["GsheetAlias"])

        elif requested_type in specialty:
            msg = _tech_get_specialty(worksheet, usermap["GsheetAlias"], requested_type)
        else:
            if requested_type in long_to_short:
                requested_type = long_to_short[requested_type]
            msg = _tech_get_module(worksheet, usermap["GsheetAlias"], requested_type)

        await feedback(ctx=ctx, msg=msg)
