# VIREON System Performance & Latency Benchmarks

**Standard:** `gemi3.6r/vvvv` (Phase 4 Benchmarks)  
**Evidence Package:** `evidence/evidence_package_239559d0f56d.json`  

## Performance Metrics Table

| Benchmark Metric | Measured Value | Unit | Specification / Target |
| :--- | :---: | :---: | :--- |
| **EventBus Throughput** | `130087.12` | ops/sec | > 10,000 ops/sec |
| **EventBus Latency (p50)** | `3.306` | µs | < 50.0 µs |
| **EventBus Latency (p99)** | `17.072` | µs | < 200.0 µs |
| **StateStore Read/Write Latency (avg)**| `0.581` | µs | < 10.0 µs |
| **StateStore Latency (p99)** | `0.612` | µs | < 50.0 µs |
| **SPSC Ring Buffer Throughput** | `10072571.87` | ops/sec | > 50,000 ops/sec |
| **Ed25519 Trace Signing Latency** | `0.029` | ms | < 1.0 ms |
| **Orchestrator Tick (10 Providers)** | `1.07` | µs | < 100.0 µs |
| **Orchestrator Tick (100 Providers)**| `8.87` | µs | < 1,000.0 µs |
| **Orchestrator Tick (1000 Providers)**| `92.54` | µs | < 10,000.0 µs |
