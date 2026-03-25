from z3 import *

# Real data from the NPL Report
fpir_table = {
    0.90: {"White": 0.0, "Black": 0.0, "Asian": 0.0},
    0.85: {"White": 0.0, "Black": 0.006, "Asian": 0.002},
    0.80: {"White": 0.0004, "Black": 0.055, "Asian": 0.04},
    0.75: {"White": 0.024, "Black": 0.237, "Asian": 0.186},
}

def check_deontological_bias():
    # Define Sorts and Variables
    Demographic = DeclareSort('Demographic')
    White, Black, Asian = Consts('White Black Asian', Demographic)
    FPIR = Function('FPIR', Demographic, RealSort())
    SearchAllowed = Bool('SearchAllowed')

    s = Solver()
    s.add(Distinct(White, Black, Asian)) # Ensure distinct categories

    # Define the Categorical Imperative (Rule)
    # For ALL demographics, if FPIR > 0.05 (5%), the search is strictly forbidden.
    d = Const('d', Demographic)
    equitability_rule = ForAll(d, Implies(FPIR(d) > 0.05, Not(SearchAllowed)))
    s.add(equitability_rule)

    print("Evaluating Ethical Equitability across different Thresholds (T)...\n")

    # Loop through the different T values to test the system dynamically
    for T_val, demographics in fpir_table.items():
        s.push() # Save the base state (the rules) before adding specific data
        
        # Feed the real NPL stats into the solver for this specific threshold
        s.add(FPIR(White) == demographics["White"])
        s.add(FPIR(Black) == demographics["Black"])
        s.add(FPIR(Asian) == demographics["Asian"])

        # Attempt to authorize the search
        s.add(SearchAllowed == True)

        result = s.check()
        
        print(f"Testing Threshold T = {T_val}:")
        print(f"  Stats: White FPIR={demographics['White']}, Black FPIR={demographics['Black']}, Asian FPIR={demographics['Asian']}")
        
        if result == unsat:
            print("  ->[BLOCKED] ETHICAL SAFEGUARD TRIGGERED: Search Withheld due to Demographic Bias.\n\n")
        else:
            print("  -> [PASSED] Search Allowed: System remains equitable.\n\n")
            
        s.pop() # Remove this threshold's data so we can test the next one cleanly

if __name__ == "__main__":
    check_deontological_bias()