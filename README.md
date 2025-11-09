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

# verify conection

curl -X POST https://automatic.bnjm.site/webhook/b0e171b4-0b94-4353-be78-6c789e9991b6 \
-H "Content-Type: application/json" \
-d '{"test": "ping"}' -v




# graphql

## sillones

query GetSillon($idSillon: Int!) {
  sillon(idSillon: $idSillon) {
    idSillon
    ubicacionSala
    estado
    observaciones
     }
}
  
{
  "idSillon": 1
}


### subs

