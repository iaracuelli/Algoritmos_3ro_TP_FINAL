from models.user import User

class Admin(User):
        def __init__(self, id, name, email, password):  
                super().__init__(id, name, email, password)     # llamo a User.__init__
                

        def assignTicket(self, agent, ticket):
                if agent.active == True:
                    agent.tickets.append(ticket) 
                    ticket.assign_to(agent, self)
                else:
                    raise Exception("Agente no activo")
                

        def reassignTicket(self, agent1, agent2 ,ticket):
              if agent2.active != True:
                    raise Exception("Agente no activo")
              if ticket in agent1.tickets:
                    agent1.tickets.remove(ticket)
              agent2.tickets.append(ticket)
              ticket.assign_to(agent2, self)

        def activateCustomer(self, customer):
              customer.active = True

        def deactivateCustomer(self, customer):
              customer.active = False

        def activateAgent(self, agent):
              agent.active = True

        def deactivateAgent(self, agent):
              agent.active = False
