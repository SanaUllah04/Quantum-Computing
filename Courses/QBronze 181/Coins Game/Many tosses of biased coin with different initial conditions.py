# define iterations as a list
iterations = [20,30,50]

# define initial probability pairs as a double list
initial_probabilities =[    
    [1/2,1/2],
    [0,1]
]


for initial_probability_pair in initial_probabilities: 
    print("probability of head is",initial_probability_pair[0])
    print("probability of tail is",initial_probability_pair[1])
    print()

    for iteration in iterations:

        # initial probabilites
        [prob_head,prob_tail] = initial_probability_pair
        
        print("the number of iterations is",iteration)
        
        for i in range(iteration):
             # the new probability of head is calculated by using the first row of table
            new_prob_head = prob_head * 0.6 + prob_tail * 0.3

            # the new probability of tail is calculated by using the second row of table
            new_prob_tail = prob_head * 0.4 + prob_tail * 0.7

            # update the probabilities
            prob_head = new_prob_head
            prob_tail = new_prob_tail

        # print prob_head and prob_tail
        print("the probability of getting head after",iteration,"coin tosses is",prob_head)
        print("the probability of getting tail after",iteration,"coin tosses is",prob_tail)
        print()
    print()