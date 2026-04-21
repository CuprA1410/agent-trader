import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from services.notification_service import NotificationService
from models.position import Position

pos = Position(
    symbol="ETHUSDT", side="short", quantity=0.042553,
    entry_price=2350, sl_price=2381, tp_price=2285,
    strategy="Momentum Short - Distribution", confidence=7,
)
notifier = NotificationService()
ok = notifier.trade_opened(pos)
print("Sent" if ok else "Failed")
