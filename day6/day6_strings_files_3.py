f=open("studnets.text","a+")

for i in range(3):
    name=input("Enter your name: ")
    f.write(name+"\n")  

f.close()