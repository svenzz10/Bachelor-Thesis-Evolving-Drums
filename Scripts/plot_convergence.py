import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter

#Plot MusicVAE
Read the CSV files
train_data = pd.read_csv("run-train-tag-loss.csv")
eval_data = pd.read_csv("run-eval-tag-loss.csv")

# Apply the Savitzky-Golay filter to the training data
window_length = 59 # choose odd number 
polyorder = 3 # choose the order of the polynomial
train_data['Value_smooth'] = savgol_filter(train_data['Value'], window_length, polyorder)

# Plot the data
plt.plot(train_data['Step'], train_data['Value_smooth'], label='Training')
plt.plot(eval_data['Step'], eval_data['Value'], label='Evaluation')

# Add labels and legend
plt.xlabel('Timestep')
plt.ylabel('Value')
plt.title("MusicVAE: Loss per timestep")
# Set the y-axis limit
plt.ylim(30, 130)
plt.legend()

# Show the plot
plt.savefig("music_vae_plot")

#Plot DRUMRnn
# Read the CSV files
train_data_drum = pd.read_csv("run-train-tag-loss-drumrnn.csv")
eval_data_drum = pd.read_csv("run-eval-tag-loss-drumrnn.csv")

# Apply the Savitzky-Golay filter to the training data
window_length = 95 # choose odd number 
polyorder = 3 # choose the order of the polynomial
train_data_drum['Value_smooth'] = savgol_filter(train_data_drum['Value'], window_length, polyorder)

# Plot the data
plt.plot(train_data_drum['Step'], train_data_drum['Value_smooth'], label='Training')
plt.plot(eval_data_drum['Step'], eval_data_drum['Value'], label='Evaluation')

# Add labels and legend
plt.xlabel('Timestep')
plt.ylabel('Value')
plt.title("DrumsRNN: Loss per timestep")
# Set the y-axis limit
plt.ylim(1.25, 3)
plt.legend()

# Show the plot
plt.savefig("drumrnn_plot")