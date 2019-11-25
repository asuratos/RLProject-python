from mapgen.dig import Digger

a = Digger(50,30)
a.dig_floor(40)
print(a)
print(a.floor.size/2)
print(a.roomcount)