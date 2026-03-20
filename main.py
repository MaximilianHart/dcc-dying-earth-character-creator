import random
import json


def main():
    print("Welcome to the DCC Dying Earth Character Generator!")

    while True:
        peasant = Character()
        peasant.generate_zero_level()

        print(f"\n--- {peasant.name or 'Unnamed Peasant'} ---")

        print(
            f"{'Strength:':13} {peasant.stats['Strength']} ({peasant.strength_mod:+})"
        )
        print(f"{'Agility:':13} {peasant.stats['Agility']} ({peasant.agility_mod:+})")
        print(f"{'Stamina:':13} {peasant.stats['Stamina']} ({peasant.stamina_mod:+})")
        print(
            f"{'Intelligence:':13} {peasant.stats['Intelligence']} ({peasant.intelligence_mod:+})"
        )
        print(
            f"{'Personality:':13} {peasant.stats['Personality']} ({peasant.personality_mod:+})"
        )
        print(f"{'Luck:':13} {peasant.stats['Luck']} ({peasant.luck_mod:+})")

        print("-" * 40)
        print(f"HP: {peasant.max_hp:<10} AC: {peasant.ac}")
        print(
            f"SAVES | Fort {peasant.fortitude_save:+} | Ref {peasant.reflex_save:+} | Will {peasant.will_save:+}"
        )
        print("-" * 40)
        print(f"Birth Augur: {peasant.birth_augur}")
        print(f"Lucky Roll: {peasant.lucky_roll} ({peasant.luck_mod:+})")
        print("-" * 40)
        print(f"{'Occupation:':12} {peasant.occupation}")
        character_equipment = ", ".join(peasant.equipment)
        print(f"{'Equipment:':12} {character_equipment}")

        user_input = input(
            "\nType r to repeat and create a new peasant, or q to finish..."
        )

        if user_input == "r":
            print("\n" + "=" * 30 + "\n")
            continue
        else:
            print("Good luck in the funnel, peasant!")
            break


def dice(number, size):
    result = 0
    for i in range(number):
        die = random.randint(1, size)
        result += die
    return result


