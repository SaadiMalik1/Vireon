.PHONY: install test test-integration lint docs sbom docker clean

install:
	pip install -e ".[dev]"
	maturin develop -m crates/neurodsl/python_ext/Cargo.toml

test:
	pytest
	cargo test --workspace

test-integration:
	pytest tests/test_integration.py

lint:
	ruff check .
	mypy src/vireon
	cargo clippy --workspace -- -D warnings
	cargo fmt --check

docs:
	mkdocs build

sbom:
	cyclonedx-py generate -o sbom.json

docker:
	docker build -f docker/vireon.Dockerfile -t vireon:latest .

clean:
	rm -rf dist build *.egg-info .pytest_cache .mypy_cache .ruff_cache target sbom.json
