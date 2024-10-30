import pandas as pd

# Di line 174, tambahkan kode berikut:
def get_service_points(selected_sp):
    # Baca file Excel
    df = pd.read_excel('sp_izin.xlsx', sheet_name='wilayah derivative')
    
    # Dapatkan level wilayah dari service point yang dipilih
    level = df[df['service_point'] == selected_sp]['Level_wilayah'].iloc[0]
    
    if level == 'kec':
        # Dapatkan nama kecamatan
        kecamatan = df[df['service_point'] == selected_sp]['kecamatan'].iloc[0]
        # Filter service points berdasarkan kecamatan
        result = df[df['kecamatan'] == kecamatan]['service_point'].tolist()
        
    elif level == 'Kota':
        # Dapatkan nama kota
        kota = df[df['service_point'] == selected_sp]['kota'].iloc[0]
        # Filter kecamatan berdasarkan kota
        kecamatan_list = df[df['kota'] == kota]['kecamatan'].unique()
        # Dapatkan semua service points dari kecamatan yang ada di kota tersebut
        result = df[df['kecamatan'].isin(kecamatan_list)]['service_point'].tolist()
    
    # Tampilkan hasil dalam format tabel
    result_df = pd.DataFrame(result, columns=['Service Points'])
    return result_df

# Gunakan fungsi
selected_service_point = 'nama_service_point_yang_dipilih'  # Ganti dengan service point yang dipilih
result_table = get_service_points(selected_service_point)
display(result_table) 