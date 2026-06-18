import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

def plot_inisialize(history):

    df = pd.DataFrame(history)

    print(df.head())
    return df

def soc_plot(history):

    df = plot_inisialize(history)
    plt.figure(figsize=(10,5))
    plt.plot(df["time"], df["soc"])

    plt.xlabel("Time (s)")
    plt.ylabel("SOC")
    plt.title("Battery State of Charge")
    plt.grid(True)

    plt.show()

def soh_plot(history):

    df = plot_inisialize(history)
    plt.figure(figsize=(10,5))
    plt.plot(df["time"], df["soh"])

    plt.xlabel("Time (s)")
    plt.ylabel("SOH")
    plt.title("Battery Health Degradation")
    plt.grid()

    plt.show()

def temp_plot(history):

    df = plot_inisialize(history)
    plt.figure(figsize=(10,5))
    plt.plot(df["time"], df["temp"])

    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.title("Battery Temperature")
    plt.grid()

    plt.show()

def ecm_plot(history):

    df = plot_inisialize(history)
    plt.figure(figsize=(10,5))
    plt.plot(df["time"], df["voltage"])

    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Terminal Voltage")
    plt.grid()

    plt.show()

def behavior_plot(history):

    df = plot_inisialize(history)
    plt.figure(figsize=(10,5))
    plt.plot(df["time"], df["power"])

    plt.xlabel("Time (s)")
    plt.ylabel("Power (W)")
    plt.title("Phone Power Consumption")
    plt.grid()

    plt.show()

def soc_temp_plot(history):

    df = plot_inisialize(history)
    fig, ax1 = plt.subplots(figsize=(10,5))

    ax1.plot(df["time"], df["soc"])
    ax1.set_ylabel("SOC")

    ax2 = ax1.twinx()

    ax2.plot(df["time"], df["temp"])
    ax2.set_ylabel("Temperature (°C)")

    plt.title("SOC and Temperature Evolution")

    plt.show()

def soc_voltage_plot(history):
    
    df = plot_inisialize(history)
    plt.figure(figsize=(8,6))

    plt.plot(df["soc"], df["voltage"])

    plt.xlabel("SOC")
    plt.ylabel("Voltage (V)")
    plt.title("SOC-Voltage Curve")

    plt.grid()
    plt.show()

def soc_temp_voltage_plot(history):

    df = plot_inisialize(history)

    fig = plt.figure(figsize=(8,6))

    ax = fig.add_subplot(111, projection='3d')

    ax.plot(
        df["soc"],
        df["temp"],
        df["voltage"]
    )

    ax.set_xlabel("SOC")
    ax.set_ylabel("Temperature")
    ax.set_zlabel("Voltage")

    plt.show()

def heat_map_plot(history):

    df = plot_inisialize(history)
    corr = df[
        [
            "soc",
            "soh",
            "temp",
            "voltage",
            "current",
            "power"
        ]
    ].corr()

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm"
    )

    plt.title("Correlation Matrix")

    plt.show()
