s = "ADOBECODEBANC"
t = "ABCAZ"

map = [0]*128

for char in t:
    map[ord(char)] +=1

print(map)
print(ord('K'))