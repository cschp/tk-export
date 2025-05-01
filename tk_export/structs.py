import typing
from dataclasses import dataclass
import datetime

@dataclass
class Settings:
    user_id: str
    cookie: typing.Dict[str, str]
    campaigns: typing.List[str]


@dataclass
class CharacterSheet:
    character: str

    def to_json(self) -> dict:
        return {
            'character': self.character
        }

    @staticmethod
    def from_json(data: dict) -> "CharacterSheet":
        if not data:
            return
        return CharacterSheet(character=data.get('character'))

@dataclass
class CharacterBio:
    background: str
    personality: str
    appearance: str

    def to_json(self) -> dict:
        return {
            'background': self.background,
            'personality': self.personality,
            'appearance': self.appearance
        }

    @staticmethod
    def from_json(data: dict) -> "CharacterBio":
        if not data:
            return
        return CharacterBio(background=data['background'],
                            personality=data['personality'],
                            appearance=data['appearance'])

@dataclass
class Character:
    id: int
    name: str
    quote: str
    nickname: str
    sheet: CharacterSheet
    bio: CharacterBio

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'quote': self.quote,
            'nickname': self.nickname,
            'sheet': self.sheet.to_json(),
            'bio': self.bio.to_json()
        }

    @staticmethod
    def from_json(data: dict) -> "Character":
        return Character(id=data['id'],
                         name=data['name'],
                         quote=data['quote'],
                         nickname=data['nickname'],
                         sheet=CharacterSheet.from_json(data.get('sheet')),
                         bio=CharacterBio.from_json(data.get('bio'))
                         )

@dataclass
class Campaign:
    created_at: datetime.datetime
    id: int
    name: str
    system_name: str

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.timestamp(),
            'system_name': self.system_name
        }

    @staticmethod
    def from_json(data: dict, is_nano: bool = False) -> "Campaign":
        created_timestamp = data['created_at'] / 1000 if is_nano else data['created_at']
        return Campaign(created_at=created_timestamp,
                        id=data['id'],
                        name=data['name'],
                        system_name=data['system_name'])

@dataclass
class Roleplay:
    created_at: datetime.datetime
    id: int
    name: str
    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.timestamp(),
        }

    @staticmethod
    def from_json(data: dict, is_nano: bool = False) -> "Roleplay":
        created_timestamp = data['created_at'] / 1000 if is_nano else data['created_at']
        return Roleplay(created_at=created_timestamp,
                        id=data['id'],
                        name=data['name'])

@dataclass
class RoleplayMessage:
    character: Character
    rerolls: int
    roll: typing.List[dict]
    content: str

    def to_json(self) -> dict:
        return {
            'character': self.character.to_json(),
            'rerolls': self.rerolls,
            'roll': self.roll,
            'content': self.content
        }

    @staticmethod
    def from_json(data: dict) -> "RoleplayMessage":
        character = Character.from_json(data['character'])
        return RoleplayMessage(character=character,
                               rerolls=data['rerolls'],
                               roll=data['roll'],
                               content=data['content'])