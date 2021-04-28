# discordbot
[![Build](https://github.com/rvegmond/discordbot/actions/workflows/01-test.yaml/badge.svg)](https://github.com/rvegmond/discordbot/actions/workflows/01-test.yaml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rvegmond_discordbot&metric=alert_status)](https://sonarcloud.io/dashboard?id=rvegmond_discordbot)  [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=rvegmond_discordbot&metric=coverage)](https://sonarcloud.io/dashboard?id=rvegmond_discordbot)

running the discordbot as a container, export your discord token and start docker-compose up.
There are two containers:
- gsheet, this is for updating the database
- bot, that is the actual bot where you interact with.

the data contains the sqlite3 database.
