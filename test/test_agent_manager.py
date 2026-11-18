from managers.agent_manager import AgentManager
from test.fake_repository import FakeRepository
import pytest 

def test_create_agent():
    manager = AgentManager(FakeRepository())
    agent = manager.create_agent("Ana", "ana@mail.com", "1234")
    assert agent in manager.list_agents()
    assert agent.name == "Ana"
    assert agent.email == "ana@mail.com"


def test_create_duplicate_agent():
    manager = AgentManager(FakeRepository())
    agent = manager.create_agent("Ana", "ana@mail.com", "1234")
    with pytest.raises(Exception):
        manager.create_agent("Ana", "ana@mail.com", "1234")