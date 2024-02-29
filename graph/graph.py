import matplotlib.pyplot as plt
import seaborn as sns

# Define the coefficients and their standard errors
coefficients = {
    'B&H Majority X B&H Founder': [0.040],
    'B&H Minority X B&H Founder': [0.016],
    'B&H Majority': [-0.020],
    'B&H Minority': [-0.002],
    'B&H Startup Founder': [-0.020],
}

std_errors = {
    'B&H Majority X B&H Founder': [0.017],
    'B&H Minority X B&H Founder': [0.025],
    'B&H Majority': [0.008],
    'B&H Minority': [0.013],
    'B&H Startup Founder': [0.007],
}

# Plot the coefficients with error bars for each label
plt.figure(figsize=(12, 8))

labels = list(coefficients.keys())
values = [value[0] for value in coefficients.values()]  # Extracting the value from the list
errors = [error[0] for error in std_errors.values()]     # Extracting the error from the list

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
