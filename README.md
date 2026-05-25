# SonarQube

Proyecto Python con integración de análisis de calidad de código mediante **SonarQube**, contenerizado con **Docker**.

---

## 📁 Estructura del proyecto

```
.
├── app.py                       # Código principal de la aplicación
├── Dockerfile                   # Imagen de producción
├── Dockerfile.dev               # Imagen de desarrollo (tests + linting)
├── docker-compose.yml           # Orquestación de contenedores
├── requirements.txt             # Dependencias de la aplicación
├── pytest.ini                   # Configuración de pytest
├── .pre-commit-config.yaml      # Hooks de pre-commit
├── hooks/
│   └── check_commit_msg.py      # Validador de formato de mensaje de commit
└── tests/
    └── test_app.py              # Tests unitarios
```

---

## 🐳 Cómo ejecutar la app con Docker

### Producción

Construir y ejecutar la imagen de producción:

```bash
docker build -t sonarqube-app .
docker run -p 8000:8000 sonarqube-app
```

### Desarrollo (con tests y linting)

Usar el servicio `dev` definido en `docker-compose.yml`:

```bash
# Levantar el contenedor de desarrollo
docker compose run dev bash

# Ejecutar los tests dentro del contenedor
docker compose run dev pytest

# Ejecutar el linter (black) dentro del contenedor
docker compose run dev black --check .
```

---

## 🔍 Cómo lanzar el análisis con SonarQube

### 1. Levantar SonarQube localmente con Docker

```bash
docker run -d --name sonarqube \
  -p 9000:9000 \
  sonarqube:community
```

Acceder a [http://localhost:9000](http://localhost:9000) con las credenciales por defecto:
- **Usuario:** `admin`
- **Contraseña:** `admin`

### 2. Crear un proyecto en SonarQube

1. En la interfaz web, crear un nuevo proyecto local.
2. Asignarle un **Project Key** (ej. `sonarqube-app`).
3. Generar un **token de autenticación** y copiarlo.

### 3. Ejecutar el análisis con sonar-scanner

```bash
docker run --rm \
  --network="host" \
  -e SONAR_HOST_URL="http://localhost:9000" \
  -e SONAR_SCANNER_OPTS="-Dsonar.projectKey=sonarqube-app -Dsonar.sources=. -Dsonar.login=<TU_TOKEN>" \
  sonarsource/sonar-scanner-cli
```

> Sustituye `<TU_TOKEN>` por el token generado en el paso anterior.

### 4. Ver los resultados

Una vez finalizado el análisis, los resultados estarán disponibles en:  
[http://localhost:9000/dashboard?id=sonarqube-app](http://localhost:9000/dashboard?id=sonarqube-app)

---

## 🪝 Pre-commit hooks

Este proyecto usa [pre-commit](https://pre-commit.com/) para garantizar la calidad del código **antes de cada commit**.

### Hooks configurados

| Hook | Descripción |
|------|-------------|
| **black** | Formatea el código Python automáticamente |
| **pytest** | Ejecuta los tests; bloquea el commit si alguno falla |
| **check-added-large-files** | Impide commits con archivos mayores de 500 KB |
| **commit-msg-format** | Exige el formato `<tipo>: <descripción>` en el mensaje de commit |

#### Tipos de commit válidos

```
feat:      Nueva funcionalidad
fix:       Corrección de bug
chore:     Tareas de mantenimiento (dependencias, config...)
docs:      Cambios en documentación
test:      Añadir o modificar tests
refactor:  Refactorización sin cambio de funcionalidad
style:     Cambios de formato o estilo
ci:        Cambios en pipelines CI/CD
```

Ejemplos válidos:
```
feat: añadir endpoint de login
fix: corregir cálculo de totales
chore: actualizar dependencias de producción
```

### Instalación

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar los hooks en el repositorio local
pre-commit install
pre-commit install --hook-type commit-msg

# (Opcional) Ejecutar todos los hooks sobre todos los archivos manualmente
pre-commit run --all-files
```

> ⚠️ Cada miembro del equipo debe ejecutar `pre-commit install` en su clon local del repositorio para activar los hooks.

---

## ✅ Buenas prácticas seguidas

### 🐍 Código Python
- Separación de responsabilidades: lógica de aplicación en `app.py` y tests en `tests/`.
- Tests unitarios con **pytest**, configurados mediante `pytest.ini`.
- Formato de código consistente con **Black** (linter incluido en la imagen de desarrollo).

### 🐳 Docker
- Imagen base ligera (`python:3.11-slim`) para reducir el tamaño del contenedor.
- Imagen separada para desarrollo (`Dockerfile.dev`) y producción (`Dockerfile`), evitando incluir herramientas de desarrollo en producción.
- Instalación de dependencias con `--no-cache-dir` para minimizar el tamaño de la imagen.
- Uso de `WORKDIR` para evitar rutas absolutas en el contenedor.
- Montaje de volúmenes en desarrollo para reflejar cambios en tiempo real sin reconstruir la imagen.

### 🔍 Análisis de calidad
- Integración con **SonarQube** para detectar bugs, vulnerabilidades, code smells y duplicaciones.
- El análisis se ejecuta de forma aislada en un contenedor sin afectar al entorno local.
- Uso de tokens de autenticación en lugar de contraseñas para el acceso a SonarQube.
