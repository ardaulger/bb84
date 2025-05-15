import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
import time

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.set_axis_off()

def run_simulation(event=None):
    ax.clear()
    ax.set_axis_off()
    ax.set_title("BB84 Kuantum Kriptografi Simülasyonu\n", fontsize=14)

    n = 10
    alice_bits = np.random.randint(0, 2, n)
    alice_bases = np.random.choice(['+', 'x'], n)
    bob_bases = np.random.choice(['+', 'x'], n)
    eva_is_listening = np.random.choice([True, False])

    qubits = []
    for bit, base in zip(alice_bits, alice_bases):
        if base == '+':
            qubits.append('|0⟩' if bit == 0 else '|1⟩')
        else:
            qubits.append('|+⟩' if bit == 0 else '|-⟩')

    eva_qubits = list(qubits)  # Eva'nın etkilediği qubit'ler
    if eva_is_listening:
        eva_qubits = []
        for q in qubits:
            # Eva ölçüm yaparsa bazen bozabilir
            if q in ['|0⟩', '|1⟩']:
                eva_qubits.append('|0⟩' if np.random.rand() < 0.5 else '|1⟩')
            else:
                eva_qubits.append('|+⟩' if np.random.rand() < 0.5 else '|-⟩')

    bob_bits = []
    for q, base in zip(eva_qubits, bob_bases):
        if base == '+':
            bob_bits.append(0 if q == '|0⟩' else 1 if q == '|1⟩' else np.random.randint(0, 2))
        else:
            bob_bits.append(0 if q == '|+⟩' else 1 if q == '|-⟩' else np.random.randint(0, 2))

    # Görselleştirme
    for i in range(n):
        y = 1 - i * 0.07
        ax.text(0.1, y, f"Alice: Bit={alice_bits[i]} Base={alice_bases[i]}", fontsize=10)
        # Eva etkisiyle bozulmuş mu?
        if eva_is_listening and qubits[i] != eva_qubits[i]:
            color = 'red'  # Bozulmuş qubit
        else:
            color = 'black'
        ax.text(0.4, y, f"Qubit={eva_qubits[i]}", fontsize=10, color=color)
        ax.text(0.7, y, f"Bob: Base={bob_bases[i]} -> Bit={bob_bits[i]}", fontsize=10)
        plt.pause(0.5)
    
    alice_bases = np.array(alice_bases)
    bob_bases = np.array(bob_bases)
    alice_bits = np.array(alice_bits)
    bob_bits = np.array(bob_bits)
    mask = alice_bases == bob_bases
    shared_key = alice_bits[mask]
    bob_key = bob_bits[mask]

    ax.text(0.1, -0.05, f"Eva dinledi mi? {'Evet' if eva_is_listening else 'Hayır'}", fontsize=12, color='blue')
    if np.array_equal(shared_key, bob_key):
        ax.text(0.1, -0.12, f"Anahtarlar uyuşuyor!", fontsize=12, color='green')
    else:
        ax.text(0.1, -0.12, f"Anahtarlar uyuşmuyor!", fontsize=12, color='red')

    ax.text(0.1, -0.2, "10 saniye içinde yeniden başlatabilirsiniz...", fontsize=10, color='gray')
    plt.draw()
    time.sleep(10)

# Buton
button_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
button = Button(button_ax, 'Yeniden Başlat')
button.on_clicked(run_simulation)

run_simulation()
plt.show()
