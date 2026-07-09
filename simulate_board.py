#!/usr/bin/env python3
import socket
import time
import math
import sys
import random

def pack_24bit(val: int) -> bytes:
    """Packs a signed integer into 3 bytes big-endian two's complement."""
    # Clip to 24-bit signed boundaries
    val = max(-8388608, min(8388607, int(val)))
    if val < 0:
        val += 16777216
    return bytes([(val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF])

def main():
    host = "127.0.0.1"
    port = 9090
    
    print(f"[BoardSim] Connecting to HIL loopback bridge at {host}:{port}...")
    
    # Try connecting with retries
    client_socket = None
    for attempt in range(5):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            break
        except Exception:
            print(f"[BoardSim] Connection failed (attempt {attempt+1}/5). Retrying in 1s...")
            time.sleep(1.0)
            
    if not client_socket:
        print("[BoardSim] Error: Could not connect to bridge. Is BCI running in HIL mode?")
        sys.exit(1)
        
    print("[BoardSim] Connected! Streaming protocol-equivalent 250 Hz raw frames...")
    
    sample_index = 0
    start_time = time.time()
    
    try:
        while True:
            # 1. Generate synthetic Parkinsonian STN LFP waveforms (20 Hz beta + 1.5 Hz envelope + noise)
            t = time.time() - start_time
            beta_rhythm = 40.0 * (1.0 + 0.4 * math.sin(2 * math.pi * 1.5 * t)) * math.sin(2 * math.pi * 20.0 * t)
            broadband = 5.0 * math.sin(2 * math.pi * 3.0 * t) + random.normalvariate(0, 2.0)
            lfp = beta_rhythm + broadband
            
            # Construct channels payload (Channel 0 holds LFP, other channels hold baseline noise)
            packet = bytearray()
            packet.append(0xA0)          # Cyton header byte
            packet.append(sample_index)  # Sample counter byte
            
            # Pack 8 channels
            for ch in range(8):
                microvolts = lfp if ch == 0 else random.normalvariate(0, 3.0)
                # Convert back to counts
                counts = int(microvolts / 0.02235174)
                packet.extend(pack_24bit(counts))
                
            # Footer / AUX bytes
            packet.extend(bytes([0, 0, 0, 0, 0, 0])) # 6 AUX bytes
            packet.append(0xC0)                      # Cyton footer byte
            
            # 2. Transmit raw 33-byte frame over loopback
            client_socket.sendall(packet)
            
            # Increment sample index
            sample_index = (sample_index + 1) % 256
            
            # 3. High-resolution sleep to maintain 250 Hz sample rate (4ms interval)
            # Take timing drift into account for real-world hardware emulation accuracy
            elapsed = time.time() - start_time
            target = (sample_index + 1) * 0.004
            diff = target - elapsed
            if diff > 0:
                time.sleep(diff)
                
    except KeyboardInterrupt:
        print("\n[BoardSim] Interrupted by user. Closing connection.")
    except Exception as e:
        print(f"[BoardSim] Connection error: {e}")
    finally:
        client_socket.close()
        print("[BoardSim] Stopped.")

if __name__ == "__main__":
    main()
