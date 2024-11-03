import pandas as pd
import streamlit as st
import plotly.graph_objects as go



# Set page config
st.set_page_config(page_title = "DPMPTSP Dashboard", layout="wide")


# Header
t1, t2 = st.columns((0.07,1))

# t1.image('images/dpmptsp_logo2.jpeg', width = 100)
t2.title('Dashboard Tipologi DPMPTSP Jakarta')
t2.markdown("**tel :** 1500164 / (021)1500164 **| website :** https://pelayanan.jakarta.go.id/ **")


with st.spinner('Updating Report .... ') : 

    # Metrics setting and rendering

    sp_izin_df = pd.read_excel('sp_izin.xlsx',sheet_name = 'service_point')
    sp = st.selectbox('Choose Service Point', sp_izin_df, help = 'Filter report to show only one service point of penanaman modal')

    # label logic : determine if kecamatan, kelurahan or kota
    if sp.startswith('Kantor Camat') : 
        level = 'kecamatan' 
    elif sp.startswith('Kantor Lurah') : 
        level = 'kelurahan'
    else :
        level = 'kota / kabupaten'

    # Data total izin berdasarkan status
    tot_status_df = pd.read_excel('sp_izin.xlsx', sheet_name = 'tot_status')
    total_izin = tot_status_df[tot_status_df['service_point']==sp]['total_diajukan']
    average_izin = tot_status_df[tot_status_df['service_point']==sp]['average_status']
    selesai_diproses = tot_status_df[tot_status_df['service_point']==sp]['total_selesai']
    ditolak_dibatalkan = tot_status_df[tot_status_df['service_point']==sp]['total_ditolak_dibatalkan']
    masih_diproses = tot_status_df[tot_status_df['service_point']==sp]['total_proses']

    # percentage
    selesai_perc = selesai_diproses / total_izin * 100
    ditolak_perc = ditolak_dibatalkan / total_izin * 100
    masih_perc = masih_diproses / total_izin * 100

    # total_izin = 597
    # average_izin = 712.1
    # selesai_diproses = 433
    # ditolak_dibatalkan = 163
    # masih_diproses = 1


    # Define layout using column in streamlit
    m1, m2, m3  = st.columns((1,1,1))
    m1.write('')
    m2.metric(label = "Total Izin yang diajukan", value = total_izin)
    m3.write(f"**In Average**")
    m3.write(f"{average_izin.iloc[0]} jumlah izin per {level.capitalize()}")
    m1.write('')
    m1.write('')

    # Layouting status lainnya yang belum masuk
    c3, c4, c5 = st.columns(3)
    c3.metric(label = "Selesai diproses", value = selesai_diproses, delta=f"{round(selesai_perc.iloc[0], 1)}%")
    c4.metric(label = "Masih diproses", value = masih_diproses, delta=f"{round(masih_perc.iloc[0], 1)}%")
    c5.metric(label = "Ditolak & dibatalkan", value = ditolak_dibatalkan, delta=f"{round(ditolak_perc.iloc[0], 1)}%")

    st.markdown("---x")
    st.markdown("---")
    st.markdown("---")

    # Layout untuk grafik piechart dan klasifikasi izin
    g1,g2 = st.columns((1,1))

    pcdf = pd.read_excel('sp_izin.xlsx', sheet_name = 'tot_bidang2')
    pcdf = pcdf[pcdf['service_point']==sp]

    fig1 = go.Figure(data = [go.Pie(labels =pcdf['bidang_recode'], values = pcdf['total_diajukan'], hole = .3, marker = dict(colors = ['#264653']))])
    fig1.update_layout(title_text = "Kategori Bidang yang Dominan", title_x = 0, margin = dict(l=0, r=10, b=10))

    cidf = pd.read_excel('sp_izin.xlsx', sheet_name = 'cluster')
    cidf = cidf[cidf['service_point']==sp]

    if not cidf.empty : 
        cluster_value = cidf['Cluster'].iloc[0]

        if cluster_value == 0 : 
            lvl_cluster = 'didominasi di Bidang **Pelayanan umum dan penataan ruang**, Bidang **Kesehatan** dan Bidang **Pelayanan Administrasi**'
        elif cluster_value == 1 :  
            lvl_cluster = 'didominasi hanya di Bidang **Pelayanan Administrasi**'
        elif cluster_value == 3 :  
            lvl_cluster = 'didominasi utama di Bidang **Kesehatan**'
        elif cluster_value == 4 :  
            lvl_cluster = 'menonjol pada bidang kesehatan yang lebih mendominasi dibandingkan cluster3'
        elif cluster_value == 6 :  
            lvl_cluster = 'didominasi utama di Bidang **Pelayanan Administrasi** dan bidang Kesbangpol'
        elif cluster_value == 7 :  
            lvl_cluster = 'cukup menyebar rata seperti Kesbangpol, Kesehatan, Lingkungan Hidup'
        else :
            lvl_cluster = 'tidak ditemukan cluster ini'

        g1.markdown(f"## <h2 style='color: blue;'> Cluster {cluster_value}</h2>", unsafe_allow_html = True)
        g1.markdown(f"### Cluster ini {lvl_cluster}")
        g2.plotly_chart(fig1, use_container_width = True)

    st.markdown("---")

    # terkait g3 utk pemohon, g4 utk yang dibawah g5 utk yang terakhir
    # pdf merupakan status pemohon apakah perushaaan atau individu
    g3 = st.columns(1)[0]
    pdf = pd.read_excel('sp_izin.xlsx', sheet_name = 'pemohon')
    pdf = pdf[pdf['service_point']==sp]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        y = pdf['service_point']
        , x=pdf['perorangan']
        , name = 'Perorangan'
        , orientation = 'h'
        , text = pdf['perorangan']
        , textposition = 'auto'
    ))
    fig2.add_trace(go.Bar(
        y = pdf['service_point']
        , x=pdf['perusahaan']
        , name = 'Perusahaan'
        , orientation = 'h'
        , text = pdf['perusahaan']
        , textposition = 'auto'
    ))

    fig2.update_layout(
        barmode = 'stack'
        , title = {
            'text'      : 'Tipe Pemohon berdasarkan izin : Perorangan vs Perusahaan'
            , 'x'         : 0.5
            , 'xanchor'   : 'center'
            , 'yanchor'   : 'top'
        }
        , height = 300
        , xaxis = {
            'showticklabels' : False
        }
    )

    g3.plotly_chart(fig2, use_container_width = True)

    g4 = st.columns(1)

    g5 = st.columns(1)


    st.markdown("---")
    st.markdown("---")
    st.markdown("---")
    st.markdown("---")
    # Metrics setting and rendering
    wdf = pd.read_excel('sp_izin.xlsx', sheet_name = 'wilayah_derivative')
    wdf = wdf[wdf['service_point']==sp]
    st.markdown("---"+sp)
    st.markdown("---"+wdf['service_point'])

    # sp_izin_df = pd.read_excel('sp_izin.xlsx',sheet_name = 'wilayah_derivative')
    # sp = st.selectbox('Choose Service Point', sp_izin_df, help = 'Filter report to show only one service point of penanaman modal')

    # Tentukan kolom `sub_region` berdasarkan level wilayah
    if level == 'kecamatan':
        sub_region_col = 'kelurahan'
    elif level == 'kota':
        sub_region_col = 'kecamatan'
    else:
        sub_region_col = 'kota'
    

    # Filter data untuk service_point yang dipilih
    # filtered_data = tot_status_df[tot_status_df['service_point'] == sp]

    # Hitung persentase `total_selesai` untuk setiap bidang di setiap `sub_region`
    # sub_region_data = (
    #     filtered_data.groupby([sub_region_col, 'service_point'])['total_selesai']
    #     .sum()
    #     .groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))  # Menghitung persentase
    #     .reset_index(name='percent_selesai')
    # )

    # # Buat grafik stack bar horizontal
    # fig = go.Figure()

    # # Tambahkan data ke grafik untuk setiap bidang recode
    # for bidang in sub_region_data['service_point'].unique():
    #     bidang_data = sub_region_data[sub_region_data['service_point'] == bidang]
    #     fig.add_trace(go.Bar(
    #         y=bidang_data[sub_region_col],
    #         x=bidang_data['percent_selesai'],
    #         name=bidang,
    #         orientation='h'
    #     ))

    # fig.update_layout(
    #     barmode='stack',
    #     title='Persentase Total Selesai per Bidang di Setiap Sub-Region',
    #     xaxis=dict(title='Persentase'),
    #     yaxis=dict(title=sub_region_col),
    #     height=500
    # )

    # # Tampilkan grafik di Streamlit
    # st.plotly_chart(fig, use_container_width=True)


