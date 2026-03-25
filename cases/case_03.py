from z3 import *

from ctl_checker import SymbolicModelChecker
def check_virtue_accountability():
    # Variables: Current state and Next state (primes)
    ack = Bool('ack')           # Operator acknowledged FPIR limitations
    unlocked = Bool('unlocked') # Profile is unlocked for viewing
    
    ack_p = Bool('ack_prime')
    unlocked_p = Bool('unlocked_prime')
    
    # Define Valid Transitions
    t_wait = And(Not(ack), Not(unlocked), Not(ack_p), Not(unlocked_p))
    # Operator clicks
    t_click = And(Not(ack), Not(unlocked), ack_p, Not(unlocked_p)) 
    # System unlocks
    t_unlock = And(ack, Not(unlocked), ack_p, unlocked_p)
    # Viewing state      
    t_view = And(ack, unlocked, ack_p, unlocked_p)                 
    
    Transition = Or(t_wait, t_click, t_unlock, t_view)
    Init = And(Not(ack), Not(unlocked)) 
    
    mc = SymbolicModelChecker()
    mc.set_model([ack, unlocked], Transition, Init)
    
    # Property: Always Globally, if unlocked is True, ack MUST be True
    safety_property = mc.AG(Implies(unlocked, ack))
    
    print("Checking Virtue Ethics UI Lock:")
    mc.check(safety_property) # Should output: Property Verified

if __name__ == "__main__":
    check_virtue_accountability()