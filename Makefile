SHELL=/bin/bash -euo pipefail

install: install-node install-python install-hooks

install-python:
	poetry install

install-node:
	sudo npm install -g yarn
	sudo npm install

install-hooks:
	cp scripts/pre-commit .git/hooks/pre-commit

lint:
	# yarn run lint
	# poetry run flake8 **/*.py

clean:
	rm -rf build
	rm -rf dist

publish: clean
	# mkdir -p build
	# yarn run publish 2> /dev/null

serve:
	npm run serve

check-licenses:
	# npm run check-licenses
	# scripts/check_python_licenses.sh

format:
	poetry run black **/*.py

sandbox: update-examples
	cd sandbox && npm run start

build-proxy:
	scripts/build_proxy.sh

release: clean publish build-proxy
	mkdir -p dist
	cp -r build/. dist

release: clean publish build-proxy
	mkdir -p dist
	tar -zcvf dist/package.tar.gz build
	for env in internal-dev internal-qa ref internal-dev-sandbox internal-qa-sandbox sandbox dev int; do \
		cp ecs-proxies-deploy-mock-jwks.yml dist/ecs-deploy-$$env.yml; \
	done

	cp -r build/. dist
	cp -r api_tests dist	

test :
	echo "TODO: add tests"
