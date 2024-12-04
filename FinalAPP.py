import tkinter as tk
from tkinter import ttk
import random


class Character:
    '''Contains character specific attributes'''

    def __init__(self, name, health, attack_damage):
        self.name = name
        self.health = health
        self.original_health = health  # Store the original health value
        self.attack_damage = attack_damage  # dictionary of the characters attacks and their dmg values
        self.abilities = []  # list of ability objects

    def attack(self, attack_choice):
        '''Returns the damage value based on the attack type'''
        return self.attack_damage.get(attack_choice, 0)

    def heal(self, amount):
        self.health += amount

    def take_damage(self, damage):
        """subtract damage from the character health"""
        self.health -= damage
        if self.health < 0:
            self.health = 0  # sets health to 0 below 0. Prevents negatives

    def add_ability(self, ability):
        '''
        A dictionary of abilities is passed and this function
        searches for the abilities belonging to this character
        '''
        self.abilities.append(ability)

    # def reset(self):
    #     '''Reset character health to its original value'''
    #     self.health = self.original_health  # Reset health to the original value


class Abilities:
    '''Used to handle character abilities and effects. Stores the effects of an ability'''

    def __init__(self, name, ability_type, damage, modifier):
        self.name = name  # ability name
        self.ability_type = ability_type  # either damage or transformation
        self.damage = damage  # stores ability modifier if damage
        self.modifier = modifier  # stores stat modifier if transformation

    # used to determine the type of ability being called and calls the apropriate function
    def activate_ability(self, hero, villain, villain_damage, villain_attack_choice):
        '''Handles any ability calls and calls the appropriate function based on the ability type'''
        if self.ability_type == 'damage':
            results = self.damage_ability(hero, villain, villain_damage, villain_attack_choice)
        else:
            results = self.transform(hero, villain, villain_damage, villain_attack_choice)

        return results

    # Process the damage ability and the resulting damage to villain
    def damage_ability(self, hero, villain, villain_damage, villain_attack_choice):
        '''Handles damage abilities'''
        # calculates damage
        hero.take_damage(villain_damage)
        villain.take_damage(self.damage)  # ability damage

        results = f"{hero.name} uses {self.name} and deals {self.damage} damage!!!\n{villain.name}'s Attack: {villain_attack_choice} dealt {villain_damage} damage!"
        return results

    # Augments the character attack_damage attributes based on the ability modifier
    def transform(self, hero, villain, villain_damage, villain_attack_choice):
        '''Handles character transformations'''
        # calculates damage
        hero.take_damage(villain_damage)

        for attack in list(hero.attack_damage.keys()):
            hero.attack_damage[attack] = hero.attack_damage[
                                             attack] * self.modifier  # adjusts the character stats according to the modifier
        hero.health = hero.original_health * self.modifier  # hero health is restored and adjusted by the modifier
        hero.original_health = hero.health  # updates the max health

        results = f"{hero.name} has transformed into {self.name} {hero.name}!!! {hero.name} feels invigorated as his strength surges!\n{villain.name}'s Attack: {villain_attack_choice} dealt {villain_damage} damage!"
        return results


