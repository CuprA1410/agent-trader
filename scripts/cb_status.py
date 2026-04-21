import sys, json
sys.path.insert(0, '.')
from utils.circuit_breaker import CircuitBreaker
cb = CircuitBreaker()
print(json.dumps(cb.status(), indent=2))
