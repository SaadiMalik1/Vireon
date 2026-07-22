# VIREON System Performance & Latency Benchmarks

**Standard:** `gemi3.6r/vvvv` (Phase 4 Benchmarks)  
**Evidence Package:** `evidence/evidence_package_aca1cdb965fd.json`  

## Performance Metrics Table

| Benchmark Metric | Measured Value | Unit | Specification / Target |
| :--- | :---: | :---: | :--- |
| **EventBus Throughput** | `150335.58` | ops/sec | > 10,000 ops/sec |
| **EventBus Latency (p50)** | `2.936` | µs | < 50.0 µs |
| **EventBus Latency (p99)** | `13.717` | µs | < 200.0 µs |
| **StateStore Read/Write Latency (avg)**| `0.563` | µs | < 10.0 µs |
| **StateStore Latency (p99)** | `0.606` | µs | < 50.0 µs |
| **SPSC Ring Buffer Throughput** | `10139976.29` | ops/sec | > 50,000 ops/sec |
| **Ed25519 Trace Signing Latency** | `0.029` | ms | < 1.0 ms |
| **Orchestrator Tick (10 Providers)** | `1.06` | µs | < 100.0 µs |
| **Orchestrator Tick (100 Providers)**| `8.74` | µs | < 1,000.0 µs |
| **Orchestrator Tick (1000 Providers)**| `92.65` | µs | < 10,000.0 µs |
