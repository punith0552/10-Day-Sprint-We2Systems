marks=int(input("Enter marks between 0 and 100 :"))

if(marks>90):
    print("A")
elif(marks>75):
    print("B")
elif(marks>50):
    print("C")
elif(marks<50):
    print("Fail")
else:
    print("Invalid marks")