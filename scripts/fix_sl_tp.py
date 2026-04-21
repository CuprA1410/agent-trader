"""
Quick fix: place SL and TP for an already-open position using BitGet's plan order API.
Usage: python scripts/fix_sl_tp.py --symbol XRPUSDT --side short --qty 69.735 --sl 1.4545 --tp 1.39
"""
import sys, json, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from exchanges.exchange_factory import get_exchange

def ccxt_symbol(raw):
    if "/" in raw: return raw
    base = raw.upper().replace("USDT","").replace("PERP","")
    return f"{base}/USDT:USDT"

def place_sl_tp(symbol, side, qty, sl_price, tp_price):
    ex = get_exchange()
    sym = ccxt_symbol(symbol)
    close_side = "sell" if side == "long" else "buy"
    results = {}

    # Method 1: BitGet plan order for SL
    for label, trigger, plan_type in [("SL", sl_price, "profit_loss"), ("TP", tp_price, "profit_loss")]:
        for attempt_params in [
            # Attempt A: planType with triggerPrice
            {"planType": plan_type, "triggerPrice": str(trigger),
             "triggerType": "fill_price", "tradeSide": "close", "reduceOnly": True},
            # Attempt B: stopLoss/takeProfit nested
            {"tradeSide": "close", "reduceOnly": True,
             **({"stopLoss": {"triggerPrice": str(trigger), "type": "fill_price"}} if label == "SL"
                else {"takeProfit": {"triggerPrice": str(trigger), "type": "fill_price"}})},
            # Attempt C: simple stop params
            {"stopPrice": trigger, "tradeSide": "close", "reduceOnly": True},
        ]:
            try:
                order = ex.create_order(
                    symbol=sym, type="market", side=close_side,
                    amount=qty, params=attempt_params,
                )
                results[label] = {"status": "OK", "order_id": order.get("id"), "params_used": attempt_params}
                break
            except Exception as e:
                results[label] = {"status": "FAIL", "error": str(e), "params": attempt_params}

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", required=True)
    p.add_argument("--side",   required=True)
    p.add_argument("--qty",    required=True, type=float)
    p.add_argument("--sl",     required=True, type=float)
    p.add_argument("--tp",     required=True, type=float)
    args = p.parse_args()
    place_sl_tp(args.symbol, args.side, args.qty, args.sl, args.tp)
