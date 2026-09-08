import aiohttp
import random
from random import randint

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.img = None
        self.power = random.randint(30, 60)
        self.hp = random.randint(200, 400)
        if pokemon_trainer not in self.pokemons:
            self.pokemons[pokemon_trainer] = self

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"""Pokemon's Name: {self.name}
                Pokemon's Power: {self.power}
                Pokemon's Health: {self.hp}"""

    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    img_url = data['sprites']['front_default']
                    return img_url 
                else:
                    return None

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "The Wizard Pokémon uses a shield during battle!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokemon's trainer @{self.pokemon_trainer} attacks @{enemy.pokemon_trainer}\nKesehatan @{enemy.pokemon_trainer} sekarang menjadi {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokemon's trainer @{self.pokemon_trainer} defeated @{enemy.pokemon_trainer}!"

class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        # Mengambil properti bawaan dari kelas Pokemon induk
        super().__init__(pokemon_trainer)
        
        # Properti unik khusus untuk kelas Wizard
        self.mana = random.randint(50, 100) 
        self.spell_power = random.randint(20, 40)

    # Metode unik khusus untuk kelas Wizard
    async def cast_spell(self, enemy):
        """Metode serangan sihir unik yang menggunakan mana"""
        if self.mana >= 20:
            self.mana -= 20  # Mengurangi mana setiap kali menggunakan sihir
            damage = self.power + self.spell_power
            
            if enemy.hp > damage:
                enemy.hp -= damage
                return f"🧙‍♂️ @{self.pokemon_trainer} chanting a spell over @{enemy.pokemon_trainer} amounting to {damage} damage!\nRemaining enemy HP: {enemy.hp} | Remaining Your Mana: {self.mana}"
            else:
                enemy.hp = 0
                return f"🧙‍♂️ @{self.pokemon_trainer} defeated @{enemy.pokemon_trainer} with deadly magic!"
        else:
            # Jika mana habis, lakukan serangan fisik biasa (memanggil attack dari induk)
            return "Mana is running out! Using a normal attack:\n" + await self.attack(enemy)


class Fighter(Pokemon):
    async def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = await super().attack(enemy)
        self.power -= super_power
        return result + f"\nThe Fighting-type Pokémon uses a super attack. The added power is:{super_power}"