# ... existing code ...
# ... kode yang ada sebelumnya ...

st.markdown("---")
st.markdown("## Distribusi Bidang Perizinan")

# Baca data wilayah
wdf = pd.read_excel('sp_izin.xlsx', sheet_name='wilayah_derivative')
selected_row = wdf[wdf['service_point'] == sp].iloc[0]
level_wilayah = selected_row['Level_wilayah']

# Color palette
colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
    '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
]

# Daftar kolom bidang
bidang_cols = ['Esdm', 'Kehutanan', 'Kelautan Dan Perikanan', 'Kepemudaan dan Keolahragaan',
               'Kesatuan Bangsa Dan Politik Dalam Negeri', 'Kesehatan', 
               'Ketenteraman, ketertiban Umum dan Pelindungan Masyarakat',
               'Lingkungan Hidup', 'Pariwisata', 'Pekerjaan Umum Dan Penataan Ruang',
               'Pelayanan Administrasi', 'Pendidikan', 'Perdagangan', 'Perhubungan',
               'Pertanahan Yang Menjadi Kewenangan Daerah', 'Pertanian',
               'Perumahan Rakyat Dan Kawasan Permukiman', 'Sosial', 'Tenaga Kerja']

if level_wilayah == 'Kel':
    st.info("Data sama dengan Pie Chart diatas")

