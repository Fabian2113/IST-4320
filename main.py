import tkinter as tk
from tkinter import ttk
import random

#main window setup
main = tk.Tk()
main.title("Dragon Ball Battles!!!!!")

#choices
hero = tk.StringVar()
villain = tk.StringVar()
attack_choice = tk.StringVar()  #variables stores attack choice

#health for heroes
hero_health = {'Goku': 100, 'Vegeta': 100, 'Gohan': 100, 'Piccolo': 90, 'Krillin': 70, 'Tien Shinhan': 80,
               'Master Roshi': 60, 'Trunks': 90, 'Goten': 70, 'Other(Specify)': 90}

villain_health = {'Frieza': 120, 'Cell': 150, 'Super Buu': 140, 'Kid Buu': 130, 'Zamasu': 110,
                  'Goku Black': 110, 'Moro': 150, 'Gas': 120, 'Other(type here)': 100}

#user attack damage numbers
hero_attack_damage = {'Punch': 15, 'Ki Blast': 25,  'Kick': 20, 'Super Attack': 30}

#villain random attack range
villain_attack_damage = {'Fists': (5, 10), 'Ki Blast': (10, 18), 'Kick': (8, 12)}

block_tracker = False  #tracks block is selected
user_heal_count = 0  #variable counter for Ki healing
villain_heal_count = 0  #counter for villain healing


#create hero label and combobox drop-down question
hero_label = tk.Label(main, text = "Select your Dragon Ball Hero to Fight! 🐉",
                       font = ('Times New Roman', 12, 'normal'))
hero_pick = ttk.Combobox(main, width=27, textvariable=hero)
hero_pick['values'] = (
 'Select Hero', 'Goku', 'Vegeta', 'Gohan', 'Piccolo', 'Krillin', 'Tien Shinhan', 'Master Roshi', 'Trunks', 'Goten', 'Other(Specify)')
hero_pick.set('Select Hero')  #default value so there is no blank space in option box for Hero


#create label as well as comboxbox for villains
villain_label = tk.Label(main, text="Choose your Dragon Ball Villain to Battle!!", font=('Times New Roman', 12, 'normal'))
villain_pick = ttk.Combobox(main, width=27, textvariable=villain)
villain_pick['values'] = (
 'Select the Villain', 'Frieza', 'Cell', 'Super Buu', 'Kid Buu', 'Zamasu', 'Goku Black', 'Moro', 'Gas', 'Other(type here)')
villain_pick.set('Select Villain')  #default value for villains to remove white space


#initialize health for heroes and villains
hero_hp = 0
villain_hp = 0


#battle state
battle_status = tk.Label(main, text="Select a Dragon Ball Hero and Villain to battle",
                     font=('Times New Roman', 12, 'normal'))


#function to start battle and display health values
def start_battle():
 global hero_hp, villain_hp, user_heal_count, villain_heal_count   #global allows variables to be accessible throughout
                                                                   #the entire program, had to be done to connect functions to one another efficently

 #set health based on chosen character and villain
 DB_hero = hero_pick.get()
 DB_villain = villain_pick.get()


 if DB_hero == 'Select Hero' or DB_villain == 'Select Villain':
     battle_status.config(text="Please select both a Hero and a Villain to start the battle!")
     return


 hero_hp = hero_health[DB_hero]
 villain_hp = villain_health[DB_villain]

 #resets ki heal count
 user_heal_count = 0
 villain_heal_count = 0


 #displays beginning health values stated earlier based off the character
 battle_status.config(text=f"{DB_hero}'s health: {hero_hp}\n{DB_villain}'s health: {villain_hp}")
 attack_frame.pack()  #show drop-down attack types
 start_button.pack_forget()  #start button once simulation begins

 attack_choice.set('Punch')  #default attack set to remove blank white space in drop-down box

#processes attack logic from user and opponent
def attack_logic():
 global hero_hp, villain_hp, block_tracker, user_heal_count, villain_heal_count


 #get player's choice of attack
 user_attack = attack_choice.get()

 if user_attack in hero_attack_damage:
     player_attack = hero_attack_damage[user_attack]

     #villain random attacks
     villain_attack_type = random.choice(list(villain_attack_damage.keys()))
     villain_attack_range = villain_attack_damage[villain_attack_type]
     villain_damage = random.randint(villain_attack_range[0], villain_attack_range[1])


     #applies block defense when button is clicked
     if block_tracker:
         player_block_damage = int(villain_damage * 0.6)  #blocks percentage of villain's damage
         villain_damage -= player_block_damage  #reduce damage from opponent


         #subtracts blocked damage from player health
         hero_hp -= player_block_damage

         #blocked damage information being displayed
         battle_status.config(text=f"You blocked {player_block_damage} damage from the villain's attack!\n\n"
                                  f"{hero_pick.get()}'s health: {max(hero_hp, 0)}\n"
                                  f"{villain_pick.get()}'s health: {max(villain_hp, 0)}")
         reset_attack()  #reset attack choice
         return


     #calculation for damage done to user or oppoonent
     villain_hp -= player_attack
     hero_hp -= villain_damage

     #villain heal randomly (done only a few times to make it more difficult for user )
     if villain_heal_count < 4 and random.random() < 0.5:  #50% chance of healing
         villain_heal()  #calls function


     #updates battle state with visible attacks
     battle_status.config(text=f"Player's Attack: {user_attack} dealt {player_attack} damage!\n"
                              f"Villain's Attack: {villain_attack_type} dealt {villain_damage} damage!\n"
                              f"{hero_pick.get()}'s health: {max(hero_hp, 0)}\n"
                              f"{villain_pick.get()}'s health: {max(villain_hp, 0)}")


     #checks for winner in battle
     if hero_hp <= 0:
         battle_status.config(text=f"{hero_pick.get()} has been defeated!\n{villain_pick.get()} wins!")
         attack_frame.pack_forget()  #hides attack combo box once fight ends
         play_again()  #shows play again button
     elif villain_hp <= 0:
         battle_status.config(text=f"{villain_pick.get()} has been defeated!\n{hero_pick.get()} wins!")
         attack_frame.pack_forget()  #hides attack combo box
         play_again()  #shows play again button

     #resets attack choice for next round
     reset_attack()


