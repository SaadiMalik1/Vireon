"""
OpenBCI Physical Hardware Device Wrappers.
Uses BrainFlow to stream live clinical data from a Cyton or Ganglion board.
"""
from typing import List
from neuroshield.plugins.devices import IDeviceWrapper

try:
    import brainflow
    from brainflow.board_shim import BoardShim, BoardIds, BrainFlowInputParams
    HAS_BRAINFLOW = True
except ImportError:
    HAS_BRAINFLOW = False

class OpenBCICytonWrapper(IDeviceWrapper):
    def __init__(self, serial_port: str = "", **kwargs):
        if not HAS_BRAINFLOW:
            raise RuntimeError(
                "BrainFlow is required to use a physical OpenBCI board. "
                "Install it using: pip install brainflow"
            )
            
        params = BrainFlowInputParams()
        if serial_port:
            params.serial_port = serial_port
            
        self.board_id = BoardIds.CYTON_BOARD
        self.board = BoardShim(self.board_id, params)

    def get_board(self):
        return self.board

    def get_eeg_channels(self) -> List[int]:
        return BoardShim.get_eeg_channels(self.board_id)

class OpenBCIGanglionWrapper(IDeviceWrapper):
    def __init__(self, serial_port: str = "", **kwargs):
        if not HAS_BRAINFLOW:
            raise RuntimeError(
                "BrainFlow is required to use a physical OpenBCI board. "
                "Install it using: pip install brainflow"
            )
            
        params = BrainFlowInputParams()
        if serial_port:
            params.serial_port = serial_port
            
        self.board_id = BoardIds.GANGLION_BOARD
        self.board = BoardShim(self.board_id, params)

    def get_board(self):
        return self.board

    def get_eeg_channels(self) -> List[int]:
        return BoardShim.get_eeg_channels(self.board_id)
