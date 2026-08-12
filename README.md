## README: Desarrollo con Docker Compose

### 1. Antes de empezar
- Estar en la segunda carpeta de: \login_django_pp

- Tener docker instalado y corriendo.

### 2. Clonar el repositorio

```bash
git clone https://github.com/gurrolaH/login_django_pp.git
```

### 3. Configurar variables de entorno

Copia el ejemplo a .env si no existe:

```bash
cp env-example.txt .env
```

Revisa que .env tenga estas variables mínimas:
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_ROOT_PASSWORD`
- `DB_HOST=db`
- `DB_PORT=3306`
- `DEBUG=True`
- `SECRET_KEY=...`

### 4. Construir y levantar el entorno de desarrollo

```bash
docker compose -f docker-compose-dev.yml up -d --build
```

Esto construye la imagen del servicio app y levanta los contenedores app y `db`.

### 5. Ver el estado de los servicios

```bash
docker compose -f docker-compose-dev.yml ps
```

Deberías ver `login-pp-app` y `pp-db` en estado `Up`.

### 6. Ejecutar migraciones

```bash
docker compose -f docker-compose-dev.yml exec app python manage.py makemigrations
docker compose -f docker-compose-dev.yml exec app python manage.py migrate
```

> Si ya generaste migraciones antes, solo necesitas correr `migrate`.

### 7. Acceder a la aplicación

Abre en tu navegador:

```text
http://localhost:8000
```

### Diagrama relacional del sistema

![Diagrama Relacional](docs/diagrama-bd.svg)