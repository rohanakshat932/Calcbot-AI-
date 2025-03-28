    #Maths Problem


print("Hello my name is Calcbot AI,I am here to help you to solve your maths problems")
print("Here is an simple guide to use me")
print("So if you want me to do- \n addition just use this symbol + \n for subtraction use this - \n for multiplication use this * \n for divison use this /\n for exponent or power use this **\n for remainder use this %")
problem = input("Enter your Maths problem or press 'E' to exit")
while(problem!= "E"):
    print("The answer to", problem, "is:", eval(problem))
    problem = input("Enter another problem, or press 'E' to exit:")
