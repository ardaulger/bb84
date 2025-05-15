import streamlit as st
import numpy as np
import pandas as pd

# Streamlit ayarları
st.set_page_config(page_title="BB84 Kuantum Kriptografi Simülasyonu", layout="centered")
st.title("🔐 BB84 Kuantum Kriptografi Simülasyonu")

# Rastgele bit üret
@st.cache_data
def generate_random_bits(length):
    return np.random.randint(0, 2, length)

# Rastgele temel üret
@st.cache_data
def generate_random_bases(length):
    return np.random.choice(['+', 'x'], length)

# Qubit hazırla
def prepare_qubits(bits, bases):
    qubits = []
    for bit, base in zip(bits, bases):
        if base == '+':
            qubits.append('|0⟩' if bit == 0 else '|1⟩')
        else:
            qubits.append('|+⟩' if bit == 0 else '|-⟩')
    return qubits

# Eva müdahale etsin mi?
def eva_intervention(qubits, probability):
    intercepted = []
    for q in qubits:
        if np.random.rand() < probability:
            rand_base = np.random.choice(['+', 'x'])
            bit = np.random.randint(0, 2)
            if rand_base == '+':
                intercepted.append('|0⟩' if bit == 0 else '|1⟩')
            else:
                intercepted.append('|+⟩' if bit == 0 else '|-⟩')
        else:
            intercepted.append(q)
    return intercepted

# Ölçüm
def measure_qubits(qubits, bases):
    measured_bits = []
    for qubit, base in zip(qubits, bases):
        if (qubit in ['|0⟩', '|1⟩']) and base == '+':
            measured_bits.append(0 if qubit == '|0⟩' else 1)
        elif (qubit in ['|+⟩', '|-⟩']) and base == 'x':
            measured_bits.append(0 if qubit == '|+⟩' else 1)
        else:
            measured_bits.append(np.random.randint(0, 2))
    return measured_bits

# Filtreleme
def filter_key(alice_bases, bob_bases, alice_bits, bob_bits):
    key_indices = alice_bases == bob_bases
    filtered_key = alice_bits[key_indices]
    bob_filtered_key = bob_bits[key_indices]
    return filtered_key, bob_filtered_key, key_indices

# Simülasyonu çalıştır
if st.button("🚀 Simülasyonu Başlat"):
    n = 10
    eva_listens = np.random.choice([True, False])
    
    alice_bits = generate_random_bits(n)
    alice_bases = generate_random_bases(n)
    qubits = prepare_qubits(alice_bits, alice_bases)

    if eva_listens:
        qubits = eva_intervention(qubits, probability=0.5)

    bob_bases = generate_random_bases(n)
    bob_bits = measure_qubits(qubits, bob_bases)

    alice_bases_np = np.array(alice_bases)
    bob_bases_np = np.array(bob_bases)
    alice_bits_np = np.array(alice_bits)
    bob_bits_np = np.array(bob_bits)

    shared_key, bob_key, matches = filter_key(alice_bases_np, bob_bases_np, alice_bits_np, bob_bits_np)

    # Tabloda göstermek için DataFrame oluştur
    df = pd.DataFrame({
        "Alice Bit": alice_bits,
        "Alice Temel": alice_bases,
        "Qubit": prepare_qubits(alice_bits, alice_bases),
        "Eva Dinledi mi?": ["✅" if not eva_listens else "🕵️"] * n,
        "Bob Temel": bob_bases,
        "Bob Ölçüm": bob_bits,
        "Temel Eşleşmesi": matches,
        "Ortak Bit (Alice)": [a if m else "-" for a, m in zip(alice_bits, matches)],
        "Ortak Bit (Bob)": [b if m else "-" for b, m in zip(bob_bits, matches)],
    })

    st.subheader("📊 BB84 Simülasyon Tablosu")
    st.dataframe(df, use_container_width=True)

    # Sonuç mesajı
    if np.array_equal(shared_key, bob_key):
        st.success("✅ Anahtarlar uyuşuyor. Güvenli iletişim mümkün.")
    else:
        st.error("⚠️ Anahtarlar uyuşmuyor. Eva iletişimi dinlemiş olabilir!")

    st.info("Simülasyon 10 saniye sonra yeniden başlatılabilir.")
