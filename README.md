# Space Trader

[![license](https://badgen.net/github/license/RPINerd/Space-Trader)](https://github.com/RPINerd/Space-Trader/blob/main/docs/LICENSE)
![commits](https://badgen.net/github/commits/RPINerd/Space-Trader?color=purple&icon=github)
![forks](https://badgen.net/github/forks/RPINerd/Space-Trader?color=green&icon=git)
![commits](https://badgen.net/github/last-commit/RPINerd/Space-Trader?color=cyan&icon=codebeat)
![dependabot](https://badgen.net/github/dependabot/RPINerd/Space-Trader?color=yellow)

An elite-inspired space trading RPG originally on PalmOS.

## Project Goals

There is currently another active (and I believe playable?) project to re-create Space Trader into a python native, modern game. I am following it with keen interest but have created this repository to follow a different path.  

My goal is to recreate the original Space Trader game as closely as possible, with the same mechanics and gameplay, but most crucially with the same look and feel. I grew up playing on my dads' Palm V and I want to recreate that experience as closely as possible.  

To this end, my build will conform only to the state of the game as it existed in version 1.2.0/1 for PalmOS. I'm using lots of others' ports and remakes as reference but the logic should follow as nearly identically as possible to the original game.

## Overview

Space Trader is a complex game, in which the player's aim is to amass enough money to be able to buy a moon to retire to. The player starts out with a small space ship, armed with one simple laser, and 1000 credits in cash.  

The safest and easiest way to earn money is to trade goods between neighbouring solar systems. If the player chooses the goods to trade wisely, it isn't too difficult to sell them with a profit. There are other ways to get rich, though. You might become a bounty hunter and hunt down pirates.  

It is also possible to become a pirate yourself and rob honest traders of their cargo. Beware, though: pirating is a way to get rich quickly, but the police force will go after you.

## Gameplay Features

- Ten different trade goods are available, two of which are considered to be illegal but can bring great profits.
- Ten different ship types are available, some of which are especially suitable for trading, some for pirating, and others for both. Ships differ in size, the distance they can travel, their hull strength, the number of weapons, shields and gadgets they can carry, the number of cargo bays and the number of crew quarters that are available.
- Ships can be equipped with different selections of equipment, among which are several types of lasers, several types of shields, an escape pod and certain special gadgets like a cloaking device.
- You can distribute skill points over your character at the start of the game, to allow you to function well in your chosen role. For the skills your character lacks, mercenaries can be hired which may have different skills.
- There are more than a hundred solar systems in the galaxy, with different sizes, tech levels, governments, resources and special situations. These are not just for background color, but play a vital role in the game.
- While travelling to another solar system, you might encounter police ships, pirates and other traders. There are several ways to handle such encounters. You can even force a trader to allow you to plunder his ship.
- There are about a dozen unique missions and offers available, some of which may bring great special rewards.
- The ships are displayed graphically during an encounter. There are also large pictures during key moments of the game.

## Screenshots

Someday something beautiful will be here!

## Requirements

Game is being built with Python 3.12.x but other than python, there are no dependencies!

## How to Play

Currently the game is barely into development, but you can see the progress by running the main file `python spacetrader.py`

I recomend using a virtual environment to run the game, as it will help keep your system clean and prevent any conflicts with other python projects.

## Credits

### Pieter Sproncks

Original author of Space Trader for PalmOS

### Jay French

Author of the [Space Trader for Windows](https://github.com/SpaceTraderGame/SpaceTrader-Windows) port

### Additional Inspirations

Benjamin Schieder aka [blind-coder](https://github.com/blind-coder) - Author and maintainer of [Space Trader, Android port](https://github.com/blind-coder/SpaceTrader)  
[Official site](https://www.benjamin-schieder.de/)

[Video Game Preservation](https://github.com/videogamepreservation) - Host of the original [Space Trader PalmOS source code](https://github.com/videogamepreservation/spacetrader)  

[Andrew Nelson](https://github.com/werdnanoslen/space-trader), [Leonis](https://github.com/LeonisX/space-trader), [GruiicK](https://github.com/gruiick/pySpaceTrader) - Authors of various Space Trader remakes and ports