elif level_wilayah == 'Kota':
    # Data untuk level kota
    kota = selected_row['kota']
    kota_data = wdf[wdf['kota'] == kota]
    agg_data = kota_data.groupby('kecamatan')[bidang_cols].sum().reset_index()
    agg_data['total'] = agg_data[bidang_cols].sum(axis=1)
    
    fig = go.Figure()
    color_idx = 0
    for bidang in bidang_cols:
        if agg_data[bidang].sum() > 0:
            fig.add_trace(go.Bar(
                y=agg_data['kecamatan'],
                x=agg_data[bidang] / agg_data['total'] * 100,
                name=bidang,
                orientation='h',
                text=[f'{x:.1f}% ({int(y)})' for x, y in zip(agg_data[bidang] / agg_data['total'] * 100, agg_data[bidang])],
                textposition='inside',
                marker_color=colors[color_idx % len(colors)],
                legendgroup=bidang,
                showlegend=True
            ))
            color_idx += 1
    title_text = f'Distribusi Bidang Perizinan di Kota {kota}'

elif level_wilayah == 'Kec':
    # Data untuk level kecamatan
    kecamatan = selected_row['kecamatan']
    kec_data = wdf[wdf['kecamatan'] == kecamatan]
    kec_data['total'] = kec_data[bidang_cols].sum(axis=1)
    
    fig = go.Figure()
    color_idx = 0
    for bidang in bidang_cols:
        if kec_data[bidang].sum() > 0:
            # Tangani nilai NaN dengan mengubah ke 0
            values = kec_data[bidang].fillna(0)
            percentages = (values / kec_data['total'] * 100).fillna(0)
            
            fig.add_trace(go.Bar(
                y=kec_data['service_point'],
                x=percentages,
                name=bidang,
                orientation='h',
                text=[f'{x:.1f}% ({int(y)})' if not pd.isna(y) else '0% (0)' 
                      for x, y in zip(percentages, values)],
                textposition='inside',
                marker_color=colors[color_idx % len(colors)],
                legendgroup=bidang,
                showlegend=True
            ))
            color_idx += 1
    title_text = f'Distribusi Bidang Perizinan di Kecamatan {kecamatan}'

if level_wilayah != 'Kel':
    # Pengaturan layout grafik
    fig.update_layout(
        barmode='stack',
        title=title_text,
        xaxis_title='Persentase (%)',
        height=800,  # Tinggi grafik diperbesar
        bargap=0.2,  # Jarak antar bar
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.3)',
            borderwidth=1,
            itemsizing='constant',
            itemwidth=40
        ),
        margin=dict(b=200),  # Margin bawah untuk legend
        uniformtext=dict(mode='hide', minsize=8)
    )

    # Tambahkan button untuk toggle legend
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"visible": [True] * len(fig.data)}],
                        label="Show All",
                        method="restyle"
                    ),
                    dict(
                        args=[{"visible": [False] * len(fig.data)}],
                        label="Hide All",
                        method="restyle"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.11,
                xanchor="left",
                y=1.1,
                yanchor="top"
            ),
        ]
    )

    st.plotly_chart(fig, use_container_width=True)