def data_analysis(input_data):
    print("Highest value:", max(input_data))
    print("Lowest value:", min(input_data))
    print("Sum of values:", sum(input_data))

data_list = []
size=int(input("Enter the size of the data: "))
for i in range(size):
    data = int(input("Enter data point {}: ".format(i + 1)))
    data_list.append(data)

data_analysis(data_list)