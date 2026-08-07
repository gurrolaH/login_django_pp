## README: Desarrollo con Docker Compose

### 1. Antes de empezar

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

### 8. Comandos útiles

- Ver logs del app:

```bash
docker compose -f docker-compose-dev.yml logs -f app
```

- Abrir una shell dentro del contenedor app:

```bash
docker compose -f docker-compose-dev.yml exec app sh
```

- Apagar los contenedores:

```bash
docker compose -f docker-compose-dev.yml down
```

### 9. Rebuild solo cuando cambies Dockerfile o dependencias

```bash
docker compose -f docker-compose-dev.yml build
docker compose -f docker-compose-dev.yml up -d
```

### 10. Notas específicas del proyecto

- El servicio de desarrollo app monta `./app:/app`.
- El comando de arranque en desarrollo usa:
  - `python manage.py runserver 0.0.0.0:8000`
- El servicio `db` usa MariaDB en el contenedor `pp-db`.

---

## Resumen rápido

```bash
cd d:/practicas_profesionales/login_django_01
git pull origin main
cp env-example.txt .env
docker compose -f docker-compose-dev.yml up -d --build
docker compose -f docker-compose-dev.yml ps
docker compose -f docker-compose-dev.yml exec app python manage.py makemigrations
docker compose -f docker-compose-dev.yml exec app python manage.py migrate
```

Con esto deberías tener el entorno listo y `localhost:8000` funcionando.