DC = docker compose
APP = docker-compose.yaml
APP_SERVICE = app
CACHE_SERVICE = redis
DB_SERVICE = db
ENV = --env-file .env

.PHONY: app
app:
	${DC} -f ${APP} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${DC} -f ${APP} logs -f

.PHONY: app-test
app-test:
	${DC} -f ${APP} exec ${APP_SERVICE} pytest

.PHONY: app-down
app-down:
	${DC} -f ${APP} down

.PHONY: pv-key
pv-key:
	mkdir -p certs && openssl genrsa -out certs/jwt-private.pem 2048

.PHONY: pb-key
pb-key:
	openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem