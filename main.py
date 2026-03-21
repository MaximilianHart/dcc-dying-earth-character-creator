from typing import Dict
from rich.console import Console
import random
import json
import textwrap

console = Console(width=70)


def main():
    print("Welcome to the DCC Dying Earth Character Generator!")

    while True:
        peasant = Character()
        peasant.generate_zero_level()

        wrapper = textwrap.TextWrapper(
            width=50, initial_indent="  ", subsequent_indent="  "
        )
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
        print(
            f"HP: {peasant.max_hp:<5} AC: {peasant.ac:<5} Alignment: {peasant.alignment}"
        )
        print(
            f"SAVES | Fort {peasant.fortitude_save:+} | Ref {peasant.reflex_save:+} | Will {peasant.will_save:+}"
        )
        print("-" * 40)
        print(f"Birth Augur: {peasant.birth_augur}")
        lucky_info = wrapper.fill(
            f"Lucky Roll: {peasant.lucky_roll} ({peasant.luck_mod:+})"
        )
        print(lucky_info)
        print("-" * 40)
        print(f"{'Occupation:':12} {peasant.occupation}")
        print("-" * 40)
        print("Starting Equipment:")
        for item in peasant.equipment:
            item_wrapper = textwrap.TextWrapper(
                width=50, initial_indent="  - ", subsequent_indent="    "
            )
            print(item_wrapper.fill(str(item)))
        print("-" * 40)
        print(f"Animus: {peasant.animus['Animus']}")
        animus_description = wrapper.fill(peasant.animus["Animus Description"] or "")
        print(animus_description)
        print("-" * 40)

        if peasant.vat_data.get("Pattern"):
            print("\n------VAT-THING------")
            print("Note: Any stat adjustments below must be made manually.")
            print(f"Starting Flaw: {peasant.vat_data['Starting Flaw']}")
            print(f"Additional Weapon Training: {peasant.vat_data['Weapon Training']}")
            print(f"Vat-thing Pattern: {peasant.vat_data['Pattern']}")
            vat_thing_description = wrapper.fill(peasant.vat_data["Description"] or "")
            print(vat_thing_description)
            print("-" * 40)

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
        self.vat_data = {
            "Pattern": "",
            "Starting Flaw": "",
            "Weapon Training": "",
            "Description": "",
        }
        self.alignment = ""
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
        with open("de-occupations.json", "r") as f:
            occupation_data = json.load(f)

        occupation_roll = dice(1, 100)
        for entry in occupation_data:
            if occupation_roll <= entry["max"]:
                self.occupation = entry["occupation"]
                self.equipment.append(entry["weapon"])
                self.equipment.append(entry["goods"])
                break

        self.sacred_beasts()
        self.seeds()
        self.libram()
        self.folio()

    def sacred_beasts(self):
        sacred_beasts = [
            "bearded thawn foundling",
            "pair of pincer-lizards",
            "tittle-bird",
            "simiode",
        ]
        for i, item in enumerate(self.equipment):
            if item == "Sacred beast":
                self.equipment[i] = random.choice(sacred_beasts)

    def seeds(self):
        seed_types = [
            "myrhadion seeds, 1 oz.",
            "dymphian seeds, 1 oz.",
            "black quince seeds, 1 oz.",
            "long-stemmed stardrop seeds, 1 oz.",
            "blood-flower seeds, 1 oz.",
            "mandrake seeds, 1 oz.",
            "star-blossom seeds, 1 oz.",
            "moon-geranium seeds, 1 oz.",
        ]
        for i, item in enumerate(self.equipment):
            if item == "Seeds, 1 oz.":
                self.equipment[i] = random.choice(seed_types)

    def libram(self):
        libram_names = [
            "Classical Killings and Mortefactions",
            "Expositions and Dissolutions of Evil",
            "History of Granvilunde",
            "Attractive and Detractive Hyperordnets",
            "Therapy for Hallucinants and Ghost-takers",
            "Procedural Suggestions in Time of Risk",
        ]

        for i, item in enumerate(self.equipment):
            if item == "Libram of obscure historical information":
                self.equipment[i] = f"{item}: ({random.choice(libram_names)})"

    def folio(self):
        folio_subject = [
            "Amberlin I",
            "Archemand of Glaere",
            "Dibarcas Maior",
            "Llorio the Sorceress",
            "Mael Lel Laio",
            "Phandaal the Great",
        ]

        for i, item in enumerate(self.equipment):
            if item == "Folio annotating the life of an arch-magician":
                self.equipment[i] = (
                    f"Folio annotating the life of the famous arch-magician ({random.choice(folio_subject)})"
                )

    def roll_animus(self):
        with open("animus.json", "r") as f:
            animus_data = json.load(f)
        animus_roll = dice(1, 30)

        for entry in animus_data:
            if animus_roll <= entry["max"]:
                self.animus["Animus"] = entry["animus"]
                self.animus["Animus Description"] = entry["desc"]
                break

    def vat_thing(self):
        if self.occupation and self.occupation.startswith("Vat-thing"):
            patterns = ["Martial", "Paragon", "Theologue"]
            alignment = ["Chaotic", "Neutral", "Lawful"]
            weapon_training = [
                "Mace, flail, dart, battle-hook",
                "Axe (any), bow (any), arrow-gun",
                "Rapier, longsword, sling, snaffle-iron",
            ]
            self.vat_data["Pattern"] = random.choice(patterns)
            self.vat_data["Alignment"] = random.choice(alignment)
            self.vat_data["Weapon Training"] = random.choice(weapon_training)

            if self.vat_data["Pattern"] == "Martial":
                self.vat_data["Description"] = (
                    "You are a fighter, a tactician, a weapons-master created bu am arch-mage to guard their manse and command their armies. At 0 level, a vat-thing created from a martial pattern increases its Strength and Stamina until each modifier increases by one (e.g., a 9 Strength increases to a 13, and an 18 Stamina increases to a 20). In addition, starting at 1st level, a martial vat-thing receives a bonus die that is used when making attacks."
                )
            elif self.vat_data["Pattern"] == "Paragon":
                self.vat_data["Description"] = (
                    "You are a sculptor, a painter, a dancer, a courtesan made to fill a reclusive magician's household with works of art and the vibrant sounds of creation. At 0 level, a vat-thing created from a paragon pattern increases its Agility and Personality until each modifier increase by one (e.g., a 9 Agility increases to a 13, and an 18 Personality increases to a 20). In addition, starting at 1st level, a paragon vat-thing receives a bonus die that can be used when making skill checks."
                )
            elif self.vat_data["Pattern"] == "Theologue":
                self.vat_data["Description"] = (
                    "You are the memory, a counselor, a savant shaped by a great sorcerer to be a living encyclopaedist. At 0 level, a vat-thing created from a theologue pattern increases its Intelligence ability score until the modifier increases by one (e.g., a 9 Intelligence increases to a 13). In addition, starting at 1st level, a theologue vat-thing receives a bonus die that can be used when making skill checks, including when attempting to learn new spells or re-roll an existing one upon leveling (see p. 27)."
                )
            else:
                self.vat_data["Description"] = ""

            self.roll_vat_flaw()

    def roll_vat_flaw(self, existing_flaws=None):
        if existing_flaws is None:
            existing_flaws = []

        with open("vat_thing_flaws.json", "r") as f:
            flaw_data = json.load(f)

        vat_roll = dice(1, 30) + self.luck_mod

        if vat_roll >= 30:
            self.roll_vat_flaw(existing_flaws)
            self.roll_vat_flaw(existing_flaws)
        else:
            for entry in flaw_data:
                if vat_roll <= entry["max"]:
                    if entry["flaw"] not in [f["name"] for f in existing_flaws]:
                        existing_flaws.append(
                            {"name": entry["flaw"], "desc": entry["desc"]}
                        )
                    break

        names = [f["name"] for f in existing_flaws]
        descriptions = [f["desc"] for f in existing_flaws]
        self.vat_data["Starting Flaw"] = ", ".join(names)
        self.vat_data["Flaw Description"] = " | ".join(descriptions)

    def roll_alignment(self):
        roll = dice(1, 4)
        if roll == 1:
            self.alignment = "Lawful"
        elif roll == 2:
            self.alignment = "Neutral"
        else:
            self.alignment = "Chaotic"

    def roll_languages(self):
        alignment_map: Dict[str, str] = {
            "Lawful": "Law",
            "Chaotic": "Chaos",
            "Neutral": "Neutrality",
        }
        self.languages = ["Common tongue of the 21st Aeon"]
        self.is_literate = self.stats["Intelligence"] > 5

        if self.stats["Intelligence"] <= 7:
            return

        is_vat = self.occupation and self.occupation.startswith("Vat-thing")
        filename = "vat_thing_languages.json" if is_vat else "human_languages.json"

        with open(filename, "r") as f:
            language_data = json.load(f)

        num_bonus = max(0, self.intelligence_mod)

        for i in range(num_bonus):
            while True:
                roll = dice(1, 100)
                selected = ""

                for entry in language_data:
                    if roll <= entry["max"]:
                        selected = entry["language"]
                        break

                if selected == "Alignment Tongue":
                    lang_noun = alignment_map.get(str(self.alignment), "Chaos")
                    selected = f"{lang_noun}"

                if selected not in self.languages:
                    self.languages.append(selected)
                    break
                else:
                    continue

    def roll_starting_equipment(self):
        with open("starting_equipment.json", "r") as f:
            items = json.load(f)

        choice = random.choice(items)
        item_name = choice["item"]

        if "options" in choice:
            sub_choice = random.choice(choice["options"])
            item_name = f"{item_name} ({sub_choice})"

        self.equipment.append(item_name)

    def roll_thaumaturgical_curio(self):
        with open("thaumaturgical_curios.json", "r") as f:
            curios = json.load(f)

        self.equipment.append(random.choice(curios)["item"])

    def roll_name(self):
        with open("names.json", "r") as f:
            names = json.load(f)

        roll = dice(1, 4)
        if roll <= 2:
            self.name = random.choice(names)
        elif roll == 3:
            first_name = random.choice(names)
            last_name = random.choice(names)
            self.name = f"{first_name} {last_name}"
        else:
            name = random.choice(names)
            place = random.choice(names)
            self.name = f"{name} of {place}"

    def generate_zero_level(self):
        self.roll_stats()
        self.roll_birth_augur()
        self.roll_hp()
        self.roll_occupation()
        self.roll_animus()
        self.vat_thing()
        self.roll_alignment()
        self.roll_languages()
        self.roll_starting_equipment()
        self.roll_thaumaturgical_curio()
        self.roll_name()


# Scan equipment for AC-boosting items
#
# Add random level 1 spell selection ofr casebook for Sage (58-59) occupation

if __name__ == "__main__":
    main()
