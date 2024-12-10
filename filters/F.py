# filters/F.py
from dataclasses import dataclass
from typing import Any, Dict, List

import glom
from data.config import load_config

config = load_config()

# ADMIN_IDS dan foydalanishni to'g'rilaymiz
ADMINS = config.bot.admin_ids


@dataclass
class F:
    """Field accessor object"""

    path: str

    def resolve(self, data: Dict[str, Any]) -> Any:
        try:
            return glom.glom(data, self.path)
        except glom.PathAccessError:
            return None
