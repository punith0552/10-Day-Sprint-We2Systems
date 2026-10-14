list_size=int(input("Enter the size of the list: "))
num_list=[]
for i in range(list_size):
    num=int(input("Enter number {}: ".format(i+1)))
    num_list.append(num)

a=set(num_list)

print("The unique numbers in the list are: ", a)