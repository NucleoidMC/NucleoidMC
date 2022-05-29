import os
from typing import Dict, Optional, List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import requests
import json
from common import Config, load_config, Contributor

@dataclass_json(undefined='EXCLUDE')
@dataclass
class DiscordUser:
    id: str
    username: str
    discriminator: str
    avatar: Optional[str] = None
    bot: bool = False

@dataclass_json(undefined='EXCLUDE')
@dataclass
class DiscordMember:
    user: DiscordUser
    roles: List[str]

def list_discord_members(bot_token: str, guild_id: str) -> List[DiscordMember]:
    res = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000', headers={
        'Authorization': f'Bot {bot_token}',
    })
    body = res.json()
    members = DiscordMember.schema().load(body, many=True)
    return members

def discord_avatar_url(user: DiscordUser) -> str:
    if user.avatar:
        return f'https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png'
    else:
        return f'https://cdn.discordapp.com/embed/avatars/{int(user.discriminator) % 5}.png'

def main():
    config = load_config()
    contributors: List[Contributor] = []
    for member in list_discord_members(bot_token=os.environ.get('BOT_TOKEN'), guild_id=config.guild_id):
        if config.contributors_role in member.roles:
            contributions = []
            for role_id, name in config.role_name_map.items():
                if role_id in member.roles:
                    contributions.append(name)
            if len(contributions) == 0:
                contributions.append('Other')
            contributors.append(Contributor(
                name=(member.user.username + '#' + member.user.discriminator),
                avatar_url=discord_avatar_url(user=member.user),
                contributions=contributions,
            ))
    with open('contributors.discord.json', 'w') as f:
        json.dump(Contributor.schema().dump(contributors, many=True), f)

if __name__ == '__main__':
    main()
