from dataclasses import dataclass, field
import json
from flask import jsonify


@dataclass
class PartylistColor:
    red: int = 0
    green: int = 0
    blue: int = 0
    alpha: float = 0.0

    def __post_init__(self):
        self.validate_values()

    def validate_values(self):
        if not 0 <= self.red <= 255:
            self.red %= 255
        if not 0 <= self.green <= 255:
            self.green %= 255
        if not 0 <= self.blue <= 255:
            self.blue %= 255
        if not 0.0 <= self.alpha <= 1.0:
            self.alpha %= 1.0

    @property
    def rgba(self):
        return (self.red, self.green, self.blue, self.alpha)


@dataclass
class JSONObject:
    data: list[dict] = field(default_factory=[])
    desc: str = ""

    @property
    def json_object_count(self):
        return len(self.data)

    @property
    def json_object(self):
        response = {"desc": self.desc, "count": self.json_object_count, "data": self.data}
        return jsonify(response)

@dataclass
class VoteData:
    region: str
    province: str
    position: str
    last_name: str
    first_name: str
    party: str
    votes: int

    # color: type[PartylistColor] = field(default_factory=PartylistColor().rgba)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def json_object(self):


        return {
            "region": self.region,
            "province": self.province,
            "position": self.position,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "party": self.party,
            "votes": self.votes,
            # "color": self.color,
        }
