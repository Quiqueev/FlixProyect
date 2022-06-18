#!/usr/bin/env bash
docker-compose --env-file=config/dev.env $@

docker-compose --env-file=config/dev.env exec postgres psql -h localhost -U movies movies