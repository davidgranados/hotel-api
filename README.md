# hotel api

El Api consta de tres endpoints

1. rooms: Te permite gestionar los cuartos del hotel
2. reservations: Te permite gestionar el manejo de reservas de habitaciones
3. invoices: Ter permite crear facturas para registrar los pagos de las reservas


# Iniciar proyecto

## Requerimientos
- Docker
- Docker Compose

## Comandos

```
$ docker-compose build
$ docker-compose up -d
$ docker-compose run --rm app sh -c "python manage.py migrate"
$ docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

# Documentación
```
/api/docs/#/
```


# Autenticación

Para autenticarte debes usar el superusuario o crear uno nuevo y obtener un token a través del endpont:
```
/api/users/token/
```
Ese token lo debes enviar en el Header Authorization ejemplo:
```
Token 6cf1e028e4991238f5d576c607b089100114278d
```

# Integración

## Pruebas unitarias
```
$ docker-compose run --rm app sh -c "python manage.py test"
```

## Linters y formaters
- isort
- black
- flake8

### Comandos
```
$ docker-compose run --rm app sh -c "isort /app"
$ docker-compose run --rm app sh -c "black /app"
$ docker-compose run --rm app sh -c "flake8"
```

### Integración continua
```
Github Actions
```
