my_list = [] 
n = int(input("Number of items you want to add? "))

for i in range(n):
    item = input(f"Enter item {i+1}: ")
    my_list.append(item)

print("Your list is:", my_list)
