#!/usr/bin/env bash

# Copy this file to ./run_<environment>.sh, add the environment parameters to the new file and remove the next line
!!! Don't edit this file  !!!!


export DISCORD_TOKEN=       # Your discord token 
export STATUS_CHANNEL=      # The id (numeric) of your status channel
export COMMAND_PREFIX=';'   # the command prefix
export WSIN_CHANNEL=        # The channel where members can post their ws subscriptions
export WSLIST_CHANNEL=      # The channel where the list of members will be posted.

pipenv run python ./__init__.py
