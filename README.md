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



### other

🧪 Cuándo usar cada una (con ejemplos reales)
✔ AlreadyExistsException

Cuando intentas crear una alergia con un nombre que ya existe:

if await repo.exists_by_name(data.nombre_condicion):
    raise AlreadyExistsException("La condición ya existe.")

✔ NotFoundException

Cuando intentas actualizar/eliminar algo que no existe:

if registro is None:
    raise NotFoundException("La condición personal no existe.")

✔ InvalidStateException

Ejemplo: intentar cerrar un caso ya cerrado.

if entidad.estado == "cerrado":
    raise InvalidStateException("El caso ya está cerrado.")

✔ ValidationException

Reglas de negocio más allá del esquema:

if data.severidad and data.tipo != "alergia":
    raise ValidationException("La severidad solo aplica para alergias.")

✔ LimitExceededException

Ej: un paciente solo puede tener 50 condiciones registradas.

if count >= 50:
    raise LimitExceededException("Se ha alcanzado el límite máximo permitido.")

✔ DependencyMissingException

Ej: una condición requiere un paciente asociado:

if paciente is None:
    raise DependencyMissingException("No existe el paciente asociado.")

✔ ConflictException

Para reglas que chocan pero no implican duplicado:

if condicion_1.incompatible_con(condicion_2):
    raise ConflictException("Las condiciones seleccionadas son incompatibles.")

✔ ResourceLockedException

Ej: un examen que está siendo procesado.

if entidad.locked:
    raise ResourceLockedException("El recurso está bloqueado temporalmente.")

✔ OperationNotAllowedException

Ej: un usuario intenta borrar una condición que solo un administrador puede borrar.

if not user.is_admin:
    raise OperationNotAllowedException("No tienes permisos para eliminar esta condición.")


# production-test

sudo nano /etc/systemd/system/d4lia.service
sudo systemctl daemon-reload
sudo systemctl enable d4lia
sudo systemctl start d4lia
systemctl status d4lia
journalctl -u d4lia -f


# certbot 

server {
    listen 80;
    server_name dbdata4life.genomas.cl;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    access_log /var/log/nginx/data4life.access.log;
    error_log /var/log/nginx/data4life.error.log;
}