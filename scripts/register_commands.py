#!/usr/bin/env python3

import httpx, os, orjson, sys

from dotenv import load_dotenv

load_dotenv()
APP_ID = os.environ["DISCORD_APP_ID"]
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
GUILD_ID = os.environ.get("DISCORD_GUILD_ID")

commands = [
    {
      "name": "roll",
      "description": "Roll dice, e.g., 2d6+3",
      "options": [
        {"name": "expr", "description": "Dice expression", "type": 3, "required": False},
        {"name": "advantage", "description": "Advantage", "type": 5, "required": False},
        {"name": "disadvantage", "description": "Disadvantage", "type": 5, "required": False},
      ]
    },
    {
      "name": "check",
      "description": "Ability check vs DC",
      "options": [
        {"name": "ability", "description":"STR/DEX/CON/INT/WIS/CHA", "type":3, "required":False},
        {"name": "score", "description":"Ability score (10 default)", "type":4, "required":False},
        {"name": "proficient", "description":"Proficient?", "type":5, "required":False},
        {"name": "expertise", "description":"Expertise?", "type":5, "required":False},
        {"name": "prof_bonus", "description":"Proficiency bonus", "type":4, "required":False},
        {"name": "dc", "description":"Difficulty Class", "type":4, "required":False},
        {"name": "advantage", "description":"Advantage", "type":5, "required":False},
        {"name": "disadvantage", "description":"Disadvantage", "type":5, "required":False},
      ]
    },
    {
      "name": "sheet",
      "description": "Character sheet operations",
      "options": [
        {
          "name": "create",
          "description": "Create or update a sheet from JSON",
          "type": 1,  # SUB_COMMAND
          "options": [
            {"name":"json","description":"JSON sheet payload","type":3,"required":True}
          ]
        },
        {
          "name": "show",
          "description": "Show a sheet by name",
          "type": 1,
          "options": [
            {"name":"name","description":"Character name","type":3,"required":True}
          ]
        }
      ]
    }
]

async def main():
#    url = f"https://discord.com/api/v10/applications/{APP_ID}/guilds/{GUILD_ID}/commands"
    url = f"https://discord.com/api/v10/applications/{APP_ID}/commands"
    headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=10) as client:
        for cmd in commands:
            r = await client.post(url, headers=headers, content=orjson.dumps(cmd))
            r.raise_for_status()
            print("Registered:", r.json()["name"])

if __name__ == "__main__":
    import asyncio
    print("AIcat!")
    asyncio.run(main())
