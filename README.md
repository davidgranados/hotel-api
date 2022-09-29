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
http://localhost:8080/api/docs/#/
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
