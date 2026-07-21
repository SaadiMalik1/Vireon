# RFC 002: Trace Bundle Compression Strategies

## Status
Proposed

## Motivation
To satisfy scientific reproducibility and regulatory auditing (FDA), the Kernel logs every capability grant, RNG seed, and State Store mutation into a "Trace Bundle".
At neuro-physiological resolutions (e.g., thousands of channels at 30kHz), this generates terabytes of trace data per hour. Uncompressed disk I/O will quickly become the primary bottleneck, causing the bifurcated clock to miss real-time deadlines.

## Proposed Architecture
We propose integrating a real-time delta-encoding and compression pipeline directly into the Kernel's logger, bypassing standard file system I/O streams.
- **Algorithm**: Zstandard (zstd) tuned for time-series data, or a custom delta-varint encoding specific to neuro-data (similar to FLAC for audio).
- **Architecture**: A dedicated Kernel thread reads from the shared memory ring buffer, compresses chunks in memory, and flushes to disk asynchronously.

## Open Questions
- Should the trace bundle be a single monolithic file (e.g., HDF5 or Parquet) or a directory of chunked binary files with a JSON index?
- Can we guarantee that the compression thread will not starve the provider threads on a CPU-constrained host machine?

## Next Steps
Requesting benchmarks from the community comparing `zstd` with custom delta-encoding for raw synthetic neural spike trains.