class Character:
    def __init__(self):
        self.name = None
        self.level = 0
        self.stats = {
            "Strength": 10,
            "Agility": 10,
            "Stamina": 10,
            "Personality": 10,
            "Intelligence": 10,
            "Luck": 10,
        }
        self.armor_bonus = 0
        self.max_hp = 0
        self.occupation = None
        self.alignment = None
        self.speed = 0
        self.initiative = 0
        self.equipment = []
        self.animus = {"Animus": None, "Animus Description": None}
        self.birth_augur = None
        self.lucky_roll = None
        self.languages = []

    @property
    def strength_mod(self):
        return self.calculate_modifier(self.stats["Strength"])

    @property
    def agility_mod(self):
        return self.calculate_modifier(self.stats["Agility"])

    @property
    def stamina_mod(self):
        return self.calculate_modifier(self.stats["Stamina"])

    @property
    def personality_mod(self):
        return self.calculate_modifier(self.stats["Personality"])

    @property
    def intelligence_mod(self):
        return self.calculate_modifier(self.stats["Intelligence"])

    @property
    def spells_memorized(self):
        if self.stats["Intelligence"] <= 3:
            return "No spellcasting possible"
        elif self.stats["Intelligence"] <= 5:
            return "-2 spells (minimum of 1 spell)"
        elif self.stats["Intelligence"] <= 7:
            return "-1 spell (minimum of 1 spell)"
        elif self.stats["Intelligence"] <= 13:
            return "No adjustment"
        elif self.stats["Intelligence"] <= 16:
            return "+1 spell"
        elif self.stats["Intelligence"] <= 18:
            return "+2 spells"
        else:
            return "+3 spells"

    @property
    def max_spell_level(self):
        if self.stats["Intelligence"] <= 3:
            return "No spellcasting possible"
        elif self.stats["Intelligence"] <= 7:
            return "1"
        elif self.stats["Intelligence"] <= 9:
            return "2"
        elif self.stats["Intelligence"] <= 11:
            return "3"
        elif self.stats["Intelligence"] <= 14:
            return "4"
        else:
            return "5"

    @property
    def luck_mod(self):
        return self.calculate_modifier(self.stats["Luck"])

    @property
    def reflex_save(self):
        return self.agility_mod

    @property
    def fortitude_save(self):
        return self.stamina_mod

    @property
    def will_save(self):
        return self.personality_mod

    @property
    def ac(self):
        return 10 + self.agility_mod + self.armor_bonus

    def calculate_modifier(self, score):
        if score >= 20:
            return 4
        elif score >= 18:
            return 3
        elif score >= 16:
            return 2
        elif score >= 13:
            return 1
        elif score >= 9:
            return 0
        elif score >= 6:
            return -1
        elif score >= 4:
            return -2
        elif score >= 2:
            return -3
        else:
            return -4

    def roll_stats(self):
        print("Rolling stats...")
        for stat_name in self.stats:
            self.stats[stat_name] = dice(3, 6)

    def roll_birth_augur(self):
        with open("birth_augurs.json", "r") as f:
            augur_data = json.load(f)

        luck_roll = augur_data[str(dice(1, 30))]

        self.birth_augur = luck_roll["sign"]
        self.lucky_roll = luck_roll["bonus"]

    def roll_hp(self):
        total_hp = dice(1, 4) + self.stamina_mod
        if self.birth_augur == "Bountiful harvest":
            total_hp += self.luck_mod
        self.max_hp = max(1, total_hp)

    def roll_occupation(self):
        with open("occupations.json", "r") as f:
            occupation_data = json.load(f)

        occupation_roll = dice(1, 100)
        for entry in occupation_data:
            if occupation_roll <= entry["max"]:
                self.occupation = entry["occupation"]
                self.equipment.append(entry["weapon"])
                self.equipment.append(entry["goods"])
                break

        if self.occupation == "Farmer":
            farmer_types = [
                "Potato",
                "Wheat",
                "Turnip",
                "Corn",
                "Rice",
                "Parsnip",
                "Radish",
                "Rutabaga",
            ]
            specialty = farmer_types[dice(1, 8) - 1]
            self.occupation = f"{specialty} Farmer"

        self.farm_animals()
        self.fill_pushcart()

    def farm_animals(self):
        variety_animals = ["Sheep", "Goat", "Cow", "Duck", "Goose", "Mule"]
        for i, item in enumerate(self.equipment):
            if item in ["Hen", "Sow", "Herding dog"]:
                pool = [item, item, random.choice(variety_animals)]
                self.equipment[i] = random.choice(pool)

    def fill_pushcart(self):
        cart_contents = [
            "Pushcart full of tomatoes",
            "Empty pushcart",
            "Pushcart full of straw",
            "Pushcart carrying your dead",
            "Pushcart full of dirt",
            "Pushcart full of rocks",
        ]
        for i, item in enumerate(self.equipment):
            if item == "Pushcart":
                self.equipment[i] = random.choice(cart_contents)

    def roll_animus(self):
        with open("animus.json", "r") as f:
            animus_data = json.load(f)
        animus_roll = dice(1, 30)

        for entry in animus_data:
            if animus_roll <= entry["max"]:
                self.animus["Animus"] = entry["animus"]
                self.animus["Animus Description"] = entry["animus"]
                break

    def generate_zero_level(self):
        self.roll_stats()
        self.roll_birth_augur()
        self.roll_hp()
        self.roll_occupation()
        self.roll_animus()


# Determine starting animus
#
# If vat-thing, determine pattern and starting flaw
#
# Determine languages
#
# Determine alignment
#
# Determine one random piece of equipment
#
# Roll on the Thaumaturgical Curious table
#
# Scan equipment for AC-boosting items
#
# Generate random name a la https://perchance.org/dying-earth-names#edit
#
# Print full character, possibly nicely formatted.
#

if __name__ == "__main__":
    main()
