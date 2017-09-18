import numpy as np
from scipy.stats import truncnorm
import pandas as pd
import matplotlib.pyplot as plt

n_innovations = 10
innovation_pool = range(n_innovations)
innovation_performances = truncnorm.rvs(0,1, size=n_innovations)  # called 'V'

consideration_interval = 10  # called "M"
# When fewer than `consideration_interval` rounds have elapsed, 
# use the full number of rounds in assessing confidence

lam = .25
# We employ a free parameter lambda(0 ≤ lambda ≤ 1) to calibrate the decision 
# function so that a firm with “average” skepticism (S = .5) would be highly 
# unlikely to believe the association between innovation and performance 
# based on a single observation.

class Firm(object):
    def __init__(self, inertia=0, skepticism=0):

        self.MARKET_POSITION = truncnorm.rvs(0,1, n_innovations)  # called "K"
        #self.MARKET_POSITION = np.random.uniform(low=0, high=1)  # called "K"
        # Market position reflects the firm’s location in a stratified pop-
        # ulation, where some firms possess exogenous structural advantages that
        # are not affected by the choice of innovation.
        
        self.choice = np.random.choice(innovation_pool)  # called "i"
        # In the first round, firms select randomly from a pool of innovations
        
        self.inertia = inertia
        # Inertia indexes the firm’s tendency toward experimentation and change.
        # Volatile firms are quick to try new innovations, even when they are doing
        # well; inert firms are slow to search, even when they are doing badly.
        
        self.skepticism = skepticism  # called "S"
        # Skepticism indexes the firm’s readiness to draw conclusions from the
        # record of outcomes it observes. Naive firms are quick to infer that today’s
        # success story can be replicated. Skeptical firms treat the association be-
        # tween innovation and performance as potentially spurious.
        #
        # ...a firm with “average” skepticism (S = .5) would
        # be highly unlikely to believe the association between innovation and per-
        # formance based on a single observation.
        
        self.choice_history = [self.choice]
        self.performance_history = []
        self.outcome()  # appends to performance history
        # Keep track of what strategy the firm pursued, and what the result was
        
        
    def outcome(self):
        global weight_on_position
        global weight_on_choice
        global weight_on_luck
        
        luck = truncnorm.rvs(0,1, size=1)  # called "epsilon"
        
        outcome = (weight_on_position * self.MARKET_POSITION +
                   weight_on_choice * innovation_performances[innovation_pool.index(self.choice)] +
                   weight_on_luck * luck) 
        
        self.performance_history.append(outcome)
        return outcome
    
    def decision(self, winning_innovation, n_winners_made):
        """
        
        The firm’s decisions are made in two steps. First, the firm decides
        whether to abandon its current innovation and search for an alternative.
        If the firm decides to retain its current innovation, the decision process
        is over for that firm in that round. If the firm abandons its innovation,
        it then moves on to the second step, the selection of a new plan.
        """
        global t
        
        # historical uses of the current choice
        uses_of_choice = [i for i,x in enumerate(self.choice_history) if x == self.choice]
        considered_uses_of_choice = [i for i in uses_of_choice if i > t-consideration_interval]
        
        considered_experience_with_choice = len(considered_uses_of_choice)  # called "n_t(i)"
        
        confidence = 1 - self.inertia**(lam * considered_experience_with_choice)  # called "C"
        
        mean_performance_in_consideration = np.mean(
            [self.performance_history[i] for i in considered_uses_of_choice])  # called "\bar{O}"
        
        p_discard = (1-mean_performance_in_consideration)*confidence  # called "Prob(D_{fit})"
        
        if np.random.binomial(1, p_discard) == 1:  # discard the current choice
            # If a firm chooses to drop its current innovation,
            # it then looks to “best practice.” In our model, this is the “winning inno-
            # vation” w used by the firm with the highest score in the last round.
            # We assume that all firms know what innovation was used by the top performer
            # in each round and that they store this information for later recall. 
            
            influence_of_external_success = 1 - self.skepticism**(lam * n_winners_made)
            
            time_since_last_tried = list(reversed(self.choice_history)).index(winning_innovation) if \
                                    winning_innovation in self.choice_history else \
                                    100000  # called t_star(w)
            
            influence_of_internal_abandonment = 1 if time_since_last_tried > consideration_interval else \
                                            (1 - self.skepticism**(lam * time_since_last_tried))
                
            p_adopt_winning_innovation = influence_of_external_success * influence_of_internal_abandonment
            
            if np.random.binomial(1, p_adopt_winning_innovation):  # adopt winning innovation
                self.choice = winning_innovation
            else:
                # If a firm abandons its current practice but elects not to emulate the top 
                # performer, it innovates without regard to what other firms are doing.
                self.choice = np.random.choice(innovation_pool)
                
        self.choice_history.append(self.choice)
        
        return self.choice



def run(firms, n_rounds=200):
    global t
    
    # first round
    t = 0
    decisions = [firm.choice for firm in firms]
    outcomes = [firm.outcome() for firm in firms]

    winning_firm = outcomes.index(max(outcomes))
    winning_innovation = decisions[winning_firm]

    winning_innovation_history = [winning_innovation]
    winning_firm_history = [winning_firm]
    
    most_popular = max(set(decisions), key=decisions.count)
    most_popular_history = [most_popular]
    
    users_of_most_popular = [i for i,x in enumerate(decisions) if x == most_popular]
    popularity_history = [len(users_of_most_popular)]
    
    

    # subsequent rounds
    for i in range(1, n_rounds):
        t = i
        yesterdays_winner = winning_innovation_history[-1]  # called "w"

        winning_uses_of_yesterdays_winner = [i for i,x in enumerate(winning_innovation_history) 
                                             if x == yesterdays_winner]
        considered_winning_uses = [i for i in winning_uses_of_yesterdays_winner if i > t-consideration_interval]
        considered_winners = [winning_firm_history[i] for i in considered_winning_uses]
        n_winners_made = len(set(considered_winners))  # called "N_t(w)"

        decisions = [firm.decision(winning_innovation, n_winners_made) for firm in firms]
        outcomes = [firm.outcome() for firm in firms]

        winning_firm = outcomes.index(max(outcomes))
        winning_innovation = decisions[winning_firm]

        winning_innovation_history.append(winning_innovation)
        winning_firm_history.append(winning_firm)
        
        most_popular = max(set(decisions), key=decisions.count)
        users_of_most_popular = [i for i,x in enumerate(decisions) if x == most_popular]
        popularity_history.append(len(users_of_most_popular))
        most_popular_history.append(most_popular)
        
    result = {
        'popularity': popularity_history,
        'turnover': sum(np.diff(most_popular_history) != 0)/(n_rounds/100) # count number of changes in most popular
    }
    
    return result



global weight_on_position
global weight_on_choice
global weight_on_luck
        
weight_on_position = 0  # called "alpha"
weight_on_choice = 0  # called "beta"
weight_on_luck = 1 - weight_on_position - weight_on_choice
n_firms = 100

firms = [Firm(inertia=0, skepticism=0) for _ in range(n_firms)]
result = run(firms)


plt.plot(result['popularity'])
plt.ylabel('Popularity')
plt.xlabel('Steps');
            