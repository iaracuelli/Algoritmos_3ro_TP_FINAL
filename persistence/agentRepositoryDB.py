# persistence/agent_repositoryDB.py
# Implementación concreta del repositorio de agentes usando SQLite.
# Esta clase cumple el contrato AgentRepository.

import sqlite3
from models.agent import Agent

class AgentRepositoryDB:
    def __init__(self, db_path="agents.db"):          
        self.conn = sqlite3.connect(db_path)
        self._create_table()                            

    def _create_table(self):                              
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            )
        """)
        self.conn.commit()

    def save(self, agent):                    
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO agents (name, email, password, active) VALUES (?, ?, ?, ?)",
            (agent.name, agent.email, agent.password, int(agent.active))
        )
        self.conn.commit()
        agent.id = cursor.lastrowid               
        return agent   

    def update(self, agent):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE agents SET name = ?, email = ?, password = ?, active = ? WHERE id = ?",
            (agent.name, agent.email, agent.password, int(agent.active), agent.id)
        )
        self.conn.commit()
        return agent

    def _to_agent(self, row):
        id, name, email, password, active = row
        agent = Agent(id, name, email, password)        # el constructor recibe 4 argumentos
        agent.active = bool(active)                     # SQLite guarda 0/1
        return agent
    
    def list(self):                               
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, email, password, active FROM agents")
        rows = cursor.fetchall()

        return [self._to_agent(row) for row in rows] # Se convierten las filas en objetos Agents
    
    def get_by_id(self, id,):              
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, email, password, active FROM agents WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()

        if row:                            
            return self._to_agent(row)
        return None
