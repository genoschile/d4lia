import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.modules.medico_especialidad.services.medico_service import MedicoService
from app.modules.medico_especialidad.entities.medico_especialidad_entity import Medico, Rut, Especializacion
from app.modules.medico_especialidad.schemas.medico_especialidad_schema import MedicoCreate
from app.core.exceptions import ConflictError, NotFoundError

async def verify_medico_service():
    print("Verifying MedicoService...")
    
    # Mocks
    pool = MagicMock()
    # Mock pool.acquire() context manager
    conn_mock = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn_mock
    
    medico_repo = AsyncMock()
    especialidad_repo = AsyncMock()
    
    service = MedicoService(pool, medico_repo, especialidad_repo)
    
    # Test Create Medico
    print("\n[Test] Create Medico")
    medico_data = MedicoCreate(
        rut="12345678-5",
        nombre="Juan",
        apellido="Perez",
        sexo="masculino"
    )
    medico_repo.get_by_rut.return_value = None
    medico_repo.create.return_value = Medico(
        id_medico=1,
        rut=Rut("12345678-5"),
        nombre="Juan",
        apellido="Perez",
        sexo="masculino"
    )
    
    created = await service.create_medico(medico_data)
    print(f"Created Medico: {created.nombre} {created.apellido} (ID: {created.id_medico})")
    assert created.id_medico == 1
    # Verify acquire was called
    pool.acquire.assert_called()
    # Verify repo was called with conn_mock
    args, _ = medico_repo.create.call_args
    assert args[0] == conn_mock
    assert isinstance(args[1], Medico)
    assert args[1].rut.value == "12345678-5"
    
    # Test Create Medico Duplicate (ConflictError)
    print("\n[Test] Create Medico Duplicate")
    medico_repo.get_by_rut.return_value = Medico(
        id_medico=1,
        rut=Rut("12345678-5"),
        nombre="Juan",
        apellido="Perez",
        sexo="masculino"
    )
    try:
        await service.create_medico(medico_data)
        print("ERROR: Should have raised ConflictError")
    except ConflictError as e:
        print(f"Caught expected error: {e}")
    
    # Test Assign Specialty
    print("\n[Test] Assign Specialty")
    medico_repo.get_by_id.return_value = Medico(
        id_medico=1,
        rut=Rut("12345678-5"),
        nombre="Juan",
        apellido="Perez",
        sexo="masculino"
    )
    especialidad_repo.get_by_id.return_value = Especializacion(
        id=10,
        nombre="Cardiologia",
        nivel="Primario",
        codigo_fonasa="123"
    )
    medico_repo.get_specialties_by_medico.return_value = []
    
    await service.assign_specialty(1, 10)
    print("Specialty assigned successfully")
    medico_repo.assign_specialty.assert_called_with(conn_mock, 1, 10)
    
    # Test Assign Specialty Duplicate (ConflictError)
    print("\n[Test] Assign Specialty Duplicate")
    medico_repo.get_specialties_by_medico.return_value = [
        Especializacion(id=10, nombre="Cardiologia", nivel="Primario", codigo_fonasa="123")
    ]
    try:
        await service.assign_specialty(1, 10)
        print("ERROR: Should have raised ConflictError")
    except ConflictError as e:
        print(f"Caught expected error: {e}")

    # Test Get Medico Not Found (NotFoundError)
    print("\n[Test] Get Medico Not Found")
    medico_repo.get_by_id.return_value = None
    try:
        await service.get_medico_by_id(999)
        print("ERROR: Should have raised NotFoundError")
    except NotFoundError as e:
        print(f"Caught expected error: {e}")

    print("\nVerification successful!")

if __name__ == "__main__":
    asyncio.run(verify_medico_service())
