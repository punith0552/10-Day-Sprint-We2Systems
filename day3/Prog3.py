num1=float(input("Enter number_1 : "))
num2=float(input("Enter number_2 : "))

op=input("choose a operator(+,-,*,/) : ")

if(op =='+'):
    print(num1+num2)
elif(op =='-'):
    print(num1-num2)
elif(op =='*'):
    print(num1*num2)
elif(op == "/"):
    print(num1/num2)
else:
    print("wrong operator choosen")