import streamlit as st
import numpy as np

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
            # Rastgele ölçüm ve yeniden gönderme
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
    return filtered_key, bob_filtered_key

# Simülasyonu çalıştır
if st.button("🚀 Simülasyonu Başlat"):
    n = 10
    eva_listens = np.random.choice([True, False])
    
    # 1️⃣ Alice bitleri ve temelleri
    st.subheader("1️⃣ Alice Bitleri ve Temelleri")
    alice_bits = generate_random_bits(n)
    alice_bases = generate_random_bases(n)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔢 Alice Bitleri**")
        st.write(alice_bits)
    with col2:
        st.markdown("**📐 Alice Temelleri**")
        st.write(alice_bases)

    # 2️⃣ Qubit hazırlama
    st.subheader("2️⃣ Alice Qubit'leri Hazırlıyor")
    qubits = prepare_qubits(alice_bits, alice_bases)
    st.write(qubits)

    # 3️⃣ Eva dinliyor mu?
    st.subheader("3️⃣ Eva Dinliyor mu?")
    st.write("🕵️‍♀️ Evet" if eva_listens else "✅ Hayır")
    if eva_listens:
        qubits = eva_intervention(qubits, probability=0.5)
        st.markdown("💥 **Qubit'ler Eva tarafından müdahaleye uğradı.**")

    # 4️⃣ Bob'un ölçümü
    st.subheader("4️⃣ Bob Temelleriyle Ölçüm Yapıyor")
    bob_bases = generate_random_bases(n)
    bob_bits = measure_qubits(qubits, bob_bases)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**📐 Bob Temelleri**")
        st.write(bob_bases)
    with col4:
        st.markdown("**🔍 Bob Ölçülen Bitler**")
        st.write(bob_bits)

    # 5️⃣ Anahtar karşılaştırması
    st.subheader("5️⃣ Anahtar Karşılaştırması")
    alice_bases_np = np.array(alice_bases)
    bob_bases_np = np.array(bob_bases)
    alice_bits_np = np.array(alice_bits)
    bob_bits_np = np.array(bob_bits)

    shared_key, bob_key = filter_key(alice_bases_np, bob_bases_np, alice_bits_np, bob_bits_np)
    
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("**🔐 Alice'in Ortak Anahtarı**")
        st.write(shared_key)
    with col6:
        st.markdown("**🔐 Bob'un Ortak Anahtarı**")
        st.write(bob_key)

    # Güvenlik kontrolü
    if np.array_equal(shared_key, bob_key):
        st.success("✅ Anahtarlar uyuşuyor. Güvenli iletişim mümkün.")
    else:
        st.error("⚠️ Anahtarlar uyuşmuyor. Eva iletişimi dinlemiş olabilir!")

    st.info("Simülasyon 10 saniye sonra yeniden başlatılabilir.")
