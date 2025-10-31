# d4lia

asyncpg

# mapear redis

ssh -L 6379:127.0.0.1:6379 ssh@genomas.cl -p 22222

# status worker

celery -A app.celery_app status

# conf worker 
celery -A app.celery_app worker --loglevel=info \
       --concurrency=4 \
       --max-tasks-per-child=50 \
       --max-memory-per-child=200000
