from mapgen.dig import Digger

a = Digger(70,30)
a.dig_floor(40)
print(a)
# print(sum(a.floor)/2)
print(a.roomcount)