#block logic function
def block_defense():
 global block_tracker   #can be accessed outside of function
 block_tracker = True
 attack_logic()  #processes defense from user


def reset_attack():  #resets to default attack
 global block_tracker       #can be accessed outside of function
 block_tracker = False
 attack_choice.set('Punch')   #default is punch


#ki healing logic
def ki_heal():
 global hero_hp, user_heal_count
 #minimizes ki heal ability to 5
 if user_heal_count >= 5:
     battle_status.config(text="Energy is running low! You can no longer heal! Be careful!!!")
     return

 hero_hp += 50         #heal player by 50 health points
 #ensures that health doesn't exceed the default max health for each hero
 max_health = hero_health[hero_pick.get()]
 if hero_hp > max_health:
     hero_hp = max_health
 user_heal_count += 1  #increase the ki heal count by 1 (continues to 5)

 #update battle state after hero heals themselves for bother characters in the battle
 battle_status.config(text=f"Ki Heal used! {hero_pick.get()}'s health: {hero_hp}\n"
                          f"{villain_pick.get()}'s health: {villain_hp}")

 #villain able to attack after healing to make it more challenging for player
 villain_attack()

#villain's attack function
def villain_attack():
 global hero_hp, villain_hp   #allows for variables to be used elsewhere in the program

 #random attacks for villains
 villain_attack_type = random.choice(list(villain_attack_damage.keys()))
 villain_attack_range = villain_attack_damage[villain_attack_type]
 villain_damage = random.randint(villain_attack_range[0], villain_attack_range[1])

 hero_hp -= villain_damage  #subtract damage from player to keep track of their health throughout the battle

 #updates battle status for the villain as well as hero
 battle_status.config(text=f"Villain's Attack: {villain_attack_type} dealt {villain_damage} damage!\n"
                          f"{hero_pick.get()}'s health: {max(hero_hp, 0)}\n"
                          f"{villain_pick.get()}'s health: {max(villain_hp, 0)}")

#villain healing function to add health
def villain_heal():
 global villain_hp, villain_heal_count
 villain_hp += 30  #adds HP points to total health
 villain_heal_count += 1  #amount of times enemy has healed


 #updates battle status when villain heals randomly for user and villain :(
 battle_status.config(text=f"{villain_pick.get()} used healing! {villain_pick.get()}'s health: {villain_hp}\n"
                          f"{hero_pick.get()}'s health: {hero_hp}")

#play again button
def play_again():
 global play_again_button  # Ensure the button is globally accessible
 play_again_button = tk.Button(main, text="Play Again", command=reset_game, font=('Arial', 14), width=15, height=2)
 play_again_button.pack()


#resets game hero and villain status for user to try once more with different characters if they choose
def reset_game():
 global hero_hp, villain_hp, user_heal_count, villain_heal_count, play_again_button
 hero_hp = 0
 villain_hp = 0
 user_heal_count = 0
 villain_heal_count = 0

 #reset labels and program
 battle_status.config(text="Select a Hero and Villain to start the battle!!!!")
 attack_frame.pack_forget()  #hides attack drop-down once the game ends and resets
 start_button.pack()  # reveal start button once game is restarted

 #removes "Play Again" button once used to appear more organized
 play_again_button.pack_forget()


#layout of boxes and labels
hero_label.pack(padx=20, pady=10)
hero_pick.pack(padx=20, pady=10)
villain_label.pack(padx=20, pady=10)  #don't forget to pack
villain_pick.pack(padx=20, pady=10)

#start button box
start_button = tk.Button(main, text="Start Battle", command=start_battle, font=('Arial', 14), width=15, height=2)
start_button.pack(pady=20)

battle_status.pack(padx=20, pady=20)   #makes display cleaner

#contains attack combo box
attack_frame = tk.Frame(main)

#adding options to dropdown
attack_label = tk.Label(attack_frame, text="Select an attack:", font=('Times New Roman', 12, 'normal'))
attack_pick = ttk.Combobox(attack_frame, width=20, textvariable=attack_choice)
attack_pick['values'] = ['Punch', 'Ki Blast', 'Kick', 'Super Attack']

#smaller buttons with the same font size
attack_button = tk.Button(attack_frame, text="Attack", command=attack_logic, font=('Arial', 14), width=15, height=2)
block_button = tk.Button(attack_frame, text="Block", command=block_defense, font=('Arial', 14), width=15, height=2)
ki_heal_button = tk.Button(attack_frame, text="Ki Heal", command=ki_heal, font=('Arial', 14), width=15, height=2)

#layout for buttons
attack_label.grid(row=0, column=0, padx=10, pady=10)
attack_pick.grid(row=0, column=1, padx=10, pady=10)
attack_button.grid(row=1, column=0, padx=10, pady=5)
block_button.grid(row=1, column=1, padx=10, pady=5)
ki_heal_button.grid(row=1, column=2, padx=10, pady=5)

#main
main.mainloop()

