from unittest.mock import patch, mock_open

# Patch the secret generation during import
with patch('os.path.exists', return_value=True), \
     patch('builtins.open', mock_open(read_data=b'secret_123_456_789_012_345_678_901_2')):
    from vireon.mcp_server import mcp, mock_authenticate_session

def test_mcp_server_creation():
    assert mcp is not None
    assert mcp.name == "VIREON-Neural-Terminal"

@patch('os.environ.get')
def test_mcp_server_auth(mock_env):
    mock_env.return_value = "secret_123"
    result = mock_authenticate_session("biomarker_hash", role="clinician", auth_signature="secret_123")
    assert "session_token" in result or "error" not in result

