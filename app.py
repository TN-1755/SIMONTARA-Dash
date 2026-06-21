import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials


now = datetime.utcnow() + timedelta(hours=7)

SPREADSHEET_ID = "11B8B7rlVEzGLUb5B3J-oAZIh87zbOdE7_-am42eJVsQ"

def load_sheet(sheet_name):

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]


    creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

    client = gspread.authorize(creds)

    worksheet = client.open_by_key(
        SPREADSHEET_ID
    ).worksheet(sheet_name)

    data = worksheet.get_all_values()

    return pd.DataFrame(data)

df = load_sheet("MONITORING ")


raw_sp2d = load_sheet("RAW_SP2D")

raw_sp2d = raw_sp2d.replace("", 0)



# Konfigurasi halaman
st.set_page_config(
    page_title="SIMONTARA",
    layout="wide"
)

# CSS KPI CARD
st.markdown("""
<style>

/* Mengurangi jarak kosong bagian atas */
.block-container{
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}

/* Hilangkan header bawaan Streamlit */
header[data-testid="stHeader"]{
    height: 0rem;
}

/* Rapikan toolbar */
div[data-testid="stToolbar"]{
    right: 1rem;
}

            
.kpi-card{
    background: #0B1730;
    border: 1px solid #2A4365;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.kpi-card:hover{
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(59,130,246,0.3);
}

.kpi-title{
    color: #A0AEC0;
    font-size: 16px;
    font-weight: 600;
}

.kpi-value{
    color: white;
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
}
            
.kpi-card-danger{
    background:#111827;
    border:1px solid #ef4444;
    border-top:4px solid #ef4444;
    border-radius:18px;
    padding:15px;
    text-align:center;
    box-shadow:0 4px 15px rgba(239,68,68,0.2);
}

.kpi-title-danger{
    color:#f87171;
    font-size:15px;
    font-weight:600;
}

.kpi-value-danger{
    color:#ffffff;
    font-size:32px;
    font-weight:700;
}
            
.chart-card{
    background:#0B1730;
    border:1px solid #2A4365;
    border-radius:18px;
    padding:15px;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# Format Rupiah Indonesia
def format_rupiah(nilai):
    return "Rp {:,.0f}".format(nilai).replace(",", ".")

# Baca sheet monitoring
df = load_sheet("MONITORING ")
raw_sp2d = load_sheet("RAW_SP2D")


def clean_numeric(series):
    s = (
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace("(", "-", regex=False)
        .str.replace(")", "", regex=False)
        .str.strip()
    )

    return pd.to_numeric(
        s,
        errors="coerce"
    ).fillna(0)


def angka_indonesia(x):

    if pd.isna(x):
        return 0

    x = str(x).strip()

    if x == "":
        return 0

    # persentase
    if "%" in x:
        return float(
            x.replace("%", "")
             .replace(".", "")
             .replace(",", ".")
        ) / 100

    # angka negatif dalam kurung
    if x.startswith("(") and x.endswith(")"):
        return -float(
            x[1:-1]
             .replace(".", "")
             .replace(",", ".")
        )

    return float(
        x.replace(".", "")
         .replace(",", ".")
    )
    

# RAW_SP2D
raw_sp2d = raw_sp2d.replace("", 0)


# Ambil KPI dari Excel
pagu = angka_indonesia(df.iloc[6, 2])
rpd = angka_indonesia(df.iloc[6, 6])
realisasi = angka_indonesia(df.iloc[6, 10])
persentase = angka_indonesia(df.iloc[6, 13])
deviasi = angka_indonesia(df.iloc[6, 16])

# Status Deviasi
if deviasi >= 0:
    status_deviasi = "🟢 Sesuai Target"
elif deviasi > -500000000:
    status_deviasi = "🟡 Perlu Perhatian"
else:
    status_deviasi = "🔴 Di Bawah Target"

# HEADER DASHBOARD
st.markdown("""
<h1 style='
    color:#2F6DB5;
    margin-bottom:0px;
'>
📊 SIMONTARA
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div style='
    font-size:20px;
    color:#d1d5db;
    margin-bottom:4px;
'>
Sistem Monitoring Tagihan dan Realisasi Anggaran 
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='
    font-size:14px;
    color:#9ca3af;
    margin-bottom:15px;
'>
Monitoring Realisasi Anggaran secara Cepat, Tepat, Transparan dan Akuntabel
</div>
""", unsafe_allow_html=True)

# WIB
now = datetime.utcnow() + timedelta(hours=7)

tanggal = now.strftime("%d-%m-%Y")
jam = now.strftime("%H:%M")

st.markdown(
    f"""
    📅 <b>{tanggal}</b>
    &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    🕒 <b>{jam} WIB</b>
    &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    📆 <b>Periode : Juni 2026</b>
    """,
    unsafe_allow_html=True
)

# GARIS PEMBATAS
st.markdown("""
<hr style="
    margin-top:5px;
    margin-bottom:20px;
    border:1px solid #2d3748;
">
""", unsafe_allow_html=True)

# =========================
# KPI BARIS PERTAMA
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 PAGU ANGGARAN</div>
        <div class="kpi-value">{format_rupiah(pagu)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📝 RPD</div>
        <div class="kpi-value">{format_rupiah(rpd)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">✅ REALISASI</div>
        <div class="kpi-value">{format_rupiah(realisasi)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📈 PERSENTASE</div>
        <div class="kpi-value">{persentase:.2%}</div>
    </div>
    """, unsafe_allow_html=True)

