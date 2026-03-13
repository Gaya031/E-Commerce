# RushCart Testing Guide

## 1) Local build checks

### Backend
```bash
cd Backend
source venv/bin/activate
python -m compileall -q app
pytest -q --cov=app --cov-report=term-missing
```

### Frontend
```bash
cd Frontend
npm run lint
npm run build
```

### Delivery Service
```bash
cd Delivery-Service
node --check src/server.js
```

## 2) Docker smoke run
```bash
docker compose up --build
```

Important URLs:
- Backend API: `http://localhost:8000/api/v1`
- Frontend: `http://localhost:5173`
- Delivery Service: `http://localhost:4001`

## 3) Health and metrics
- Liveness: `GET /api/v1/system/health/live`
- Readiness: `GET /api/v1/system/health/ready`
- JSON metrics: `GET /api/v1/system/metrics`
- Prometheus metrics: `GET /api/v1/system/metrics/prometheus`

## 4) Resilience smoke checker
```bash
cd Backend
source venv/bin/activate
python scripts/resilience_check.py --base-url http://localhost:8000/api/v1 --iterations 80 --concurrency 10
python scripts/load_test.py --base-url http://localhost:8000/api/v1 --iterations 500 --concurrency 25
```

## 5) Chaos / Failover checks
```bash
docker compose stop redis
python Backend/scripts/failover_check.py --base-url http://localhost:8000/api/v1 --expect degraded --timeout-seconds 60
docker compose start redis
python Backend/scripts/failover_check.py --base-url http://localhost:8000/api/v1 --expect ready --timeout-seconds 90
```

## 6) Security review checks
```bash
cd Backend
source venv/bin/activate
pip install bandit pip-audit
bandit -q -r app
pip-audit -r requirements.txt

cd ../Frontend
npm audit --audit-level=high
cd ../Delivery-Service
npm audit --audit-level=high
```

## 7) Banner slider validation
1. Login as admin.
2. Open `Admin -> Homepage Banners`.
3. Upload an image and create a banner.
4. Verify banner appears on buyer home hero slider.
