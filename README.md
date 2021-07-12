# Papel

Simple REST API que permite registrar, activar usuarios y enviar emails (Python, Django, Celery, Redis, PostgreSql)

## Instalación

Necesitas tener Docker y Docker Compose instalado.

Crea un archivo `.env`, pega el contenido de `.env.example` y actualiza los valores del correo electrónico de ejemplo:

```text
DEBUG=True
DJANGO_SECRET_KEY=gNCbtiguLq7fLcl8OzaNFfNB3tRaXLD5uOrW
CORS_ALLOWED_ORIGINS=*
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=mail@mail.com
EMAIL_HOST_PASSWORD=mysupersecretpassword
EMAIL_USE_TLS=True

ACCOUNT_ACTIVATION_URL=https://www.confortdeporvida.cl/account-activation/
```

Migra la base de datos, crea el super usuario y ejecuta el proyecto

```bash
$ docker-compose run app python manage.py migrate
$ docker-compose run app python manage.py createsuperuser
$ docker-compose up
```

Si lo deseas, puedes generar usuarios en masa con el siguiente comando

```bash
$ docker-compose run app python manage.py seed users --number=1000
```

> Es probable que durante la ejecución de este comando se genere el error: `DETAIL: Key (username)=(umyers) already exists.`. Simplemente vuelve a ejecutarlo hasta obtener un número considerable de usuarios que permitan probar el desempeño de la solución.

## Endpoints

```
http://127.0.0.1:8000/api
```

### Registro de usuarios

```
POST /accounts/register/
```

| Campo      | Tipo             | Información adicional         |
| ---------- | ---------------- | ----------------------------- |
| username   | String: formData | **Requerido**. 150 caracteres |
| email      | String: formData | **Requerido**. 60 caracteres  |
| bio        | String: formData | **Opcional**. 500 caracteres  |
| phone      | String: formData | **Requerido**. 15 caracteres  |
| address    | String: formData | **Requerido**. 100 caracteres |
| first_name | String: formData | **Requerido**. 150 caracteres |
| last_name  | String: formData | **Requerido**. 150 caracteres |

#### Respuestas

##### 201 Created

```json
{
  "id": 2,
  "username": "username",
  "email": "username@username.com",
  "first_name": "name",
  "last_name": "last_name",
  "phone": "7842934",
  "address": "Las Camelias 123",
  "bio": "Amo el confort"
}
```

La cuenta del usuario no será tomada en cuenta para el concurso hasta después de su validación y activación.

##### 400 Bad Request

```json
{
  "username": ["This field is required."],
  "email": ["user with this email address already exists."]
}
```

### Validación de cuentas

Al momento de registrarse, se enviará un correo electrónico a la dirección del usuario con el enlace de activación en el siguiente formato:

```
http://fontend-url/account-activation/?token=superweirdtoken&user_id=22
```

El desarrollador frontend deberá capturar el **token** y el **user_id** desde los parámetros de la url y enviar una nueva petición para activar la cuenta del usuario:

```
PUT /accounts/activate/{user_id}/?token={token}
```

| Campo     | Tipo             | Información adicional         |
| --------- | ---------------- | ----------------------------- |
| user_id   | Integer: path    | **Requerido**.                |
| token     | String: query    | **Requerido**.                |
| password  | String: formData | **Requerido**. 128 caracteres |
| password2 | String: formData | **Requerido**. 128 caracteres |

```json
{
  "password": "mysupersecretpassword",
  "password2": "mysupersecretpassword"
}
```

#### Respuestas

##### 200 OK

```json
{
  "username": "username",
  "email": "username@username.com",
  "is_active": true
}
```

##### 400 Bad Request

```json
{
  "token": "Token is missing or invalid."
}
```

```json
{
  "password": ["Password fields didn't match."]
}
```

### Contest Winner

Solo los administradores pueden acceder a este endpoint. El sorteo se llevará a cabo entre los usuarios con cuenta activa, excluyendo staff y super usuarios.

```
GET /contest-winner/
```

#### Respuestas

##### 200 OK

```json
[
  {
    "id": 2,
    "email": "username@username.com",
    "first_name": "name",
    "last_name": "last_name",
    "address": "Las Camelias 123",
    "phone": "7842934",
    "bio": "Amo el confort"
  }
]
```

##### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

```json
{
  "detail": "Invalid username/password."
}
```

##### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```
