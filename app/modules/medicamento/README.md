# Módulo Medicamento - Documentación Rápida

## 📦 Archivos Creados

- ✅ [medicamento_entity.py](file:///home/fermin/d4lia/app/modules/medicamento/entities/medicamento_entity.py) - Entidad de dominio
- ✅ [medicamento_schema.py](file:///home/fermin/d4lia/app/modules/medicamento/schemas/medicamento_schema.py) - Schemas Pydantic
- ✅ [medicamento_interfaces.py](file:///home/fermin/d4lia/app/modules/medicamento/interfaces/medicamento_interfaces.py) - Interface del repositorio
- ✅ [medicamento_repository.py](file:///home/fermin/d4lia/app/modules/medicamento/repositories/medicamento_repository.py) - Repositorio con queries SQL
- ✅ [medicamento_service.py](file:///home/fermin/d4lia/app/modules/medicamento/services/medicamento_service.py) - Lógica de negocio
- ✅ [medicamento_controller.py](file:///home/fermin/d4lia/app/modules/medicamento/controllers/medicamento_controller.py) - Endpoints REST

## 🔌 Endpoints Disponibles

### CRUD Básico
```
GET    /medicamento/              - Listar todos los medicamentos
POST   /medicamento/              - Crear medicamento
GET    /medicamento/{id}          - Obtener medicamento por ID
PATCH  /medicamento/{id}          - Actualizar medicamento
DELETE /medicamento/{id}          - Eliminar medicamento
```

### Consultas Especializadas
```
GET    /medicamento/stock/bajo?umbral=10           - Medicamentos con stock bajo
GET    /medicamento/laboratorio/{laboratorio}      - Medicamentos por laboratorio
```

## 📊 Campos del Medicamento

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `nombre_comercial` | string | ✅ Sí | Nombre comercial del medicamento |
| `nombre_generico` | string | ❌ No | Nombre genérico |
| `concentracion` | string | ❌ No | Concentración (ej: "500mg") |
| `forma_farmaceutica` | string | ❌ No | Forma (ej: "comprimido", "jarabe") |
| `via_administracion` | string | ❌ No | Vía (ej: "oral", "intravenosa") |
| `laboratorio` | string | ❌ No | Laboratorio fabricante |
| `requiere_receta` | boolean | ❌ No | Default: `true` |
| `stock_disponible` | integer | ❌ No | Default: `0` (≥ 0) |
| `observaciones` | string | ❌ No | Notas adicionales |

## 🧪 Ejemplos de Uso

### Crear medicamento
```bash
curl -X POST http://localhost:8000/medicamento/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_comercial": "Paracetamol 500mg",
    "nombre_generico": "Paracetamol",
    "concentracion": "500mg",
    "forma_farmaceutica": "Comprimido",
    "via_administracion": "Oral",
    "laboratorio": "Laboratorio XYZ",
    "requiere_receta": false,
    "stock_disponible": 100,
    "observaciones": "Analgésico y antipirético"
  }'
```

### Listar medicamentos con stock bajo
```bash
curl "http://localhost:8000/medicamento/stock/bajo?umbral=20"
```

### Buscar por laboratorio
```bash
curl http://localhost:8000/medicamento/laboratorio/Pfizer
```

### Actualizar stock
```bash
curl -X PATCH http://localhost:8000/medicamento/1 \
  -H "Content-Type: application/json" \
  -d '{
    "stock_disponible": 50
  }'
```

## ✨ Métodos de Negocio

La entidad `Medicamento` incluye métodos útiles:

- `tiene_stock()` - Verifica si hay stock disponible
- `es_controlado()` - Indica si requiere receta
- `stock_bajo(umbral)` - Verifica si el stock está bajo
- `descripcion_completa()` - Genera descripción formateada

## 🔒 Validaciones

- ✅ Nombre comercial obligatorio y no vacío
- ✅ Stock no puede ser negativo
- ✅ Prevención de nombres comerciales duplicados
- ✅ Validación en creación y actualización

## 🚀 Para Probar

```bash
# Reconstruir Docker
docker compose down && docker compose up --build -d

# Ver documentación interactiva
curl http://localhost:8000/docs
```

## 📝 Notas

- Compatible con la tabla `medicamento` existente en la BD
- Sigue el mismo patrón DDD que los otros módulos
- Incluye queries especializadas para gestión de inventario
