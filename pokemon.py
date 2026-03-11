from fastapi import FastAPI
from pydantic import BaseModel
import csv

app = FastAPI(title="Pokemon API Parcial", description="A simple API to manage Pokemon data", version="1.0.0")

# Define the Pokemon model using Pydantic
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

# Create a fuction to read a archive CSV and return a list of Pokemon objects

def read_pokemon_csv(file_path: str):
    pokemon_list = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            pokemon = Pokemon(
                id=int(row['id']),
                name=row['name'],
                attack=int(row['attack']),
                lives=int(row['lives']),
                type=row['type']
            )
            pokemon_list.append(pokemon)
    return pokemon_list    

pokemons = read_pokemon_csv('pokemon.csv')

# Create a endpoint to create a new Pokemon


