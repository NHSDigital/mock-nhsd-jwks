SHELL=/bin/bash -euo pipefail

install:
	 npm install

lint:
	npm run lint

build:
	docker build -t mock-nhsid-jwks .

run:
	docker run -p 9000:9000 mock-nhsid-jwks:latest

