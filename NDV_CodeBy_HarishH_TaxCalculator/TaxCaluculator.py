def calculate_tax(income, slabs):
   
    tax = 0
    for upper_limit, rate, base_tax in slabs:
        if income <= upper_limit:
            tax = base_tax + (income - (upper_limit - (upper_limit - (base_tax / rate)))) * rate
            break
        tax = base_tax + (upper_limit - (upper_limit - (base_tax / rate))) * rate
    return tax

def calculate_tax_from_slabs(income, slabs_config):
   
    tax = 0.0
    for slab in slabs_config:
        lower_bound = slab.get('lower_bound', 0)
        upper_bound = slab['upper_bound']
        rate = slab['rate']
        base_tax = slab.get('base_tax', 0)

        if income <= lower_bound:
            tax = 0.0
            break
        elif income <= upper_bound:
            tax = base_tax + (income - lower_bound) * rate
            break
        else:
            tax = base_tax + (upper_bound - lower_bound) * rate # Accumulate tax for full slabs passed
    return tax

try:
    ctc = float(input("Enter your Total CTC: "))
    bonus = float(input("Enter your Bonus Amount: "))
except ValueError:
    print("Invalid input. Please enter numeric values for CTC and Bonus.")
    exit()

total_income = ctc + bonus
print(f"Total Income: {total_income:.2f}")


old_regime_taxable_income = max(0, total_income - 220000)

old_regime_slabs = [
    {'lower_bound': 0, 'upper_bound': 250000, 'rate': 0.00, 'base_tax': 0},
    {'lower_bound': 250000, 'upper_bound': 500000, 'rate': 0.05, 'base_tax': 0},
    {'lower_bound': 500000, 'upper_bound': float('inf'), 'rate': 0.20, 'base_tax': 12500}, # 'inf' for the highest slab
]
old_tax = calculate_tax_from_slabs(old_regime_taxable_income, old_regime_slabs)


new_regime_slabs = [
    {'lower_bound': 0, 'upper_bound': 250000, 'rate': 0.00, 'base_tax': 0},
    {'lower_bound': 250000, 'upper_bound': 500000, 'rate': 0.05, 'base_tax': 0},
    {'lower_bound': 500000, 'upper_bound': 1000000, 'rate': 0.20, 'base_tax': 12500},
    {'lower_bound': 1000000, 'upper_bound': float('inf'), 'rate': 0.30, 'base_tax': 112500}, # 12500 + (500000 * 0.2) = 112500
]
new_tax = calculate_tax_from_slabs(total_income, new_regime_slabs)

print(f"Old Regime Tax: {old_tax:.2f}")
print(f"New Regime Tax: {new_tax:.2f}")

if old_tax < new_tax:
    print(f"Old Regime is more beneficial. You save: {(new_tax - old_tax):.2f}")
elif new_tax < old_tax:
    print(f"New Regime is more beneficial. You save: {(old_tax - new_tax):.2f}")
else:
    print("Both regimes result in the same tax.")
