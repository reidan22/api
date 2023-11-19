from collections import defaultdict
from dataclasses import dataclass, field
import os

from app.utils.utils import read_parquet_to_df


@dataclass
class ColorInfo:
    r: int
    g: int
    b: int

    def __post_init__(self):
        self.validate_color_range(self.r, "r")
        self.validate_color_range(self.g, "g")
        self.validate_color_range(self.b, "b")

    @staticmethod
    def validate_color_range(value: int, color_name: str):
        if not (0 <= value <= 255):
            raise ValueError(f"{color_name} value must be between 0 and 255.")

    def get_rgb(self):
        return (self.r, self.g, self.b)

    def get_rgb_string(self):
        return str(self.get_rgb())


@dataclass
class CandidateInfo:
    first_name: str
    last_name: str
    position: str
    party: str
    campaign_color: ColorInfo or None = None
    regions: dict[str,int] or None = None
    provinces: dict[str,int] or None = None

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def clear_unneeded_attrs(self):
        self.region = None
        self.province = None
        self.votes = 0

    def get_total_votes(self):
        votes = sum([votes for votes in self.provinces.values()])
        return votes
    
    @property
    def total_votes(self):
        return self.get_total_votes()
    
    @property
    def full_name(self):
        return self.get_full_name()
    
    def to_json(self):
        res = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "position": self.position,
            "party": self.party,
            "color": self.campaign_color,
            "total_votes": self.total_votes,
            "votes_per_region":self.regions,
            "votes_per_province":self.provinces,
        }
        return res    
current_file_dir = os.path.dirname(__file__)
election_parquet_file_dir = os.path.join(current_file_dir, "../../src/election_data")
parquet_file_path = os.path.join(election_parquet_file_dir, "summarized_data.parquet")

ELECTIONS_DF = read_parquet_to_df(parquet_file_path)
# export PYTHONPATH=$PYTHONPATH:.
POSITIONS = ELECTIONS_DF.position.unique()
REGIONS = ELECTIONS_DF.region.unique()
PROVINCES = ELECTIONS_DF.province.unique()
PARTIES = ELECTIONS_DF.party.unique()
FIRST_NAMES = ELECTIONS_DF.first_name.unique()
LAST_NAMES = ELECTIONS_DF.last_name.unique()

RAW_DATA_DICT = {
    "position": list(POSITIONS),
    "region": list(REGIONS),
    "province": list(PROVINCES),
    "party": list(PARTIES),
    "first_name": list(FIRST_NAMES),
    "last_name": list(LAST_NAMES),
}

CANDIDATE_INFOS : list[CandidateInfo] = {}
for data in ELECTIONS_DF.values.tolist():
    region, province, position, last_name, first_name, party, votes = data
    candidate_info = CandidateInfo(
        last_name=last_name,
        first_name=first_name,
        position=position,
        party=party,
    )
    full_name = candidate_info.get_full_name()
    if full_name not in CANDIDATE_INFOS:
        CANDIDATE_INFOS[full_name] = candidate_info
        CANDIDATE_INFOS[full_name].regions = defaultdict(int)
        CANDIDATE_INFOS[full_name].provinces = defaultdict(int)

    CANDIDATE_INFOS[full_name].regions[region] += votes
    CANDIDATE_INFOS[full_name].provinces[province] += votes

