from discord.ext import commands
from loguru import logger
import gspread
import os

from ..robin import Robin
from ..utils import feedback

SHEET_CONFIG = [
    {"column": 1, "spec": "div", "full_name": "influence", "short_name": "infl"},
    {"column": 2, "spec": "div", "full_name": "Naam", "short_name": ""},
    {"column": 3, "spec": "div", "full_name": "Bijgewerkt", "short_name": ""},
    {"column": 4, "spec": "div", "full_name": "Cred.cap.", "short_name": ""},
    {"column": 5, "spec": "div", "full_name": "taakstelling", "short_name": ""},
    {"column": 6, "spec": "div", "full_name": "ws-count", "short_name": ""},
    {"column": 7, "spec": "ship", "full_name": "Transport", "short_name": ""},
    {"column": 8, "spec": "ship", "full_name": "Total Cargo Slots", "short_name": ""},
    {"column": 9, "spec": "ship", "full_name": "Miner", "short_name": ""},
    {"column": 10, "spec": "ship", "full_name": "Hydrogen Capacity", "short_name": ""},
    {"column": 11, "spec": "ship", "full_name": "Battleship", "short_name": ""},
    {
        "column": 12,
        "spec": "trade",
        "full_name": "Cargo bay extension",
        "short_name": "cbe",
    },
    {
        "column": 13,
        "spec": "trade",
        "full_name": "Shipment Computer",
        "short_name": "sc",
    },
    {"column": 14, "spec": "trade", "full_name": "Trade boost", "short_name": "tboost"},
    {"column": 15, "spec": "trade", "full_name": "Rush", "short_name": "rush"},
    {"column": 16, "spec": "trade", "full_name": "Trade burst", "short_name": "burst"},
    {
        "column": 17,
        "spec": "trade",
        "full_name": "Shipment Drone",
        "short_name": "sdrone",
    },
    {"column": 18, "spec": "trade", "full_name": "Offload", "short_name": "offl"},
    {"column": 19, "spec": "trade", "full_name": "Shipment Beam", "short_name": "sb"},
    {"column": 20, "spec": "trade", "full_name": "Entrust", "short_name": "entr"},
    {"column": 21, "spec": "trade", "full_name": "Dispatch", "short_name": "disp"},
    {"column": 22, "spec": "trade", "full_name": "Recall", "short_name": "rec"},
    {"column": 23, "spec": "trade", "full_name": "Relic Drone", "short_name": "rdrone"},
    {
        "column": 24,
        "spec": "mining",
        "full_name": "Mining Boost",
        "short_name": "mboost",
    },
    {
        "column": 25,
        "spec": "mining",
        "full_name": "Hydrogen bay extension",
        "short_name": "hbe",
    },
    {"column": 26, "spec": "mining", "full_name": "Enrich", "short_name": "enr"},
    {"column": 27, "spec": "mining", "full_name": "Remote mining", "short_name": "rm"},
    {
        "column": 28,
        "spec": "mining",
        "full_name": "Hydrogen upload",
        "short_name": "hu",
    },
    {"column": 29, "spec": "mining", "full_name": "Mining Unity", "short_name": "mu"},
    {"column": 30, "spec": "mining", "full_name": "Crunch", "short_name": "cr"},
    {"column": 31, "spec": "mining", "full_name": "Genesis", "short_name": "gen"},
    {
        "column": 32,
        "spec": "mining",
        "full_name": "Hydrogen Rocket",
        "short_name": "hr",
    },
    {
        "column": 33,
        "spec": "mining",
        "full_name": "Mining Drone",
        "short_name": "mdrone",
    },
    {
        "column": 34,
        "spec": "weapons",
        "full_name": "Weak Battery",
        "short_name": "wbat",
    },
    {"column": 35, "spec": "weapons", "full_name": "Battery", "short_name": "bat"},
    {"column": 36, "spec": "weapons", "full_name": "Laser", "short_name": "las"},
    {
        "column": 37,
        "spec": "weapons",
        "full_name": "Mass battery",
        "short_name": "mbat",
    },
    {"column": 38, "spec": "weapons", "full_name": "Dual laser", "short_name": "dlas"},
    {"column": 39, "spec": "weapons", "full_name": "Barrage", "short_name": "barrage"},
    {
        "column": 40,
        "spec": "weapons",
        "full_name": "Dart Launcher",
        "short_name": "dart",
    },
    {"column": 41, "spec": "shields", "full_name": "Alpha Shield", "short_name": "as"},
    {
        "column": 42,
        "spec": "shields",
        "full_name": "Delta shield",
        "short_name": "delta",
    },
    {
        "column": 43,
        "spec": "shields",
        "full_name": "Passive shield",
        "short_name": "pass",
    },
    {
        "column": 44,
        "spec": "shields",
        "full_name": "Omega shield",
        "short_name": "omega",
    },
    {
        "column": 45,
        "spec": "shields",
        "full_name": "Mirror shield",
        "short_name": "mirror",
    },
    {
        "column": 46,
        "spec": "shields",
        "full_name": "Blast Shield",
        "short_name": "blast",
    },
    {"column": 47, "spec": "shields", "full_name": "Area shield", "short_name": "area"},
    {"column": 48, "spec": "support", "full_name": "EMP", "short_name": "emp"},
    {"column": 49, "spec": "support", "full_name": "Teleport", "short_name": "tp"},
    {
        "column": 50,
        "spec": "support",
        "full_name": "Red star life extender",
        "short_name": "rse",
    },
    {"column": 51, "spec": "support", "full_name": "Remote Repair", "short_name": "rr"},
    {"column": 52, "spec": "support", "full_name": "Time warp", "short_name": "tw"},
    {"column": 53, "spec": "support", "full_name": "Unity", "short_name": "unit"},
    {"column": 54, "spec": "support", "full_name": "Sanctuary", "short_name": "sanc"},
    {"column": 55, "spec": "support", "full_name": "Stealth", "short_name": "stealth"},
    {"column": 56, "spec": "support", "full_name": "Fortify", "short_name": "fort"},
    {"column": 57, "spec": "support", "full_name": "Impulse", "short_name": "imp"},
    {"column": 58, "spec": "support", "full_name": "Alpha Rocket", "short_name": "ar "},
    {"column": 59, "spec": "support", "full_name": "Salvage", "short_name": "salv"},
    {"column": 60, "spec": "support", "full_name": "Suppress", "short_name": "supp"},
    {"column": 61, "spec": "support", "full_name": "Destiny", "short_name": "dest"},
    {"column": 62, "spec": "support", "full_name": "Barrier", "short_name": "barr"},
    {"column": 63, "spec": "support", "full_name": "Vengeance", "short_name": "veng"},
    {"column": 64, "spec": "support", "full_name": "Delta Rocket", "short_name": "dr"},
    {"column": 65, "spec": "support", "full_name": "Leap", "short_name": "leap"},
    {"column": 66, "spec": "support", "full_name": "Bond", "short_name": "bond"},
    {"column": 67, "spec": "support", "full_name": "Laser Turret", "short_name": "lt"},
    {"column": 68, "spec": "support", "full_name": "Alpha Drone", "short_name": "ad"},
    {"column": 69, "spec": "support", "full_name": "Suspend", "short_name": "susp"},
    {"column": 70, "spec": "support", "full_name": "Omega Rocket", "short_name": "or"},
    {"column": 71, "spec": "support", "full_name": "Remote Bomb", "short_name": "rb"},
]

