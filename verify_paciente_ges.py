import asyncio
import asyncpg
from datetime import date
from app.modules.paciente_ges.services.paciente_ges_service import PacienteGesService
from app.modules.paciente_ges.repositories.paciente_ges_repository import PacienteGesRepository
from app.modules.paciente_ges.schemas.paciente_ges_schema import PacienteGesCreate
from app.database.database import connect_to_db

# Mock repositories for dependencies we don't need to test deeply
class MockRepo:
    async def get_by_id(self, conn, id):
        return type('obj', (object,), {'id': id, 'dias_limite_diagnostico': 45, 'dias_limite_tratamiento': 30})

class MockPacienteRepo:
    async def get_by_id(self, conn, id):
        return True

async def verify():
    pool = await connect_to_db()
    if not pool:
        print("Failed to connect to DB")
        return

    # Repositories
    paciente_ges_repo = PacienteGesRepository(pool)
    paciente_repo = MockPacienteRepo()
    ges_repo = MockRepo()
    diagnostico_repo = MockRepo()

    service = PacienteGesService(pool, paciente_ges_repo, paciente_repo, ges_repo, diagnostico_repo)

    # Test Case 1: Create without dias_limite (should use diagnostic limit 45)
    print("\n--- Test Case 1: Create without dias_limite (Diagnostic Phase) ---")
    data_1 = PacienteGesCreate(
        id_paciente=1, # Assuming patient 1 exists or mock handles it
        id_ges=1,      # Assuming GES 1 exists
        # dias_limite omitted
        id_diagnostico=None
    )
    
    # We need to mock the actual DB calls inside service.create because we don't want to insert into real DB if possible,
    # OR we insert and then rollback. Since we are using the real service, it will try to use real repos.
    # Let's use the real DB but maybe catch the insert error or just print what would happen if we could mock the insert.
    # Actually, the service uses `self.ges_repo`. I passed a MockRepo for `ges_repo`.
    # So `ges = await self.ges_repo.get_by_id` will return my mock object with limits.
    # But `self.paciente_ges_repo.create` is the real one.
    
    # Let's mock `paciente_ges_repo.create` too to avoid DB writes and just verify the passed entity.
    original_create = paciente_ges_repo.create
    
    async def mock_create(conn, entity):
        print(f"✅ [MOCK DB] Inserting PacienteGes with dias_limite: {entity.dias_limite}")
        # Return a fake object to satisfy the service return type
        entity.id_paciente_ges = 999
        entity.fecha_vencimiento = date.today() # Dummy
        return entity

    paciente_ges_repo.create = mock_create

    try:
        await service.create(data_1)
        print("Test 1 Passed: Service accepted missing dias_limite")
    except Exception as e:
        print(f"Test 1 Failed: {e}")

    # Test Case 2: Create with explicit dias_limite
    print("\n--- Test Case 2: Create with explicit dias_limite ---")
    data_2 = PacienteGesCreate(
        id_paciente=1,
        id_ges=1,
        dias_limite=10, # Explicit override
        id_diagnostico=None
    )
    try:
        await service.create(data_2)
        print("Test 2 Passed: Service accepted explicit dias_limite")
    except Exception as e:
        print(f"Test 2 Failed: {e}")

    await pool.close()

if __name__ == "__main__":
    asyncio.run(verify())
