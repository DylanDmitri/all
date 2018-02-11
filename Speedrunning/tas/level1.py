from tools import key_down, key_up, mouse_down, mouse_up
from time import sleep

sleep(3)
key_down('d')
sleep(.8)
key_down('w')
sleep(.2)
mouse_down(800, 340)
sleep(1)
key_up('d')
key_up('w')
mouse_up()

