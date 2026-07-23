> [!NOTE]
> **Notice:** This document is an internally generated, AI-assisted self-review produced during development. It is not an independent or third-party audit.

# VIREON System Performance & Latency Benchmarks

**Evidence Package:** `evidence/evidence_package_379fe46ac66d.json`  

## Performance Metrics Table

| Benchmark Metric | Measured Value | Unit | Specification / Target |
| :--- | :---: | :---: | :--- |
| **EventBus Throughput** | `122109.19` | ops/sec | > 10,000 ops/sec |
| **EventBus Latency (p50)** | `3.547` | µs | < 50.0 µs |
| **EventBus Latency (p99)** | `16.017` | µs | < 200.0 µs |
| **StateStore Read/Write Latency (avg)**| `0.726` | µs | < 10.0 µs |
| **StateStore Latency (p99)** | `1.398` | µs | < 50.0 µs |
| **SPSC Ring Buffer Throughput** | `9684935.48` | ops/sec | > 50,000 ops/sec |
| **Ed25519 Trace Signing Latency** | `0.029` | ms | < 1.0 ms |
| **Orchestrator Tick (10 Providers)** | `1.08` | µs | < 100.0 µs |
| **Orchestrator Tick (100 Providers)**| `8.79` | µs | < 1,000.0 µs |
| **Orchestrator Tick (1000 Providers)**| `93.16` | µs | < 10,000.0 µs |
