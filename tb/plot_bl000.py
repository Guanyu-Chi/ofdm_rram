import re
import matplotlib.pyplot as plt

infile = "results/sim_ascii/tbtran.tran.tran"
outfile = "results/sim_ascii/bl000_waveform.png"

times = []
values = []

current_time = None

with open(infile, "r", errors="ignore") as f:
    after_value = False

    for line in f:
        line = line.strip()

        if line == "VALUE":
            after_value = True
            continue

        if not after_value:
            continue

        m_time = re.match(r'"time"\s+([-+0-9.eE]+)', line)
        if m_time:
            current_time = float(m_time.group(1))
            continue

        m_bl = re.match(r'"bl000"\s+([-+0-9.eE]+)', line)
        if m_bl and current_time is not None:
            times.append(current_time)
            values.append(float(m_bl.group(1)))

if len(times) == 0:
    raise RuntimeError("No bl000 data found.")

plt.figure(figsize=(9, 4))
plt.plot(times, values)
plt.xlabel("Time (s)")
plt.ylabel("bl000 voltage (V)")
plt.title("Transient waveform: bl000")
plt.grid(True)
plt.tight_layout()
plt.savefig(outfile, dpi=300)

print(f"Saved: {outfile}")
print(f"Number of points: {len(times)}")
print(f"Time range: {times[0]} to {times[-1]} s")