# used to handle the various battle interactions that can occur
class Battle:
    '''Used to handle battle interactions'''

    def __init__(self, hero, villain):
        self.hero = hero
        self.villain = villain
        self.hero_heal_count = 0  # keeps track of hero heals
        self.villain_heal_count = 0  # keeps track of villain heals
        self.block_tracker = False  # tracks block usage

    def process_attack(self, hero_attack_choice):
        player_damage = self.hero.attack(
            hero_attack_choice or 0)  # returns an attack value for hero. Set to 0 for block attacks

        # villain attack logic
        villain_attack_choice = random.choice(
            list(self.villain.attack_damage.keys()))  # randomly chooses a villain attack
        pre_damage = self.villain.attack_damage.get(
            villain_attack_choice)  # stores the damage value of the chosen attack
        villain_damage = random.randint((pre_damage - 2), (pre_damage + 2))  # randomizes the damage

        # handles any blocking action
        if self.block_tracker or hero_attack_choice == None:
            original_damage = villain_damage  # stores the original villain damage before any block modifiers
            villain_damage -= int(original_damage * 0.6)  # reduce damage from opponent
            player_block_damage = int(original_damage - villain_damage)  # blocks reduce villain damage to 60%

            # damage to health calcaulation
            self.hero.take_damage(villain_damage)  # only villain attacks during blocks

            # resets block_tracker to false
            self.block_tracker = False

            # blocked damage information being displayed
            # battle_status.config(text=f"You blocked {player_block_damage} damage from the {self.villain.name}'s attack!")
            # f"{self.hero.name}'s health: {self.hero.health}\n"
            # f"{self.villain.name}'s health: {self.villain.health}")

            reset_attack()  # reset attack choice

            # checks for win in block actions
            if win_check():
                return None
            else:
                return player_block_damage, self.villain.name

        # Handles any heal actions
        if hero_attack_choice == 'Heal':
            self.hero.take_damage(villain_damage)
            if win_check():
                return None
            else:
                return f"{self.villain.name}'s Attack: {villain_attack_choice} dealt {villain_damage} damage!"

        # Handles ability logic during battle. hero_attack_choice will contain the name of the selected ability
        for ability in self.hero.abilities:
            if ability.name == hero_attack_choice:
                results = ability.activate_ability(self.hero, self.villain, villain_damage,
                                                   villain_attack_choice)  # calls function to appropriatly handle ability types and effects

                update_health(self.hero, self.villain)  # updates health after ability usage

                if win_check():
                    return 0
                else:
                    return results  # returns to attack_logic()return results

        # villain will have a 20% to heal 2 times on normal attacks
        if (self.villain_heal_count < 2) and (random.random() < 0.2):
            villain_heal()

        # damage to health calcaulation
        self.hero.take_damage(villain_damage)
        self.villain.take_damage(player_damage)

        # # checks for win
        if win_check():
            return None  # returns to attack_logic()

        return (f"{self.hero.name}'s Attack: {hero_attack_choice} dealt {player_damage} damage!\n"
                f"{self.villain.name}'s Attack: {villain_attack_choice} dealt {villain_damage} damage!")

    def process_heal(self):
        '''Handles hero healing actions'''
        if self.hero_heal_count < 5:  # ensures players only use no more than 5 heals
            self.hero.heal(50)
            if self.hero.original_health < self.hero.health:  # ensures health does not exceed original max
                self.hero.health = self.hero.health
            self.hero_heal_count += 1  # increment heal counter
            return f"{self.hero.name} healed for 50!"
        else:
            return "No more healing available!"

    def villain_heal_process(self):
        '''Handles villain healing'''
        if self.villain_heal_count < 2:  # only 2 villain heals per battle
            self.villain.heal(20)  # adds HP points to total health
            self.villain_heal_count += 1  # amount of times enemy has healed
            return f'{self.villain.name} healed for 30 '
        else:
            return f'{self.villain.name} tried to heal but couldn\'t 🎯'

    def block(self):
        self.block_tracker = True


# ---------------------------------------------------------------------------------------------------------------

# Battle state
battle = None


# initializes the battle state at the beginning of battle after Start button is pressed
def start_battle():
    global battle
    global hero_health_text
    global villain_health_text

    h_name = hero_name.get()
    v_name = villain_name.get()

    # checks to ensure a hero and villain is selected
    if h_name == 'Select Hero' or v_name == 'Select Villain':
        battle_status.config(text="Please select both a Hero and a Villain to start the battle!")
        return

    # battle setup
    hero = heroes[hero_name.get()]  # stores the associateed hero character object
    villain = villains[villain_name.get()]  # stores the villain associated character object
    battle = Battle(hero, villain)

    # implements hero abilities into the hero after selection
    inputs_char_abilities()

    # Overlay text for health values
    hero_health_text = canvas.create_text(100, 20, text=f"{h_name}: {battle.hero.health}/{battle.hero.original_health}",
                                          fill="white")
    villain_health_text = canvas.create_text(100, 50,
                                             text=f"{v_name}: {battle.villain.health}/{battle.villain.original_health}",
                                             fill="white")

    canvas.pack()

    # buttons
    attack_frame.pack()  # Show attack options
    start_button.pack_forget()  # Hide start button
    battle_status.configure(text='')


