from combat.old.definitions import *

head = BodypartConstructor('head',   Slot.mask, Slot.helmet, vital=True)
torso = BodypartConstructor('torso', Slot.chest,Slot.amulet, vital=True)
arm = BodypartConstructor('arm',     Slot.arm)
hand = BodypartConstructor('hand',   Slot.hand, Slot.glove, Slot.ring)
leg = BodypartConstructor('leg',     Slot.leg)
foot = BodypartConstructor('foot',   Slot.shoe)

Equipment('Good Helmet', Slot.helmet,
          base_cost=9, weight=5,
          stats={'armor':5,'health_regen':3})

Equipment('Crappy Helmet', Slot.helmet,
          base_cost=3, weight=4)

Equipment('Spooky Helmet',Slot.helmet,
          base_cost=3,weight=4)

Equipment('Big Axe', Slot.hand, Slot.hand,
          base_cost=2.7,weight=2,
          attack=Attack(attack_type.melee,reach.short,damage_type.slash,skill_bonus=2))

Equipment('Shield', Slot.hand, Slot.arm, Slot.amulet,
          base_cost=2.7,weight=2,
          attack=Attack(attack_type.melee,reach.short,damage_type.slash,skill_bonus=2))

humanoid = torso(
            head(),
            arm(hand()),
            arm(hand()),
            leg(foot()),
            leg(foot()))

ogre = head(head())

goblin = Race(humanoid, intelligence=2, wisdom=1, strength=4, dexterity=5)

ogre.inventory = [equipment['Good Helmet'], equipment['Crappy Helmet'], equipment['Good Helmet']]

ogre.display()
print(ogre.equip(equipment['Good Helmet']))
ogre.display()
print(ogre.equip(equipment['Crappy Helmet']))
ogre.display()
print(ogre.remove(equipment['Good Helmet']))
ogre.display()

