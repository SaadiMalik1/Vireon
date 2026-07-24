.PHONY: install test test-integration lint docs sbom docker verify validate clean

install:
	pip install -e ".[dev]"
	maturin develop -m crates/neurodsl/python_ext/Cargo.toml

test:
	pytest
	cargo test --workspace

test-integration:
	pytest tests/test_integration.py

verify:
	python scripts/run_validation.py
	python scripts/validate_docs.py

validate:
	python scripts/run_validation.py
	python scripts/validate_docs.py

lint:
	ruff check .
	mypy vireon
	python scripts/validate_docs.py
	cargo clippy --workspace -- -D warnings
	cargo fmt --check

docs:
	mkdocs build

sbom:
	vireon sbom -o sbom.json

docker:
	docker build -f docker/Dockerfile -t vireon:latest .

clean:
	rm -rf dist build *.egg-info .pytest_cache .mypy_cache .ruff_cache target sbom.json