short_to_long = {}
for item in SHEET_CONFIG:
    short_to_long[item["short_name"]] = item["full_name"]

specialty = {}

for item in SHEET_CONFIG:
    if item["spec"] not in specialty:
        specialty[item["spec"]] = []
    specialty[item["spec"]].append(item["full_name"])


class Tech(Robin):
    """
    The class that gets tech info
    """

    def _tech_get(self, worksheet, user, module):
        """
        Get a specific module level
        """
        list_of_lists = worksheet.get_all_records()
        for item in list_of_lists:
            if item["Naam"] == user:
                mod_config = item
                pass
        return f"{module}: {mod_config[module]}"

    def _tech_get_specialty(self, worksheet, user, spec):
        """
        get all levels in a specific specialty
        """
        list_of_lists = worksheet.get_all_records()
        for item in list_of_lists:
            if item["Naam"] == user:
                mod_config = item
        msg = f"**{spec}** for **{user}**, laatst bijgewerkt: **{mod_config['Bijgewerkt']}**\n"
        for item in specialty[spec]:
            msg = msg + f"{item}: {mod_config[item]}\n"
        return msg

    def _tech_get_all(self, worksheet, user):
        """
        Just get all tech for a user
        """
        list_of_lists = worksheet.get_all_records()
        for item in list_of_lists:
            if item["Naam"] == user:
                mod_config = item
        msg = f"**Tech** for **{user}**, laatst bijgewerkt: **{mod_config['Bijgewerkt']}**\n"
        i = 0
        for item in mod_config:
            if i > 6 or i == 0:
                msg = msg + f"{item}: {mod_config[item]}\n"
            i = i + 1
        return msg

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
            f"**tech get discordnaam**             - geeft alle modules van een speler\n"
            f"**tech get discordnaam** modulenaam  - geeft het modulelevel van een speler\n"
            f"**tech get discordnaam** tech  - geeft de modules voor een bepaalde tech van een speler\n"
            f"     waar waar tech = [{specialty.keys()}]]"
            "\n"
            "\n"
        ),
    )
    async def tech(self, ctx, *args):
        """
        Get and display the tech levels for a user/group
        """
        if len(args) < 3:
            await ctx.send_help(ctx.command)
            return None
        action = args[0]
        user = args[1]
        # if user in ['ws1', 'ws2', 'ws3']:

        # else:
        usermap = self._getusermap_by_alias(user)
        logger.info(f"user {user}")
        logger.info(f"exists: {self._known_user(usermap['DiscordAlias'])}")
        if self._known_user(usermap["DiscordAlias"]):
            gc = gspread.service_account()
            wks = gc.open_by_key(os.getenv("GSHEET_ID"))
            worksheet = wks.worksheet("Modules")
            if len(args) == 3:
                module = args[2]
                if module in specialty:
                    msg = self._tech_get_specialty(
                        worksheet, usermap["GsheetAlias"], module
                    )
                else:
                    msg = self._tech_get(worksheet, usermap["GsheetAlias"], module)
            else:
                msg = self._tech_get_all(worksheet, usermap["GsheetAlias"])
        else:
            msg = "Speler is niet bekend, typo??"

        await feedback(ctx=ctx, msg=msg)
