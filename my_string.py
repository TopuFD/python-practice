
# lopping in a string
name = "Topu"
for x in name:
    print(x)


# ===================================string length using (len())
a = "Banana"
print("This is the lenght :",len(a))

# ===================================find character is present in a string using (in, not in)
b = "i am a flutter developer"
c = "i am python guru"
resultIN = "flutter" in b
resultNot = "guruu" not in c
print("The carecter is in the sentence :",resultIN),
print("The carecter is in the sentence :",resultNot),


# ===================================slicing in string
fruit = "banana"
print("Slicing Fruit==>",fruit[0:2]),
print("Slicing Fruit==>",fruit[0:]),
print("Slicing Fruit==>",fruit[:6]),
print("Slicing Fruit==>",fruit[-6:-2]),
