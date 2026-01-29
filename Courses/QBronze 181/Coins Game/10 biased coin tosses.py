# start with one euro,
#    and so, we assume that the probability of having head is 1 at the beginning.
prob_head = 1
prob_tail = 0


#
# first coin-flip
#

# the new probability of head is calculated by using the first row of table
new_prob_head = prob_head * 0.6 + prob_tail * 0.3

# the new probability of tail is calculated by using the second row of the table
new_prob_tail = prob_head * 0.4 + prob_tail * 0.7

# update the probabilities for the second round
prob_head = new_prob_head
prob_tail = new_prob_tail

#
# second coin-flip
#
# we do the same calculations

new_prob_head = prob_head * 0.6 + prob_tail * 0.3
new_prob_tail = prob_head * 0.4 + prob_tail * 0.7

prob_head = new_prob_head
prob_tail = new_prob_tail

#
# third coin-flip
#
# we do the same calculations

new_prob_head = prob_head * 0.6 + prob_tail * 0.3
new_prob_tail = prob_head * 0.4 + prob_tail * 0.7

prob_head = new_prob_head
prob_tail = new_prob_tail





# initial condition:
# start with one euro,
#    and so, we assume that the probability of having head is 1 at the beginning.
prob_head = 1
prob_tail = 0

number_of_iterations = 10

for i in range(number_of_iterations):
    # the new probability of head is calculated by using the first row of table
    new_prob_head = prob_head * 0.6 + prob_tail * 0.3

    # the new probability of tail is calculated by using the second row of table
    new_prob_tail = prob_head * 0.4 + prob_tail * 0.7

    # update the probabilities
    prob_head = new_prob_head
    prob_tail = new_prob_tail
    
# print prob_head and prob_tail
print("the probability of getting head after",number_of_iterations,"coin tosses is",prob_head)
print("the probability of getting tail after",number_of_iterations,"coin tosses is",prob_tail)