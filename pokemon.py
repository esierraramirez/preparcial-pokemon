from fastapi import FastAPI, Query
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

@app.get("/")
def home():
    return {"message": "Welcome to the Pokemon API!"}

# Create a endpoint to show all pokemons with query parameters
@app.get("/showallpokemons/", response_model=list[Pokemon])
def show_all_pokemon():
    return pokemons

# Create a endpoint to show one pokemon by name with query parameters
@app.get("/showpokemon/", response_model=Pokemon)
def show_pokemon(name: str = Query(...)):
    for pokemon in pokemons:
        if pokemon.name.lower() == name.lower():
            return pokemon
    return {"message": "Pokemon not found"}

# Create a endpoint to show one pokemon by id with query parameters
@app.get("/showpokemonbyid/", response_model=Pokemon)
def show_pokemon_by_id(id: int = Query(...)):
    for pokemon in pokemons:
        if pokemon.id == id:
            return pokemon
    return {"message": "Pokemon not found"}

# Create a endpoint to battle between two pokemons and return the winner, if the attack is the same, return for score winner
@app.get("/battle/")
def battle(pokemon1: str = Query(...), pokemon2: str = Query(...)):
    p1 = None
    p2 = None
    for pokemon in pokemons:
        if pokemon.name.lower() == pokemon1.lower():
            p1 = pokemon
        if pokemon.name.lower() == pokemon2.lower():
            p2 = pokemon
    if not p1 or not p2:
        return {"message": "One or both Pokemon not found"}
    
    if p1.attack > p2.attack:
        return {"winner": p1.name, "reason": "Higher attack power"}
    elif p2.attack > p1.attack:
        return {"winner": p2.name, "reason": "Higher attack power"}
    else:
        if p1.lives > p2.lives:
            return {"winner": p1.name, "reason": "Higher lives"}
        elif p2.lives > p1.lives:
            return {"winner": p2.name, "reason": "Higher lives"}
        else:
            return {"message": "It's a tie!"}

# Create a endpoint to order pokemons by a specific parameter return a list of pokemons ordered by the parameter
@app.get("/orderpokemons/")
def order_pokemons(parameter: str = Query(...)):
    if parameter not in ['id', 'name', 'attack', 'lives', 'type']:
        return {"message": "Invalid parameter"}
    return sorted(pokemons, key=lambda x: getattr(x, parameter))

