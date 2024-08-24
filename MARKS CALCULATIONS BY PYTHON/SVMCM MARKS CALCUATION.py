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