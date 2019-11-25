from mapgen.dig import Digger

a = Digger(50,30)
a.dig_floor(30)
print(a)
# print(sum(a.floor)/2)
print(a.roomcount)