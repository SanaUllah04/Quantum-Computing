from random import randrange

for experiment in [100,1000,10000,100000]:
    
    heads = tails = 0

    # Perform coin flips for the number of times specified by experiment
    for i in range(experiment):
        
        # Generate a random number (0 or 1) to simulate a coin flip
        if randrange(2) == 0: heads = heads + 1  # Increment heads counter if result is 0
        else: tails = tails + 1                  # Increment tails counter if result is 1
    
    print("experiment:",experiment)
    print("heads =",heads,"  tails = ",tails)    
    print("the ratio of #heads/#tails is",(round(heads/tails,4)))
    print() 