import dataclasses


@dataclasses.dataclass
class Article:
    title: str
    link: str
    site: str
    points: int
    comments: int