# Handle attack logic when attack button clicked
def attack_logic():
    if battle:
        result = battle.process_attack(stored_attack.get())
        update_health(battle.hero, battle.villain)
        if result:  # If result is not None

            battle_status.config(text=f"{result}")
            reset_attack()


# called whenever users click on Ki Heal button
def ki_heal():
    if battle:
        result = battle.process_heal()
        result2 = battle.process_attack('Heal')
        if result and result2:
            # battle_status.config(text=f"{result}\n{battle.hero.name}'s health: {hero_health}\n{battle.villain.name}'s health: {villain_health}")
            # processes rest of attack
            battle_status.config(text=f"{result}\n{result2}")

        update_health(battle.hero, battle.villain)


def block_defense():
    if battle:
        battle.block()  # sets the block flag to True
        result = battle.process_attack(None)  # processes rest of attack
        if result:
            player_block_damage, villain_name = result
            battle_status.config(text=f"You blocked {player_block_damage} damage from the {villain_name}'s attack!")

        update_health(battle.hero, battle.villain)


# villain can randomly heal during battle
def villain_heal():
    if battle:
        result = battle.villain_heal_process()
        battle_status.config(text=f"{result}\n")

        update_health(battle.hero, battle.villain)


# used to show available abilities on screen
def show_abilities():
    # Hides the onscreen widgets
    label_frame.pack_forget()
    attack_frame.pack_forget()
    battle_status.pack_forget()
    canvas.pack_forget()

    # Clear any existing buttons in the abilities frame
    for widget in abilities_frame.winfo_children():
        widget.destroy()

    # Dynamically create buttons for each ability
    hero_abilities = battle.hero.abilities
    for ability in hero_abilities:
        ability_buttons = tk.Button(abilities_frame, text=ability.name, font=('Times', 15),
                                    command=lambda a=ability: on_ability_click(
                                        a))  # Pressed abilities are then passed to on_ability_click
        ability_buttons.pack(pady=10, padx=10)  # displays the abilities on screen

    abilities_frame.pack(pady=10)  # shows the dedicated ability screen


# called whenever an ability is clicked on
def on_ability_click(ability):
    results = battle.process_attack(ability.name)  # processes the rest of the turn

    if results:  # if ability does no result in a win
        battle_status.config(text=results)

        # redisplay main screen
        label_frame.pack()
        battle_status.pack(padx=20, pady=20)
        canvas.pack()
        attack_frame.pack()

        abilities_frame.pack_forget()
    else:  # if ability wins on first move
        # redisplay main screen
        label_frame.pack()
        battle_status.pack(padx=20, pady=20)
        canvas.pack()

        reset_button.pack_forget()
        reset_button.pack(pady=20)
        abilities_frame.pack_forget()

    # used to check for wins after actions


def win_check():
    """Checks if there is a winner and updates the UI accordingly."""
    if battle.hero.health <= 0:  # Hero loses
        battle_status.config(text=f"{battle.hero.name} has been defeated.\n {battle.villain.name} wins.")
        attack_frame.pack_forget()  # Hide the attack options
        reset_button.pack(pady=20)
        return True
    elif battle.villain.health <= 0:  # Villain loses
        battle_status.config(text=f"{battle.villain.name} has been defeated!\n {battle.hero.name} wins!")
        attack_frame.pack_forget()  # Hide the attack options
        reset_button.pack(pady=20)
        return True

    return False  # no winner yet


def reset_attack():
    attack_pick.set('Punch')


