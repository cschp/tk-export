import typing
from dataclasses import dataclass
import datetime

@dataclass
class settings:
    user_id: str
    cookie: str
    campaigns: typing.List[str]


@dataclass
class character_sheet:
    character: str

    def to_json(self) -> dict:
        return {
            'character': self.character
        }

    @staticmethod
    def from_json(data: dict) -> "character_sheet":
        return character_sheet(character=data['character'])

@dataclass
class character_bio:
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
    def from_json(data: dict) -> "character_bio":
        return character_bio(background=data['background'],
                            personality=data['personality'],
                            appearance=data['appearance'])

@dataclass
class character:
    id: int
    name: str
    quote: str
    nickname: str
    sheet: character_sheet
    bio: character_bio

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
    def from_json(data: dict) -> "character":
        return character(id=data['id'],
                         name=data['name'],
                         quote=data['quote'],
                         nickname=data['nickname'],
                         sheet=character_sheet.from_json(data['sheet']),
                         bio=character_bio.from_json(data['bio'])
        )

@dataclass
class campaign:
    created_at: datetime.datetime
    id: int
    name: str
    system_name: str

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'system_name': self.system_name
        }

    @staticmethod
    def from_json(data: dict) -> "campaign":
        return campaign(created_at=datetime.datetime.fromisoformat(data['created_at']),
                        id=data['id'],
                        name=data['name'],
                        system_name=data['system_name'])


