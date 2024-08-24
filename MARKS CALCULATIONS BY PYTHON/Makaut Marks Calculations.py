def menu():
    print()
    print("****MAKAUT MARKS CALCULATIONS****")
    print()
    print("1. Calculate Total Marks & Percentage(%) for Scholarship")
    print("2. Calculate SGPA/YGPA/DGPA to Percentage(%)")
    print("3. Calculate SGPA to YGPA")
    print("0. Exit the program")
menu()
print()
option=int(input("Enter your above required option : "))

while option !=0:   
    if option==1:
        a=float(input("Enter your odd sem SGPA : "))
        b=((a*10)-7.5)
        print("Percentage of odd sem is :",b,"%")
        c=float(input("Enter your even sem SGPA : "))
        d=((c*10)-7.5)
        print("Percentage of even sem is :",d,"%")
        e=((a+c)/2)
        print("Your one year YGPA is :",e)
        g=int(input("Enter the no. of odd sem subject : "))
        h=int(input("Enter the no. of even sem subject : "))
        g=g*100
        print("Total marks of odd sem is : ",g)
        h=h*100
        print("Total marks of even sem is : ",h)
        i=g+h
        print("Total marks of a year is : ",i)
        j=(b*g)/100
        print("Total obtained marks of odd sem is : ",j)
        k=(d*h)/100
        print("Total obtained marks of even sem is : ",k)
        l=j+k
        print("Total obtained marks of a year is : ",l)
        f=((l*100)/i)
        print("Your one year percentage is :",f,"%")

    elif option==2:
        a1=float(input("Enter your SGPA/YGPA/DGPA : "))
        b=((a1*10)-7.5)
        print("Percentage of SGPA/YGPA/DGPA is :",b,"%")

    elif option==3:
        a2=float(input("Enter your odd sem SGPA : "))
        b=((a2*10)-7.5)
        print("Percentage of odd sem is :",b,"%")
        c1=float(input("Enter your even sem SGPA : "))
        d=((c1*10)-7.5)
        print("Percentage of even sem is :",d,"%")
        e=((a2+c1)/2)
        print("Your one year YGPA is :",e)
        f=((e*10)-7.5)
        print("Your one year percentage is :",f,"%")

    else:
        print("Please Enter Correct Options")

    print()
    menu()
    print()
    option=int(input("Enter your above required option : "))
print("Thanks for using this program..Goodbye.")
