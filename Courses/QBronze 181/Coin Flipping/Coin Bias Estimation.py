# Define a function that simulates a biased coin flip


from random import randrange

def biased_coin(N,B):
    
    # Generate a random number between 0 and N-1
    random_number = randrange(N)
    
    
    # Return "Heads" if random number is less than bias B, otherwise return "Tails"
    if random_number < B:
        return "Heads"
    else:
        return "Tails"


# Set the range for the bias (N = 101, so bias can be 0 to 100)
N = 101

# Generate a random bias value between 0 and N (inclusive)
B = randrange(N+1)


# total number of coin tosses
total_tosses = 500


# counter to track the number of heads observed
the_number_of_heads = 0

for i in range(total_tosses):


    # If the coin flip returns "Heads", increment the heads counter
    if biased_coin(N,B) == "Heads":
        the_number_of_heads = the_number_of_heads + 1


# Calculate the estimated bias based on observed heads ratio
my_guess =  the_number_of_heads/total_tosses   
real_bias = B/N
error = abs(my_guess-real_bias)/real_bias*100 


print("my guess is",my_guess)
print("real bias is",real_bias)
print("error (%) is",error)