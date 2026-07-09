# QIF Whitepaper v8.0 — Working Draft \| Qinnovate

**Source URL:** <https://qinnovate.com/research/whitepaper/>

**Domain:** qinnovate.com

**Extracted At (UTC):** 2026-07-09T06:09:44.935Z

---

[Q innovate \| Open Neural Atlas](/)    [Mission](/mission/)

 [Atlas](/atlas/)

 [R&D](/research/)

      [Demo Atlas \(PoC\)](/demo-atlas/)  [Atlas Overview](/atlas/)  [Whitepaper](/research/whitepaper/)

1. [Home](https://qinnovate.com/)
2. Whitepaper

      Table of Contents

 [Executive Summary](#summary)[The Proposal](#proposal)[BCI Industry](#landscape)  [1. The Problem](#problem)[2. Our Approach](#approach)[3. The Hourglass](#hourglass)[4. TARA Atlas](#tara)[5. NISS Scoring](#niss)[6. Neural Impact Chain](#neural-impact)[8. Governance](#governance)[9. NSP Protocol](#nsp)  [Neural Terminal](#neural-terminal)[Neural OS](#neural-os)[Vision Restoration](#vision-pipeline)  [How to Help](#adopt)[What's Next](#roadmap)[Glossary](#glossary)[Limitations](#limitations)

       ⚠  Working Draft — v8.0

 This version is under active development. Content may change. The [archived v7.1](https://qinnovate.com/research/whitepaper/v7-1/) remains the last stable release.

    ## Executive Summary

  Brain-computer interfaces are shipping in human skulls with no security standard protecting them. The same techniques used therapeutically to treat depression, Parkinson's, and blindness can be weaponized through the same physical mechanisms. The difference between therapy and attack is consent, dosage, and oversight. No existing framework addresses this.

 QIF is a proposed open security framework for neural devices. It provides three things: **TARA**, a catalog of 161 attack techniques mapped to their therapeutic analogs across 11 biological domains; **NISS**, a 6-dimensional severity scoring system that captures what CVSS cannot \(biological impact, consent violation, reversibility, neuroplasticity\); and **NSP**, a post-quantum wire protocol designed for the 50\+ year lifespan of implanted devices.

 This is a proposed framework, not an adopted standard. It has not been independently peer-reviewed. It is built by one researcher with 15 years of security engineering experience. Everything here is open-source, open to criticism, and designed to be replaced by something better.

    If you're a CISO

 Start with [Executive Summary](https://qinnovate.com/research/whitepaper/#summary), then [The Problem](https://qinnovate.com/research/whitepaper/#problem) \(comparison table\), [NISS Scoring](https://qinnovate.com/research/whitepaper/#niss), and [Governance](https://qinnovate.com/research/whitepaper/#governance).

  If you're a researcher

 Read [Our Approach](https://qinnovate.com/research/whitepaper/#approach), [The Hourglass](https://qinnovate.com/research/whitepaper/#hourglass), [TARA Atlas](https://qinnovate.com/research/whitepaper/#tara), and [Limitations](https://qinnovate.com/research/whitepaper/#limitations). Check the [Derivation Log](https://qinnovate.com/news/derivation/).

  If you're a clinician

 Focus on [Neural Impact Chain](https://qinnovate.com/research/whitepaper/#neural-impact), [TARA Atlas](https://qinnovate.com/research/whitepaper/#tara) \(clinical tab\), and [Neurorights](https://qinnovate.com/research/whitepaper/#neurorights).

  If you're a student

 Read top to bottom. Start with [The Proposal](https://qinnovate.com/research/whitepaper/#proposal). The [Defense Paradox](https://qinnovate.com/research/whitepaper/#defense-paradox) and [Design Principles](https://qinnovate.com/research/whitepaper/#design-principles) teach the foundations.

## Author's Note

  I built this framework because no one else had. To my knowledge, there was no threat model for the human mind. So I wrote one.

 It started with a question: what would threat modeling for the human mind look like? That question led me into the world of brain-computer interfaces, and quickly made clear that you cannot build for the brain the way you build for a screen. The technical architecture alone is not enough. To do this right from the design phase, I applied two decades of security instincts and went deep into the disciplines that should inform every decision at this layer: neuroethics, AI ethics, and the emerging fields of neurorights and neuroprivacy.

 I believe it is vital for the adoption of BCIs, and in the best interest of every company building them, that we embed ethics and security by design. The last thing we should do in pursuit of cures for the sick and the unable is introduce vulnerabilities to an already vulnerable mind. It is our duty as engineers and architects to understand the full scope in which a clinical remedy may introduce more risk than reward, and to design systems that make that calculus transparent.

 That is the mission behind this paper.

 The concepts here span neuroscience, security architecture, ethics, law, and clinical medicine. Some are well-established; many are proposed and unvalidated. I have worked to distill them into a single coherent framework, and to be explicit about where the evidence is strong and where the work is still theoretical.

 — Kevin Qi

## The Proposal

  Every transformative technology gets one chance to build its foundation right. The internet did not take that chance. TCP/IP shipped without authentication. HTTP shipped without encryption. DNS shipped without integrity verification. We spent the next four decades bolting on security after the fact. TLS, DNSSEC, OAuth, zero-trust architectures. Each one a patch on a foundation that was never designed to be secure.

 Brain-computer interfaces are at that same inflection point. The first cortical implants are in human skulls. The first commercial devices are shipping. And the security architecture is, once again, an afterthought. The difference this time is that the attack surface is not a credit card number or a social security record. It is the human nervous system. There are no rollbacks for neural tissue damage. There is no “change your password” for a compromised sensory cortex.

 This is not a warning. It is a proposal.

### The Blank Slate

 We are building from a blank slate. That is the advantage. We have full knowledge of every security failure that preceded us. The goal is to design a BCI security architecture that introduces as little technical debt as possible. Every layer is intentional. Every protocol earns its place. Where the internet added security as middleware, this architecture embeds it at the kernel level. Where medical devices shipped firmware as proprietary black boxes, this architecture proposes open-source auditability from day one.

### The Vision

 QIF proposes a BCI security architecture designed to stand the test of time. Not for a product cycle, but for the full span of a human life. A person implanted at 30 may carry that device for 70 years. The architecture must outlast the company that built it, the protocol standard it launched with, and the threat environment it was designed against.

### This already happened

  In March 2020, Second Sight Medical Products announced it would wind down operations, laying off 84 of 108 employees. More than 350 patients worldwide had Argus II retinal implants in their eyes. They were not notified directly. Some learned from their vision rehabilitation therapists, who had just been laid off.

 The company stopped software upgrades, stopped supplying replacement components, and stopped answering physician support lines. One patient needed an MRI to check for a possible brain tumor. His doctors could not proceed because the Argus II's interaction with MRI magnetic fields required manufacturer consultation, and the manufacturer was not responding. He got a CT scan instead. He still does not know if he has a brain tumor.

 Another patient heard a small beeping sound while changing trains in a New York subway station. Her device powered down permanently. It never worked again. The defunct hardware remains in her eye because explantation surgery risks retinal detachment and further vision loss.

 Second Sight did not formally dissolve. It merged with Nano Precision Medical in 2022, becoming Vivani Medical. The neurostimulation business was spun off as Cortigent in 2025. No structured support program for the 350\+ Argus II patients has been publicly announced.

 Sources: [IEEE Spectrum](https://spectrum.ieee.org/bionic-eye-obsolete) \(Strickland & Harris, 2022\), [BusinessWire](https://www.businesswire.com/news/home/20200330005581/en/) \(March 30, 2020\).

### Patient-First Equity

 The starting point is the patient. The people who need BCIs most urgently, those with severe motor impairment, blindness, locked-in syndrome, are also the most vulnerable to exploitation by closed systems they cannot inspect, modify, or leave. Building patient sovereignty into the architecture is not a feature. It is a prerequisite for equitable access. The patient can inspect every signal entering their nervous system. The patient can disconnect without asking a cloud service for permission. The patient can switch hardware without being locked into a vendor's ecosystem.

## Claims and Disclaimers

### What This Paper Claims

     BCI security is under-addressed

 The threat surface of neural interfaces has not received the same architectural rigor as enterprise IT, mobile, or IoT security. The attack techniques cataloged in TARA are derived from published neuroscience, signal processing, and cybersecurity literature.

    Security and ethics are inseparable at this layer

 A BCI security architecture that ignores neuroethics will fail its patients. A neuroethics framework that ignores security engineering will remain aspirational. This paper attempts to bridge both.

    The blank slate window is closing

 Designing from a blank slate is possible now, and will not be later. Once devices ship at scale with baked-in architectural decisions, changing those decisions becomes exponentially harder.

### What This Paper Does Not Claim

   QIF is not a standard

 It is a proposed framework. Not adopted by any standards body, not independently peer-reviewed, not validated in clinical deployment. All components \(TARA, NISS, NSP, Runemate\) are proposals.

  NISS does not measure cognitive harm

 NISS scores physical signal-level disruption. DSM-5-TR category mappings are for threat modeling purposes only — diagnostic category references, not diagnostic claims.

  This paper does not read minds

 Current BCI technology cannot "read thoughts." Decoded outputs are selected from constrained vocabularies, require user cooperation, and depend on individually trained algorithms.

  Engineering benchmarks are unverified

 Quantitative claims about NSP compression, power overhead, and latency are AI-derived estimates, not empirical measurements. They require independent engineering validation.

### Epistemic Framework

| Level | Meaning | Example |
| --- | --- | --- |
| Verified | Peer-reviewed, resolved DOI | Published attack techniques, cited neuroscience |
| Established | Strong consensus, official docs | NIST AI RMF, EU AI Act, CVSS methodology |
| Inferred | Logical deduction from verified premises | Threat chain mappings, architectural implications |
| Theoretical | Author's proposed framework | QIF hourglass, NISS, Cs metric, NSP, Runemate |
| Unknown | Insufficient evidence | Open questions stated explicitly |

## The Defense Paradox

  Every security defense introduces new attack surface. This is inevitable. SSL was designed to secure the web and gave us Heartbleed. Firewalls were designed to filter traffic and became misconfiguration targets. Password managers were designed to store credentials, and LastPass was breached. The defense paradox is not an argument against defense. It is a design constraint: **minimize the number of layers, because each layer is a place the paradox can bite.**

### The Stubborn Eyelash

 Think of trying to remove a stray eyelash that has half fallen off and is poking at your eyeball. Using your fingers to surgically extract it pushes it deeper into the eye. The tool you reach for creates the problem you are trying to solve. Precision and technique matter more than force. The same principle applies to BCI security: adding more layers without precision creates more surfaces for the paradox to exploit.

### From Armor to Kevlar: Security Through Innovation

   🛡

 Armor

 Piling on layers. Brute-force protection. Heavy, slow, vulnerable at joints.

  ⚔

 Steel

 Iron \+ carbon. A material innovation that replaced brute thickness with engineered strength.

  🧪

 Kevlar

 Synthetic aramid polymer \(Kwolek, DuPont, 1965\). Moved beyond carbon entirely. Lighter, stronger, engineered at the molecular level.

 We are not trying to fabricate steel from iron ore. We are engineering a metaphorical polymer. **AI has the potential to be that polymer**, but only if it is crafted with precision. The fundamentals are non-negotiable: human-in-the-loop oversight at every decision boundary, consent that is explicit and informed rather than implicit or buried in terms of service, and neurorights enforced at the architecture level rather than assumed by policy. Without these constraints, AI-driven neural security becomes AI-driven neural surveillance. The difference between the two is not the technology. It is the governance. Beyond ethics, the engineering challenge is equally unforgiving: **configuration drift** must not occur. Drift is too common in code, and at wide scale with neural devices, it would be catastrophic.

### Golden Image: Hardening at Every Layer

| Layer | QIF Component | Golden Image Mechanism |
| --- | --- | --- |
| Hardware | Neurowall | Cryptographic firmware attestation \(SPHINCS\+\). Secure boot chain. Any deviation from the signed image = reject. |
| Software | NSP \+ Runemate | Protocol-level integrity checks. Every frame authenticated with AES-256-GCM. Content compiled to deterministic bytecode. |
| Configuration | Tiers 3–5 | Explicit reconsent for any model update. Drift detection via coherence metric time series. Anomaly signals on deviation. |
| Biomarker | Baseline | Per-patient neural baseline established at calibration. Adaptive model bounded within consented envelope. Drift beyond bounds = alert. |

## Design Principles

 Nine principles governing every architectural decision in this framework.

    1 #### Zero technical debt

 Every protocol earns its place. No inherited assumptions from screen-based computing.

  2 #### Patient sovereignty by default

 Inspect, disconnect, switch. Not aspirational. Architectural.

  3 #### Minimize perimeter

 Fewer layers = fewer attack surfaces = fewer places the defense paradox can bite.

  4 #### Security enables medicine

 NSP is not the brake. It is the safety certification that makes clinical BCI possible.

  5 #### Dual-use registry

 Every attack technique has a therapeutic analog. The boundary is consent, dosage, and oversight.

  6 #### Post-quantum from day one

 Neural data has a lifetime shelf life. Harvest Now, Decrypt Later is not theoretical.

  7 #### Open by default

 Apache 2.0. Neural security standards are too critical to be proprietary.

  8 #### Ethics by architecture

 Neuroethics, AI ethics, and neurorights encoded as kernel-level constraints, not policy documents.

  9 #### AI honesty, not AI obscurity

 The system says "I don't know" when it doesn't know. Trust through verifiability.

## BCI Industry Overview

 Over $4 billion in disclosed venture funding deployed into BCI companies through 2024 \(source: Pitchbook, Tracxn\), with annual investment reaching $2.3B in 2024 alone. To our knowledge, none have published public-facing security documentation. This section surveys the companies building neural interface technology.

  **The security gap:** To our knowledge, no BCI manufacturer, Neuralink, Synchron, Blackrock Neurotech, Science Corp, OpenBCI, or Emotiv, has published an independent security audit or a full wireless security specification. Emotiv's AES-128-ECB encryption was [disclosed as using broken ECB mode in 2013](https://www.cryptofails.com/post/70333773685/broadcast-your-brain-fixed-key-ecb-mode). OpenBCI's protocol documentation contains zero mentions of encryption.

#### Neuralink

 $1.29B · Implantable · Bidirectional

 N1 implant \(1,024 electrodes\). First human implants 2024. Motor intent decoding. Telepathy app for device control.

#### Synchron

 $145M\+ · Endovascular · Read

 Stentrode deployed via blood vessels \(no open-brain surgery\). FDA Breakthrough designation. Motor-impaired patients controlling devices.

#### Paradromics

 $103M\+ · Implantable · Read

 Connexus Direct Data Interface. 65,000\+ electrodes. High-bandwidth cortical recording for speech prosthesis.

#### Precision Neuroscience

 $93M\+ · Implantable · Read

 Layer 7 Cortical Interface — thin-film electrode array placed on the brain surface. Minimally invasive, high-resolution recording.

#### Science Corp

 $552M\+ · Implantable · Write

 Founded by Max Hodak \(Neuralink co-founder\). PRIMA retinal implant \(2,378 photovoltaic pixels\). Acquired Pixium Vision \(2024\). Vision restoration via subretinal stimulation.

#### Blackrock Neurotech

 $10M\+ · Implantable · Bidirectional

 Utah Array — the most widely used implanted BCI in research. Over 30 years of human implant data. Foundation for BrainGate trials.

  **Disclaimer:** This is not an exhaustive list. Other companies are building in stimulation therapy, consumer EEG, neurofeedback, and neural data analytics. This section will be updated as new entrants are identified.

# The same technique that can harm a brain can also heal one

 QIF is a proposed open framework that maps BCI techniques to their security risks, clinical applications, and potential psychiatric outcomes in a single unified model.

 161 catalogued techniques. 11 architectural bands. 6 neural-specific scoring metrics. DSM-5-TR diagnostic category references \(for threat modeling, not diagnostic claims\). Therapeutic applications for the majority of known attack vectors. *Clinical mappings are research-based references requiring validation by psychiatrists and neuroscientists.*

## BCI Industry Funding

 Over $4 billion in disclosed venture funding deployed into BCI companies through 2024 \(source: Pitchbook, Tracxn\), with annual investment reaching $2.3B in 2024 alone \(Neuralink $1.29B, Synchron $145M, Paradromics $103M, Precision Neuroscience $93M, and others\). To our knowledge, none have published public-facing security documentation. Click any company for funding rounds and investors.

 Source: QIF BCI Landscape Database v2.0. Hover to inspect, click to expand.

## QIF Hourglass Model

     ↑ Indeterministic Deterministic ↓

      Neural Domain

 [N7 Neocortex](/news/derivation/hourglass.html#N7) [N6 Limbic System](/news/derivation/hourglass.html#N6) [N5 Basal Ganglia](/news/derivation/hourglass.html#N5) [N4 Diencephalon](/news/derivation/hourglass.html#N4) [N3 Cerebellum](/news/derivation/hourglass.html#N3) [N2 Brainstem](/news/derivation/hourglass.html#N2) [N1 Spinal Cord](/news/derivation/hourglass.html#N1)   I0 — Interface Bottleneck

[I0 Neural Interface](/news/derivation/hourglass.html#I0)   Synthetic Domain

[S1 Near-Field / On-Device](/news/derivation/hourglass.html#S1) [S2 Guided-Wave / Host-Local](/news/derivation/hourglass.html#S2) [S3 Far-Field / Wide-Area](/news/derivation/hourglass.html#S3)   ← Spatial Scale →

  [Explore the full interactive model →](/news/derivation/hourglass.html)

     Working Paper

 Securing Neural Interfaces: Architecture, Threat Taxonomy, and Neural Impact Scoring for Brain-Computer Interfaces

 Kevin Qi · Qinnovate · Feb 2026 · 28 pages, 6 figures · CC-BY 4.0

 DOI: [10.5281/zenodo.18640105](https://doi.org/10.5281/zenodo.18640105)

 This working paper contains the full mathematical derivations, QI equation, and falsifiability conditions. The research proposal below is the accessible companion.

  [Download PDF](/papers/qif-bci-security-2026.pdf) [View on Zenodo](https://zenodo.org/records/18640105)

    161

 techniques catalogued

  32

 critical severity

  70

 irreversible

  102

 with therapeutic use

  76

 DSM-5-TR mapped

  11

 hourglass bands

     ## 1. The Problem

  There are chips in human brains right now with no security standard protecting them.

 Neuralink has implanted its N1 chip in human patients. Synchron's Stentrode is in FDA-approved clinical trials. Blackrock Neurotech has shipped Utah arrays for over a decade. Commercial EEG headsets from Emotiv, Muse, and OpenBCI sit on consumer shelves. These devices are tested for safety and efficacy. They are not tested against adversarial threats. To our knowledge, no standardized framework exists to classify, score, or mitigate attacks on the human brain.

 Existing vulnerability scoring systems were designed for software. CVSS v4.0 measures three properties: confidentiality, integrity, and availability. These are sufficient for databases and web servers. These metrics are insufficient for devices that directly interface with the human brain. CVSS cannot express biological tissue damage. It cannot quantify the loss of cognitive integrity. It lacks metrics for consent violation, irreversibility, and neuroplastic change.

 The result is a scoring gap. Current CVSS scores for BCI vulnerabilities capture only a partial picture of potential impact. A signal injection attack that induces phantom sensory perception receives the same severity score as a buffer overflow, despite one being a software bug and the other a direct violation of an individual's subjective experience.

 This is an immediate concern. The threat surface already exists. We have catalogued **161 techniques** across 8 categories, from signal injection to cognitive integrity violations. **32 are critical severity**. **39 trigger the PINS flag** for Potential Impact to Neural Safety. **70 cause irreversible or partially irreversible damage**.

  The gap in numbers

 CVSS v4.0 cannot score 63.4% of the catalogued techniques. Their neural-specific impacts have no CVSS equivalent. Before NISS, no scoring framework could quantify biological impact, cognitive disruption, consent violation, reversibility, or neuroplastic change.

  How QIF compares

| Capability | CVSS 4.0 | ATT&CK | IEC 62443 | QIF |
| --- | --- | --- | --- | --- |
| Neural impact scoring | ✗ | ✗ | ✗ | ✓ |
| BCI threat technique catalog | ✗ | Partial | ✗ | ✓ |
| Dual-use mapping \(therapy ↔ attack\) | ✗ | ✗ | ✗ | ✓ |
| Consent violation metrics | ✗ | ✗ | ✗ | ✓ |
| Reversibility / neuroplasticity | ✗ | ✗ | ✗ | ✓ |
| Post-quantum protocol | ✗ | ✗ | ✗ | ✓ |
| Neuroethics guardrails | ✗ | ✗ | ✗ | ✓ |
| IT/enterprise coverage | ✓ | ✓ | ✓ | ✗ |
| Industry adoption | Standard | Standard | Standard | Proposed |
| Peer review | Yes | Yes | Yes | Pending |

 QIF supplements these frameworks for a domain they do not cover. It does not replace them.

     ## 2. Our Approach

  The same physics that makes a BCI technique dangerous also makes it therapeutic. Transcranial magnetic stimulation treats depression and induces seizures. Deep brain stimulation manages Parkinson's and causes involuntary movement. The mechanism is identical. The difference is intent, dosage, and governance.

 Security and clinical safety are not separate problems. They are two views of the same system. A framework that only catalogs threats misses half the picture. A framework that only tracks therapies misses the risks. QIF maps both, for every technique, in a single proposed framework.

 All publications are released under the Apache 2.0 license. Neural security standards are too critical to be proprietary. The people whose brains will be connected deserve to understand exactly how they are protected.

 We address this with three interlocking pillars:

   [◆ QIF Model Quantified Interconnection Framework **The governance architecture.** The OSI of Mind. An 11-band hourglass model mapping every surface — from neural tissue to synthetic systems — where security threats and ethical risks converge. One auditable framework for both. 8.0 · Published](/research/whitepaper/)[▲ TARA Therapeutic Applications & Risk Assessment **The TARA Atlas.** 161 BCI techniques mapped across four projections — modality, clinical, diagnostic \(DSM-5-TR\), and governance — each scored with NISS and traced through the Neural Impact Chain from attack to clinical outcome. 1.7 · Atlas Published](/atlas/tara/)[■ NSP Neural Sensory Protocol **The wire protocol.** An RFC-style post-quantum protocol ensuring patient safety and data privacy — securing BCI data links with five defense layers at 3.25% power overhead. 0.4 · Secure Core Complete](/guardrails/nsp/)

#### Why all three are required

  **QIF without NSP** identifies threats but cannot prevent their transmission. A threat model lacking a wire protocol is a map with no vehicle.

 **NSP without QIF** encrypts data but cannot detect manipulation at the electrode-tissue boundary. A protocol without an underlying threat model provides protection without informed strategy.

 **Both without a compiler** hit a bandwidth wall. Post-quantum cryptographic keys — the mathematical structures that protect data from future quantum computers — are 18–46× larger than their classical equivalents. This overhead strains adoption on implants operating within a 40 mW power budget over Bluetooth Low Energy \(BLE\). Runemate’s proposed Staves DSL compiler targets 65–90% compression of multimodal BCI content in benchmarks, aiming to make post-quantum security practical on constrained hardware. Unlike today’s outward-only BCIs \(Neuralink N1, BrainGate\) where all rendering happens on a phone, Runemate targets next-generation implants that render content inward — directly to cortical tissue — requiring on-chip decode, safety-check, and render with no external device in the loop.

    ### Worked Example: Signal Injection via Compromised Stream

 One technique traced through the full QIF pipeline. Hourglass band → TARA technique → NISS score → clinical reference → defensive control.

      S2

   Entry Point Transport [QIF-T0003](/atlas/tara/T0003/)

 Attacker on local network discovers an unencrypted LSL stream broadcasting raw EEG data from a research headset.

  S1

   Pivot Near-Field [QIF-T0009](/atlas/tara/T0009/)

 Using captured signal characteristics \(dominant alpha frequency, electrode impedance profile\), attacker crafts a spoofed signal matching the device signature.

  I0

   Injection Interface [QIF-T0001](/atlas/tara/T0001/)

 Crafted RF signal couples through the electrode-tissue boundary at I0. The device cannot distinguish injected signal from endogenous neural activity.

  N7

   Neural Impact Neocortex

 Injected signal disrupts cortical oscillations at target frequency band. Neurofeedback application provides incorrect feedback based on corrupted signal.

 NISS:1.1/BI:H/CR:H/CD:H/CV:E/RV:P/NP:T → 6.1 \(Medium\)

  DSM-5

   Clinical Reference Threat Model

 For threat modeling purposes: disruption pattern corresponds to adjustment disorder categories. This is a threat modeling reference, not a diagnostic claim.

  Control

   Defense Mitigation

 Break the chain at S2: encrypt the LSL stream \(TLS tunnel or BrainFlow encrypted WebSocket\). Break at I0: amplitude bounds and impedance monitoring. Break at N7: coherence metric \(Cs\) anomaly detection.

  Transport encryptionAmplitude bounds at I0Coherence monitoring

 The chain breaks at any defended point. Three independent controls \(transport encryption, amplitude bounds, coherence monitoring\) must all fail for the attack to reach neural impact. Defense in depth, not defense in one layer.

     ## 3. The Hourglass

### 3.1 Where the Architecture Comes From

 The 11-band model was not designed from first principles. It was derived by converging three established layered architectures:

1. **The OSI model** \([ISO/IEC 7498](https://www.iso.org/standard/20269.html)\) — 7 layers that decompose a network into physical, data link, network, transport, session, presentation, and application. Every security framework for digital systems uses some variant of this decomposition. But the OSI model stops at the wire. It has no concept of the biological system connected to the other end.
2. **Neural systems anatomy** \([Kandel et al., *Principles of Neural Science*, 6th ed., 2021](https://neurology.mhmedical.com/book.aspx?bookid=3024)\) — The brain is not a single structure. It is a hierarchy of functionally distinct regions: spinal cord, brainstem, cerebellum, diencephalon \(thalamus/hypothalamus\), basal ganglia, limbic system, and neocortex. Each has different cellular architecture, different oscillatory regimes, and different clinical consequences if compromised. The 7 neural bands \(N7–N1\) map directly to this established neuroanatomical hierarchy, with thalamic relay logic \([Sherman & Guillery, 2006](https://mitpress.mit.edu/9780262513449/exploring-the-thalamus-and-its-role-in-cortical-function/)\) providing the gating mechanism between cortical and subcortical layers. An architecture that treats “the brain” as one layer misses this entirely.
3. **The bio-digital boundary** \([Deering, 2001](https://www.ietf.org/proceedings/51/slides/plenary-1/); the Internet hourglass principle\) — Where electrodes touch tissue, signals transition from ionic to electronic. This is not a clean handoff. It is a physical interface with its own impedance characteristics, its own failure modes, and its own threat profile. The I0 band applies Deering’s hourglass insight — that all traffic must pass through a narrow waist — to the electrode-tissue boundary, where every neural signal crosses from biology to silicon. Neither the OSI model nor neuroanatomy alone accounts for this zone.

 QIF maps all three onto a single stack. The 7 neural bands \(N7–N1\) come from neuroanatomy, ordered by clinical severity. The 3 synthetic bands \(S1–S3\) come from the electronic processing chain, analogous to OSI's lower layers. The interface band \(I0\) is the bridge — the electrode-tissue boundary where biology becomes data. The result is an 11-band, **7-1-3 asymmetric hourglass**: wide at the top \(neural complexity\), narrow at the center \(physical bottleneck\), and wider at the bottom \(synthetic processing\).

#### 3.2 Why These Bands and Not Others

 Each band corresponds to a distinct **scale-frequency regime**. Cortical oscillations at N7 operate in the 1–100 Hz range across centimeter-scale structures. Spinal reflexes at N1 propagate at 80–120 m/s through meter-scale pathways. The analog front-end \(S1\) processes signals in the kHz–MHz range. Radio telemetry \(S3\) operates at 2.4 GHz.

 The physics that governs each regime is fundamentally different, and so are the threats. An anomalous 40 Hz gamma injection at N7 is detected differently than a firmware exploit at S2. The band boundaries are not arbitrary — they follow the relationship L = v/f \(wavelength equals propagation velocity divided by frequency\), where the physical scale of each structure matches its characteristic frequency. When a measured signal violates this constraint, it indicates injection from outside the expected regime.

 The mathematical formalization of signal integrity scoring is future work, pending collaboration with physicists and neuroscientists. See [BCI Physics Constraints](https://qinnovate.com/research/physics/) for the current constraint system.

### 3.3 Architecture

 The QIF Hourglass is an 11-band architectural model that maps all potential threat surfaces within a BCI, from the highest cortical structures through the electrode-tissue boundary and into the synthetic processing chain.

 Seven bands are **neural** \(N7 Neocortex through N1 Spinal Cord\), representing biological tissue with distinct functional properties and vulnerability profiles. One band is the **interface** \(I0\), the electrode-tissue boundary where biological signals are converted to digital data, and where the highest concentration of techniques converges. Three bands are **synthetic** \(S1 Near-Field through S3 Far-Field\), covering the electronic processing, host compute, and communication chain.

 The hourglass shape is deliberate. I0, the neural interface band, constitutes the architectural chokepoint. All signals must traverse this point. With over half of the 161 catalogued techniques targeting this band, it represents the majority of the total threat surface. Securing I0 is the single highest-leverage investment in BCI safety.

### The 11-Band Hourglass

 7 neural \+ 1 interface \+ 3 synthetic bands

  Neural \(N7 – N1\)

    N7 Neocortex

 47

  N6 Limbic System

 38

  N5 Basal Ganglia

 29

  N4 Diencephalon

 33

  N3 Cerebellum

 18

  N2 Brainstem

 21

  N1 Spinal Cord

 12

  Interface \(I0\)

    I0 Neural Interface

 52

  ↑ Bottleneck — highest attack surface

  Synthetic \(S1 – S3\)

    S1 Near-Field/On-Device

 34

  S2 Guided-Wave/Host-Local

 41

  S3 Far-Field/Wide-Area

 28

 11 bands ·
353 total attack mappings ·
I0 concentrates 52 techniques at the neural–silicon boundary

#### How to read the hourglass

  **Y-axis \(vertical\):** Bands ordered by anatomical hierarchy, from neocortex \(N7\) at the top through the electrode-tissue interface \(I0\) at the waist to radio/wireless \(S3\) at the bottom.

 **X-axis \(bar width\):** Number of catalogued techniques targeting that band. Wider bars mean a larger attack surface. I0 is the widest because every technique that crosses the bio-digital boundary converges at this single point.

 **The shape:** The hourglass narrows at I0 not because it has fewer threats, but because it is a physical bottleneck. All neural data must pass through this point. The concentration of techniques at the waist is what makes it the highest-leverage target for both attack and defense.

  Each band has a distinct threat profile. Neural bands \(N7–N1\) are susceptible to attacks that induce biological damage, cognitive disruption, and potentially irreversible neuroplastic change. Synthetic bands \(S1–S3\) confront classical cybersecurity threats such as eavesdropping, data manipulation, and denial of service. The interface band \(I0\) is uniquely vulnerable to both, serving as the nexus where synthetic attacks can translate into neural damage.

| Band | Name | Zone | Description |
| --- | --- | --- | --- |
| N7 | Neocortex | neural | PFC, M1, V1, Broca, Wernicke — executive function, language, movement, perception |
| N6 | Limbic System | neural | Hippocampus, amygdala, insula — emotion, memory, interoception |
| N5 | Basal Ganglia | neural | Striatum, STN, substantia nigra — motor selection, reward, habit |
| N4 | Diencephalon | neural | Thalamus, hypothalamus — sensory gating, consciousness relay |
| N3 | Cerebellum | neural | Cerebellar cortex, deep nuclei — motor coordination, timing |
| N2 | Brainstem | neural | Medulla, pons, midbrain — vital functions, arousal, reflexes |
| N1 | Spinal Cord | neural | Cervical through sacral — reflexes, peripheral relay |
| I0 | Neural Interface | interface | Electrode-tissue boundary — measurement/collapse, quasi-quantum zone |
| S1 | Near-Field / On-Device | synthetic | Amplification, ADC, near-field EM coupling \(0-10 kHz, on-device\) |
| S2 | Guided-Wave / Host-Local | synthetic | Firmware, drivers, host compute, USB, decoding, BLE/WiFi baseband \(10 kHz - 1 GHz, device-local\) |
| S3 | Far-Field / Wide-Area | synthetic | RF transmission, directed energy, application layer \(1 GHz\+, off-device\) |

  [Explore the Interactive Layer Explorer →](/news/derivation/hourglass.html)

     ## 4. TARA Atlas

 One proposed framework for both sides of the brain.

  TARA \(Therapeutic Applications & Risk Assessment\) is a dual-use atlas of 161 BCI techniques. Every entry is three things at once: a security threat, an ethical concern, and a potential therapy. Of these, 102 have confirmed therapeutic applications with published clinical evidence. 76 are mapped to DSM-5-TR psychiatric diagnoses. This is not a threat registry with clinical notes appended. It is a single atlas built from the ground up to serve security engineers, clinicians, researchers, and regulators from the same source of truth.

 TARA exposes each technique through four explicit projections:

- **Modality** — Attack severity, status, and physical coupling mechanism
- **Clinical** — Therapeutic analog, FDA status, evidence level, treated conditions
- **Diagnostic** — DSM-5-TR diagnostic mapping via the Neural Impact Chain
- **Governance** — Consent tier, regulatory requirements, data classification

 Each technique can be analyzed through any of these projections. Interactive exploration of the TARA grid reveals all four perspectives for a given technique: its neural effects, potential therapeutic applications, diagnostic mappings, and applicable regulations.

 TARA organizes 161 techniques across 7 operational domains and 17 tactics using a `QIF-[Domain].[Action]` format:

     QIF-N.SC 3

 Neural Scan

  QIF-B.IN 6

 BCI Intrusion

  QIF-N.IJ 11

 Neural Injection

  QIF-C.IM 6

 Cognitive Imprinting

  QIF-B.EV 6

 BCI Evasion

  QIF-D.HV 11

 Data Harvest

  QIF-P.DS 19

 Physiological Disruption

  QIF-N.MD 24

 Neural Modulation

  QIF-C.EX 17

 Cognitive Exploitation

  QIF-E.RD 13

 Energy Radiation

  QIF-M.SV 9

 Model Subversion

  QIF-S.RP 5

 Sensor Repurposing

  QIF-S.FP 4

 Sensor Fingerprinting

  QIF-S.HV 16

 Sensor Harvest

  QIF-S.CH 6

 Sensor Chaining

  QIF-S.SC 2

 Sensor Side-Channel

  QIF-N.NM 3

 Nanoparticle-Mediated Neuromodulation

### Attack Categories

 9 taxonomic categories spanning the BCI attack surface

   Signal Injection \(SI\)

 18

 Cognitive Reconnaissance \(CR\)

 16

 Cognitive/Functional Disruption \(CD\)

 16

 Data Manipulation \(DM\)

 14

 Privilege Escalation \(PE\)

 12

 Denial of Service \(DS\)

 11

 Physical Safety \(PS\)

 10

 Signal Eavesdropping \(SE\)

 9

 Data Exfiltration \(EX\)

 9

### Severity Distribution

 Classified by potential impact on neural integrity

   Critical

 32

 High

 69

 Medium

 56

 Low

 4

 161 techniques catalogued

### Dual-Use Classification

 Every technique that can harm a brain can also heal one

  131 of 161 therapeutic

     Confirmed \(102\)

   Probable \(19\)

   Possible \(10\)

   Silicon Only \(30\)

 81.4% of catalogued techniques have confirmed, probable, or possible therapeutic applications

  Of the 161 techniques, 102 have **confirmed** therapeutic applications — published clinical use with evidence. Another 19 are **probable** \(under active investigation\) and 10 are **possible** \(theoretical mapping exists\). Only 30 are pure silicon-only vectors with no known tissue analog.

  Latest · v1.6

 FDORA §3305 Regulatory Compliance Mapping: 0 new techniques, all with confirmed clinical applications.

- \+ Regulatory gap analysis enables targeted FDORA compliance for BCI manufacturers
- \+ Coverage scoring identifies techniques where existing standards are insufficient
- \+ 74 techniques have coverage below 0.5 \(major gaps\)
- \+ Per-technique gap lists provide actionable compliance checklists

 [View recent additions in the TARA Atlas →](/atlas/tara/)

#### How to Read the TARA Atlas

  TARA is structured as an interactive grid. Each row is a technique \(identified by a QIF-T ID\). Each column depends on which **projection** you are viewing:

   Modality Projection

 Shows the technique's severity rating \(critical/high/medium/low\), current status \(theoretical, demonstrated, or deployed\), coupling mechanism \(how it reaches tissue\), and which hourglass bands it targets.

  Clinical Projection

 Reveals the therapeutic analog — the established medical procedure that shares the same physics. Includes FDA approval status, evidence level \(confirmed, probable, possible, silicon-only\), and treated conditions.

  Diagnostic Projection

 Maps each technique through the Neural Impact Chain to corresponding DSM-5-TR diagnostic category references \(for threat modeling purposes\), risk class \(acute, chronic, progressive\), and the specific cognitive or motor function disrupted.

  Governance Projection

 Displays the consent tier \(open, informed, IRB, prohibited\), applicable regulatory frameworks, and data classification level. Use this to determine what oversight a technique requires before deployment.

 **Reading a cell:** Click any technique to expand its full detail. The NISS vector \(e.g., BI:H/CR:H/CD:C/CV:H/RV:P/NP:T\) encodes all six scoring dimensions. The DSM-5-TR mapping shows which diagnostic category references the technique's impacts correspond to \(for threat modeling purposes\). The dual-use flag indicates whether the same mechanism has an established therapeutic application.

 **Severity colors:** Red = critical \(NISS ≥ 9.0\), Orange = high \(7.0–8.9\), Yellow = medium \(4.0–6.9\), Green = low \(< 4.0\). The PINS flag \(persistent involuntary neural stimulation\) is shown separately — 39 techniques carry this flag, indicating potential for ongoing harm after the initial exposure.

  [Open the TARA Atlas →](/atlas/tara/) Browse the full grid. Click any cell. Switch between all four projections.

     ## 5. NISS Scoring

  NISS is a proposed vulnerability scoring system built for neural devices. CVSS measures three things: confidentiality, integrity, availability. NISS measures six:

      #### Biological Impact \(BI\)

 Quantifies physical damage to neural tissue. Scores range from None \(N\) through Low, High, to Critical \(C\), denoting permanent tissue destruction. A buffer overflow scores BI:N, whereas a seizure-inducing technique scores BI:H or BI:C.

    #### Cognitive Reconnaissance \(CR\)

 Captures read-side attacks: neural data inference, signal pattern classification, and state estimation. Neural eavesdropping with partial state inference scores CR:L, while comprehensive neural data exfiltration scores CR:C. Techniques with no cognitive read impact score CR:N.

    #### Cognitive/Functional Disruption \(CD\)

 Captures write-side attacks: perception manipulation, identity modification, and cognitive coercion. A phantom sensory injection scores CD:H, while a technique that alters the subject's sense of agency scores CD:C. Techniques with no cognitive write impact score CD:N.

    #### Consent Violation \(CV\)

 Measures the degree to which a subject's autonomy is compromised. Ranges from None \(N\) for standard operation, to Partial \(P\) for degraded consent, Extensive \(E\) for bypassed consent, and Involuntary \(I\) when the subject lacks awareness of the intervention.

    #### Reversibility \(RV\)

 Indicates the potential for damage to be undone. Fully Reversible \(F\) implies complete expected recovery, Treatable \(T\) indicates recovery requiring intervention, Partially Reversible \(P\) denotes some permanent change, and Irreversible \(I\) signifies permanent damage.

    #### Neuroplasticity \(NP\)

 Reflects whether the technique induces physical reorganization of the brain. None \(N\) indicates no neural change, Temporary \(T\) signifies transient plasticity, Partial \(P\) denotes moderate synaptic reorganization persisting weeks to months, and Structural \(S\) denotes permanent neural pathway alteration — effectively rewriting brain architecture.

    #### PINS Flag

 Potential Impact to Neural Safety. Triggered when Biological Impact \(BI\) is assessed as High/Critical or Reversibility \(RV\) is Irreversible.
**39 of 161 techniques** carry this flag, indicating their potential to induce persistent, non-consensual alterations to neural function.

   NISS = Σ\(wi × Mi\) / Σ\(wi\)

   BI

 Biological Impact

 w=1.0

  CR

 Cognitive Reconnaissance

 w=0.5

  CD

 Cognitive/Functional Disruption

 w=0.5

  CV

 Consent Violation

 w=1.0

  RV

 Reversibility

 w=1.0

  NP

 Neuroplasticity

 w=1.0

  NISS scores are computed as a weighted average of all assessed metrics, normalized to a 0–10 scale. Default weights: BI=1.0, CR=0.5, CD=0.5, CV=1.0, RV=1.0, NP=1.0. CR and CD are weighted at 0.5 each to maintain backward compatibility with v1.0’s single Cognitive Integrity dimension, keeping cognitive contribution at 20% of the total score. Severity bands align with CVSS thresholds: 0.0 \(None\), 0.1–3.9 \(Low\), 4.0–6.9 \(Medium\), 7.0–8.9 \(High\), and 9.0–10.0 \(Critical\). Four context profiles \(Clinical, Research, Consumer, Military\) override these defaults for domain-specific scoring.

### CVSS vs NISS: The Scoring Gap

 94.4% of techniques have neural impacts invisible to CVSS

     CVSS v4.0 3 metrics

   C Confidentiality

 I Integrity

 A Availability

  No neural metrics

  No neural metrics

  No neural metrics

    NISS v1.1 6 metrics

   BI Biological Impact New

 CR Cognitive Reconnaissance New

 CD Cognitive/Functional Disruption New

 CV Consent Violation New

 RV Reversibility New

 NP Neuroplasticity New

  6 metrics vs 3 —
NISS captures
biological damage,
cognitive reconnaissance,
cognitive disruption,
consent violations,
reversibility, and
neuroplastic changes
that CVSS cannot express. Traditional scoring treats a brain implant breach the same as a stolen cookie.

 NISS is purpose-built for neural security — every metric addresses a dimension of harm unique to brain–computer interfaces

   Same technique, different scores

#### Signal Injection \(T-0001\)

  CVSS 4.06.5

 NISS 1.16.1

 CVSS captures integrity violation. Misses: biological tissue impact, consent violation, partial reversibility, temporary neuroplastic change.

#### Envelope Modulation \(T-0014\)

  CVSS 4.05.3

 NISS 1.18.1

 CVSS: availability impact only. NISS: critical biological impact, forced consent violation, irreversible neural pathway changes. The 2.8-point gap is the scoring blind spot.

#### EEG Eavesdropping \(T-0003\)

  CVSS 4.07.5

 NISS 1.12.7

 CVSS rates high \(confidentiality\). NISS rates lower: no biological impact, no neuroplastic change, fully reversible. Different framework, different priorities.

 CVSS scores are estimated equivalents \(for threat modeling purposes\). NISS scores from the TARA registrar. Both are proposed, unvalidated.

  **Mathematical formalization** — signal integrity equations, spectral decomposition, and coupling mechanisms — is future work pending collaboration with domain experts. This section presents the scoring system; the underlying physics constraints are documented at [BCI Physics Constraints](https://qinnovate.com/research/physics/).

  [Explore NISS Scoring →](/atlas/scoring/)

### 5.8 Beyond DSM-5-TR: Sensory and Neurological Weighting

  The current NISS scoring maps attack outcomes to DSM-5-TR diagnostic categories for threat modeling purposes. This mapping is useful but incomplete. DSM-5-TR is a psychiatric classification system. It was not designed to capture the full spectrum of neurological disruption that a BCI attack could produce.

 **Sensory modality disruption.** A BCI attack that corrupts olfactory processing — causing phantosmia, anosmia, or parosmia — has no primary DSM-5-TR diagnostic category. The same is true for vestibular disruption, somatosensory attacks, and gustatory hallucinations. These are clinically documented neurological conditions with ICD-11 codes and known neural pathway correlates. They are not psychiatric disorders.

 **Neurological disorders absent from DSM.** Conditions like tinnitus, central pain syndrome, cortical blindness, prosopagnosia, spatial neglect, and movement disorders are well-characterized in neurology. A BCI attack targeting the relevant circuits could induce or exacerbate any of them.

   NISS v2.0 Extension \(Proposed\)

| Source | What It Adds |
| --- | --- |
| **ICD-11 Ch. 8** | Tinnitus, neuropathic pain, vestibular disorders, movement disorders |
| **ICD-11 Ch. 22** | Anosmia, phantosmia, paresthesia, proprioceptive dysfunction |
| **Neurology literature** | Cortical stimulation studies documenting sensory disruption in therapeutic BCI use |

  **Note.** All ICD-11 and neurological disorder mappings are for threat modeling purposes. NISS produces severity scores corresponding to clinical outcome categories, not clinical diagnoses.

### 5.9 The Neuroplasticity Metric \(NP\)

  Traditional cybersecurity scoring assumes attacks are discrete events. Neural attacks break this assumption. The brain is a learning system. It rewires itself in response to sustained input. An attack that delivers malicious stimulation patterns over time does not just cause momentary disruption — it causes the brain to *adapt* to the malicious pattern, creating lasting neural pathway changes that persist after the attack ends.

 NP values \(expanded from 3 to 4 levels in v1.1.1\):

| Value | Score | Meaning |
| --- | --- | --- |
| **N** \(None\) | 0.0 | No lasting neural pathway changes |
| **T** \(Temporary\) | 3.3 | Temporary plasticity changes, resolve over days to weeks |
| **P** \(Partial\) | 6.7 | Partial structural changes; recovery possible with intervention |
| **S** \(Structural\) | 10.0 | Permanent or long-lasting neural pathway reorganization |

  Current severity distribution across 161 techniques: 24 structural, 6 partial, 38 temporary, 67 none. The 4-level NP scale provides finer granularity. Techniques previously scored as structural \(NP:S\) may now score as partial \(NP:P\) where recovery is possible with intervention.

 **Why NP has no traditional analogue.** A firewall breach does not make future breaches easier by physically restructuring the target network. A neural attack with NP:S does exactly that. The brain adapts through Hebbian learning, making the attack’s effects self-reinforcing. For these techniques, “turn it off” is not sufficient remediation. The damage persists after the device is removed because the damage is encoded in the biology, not the technology.

   **Note.** NP is a proposed metric within an unvalidated scoring system. The claim that specific attacks cause structural neuroplasticity is grounded in the neuroscience literature on maladaptive plasticity \(Pascual-Leone et al. 2005, Merzenich et al. 2014\) but has not been validated in the specific context of BCI attack scenarios. The mapping from attack technique to NP score is the author’s assessment, not an empirically calibrated measurement.

     ## 6. The Neural Impact Chain

  Why this matters

 When a BCI attack disrupts your amygdala, what are the potential clinical consequences? The Neural Impact Chain traces this question for every technique in the atlas — as threat modeling references, not diagnostic claims. Neuroscience does not yet fully understand how the brain produces cognition and emotion \(Morse, 2006\); these mappings reflect current knowledge and will evolve as the science matures.

  The Neural Impact Chain \(NIC\) is a six-stage mapping that traces every technique from its physical mechanism to its potential clinical outcome for threat modeling purposes. For each entry in TARA, the chain identifies the targeted hourglass band, the affected neural structure, the disrupted cognitive or motor function, the resulting NISS severity score, and the corresponding DSM-5-TR diagnostic reference. These references illustrate the potential severity of sustained attack patterns; they are not diagnostic predictions.

 To our knowledge, this represents a **systematic mapping from cybersecurity severity to clinical outcome references**. It traces a structured pathway: specific techniques, applied to specific neural bands, produce functional impacts that correspond to recognized clinical conditions. A security engineer can see that a technique targeting the limbic system \(N6\) with high cognitive integrity impact references mood and trauma-related disorders. A clinician can see that the same attack vector shares its mechanism with an FDA-approved therapy. These references must be interpreted with caution — neural correlates do not prove causation, and the brain's complexity means that identical stimulation can produce different outcomes across individuals.

 This is the bridge between cybersecurity and clinical neuroscience that we found missing from existing frameworks.

### The Neural Impact Chain

 Research mapping from security severity to psychiatric diagnostic categories

    Technique

  161 catalogued

  →

  Hourglass Band

  11 bands

  →

  Neural Structure

  Targeted anatomy

  →

  Function Impact

  Cognitive/Motor/Affective

  →

  NISS Score

  5 neural metrics

  →

  DSM-5-TR

  Diagnostic mapping

   Example Trace

 Transcranial Magnetic Stimulation \(QIF-T0042\) → N7 Neocortex → Prefrontal cortex → Executive function disruption → NISS 7.4 \(high\) → F06.7 Mild neurocognitive disorder

 Each of the 161 techniques traces a research path from exploit mechanism to diagnostic category reference

  The chain produces a diagnostic profile for each technique. 76 of 161 techniques have DSM-5-TR mappings, organized into five diagnostic clusters:

### DSM-5-TR Diagnostic Clusters

 Neural Impact Chain mapping: attack technique → psychiatric outcome

   Cognitive/Psychotic

 28

 Mood/Trauma

 24

 Motor/Neurocognitive

 22

 Non-Diagnostic

 16

 Persistent/Personality

 9

 Clinical outcome references for threat modeling — mapping BCI attack vectors to potential DSM-5-TR diagnostic patterns. Not diagnostic claims; neuroscience understanding remains incomplete.

  **Cognitive/Psychotic** \(22 techniques\) — Attacks that disrupt perception, cognition, or reality testing. Primarily driven by high Cognitive Reconnaissance \(CR\) and Cognitive/Functional Disruption \(CD\) scores, corresponding to diagnostic categories such as brief psychotic disorder, delirium, and dissociative conditions \(for threat modeling purposes\).

 **Mood/Trauma** \(27 techniques\) — Attacks that alter emotional state or violate autonomy. Driven by Consent Violation \(CV\) metrics, corresponding to categories including PTSD, acute stress disorder, and adjustment disorders.

 **Motor/Neurocognitive** \(26 techniques\) — Attacks that cause physical neural damage. Driven by Biological Impact \(BI\) scores, corresponding to neurocognitive disorder and movement condition categories.

 **Persistent/Personality** \(9 techniques\) — Attacks that induce lasting neural reorganization. Driven by Neuroplasticity \(NP\) and Reversibility \(RV\) scores, corresponding to categories such as personality change due to medical condition and persistent functional alterations.

 **Non-Diagnostic** \(51 techniques\) — Silicon-only attacks that lack a direct neural impact pathway.

  Risk classes

    75 Direct — Mechanism corresponds directly to the mapped diagnostic category

   11 Indirect — Effects manifest downstream through secondary pathways

   49 None — No identifiable diagnostic risk pathway

     ## 7. Neurorights Mapping

  From diagnosis to rights

 The Neural Impact Chain tells us what psychiatric harm a technique can cause. The neurorights mapping asks the next question: **which fundamental rights does it violate?**

  Ienca & Andorno \(2017\) proposed four neurorights: Mental Privacy, Cognitive Liberty, Mental Integrity, and Psychological Continuity. Chile enshrined them in law. The OECD published neurotechnology governance guidelines \(2019\). But to our knowledge, no published work had tested them against a systematic threat taxonomy.

 Every technique in the TARA atlas is now mapped to the affected neurorights through a systematic, multi-layer process: UI category provides the primary signal, DSM-5-TR cluster adds overlays, and NISS vector components refine the result. This mapping is deterministic and reproducible — the same technique always maps to the same rights.

 Running 161 techniques through this process confirmed all four established rights from Ienca & Andorno \(2017\). QIF operationalizes Mental Integrity with engineering-level signal dynamics specifications and Mental Privacy with data-lifecycle specifications. QIF also maps these neurorights onto the CIA triad \(MP = Confidentiality, MI = Integrity\) and demonstrates both violations via a disclosed vulnerability in a BCI-adjacent streaming library. Cross-validated against six established frameworks \(Ienca & Andorno 2017, Yuste/NeuroRights Foundation 2017, Chile Law 21.383, UNESCO 2025 Recommendation, Farahany 2023, Bublitz 2022\):

    MP Mental Privacy QIF Operationalized

 106 of 161 techniques

  CL Cognitive Liberty

 85 of 161 techniques

  MI Mental Integrity QIF Operationalized

 101 of 161 techniques

  PC Psychological Continuity

 79 of 161 techniques

  **CIA Triad Mapping:** QIF maps Ienca & Andorno's neurorights onto the CIA triad: Mental Privacy = Confidentiality \(don't *read* my neural data\), Mental Integrity = Integrity \(don't *write* into my neural signals\). A disclosed vulnerability in a BCI-adjacent streaming library demonstrates both violations in a single exploit chain: Phase 2 \(exfiltrate neural data\) = MP violation, Phase 3 \(inject false signals\) = MI violation.

 **Mental Integrity \(MI\) — QIF Operationalized:** QIF provides engineering-level specifications for Mental Integrity \(Ienca & Andorno, 2017\), including signal dynamics protections. Some attacks don't break neural function; they *retune* it. Gradual drift, neurofeedback falsification, and baseline adaptation poisoning reshape the brain's homeostatic equilibrium. QIF operationalizes MI with measurable specifications for detecting these dynamical retuning attacks. 101 techniques map to MI.

 **Mental Privacy \(MP\) — QIF Operationalized:** QIF provides engineering-level specifications for Mental Privacy \(Ienca & Andorno, 2017\), including data-lifecycle protections. Multi-modal biometric fusion attacks correlate neural data with gait, voice, and typing rhythm. QIF operationalizes MP to cover cross-modal re-identification and the right to consent to each data modality independently.

  Consent Complexity Index \(CCI\)

  CCI = \(consent\_weight × rights\_count × severity\_factor\) / 10. It quantifies whether a technique's consent process is adequate for the rights it violates. Mean CCI across 161 techniques: **0.89**. 6 techniques exceed 2.0 \(high complexity\).

 A low CCI with a high NISS score signals a consent blind spot — the consent infrastructure under-protects the neural impact. Four silicon-only attacks have CCI below 0.6 but NISS above 6.4.

### Policy-Layer Rights

 Three additional neurorights proposed by Yuste and the NeuroRights Foundation \(2017\) and reinforced by UNESCO's 2025 Recommendation — **equitable access to mental augmentation**, **protection from algorithmic bias**, and **free will** — are not mapped in the threat taxonomy. These are distributive justice and governance concerns: no attack technique directly violates “fair access,” and algorithmic bias arises from systems processing neural data, not from attacks on the interface itself. Free will substantially overlaps with Cognitive Liberty when mapping threats to harm. These rights are addressed at QIF's governance layer rather than the security layer. See [Governance → Neuroethics Alignment](https://qinnovate.com/governance/) for the full mapping.

### The Gap

 Ienca & Andorno \(2017\) proposed four neurorights. With Equitable Access \(from Yuste/NeuroRights Foundation, 2017\), QIF maps five. Philosophical frameworks define what they mean. None specify how a BCI system would actually enforce them.

   Mental Integrity: “unaltered” is not “self-originating”

 Current MI formulations protect against *modification* of neural signals — tampering, injection, disruption. But we are building systems that inject, simulate, or reshape neural signals as a core function. A perfectly intact signal that was never generated by your brain passes every integrity check and violates everything MI is supposed to protect. Deep Brain Stimulation injects synthetic signals as therapy. Sensory prostheses generate neural patterns the brain never produced. The signal arrives “unaltered” at the point of measurement because it was synthetic from the start. Governance must distinguish between “unaltered” and “self-originating.” That distinction requires engineering, not philosophy — a metric that verifies whether a signal's statistical properties match your baseline neural signature. QIF's Coherence Metric and NISS consent dimension are a first attempt at operationalizing this distinction.

  Equal Access: the gap we already know

 BCI technology is expensive, concentrated in wealthy institutions, and advancing fastest in military and consumer entertainment. The people who need it most — patients with locked-in syndrome, spinal cord injuries, treatment-resistant neurological conditions — are the last to benefit and the least represented in design decisions. This is not a future concern. It is the present reality. Equal Access is a distributive justice problem that requires the least engineering and the most political will to close. No amount of protocol design solves this without legislative and economic intervention.

  What the gap means

 QIF does not claim to close these gaps. QIF provides engineering specifications — signal verification, consent architecture, impact scoring — that make the gaps *measurable*. You cannot legislate what you cannot detect. You cannot govern what you cannot score. The philosophical rights need engineering counterparts, and the engineering needs legislative backing. Neither alone is sufficient.

     ## 8. Governance

  Each technique within the TARA atlas is assigned a consent tier reflecting the minimum regulatory oversight necessary for its deployment. These tiers are derived directly from NISS scores: higher biological impact, lower reversibility, and greater consent violation require stricter governance.

### Consent Tier Distribution

 Ethical oversight requirements across all 161 catalogued techniques

   34

 66

 52

 9

     Standard \(34\) Normal informed consent

   Enhanced \(66\) Additional safeguards required

   IRB Required \(52\) Institutional review board oversight

   Prohibited \(9\) Not permissible under any protocol

 161 techniques across
4 consent tiers

  The consent tier system aligns with existing regulatory frameworks:

- **FDA 21 CFR Part 820 / 524B** — Quality system requirements and cybersecurity expectations for medical devices
- **EU Medical Device Regulation \(MDR\) 2017/745** — Post-market surveillance and clinical evaluation requirements
- **HIPAA** — Neural signals constitute Protected Health Information \(PHI\) when linked to an individual. Raw EEG, decoded intentions, and cognitive state inferences all fall under the Security Rule and Breach Notification Rule. See the full [Regulatory Compliance Guide](https://qinnovate.com/governance/REGULATORY_COMPLIANCE/) for neural data classification
- **GDPR Article 9** — Neural data is special category data \(health data\) under EU regulation, requiring explicit consent for processing. The right to erasure poses unique challenges for neural recordings
- **ISO 14971** — Risk management for medical devices, mapped to NISS severity levels
- **IEC 62304** — Software lifecycle for medical devices, with Runemate targeting Class C certification

 These alignments are not merely aspirational. Each consent tier directly corresponds to specific regulatory obligations. An IRB-tier technique, for instance, mandates review processes equivalent to those governing invasive research protocols. A prohibited-tier technique is not merely categorized as "high risk" — it is explicitly ineligible for any clinical or research protocol under existing frameworks.

### 8.2 FDORA §3305 Compliance Mapping

  Why this matters for manufacturers

 Since October 2023, the FDA enforces a Refuse-to-Accept policy under FDORA Section 524B: premarket submissions for "cyber devices" lacking cybersecurity documentation are rejected before review begins. Every BCI is a cyber device. TARA provides the threat catalog these submissions require.

  Section 3305 of the Food and Drug Omnibus Reform Act \(FDORA, 2022\) defines a "cyber device" as one that \(1\) contains software, \(2\) can connect to the internet, and \(3\) could be vulnerable to cybersecurity threats. Every technique in TARA is classified against this three-prong test.

   68

 Target cyber devices

  0.39

 Mean regulatory coverage \(0–1\)

  74

 Techniques with major gaps \(<0.5\)

  Section 524B requires five categories of cybersecurity documentation. Each technique is mapped to the requirements it is relevant to:

| Requirement | Section 524B Mandate | Techniques |
| --- | --- | --- |
| TM | Threat modeling — identification of cybersecurity risks | 135 |
| VA | Vulnerability assessment — severity ratings for known vulnerabilities | 134 |
| SBOM | Software Bill of Materials — component transparency | 61 |
| SA | Security architecture — design controls for cybersecurity | 97 |
| PM | Post-market monitoring — ongoing vulnerability surveillance | 130 |

  The regulatory coverage score \(0.0–1.0\) measures how well *existing* standards cover each technique. A score of 0.8 means current FDA pathways, IEC standards, and privacy regulations adequately address the risk. A score below 0.5 indicates a **major regulatory gap** — the technique represents a neural-specific threat that pre-FDORA frameworks were not designed to handle. 74 of 161 techniques fall below this threshold.

 The top gaps are structural, not incidental: **CVSS cannot express neural-specific impacts** for the majority of techniques, and **no FDA pathway exists** for consumer sensor exploitation in the S-domain. These are precisely the gaps that TARA and NISS were built to fill — providing the neural threat catalog and impact scoring that Section 524B mandates but existing standards do not supply.

     ### 8.3 AI Ethics: The Regulatory Environment

  BCIs that use AI for stimulation decisions, signal decoding, or adaptive learning are subject to emerging regulation that spans AI ethics, medical device law, and neurotechnology governance. This section maps the frameworks that will define the legal environment QIF operates within.

### Regulatory Convergence Timeline

 The window for proactive architecture is closing. Regulation is arriving from three directions simultaneously.

    Law / Regulation

  Policy / Guideline

  Technical Standard

      2019

 OECD Neurotech Guidelines

  2021

 Chile Neurorights Law

  2023

 FDA FDORA 524B

  2024

 EU AI Act Entry

  2024

 CoE AI Convention

  2025

 UNESCO Neuroethics

  2025

 NIST IR 8547 \(Draft\)

  2026

 EU AI Act Enforcement

  2030

 NIST PQC Deprecation

  2035

 NIST PQC Disallowance

 A BCI implanted today must comply with regulations that do not yet exist. Post-quantum cryptography, neurorights legislation, and AI governance are converging on a single timeline. Designing for compliance now is cheaper than retrofitting later.

#### NIST AI RMF 1.0

 January 2023 · US Federal · Voluntary

 Four core functions: GOVERN, MAP, MEASURE, MANAGE. Seven properties of trustworthy AI. Increasingly referenced as compliance safe harbor.

#### UNESCO AI Ethics

 November 2021 · 194 member states · Voluntary

 First global normative instrument on AI ethics. 10 core principles, 11 policy areas. Universal adoption but no enforcement mechanism.

#### UNESCO Neurotechnology Ethics

 November 12, 2025 · Global · Voluntary

 Directly addresses devices that read and write neural data. The closest international instrument to what QIF proposes at the technical level.

#### EU AI Act

 August 2024 · EU · **Binding**

 First comprehensive AI law. Risk tiers: Unacceptable \(banned\), High \(conformity assessment\), Limited \(transparency\), Minimal. Neural interfaces with AI likely classified as high-risk. Penalties up to 7% of global revenue.

#### Council of Europe Convention

 Opened for signature September 5, 2024 · EU \+ additional countries · **Binding treaty**

 First legally binding international AI treaty. Requires human rights safeguards, procedural transparency, discrimination prevention, and remedy for affected persons.

#### FDA SaMD / PCCP

 Ongoing · US · **Binding**

 Predetermined Change Control Plan: AI medical devices can adapt within pre-specified guardrails without new regulatory submissions. Directly applicable to adaptive BCIs.

  **Why this matters for architecture:** Policy says “AI should be transparent.” The question is whether a technical framework can operationalize that as an architectural constraint — not a suggestion, but a requirement enforced by the system itself. QIF proposes that it can, through mandatory audit logging, amplitude bounds, and consent gates. Whether this approach is sufficient is an open question requiring independent validation.

  [Read the Full AI Ethics Reference →](/governance/ai-ethics/)

     ## 9. NSP Protocol

  Why post-quantum cryptography is non-negotiable for neural devices

 Neural data cannot be reset like a password. A brainwave recording taken today will identify you in twenty years. Adversaries know this — a strategy called **Harvest Now, Decrypt Later** \(HNDL\) involves recording encrypted traffic today and waiting for quantum computers to break the encryption retroactively. For implants with multi-year to multi-decade operational lifetimes \(varying by type: 1–5 years for intracortical arrays, 10–20 years for DBS leads, 25\+ years for cochlear implants\), data encrypted with today’s standard algorithms may be decryptable well within the device’s service life.

 This is not theoretical. NIST has [mandated](https://csrc.nist.gov/pubs/ir/8547/ipd) that all legacy encryption algorithms \(RSA, ECDSA, Diffie-Hellman\) be deprecated by 2030 and fully disallowed by 2035. NSP is designed from the ground up with their quantum-resistant replacements — so neural data encrypted today remains protected for the lifetime of the patient, not just the lifetime of the algorithm.

  The gap NSP fills

 Post-quantum cryptography is production-ready for web traffic — OpenSSL 3.5, BoringSSL, and wolfSSL all ship ML-KEM today, and as of late 2025, over 50% of connections through Cloudflare use hybrid post-quantum key agreement \(per Cloudflare Radar Year in Review\). But **none of this reaches the BCI data link.** Bluetooth Low Energy, the only practical wireless transport for implanted devices, uses ECDH on the P-256 curve for key exchange — an algorithm that Shor’s algorithm breaks outright. The Bluetooth specification \(through 5.4\) offers **no post-quantum upgrade path**.

 The device market confirms the urgency. To our knowledge, no BCI manufacturer, Neuralink, Synchron, Blackrock Neurotech, OpenBCI, or Emotiv, has published an independent security audit or a full wireless security specification. Emotiv’s AES-128-ECB encryption was [disclosed as using broken ECB mode in 2013](https://www.cryptofails.com/post/70333773685/broadcast-your-brain-fixed-key-ecb-mode). OpenBCI’s protocol documentation contains zero mentions of encryption. A 2021 ACM Computing Surveys review concluded that “from the security perspective, BCIs are in an early and immature stage” \([Bernal et al.](https://dl.acm.org/doi/10.1145/3427376)\).

 Meanwhile, NIST’s IR 8547 transition timeline mandates deprecation by 2030 and disallowance by 2035 — but provides **no device-specific migration guidance** for BLE, IoT, or medical devices. No existing standard tells a BCI manufacturer how to migrate from ECDH to ML-KEM on a 40 mW power budget.

 Beyond cryptography, no existing protocol performs **physics-based signal validation** \(verifying neural signals match expected brain activity patterns\) or **per-user adaptive anomaly detection** \(learning each patient’s unique neural baseline to catch slow-drift attacks\). Both remain research-stage concepts with no deployed implementations. NSP addresses all three gaps — PQC at I0, signal integrity, and adaptive detection — as a single protocol designed for constrained neural hardware.

  The Neural Sensory Protocol \(NSP\) is a proposed post-quantum security protocol specifically designed for BCI data links. It protects every neural data frame using ML-KEM key exchange \(NIST’s quantum-resistant replacement for classical key exchange, standardized as FIPS 203\), ML-DSA digital signatures \(the quantum-resistant replacement for RSA and ECDSA signing, FIPS 204\), and AES-256-GCM authenticated encryption \(which both encrypts data and cryptographically verifies it has not been tampered with in transit\). Power modeling against the Neuralink N1 reference platform estimates an overhead of **approximately 3–4%** of a 40 mW implant budget \(AI-derived estimate, hardware validation pending\).

 NSP defines five independent defense layers. Each layer operates independently — failure of one does not compromise the others:

    L1 #### Hardware Root of Trust

 Firmware integrity and secure boot chain. Ensures the device is running authentic, untampered software from the moment it powers on. Uses SPHINCS\+ hash-based signatures \(FIPS 205\) for firmware attestation, chosen because hash-based cryptography has no known quantum attack vector.

   L2 #### PQC Key Exchange

 Hybrid post-quantum key exchange, frame encryption, and mutual authentication. Combines classical ECDH with ML-KEM so that even if one algorithm is broken, the other still protects the session. All frame data is encrypted with AES-256-GCM. This is the layer that defeats Harvest Now, Decrypt Later.

   L3 #### QI Signal Integrity

 Physics-based signal validation at the electrode-tissue boundary. Uses STFT \(Short-Time Fourier Transform\) spectral analysis to decompose neural signals into their frequency components over time. Injected signals that violate the expected scale-frequency relationship \(L = v/f\) are flagged, catching attacks that cryptography alone cannot detect.

   L4 #### Adaptive TTT

 Per-user anomaly detection using Test-Time Training — a machine learning technique that continuously adapts to each patient’s unique neural baseline. Detects slow-drift attacks and gradual signal poisoning that would pass static threshold checks. What looks normal for one brain may be anomalous for another. Detection thresholds are tuned conservatively to prioritize patient safety; clinical deployment protocols must define acceptable false positive rates for each device class.

   L5 #### EM Environment

 Electromagnetic interference detection and spectral scanning. Monitors the RF environment around the device for anomalous emissions that could indicate active signal injection or intermodulation attacks, where external electromagnetic fields interact with the implant’s own circuitry to produce unintended signals.

  The protocol is specified across three device tiers: implanted \(most constrained, ≤40 mW\), wearable \(moderate power budget\), and external \(unconstrained\). Not all tiers require all layers. Consumer wearables implement Layers 1–3, while implanted devices implement all five. Each tier uses the same cryptographic primitives but with different parameter sets and duty cycles.

 Post-quantum key sizes represent the primary implementation challenge. ML-KEM-768 public keys are 1,184 bytes, 18 times larger than classical X25519 keys \(the standard used in most encrypted connections today\). [Runemate](https://qinnovate.com/guardrails/runemate/), a purpose-built compression layer for BCI payloads, mitigates this by encoding neural interface content \(visual, auditory, haptic\) through a closed-vocabulary DSL, achieving 65–90% compression and net bandwidth savings over classical transport for typical BCI content exceeding 23 KB.

 **Scope:** NSP secures the I0 data link, the wireless boundary between implant and external device. It does not address physical-layer failures such as electrode migration, chronic immune response, or biocompatibility degradation. These are clinical monitoring concerns outside the protocol’s threat model.

  [Read the Full NSP Specification →](/guardrails/nsp/)

     ## 10. The Neural Terminal

### 10.1 Why Not a Browser

  Web browsers are rendering engines built for screens. They parse HTML into a Document Object Model \(DOM\), execute JavaScript in a sandboxed runtime, apply CSS stylesheets through a cascade algorithm, composite visual layers, and rasterize the result onto a pixel grid. This pipeline — which evolved from Tim Berners-Lee’s original WorldWideWeb \(1990\) through Mosaic, Netscape, and the modern Chromium/WebKit duopoly — assumes a rectangular display with fixed pixel density, a pointing device, and a keyboard.

 None of these assumptions hold for a cortical visual prosthesis.

 A cortical implant drives an electrode array on the surface of the primary visual cortex \(V1\). The “pixels” are phosphenes — perceived spots of light induced by electrical stimulation of cortical tissue. Their arrangement is not a rectangular grid but a retinotopic map that varies between individuals based on cortical folding patterns. The “rendering engine” cannot be a browser because there is no DOM to parse, no CSS to cascade, no pixel grid to rasterize onto. The content must be compiled directly into electrode-addressable stimulation patterns — a fundamentally different pipeline.

 Beyond architectural mismatch, browsers carry an attack surface that is unnecessary and dangerous for neural devices:

| Attack Surface | Browser Risk | Neural Consequence |
| --- | --- | --- |
| JavaScript engine \(V8/SpiderMonkey\) | Memory corruption, type confusion, JIT spray | Arbitrary code execution on a device connected to neural tissue |
| DOM parsing | XSS, DOM clobbering, mutation XSS | Injected content could manipulate stimulation patterns |
| Extension model | Malicious extensions, permission escalation | Third-party code with access to neural data streams |
| Network stack | MITM, certificate spoofing, DNS poisoning | Compromised content delivered directly to the brain |
| Compositor | Screen capture, overlay attacks | Irrelevant — no screen exists |
| Cookie/storage | Tracking, fingerprinting, session hijacking | Neural usage patterns as surveillance data |

  Each layer of the browser stack represents a class of vulnerabilities accumulated over three decades of web development. These vulnerabilities exist because browsers must execute arbitrary code from arbitrary sources, a requirement that is antithetical to the security needs of an implanted medical device.

 Runemate eliminates the browser entirely. Content is compiled from a declarative, non-Turing-complete DSL \(Staves\) into compact bytecode, validated against TARA safety bounds at compile time, encrypted via NSP, and delivered directly to the on-device interpreter \(Scribe\). There is no arbitrary code execution. There is no third-party extension model. There is no DOM.

### 10.2 Why Not an App Store

  App stores introduce three categories of risk that are unacceptable for neural devices:

     Centralized control

 A patient’s perceptual experience would be subject to a platform’s content policies, review timelines, and commercial decisions. If the app store operator decides to remove a perceptual application, the patient loses a component of their sensory experience. This is qualitatively different from losing access to a mobile app. It is the digital equivalent of confiscating a prosthetic limb.

    Forced updates

 App stores routinely push updates that users cannot decline. For a neural device, an untested update to a stimulation pattern could alter a patient’s visual field, auditory processing, or haptic sensation without their informed consent. The patient must have the ability to inspect, approve, and roll back every change to the software that drives their sensory experience.

    Additional attack surface

 The app store itself is a target. Supply chain attacks — where malicious code is injected into a legitimate application during the distribution pipeline — have compromised npm, PyPI, and the Chrome Web Store. An app store for neural content adds a distribution layer that does not need to exist. If the content is compiled locally or on a trusted gateway, and delivered via an authenticated protocol \(NSP\), the distribution problem is solved without introducing a third-party intermediary.

### 10.3 The Terminal as Interface

  The terminal is the proposed primary interface for neural devices. It provides:

     Direct parameter access

 Stimulation parameters \(contrast, brightness, refresh rate, spatial resolution, electrode mapping\) are exposed as named configuration values, not hidden behind a graphical settings menu designed for a display the patient may not have.

    Scriptability

 Patients can automate perceptual adjustments, create macros for common tasks, and build personal workflows. A patient who prefers spatial audio cues for navigation can script that behavior once and invoke it with a single command.

    Auditability

 Every packet entering the nervous system is logged and inspectable. `runemate log --stream` provides real-time visibility into what content is being delivered and what stimulation patterns are being generated, the neural equivalent of `tcpdump`.

    Offline operation

 `runemate --offline` ensures the device functions without a network connection, without a cloud service, and without phoning home. The terminal makes this verifiable. The patient can confirm that no outbound connections are active.

    Troubleshooting

 When something goes wrong — a rendering artifact, a calibration drift, an unexpected stimulation pattern — the patient has the tools to investigate. They are not dependent on a manufacturer’s support queue to diagnose a problem with their own sensory system.

### 10.4 Autodidactic Navigation

  Traditional interfaces impose a navigation paradigm: menus, scroll, tap, swipe. These paradigms were designed for fingers on glass. They do not translate to a cortical interface where input may arrive via motor cortex BCI, subvocalization, or eye tracking.

 The terminal provides primitives — commands, pipes, scripts — and lets the patient compose their own navigation model. One patient might prefer spatial audio landmarks. Another might use haptic pulses as navigation anchors. A third might develop a completely novel interaction pattern that no UX designer anticipated.

 This is not a design limitation. It is a design principle. The terminal does not force someone new to the system to learn a prescribed way of navigating. Instead, it adapts — autodidactically — to how the user thinks and moves. The user teaches the system, not the other way around.

 The same philosophy made Linux the foundation of every server, every supercomputer, and every Android phone: give people the tools, and they build what they need.

     ## 11. Patient Self-Sovereignty

### 11.1 The Four Rights

  When a device IS the patient’s sensory system, the conventional user-vendor relationship is inadequate. The patient is not a “user” in the consumer technology sense. They are a person whose perception depends on the correct, continuous, and trustworthy operation of an implanted system. This relationship demands four operational rights:

     Right to repair

 When a cortical implant is the patient’s visual system, they cannot wait for a manufacturer’s scheduled update to fix a rendering artifact in their field of vision. A terminal lets them adjust stimulation parameters, recalibrate electrode mappings, and verify that firmware updates have not altered their perceptual baseline.

    Right to inspect

 Every packet entering the patient’s nervous system should be auditable. The patient must be able to examine what content is being delivered, what patterns are being generated, and what safety bounds are active. Opacity is not acceptable for a device that directly interfaces with neural tissue.

    Right to customize

 Sighted users choose dark mode, font sizes, and color schemes. A patient with a cortical prosthesis should be able to adjust contrast curves, phosphene brightness, temporal refresh rates, and spatial resolution, not through a settings menu designed by someone who can see, but through direct parameter control that reflects the patient’s subjective perceptual experience.

    Right to disconnect

 The device must function without a network connection, without a cloud service, and without phoning home. An implanted medical device that requires continuous internet connectivity to operate is a device that can be remotely disabled by a network outage, a server decommission, or a corporate bankruptcy. The terminal makes disconnected operation verifiable.

### 11.2 Subvocalization and Intent

   In a proposed neural OS, the patient controls AI through subvocalization, thinking commands rather than typing them. Subvocalization BCI is an experimental prototype \(e.g., MIT AlterEgo\) that captures intended speech or motor commands before they reach the muscles, enabling silent, private interaction with the system.

 The AI is the tool. It processes, suggests, retrieves, compiles, renders. But the decision to act, the consent to a thought becoming an action, the creative impulse that initiates a query or dismisses a suggestion — that is the human. That is what the terminal architecture protects.

 Without this boundary, AI does not augment human capability. It replaces it. The patient becomes a passenger in their own perceptual system, receiving whatever the algorithm decides to deliver, with no mechanism to inspect, reject, or redirect.

 The distinction is operational:

     A tool

 “Show me what’s on this webpage.” Patient initiates. AI compiles. Runemate delivers. Every interaction begins with patient intent. Every delivery requires patient consent.

    A feed

 Content streams continuously, selected by an algorithm, with no patient-initiated gate. The user receives. The user does not choose.

  The terminal ensures the first model. The absence of a terminal enables the second.

### 11.3 The Steering Argument

  If we do not have free will through consent and agency, then who is driving the car if we are not steering?

 This is not a philosophical abstraction. It is a design constraint. A neural interface that delivers content without patient-initiated consent is a system where the patient is cargo, not the driver. The difference between a tool and a cage is whether the person holding it chose to pick it up.

 Neural interfaces must be steering wheels, not conveyor belts. The terminal is the steering column — the mechanical linkage between the patient’s intent and the system’s behavior. Remove it, and the patient is along for the ride.

### 11.4 Protecting Creativity

  Creativity requires agency — the ability to combine ideas in unexpected ways, to follow a thought that no algorithm would predict, to say “no, show me something else.” If the AI drives and the patient rides, creativity does not diminish — it atrophies. Not because AI cannot generate, but because the human loses the practice of choosing. And a capacity that is not exercised degrades.

 This is particularly acute for neural interfaces because the input channel \(motor cortex, subvocalization\) is also a neural pathway. If the AI is both reading the patient’s intent and generating the patient’s experience, the boundary between “what I thought” and “what the system suggested” becomes ambiguous. The terminal provides a clean separation: the patient composes commands, the system executes them. Intent flows in one direction. Content flows in the other. The boundaries are explicit.

 Neurorights \(MP, CL, MI, PC, EA\) are the formal expression of this principle. But the terminal is what makes them enforceable. Without a CLI, neurorights are policy. With a CLI, they are access control.

     ## 12. Autonomy Guardrails

### 12.1 The Autonomy Spectrum

  Assistive autonomy exists on a spectrum. The automotive industry has standardized this spectrum \(SAE J3016\), and the mapping to neural interfaces is instructive:

| Level | Automotive | Neural Equivalent | Control Model |
| --- | --- | --- | --- |
| 0 | No automation | Raw BCI, no correction | Patient 100% |
| 1 | Driver assistance | Gait correction for nerve damage | Patient steers, system nudges |
| 2 | Partial automation | Active motor pattern stabilization | System steers, patient can override |
| 3 | Conditional automation | AI manages routine motor function | System steers, patient supervises |
| 4 | High automation | AI manages cognitive support functions | System operates within bounded domain |
| 5 | Full automation | AI modifies thought/behavior patterns autonomously | System drives, patient is cargo |

  Levels 1–2 are clearly therapeutic. Level 5 is clearly a violation of cognitive liberty. The design challenge — and the ethical battleground — is Levels 3–4: systems that operate autonomously within a bounded domain, with the patient in a supervisory role.

 Lane-keep assist is Level 1. The system nudges; the driver can override instantly. Lane-keep control is Level 2. The system actively steers; the driver must exert force to override. For a nerve-damage patient whose BCI corrects their gait, Level 2 is appropriate. The system compensates for damaged motor pathways, and the patient retains the ability to override \(e.g., to stop, turn, sit down\).

 The question is: what happens when the same architecture is applied to cognitive function?

### 12.2 The Escalation Problem

  Consider a patient with spinal nerve damage who receives a BCI for motor restoration. The following escalation is medically plausible:

     Step 1: Walk assistance

  Motor cortex \(M1\) stimulation corrects gait instability. M1 is one target in multi-site approaches; primary clinical targets for gait include STN \(deep brain stimulation\) and spinal cord stimulation. This is Level 2 autonomy — the system compensates for damaged nerve pathways. The consent is specific: “help me walk in a straight line.” The outcome is measurable: gait symmetry, step consistency, fall prevention. The neural territory is motor cortex.

    Step 2: Quit prescribed painkillers

  The patient was prescribed opioids after the accident that caused their nerve damage. They want to stop. Peripheral neurostimulation for withdrawal has been demonstrated \(e.g., BRIDGE auricular device\). Cortical BCI-mediated withdrawal management remains theoretical. This request crosses from motor cortex to limbic/prefrontal circuits — from muscle control to emotion regulation. The neuron is still a neuron, but the territory changed. The system that corrected a gait is now being asked to modulate a craving.

    Step 3: Quit alcohol

 The patient developed an alcohol dependency during recovery. They ask the BCI to help. This is still therapeutic, but the system is now modifying behavioral patterns, not motor patterns. The BCI has become a governor for decision-making, a fundamentally different function than the walking assistance it was originally consented for.

    Step 4: Run faster than the body allows

  The patient, now mobile and sober, asks the BCI to enhance their running performance by overriding central fatigue signals in motor cortex. This crosses from therapeutic to enhancement. Central fatigue modulation \(suppressing the brain’s protective fatigue signaling\) could mask injury risk. The musculoskeletal system has not been augmented alongside the neural interface.

  Each step is individually reasonable. A clinician could justify each one. Together, they are a ramp from assistive tool to autonomous controller. And the patient initiated every step.

### 12.3 Ghost in the Shell

  The title references Masamune Shirow’s 1989 manga \(and Mamoru Oshii’s 1995 film\), which posed the question directly: if a human consciousness \(the “ghost”\) runs on a cybernetic body \(the “shell”\), and the shell has rules the ghost cannot override, is the ghost free?

 This is not science fiction when applied to neural interfaces. If the kernel \(Neurowall\) has immutable safety rules that the patient cannot override, then the patient’s consciousness operates within constraints set by the system’s designers. The manufacturer, the regulator, the clinician: some combination of these entities decided what the patient is and is not allowed to do with their own neural device.

 The resolution proposed here is: **the kernel protects the hardware, not the software.**

 A seatbelt does not control where you drive. It prevents the physics of a crash from killing you. The immutable kernel layer works the same way:

      Amplitude ceiling

 The electrical current delivered to neural tissue cannot exceed the tissue damage threshold. This is a physics constraint. Exceeding it destroys neurons. The limit is not a policy choice; it is a material property of cortical tissue.

    Rate limiting

 Stimulation pulses cannot fire faster than the neural refractory period allows. This is a biological constraint. Neurons that have not recovered from the previous pulse cannot respond to the next one. Exceeding this rate does not produce stronger stimulation; it produces tissue damage.

    Thermal bounds

  The electrode array cannot heat beyond the safe operating temperature of brain tissue. Thermal damage thresholds for neural tissue are approximately 39–41°C depending on exposure duration \(cumulative equivalent minutes at 43°C model\). This is a thermodynamic constraint — exceeding it causes protein denaturation and cell death. Separately, Shannon \(1992\) established electrical charge density safety limits \(k=1.85\) for stimulation-induced tissue damage — a distinct mechanism from thermal injury.

  These are not cognitive restrictions. They do not say “you cannot think that.” They say “the signal cannot physically exceed what your tissue can survive.” The ghost is free. The shell has material limits.

  But the escalation scenario in Section 12.2 breaks this clean separation. When the patient asks to quit alcohol, the relevant “tissue” is the reward circuit. The “safe amplitude” for modifying dopaminergic pathways in the ventral tegmental area \(VTA\) or nucleus accumbens \(NAc\) is not a settled question — it is an active area of neuroscience research with conflicting results across studies. No standardized safe parameters have been established by regulatory bodies; published parameters are from experimental studies and require subject-specific calibration. And “run faster than body allows” puts the motor cortex in conflict with the musculoskeletal system, which has its own damage thresholds that the neural kernel cannot measure.

### 12.4 The Five-Tier Guardrail Model

  The proposed resolution is a five-tier guardrail model that separates immutable physical safety from configurable therapeutic and policy decisions:

| Tier | Domain | Immutable? | Authority |
| --- | --- | --- | --- |
| 1. Hardware safety | Amplitude, rate, thermal limits | Yes — kernel \(Neurowall\) | Physics and biology. Not negotiable. |
| 2. Biological safety | Tissue damage thresholds, seizure thresholds, inflammation markers | Yes — kernel \(Neurowall\) | Clinical evidence, periodically updated. Requires clinician \+ patient co-signature. |
| 3. Therapeutic bounds | Stimulation dosage, session duration, target neural region, success criteria, exit conditions | No — configurable | Clinician sets defaults within evidence-based ranges. Patient can adjust within the clinician-defined range. |
| 4. Behavioral scope | Which neural domains the BCI is authorized to influence \(motor, limbic, prefrontal, sensory\) | No — consent-gated | Patient decides. Each domain requires separate, explicit informed consent. Consent is revocable. |
| 5. Enhancement limits | Applications beyond therapeutic need \(performance enhancement, cognitive augmentation, sensory expansion\) | No — policy layer | Patient \+ clinician \+ regulatory framework. No consensus exists. This tier will evolve with law, ethics, and technology. |

  The kernel \(Neurowall\) enforces Tiers 1–2. These limits cannot be overridden by the patient, the clinician, the manufacturer, or a software update. They are derived from the physical and biological properties of neural tissue.

 Tiers 3–5 live in the capability system, where consent is explicit, domain-scoped, time-bounded, and revocable. The patient can expand their BCI’s scope, but only through a deliberate, auditable consent process, never through scope creep.

### 12.5 Operationalized: The Addiction Scenario

  Applying the five-tier model to the escalation scenario in Section 12.2:

 The patient’s walk-assist BCI was consented under Tier 4 for motor cortex \(M1\) only. When they say “help me quit painkillers”:

   1. Domain recognition

 The system identifies that the request targets limbic/prefrontal circuits, outside the consented motor scope. The capability `modify.limbic` is not in the patient’s current session.

  1. Consent gate

 The system presents a Tier 4 consent request. The patient must explicitly authorize the new domain. The clinician must co-sign, establishing evidence-based therapeutic bounds \(Tier 3\): stimulation parameters, session duration, success criteria, and exit conditions.

  1. Separate capability grant

 The new consent creates a separate, time-bounded capability: `modify.limbic [duration: 90d] [bounds: clinician-defined] [exit: criteria-met OR patient-revoked]`. This capability is independent of the motor cortex consent and can be revoked without affecting walking assistance.

  1. Audit trail

 Every consent decision, parameter change, and stimulation event is logged. The patient’s future self, their clinician, their advocate, or a regulatory auditor can review the complete history.

  When the patient then says “help me run faster than my body allows”:

   1. Kernel enforcement \(Tier 1\)

 The requested stimulation pattern would suppress central fatigue signaling beyond safe thresholds, masking the body’s protective signals. The Neurowall kernel rejects the command, not because a policy prohibits enhancement, but because overriding fatigue protection creates unacceptable injury risk.

  1. Tier 5 flag

 Separately, the system flags this as an enhancement request \(Tier 5\), noting that no regulatory framework currently governs BCI-mediated performance enhancement. The patient is informed; the decision is logged; the request is denied on Tier 1 grounds regardless of Tier 5 status.

  The patient’s cognitive liberty is preserved — they can ask anything. The system’s response is determined by the tier hierarchy: physics first, biology second, therapeutics third, consent fourth, policy fifth.

### 12.6 Motor vs. Cognitive Neurons

  The escalation problem raises a fundamental question: if we allow assistive control over motor neurons \(gait correction\), how do we prevent the same architecture from being applied to cognitive neurons \(thought modification\)?

 The honest answer is: we cannot prevent it architecturally. A neuron is a neuron. The Hodgkin-Huxley model \(1952\) describes the same ion channel dynamics in motor cortex and prefrontal cortex. An electrode that can stimulate M1 to correct a gait can, with different parameters and different placement, stimulate dorsolateral prefrontal cortex \(DLPFC\) to modify executive function.

 The constraint must be organizational, not physical:

     Tier 4 \(Behavioral Scope\)

 Requires separate consent for each neural domain. Motor consent does not grant limbic access. The patient cannot accidentally authorize cognitive modification by consenting to motor assistance.

    Tier 3 \(Therapeutic Bounds\)

 Ensures that even within a consented domain, the stimulation is bounded by clinical evidence. A clinician cannot authorize parameters outside the evidence-based range.

    Tier 2 \(Biological Safety\)

 Ensures that regardless of consent or clinical authorization, the stimulation cannot exceed tissue-safe thresholds. This protects the patient from errors, not from malice.

  The distinction between motor and cognitive neurons is not architectural — it is procedural. The five-tier model enforces that distinction through consent gates, not through hardware limitations. This is an honest acknowledgment that the technology capable of restoring movement is the same technology capable of modifying thought. The guardrails must be as strong as the capability they constrain.

   Epistemic note

 The five-tier guardrail model is a proposed framework within QIF. The specific thresholds for Tiers 1–3 are subjects of active neuroscience research and clinical debate — particularly for limbic and prefrontal stimulation, where safe parameters are not established. No clinical validation of this model has been performed. The operational neurorights \(Tier 5\) reference Yuste et al. \(2017\) and Ienca & Andorno \(2017\), whose proposals are under active academic and legal debate. This model is a starting point for the conversation, not a settled standard.

     ## 13. Passwordless Security Architecture

### 13.1 Why Passwords Fail for Neural Devices

  Passwords assume a user who can type, a device with a keyboard, and a transmission channel that can be secured. None of these assumptions hold for implanted neural devices:

     The patient may lack the motor function to type \(the device may have been implanted because of motor impairment\).

    The device has no keyboard and no screen for password entry.

    A password transmitted wirelessly to an implanted chip is a password that can be intercepted, replayed, or brute-forced.

    Password reset requires a recovery mechanism. For an implanted device, “account lockout” could mean losing sensory function.

  The security architecture must be passwordless by design, not as a convenience feature, but as a medical necessity.

### 13.2 Factor 1: Post-Quantum Key Cryptography

  The NSP handshake establishes a session using ML-KEM-768 \(NIST FIPS 203, finalized August 2024\) for key encapsulation and ML-DSA-65 \(NIST FIPS 204, finalized August 2024\) for digital signatures. The device’s identity is a hardware-bound keypair provisioned at implantation and stored in a secure enclave on the implanted processor.

```
Patient Device ---- ML-KEM-768 encapsulation ----> Gateway
     |                                                |
     '---- ML-DSA-65 signature ---------------------->|
           (hardware-bound keypair,                   |
            provisioned at implantation)              |
                                                      |
     <---- Encrypted session key ---------------------'
           (AES-256-GCM-SIV, key-committed)
```

  There is no password to remember, no token to carry, and no credential to phish. The device proves its identity through a cryptographic challenge-response that requires possession of the hardware key, which cannot be extracted from the secure enclave without physical access to the implanted chip.

  Post-quantum algorithms are specified because implant operational lifetimes vary by type: cochlear implants are designed for lifetime use \(25\+ year track records\), DBS leads last 10–20 years, but intracortical microelectrode arrays \(e.g., Utah arrays\) degrade within 1–5 years due to gliosis. Even the shorter-lived devices exceed the projected timeline for cryptographically relevant quantum computers. A device implanted today must be secure against threats that emerge in 2036–2046.

### 13.3 Factor 2: Biomarker MFA

   The second authentication factor is the patient themselves. Neural biomarkers, unique patterns in electrophysiological signals, are as individual as fingerprints and as difficult to forge. Short-term stability \(30-day retest\) has been demonstrated in lab settings. Long-term stability across months, emotional states, and aging remains an open research question.

| Biomarker | Signal Characteristics | Stability | Spoofing Resistance |
| --- | --- | --- | --- |
| Resting-state EEG signature | Alpha rhythm \(8–13 Hz\) spectral profile, individually unique peak frequency and amplitude distribution | Stable across sessions over months–years \(Näpflin et al., 2007\) | Requires real-time generation of patient-specific spectral patterns |
| Evoked potentials | P300 latency/amplitude, N170 face-selective response, SSVEP frequency response | Stimulus-locked, consistent within individual | Requires knowledge of patient’s specific response to specific stimuli |
| Motor cortex signature | Movement-related cortical potential \(MRCP\) patterns during intended movement | Consistent within individual, adapts with training | Behavioral biometric, continuous, difficult to replicate passively |
| Cross-channel coherence profile | Phase synchrony patterns across electrode channels at rest | Structural, determined by individual cortical connectivity | Tied to physical connectome, cannot be replicated without patient’s brain |

  This is not a login ceremony. It is continuous, passive verification that the person using the device is the person it was calibrated for. The biomarker check runs continuously in the background, consuming minimal additional processing because the neural signals are already being read for the device’s primary function.

 If biomarker drift exceeds the patient’s baseline envelope \(as established during calibration\), the device can:

     Soft lock

 Restrict access to sensitive operations \(parameter changes, firmware updates, data export\) while maintaining basic perceptual function.

    Alert

 Notify the patient and/or clinician of the discrepancy.

    Audit

 Log the event for later review.

  The device does not shut down. A biomarker anomaly might indicate a medical event \(seizure, medication change, fatigue\), not a security threat. The response is proportional: restrict sensitive operations, maintain basic function, alert and log.

### 13.4 Continuous Authentication

  Traditional authentication is a gate: prove your identity once, then operate freely until the session expires. For a neural device, this model is insufficient. The device should continuously verify that the person using it is the person it was calibrated for, not through repeated login prompts, but through passive biometric monitoring that is already occurring as part of the device’s normal operation.

 The continuous authentication model:

    1. Session establishment

 PQKC handshake \+ initial biomarker verification. This is the “login” — but it happens automatically when the device powers on and detects the patient’s neural signature.

  1. Continuous verification

 Biomarker coherence is checked against the patient’s baseline envelope at regular intervals \(proposed: every 30 seconds — a proposed design parameter, not an evidence-based interval\). No patient action required.

  1. Graceful degradation

 If verification fails, the device does not shut down. It restricts capabilities proportional to the confidence deficit. Basic perceptual function continues.

  1. Re-verification

 If the patient returns to baseline \(e.g., after waking from anesthesia, recovering from a seizure\), full capabilities are automatically restored. No manual re-authentication needed.

### 13.5 Capability-Based Access Control

  The terminal does not grant root. It uses capability-based security \(Dennis & Van Horn, 1966\), where each session, script, and command has explicitly declared capabilities:

   Patient session — full perceptual control, no firmware access

```
capabilities: [perceive.visual, perceive.auditory, perceive.haptic,
               config.contrast, config.refresh, config.spatial,
               log.read, device.status]
```

  Clinician session — calibration access, audit trail

```
capabilities: [calibrate.electrodes, calibrate.thresholds,
               log.read, log.export, device.diagnostics]
```

  Firmware update — one-time, cryptographically signed

```
capabilities: [firmware.apply]
requires: [device.owner.approval, manufacturer.signature]
```

  No command can exceed its declared capabilities. Capability escalation requires multi-party cryptographic consent, not a password prompt, not a sudo command, but a signed authorization from the required parties \(patient, clinician, manufacturer, depending on the operation\).

### 13.6 Neurorights as ACL Flags

  The five proposed neurorights \(Yuste et al., 2017; Ienca & Andorno, 2017\) map to access control flags enforced at the protocol level:

| Neuroright | ACL Flag Namespace | Operational Definition |
| --- | --- | --- |
| Mental Privacy \(MP\) | `privacy.*` | Controls whether neural data can be read, recorded, exported, or shared. Default: deny all except device-local processing. |
| Cognitive Liberty \(CL\) | `liberty.*` | Controls whether stimulation patterns can be externally imposed without patient initiation. Default: deny — all stimulation requires patient intent. |
| Mental Integrity \(MI\) | `integrity.*` | Controls whether device parameters can be modified without explicit patient consent. Default: deny — parameter changes require patient confirmation. |
| Psychological Continuity \(PC\) | `continuity.*` | Controls whether changes can alter the patient’s baseline perceptual experience beyond a defined threshold. Default: warn and require consent for changes exceeding 10% of baseline. |
| Equal Access \(EA\) | `access.*` | Controls whether content or capabilities can be restricted by a content provider, manufacturer, or third party. Default: deny — the patient determines what content they access. |

  These are not philosophical concepts in this architecture. They are ACL flags enforced at the Neurowall kernel level. A content provider that attempts to modify stimulation parameters without the `integrity.write` capability receives a permission denial, not a policy discussion.

   Epistemic note

 Neurorights as a legal and philosophical concept are under active academic debate. The operational definitions above are QIF-specific mappings for threat modeling and access control purposes. They are not settled legal standards, and the specific ACL implementation has not been validated against real clinical or regulatory requirements. The threshold values \(e.g., “10% of baseline” for psychological continuity\) are proposed defaults, not evidence-based thresholds.

     ## 14. Neural OS Architecture

  Runemate is the userspace layer of a proposed neural operating system. The architecture maps directly to the Unix/Linux model that has proven itself across five decades of systems engineering.

### 14.1 The Linux Mapping

| Linux Component | Neural OS Component | Function |
| --- | --- | --- |
| Kernel | Neurowall | Zero-trust enforcement at I0 \(hardware-biology boundary\). Amplitude bounds, rate limiting, thermal monitoring, DoS detection, integrity verification. Cannot be bypassed by userspace. |
| Device drivers | NSP | Encrypted communication layer. ML-KEM key exchange, ML-DSA authentication, AES-256-GCM-SIV session encryption, frame-level integrity verification. Handles the wire protocol between gateway and implant. |
| Userspace | Runemate | Content compilation, rendering pipeline, multimodal delivery \(visual, auditory, haptic\). The Forge compiles on the gateway; the Scribe interprets on-device. |
| Shell \(bash/zsh\) | Terminal | Patient CLI. Inspect device state, configure parameters, script automation, troubleshoot issues, compose custom navigation patterns. |
| File permissions | Neurorights | MP, CL, MI, PC, EA as capability-based ACL flags on every operation. |
| Package manager | Staves registry | Verified, signed content packages. Each package declares its required capabilities. \(Proposed.\) |
| System logs | runemate log | Auditable record of every packet delivered to the nervous system, every consent decision, every parameter change. |
| Process isolation | Capability tokens | Each session, command, and script runs within its declared capability set. No command can escalate beyond its token. |

### 14.2 CLI Security Analysis

  A reasonable objection: does adding a CLI to a neural device introduce new attack surface?

 No. The CLI does not expand the attack surface beyond what already exists. Runemate already executes bytecode. The Scribe interpreter processes arbitrary compiled content on-device. The execution surface already exists. A CLI is a structured, capability-gated interface to that same execution engine. It is a *subset* of what the interpreter can do, constrained by explicit capability tokens.

  The Rust `no_std` runtime eliminates the class of vulnerabilities that make traditional shells dangerous:

     #### No buffer overflows

 Rust’s borrow checker enforces memory safety at compile time. There is no `strcpy`, no `sprintf`, no unchecked array index.

    #### No heap corruption

 The `no_std` runtime uses a fixed-size arena allocator with bounds checking. There is no `malloc`/`free` cycle to abuse.

    #### No shell injection

 There is no `exec()`, no `system()`, no string interpolation into command invocations. Commands are parsed through the same recursive descent parser that handles Staves bytecode, with the same security properties, same input validation, same bounds checking.

    #### No arbitrary code execution

 The Staves DSL is non-Turing-complete. The CLI parses a fixed command grammar. Neither can execute arbitrary instructions.

  A capability-based shell is strictly less powerful than the bytecode interpreter it sits on top of. It can do only what the capability token authorizes, which is always a subset of what the interpreter can process. The CLI adds visibility and control without adding capability.

### 14.3 Why Open Source

  The same reasons Linux won:

     #### Auditability

 Anyone can read the code that runs inside a patient’s skull. No black boxes. A patient, their advocate, or an independent security researcher can verify every line of code in the stack.

    #### No vendor lock-in

 A patient’s perceptual system should not be tied to a single manufacturer’s proprietary stack. If the manufacturer goes bankrupt, pivots, or makes decisions the patient disagrees with, the patient’s sensory system continues to function.

    #### Community security

 More eyes on the code means more vulnerabilities found before they reach patients. The Linux kernel receives security patches from thousands of contributors. A neural device’s kernel should benefit from the same model.

    #### Longevity

 Implants outlast companies. The average corporate lifespan of an S&P 500 company is 21 years \(Innosight, 2021\). A neural implant may operate for 20–30 years. Open-source code outlasts both corporations and their proprietary formats.

    #### Right to fork

 If the maintainers make decisions a patient disagrees with, the patient \(or their advocate\) can fork the stack and run their own version. This is not theoretical — it is the mechanism by which patients retain ultimate control over their own neural device.

     ## 15. Vision Restoration Pipeline

### 15.1 Runemate \+ NSP for Vision

  The pipeline for restoring vision to a patient with a cortical visual prosthesis:

```
Internet Content          The Forge (Gateway)           NSP Wire              The Scribe (Implant)
─────────────────    ──────────────────────────    ───────────────    ─────────────────────────────
                     ┌─────────────────────────┐
  HTML/media    ──►  │ 1. Parse semantic content│
                     │ 2. Extract visual intent │
                     │ 3. Compile to Staves     │
                     │ 4. TARA safety check     │──► REJECT if unsafe
                     │ 5. Compress (67.8%*)     │
                     │ 6. NSP encrypt (PQ)      │
                     └────────────┬────────────┘
                                  │
                          Encrypted Staves
                           bytecode (341 B*
                           avg per frame)
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ Neurowall inspection   │──► REJECT if bounds exceeded
                     │ (amplitude, rate, DoS) │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ 7. Decrypt + verify    │
                     │ 8. Decode bytecode     │
                     │ 9. Retinotopic map     │──► V1 electrode coordinates
                     │10. Stimulate cortex    │
                     └────────────────────────┘
                                  │
                                  ▼
                         Patient perceives
                         visual content
```

  The Forge compiler on the gateway converts internet content \(HTML, images, video\) into semantic visual intent, not pixel data, but structural content: “heading, paragraph, image with these edges, link.” This intent is compiled into Staves bytecode, validated against TARA safety bounds \(ensuring no stimulation pattern exceeds tissue-safe thresholds\), and encrypted via NSP for transmission.

  On-device, the Scribe interpreter decrypts the bytecode, applies a retinotopic coordinate transform \(mapping visual content positions to V1 electrode locations based on the patient’s individual cortical geometry\), and generates stimulation patterns that the patient perceives as visual content.

 The same pipeline handles auditory content \(tonotopic mapping to primary auditory cortex, A1\) and haptic content \(somatotopic mapping to primary somatosensory cortex, S1\). A single Staves file can contain all three modalities, synchronized to the same timestamp.

### 15.2 Multimodal Content Delivery

  This means a blind patient can browse a website, watch a video, read a meme, listen to music, or build with AI — the same content sighted users access, compiled into a format their visual cortex can interpret. No browser required. No app store. No middleman. Just a compiler, a protocol, and a terminal.

 The patient sees what they choose to see, hears what they choose to hear, and feels what they choose to feel. The choice is theirs. The terminal is how they exercise it.

   ⚠ Epistemic note

 Cortical visual prostheses are an active area of research \(Second Sight Orion, Gennaris/Monash Vision Group, CORTIVIS/Miguel Hernandez University\). Current devices produce low-resolution phosphene patterns \(tens to hundreds of electrodes\), not the high-fidelity perception described in the pipeline above. The pipeline is a proposed architecture — the retinotopic coordinate transforms, stimulation patterns, and perceptual quality are subjects of ongoing research. The compression ratio \(67.8%\) and average frame size \(341 B\) are internal PoC benchmarks from the Forge v1.0 demo run and require independent replication; visual content compression has not been benchmarked. Clinical efficacy of the described pipeline is unknown and requires independent validation.

     ## 16. Governance

### 16.1 RACI Matrix

  The complete RACI matrix covers 30\+ scenarios across six stakeholder categories: **Patient**, **Clinician**, **Manufacturer**, **Regulator**, **Open Standard \(QIF\)**, and **AI System**.

#### Hardware & Safety

 Amplitude ceilings, seizure thresholds, recalls

#### Therapeutic Operations

 Stimulation bounds, domain expansion, patient scripts

#### Software & Firmware

 Routine updates, security patches, OS choice

#### Data & Privacy

 Export, research sharing, law enforcement, post-mortem

#### Autonomy & Enhancement

 Off-label expansion, cognitive enhancement, AI suggestions

#### Emergency & Edge Cases

 Cyber attack, manufacturer bankruptcy, incapacitation

  See [QIF-GOVERNANCE-QUESTIONS.md](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-GOVERNANCE-QUESTIONS.md) Part II for the complete RACI matrix.

### 16.2 Neuroethics and Neurorights Mapping

  Every governance question maps to one or more of the five proposed neurorights:

| Neuroright | Governance Questions |
| --- | --- |
| Mental Privacy \(MP\) | Data export, source code escrow, law enforcement access, telemetry consent |
| Cognitive Liberty \(CL\) | Domain access authorization, root access, patient vs clinician authority |
| Mental Integrity \(MI\) | Amplitude ceilings, therapeutic vs enhancement, escalation prevention |
| Psychological Continuity \(PC\) | Device as identity, firmware updates, support commitment, evolving capabilities |
| Equal Access \(EA\) | Interoperability, open vs proprietary, Neural Atlas, funding models |

  These map directly to the ACL flags defined in the passwordless security architecture and the guardrails defined in [GUARDRAILS.md](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/GUARDRAILS.md).

### 16.3 Open Source Neural Atlas

  Why it matters now

 Second Sight’s 2020 closure left Argus II patients with unsupported hardware in their eyes. Open standards prevent this. TCP/IP took 9 years from proposal to adoption. The discussion must precede the technology.

  A proposed open hardware specification for neural interfaces enabling:

#### Hardware interchangeability

 Electrode arrays, processing units, communication modules

#### Software portability

 OS choice independent of hardware

#### Data portability

 Calibration data, configurations, content libraries

#### Manufacturer independence

 No vendor lock-in

  **The hybrid path:** Open standard \(QIF \+ NSP \+ Staves\) \+ certified implementations \+ source code escrow \+ formal certification body \+ AI-assisted support. See [QIF-GOVERNANCE-QUESTIONS.md](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-GOVERNANCE-QUESTIONS.md) Part V for the full evaluation.

### 16.4 Open Questions

  QIF raises 30\+ governance questions that society must answer. They are documented in [QIF-GOVERNANCE-QUESTIONS.md](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-GOVERNANCE-QUESTIONS.md) and [QIF-NEUROETHICS.md](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-NEUROETHICS.md). Key unresolved tensions:

     #### Autonomy vs. Safety

 Patient’s right to modify vs. risk of self-harm

    #### Privacy vs. Research

 Neural data privacy vs. advancing neuroscience

    #### Innovation vs. Standardization

 Open standards vs. constraining innovation

    #### Individual vs. Collective

 One patient’s experiment vs. field reputation

    #### Present vs. Future Consent

 Consenting to capabilities that don’t exist yet

    #### Access vs. Security

 More patients = more targets = more risk

  These are not QIF’s questions to answer. They are society’s. QIF provides the technical framework that makes the answers enforceable.

     ## 17. Research Validation: Field Evidence

  This framework was not built in isolation from real systems. During the initial research pass that led to QIF, the author discovered a previously undisclosed vulnerability in a widely deployed, open-source data transport protocol used by nearly all BCI research platforms. The protocol operates bidirectionally — it both reads from and writes to the endpoint — and the vulnerability exists at the endpoint layer, where no authentication, encryption, or integrity verification is enforced. Any device on the local network can inject arbitrary data streams indistinguishable from legitimate neural signals.

 The author performed responsible disclosure to the protocol’s maintainers. The maintainers acknowledged the finding and characterized the lack of security as “by design” — the protocol was built for laboratory convenience, not adversarial environments. The disclosure resulted in maintainer discussions about developing a secure variant of the protocol. The protocol’s name is withheld here as the underlying architecture remains unchanged in production deployments.

  The core thesis, validated

 This single finding validates the core thesis of this paper: the most widely used BCI infrastructure was never designed with security in mind, and the transition from laboratory to clinical deployment does not magically add the security properties that were never there. The vulnerability is not exotic. It is the kind of basic endpoint exposure that would fail a first-year penetration test in enterprise IT. That it persists in a protocol handling neural data underscores how far behind the BCI ecosystem is on security fundamentals.

### 17.1 NISS and the Standards Community

  NISS attracted attention from the FIRST.org community responsible for maintaining CVSS, the global standard for vulnerability severity scoring. The author was invited to contribute NISS to the CVSS Resources repository as a domain-specific extension for neural interface vulnerabilities.

 The author declined, temporarily. NISS is currently a single-author derivation. The mathematical model has not been independently reviewed, replicated, or stress-tested by another researcher. Contributing it to a standards resource repository before that independent validation would be premature and would risk lending unearned authority to unvalidated math.

  The invitation itself is validation that the problem NISS addresses is recognized by the standards community. The restraint in accepting it is validation that this project prioritizes rigor over recognition.

### 17.2 Preprint and Publication Status

  The academic preprint is published on Zenodo \(DOI: [10.5281/zenodo.18640105](https://doi.org/10.5281/zenodo.18640105), v1.4 as of February 2026, CC-BY 4.0\). arXiv submission is pending endorsement.

 The preprint history includes a transparency note: v1.0 shipped with 3 fabricated citations that were AI-generated and not caught before publication. These were corrected in v1.1 and the incident is disclosed in the paper’s AI collaboration section. This is mentioned not as a disclaimer but as evidence that the verification protocol described in this paper exists because the author learned the hard way that AI-generated citations cannot be trusted without independent resolution.

  The complete derivation log contains 106 entries spanning the full development arc, from the first “OSI is wrong” insight through TARA expansion, NISS scoring, neurorights mapping, and the Neural OS architecture. Every entry documents the human decision, which AI systems were involved, and what was accepted versus rejected. Read the full log at [QIF-DERIVATION-LOG.md](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md).

     ## 18. How to Help

  QIF is open research, not a finished product. It was built by one independent researcher with AI collaboration. No lab, no faculty advisor, no institutional review board. The framework, the threat taxonomy, the scoring system, and the neurorights mappings all need stress testing by domain experts. Nothing here has been peer-reviewed yet. Here's where your expertise fits.

     🩺 ### Clinicians

- Use the [Neural Impact Chain](https://qinnovate.com/research/whitepaper/#neural-impact) to understand security risks in terms of clinical outcomes
- Review [TARA Clinical projections](https://qinnovate.com/atlas/tara/) for therapeutic analogs and risk profiles
- Apply [consent tiers](https://qinnovate.com/research/whitepaper/#governance) to BCI technique selection in treatment planning
- The DSM-5-TR mapping bridges security language and clinical language

    🧠 ### Psychologists

- Use the [DSM-5-TR diagnostic mapping](https://qinnovate.com/research/whitepaper/#neural-impact) to assess cognitive and psychiatric risks of BCI techniques
- Evaluate [NISS Cognitive Reconnaissance and Disruption scores](https://qinnovate.com/atlas/scoring/) for impact on perception, agency, and decision-making
- Inform neuropsychological assessment protocols with the [band-to-function mapping](https://qinnovate.com/research/whitepaper/#hourglass)
- Contribute clinical expertise to the dual-use classification of emerging neurotechnologies

    🔬 ### Researchers

- Use the [TARA atlas](https://qinnovate.com/atlas/tara/) to identify risk profiles for BCI techniques in your studies
- Apply [NISS scoring](https://qinnovate.com/atlas/scoring/) to quantify neural impact in vulnerability reports
- Reference the [Neural Impact Chain](https://qinnovate.com/research/whitepaper/#neural-impact) for technique-to-diagnosis mapping
- Cite: `Qi, K. (2026). QIF v8.0. Qinnovate. Available at qinnovate.com`

    ⚙ ### Engineers & Implementers

- **Post-quantum native.** [NSP](https://qinnovate.com/guardrails/nsp/) and Runemate are designed PQC-first — no legacy cipher inheritance. NIST [mandates](https://csrc.nist.gov/pubs/ir/8547/ipd) all legacy encryption deprecated by 2030 and disallowed by 2035 — and adversaries are already harvesting encrypted data today to crack later. Neural data has a lifetime shelf life; we’re not shipping it with an expiration date.
- Employ the [hourglass model](https://qinnovate.com/research/whitepaper/#hourglass) to structure threat assessments by architectural band
- Map your device's threat surface to [TARA categories](https://qinnovate.com/atlas/tara/)
- All specifications are Apache 2.0 — fork, implement, contribute

    🏛 ### Standards Bodies

- Evaluate NISS as a neural-specific complement to CVSS for BCI vulnerability scoring
- Review the [consent tier](https://qinnovate.com/research/whitepaper/#governance) framework for alignment with your regulatory structure
- The hourglass model provides a neutral, device-agnostic architectural taxonomy
- Collaboration welcome: [github.com/qinnovates](https://github.com/qinnovates)

  ## 19. What’s Next

  QIF is designed as a living framework. As neural devices mature, new threats will emerge. The framework has to keep up. Our immediate priorities:

  #### NISS v2.0

 Five new weighting factors \(reversibility severity, functional impact domains, pathway specificity, clinical evidence strength, modality criticality\). Extended clinical outcome mapping across 5 sensory modalities with ICD-10-CM coverage. Calibrate weights via expert elicitation and interrater reliability studies.

    #### NSP Reference Implementation

 Open-source reference implementation of the full 5-layer protocol stack on a constrained ARM Cortex-M4 target.

    #### Runemate Forge v1.0

 Native Staves DSL compiler with multimodal support \(visual, auditory, haptic\). Hand-rolled lexer, recursive descent parser, TARA safety bounds at compile time. 67.8% compression \(internal PoC benchmark from Forge v1.0 demo run, requires independent replication\), 430µs compile\+encrypt \(AI-derived simulation estimate, hardware validation pending\). Targeting IEC 62304 Class C. Today’s BCIs are outward-only \(Neuralink, BrainGate\); Runemate targets the next generation of inward-rendering implants.

 **Hardware-first rendering architecture:** The vision restoration pipeline uses depth sensors \(Kinect-class hardware\) as the primary spatial input, with AI operating as a color reconstruction layer on top — not as the sole rendering engine. This is intentional by design. Hardware sensors return deterministic geometry: distance, surface, edges. AI uses depth and transforms \(much like Unreal Engine\) to infer and render color back into the scene rather than generating the full environment from scratch. We propose this as a **human-continuity guardrail**: the principle that a patient’s primary sensory experience must never fully depend on software that can fail, be corrupted, or go offline. The hardware provides that continuity. If the AI layer fails or goes offline during system upgrades or patches, the spatial environment is still visually represented through hardware sensor data alone. Color may not exist temporarily during outages — but vision itself persists from the depth data. You lose the paint, not the canvas.

 **Lesson from prototyping:** During development of the depth-sensor visualization on this site, we discovered that sensor-to-vector-space mapping does not require high-fidelity source video. A heavily compressed, low-resolution depth feed produced the same spatial point cloud as the original high-quality capture. This reinforces the architecture: sensors capture geometry in vector space — points, distances, surfaces — not pixels. The AI rendering layer reconstructs visual quality from that spatial data. This means the bandwidth and processing requirements for the sensor-to-device link are significantly lower than a traditional video pipeline, because the bottleneck is spatial accuracy, not pixel density.

    #### Community & Governance

 Establish a technical advisory board. Formalize the contribution process. Build partnerships with academic neuroscience labs and BCI manufacturers.

  The internet got one chance to build its foundation right, and missed it. Brain-computer interfaces are getting that same chance right now. The chips are in human skulls. The clinical trials are running. The question is not whether these devices need security. The question is whether we build it before or after the first patient is harmed.

 This framework is one proposal. It is open, it is incomplete, and it is waiting for better ideas. What it is not is optional. Neural devices will be secured. The only question is by whom, and whether patients had a voice in the design.

  QIF, its underlying standards, and the TARA atlas are all maintained as open resources. For developers of devices that interface with the brain, we offer support in securing these critical systems.

  [GitHub →](https://github.com/qinnovates) [Framework Overview →](/framework/)

     ## Glossary

   BCI Brain-Computer Interface. A device that reads or writes neural signals.

 QIF The proposed open security framework described in this paper.

 TARA The threat technique catalog. Attack techniques mapped to therapeutic analogs across 11 biological domains.

 NISS Neural Impact Scoring System. 6-dimension severity scoring that supplements CVSS.

 NSP Neural Sensory Protocol. Post-quantum wire protocol for neural data streams.

 CVSS Common Vulnerability Scoring System \(FIRST.org\). Industry standard for IT.

 PINS Potential Impact to Neural Safety. Flag for techniques with ongoing harm risk.

 Hourglass 11-band architecture model: 7 neural \(N7-N1\), 1 interface \(I0\), 3 synthetic \(S1-S3\).

 I0 Interface band. The electrode-tissue boundary where biology meets silicon.

 Dual-use Same mechanism used for therapy and attack. Difference: consent, dosage, oversight.

 Neuromodesty Principle that neural correlates do not prove causation \(Morse 2006\).

 Runemate Proposed on-device DSL compiler for neural content with safety bounds.

 Cs Coherence Metric. Proposed signal integrity score for real-time BCI monitoring.

 PQC Post-Quantum Cryptography. Algorithms resistant to quantum computer attacks.

 ML-KEM Module Lattice Key Encapsulation. NIST-selected PQC key exchange standard.

 DSM-5-TR Diagnostic and Statistical Manual \(APA\). Referenced for threat modeling, not diagnosis.

     ## 20. Limitations, AI Methodology & Transparency

  QIF was developed by a single independent researcher. The framework, threat taxonomy, scoring system, clinical mappings, and architectural decisions are mine. One perspective. Multi-disciplinary peer review is essential before any component informs clinical or regulatory practice.

### 20.1 Known Limitations

   No empirical validation on real BCI devices

 TARA was developed through literature review, threat modeling, and systematic analysis, not penetration testing of neural hardware. One real-world software vulnerability has been validated \(see case studies\); neural-zone validation requires clinical access unavailable to independent researchers.

  DSM-5-TR references are for threat modeling, not clinical diagnosis

 The Neural Impact Chain references DSM-5-TR diagnostic criteria to illustrate potential clinical severity of attack patterns. These are threat modeling references, not diagnostic claims. Neuroscience does not yet fully understand how the brain produces cognition and emotion \(Morse, 2006\). Neural correlates do not prove causation. These mappings have not been reviewed by psychiatrists or clinical neuroscientists. Clinical validation is required before they can inform any clinical practice.

  NISS weights not calibrated

 Default weights \(BI=1.0, CR=0.5, CD=0.5, CV=1.0, RV=1.0, NP=1.0\) were set analytically to maintain backward compatibility with v1.0, not derived from empirical data. Context profiles \(Clinical, Research, Consumer, Military\) propose differential weights, but none have been calibrated against clinical outcomes or expert elicitation.

  No interrater reliability study

 NISS scores were assigned by a single analyst. No interrater reliability study has assessed whether independent scorers would assign the same metric values. CVSS interrater reliability is a known challenge; NISS likely faces greater variability.

  Taxonomy completeness

 161 techniques as of v1.4. The BCI threat surface is expanding. 26 techniques are classified as Theoretical and 1 as Speculative — grounded in known physics but not empirically demonstrated. This registry is a foundation, not a complete enumeration.

### 20.2 Key Design Decisions

  Every architectural choice in QIF is documented in a [106-entry derivation log](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md) written like a lab notebook. Below are the pivotal decisions that shaped the framework, each one traceable to a specific entry with full reasoning chains.

      #### “OSI layers are meaningless for BCI.”

 [Entry 1](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md#entry-1-osi-layers-are-meaningless-for-bci)

 The original 14-layer model stacked neural layers on top of the OSI networking model. I realized this was actively misleading. There is no MAC addressing in the cortex, no IP routing in neural tissue. The entire OSI heritage was stripped and replaced with a model derived from neuroscience and physics, not 1984 telecom.

     #### The hourglass: “like a black hole — everything funnels through one point.”

 [Entry 7](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md#entry-7-the-hourglass-model)

 After noticing that the electrode and the trust boundary are literally the same physical location \(Entry 2\), the circular topology evolved into an hourglass. Width represents state space: quantum possibility above, classical pathways below, with the measurement bottleneck \(I0\) at the narrowest point. Every BCI signal — therapeutic or adversarial — must pass through this single point.

     #### Post-quantum because implants outlive algorithms.

 [Entry 31](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md#entry-31-nsp-goes-post-quantum--the-implant-lifetime-argument)

 A brain implant cannot be firmware-updated like a phone. If it ships with RSA-2048 and quantum computers break RSA in 2035, every patient with that implant is permanently exposed. NIST mandates legacy encryption deprecated by 2030 and disallowed by 2035. NSP was designed PQC-first \(ML-KEM, ML-DSA\) because neural data has a lifetime shelf life. Adversaries are already harvesting encrypted traffic to crack later.

     #### TARA: the attack registry IS the therapy registry.

 [Entry 50](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md#entry-50-tara--therapeutic-atlas-of-risks-and-applications)

 While cataloguing attack techniques, I kept finding the same mechanisms on the therapeutic side. Signal injection is an attack vector — and the basis of DBS for Parkinson’s. The distinction isn’t mechanism; it’s consent, dosage, and oversight. This insight reframed the entire threat registry from a pure attack catalog into a dual-use mechanism atlas. The name TARA \(Sanskrit: “star,” bodhisattva of compassion\) was chosen deliberately.

     #### NISS scores correspond to psychiatric diagnostic categories — unintentionally.

 [Entry 53](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md#entry-53-tara-to-dsm-5-tr-diagnostic-mapping-via-neural-impact-chain)

 NISS was designed as a security scoring system. When I mapped the six metrics against DSM-5-TR chapters, the correspondence was immediate: high Biological Impact maps to motor/neurocognitive disorders; high Cognitive Reconnaissance and Disruption scores correspond to psychotic features; elevated Consent Violation maps to mood/trauma disorders. The security metrics corresponded to psychiatric diagnostic categories without being designed to. This structural observation requires clinical validation \(which we are actively seeking\).

     #### “Don’t add components — deepen existing ones.”

 [Entry 47](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md#entry-47-dsm-dissolved-into-nsp--no-separate-component)

 When dynamical systems monitoring \(phase dynamics, bifurcation detection, Lyapunov tracking\) needed a home, the instinct was to create a new named component. Instead, these capabilities folded naturally into NSP’s existing Biological TLS validation layers. No new acronym. No parallel system. This reflects a core QIF philosophy: if a capability belongs inside an existing component, it isn’t a new component — it’s a sharper tool for the one you already have.

     #### NSP is not the brake — it’s the safety certification that enables medicine.

 [Entry 48](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md#entry-48-nsp-reframed--the-trust-layer-that-enables-medicine)

 NSP was initially framed as a defense protocol. The reframe: no audiologist prescribes a stimulation implant if the patterns can be replayed or corrupted. No clinician trusts a vision prosthesis if the signal can be intercepted. NSP \+ Runemate are the secure infrastructure that makes clinical BCI applications possible. Security enables medicine; it doesn’t constrain it.

  The complete derivation log contains 106 entries spanning weeks of development, from the first “OSI is wrong” insight through the final neurorights restructuring. Every entry documents the human decision, which AI systems were involved, and what was accepted versus rejected. Read the full log at [QIF-DERIVATION-LOG.md](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md).

### 20.3 AI Methodology

  This project spans 161 attack techniques across clinical, neural, and digital domains. I used Claude, Gemini, and ChatGPT as computational research assistants to synthesize regulatory datasets, cross-reference neuroscience literature, and generate code. Every AI-generated claim was verified against primary sources. The verification methodology and full AI interaction protocol are documented in the [Derivation Log](https://qinnovate.com/news/derivation/).

   AI-Assisted

- Literature synthesis and cross-domain mapping across FDA, ISO, GDPR regulatory frameworks
- Code generation for data pipelines, visualization components, and analysis scripts
- Draft text generation \(estimated <15% retained verbatim; remainder rewritten by author\)
- Cross-validation of factual claims across multiple AI systems to reduce single-model bias

  Human-Originated

- The 11-band hourglass architecture and its mathematical derivation
- TARA threat taxonomy structure and all 161 technique classifications
- NISS scoring methodology, all metric assignments, and all NISS scores
- Neural Impact Chain pipeline and all DSM-5-TR diagnostic mappings
- All architectural decisions, research conclusions, and governance design

  **Citation integrity note:** The working paper v1.0 shipped with 3 fabricated citations introduced during AI-assisted bibliography construction. These were caught and corrected in v1.1 through a two-pass independent verification audit. All references in the current version have been verified against their source publications via DOI resolution and publisher page confirmation. This experience led to a mandatory [automated citation verification pipeline](https://github.com/qinnovates/neurosecurity/blob/main/scripts/verify/verify_citations.py).

  The author takes full responsibility for all content in this research proposal, irrespective of how it was generated. AI tools cannot be listed as authors per arXiv, ACM, and IEEE policy. No AI system originated any architectural or methodological contribution.

  ### 20.4 Audit Trail

  Every decision, derivation, and AI interaction is logged in a cryptographically verifiable audit trail. Monthly checksums of collaboration logs are GPG-signed by the maintainer. The full chain of evidence:

  [Peer-Citable Working Paper DOI: 10.5281/zenodo.18640105 — Full paper with Section 9: Limitations & AI Disclosure. CC-BY 4.0.](https://doi.org/10.5281/zenodo.18640105) [Transparency Statement Full AI collaboration disclosure, HITL methodology, GPG-signed monthly checksums, cross-AI validation sessions.](https://github.com/qinnovates/neurosecurity/blob/main/governance/TRANSPARENCY.md) [Derivation Log 97 timestamped entries documenting every architectural decision, hypothesis, and reasoning chain. Lab-notebook format.](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-DERIVATION-LOG.md) [Field Journal Personal research observations, experiential notes, and cross-disciplinary insights recorded during development.](https://github.com/qinnovates/neurosecurity/blob/main/osi-of-mind/QIF-FIELD-JOURNAL.md)

  **Verification:** Every development session is logged. Monthly checksums are GPG-signed \(`gpg --verify _memory/collab/YYYY-MM.md.asc`\). Cross-AI validation sessions are recorded in the Transparency Statement with date, topic, AI systems involved, and the human decision for each disagreement. The full commit history is public at [github.com/qinnovates/qinnovate](https://github.com/qinnovates/neurosecurity).

     v8.0 Working Draft 2026-03-11 Apache 2.0

 **Author:** Kevin Qi ·
**Organization:** [Qinnovate](https://qinnovate.com/)

  [v7.1](/research/whitepaper/v7-1/) [v6.0](/research/whitepaper/v6/) [All older \(archived\)](https://github.com/qinnovates/neurosecurity/tree/main/src/pages/whitepaper)

     Version

  [v8.0 Current 2026-03-11 — Working draft — Author's Note, Claims & Disclaimers, Defense Paradox, AI Ethics, BCI Landscape](/research/whitepaper/)[v7.1 Archive 2026-03-05 — Guardrail compliance, neurorights attribution, terminology consistency](/research/whitepaper/v7-1/)[v7.0 Archive 2026-02-21 — BrainFlow validation, living validation system, interactive funding timeline](/research/whitepaper/v7/)[v6.0 Archive 2026-02-16 — Neurorights mapping, CCI, governance](/research/whitepaper/v6/)[v5.2 Archive 2026-02-14 — TARA expansion, physics feasibility tiering](/research/whitepaper/v5/)[v3.1 Archive 2026-02-08 — NSP protocol, Runemate DSL, hourglass validation](/research/whitepaper/v3/)[v2.0 Archive 2026-02-04 — Initial 11-band hourglass model](/research/whitepaper/v2/)

        [Qinnovate Open Neural Atlas](/) Open research on the security and governance of neural interfaces.

 QIF v8.0 Hourglass · Proposed Framework

### Neural Atlas

- [Atlas Overview](https://qinnovate.com/atlas/)
- [QIF Framework](https://qinnovate.com/framework/)
- [TARA Atlas](https://qinnovate.com/atlas/tara/)
- [NISS Scoring](https://qinnovate.com/atlas/scoring/)
- [Whitepaper](https://qinnovate.com/research/whitepaper/)

### Research & Development

- [Research Hub](https://qinnovate.com/research/)
- [BCI Landscape](https://qinnovate.com/research/landscape/)
- [Neurowall](https://qinnovate.com/guardrails/)
- [NSP Protocol](https://qinnovate.com/guardrails/nsp/)
- [Runemate](https://qinnovate.com/guardrails/runemate/)
- [News](https://qinnovate.com/news/)
- [RSS Feed](https://qinnovate.com/rss.xml)

### Connect

- [Mission](https://qinnovate.com/mission/)
- [Governance](https://qinnovate.com/governance/)
- [GitHub](https://github.com/qinnovates)
- [License \(Apache 2.0\)](https://github.com/qinnovates/neurosecurity/blob/main/LICENSE)

  © 2026 Qinnovate. Open research on the security and governance of neural interfaces.
