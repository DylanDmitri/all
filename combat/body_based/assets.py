from combat.body_based.body import *

class HorrorTorso(BodyPart):
    def init(self):
        self.heart = internals.heart

    def slice(self,severity):
        if random() < .1 * (severity-3):
            self.heart.damage(severity-2)

    def crush(self,severity):
        pass

    def stab(self, severity):

        if severity > 2:
            add_condition(self,conditions.impaled)

        print(.1 * (severity-1))
        if random() < .1 * (severity-1):
            print('heart')
            self.heart.damage(severity)

    def update(self):

        self.heart.missinghealth = 10 - self.heart.hp
        self.bleeding *= (1 + self.heart.missinghealth/5)


class GoblinTorso(BodyPart):
    def init(self):
        self.heart = internals.heart
        self.ribcage = internals.bone
        self.lungs = internals.lungs
        self.intestines = internals.intestines

    def update(self):
        if not self.heart.functional:
            self.bleeding += 10


class GoblinHead(BodyPart):
    def init(self):
        self.lefteye = internals.eye
        self.righteye = internals.eye
        self.mouth = internals.mouth

class GoblinHand(BodyPart):
    def init(self):
        self.fingers = internals.finger
        self.fingers.number = 5

class GoblinFoot(BodyPart):
    def init(self):
        pass





creepy = Creature(HorrorTorso(Limb(), Limb(), GoblinHead()))

body = creepy.base_part
body.hitpoints = 100

while True:
    print('hp -', body.hitpoints)
    print('blood -', creepy.blood)
    print('heart -', body.heart.hp, body.heart.functional)
    damage = int(input(': ') or 0)
    if damage: body.take_damage(damage, dmgType.stab)
    creepy.update()
    print()

