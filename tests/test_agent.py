import pytest
from qrscan.agent import QRCodeAgent

def test_agent_init():
    agent = QRCodeAgent()
    assert agent.output_format == "json" 