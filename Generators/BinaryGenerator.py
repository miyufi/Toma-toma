import pandas as pd
import itertools

test = int(input("Test: "))
ary = []
unwanted = {",", " ", "'", "(", ")"}
for n in range(1, test):
    lst = list(map(str, itertools.product([0, 1], repeat = n)))
    ary.extend(lst)
    
# ary = [x.strip("/(/)") for x in ary]

for n in range(len(ary)):
    temp = list(ary[n])
    temp = [un for un in temp if un not in unwanted]
    temp = "".join(temp)
    ary[n] = temp
    
df = pd.DataFrame(ary)
df.to_csv("Binary.csv", index = False)
# ary = ",".join(ary)
#print(ary)