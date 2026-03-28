from z3 import *

# Real data from the NPL Report
fpir_table = {
    0.90: {"White": 0.0, "Black": 0.0, "Asian": 0.0},
    0.85: {"White": 0.0, "Black": 0.006, "Asian": 0.002},
    0.80: {"White": 0.0004, "Black": 0.055, "Asian": 0.04},
    0.75: {"White": 0.024, "Black": 0.237, "Asian": 0.186},
}

def check_deontological_bias(suspect_demographic: str):
    # Define Sorts and Variables
    Demographic = DeclareSort('Demographic')
    White, Black, Asian = Consts('White Black Asian', Demographic)
    FPIR = Function('FPIR', Demographic, RealSort())
    SearchAllowed = Bool('SearchAllowed')

    # Map string label -> Z3 constant
    demo_map = {"White": White, "Black": Black, "Asian": Asian}
    suspect = demo_map.get(suspect_demographic, None)

    s = Solver()
    s.add(Or(suspect == White, suspect == Black, suspect == Asian))
    s.add(Distinct(White, Black, Asian))

    # Categorical Imperative: only the SEARCHED demographic's FPIR is relevant.
    equitability_rule = Implies(FPIR(suspect) > 0.05, Not(SearchAllowed))
    s.add(equitability_rule)

    print(f"Suspect demographic: {suspect_demographic}")

    for T_val, demographics in fpir_table.items():
        s.push()

        # Assign real FPIR values for all demographics (system has full picture)
        s.add(FPIR(White) == demographics["White"])
        s.add(FPIR(Black) == demographics["Black"])
        s.add(FPIR(Asian) == demographics["Asian"])

        # Attempt to authorise the search
        s.add(SearchAllowed == True)

        result = s.check()

        suspect_fpir = demographics[suspect_demographic]
        print(f"T = {T_val} | {suspect_demographic} FPIR = {suspect_fpir:.4f}", end="  ->  ")

        if result == unsat:
            print(f"[BLOCKED] FPIR({suspect_demographic}) > 5% — Search withheld.")
        else:
            print(f"[PASSED]  Search permitted.")

        s.pop()
    print("\n")

if __name__ == "__main__":
    check_deontological_bias("White")
    check_deontological_bias("Black")
    check_deontological_bias("Asian")