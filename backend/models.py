from typing import Counter, Dict, List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime
from marshmallow import fields


@dataclass_json
@dataclass
class Poll:
    id: str
    date: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    question: str
    result: Counter[Dict[str, int]]
    user: str = None


@dataclass_json
@dataclass
class Vote:
    id: str
    date: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    poll: str
    answer: str
    user: str = None


@dataclass
class User:
    id: str
    date: datetime
    user: str
