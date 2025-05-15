import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
st.title("Dashboard Penggunaan Sepeda")

# Upload file
uploaded_file = st.file_uploader("Unggah file CSV", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Pastikan kolom sesuai
    if all(col in df.columns for col in ['cnt', 'casual', 'registered', 'workingday']):
        df_baru = df.copy()
        tbl_hari = df.copy()

        st.subheader("📊 Perbandingan Hari Terbanyak vs Tersedikit")

        # Ambil data hari dengan cnt terbanyak dan tersedikit
        hari_terbanyak = df_baru.loc[df_baru['cnt'].idxmax()]
        hari_tersedikit = df_baru.loc[df_baru['cnt'].idxmin()]

        # Siapkan data untuk bar chart
        labels = ['Tersedikit', 'Terbanyak']
        casual_values = [hari_tersedikit['casual'], hari_terbanyak['casual']]
        registered_values = [hari_tersedikit['registered'], hari_terbanyak['registered']]
        x = range(len(labels))
        width = 0.35

        fig1, ax1 = plt.subplots(figsize=(8, 5))
        ax1.bar(x, casual_values, width=width, label='Casual', color='skyblue')
        ax1.bar([i + width for i in x], registered_values, width=width, label='Registered', color='lightgreen')
        ax1.set_xticks([i + width/2 for i in x])
        ax1.set_xticklabels(labels)
        ax1.set_ylabel("Jumlah Pengguna")
        ax1.set_title("Perbandingan Pengguna Sepeda\n(Hari Terbanyak vs Tersedikit)")
        ax1.legend()
        st.pyplot(fig1)

        # ------------------- Hari Kerja -------------------
        st.subheader("🏢 Penggunaan Sepeda Saat Hari Kerja")
        kerja_df = tbl_hari[tbl_hari['workingday'] == 1]
        total_casual = kerja_df['casual'].sum()
        total_registered = kerja_df['registered'].sum()

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie([total_casual, total_registered],
                labels=['Casual', 'Registered'],
                autopct='%1.1f%%',
                colors=['skyblue', 'lightgreen'],
                startangle=90)
        ax2.set_title('Penggunaan Sepeda saat Hari Kerja (workingday=1)')
        ax2.axis('equal')
        st.pyplot(fig2)

        # ------------------- Hari Libur -------------------
        st.subheader("🎉 Penggunaan Sepeda Saat Hari Libur")
        libur_df = tbl_hari[tbl_hari['workingday'] == 0]
        total_casual = libur_df['casual'].sum()
        total_registered = libur_df['registered'].sum()

        fig3, ax3 = plt.subplots(figsize=(6, 6))
        ax3.pie([total_casual, total_registered],
                labels=['Casual', 'Registered'],
                autopct='%1.1f%%',
                colors=['skyblue', 'lightgreen'],
                startangle=90)
        ax3.set_title('Penggunaan Sepeda saat Hari Libur (workingday=0)')
        ax3.axis('equal')
        st.pyplot(fig3)

    else:
        st.error("Kolom pada file CSV tidak lengkap. Pastikan ada kolom: cnt, casual, registered, workingday.")
else:
    st.info("Silakan unggah file CSV yang berisi data penggunaan sepeda.")