# reset game state and bring back the original window
def reset_game():
    global battle
    # reset the battle object (discards the current battle state)
    battle = None

    # reset health and attack choices for both hero and villain
    hero_name.set('Select Hero')
    villain_name.set('Select Villain')
    stored_attack.set('Punch')  # reset attack choice to default

    # reset the battle status
    battle_status.config(text="Select a Dragon Ball Hero and Villain to battle")

    # reset the hero and villain attributes by calling their reset method
    global heroes, villains  # used to reset character attributes
    heroes, villains = create_characters()

    # hide attack options and reset UI
    attack_frame.pack_forget()
    start_button.pack(pady=20)  # Show the start button again

    # reset any additional UI or state
    hero_pick.set('Select Hero')
    villain_pick.set('Select Villain')

    # Hide the reset button after resetting the game
    reset_button.pack_forget()

    # clear and reset canvas
    global hero_health_rect, villain_health_rect, hero_health_text, villain_health_text  # used to reset the canvas

    canvas.delete("all")
    canvas.pack_forget()

    # Recreate health bar rectangles
    hero_health_rect = canvas.create_rectangle(10, 10, 340, 30, fill="green", outline="white")
    villain_health_rect = canvas.create_rectangle(10, 40, 340, 60, fill="green", outline="white")

    # Recreate text items
    hero_health_text = canvas.create_text(100, 20, text="", fill="white")
    villain_health_text = canvas.create_text(100, 50, text="", fill="white")


# creates all the heroes
def create_characters():
    heroes = {name: Character(*data) for name, data in {
        'Goku': ('Goku', 150, {'Punch': 15, 'Ki Blast': 20, 'Kick': 15, 'Super Attack': 30}),
        'Vegeta': ('Vegeta', 140, {'Punch': 20, 'Ki Blast': 25, 'Kick': 20, 'Super Attack': 30}),
        'Gohan': ('Gohan', 130, {'Punch': 13, 'Ki Blast': 22, 'Kick': 17, 'Super Attack': 30}),
        'Piccolo': ('Piccolo', 120, {'Punch': 17, 'Ki Blast': 20, 'Kick': 12, 'Super Attack': 30}),
        'Krillin': ('Krillin', 100, {'Punch': 10, 'Ki Blast': 15, 'Kick': 13, 'Super Attack': 30}),
        'Tien Shinhan': ('Tien Shinhan', 90, {'Punch': 15, 'Ki Blast': 25, 'Kick': 20, 'Super Attack': 30}),
        'Master Roshi': ('Master Roshi', 90, {'Punch': 15, 'Ki Blast': 25, 'Kick': 20, 'Super Attack': 30}),
        'Trunks': ('Trunks', 110, {'Punch': 15, 'Ki Blast': 25, 'Kick': 20, 'Super Attack': 30}),
        'Goten': ('Goten', 110, {'Punch': 15, 'Ki Blast': 25, 'Kick': 20, 'Super Attack': 30}),
        # Add more heroes here
    }.items()}

    # creates all the villains
    villains = {name: Character(*data) for name, data in {
        'Frieza': ('Frieza', 170, {'Fists': 35, 'Ki Blast': 40, 'Kick': 10}),
        'Cell': ('Cell', 180, {'Fists': 50, 'Ki Blast': 60, 'Kick': 35}),
        'Super Buu': ('Super Buu', 200, {'Fists': 90, 'Ki Blast': 65, 'Kick': 50}),
        'Kid Buu': ('Kid Buu', 250, {'Fists': 80, 'Ki Blast': 75, 'Kick': 70}),
        'Zamasu': ('Zamasu', 500, {'Fists': 80, 'Ki Blast': 90, 'Kick': 35}),
        'Goku Black': ('Goku Black', 500, {'Fists': 90, 'Ki Blast': 80, 'Kick': 35}),
        'Moro': ('Moro', 1200, {'Fists': 220, 'Ki Blast': 160, 'Kick': 60}),
        'Gas': ('Gas', 1500, {'Fists': 250, 'Ki Blast': 170, 'Kick': 75}),
        'Jiren': ('Jiren', 999, {'Fists': 200, 'Ki Blast': 150, 'Kick': 100}),
        # Add more villains here
    }.items()}

    return heroes, villains


