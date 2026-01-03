import random
from classes.game import Person,bcolours
from classes.magic import Spell
from classes.inventory import Item

# create black magic
fire=Spell("Fire",10,600,"black")
thunder=Spell("Thunder",10,600,"black")
blizzard=Spell("Blizzard",10,600,"black")
meteor=Spell("Meteor",20,1200,"black")
quake=Spell("Quake",14,200,"black")

# create white magic
cure=Spell("Cure",25,500,"white")
cura=Spell("Cura",32,1000,"white")

# create items
potion=Item("Potion","potion","Heals 200HP",200)
hipotion=Item("Hi-Potion","potion","Heals 500HP",500)
superpotion=Item("Super Potion","potion","Heals 1000HP",1000)
elixer=Item("Elixer","elixer","Fully restores HP/MP of one party member.",9999)
hielixer=Item("MegaElixer","elixer","Fully restores party's HP/MP ",9999)

grenade=Item("Grenade","attack","Deals 500 damage",500)

player_spells=[fire,thunder,blizzard,meteor,quake,cure,cura]
enemy_spells=[fire,thunder,blizzard,meteor,quake,cure,cura]

player_items=[{"item":potion,"quantity":10},{"item":hipotion,"quantity":5},{"item":superpotion,"quantity":2},{"item":elixer,"quantity":5},{"item":hielixer,"quantity":2},{"item":grenade,"quantity":7}]

def create_player(name):
    hp=int(input(f"Enter HP for {name}: "))
    mp=int(input(f"Enter MP for {name}: "))
    atk=int(input(f"Enter ATK for {name}: "))
    df=int(input(f"Enter DEF for {name}: "))
    return Person(name,hp,mp,atk,df,player_spells,player_items)

def create_enemy(name):
    hp=int(input(f"Enter HP for {name}: "))
    mp=int(input(f"Enter MP for {name}: "))
    atk=int(input(f"Enter ATK for {name}: "))
    df=int(input(f"Enter DEF for {name}: "))
    return Person(name,hp,mp,atk,df,enemy_spells,[])

players=[create_player("Player1"),create_player("Player2"),create_player("Player3")]
enemies=[create_enemy("Enemy1"),create_enemy("Enemy2"),create_enemy("Enemy3")]

running=True
i=0
enemies_backup=enemies
players_backup=players

print(bcolours.FAIL + bcolours.BOLD + "AN ENEMY ATTACKS!"+bcolours.ENDC)

while running:
    print("=======================")

    print("\n\n")
    print("Name          HP                                        MP")
    for player in players:
        player.get_stats()

    print("\n")
    print("Name          HP                                        ")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        if len(enemies)==0:
            break
        if player.get_hp() == 0:
            continue
        enemy = player.choose_action()
        choice=input("    Choose action: ")
        index=int(choice) - 1

        if index==0:
            dmg=player.generate_damage()
            enemy=player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked "+ enemies[enemy].name +" for ",dmg,"points of damage .")

            if enemies[enemy].get_hp()==0:
                print(bcolours.OKGREEN+bcolours.BOLD+enemies[enemy].name.replace(" ","")+" has died"+bcolours.ENDC)
                del enemies[enemy]


        elif index==1:
            player.choose_magic()
            magic_choice=int(input("    Choose Magic: ")) - 1

            if magic_choice==-1:
                continue

            spell=player.magic[magic_choice]
            magic_dmg=spell.generate_damage()

            current_mp=player.get_mp()
            if spell.cost>current_mp:
                print(bcolours.FAIL+"\nNot Enough MP\n"+bcolours.ENDC)
                continue

            player.reduce_mp(spell.cost)
            
            if spell.type=="white":
                player.heal(magic_dmg)
                print(bcolours.OKBLUE+"\n"+spell.name+" heals for ",str(magic_dmg),"HP."+bcolours.ENDC)
            
            elif spell.type=="black":
                enemy=player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolours.OKBLUE+"\n"+spell.name+" deals",str(magic_dmg),"points of damage to "+ enemies[enemy].name +bcolours.ENDC)
                
                if enemies[enemy].get_hp()==0:
                    print(bcolours.OKGREEN+bcolours.BOLD+enemies[enemy].name.replace(" ","")+" has died"+bcolours.ENDC)
                    del enemies[enemy]


        elif index==2:
            player.choose_item()
            item_choice=int(input("Choose Item: ")) - 1

            if item_choice == -1:
                continue

            item=player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolours.FAIL+"\n"+"None left....."+bcolours.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type=="potion":
                player.heal(item.prop)
                print(bcolours.OKGREEN+"\n"+item.name+" heals for ",str(item.prop),"HP"+bcolours.ENDC)

            elif item.type=="elixer":
                if item.name=="MegaElixer":
                    for i in players:
                        i.hp=i.maxhp
                        i.mp=i.maxmp
                else:
                    player.hp=player.maxhp
                    player.mp=player.maxmp
                print(bcolours.OKGREEN+"\n"+item.name+" fully restores HP/MP "+bcolours.ENDC)
            
            elif item.type=="attack":
                enemy=player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolours.FAIL+"\n"+item.name+" deals ",str(item.prop)," points of damage to "+ enemies[enemy].name +bcolours.ENDC)
                if enemies[enemy].get_hp()==0:
                    print(bcolours.OKGREEN+bcolours.BOLD+enemies[enemy].name.replace(" ","")+" has died"+bcolours.ENDC)
                    del enemies[enemy]

    defeated_enemies=0
    defeated_players=0
    
    for enemy in enemies:
        if enemy.get_hp()==0:
            defeated_enemies+=1
    for player in players:
        if player.get_hp()==0:
            defeated_players+=1

    if defeated_enemies==len(enemies_backup):
        print(bcolours.OKGREEN+"YOU WIN!"+bcolours.ENDC)
        running=False
        break

    elif defeated_players==len(players_backup):
        print(bcolours.FAIL+"Your enemy has defeated you!"+bcolours.ENDC)
        running=False
        break

    for enemy in enemies:
        enemy_choice=random.randrange(0,2)

        if enemy_choice==0:
            target=random.randrange(len(players))
            enemy_dmg=enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ","")+" attacks "+ players[target].name.replace(" ","") +" for ",enemy_dmg)
        
        elif enemy_choice==1:
            spell,magic_dmg=enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type=="white":
                enemy.heal(magic_dmg)
                print(bcolours.OKBLUE+"\n"+spell.name+" heals "+ enemy.name +" for ",str(magic_dmg),"HP."+bcolours.ENDC)
            
            elif spell.type=="black":        
                target = random.randrange(0,3)
                players[target].take_damage(magic_dmg)

                print(bcolours.OKBLUE+"\n"+enemy.name.replace(" ","")+"'s "+spell.name+" deals",str(magic_dmg),"points of damage to "+ players[target].name +bcolours.ENDC)
                
                if players[target].get_hp()==0:
                    print(bcolours.OKGREEN+bcolours.BOLD+players[target].name.replace(" ","")+" has died"+bcolours.ENDC)
                    del players[target]
            print("Enemy chose ",spell.name, " damage is ", magic_dmg)
