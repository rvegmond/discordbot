#!/usr/bin/env python

import gspread
import sqlite3
from datetime import datetime
from icecream import ic
from modules import ws, db, utils, members

import base64
import boto3
import json
from botocore.exceptions import ClientError

gc_prd = boto3.session.Session(profile_name="gc-prd")
sqs_client = gc_prd.client("sqs")

db.session = db.init("sqlite:///../data/hades.db")


def add_gsheet_row(row):
    if " leeg" not in row[1]:
        try:
            r_datetime = row[2].split("-")
            # ic(r_datetime)
            r_datetime = datetime.strptime(
                f"{r_datetime[0]:0>2}-{r_datetime[1]:0>2}-{r_datetime[2]:0>2}",
                "%d-%m-%Y",
            )
            # ic(r_datetime)
            new_row = db.Gsheet(
                influence=row[0],
                Naam=row[1],
                Bijgewerkt=r_datetime,
                CreditCap=row[3],
                task=row[4],
                WhitStar=row[5],
                Transport=row[6],
                TotalCargoSlots=row[7],
                Miner=row[8],
                HydrogenCapacity=row[9],
                Battleship=row[10],
                CargoBayExtension=row[11],
                ShipmentComputer=row[12],
                TradeBoost=row[13],
                Rush=row[14],
                TradeBurst=row[15],
                ShipmentDrone=row[16],
                Offload=row[17],
                ShipmentBeam=row[18],
                Entrust=row[19],
                Dispatch=row[20],
                Recall=row[21],
                RelicDrone=row[22],
                MiningBoost=row[23],
                HydrogenBayExtension=row[24],
                Enrich=row[25],
                RemoteMining=row[26],
                HydrogenUpload=row[27],
                MiningUnity=row[28],
                Crunch=row[29],
                Genesis=row[30],
                HydrogenRocket=row[31],
                MiningDrone=row[32],
                WeakBattery=row[33],
                Battery=row[34],
                Laser=row[35],
                MassBattery=row[36],
                DualLaser=row[37],
                Barrage=row[38],
                DartLauncher=row[39],
                AlphaShield=row[40],
                DeltaShield=row[41],
                PassiveShield=row[42],
                OmegaShield=row[43],
                MirrorShield=row[44],
                BlastShield=row[45],
                AreaShield=row[46],
                EMP=row[47],
                Teleport=row[48],
                RedStarLifeExtender=row[49],
                RemoteRepair=row[50],
                TimeWarp=row[51],
                Unity=row[52],
                Sanctuary=row[53],
                Stealth=row[54],
                Fortify=row[55],
                Impulse=row[56],
                AlphaRocket=row[57],
                Salvage=row[58],
                Suppress=row[59],
                Destiny=row[60],
                Barrier=row[61],
                Vengeance=row[62],
                DeltaRocket=row[63],
                Leap=row[64],
                Bond=row[65],
                LaserTurret=row[66],
                AlphaDrone=row[67],
                Suspend=row[68],
                OmegaRocket=row[69],
                RemoteBomb=row[70],
            )
            db.session.merge(new_row)
            db.session.commit()
        except IndexError:
            ic(f"insert failed for {row[1]}")


def insert_gsheet_into_table(worksheet):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    for row in worksheet.get_all_values()[1:]:
        # ic(row)
        add_gsheet_row(row)

    # new_user = db.User(
    #     UserId=member.id, DiscordAlias=membername, LastChannel=channel.name
    # )
    # db.session.add(new_user)
    # list_of_lists = worksheet.get_all_values()
    # cur = conn.cursor()
    # query = "delete from gsheet"
    # cur.execute(query)

    # query = "insert into gsheet values (?"
    # for i in range(len(header_list)):
    #     query += ", ?"
    # query += ")"
    # # print("query: {}".format(query))
    # for idx, item in enumerate(list_of_lists):
    #     # ic(item)
    #     item.insert(0, idx)
    #     # ic(item)
    #     # ic(len(item))
    #     result = cur.execute(query, item)
    #     # print("{}".format(result))
    # conn.commit()


def update_table():
    more_messages = True
    while more_messages:
        received_messages = sqs_client.receive_message(
            QueueUrl="https://sqs.eu-west-1.amazonaws.com/686403619219/gc-robin-queue",
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=2,
        )
        # for message in received_messages:
        #     path, body, line = unpack_message(message)
        #     received_lines[line] = body
        # if received_messages:
        #     delete_messages(queue, received_messages)
        # else:
        # ic(received_messages)
        if "Messages" in received_messages:
            for message in received_messages["Messages"]:
                #      print(f"{type(dict(base64.b64decode(message['Body'])))}")
                row_dict = json.loads(base64.b64decode(message["Body"]).decode("utf-8"))
                print(f"{row_dict}")
                print(f"{row_dict.values()}")
                row_dict.pop("id")
                print(f"{row_dict}")
                print(f"{row_dict.values()}")
                row_dict.pop("row")
                print(f"{row_dict}")
                print(f"{row_dict.values()}")
                row_dict.pop("_content_hash")
                print(f"{row_dict}")
                print(f"{row_dict.values()}")
                add_gsheet_row(list(row_dict.values()))
        else:
            more_messages = False


def main():
    gc = gspread.service_account()

    # Open a sheet from a spreadsheet in one go
    wks = gc.open("Hades Star Spreadsheet")
    # Update a range of cells using the top left corner address
    worksheet = wks.worksheet("Modules")

    insert_gsheet_into_table(worksheet)
    update_table()


if __name__ == "__main__":
    main()
