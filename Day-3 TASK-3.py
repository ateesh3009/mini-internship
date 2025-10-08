#TASK-1

number=int(input("Enter Your Number"))
if number % 2 == 0:
    print("The Number is Even")
else:
        print("The Number is Odd")


#TASK-2
number=int(input("Enter Your Number:"))
if(number >=18):
    print("You can Vote")
else:
    print("you can't Vote")


#TASK-3
number=int(input("Enter Your Number"))
if(number % 3==0 and number % 5==0):
    print("fizz and buzz")
elif(number % 3 ==0):
    print("The Number is fizz")
elif(number % 5 ==0):
    print("The Number is buzz")
else:
    print("The Number is not divisble")
