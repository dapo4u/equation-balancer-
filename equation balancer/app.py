import tkinter as tk
from sympy import symbols, Eq, solve, lcm
from sympy.core.numbers import Rational

def parse_compound(compound):
    """Parse chemical formulas into a dictionary of elements and their counts."""
    import re
    pattern = r'([A-Z][a-z]*)(\d*)'
    elements = {}
    for match in re.findall(pattern, compound):
        element = match[0]
        count = int(match[1]) if match[1] else 1
        elements[element] = elements.get(element, 0) + count
    return elements

def balance_equation():
    try:
        # Input from GUI fields
        reactants_input = reactants_entry.get().strip()
        products_input = products_entry.get().strip()

        # Parse reactants and products
        reactants = reactants_input.split("+")
        products = products_input.split("+")
        reactants = [parse_compound(comp.strip()) for comp in reactants]
        products = [parse_compound(comp.strip()) for comp in products]

        # Gather unique elements
        elements = set()
        for compound in reactants + products:
            elements.update(compound.keys())
        elements = list(elements)

        # Define variables for coefficients
        variables = symbols(f"x0:{len(reactants) + len(products)}")

        # Build equations for each element
        equations = []
        for element in elements:
            eq = 0
            for i, compound in enumerate(reactants):
                eq -= compound.get(element, 0) * variables[i]
            for i, compound in enumerate(products):
                eq += compound.get(element, 0) * variables[len(reactants) + i]
            equations.append(Eq(eq, 0))

        # Solve equations
        solution = solve(equations, variables, dict=True)
        if not solution:
            result_label.config(text="No solution found! Check the equation.")
            return

        # Extract coefficients and scale to integers
        coefficients = [solution[0].get(var, 0) for var in variables]
        denom_lcm = lcm([c.as_numer_denom()[1] for c in coefficients if c.is_Rational])
        coefficients = [int(c * denom_lcm) for c in coefficients]

        # Build the balanced equation
        reactant_str = " + ".join(
            f"{coefficients[i]}{reactants_input.split('+')[i].strip()}"
            for i in range(len(reactants))
        )
        product_str = " + ".join(
            f"{coefficients[len(reactants) + i]}{products_input.split('+')[i].strip()}"
            for i in range(len(products))
        )
        result = f"{reactant_str} → {product_str}"
        result_label.config(text=f"Balanced Equation: {result}")
    except Exception as e:
        # Log and display error messages
        print(f"Error: {e}")
        result_label.config(text=f"Error: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Chemical Equation Balancer")

# Widgets
tk.Label(root, text="Enter Reactants (e.g., H2 + O2):").grid(row=0, column=0, padx=10, pady=5)
reactants_entry = tk.Entry(root, width=40)
reactants_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Enter Products (e.g., H2O):").grid(row=1, column=0, padx=10, pady=5)
products_entry = tk.Entry(root, width=40)
products_entry.grid(row=1, column=1, padx=10, pady=5)

balance_button = tk.Button(root, text="Balance", command=balance_equation)
balance_button.grid(row=2, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="", fg="green", wraplength=400)
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the GUI event loop
root.mainloop()
