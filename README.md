# Botto, a StarCraft 2 bot

[![Build Status](https://travis-ci.org/Vilsepi/sc2-botto.svg?branch=main)](https://travis-ci.org/Vilsepi/sc2-botto)

This bot plays [StarCraft 2](https://starcraft2.com/).

## Prerequisites

- [StarCraft 2](https://us.battle.net/account/sc2/starter-edition/) (tested on Windows 5.0.4)
- [Some maps](https://github.com/Blizzard/s2client-proto#downloads) (tested on Ladder 2017 Season 1 & 2)
- Python 3 (tested on 3.9.0)

Install dependencies (installing and enabling a virtualenv is strongly encouraged):

    pip install -r requirements.txt

## Running the bot

    ./run.sh

## Developing the bot

Install pre-commit hooks:

    pre-commit install

## Reference for developing a bot

- [python-sc2](https://github.com/BurnySc2/python-sc2) Python client library and its [documentation](https://burnysc2.github.io/python-sc2/docs/index.html)
- Blizzard's official [s2client-proto](https://github.com/Blizzard/s2client-proto) protocol definition
- [sharpy-sc2](https://github.com/DrInfy/sharpy-sc2) framework for rapid development of Starcraft 2 AI bots
- A list of [build orders](https://lotv.spawningtool.com/build/) to draw inspiration from
- [sc2ai](https://sc2ai.net/) and [AI arena](https://aiarena.net/) AI ladders
- Community Discord server [(invite link)](https://discord.gg/BH58ZVt)
