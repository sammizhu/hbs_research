import matplotlib.pyplot as plt
import seaborn as sns

# Define the coefficients and their standard errors
coefficients = {
    'B&H Majority X B&H Founder': [0.],
    'B&H Minority X B&H Founder': [0.],
    'B&H Majority': [-0.],
    'B&H Minority': [-0.],
    'B&H Startup Founder': [-0.],
}

std_errors = {
    'B&H Majority X B&H Founder': [0.],
    'B&H Minority X B&H Founder': [0.],
    'B&H Majority': [0.],
    'B&H Minority': [0.],
    'B&H Startup Founder': [0.],
}

# Plot the coefficients with error bars for each label
plt.figure(figsize=(12, 8))

labels = list(coefficients.keys())
values = [value[0] for value in coefficients.values()]  
errors = [error[0] for error in std_errors.values()]    

plt.errorbar(range(len(labels)), values, yerr=errors, fmt='o', color='black', capsize=5)

plt.axhline(y=0, color='black', linestyle='--')
plt.xlabel('Dependent Variables')
plt.ylabel('Coefficient')
plt.xticks(range(len(labels)), labels, rotation=45, ha='right')

# Remove the box and title
sns.despine()
plt.title("")  # Empty string for title

plt.tight_layout()
plt.savefig('A7.png')
plt.show()

