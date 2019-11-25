from mapgen.dig import Digger

a = Digger(70,35)
a.dig_floor(50)
print(a)
print(a.floor.size/2)
print(a.roomcount)