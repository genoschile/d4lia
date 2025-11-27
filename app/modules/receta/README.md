# Módulos Receta y Receta_Medicamento - Documentación

## 📦 Módulos Implementados

### 1. Módulo Receta
Gestión de recetas médicas con relaciones a paciente, médico y consulta médica.

**Archivos creados:**
- ✅ [receta_entity.py](file:///home/fermin/d4lia/app/modules/receta/entities/receta_entity.py)
- ✅ [receta_schema.py](file:///home/fermin/d4lia/app/modules/receta/schemas/receta_schema.py)
- ✅ [receta_interfaces.py](file:///home/fermin/d4lia/app/modules/receta/interfaces/receta_interfaces.py)
- ✅ [receta_repository.py](file:///home/fermin/d4lia/app/modules/receta/repositories/receta_repository.py)
- ✅ [receta_service.py](file:///home/fermin/d4lia/app/modules/receta/services/receta_service.py)
- ✅ [receta_controller.py](file:///home/fermin/d4lia/app/modules/receta/controllers/receta_controller.py)

### 2. Módulo Receta_Medicamento
Relación many-to-many entre receta y medicamento con detalles de prescripción.

**Archivos creados:**
- ✅ [receta_medicamento_entity.py](file:///home/fermin/d4lia/app/modules/receta_medicamento/entities/receta_medicamento_entity.py)
- ✅ [receta_medicamento_schema.py](file:///home/fermin/d4lia/app/modules/receta_medicamento/schemas/receta_medicamento_schema.py)
- ✅ [receta_medicamento_interfaces.py](file:///home/fermin/d4lia/app/modules/receta_medicamento/interfaces/receta_medicamento_interfaces.py)
- ✅ [receta_medicamento_repository.py](file:///home/fermin/d4lia/app/modules/receta_medicamento/repositories/receta_medicamento_repository.py)
- ✅ [receta_medicamento_service.py](file:///home/fermin/d4lia/app/modules/receta_medicamento/services/receta_medicamento_service.py)
- ✅ [receta_medicamento_controller.py](file:///home/fermin/d4lia/app/modules/receta_medicamento/controllers/receta_medicamento_controller.py)

---

## 🔌 Endpoints

### Receta
```
GET    /receta/                          - Listar todas las recetas
POST   /receta/                          - Crear receta
GET    /receta/{id}                      - Obtener receta por ID
PATCH  /receta/{id}                      - Actualizar receta
DELETE /receta/{id}                      - Eliminar receta
GET    /receta/paciente/{id_paciente}    - Recetas de un paciente
GET    /receta/medico/{id_medico}        - Recetas de un médico
GET    /receta/consulta/{id_consulta}    - Recetas de una consulta
```

### Receta-Medicamento
```
GET    /receta_medicamento/                                  - Listar todas las prescripciones
POST   /receta_medicamento/                                  - Agregar medicamento a receta
PATCH  /receta_medicamento/{id_receta}/{id_medicamento}      - Actualizar prescripción
DELETE /receta_medicamento/{id_receta}/{id_medicamento}      - Eliminar medicamento de receta
GET    /receta_medicamento/receta/{id_receta}/medicamentos   - Medicamentos de una receta
GET    /receta_medicamento/medicamento/{id}/recetas          - Recetas con un medicamento
```

---

## 📊 Estructura de Datos

### Receta
| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `id_paciente` | int | ✅ Sí | ID del paciente |
| `id_medico` | int | ❌ No | ID del médico que prescribe |
| `id_consulta` | int | ❌ No | ID de la consulta médica |
| `fecha_inicio` | date | ✅ Sí | Fecha de inicio de vigencia |
| `fecha_fin` | date | ❌ No | Fecha de fin de vigencia |
| `observaciones` | string | ❌ No | Notas adicionales |

### Receta_Medicamento (Prescripción)
| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `id_receta` | int | ✅ Sí | ID de la receta |
| `id_medicamento` | int | ✅ Sí | ID del medicamento |
| `dosis` | string | ❌ No | Dosis (ej: "500mg") |
| `frecuencia` | string | ❌ No | Frecuencia (ej: "cada 8 horas") |
| `duracion` | string | ❌ No | Duración (ej: "7 días") |
| `instrucciones` | string | ❌ No | Instrucciones adicionales |

---

## 🧪 Ejemplos de Uso

### 1. Crear una receta
```bash
curl -X POST http://localhost:8000/receta/ \
  -H "Content-Type: application/json" \
  -d '{
    "id_paciente": 1,
    "id_medico": 1,
    "id_consulta": 1,
    "fecha_inicio": "2025-11-27",
    "fecha_fin": "2025-12-27",
    "observaciones": "Tratamiento para infección"
  }'
```

### 2. Agregar medicamento a receta con prescripción
```bash
curl -X POST http://localhost:8000/receta_medicamento/ \
  -H "Content-Type: application/json" \
  -d '{
    "id_receta": 1,
    "id_medicamento": 1,
    "dosis": "500mg",
    "frecuencia": "Cada 8 horas",
    "duracion": "7 días",
    "instrucciones": "Tomar con alimentos"
  }'
```

### 3. Ver medicamentos de una receta
```bash
curl http://localhost:8000/receta_medicamento/receta/1/medicamentos
```

### 4. Actualizar prescripción
```bash
curl -X PATCH http://localhost:8000/receta_medicamento/1/1 \
  -H "Content-Type: application/json" \
  -d '{
    "dosis": "1000mg",
    "frecuencia": "Cada 12 horas"
  }'
```

### 5. Ver recetas de un paciente
```bash
curl http://localhost:8000/receta/paciente/1
```

---

## ✨ Características Especiales

### Validaciones
- ✅ Fecha de fin no puede ser anterior a fecha de inicio
- ✅ Validación de existencia de paciente, médico y consulta
- ✅ Prevención de medicamentos duplicados en la misma receta
- ✅ Validación de IDs positivos

### Métodos de Negocio
**Receta:**
- `esta_vigente()` - Verifica si la receta está vigente hoy
- `dias_vigencia()` - Calcula días de vigencia

**RecetaMedicamento:**
- `tiene_instrucciones_completas()` - Verifica si tiene dosis, frecuencia y duración

### Queries con JOINs
- Medicamentos de receta incluyen datos del medicamento (nombre, concentración, etc.)
- Recetas con medicamento incluyen datos de la receta

---

## 🔗 Relaciones

```
Receta
  ├─→ Paciente (id_paciente) - OBLIGATORIO
  ├─→ Medico (id_medico) - OPCIONAL
  └─→ ConsultaMedica (id_consulta) - OPCIONAL

RecetaMedicamento
  ├─→ Receta (id_receta) - OBLIGATORIO
  └─→ Medicamento (id_medicamento) - OBLIGATORIO
```

---

## 🚀 Para Probar

```bash
# Reconstruir Docker
docker compose down && docker compose up --build -d

# Ver documentación interactiva
curl http://localhost:8000/docs
```

---

## 💡 Diferencia con Patologia_Tratamiento

A diferencia de `patologia_tratamiento` que solo vincula dos entidades, `receta_medicamento` incluye **campos adicionales** para la prescripción médica:
- **Dosis**: Cantidad del medicamento
- **Frecuencia**: Cada cuánto tomarlo
- **Duración**: Por cuánto tiempo
- **Instrucciones**: Indicaciones especiales

Esto hace que sea un módulo más completo para gestión de prescripciones médicas.
