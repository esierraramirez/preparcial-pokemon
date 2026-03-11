from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Pokemon API Parcial", description="A simple API to manage Pokemon data", version="1.0.0")

class Pokemon(BaseModel):
    id: int
    name: str
    attack: int
    lives: int
    type: str
    
    def attack_action(self):
        return f"{self.name} attacks with {self.attack} power!"
    
    def leave_pokeball(self):
        return f"{self.name} leaves the Pokeball!"