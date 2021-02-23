import math
print('''What do you want to calculate?
type "n" for number of monthly payments,
type "a" for annuity monthly payment amount,
type "p" for loan principal:''')
whats_todo = input()
if whats_todo == "n":
    print("Enter the loan principal:")
    loan = int(input())
    print("Enter the monthly payment:")
    payment = float(input())
    print("Enter the loan interest:")
    interest = float(input())
    rate = interest / 1200
    months = math.ceil(math.log(payment / (payment - rate * loan), 1 + rate))
    years = months // 12
    mont = months % 12
    if years == 0:
        print(f'It will take {mont} months to repay this loan!')
    elif mont == 0:
        print(f'It will take {years} years to repay this loan!')    
    else:
        print(f'It will take {years} years and {mont} months to repay this loan!')    
elif whats_todo == 'a':
    print("Enter the loan principal:")
    loan = int(input())
    print("Enter the number of periods:")
    periods = int(input())
    print("Enter the loan interest:")
    interest = float(input())
    rate = interest / 1200
    payment = math.ceil(loan * (rate * (1 + rate) ** periods / ((1 + rate) ** periods - 1)))
    print(f'Your monthly payment = {payment}!')     
else:
    print("Enter the annuity payment:")
    payment = float(input())
    print("Enter the number of periods:")
    periods = int(input())
    print("Enter the loan interest:")
    interest = float(input())
    rate = interest / 1200
    loan = math.floor(payment / (rate * (1 + rate) ** periods / ((1 + rate) ** periods - 1))) 
    print(f'Your loan principal = {loan}!')
