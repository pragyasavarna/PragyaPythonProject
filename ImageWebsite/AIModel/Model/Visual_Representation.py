import pickle
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

# Where to save plots
OUTPUT_DIR = "static/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Load history.pkl from Django server
# Go one folder up from BASE_DIR

# Then join "Model"
file_name = "animal_history.pkl"
model_dir = os.path.join(BASE_DIR, "Model/artifacts/"+file_name)
print(model_dir)


# url = "http://127.0.0.1:8000/Artifacts/animal_history.pkl"
# response = requests.get(url)
# response.raise_for_status()
# history_dict = pickle.loads(response.content)
with open(model_dir, "rb") as f:
    history_dict = pickle.load(f)

# Convert to DataFrame
history_df = pd.DataFrame(history_dict)

# Save plots as PNG
def save_plot(columns, title, filename):
    fig, ax = plt.subplots()
    history_df.loc[:, columns].plot(ax=ax, title=title)
    ax.set_xlabel("Epochs")
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, bbox_inches="tight")
    plt.close(fig)

save_plot(['loss', 'val_loss'], "Model Loss", "animal_loss.png")
save_plot(['accuracy', 'val_accuracy'], "Model Accuracy", "animal_accuracy.png")

print("✅ Plots saved in static/plots/")
