import json
from dataclasses import dataclass


@dataclass
class Response:
    status_code: int
    content: bytes
    text: str
    cookies: dict
    headers: dict

    def json(self):
        try:
            return json.loads(self.text)
        except json.JSONDecodeError:
            return None
