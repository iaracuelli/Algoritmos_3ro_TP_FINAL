from models.user import User
from models.agent import Agent


class AgentManager:
    def __init__(self, repository):
        self.repository = repository                 


    def create_agent(self, name, email, password):
            for agent in self.repository.list():
                if agent.email == email:
                    raise Exception("Ya existe un agente con ese email")
            
            agent = Agent(
                id=None,
                name=name,
                email=email,
                password=password   
            )
            return self.repository.save(agent)
        

    def list_agents(self):
        return self.repository.list()
        

    def get_agent_by_id(self, id):
       return self.repository.get_by_id(id)

    def update_agent(self, agent):
       return self.repository.update(agent)
