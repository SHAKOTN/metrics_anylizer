tests:
	docker-compose -f docker-compose-ci.yml build
	sleep 5
	docker-compose -f docker-compose-ci.yml run consume pytest --cov=.
	docker-compose -f docker-compose-ci.yml run produce pytest --cov=.

build:
	docker-compose -f docker-compose.yml build


stop_service:
	docker-compose -f docker-compose.yml down

full_run:
	docker-compose -f docker-compose.yml up -d db
	docker-compose -f docker-compose.yml up migrate
	docker-compose -f docker-compose.yml up -d kafka
	sleep 5
	docker-compose -f docker-compose.yml up -d consume
	docker-compose -f docker-compose.yml up -d produce
	make histograms
	make stop_service

histograms:
	docker-compose -f docker-compose.yml up hist