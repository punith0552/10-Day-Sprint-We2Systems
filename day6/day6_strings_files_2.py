sentence=input("Enter a sentences: ")

count=0 

for i in range(len(sentence)):
    if sentence[i] in ['a','e','i','o','u']:
        count=count+1
    else:
        pass

print("The number of vowels in the sentence is:", count )