"""Save the already-placed XRP short to the position repository."""
import sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.position import Position
from repositories.position_repository import PositionRepository

pos = Position(
    symbol="XRPUSDT",
    side="short",
    quantity=69.735,
    entry_price=1.434,
    sl_price=1.4545,
    tp_price=1.39,
    strategy="Momentum Short - Distribution",
    confidence=7,
    order_id="1429361458306711553",
    sl_order_id="1429361625005584384",
    tp_order_id="1429361628369403904",
    opened_at=datetime(2026, 4, 18, 14, 37, 28),
)

repo = PositionRepository()
repo.save(pos)
print(f"Saved: {pos.symbol} {pos.side} qty={pos.quantity} entry={pos.entry_price}")
