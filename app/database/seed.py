"""
Script de seed para inicializar la base de datos con datos de prueba.
Usa asyncpg directamente, sin ORM, respetando todas las foreign keys.
"""
import asyncio
import asyncpg
from datetime import date, time
from app.config.environment import settings

settings = settings
    

async def seed_database():
    """Inserta datos iniciales en la base de datos."""
    
    # Conectar a la base de datos
    # Determinar host y puerto según el entorno
    from app.config.config import APP_STATES
    if settings.ENV == APP_STATES.PRODUCTION:
        host = settings.PROD_DB_HOST
        port = settings.PROD_DB_PORT
    else:
        host = settings.DEV_DB_HOST
        port = settings.DEV_DB_PORT
    
    conn = await asyncpg.connect(
        host=host,
        port=port,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        database=settings.DATABASE_NAME
    )
    
    try:
        print("🌱 Iniciando seed de la base de datos...")
        
        # 🧹 Limpiar datos existentes (en orden inverso a las FK)
        print("🧹 Limpiando datos existentes...")
        await conn.execute("TRUNCATE TABLE encuesta_paciente_json, encuesta_sesion_json, "
                          "medicamento_hospitalizacion, tratamiento_hospitalizacion, "
                          "hospitalizacion, orden_hospitalizacion, receta_medicamento, "
                          "receta, medicamento, examen, orden_examen, diagnostico, "
                          "consulta_medica, sesion, paciente_ges, paciente_condicion, "
                          "paciente, sillon, patologia_tratamiento, tratamiento, patologia, "
                          "encargado, tipo_examen, cie10_ges, ges, cie10, condicion_personal, "
                          "consulta_profesional, medico, especializacion, estado, instalacion "
                          "RESTART IDENTITY CASCADE")
        
        # 🔹 Encargados
        print("✅ Insertando encargados...")
        encargados = await conn.fetch("""
            INSERT INTO encargado (nombre_completo, rut, correo, telefono, cargo, especialidad)
            VALUES
                ('Dra. Carolina Gómez Muñoz', '15.234.567-8', 'carolina.gomez@hospital.cl', '+56912345678', 'doctor', 'Oncología'),
                ('Enf. Rodrigo Salinas Paredes', '16.345.678-9', 'rodrigo.salinas@hospital.cl', '+56998765432', 'enfermero', 'Quimioterapia'),
                ('Téc. Ana Torres Fuentes', '17.987.654-3', 'ana.torres@hospital.cl', '+56955555555', 'técnico', 'Apoyo clínico')
            RETURNING id_encargado, nombre_completo
        """)
        print(f"   📌 {len(encargados)} encargados insertados")
        
        # 🔹 Patologías
        print("✅ Insertando patologías...")
        patologias = await conn.fetch("""
            INSERT INTO patologia (
                codigo, nombre_patologia, especialidad, tiempo_estimado, explicacion,
                tratamientos_principales, farmacos, efectos_adversos, gravedad,
                costo_aprox, evidencia, exito_porcentaje, edad_promedio, notas
            )
            VALUES (
                'O001',
                'Cáncer de próstata (local/alto riesgo)',
                'Oncología',
                '1 hr/sesión - total 6 meses',
                'Tumor prostático tratado con radioterapia (RT), quimioterapia (QT) y/o hormonoterapia según riesgo.',
                'Radioterapia, Quimioterapia, Hormonoterapia',
                'Docetaxel, Bicalutamida (± Goserelina/Leuprorelina)',
                'Fatiga, náuseas, neutropenia, sofocos',
                'Severa',
                'US$2.000–5.000/sesión',
                'Alta',
                '70–80% control',
                '65+',
                'Puede requerir deprivación androgénica prolongada'
            )
            RETURNING id_patologia, codigo
        """)
        id_patologia = patologias[0]['id_patologia']
        print(f"   📌 Patología insertada con ID: {id_patologia}")
        
        # 🔹 Tratamientos
        print("✅ Insertando tratamientos...")
        tratamientos = await conn.fetch("""
            INSERT INTO tratamiento (nombre_tratamiento, descripcion, duracion_estimada, costo_aprox, observaciones, document_path)
            VALUES
                ('Radioterapia', 'Terapia con radiación dirigida para destruir células cancerosas', '6 meses', 'US$2.500/sesión', 'Requiere seguimiento de efectos secundarios', NULL),
                ('Quimioterapia', 'Tratamiento con fármacos citotóxicos', '6 meses', 'US$3.000/sesión', 'Control de toxicidad hematológica necesario', NULL),
                ('Hormonoterapia', 'Bloqueo hormonal para cáncer hormono-dependiente', '12 meses', 'US$1.500/sesión', 'Requiere control de testosterona y PSA', NULL)
            RETURNING id_tratamiento, nombre_tratamiento
        """)
        print(f"   📌 {len(tratamientos)} tratamientos insertados")
        
        # 🔹 Vinculación Patología ↔ Tratamiento
        print("✅ Vinculando patologías con tratamientos...")
        for tratamiento in tratamientos:
            await conn.execute("""
                INSERT INTO patologia_tratamiento (id_patologia, id_tratamiento)
                VALUES ($1, $2)
            """, id_patologia, tratamiento['id_tratamiento'])
        print(f"   📌 {len(tratamientos)} vinculaciones creadas")
        
        # 🔹 Pacientes
        print("✅ Insertando pacientes...")
        from datetime import date
        pacientes_data = [
            ('12.345.678-9', 'Juan Pérez Soto', 'juan.perez@example.com', 62, 
             'Avenida 2 Sur 1456, Talca, Región del Maule', 'Hipertensión, Diabetes', 
             'Buen estado general', date(2025, 9, 1)),
            ('9.876.543-2', 'María López Díaz', 'maria.lopez@example.com', 45,
             'Calle Estado 235, Curicó, Región del Maule', 'Ninguno',
             'HER2 positivo', date(2025, 9, 15)),
            ('13.456.789-0', 'Pedro González Vera', 'pedro.gonzalez@example.com', 58,
             'Pasaje Los Robles 123, Talca, Región del Maule', 'Hipertensión',
             'Requiere control de dolor', date(2025, 9, 20)),
            ('14.567.890-1', 'Carmen Silva Rojas', 'carmen.silva@example.com', 52,
             'Avenida Lircay 456, Talca, Región del Maule', 'Diabetes tipo 2',
             'Linfoma en tratamiento', date(2025, 9, 25))
        ]
        
        pacientes = []
        for i, (rut, nombre, correo, edad, direccion, antecedentes, obs, fecha) in enumerate(pacientes_data):
            id_encargado = encargados[i % len(encargados)]['id_encargado']
            paciente = await conn.fetchrow("""
                INSERT INTO paciente (
                    rut, nombre_completo, correo, telefono, edad, direccion, 
                    antecedentes_medicos, id_patologia, id_encargado_registro, 
                    fecha_inicio_tratamiento, observaciones
                )
                VALUES ($1, $2, $3, NULL, $4, $5, $6, $7, $8, $9, $10)
                RETURNING id_paciente, rut, nombre_completo
            """, rut, nombre, correo, edad, direccion, antecedentes, 
                id_patologia, id_encargado, fecha, obs)
            pacientes.append(paciente)
        print(f"   📌 {len(pacientes)} pacientes insertados")
        
        # 🔹 Sillones
        print("✅ Insertando sillones...")
        sillones = await conn.fetch("""
            INSERT INTO sillon (ubicacion_sala, estado, observaciones)
            VALUES
                ('consultorio_1', 'disponible', 'Sillón ergonómico, con bomba infusora'),
                ('consultorio_2', 'disponible', 'Sillón con soporte reclinable')
            RETURNING id_sillon
        """)
        print(f"   📌 {len(sillones)} sillones insertados")
        
        # 🔹 Estados
        print("✅ Insertando estados...")
        estados = await conn.fetch("""
            INSERT INTO estado (nombre, descripcion)
            VALUES
                ('Pendiente', 'Solicitud recibida, aún no procesada'),
                ('En proceso', 'Orden en ejecución'),
                ('Completado', 'Orden finalizada exitosamente'),
                ('Cancelado', 'Orden cancelada')
            RETURNING id_estado, nombre
        """)
        print(f"   📌 {len(estados)} estados insertados")
        
        # 🔹 Sesiones
        print("✅ Insertando sesiones...")
        sesion1 = await conn.fetchrow("""
            INSERT INTO sesion (
                id_paciente, id_patologia, id_tratamiento, id_sillon, id_encargado,
                fecha, hora_inicio, hora_fin, tiempo_aseo_min, materiales_usados, estado
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id_sesion
        """, pacientes[0]['id_paciente'], id_patologia, tratamientos[0]['id_tratamiento'],
            sillones[0]['id_sillon'], encargados[1]['id_encargado'],
            date(2025, 10, 10), time(9, 0), time(11, 40), 15, 
            'Guantes, Jeringas, Vías periféricas', 'confirmado')
        
        sesion2 = await conn.fetchrow("""
            INSERT INTO sesion (
                id_paciente, id_patologia, id_tratamiento, id_sillon, id_encargado,
                fecha, hora_inicio, hora_fin, tiempo_aseo_min, materiales_usados, estado
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            RETURNING id_sesion
        """, pacientes[1]['id_paciente'], id_patologia, tratamientos[1]['id_tratamiento'],
            sillones[1]['id_sillon'], encargados[2]['id_encargado'],
            date(2025, 10, 10), time(9, 15), time(13, 25), 15,
            'Guantes, Catéter central, Soluciones', 'confirmado')
        print(f"   📌 2 sesiones insertadas")
        
        # 🔹 Encuestas de Sesión
        print("✅ Insertando encuestas de sesión...")
        await conn.execute("""
            INSERT INTO encuesta_sesion_json (id_sesion, tipo_encuesta, datos)
            VALUES 
                ($1, $2, $3::jsonb),
                ($4, $5, $6::jsonb)
        """, sesion1['id_sesion'], 'satisfaccion',
            '{"puntaje_global": 9, "atencion_personal": 10, "comodidad_sillon": 8}',
            sesion2['id_sesion'], 'satisfaccion',
            '{"puntaje_global": 8, "atencion_personal": 9, "comodidad_sillon": 7}')
        print(f"   📌 2 encuestas de sesión insertadas")
        
        # 🔹 Encuestas de Paciente
        print("✅ Insertando encuestas de paciente...")
        await conn.execute("""
            INSERT INTO encuesta_paciente_json (id_paciente, tipo_encuesta, datos)
            VALUES 
                ($1, $2, $3::jsonb),
                ($4, $5, $6::jsonb)
        """, pacientes[0]['id_paciente'], 'antecedentes_medicos',
            '{"fuma": false, "alcohol": "ocasional", "alergias": ["penicilina"]}',
            pacientes[1]['id_paciente'], 'habitos',
            '{"fuma": true, "alcohol": "moderado", "actividad_fisica": "3 veces por semana"}')
        print(f"   📌 2 encuestas de paciente insertadas")
        
        # 🔹 Condiciones personales
        print("✅ Insertando condiciones personales...")
        condiciones = await conn.fetch("""
            INSERT INTO condicion_personal (codigo, nombre_condicion, tipo, severidad, observaciones)
            VALUES
                ('E11', 'Diabetes tipo 2', 'preexistencia', 'moderada', 'Control con metformina'),
                ('I10', 'Hipertensión arterial esencial', 'preexistencia', 'alta', 'Tratada con losartán'),
                ('A001', 'Alergia a la penicilina', 'alergia', 'alta', 'Evitar antibióticos betalactámicos')
            RETURNING id_condicion, codigo
        """)
        print(f"   📌 {len(condiciones)} condiciones insertadas")
        
        # 🔹 Paciente ↔ Condición
        print("✅ Vinculando pacientes con condiciones...")
        await conn.execute("""
            INSERT INTO paciente_condicion (id_paciente, id_condicion, fecha_inicio, validada_medico, observaciones)
            VALUES
                ($1, $2, $3, TRUE, 'Diagnosticada hace 10 años'),
                ($1, $4, $5, TRUE, 'Controlada con medicación')
        """, pacientes[0]['id_paciente'], condiciones[0]['id_condicion'], date(2015, 3, 10),
            condiciones[1]['id_condicion'], date(2018, 7, 20))
        print(f"   📌 2 vinculaciones paciente-condición creadas")
        
        # 🔹 Especializaciones
        print("✅ Insertando especializaciones médicas...")
        especializaciones = await conn.fetch("""
            INSERT INTO especializacion (nombre, descripcion, codigo_fonasa, nivel)
            VALUES
                ('Oncología Médica', 'Tratamiento del cáncer mediante quimioterapia', 'F001', 'especialista'),
                ('Cardiología', 'Diagnóstico y tratamiento de enfermedades del corazón', 'F002', 'especialista'),
                ('Medicina Interna', 'Evaluación y manejo integral de pacientes adultos', 'F003', 'general')
            RETURNING id_especializacion, nombre
        """)
        print(f"   📌 {len(especializaciones)} especializaciones insertadas")
        
        # 🔹 Médicos
        print("✅ Insertando médicos...")
        medicos = await conn.fetch("""
            INSERT INTO medico (rut, nombre, apellido, sexo, correo, telefono, codigo_fonasa, activo)
            VALUES
                ('15.234.567-8', 'Carolina', 'Gómez', 'femenino', 'carolina.gomez@hospital.cl', '+56912345678', 'M001', TRUE),
                ('18.111.222-3', 'Rodrigo', 'Salinas', 'masculino', 'rodrigo.salinas@hospital.cl', '+56998765432', 'M002', TRUE)
            RETURNING id_medico, nombre, apellido
        """)
        print(f"   📌 {len(medicos)} médicos insertados")
        
        # 🔹 Consulta Profesional (Médico ↔ Especialización)
        print("✅ Vinculando médicos con especializaciones...")
        consulta_prof = await conn.fetch("""
            INSERT INTO consulta_profesional (id_medico, id_especializacion)
            VALUES
                ($1, $2),
                ($3, $4)
            RETURNING id_profesional
        """, medicos[0]['id_medico'], especializaciones[0]['id_especializacion'],
            medicos[1]['id_medico'], especializaciones[2]['id_especializacion'])
        print(f"   📌 {len(consulta_prof)} vinculaciones médico-especialización creadas")
        
        # 🔹 CIE10
        print("✅ Insertando códigos CIE10...")
        cie10_list = await conn.fetch("""
            INSERT INTO cie10 (codigo, nombre, categoria, descripcion)
            VALUES
                ('C61', 'Tumor maligno de la próstata', 'Neoplasias', 'Carcinoma prostático'),
                ('E11', 'Diabetes mellitus tipo 2', 'Enfermedades endocrinas', 'Diabetes tipo 2 no insulinodependiente')
            RETURNING id_cie10, codigo
        """)
        print(f"   📌 {len(cie10_list)} códigos CIE10 insertados")
        
        # 🔹 GES
        print("✅ Insertando garantías GES...")
        ges_list = await conn.fetch("""
            INSERT INTO ges (codigo_ges, nombre, descripcion, dias_limite_diagnostico, dias_limite_tratamiento)
            VALUES
                ('GES001', 'Cáncer de próstata', 'Garantía GES para diagnóstico y tratamiento', 30, 60),
                ('GES002', 'Diabetes Mellitus tipo 2', 'Garantía GES para control y tratamiento', 45, 90)
            RETURNING id_ges, codigo_ges
        """)
        print(f"   📌 {len(ges_list)} garantías GES insertadas")
        
        # 🔹 CIE10 ↔ GES
        print("✅ Vinculando CIE10 con GES...")
        await conn.execute("""
            INSERT INTO cie10_ges (id_cie10, id_ges)
            VALUES ($1, $2), ($3, $4)
        """, cie10_list[0]['id_cie10'], ges_list[0]['id_ges'],
            cie10_list[1]['id_cie10'], ges_list[1]['id_ges'])
        print(f"   📌 2 vinculaciones CIE10-GES creadas")
        
        # 🔹 Paciente GES
        print("✅ Insertando pacientes GES...")
        await conn.execute("""
            INSERT INTO paciente_ges (id_paciente, id_ges, dias_limite, fecha_activacion, estado, observaciones)
            VALUES ($1, $2, 60, $3, 'activo', 'Paciente con GES activo')
        """, pacientes[0]['id_paciente'], ges_list[0]['id_ges'], date(2025, 9, 1))
        print(f"   📌 1 paciente GES insertado")
        
        # 🔹 Tipo de Examen
        print("✅ Insertando tipos de examen...")
        tipos_examen = await conn.fetch("""
            INSERT INTO tipo_examen (nombre, descripcion, codigo_interno, requiere_ayuno, tiempo_estimado, observaciones)
            VALUES
                ('Hemograma completo', 'Análisis de sangre completo', 'LAB001', FALSE, '15 min', 'Requiere muestra de sangre'),
                ('Radiografía de tórax', 'Imagen del tórax', 'IMG002', FALSE, '20 min', 'Evitar objetos metálicos')
            RETURNING id_tipo_examen, nombre
        """)
        print(f"   📌 {len(tipos_examen)} tipos de examen insertados")
        
        # 🔹 Instalaciones
        print("✅ Insertando instalaciones...")
        instalaciones = await conn.fetch("""
            INSERT INTO instalacion (nombre, tipo, ubicacion, contacto, observaciones)
            VALUES ('Laboratorio Central', 'laboratorio', 'Edificio B - Piso 1', 'lab@hospital.cl', 'Muestra de sangre')
            RETURNING id_instalacion, nombre
        """)
        print(f"   📌 {len(instalaciones)} instalaciones insertadas")
        
        # 🔹 Consultas Médicas
        print("✅ Insertando consultas médicas...")
        consulta = await conn.fetchrow("""
            INSERT INTO consulta_medica (id_paciente, id_profesional, especialidad, fecha, motivo, tratamiento, observaciones)
            VALUES ($1, $2, 'Oncología Médica', $3, 'Control post-quimioterapia', 'Revisión de análisis', 'Paciente estable')
            RETURNING id_consulta
        """, pacientes[0]['id_paciente'], consulta_prof[0]['id_profesional'], date(2025, 9, 10))
        print(f"   📌 1 consulta médica insertada")
        
        # 🔹 Orden de Examen
        print("✅ Insertando órdenes de examen...")
        await conn.execute("""
            INSERT INTO orden_examen (id_consulta, id_profesional, id_paciente, id_tipo_examen, id_estado, fecha, motivo, documento)
            VALUES ($1, $2, $3, $4, $5, $6, 'Control post-quimioterapia', NULL)
        """, consulta['id_consulta'], consulta_prof[0]['id_profesional'], pacientes[0]['id_paciente'],
            tipos_examen[0]['id_tipo_examen'], estados[0]['id_estado'], date(2025, 10, 5))
        print(f"   📌 1 orden de examen insertada")
        
        # 🔹 Medicamentos
        print("✅ Insertando medicamentos...")
        medicamentos = await conn.fetch("""
            INSERT INTO medicamento (
                nombre_comercial, nombre_generico, concentracion, forma_farmaceutica,
                via_administracion, laboratorio, requiere_receta, stock_disponible, observaciones
            )
            VALUES
                ('Paracetamol 500 mg', 'Paracetamol', '500 mg', 'Comprimido', 'Oral', 'Lab Chile', FALSE, 250, 'Analgésico común'),
                ('Losartán 50 mg', 'Losartán potásico', '50 mg', 'Comprimido', 'Oral', 'Recalcine', TRUE, 180, 'Antihipertensivo')
            RETURNING id_medicamento, nombre_generico
        """)
        print(f"   📌 {len(medicamentos)} medicamentos insertados")
        
        # 🔹 Recetas
        print("✅ Insertando recetas...")
        receta = await conn.fetchrow("""
            INSERT INTO receta (id_paciente, id_medico, id_consulta, fecha_inicio, fecha_fin, observaciones)
            VALUES ($1, $2, $3, $4, $5, 'Tratamiento para control de dolor')
            RETURNING id_receta
        """, pacientes[0]['id_paciente'], medicos[0]['id_medico'], consulta['id_consulta'],
            date(2025, 10, 10), date(2025, 10, 24))
        print(f"   📌 1 receta insertada")
        
        # 🔹 Receta ↔ Medicamento
        print("✅ Vinculando recetas con medicamentos...")
        await conn.execute("""
            INSERT INTO receta_medicamento (id_receta, id_medicamento, dosis, frecuencia, duracion, instrucciones)
            VALUES ($1, $2, '500 mg', 'Cada 8 horas', '7 días', 'Tomar después de las comidas')
        """, receta['id_receta'], medicamentos[0]['id_medicamento'])
        print(f"   📌 1 vinculación receta-medicamento creada")
        
        # 🔹 Examen (resultados de exámenes médicos)
        print("✅ Insertando resultados de exámenes...")
        examen = await conn.fetchrow("""
            INSERT INTO examen (
                id_paciente, id_tipo_examen, id_profesional, id_orden_examen, 
                id_instalacion, id_estado, fecha, resultados, resumen_resultado, observaciones
            )
            VALUES ($1, $2, $3, 
                (SELECT id_orden_examen FROM orden_examen WHERE id_paciente = $1 LIMIT 1),
                $4, $5, $6, 
                'Hemoglobina: 14.2 g/dL, Leucocitos: 7.800/μL, Plaquetas: 245.000/μL',
                'Valores dentro de rangos normales', 'Paciente en buen estado general')
            RETURNING id_examen
        """, pacientes[0]['id_paciente'], tipos_examen[0]['id_tipo_examen'], 
            consulta_prof[0]['id_profesional'], instalaciones[0]['id_instalacion'],
            estados[2]['id_estado'], date(2025, 10, 6))
        print(f"   📌 1 examen insertado")
        
        # 🔹 Diagnóstico (asociado a consulta médica con CIE10)
        print("✅ Insertando diagnósticos médicos...")
        diagnostico = await conn.fetchrow("""
            INSERT INTO diagnostico (
                id_consulta_medica, id_cie10, id_ges, descripcion, tipo, fecha_registro, observaciones
            )
            VALUES ($1, $2, $3, 
                'Carcinoma prostático en tratamiento activo con quimioterapia',
                'confirmado', $4, 'Respuesta favorable al tratamiento')
            RETURNING id_diagnostico
        """, consulta['id_consulta'], cie10_list[0]['id_cie10'], ges_list[0]['id_ges'], 
            date(2025, 9, 10))
        print(f"   📌 1 diagnóstico insertado")
        
        # 🔹 Orden de Hospitalización
        print("✅ Insertando órdenes de hospitalización...")
        orden_hosp = await conn.fetchrow("""
            INSERT INTO orden_hospitalizacion (
                id_paciente, id_profesional, fecha, motivo, estado
            )
            VALUES ($1, $2, $3, 
                'Complicaciones post-quimioterapia - requiere observación',
                'completada')
            RETURNING id_orden_hospitalizacion
        """, pacientes[1]['id_paciente'], consulta_prof[0]['id_profesional'], date(2025, 10, 15))
        print(f"   📌 1 orden de hospitalización insertada")
        
        # 🔹 Hospitalización
        print("✅ Insertando hospitalizaciones...")
        hospitalizacion = await conn.fetchrow("""
            INSERT INTO hospitalizacion (
                id_orden_hospitalizacion, id_paciente, id_profesional,
                fecha_ingreso, fecha_alta, habitacion, observacion, estado
            )
            VALUES ($1, $2, $3, $4, $5, '301-A', 
                'Paciente ingresó con neutropenia febril, respondió favorablemente a antibióticos',
                'alta')
            RETURNING id_hospitalizacion
        """, orden_hosp['id_orden_hospitalizacion'], pacientes[1]['id_paciente'],
            consulta_prof[0]['id_profesional'], date(2025, 10, 15), date(2025, 10, 20))
        print(f"   📌 1 hospitalización insertada")
        
        # 🔹 Tratamiento durante Hospitalización
        print("✅ Insertando tratamientos durante hospitalización...")
        await conn.execute("""
            INSERT INTO tratamiento_hospitalizacion (
                id_hospitalizacion, id_tratamiento, id_profesional,
                fecha_aplicacion, dosis, duracion, observaciones
            )
            VALUES ($1, $2, $3, $4, 'Dosis estándar', '5 días',
                'Tratamiento de soporte durante neutropenia')
        """, hospitalizacion['id_hospitalizacion'], tratamientos[1]['id_tratamiento'],
            consulta_prof[0]['id_profesional'], date(2025, 10, 16))
        print(f"   📌 1 tratamiento de hospitalización insertado")
        
        # 🔹 Medicamento durante Hospitalización
        print("✅ Insertando medicamentos durante hospitalización...")
        await conn.execute("""
            INSERT INTO medicamento_hospitalizacion (
                id_hospitalizacion, id_medicamento, id_profesional,
                dosis, frecuencia, via_administracion, duracion, observaciones
            )
            VALUES ($1, $2, $3, '1g', 'Cada 8 horas', 'Intravenosa', '5 días',
                'Ceftriaxona para cobertura antibiótica amplia')
        """, hospitalizacion['id_hospitalizacion'], medicamentos[1]['id_medicamento'],
            consulta_prof[0]['id_profesional'])
        print(f"   📌 1 medicamento de hospitalización insertado")
        
        print("\n" + "="*60)
        print("✅ SEED COMPLETADO EXITOSAMENTE")
        print("="*60)
        print(f"📊 Resumen:")
        print(f"   • {len(encargados)} encargados")
        print(f"   • {len(pacientes)} pacientes")
        print(f"   • {len(tratamientos)} tratamientos")
        print(f"   • {len(medicos)} médicos")
        print(f"   • {len(especializaciones)} especializaciones")
        print(f"   • {len(tipos_examen)} tipos de examen")
        print(f"   • {len(medicamentos)} medicamentos")
        print(f"   • 1 examen + 1 diagnóstico")
        print(f"   • 1 hospitalización completa")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR durante el seed: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await conn.close()
        print("🔒 Conexión cerrada")


if __name__ == "__main__":
    asyncio.run(seed_database())