# will set the appropriate abilities based on chosen character
def inputs_char_abilities():
    '''Creates an Ability class object for every ability that a character has.'''
    hero = battle.hero
    hero_abilities = character_abilities.get(hero.name)  # Get hero abilities from the dictionary

    # Loop through the abilities and create an Ability object for each
    for ability_name, ability_data in hero_abilities.items():
        ability_type, damage, modifier = ability_data
        ability_obj = Abilities(ability_name, ability_type, damage, modifier)

        # Dynamically assign the ability object to the character's abilities list
        hero.add_ability(ability_obj)
        setattr(hero, ability_name, ability_obj)  # This will add the ability as an attribute of the hero


# used to update health bars after actions
def update_health(hero_current, villain_current):
    # Update health values
    hero_health = hero_current.health
    villain_health = villain_current.health

    # Calculate new widths
    hero_width = (hero_health / hero_current.original_health)
    villain_width = (villain_health / villain_current.original_health)

    # Update the rectangles
    if hero_width <= 0 or villain_width <= 0:
        if hero_width <= 0:
            canvas.coords(hero_health_rect, 0, 0, 0, 0)
        else:
            canvas.coords(villain_health_rect, 0, 0, 0, 0)
    else:
        canvas.coords(hero_health_rect, 10, 10, 340 * hero_width, 30)
        canvas.coords(villain_health_rect, 10, 40, 340 * villain_width, 60)

    # Update the colors e5340ey
    hero_color = "green" if hero_health > (hero_current.original_health * .5) else "#ec933f" if hero_health > (
                hero_current.original_health * .3) else "#e5340e"
    villain_color = "green" if villain_health > (
                villain_current.original_health * .5) else "#ec933f" if villain_health > (
                villain_current.original_health * .3) else "#e5340e"

    canvas.itemconfig(hero_health_rect, fill=hero_color)
    canvas.itemconfig(villain_health_rect, fill=villain_color)

    # Update the text
    canvas.itemconfig(hero_health_text, text=f"{hero_current.name}: {hero_health}/{hero_current.original_health}")
    canvas.itemconfig(villain_health_text,
                      text=f"{villain_current.name}: {villain_health}/{villain_current.original_health}")


