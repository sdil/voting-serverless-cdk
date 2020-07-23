from dataclasses import dataclass
from typing import List, Counter, Dict
from datetime import datetime


@dataclass
class Poll:
    __slots__ = ["id", "date", "question", "choices", "result", "user"]
    id: str
    date: datetime
    question: str
    choices: Dict[int, str]
    result: Counter[Dict[int, int]]
    user: str


@dataclass
class Vote:
    __slots__ = ["id", "date", "vote", "poll", "user"]
    id: str
    date: datetime
    poll: str
    vote: str
    user: str


@dataclass
class User:
    __slots__ = ["id", "date", "user"]
    id: str
    date: datetime
    user: str