# JARAK ANTAR BARIS
st.markdown("<br>", unsafe_allow_html=True)

# =========================
# KPI DEVIASI (FULL WIDTH)
# =========================

if deviasi < 0:
    st.markdown(f"""
    <div class="kpi-card-danger">
        <div class="kpi-title-danger">⚠️ DEVIASI</div>
        <div class="kpi-value-danger">{format_rupiah(deviasi)}</div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">✅ DEVIASI</div>
        <div class="kpi-value">{format_rupiah(deviasi)}</div>
    </div>
    """, unsafe_allow_html=True)

# Garis pemisah
st.markdown("---")

# Status Monitoring
st.subheader("🚨 Status Monitoring")

if deviasi >= 0:
    st.success(
        f"🟢 SESUAI TARGET | Kelebihan Realisasi {format_rupiah(deviasi)}"
    )

elif deviasi > -500000000:
    st.warning(
        f"🟡 PERLU PERHATIAN | Kekurangan Realisasi {format_rupiah(abs(deviasi))}"
    )

else:
    st.error(
        f"🔴 DI BAWAH TARGET | Kekurangan Realisasi {format_rupiah(abs(deviasi))}"
    )
# Grafik RPD vs Realisasi
st.markdown("---")

st.subheader("📊 Grafik RPD vs Realisasi")

st.caption(
    "Perbandingan target RPD dan Realisasi per Jenis Belanja"
)

grafik_df = pd.DataFrame({
    "Jenis Belanja": raw_sp2d.iloc[4:7, 13].values,
    "RPD": clean_numeric(raw_sp2d.iloc[4:7, 14]),
    "Realisasi": clean_numeric(raw_sp2d.iloc[4:7, 15])
})

# Ubah ke format panjang agar Plotly mudah membaca
grafik_long = grafik_df.melt(
    id_vars="Jenis Belanja",
    value_vars=["RPD", "Realisasi"],
    var_name="Kategori",
    value_name="Nilai"
)

fig = px.bar(
    grafik_long,
    x="Jenis Belanja",
    y="Nilai",
    color="Kategori",
    barmode="group",
    text="Nilai",
    color_discrete_map={
        "RPD": "#F59E0B",
        "Realisasi": "#3B82F6"
    }
)

# Format angka Indonesia dengan titik
for trace in fig.data:
    trace.text = [
        f"{float(str(x).replace('.','').replace(',','.')):,.0f}".replace(",", ".")
        if str(x).strip() != ""
        else "0"
        for x in trace.y
    ]

fig.update_traces(
    textposition="outside",
    cliponaxis=False
)

fig.update_layout(
    height=500,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    legend_title="",
    margin=dict(l=20,r=20,t=20,b=20),
    xaxis_title="",
    yaxis_title="",
    uniformtext_minsize=8,
    uniformtext_mode="hide"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)


