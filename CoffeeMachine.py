class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550
        self.status = 'choosing an action'
        self.off = False
        self.filledsources = 0 
        self.res_list = ['ml of water', 'ml of milk', 'grams of coffee beans', 'disposable cups of coffee']
       
    def currentstate(self):
        print('The coffee machine has:\n{} of water\n{} of milk\n{} of coffee beans\n{} of disposable cups\n${} of money'.format(self.water, self.milk, self.beans, self.cups, self.money))

    def check_resources(self, w, m, b):
        if self.cups == 0:
            print('Sorry, not enough cups!')
            return False
        else:    
            if ((self.water - w < 0) or (self.beans - b < 0) or (self.milk - m < 0)):  
                if self.water - w < 0:
                    print('Sorry, not enough water!')
                elif self.beans - b < 0:    
                    print('Sorry, not enough coffee beans!')
                elif self.milk - m < 0:
                    print('Sorry, not enough milk!')
                return False
            else:    
                print('I have enough resources, making you a coffee!')
                return True

    def taking(self):
        print('I gave you $' + str(self.money))
        self.money = 0
    
    def buying(self, action):
        if action == "1":
            if self.check_resources(250, 0, 16):
                self.water -= 250
                self.beans -= 16
                self.cups -= 1
                self.money += 4 
        elif action == "2":
            if self.check_resources(350, 75, 20):
                self.water -= 350 
                self.milk -= 75
                self.beans -= 20
                self.cups -= 1
                self.money += 7 
        elif action == "3":        
            if self.check_resources(200, 100, 12):
                self.water -= 200 
                self.milk -= 100
                self.beans -= 12
                self.cups -= 1
                self.money += 6 
        self.status = 'choosing an action'        
                
    def useraction(self, action):
        if self.status == 'choosing an action':
            if action == 'remaining':
                self.currentstate()
            elif action == 'buy':
                self.status = 'choosing a type of coffee'
            elif action == 'fill':
                self.status = 'filling'
                self.filledsources = 0
            elif action == 'take':
                self.taking()
            else:
                self.off = True
        elif self.status == 'choosing a type of coffee':
            if action != 'back':
                self.buying(action)
            self.status = 'choosing an action'
        else:
            if self.filledsources == 0:
                self.water += int(action)
                self.filledsources += 1
            elif self.filledsources == 1:
                self.milk += int(action)
                self.filledsources += 1
            elif self.filledsources == 2:
                self.beans += int(action)
                self.filledsources += 1
            elif self.filledsources == 3:
                self.cups += int(action)
                self.status = 'choosing an action'
                    
machine = CoffeeMachine()
while True:
    if machine.status == 'choosing an action':
        machine.useraction(input('Write action (buy, fill, take, remaining, exit):'))
        if machine.off:
            break
    elif machine.status == 'choosing a type of coffee':
        machine.useraction(input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:'))
    elif machine.status == 'filling':
        for source in machine.res_list:
            machine.useraction(input('Write how many {} do you want to add:'.format(source)))
    else:
        break
