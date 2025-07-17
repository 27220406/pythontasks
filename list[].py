my_list = [] 
n = int(input("Number of items you want to add in list? "))

for i in range(n):
    item = int(input(f"Enter item {i+1}: "))  
    my_list.append(item)

print("Your list is:", my_list)
maximum = max(my_list)
minimum = min(my_list)
print("This is my max:", maximum)
print("This is my min:", minimum)
total = sum(my_list)
print("This is the total sum:", total)
