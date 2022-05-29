from dataclasses_json import dataclass_json
from dataclasses import dataclass
from typing import List, Dict
import os

@dataclass_json(undefined='EXCLUDE')
@dataclass
class Contributor:
    name: str
    avatar_url: str
    contributions: List[str]

@dataclass_json(undefined='EXCLUDE')
@dataclass
class Config:
    guild_id: str
    contributors_role: str
    role_name_map: Dict[str, str]

def load_config() -> Config:
    path = 'config.json'
    if os.path.exists('config.override.json'):
        path = 'config.override.json'
    with open(path) as f:
        return Config.from_json(f.read())
