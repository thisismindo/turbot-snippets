project-name = endpoint

up:
	@echo Start: && \
	docker run -it endpoint
build:
	@echo Build: && \
	docker build -t endpoint .
reset:
	@echo [WARNING] Reset project: && \
	docker ps --filter status=exited -q | xargs docker rm
