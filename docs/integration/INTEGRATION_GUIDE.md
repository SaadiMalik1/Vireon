# VIREON Integration Guide

This document assists commercial vendors and medical device manufacturers in integrating proprietary systems with the VIREON runtime.

## 1. Zero Trust Integrations
When integrating closed-source hardware models, you must use the `vireon.sdk.SubprocessProvider` class. This spawns your binary in a sandbox, communicating with the core orchestrator via Protobufs over `stdio` or a local socket.

## 2. FlatBuffer Schema
To prevent versioning mismatches between VIREON and your internal systems, ensure that your integration serializes and deserializes data strictly according to the `.fbs` schemas located in `workspace/schemas/`. Do not rely on internal Python dictionary structures.
