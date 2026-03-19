import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- KONFIGURASI TAMPILAN ---
st.set_page_config(page_title="NU RESIK - Seputih Surabaya", layout="wide", page_icon="🟢")

# CSS Kustom Hijau NU
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-header { color: #006400; font-size: 30px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .stButton>button { background-color: #006400; color: white; border-radius: 10px; width: 100%; }
    .card { background: white; padding: 20px; border-radius: 15px; shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- DATA STATIS ---
RANTINGS = ["Gaya Baru I", "Gaya Baru II", "Gaya Baru III", "Gaya Baru IV", "Gaya Baru VI", "Gaya Baru VII", "Gaya Baru VIII", "Kenanga Sari", "Mataram Ilir", "Rawa Betik", "Sri Katon", "Sri Mulya Jaya", "Sumber Katon"]
HARGA = {"Plastik": 2500, "Kertas": 2000, "Logam": 6000, "Minyak": 4000}

# --- SIMULASI DATABASE (Untuk Demo Langsung) ---
if 'db_warga' not in st.session_state:
    st.session_state.db_warga = pd.DataFrame([
        {'Nama': 'KH. Ahmad', 'Ranting': 'Gaya Baru I', 'Banom': 'NU', 'Saldo': 50000},
        {'Nama': 'Gus Fauzi', 'Ranting': 'Sri Katon', 'Banom': 'Ansor', 'Saldo': 25000}
    ])
if 'db_trx' not in st.session_state:
    st.session_state.db_trx = pd.DataFrame(columns=['Tanggal', 'Nama', 'Jenis', 'Berat', 'Total'])

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/id/thumb/a/a2/Logo_Nahdlatul_Ulama.svg/1200px-Logo_Nahdlatul_Ulama.svg.png", width=100)
    st.title("NU RESIK DIGITAL")
    st.write("MWC Seputih Surabaya")
    st.markdown("---")
    menu = st.radio("PILIH MODUL", ["🏠 Dashboard", "👥 Database Warga", "♻️ Bank Sampah", "🗞️ NU Online (Berita)", "💰 Wallet & Tukar Saldo"])

# --- 1. DASHBOARD ---
if menu == "🏠 Dashboard":
    st.markdown("<div class='main-header'>EKOSISTEM DIGITAL NU RESIK</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Warga", len(st.session_state.db_warga))
    col2.metric("Total Saldo (Rp)", f"Rp {st.session_state.db_warga['Saldo'].sum():,.0f}")
    col3.metric("Sampah (Kg)", f"{st.session_state.db_trx['Berat'].sum():.1f}")

    st.markdown("---")
    st.subheader("Statistik Per Ranting")
    fig = px.pie(st.session_state.db_warga, names='Ranting', title="Distribusi Warga per Ranting")
    st.plotly_chart(fig, use_container_width=True)

# --- 2. DATABASE WARGA ---
elif menu == "👥 Database Warga":
    st.header("👥 Data Warga & Banom")
    with st.expander("➕ Tambah Warga Baru"):
        with st.form("reg"):
            n = st.text_input("Nama Lengkap")
            r = st.selectbox("Ranting", RANTINGS)
            b = st.selectbox("Banom", ["NU", "Muslimat", "Ansor", "Fatayat", "IPNU", "IPPNU"])
            if st.form_submit_button("Daftarkan"):
                new_data = pd.DataFrame([{'Nama': n, 'Ranting': r, 'Banom': b, 'Saldo': 0}])
                st.session_state.db_warga = pd.concat([st.session_state.db_warga, new_data], ignore_index=True)
                st.success("Warga berhasil didaftarkan!")
    st.table(st.session_state.db_warga)

# --- 3. BANK SAMPAH ---
elif menu == "♻️ Bank Sampah":
    st.header("♻️ Penimbangan Bank Sampah")
    c1, c2 = st.columns([1, 2])
    with c1:
        with st.form("setor"):
            nasabah = st.selectbox("Pilih Nama", st.session_state.db_warga['Nama'])
            jenis = st.selectbox("Jenis Sampah", list(HARGA.keys()))
            berat = st.number_input("Berat (Kg)", min_value=0.1)
            if st.form_submit_button("Proses Menjadi Saldo"):
                total = berat * HARGA[jenis]
                st.session_state.db_warga.loc[st.session_state.db_warga['Nama'] == nasabah, 'Saldo'] += total
                new_trx = pd.DataFrame([{'Tanggal': datetime.now().date(), 'Nama': nasabah, 'Jenis': jenis, 'Berat': berat, 'Total': total}])
                st.session_state.db_trx = pd.concat([st.session_state.db_trx, new_trx], ignore_index=True)
                st.success(f"Saldo Rp {total:,.0f} masuk!")
    with c2:
        st.write("Riwayat Setoran Terakhir")
        st.dataframe(st.session_state.db_trx.tail(5), use_container_width=True)

# --- 4. NU ONLINE (BERITA) ---
elif menu == "🗞️ NU Online (Berita)":
    st.header("🗞️ Portal Berita NU Seputih Surabaya")
    st.image("https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?w=1000", caption="Aktivitas MWC NU")
    st.info("**BERITA UTAMA:** MWC NU Seputih Surabaya mengaktifkan sistem Digital Ecosystem NU RESIK untuk seluruh ranting.")
    st.markdown("---")
    st.subheader("Kegiatan Terbaru")
    st.write("- **Gaya Baru I:** Lailatul Ijtima' dihadiri 200 Jamaah.")
    st.write("- **Sri Katon:** Lazisnu menyalurkan bantuan beras hasil bank sampah.")

# --- 5. WALLET & TUKAR ---
elif menu == "💰 Wallet & Tukar Saldo":
    st.header("💰 Wallet Ekonomi & Penukaran")
    user = st.selectbox("Lihat Saldo Siapa?", st.session_state.db_warga['Nama'])
    saldo_user = st.session_state.db_warga[st.session_state.db_warga['Nama'] == user]['Saldo'].values[0]
    
    st.subheader(f"Saldo Anda: Rp {saldo_user:,.0f}")
    
    st.write("Pilih Penukaran:")
    col_a, col_b, col_c = st.columns(3)
    col_a.button("📱 Pulsa/Data")
    col_b.button("⚡ Token PLN")
    col_c.button("🛒 Sembako")
    
    st.markdown("---")
    req = st.text_input("Request Penukaran Lain (Bebas):")
    if st.button("Kirim Permintaan Ke Admin"):
        st.success(f"Permintaan '{req}' telah dikirim ke Admin MWC.")
