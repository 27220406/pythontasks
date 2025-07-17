# Age Classification Program

# Ask the user to enter their age
age = int(input("Enter your age: "))

# Use if-elif-else to classify the age group
if age < 13:
    print("You are a Child.")
elif age >= 13 and age <= 19:
    print("You are a Teenager.")
elif age >= 20 and age <= 59:
    print("You are an Adult.")
else:
    print("You are a Senior.")
