#include <iostream>
#include <fstream>
#include <vector>
#include <unistd.h>

// Mock the bare minimum definitions to simulate the Cyton Parsing logic
#define PACKET_START 0xA0
#define PACKET_END_STANDARD 0xC0
#define PACKET_END_RAW_AUX 0xC1

using namespace std;

// This closely mimics InterfaceSerial.pde and the OpenBCI_Cyton_Library parsing
void interpretBinaryStream(ifstream& serialStream) {
    int readState = 0;
    int localByteCounter = 0;
    int localChannelCounter = 0;
    
    char actbyte;
    int serialErrorCounter = 0;
    
    // Arrays representing the buggy old parser
    unsigned char localAdsByteBuffer[3] = {0};
    unsigned char localAccelByteBuffer[2] = {0}; // Vulnerable 2-byte array

    cout << "[C++ Firmware Mock] Listening for Cyton packets..." << endl;

    while (serialStream.get(actbyte)) {
        unsigned char u_actbyte = (unsigned char)actbyte;
        
        switch (readState) {
            case 0:
                // Look for header byte
                if (u_actbyte == PACKET_START) {
                    readState++;
                }
                break;
            case 1:
                // Packet counter
                readState++;
                localByteCounter = 0;
                localChannelCounter = 0;
                break;
            case 2:
                // ADS Channel Values
                localAdsByteBuffer[localByteCounter] = u_actbyte;
                localByteCounter++;
                if (localByteCounter == 3) {
                    localChannelCounter++;
                    if (localChannelCounter == 8) {
                        // All ADS channels arrived
                        readState++; 
                        localByteCounter = 0;
                        localChannelCounter = 0;
                    } else {
                        localByteCounter = 0;
                    }
                }
                break;
            case 3:
                // Accelerometer values - VULNERABLE LOGIC
                // The buggy parser just does localByteCounter++ without bounds checking when going to state 4!
                // We'll mimic the vulnerability we found in InterfaceSerial.pde
                
                // BOOM! Out of bounds memory corruption if framing desync happens
                localAccelByteBuffer[localByteCounter] = u_actbyte;
                localByteCounter++;
                
                if (localByteCounter == 6) { // Cyton has 6 aux bytes
                    readState++;
                }
                break;
            case 4:
                // End byte
                if (u_actbyte == PACKET_END_STANDARD || u_actbyte == PACKET_END_RAW_AUX) {
                    // Valid packet
                } else {
                    serialErrorCounter++;
                    cout << "[C++ Firmware Mock] Framing Error! Expected 0xC0 but got: 0x" << hex << (int)u_actbyte << endl;
                }
                readState = 0;
                break;
            default:
                readState = 0;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <pty_path>" << endl;
        return 1;
    }

    ifstream serialStream(argv[1], ios::in | ios::binary);
    if (!serialStream.is_open()) {
        cerr << "Failed to open PTY port: " << argv[1] << endl;
        return 1;
    }

    try {
        interpretBinaryStream(serialStream);
    } catch (const exception& e) {
        cerr << "\n[C++ Firmware Mock] FATAL CRASH: " << e.what() << endl;
        return 1;
    }

    return 0;
}
