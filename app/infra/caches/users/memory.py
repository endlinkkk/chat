from dataclasses import dataclass, field

from infra.caches.users.base import BaseUserCache


@dataclass
class MemoryUserCache(BaseUserCache):
    _saved_codes: dict = field(default_factory=dict)

    async def add_code(self, phone: str, code: str):
        self._saved_codes[phone] = code

    async def delete_code(self, phone: str):
        del self._saved_codes[phone]

    async def check_code(self, phone: str, code: str) -> bool:
        return (
            code == self._saved_codes[phone] if self._saved_codes.get(phone) else False
        )
