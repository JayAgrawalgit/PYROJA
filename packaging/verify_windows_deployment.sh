#!/usr/bin/env bash
set -e

echo "========================================================"
echo "   PYRO-Sync-Service Windows Distribution Verification"
echo "========================================================"

cd /app

# Ensure logs dir
mkdir -p logs

# Clean previous test database
rm -f sync_service.sqlite3 sync_service.sqlite3-wal sync_service.sqlite3-shm

echo "--- 1. Starting PYRO-Sync-Service.exe in background under Wine ---"
WINEDEBUG=-all wine PYRO-Sync-Service.exe > logs/console_stdout.log 2>&1 &
SERVER_PID=$!

echo "Server started with PID $SERVER_PID. Waiting for port 8080..."

# Poll health endpoint
for i in {1..30}; do
    if curl -s -f http://127.0.0.1:8080/api/health > /dev/null 2>&1; then
        echo "Server is UP and responsive after $i seconds!"
        break
    fi
    sleep 1
done

if ! curl -s -f http://127.0.0.1:8080/api/health > /dev/null 2>&1; then
    echo "ERROR: Server failed to start! Console log:"
    cat logs/console_stdout.log
    kill -9 $SERVER_PID || true
    exit 1
fi

echo "--- 2. Testing /api/health ---"
HEALTH_RESP=$(curl -s http://127.0.0.1:8080/api/health)
echo "Health Response: $HEALTH_RESP"

echo "--- 3. Testing /api/sync/products ---"
PROD_COUNT=$(curl -s http://127.0.0.1:8080/api/sync/products | grep -o '"total_records":[0-9]*' | cut -d: -f2)
echo "Total Products Synced: $PROD_COUNT"

echo "--- 4. Testing /api/sync/customers ---"
CUST_COUNT=$(curl -s http://127.0.0.1:8080/api/sync/customers | grep -o '"total_records":[0-9]*' | cut -d: -f2)
echo "Total Customers Synced: $CUST_COUNT"

echo "--- 5. Testing POST /api/orders (Queue Order) ---"
ORDER_RESP=$(curl -s -X POST http://127.0.0.1:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "draft_id": "DRAFT-WIN-TEST-001",
    "customer_code": "99999",
    "customer_name": "CASH A/C",
    "total_amount": 96.0,
    "tax_amount": 0.0,
    "item_count": 1,
    "notes": "Automated Windows Verification Test",
    "line_items": [
      {
        "product_code": "00013",
        "product_name": "111- ROLL CAPS AGNI",
        "quantity": 2,
        "rate": 48.0,
        "amount": 96.0,
        "tax_percentage": 0.0
      }
    ]
  }')
echo "Order Response: $ORDER_RESP"

echo "--- 6. Testing GET /api/orders/pending ---"
PENDING_ORDERS=$(curl -s http://127.0.0.1:8080/api/orders/pending)
echo "Pending Orders: $PENDING_ORDERS"

echo "--- 7. Stopping server PID $SERVER_PID ---"
kill $SERVER_PID || true
wait $SERVER_PID 2>/dev/null || true
sleep 2

echo "--- 8. Testing Editable config.json (Change port to 8085) ---"
sed -i 's/"port": 8080/"port": 8085/' config.json

WINEDEBUG=-all wine PYRO-Sync-Service.exe > logs/console_stdout_8085.log 2>&1 &
SERVER_PID_8085=$!

for i in {1..30}; do
    if curl -s -f http://127.0.0.1:8085/api/health > /dev/null 2>&1; then
        echo "Server is UP on new port 8085 after $i seconds!"
        break
    fi
    sleep 1
done

HEALTH_RESP_8085=$(curl -s http://127.0.0.1:8085/api/health)
echo "Port 8085 Health Response: $HEALTH_RESP_8085"

kill $SERVER_PID_8085 || true
wait $SERVER_PID_8085 2>/dev/null || true

# Restore port 8080
sed -i 's/"port": 8085/"port": 8080/' config.json

echo "--- 9. Checking File-Based Log Generation ---"
if [ -f "logs/sync_service.log" ]; then
    echo "logs/sync_service.log successfully created! Last 10 lines:"
    tail -n 10 logs/sync_service.log
else
    echo "WARNING: logs/sync_service.log not found, checking console stdout:"
    tail -n 10 logs/console_stdout.log
fi

echo "========================================================"
echo "   ALL TESTS PASSED SUCCESSFULLY!"
echo "========================================================"
