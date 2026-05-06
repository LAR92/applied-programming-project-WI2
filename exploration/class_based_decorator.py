from icecream import ic  
import time 
from pprint import pprint 


#class based decorator example for teaching purpo
class Call_Counter: 
    def _init_ (self, func): 
        self.func = func
        self.count = 0 
    def _call_ (self, *arg, **kwargs): 
        self.count += 1 #Bezug auf das Objekt selbst
        print (f"[Call_Counter]  {self.func. _name_} has been called {self.count} times.")
        print (f"[Call_Counter] Arguments: args= {arg}, kwargs ={kwargs}")
        return self.func(*arg, **kwargs) 

class Cache: #temporärer schneller Zwischenspeicher 

    def _init_ (self, func): 
        self.func = func
        self.history = []
        self.cache = {}
        ic("init")


    def _call_ (self, *args, **kwargs): 
        ic("call")
        key = (args, frozenset(kwargs.items()))
        ic(kwargs.items())
        ic(frozenset(kwargs.items()))
        ic(list(frozenset(kwargs.items())))
        ic(key) 
        if key in self.cache: 
            self.history.append(("cache", args, kwargs, self.cache[key]))
            return self.cache[key]
        
        else: 
            result = self.func(*args, **kwargs)
            self.cache[key] = result
            self.history.append(("calc", args, kwargs, result))
            return result
    
        
@Cache
def complicated_calculation(x, comment = "no comment"): 
    print (f"Performing complicated calculation for {x}...")
    time.sleep(2)  # Simulate a time-consuming calculation
    return x * x 


@Cache
def complicated_calculation_2(x, comment = "no comment"): 
    print (f"Performing complicated calculation 2 for {x}...")
    time.sleep(2)  # Simulate a time-consuming calculation
    return x + x 


result = complicated_calculation(5)
print (f"Result: {result}")

result = complicated_calculation(6)
print (f"Result: {result}")
result = complicated_calculation(7)
print (f"Result: {result}")
result = complicated_calculation(5)
print (f"Result: {result}")
result = complicated_calculation(6)
print (f"Result: {result}")
result = complicated_calculation(7)
print (f"Result: {result}")
result = complicated_calculation(8)
print (f"Result: {result}")

result = complicated_calculation(10)
print (f"Result: {result}")

result = complicated_calculation_2(50)
print (f"Result: {result}")

result = complicated_calculation_2(100)
print (f"Result: {result}")

print (f"History: ")
pprint (complicated_calculation.history)
pprint (complicated_calculation.cache)
print (f"History 2: ")
pprint (complicated_calculation_2.history)



#example usage 
if False and _name_ == "_main_": 
    @Call_Counter
    def greet(name:str, greeting:str = "Hello"): 
        print (f"{greeting}, {name}!")

    greet ("Alice", greeting = "Hi") 
    greet ("Bob")
    greet ("Charlie", greeting = "Tschüssi") 
    print (f"Total calls: {greet.count}")