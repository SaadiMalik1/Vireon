# VIREON Operations & Deployment Guide

This guide covers deployment strategies for running VIREON in production or cloud environments.

## 1. Cloud Execution (Kubernetes)
To run massive parallel Monte Carlo simulations in a cloud environment:
- Use the `vireon-base-python` Docker image.
- Deploy the `EventBus` as a standalone Pod if utilizing distributed actor topologies (e.g., Ray or Dask integrations).

## 2. CI/CD Pipeline Configuration
To enable deterministic CI tests, configure your runner to export the `VIREON_STRICT_DETERMINISM=1` environment variable. This ensures the master seed overrides any local developer configurations.
