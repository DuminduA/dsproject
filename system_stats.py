import matplotlib.pyplot as plt
import psutil
import time

def collect_system_stats(duration_seconds):
    cpu_usage = []
    memory_usage = []

    # Collect system stats for the specified duration
    for _ in range(duration_seconds):
        cpu_usage.append(psutil.cpu_percent())
        memory_usage.append(psutil.virtual_memory().percent)
        time.sleep(1)  # Collect stats every second

    return cpu_usage, memory_usage

def plot_system_stats(cpu_usage, memory_usage, title):
    plt.figure(figsize=(10, 6))
    plt.plot(cpu_usage, label='CPU Usage (%)', color='blue')
    plt.plot(memory_usage, label='Memory Usage (%)', color='green')
    plt.title(title)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Usage (%)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
duration_seconds = 60  # Duration to collect stats
cpu_usage_5_contacts, memory_usage_5_contacts = collect_system_stats(duration_seconds)
plot_system_stats(cpu_usage_5_contacts, memory_usage_5_contacts, 'API with 5000 Contacts')