with col1:

    st.subheader("📈 Capaian Realisasi (%)")

    persentase_raw = (
    raw_sp2d.iloc[11:19, 17]
    .astype(str)
    .str.extract(r'(\d+)')[0]
)

    capaian_df = pd.DataFrame({
    "Kluster": raw_sp2d.iloc[11:19, 13].values,
    "Persentase": clean_numeric(
        raw_sp2d.iloc[11:19, 17]
    )
})

    capaian_df = capaian_df.iloc[::-1]

    capaian_df["Label"] = (
        capaian_df["Persentase"]
        .round(0)
        .astype(int)
        .astype(str) + "%"
    )

    fig2 = px.bar(
        capaian_df,
        x="Persentase",
        y="Kluster",
        orientation="h",
        text="Label"
    )

    fig2.update_traces(
        marker_color="#60A5FA",
        textposition="outside",
        cliponaxis=False
    )

    fig2.update_layout(
        height=350,
        margin=dict(l=10, r=60, t=10, b=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            visible=False
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with col2:

    st.subheader("📉 Kekurangan Realisasi")

    kekurangan_df = pd.DataFrame({
    "Kluster": raw_sp2d.iloc[11:19, 13].values,
    "Kekurangan": -clean_numeric(
    raw_sp2d.iloc[11:19, 16]
).abs()
})

    kekurangan_df = kekurangan_df.iloc[::-1]
    
    # Format angka dengan titik
    kekurangan_df["Label"] = (
        kekurangan_df["Kekurangan"]
        .apply(lambda x: f"{x:,.0f}".replace(",", "."))
    )

    fig3 = px.bar(
    kekurangan_df,
    x="Kekurangan",
    y="Kluster",
    orientation="h",
    text="Label"
)

    fig3.update_traces(
    marker_color="#F97316",
    textposition="outside"
)

    fig3.update_layout(
    height=350,
    margin=dict(l=10, r=120, t=10, b=10),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    xaxis_title="",
    yaxis_title="",
    xaxis=dict(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
        visible=False
    )
)

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

st.markdown("---")

col3, col4 = st.columns([1.4, 1])

with col3:

    st.subheader("📋 Detail Realisasi per Kluster")

    detail_df = pd.DataFrame({
        "Kluster": raw_sp2d.iloc[22:31, 13].values,
        "51": clean_numeric(raw_sp2d.iloc[22:31, 14]),
        "52": clean_numeric(raw_sp2d.iloc[22:31, 15]),
        "57": clean_numeric(raw_sp2d.iloc[22:31, 16])
    })

    detail_df = detail_df[
        detail_df["Kluster"].notna()
    ]

    detail_df["Total"] = (
        detail_df["51"] +
        detail_df["52"] +
        detail_df["57"]
    )

    # Urutkan berdasarkan total terbesar
    detail_df = detail_df.sort_values(
        by="Total",
        ascending=False
    )

    detail_df_format = detail_df.copy()

    for col in ["51", "52", "57", "Total"]:

        detail_df_format[col] = detail_df_format[col].apply(
            lambda x:
            f"{int(x):,}".replace(",", ".")
            if x > 0
            else "-"
        )

    st.dataframe(
        detail_df_format,
        use_container_width=True,
        hide_index=True,
        height=320
    )


with col4:

    st.markdown("""
    <h2 style="
    text-align:center;
    color:white;
    margin-bottom:10px;
    ">
    📊 Komposisi Realisasi
    </h2>
    """, unsafe_allow_html=True)

    donut_df = pd.DataFrame({
    "Kategori": raw_sp2d.iloc[4:7, 13].values,
    "Nilai": clean_numeric(
        raw_sp2d.iloc[4:7, 15]
    )
})

    fig4 = px.pie(
        donut_df,
        names="Kategori",
        values="Nilai",
        hole=0.60,
        color="Kategori",
        color_discrete_map={
            "Belanja Pegawai (51)": "#1f77b4",
            "Belanja Barang Jasa (52)": "#9467bd",
            "Belanja Bansos (57)": "#2ca02c",
            "Belanja Pegawai": "#1f77b4",
            "Belanja Barang Jasa": "#9467bd",
            "Belanja Bansos": "#2ca02c"
        }
    )

    total_realisasi = donut_df["Nilai"].sum()

    nilai_tengah = (
        f"{total_realisasi/1000000000:.2f}"
        .replace(".", ",")
    )

    fig4.add_annotation(
        text=f"""
        <b>{nilai_tengah} M</b>
        <br>
        <span style='font-size:12px'>
        Realisasi
        </span>
        """,
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=22)
    )

    fig4.update_traces(
        textinfo="percent",
        textfont_size=14
    )

    fig4.update_layout(
        height=420,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.markdown(
        """
        <div style='text-align:center; font-size:14px; margin-top:-10px'>
            🟦 Belanja Pegawai (51)
            &nbsp;&nbsp;&nbsp;&nbsp;
            🟪 Belanja Barang Jasa (52)
            &nbsp;&nbsp;&nbsp;&nbsp;
            🟩 Belanja Bansos (57)
        </div>
        """,
        unsafe_allow_html=True
    )