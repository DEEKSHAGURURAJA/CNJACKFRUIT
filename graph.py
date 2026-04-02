import matplotlib.pyplot as plt

times = []
labels = []

with open("results.txt", "r") as f:
    for line in f:
        parts = line.split("->")
        host_port = parts[0].strip()
        time_part = parts[1].split("(")[1].split("ms")[0]

        labels.append(host_port)
        times.append(float(time_part))

plt.bar(labels, times)
plt.xlabel("Host:Port")
plt.ylabel("Response Time (ms)")
plt.title("Server Response Times")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()