# RFC 007: PLL Software Synchronization for Wall-Time

## Status
Proposed

## Motivation
In Wall-Time mode (ADR-005), the simulation is slaved to the real-time clock to interact with physical Hardware-in-the-Loop (HIL) emulators. However, physical hardware uses its own onboard crystal oscillator, while the Host PC running VIREON uses another. Over a 24-hour validation run, these crystals will drift relative to each other by several milliseconds due to temperature and manufacturing tolerances.
If VIREON strictly relies on its own Host clock, it will eventually begin dropping frames or blocking indefinitely because the hardware emulator's "tick" will gradually desynchronize from the Host's "tick".

## Proposed Architecture
We propose implementing a **Software Phase-Locked Loop (PLL)** within the Wall-Time scheduler.
1. The Abstract Protocol Adapter (RFC-003) timestamps incoming hardware packets using the Host clock.
2. The Kernel continuously measures the phase error between the hardware's expected packet arrival time and the actual arrival time.
3. The Kernel gently slews (speeds up or slows down) its internal Wall-Time clock frequency by parts-per-million (PPM) to track the hardware emulator's crystal oscillator, keeping the phase error bounded.

## Open Questions
- If the hardware clock drifts, slewing the VIREON clock means the "1 millisecond" simulation tick is no longer exactly 1 real-world millisecond. Does this mathematically invalidate the physical physics calculations (e.g., integration over time $dt$)?
- If multiple disjoint hardware emulators with different crystal drifts are attached simultaneously, whose clock does the PLL slave itself to?

## Next Steps
Determine the regulatory tolerance for clock slewing during biological physics integration.
