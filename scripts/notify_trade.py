import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from services.notification_service import NotificationService
from models.position import Position
from datetime import datetime

pos = Position(
    symbol="XRPUSDT", side="short", quantity=69.735,
    entry_price=1.434, sl_price=1.4545, tp_price=1.39,
    strategy="Momentum Short - Distribution", confidence=7,
)
notifier = NotificationService()
ok = notifier.trade_opened(pos)
print("Sent" if ok else "Failed")
