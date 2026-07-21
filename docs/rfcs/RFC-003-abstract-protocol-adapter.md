# RFC 003: Abstract Protocol Adapter Layer

## Status
Proposed

## Motivation
The Constitution forbids the VIREON runtime from containing protocol-specific code. However, existing vendor emulators and proprietary hardware devices communicate using proprietary protocols (e.g., custom UDP schemas, BLE GATT characteristics).
If we force vendors to rewrite their proprietary hardware emulators to natively speak VIREON's FlatBuffers schema, adoption will fail. We need a bridge.

## Proposed Architecture
We propose introducing an **Abstract Protocol Adapter Layer** that sits outside the core Kernel but inside the VIREON ecosystem.
1. The Adapter is a generic translation daemon.
2. Vendors provide a declarative mapping file (e.g., JSON or DSL) that describes how their proprietary byte stream maps to the standardized VIREON State Graph schema.
3. The Adapter ingests the raw proprietary network packets (e.g., via a virtual TUN/TAP interface or raw socket), unpacks the binary fields according to the vendor's mapping, and pushes the data to the VIREON Data Plane via the Zero-Copy Handoff (ADR-007).

## Open Questions
- Is a declarative mapping file expressive enough to handle complex, stateful packet protocols, or must the adapter support execution of a lightweight parsing script (e.g., Lua)?
- How do we handle protocol-specific encryption (e.g., TLS/DTLS) within this abstract layer?

## Next Steps
Soliciting feedback from network engineers and hardware vendors regarding the edge cases of their proprietary telemetry protocols.