# a dictionary of all charcter abilities
character_abilities = {
    'Goku': {'Kamehameha': ('damage', 180, None),
             'Super Saiyan': ('transformation', 0, 4),
             'Perfected Ultra Instinct': ('transformation', 0, 15)},
    'Vegeta': {'Galik Gun': ('damage', 200, None),
               'Super Saiyan': ('transformation', 0, 4),
               'Ultra Ego': ('transformation', 0, 15)},
    'Gohan': {'Masenko': ('damage', 165, None),
              'Super Saiyan 2': ('transformation', 0, 6),
              'Beast ': ('transformation', 0, 15)},
    'Piccolo': {'Special Beam Cannon': ('damage', 140, None),
                'Orange Piccolo': ('transformation', 0, 15)},
    'Krillin': {'Destructo Disk': ('damage', 140, None),
                'Selflessness State': ('transformation', 0, 69)},
    'Tien Shinhan': {'Tri-Beam': ('damage', 60, None),
                     'Neo Tri-Beam': ('damage', 180, None)},
    'Master Roshi': {'The Original Kamehameha': ('damage', 180, None),
                     'Max Power': ('transformation', 0, 3)},
    'Trunks': {'Double Buster': ('damage', 120, None),
               'Super Saiyan 2': ('transformation', 0, 6)},
    'Goten': {'Kamehameha': ('damage', 150, None),
              'Super Saiyan 2': ('transformation', 0, 6)}
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------

# main window setup
main = tk.Tk()
main.title("Dragon Ball Battles!!!!!")

# character setup
heroes, villains = create_characters()  # create characters
hero_name = tk.StringVar()  # stores the selected hero name
villain_name = tk.StringVar()  # stores the selected villain name

# frame containing the labels and comboboxes
label_frame = tk.Frame(main)

# create hero label and combobox drop-down question
hero_label = tk.Label(label_frame, text="Select your Dragon Ball Hero to Fight! 🐉",
                      font=('Times New Roman', 12, 'normal'))
hero_pick = ttk.Combobox(label_frame, width=27, textvariable=hero_name, values=list(heroes.keys()))
hero_pick.set('Select Hero')  # default value for hero box

# create label as well as comboxbox for villains
villain_label = tk.Label(label_frame, text="Choose your Dragon Ball Villain to Battle!!",
                         font=('Times New Roman', 12, 'normal'))
villain_pick = ttk.Combobox(label_frame, width=27, textvariable=villain_name, values=list(villains.keys()))
villain_pick.set('Select Villain')  # default value for villain box

# layout of boxes and labels
hero_label.pack(padx=20, pady=10)
hero_pick.pack(padx=20, pady=10)
villain_label.pack(padx=20, pady=10)
villain_pick.pack(padx=20, pady=10)
label_frame.pack()  # displays the labels onto the mains screen

# Create a canvas for the health bars
canvas = tk.Canvas(main, width=350, height=70, bg="grey")

# Create health bar rectangles
hero_health_rect = canvas.create_rectangle(10, 10, 340, 30, fill="green", outline="white")
villain_health_rect = canvas.create_rectangle(10, 40, 340, 60, fill="green", outline="white")

# BELOW IS ALL RELATED TO BUTTONS
# start button box
start_button = tk.Button(main, text="Start Battle", command=start_battle, font=('Arial', 14), width=15,
                         height=2)  # NEED TGO ADD COMMAND
start_button.pack(pady=20)

# battle status display
battle_status = tk.Label(main, text="Select a Dragon Ball Hero and Villain to battle",
                         font=('Times New Roman', 12, 'normal'))
battle_status.pack(padx=20, pady=20)  # makes display cleaner

# contains attack combo box
attack_frame = tk.Frame(main)
attack_list = ['Punch', 'Ki Blast', 'Kick', 'Super Attack']  # choices for attacking
stored_attack = tk.StringVar()  # stores the user attack choice

# adding options to dropdown
attack_label = tk.Label(attack_frame, text="Select an attack:", font=('Times New Roman', 12, 'normal'))
attack_pick = ttk.Combobox(attack_frame, width=20, textvariable=stored_attack, values=attack_list)
attack_pick.set('Punch')  # deault attack choice

# UI Buttons for attack, block , and heal
attack_button = tk.Button(attack_frame, text="Attack", command=attack_logic, font=('Arial', 14), width=15, height=2)
block_button = tk.Button(attack_frame, text="Block", command=block_defense, font=('Arial', 14), width=15, height=2)
ki_heal_button = tk.Button(attack_frame, text="Ki Heal", command=ki_heal, font=('Arial', 14), width=15, height=2)
abilities_button = tk.Button(attack_frame, text='Abilities', command=show_abilities, font=('Arial', 14), width=15,
                             height=2)

# attack framelayout for buttons
attack_label.grid(row=0, column=0, padx=10, pady=10)
attack_pick.grid(row=0, column=1, padx=10, pady=10)
attack_button.grid(row=1, column=0, padx=10, pady=20)
block_button.grid(row=1, column=1, padx=10, pady=20)
ki_heal_button.grid(row=2, column=0, padx=10, pady=20)
abilities_button.grid(row=2, column=1, padx=10, pady=20)

# creates a dedicated frame for the ability window
abilities_frame = tk.Frame(main)

# Create the reset button
reset_button = tk.Button(main, text="Reset Game", command=reset_game, font=('Arial', 14), width=15, height=2)

# main
main.mainloop()