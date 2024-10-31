import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load data from the two sheets
file_path = 'sp_izin.xlsx'
service_point_data = pd.read_excel(file_path, sheet_name='service_point')
tot_status_data = pd.read_excel(file_path, sheet_name='tot_status')

# Convert relevant columns to string to avoid matching issues
service_point_data['kota'] = service_point_data['kota'].astype(str)
service_point_data['kecamatan'] = service_point_data['kecamatan'].astype(str)
service_point_data['kelurahan'] = service_point_data['kelurahan'].astype(str)
service_point_data['service_point'] = service_point_data['service_point'].astype(str)

# Sidebar for level selection with default Kota selection
st.sidebar.header("Select Level and Service Point")

# Set default selection for Kota as 'Wilayah Jakarta'
selected_kota = st.sidebar.selectbox("Kota", service_point_data['kota'].unique(), index=service_point_data['kota'].tolist().index("Wilayah Jakarta"))

# Set Kecamatan, Kelurahan, and Service Point options to be blank initially
kecamatan_options = service_point_data[service_point_data['kota'] == selected_kota]['kecamatan'].unique()
selected_kecamatan = st.sidebar.selectbox("Kecamatan", ["-"] + list(kecamatan_options))

# Filter Kelurahan options based on selected Kecamatan
if selected_kecamatan and selected_kecamatan != "-":
    kelurahan_options = service_point_data[(service_point_data['kota'] == selected_kota) & 
                                           (service_point_data['kecamatan'] == selected_kecamatan)]['kelurahan'].unique()
else:
    kelurahan_options = []

selected_kelurahan = st.sidebar.selectbox("Kelurahan", ["-"] + list(kelurahan_options))

# Filter Service Point options based on selected Kelurahan or directly under Kota if no lower levels are chosen
if selected_kelurahan and selected_kelurahan != "-":
    service_point_options = service_point_data[(service_point_data['kota'] == selected_kota) & 
                                               (service_point_data['kecamatan'] == selected_kecamatan) &
                                               (service_point_data['kelurahan'] == selected_kelurahan)]['service_point'].unique()
elif selected_kecamatan and selected_kecamatan != "-":
    service_point_options = service_point_data[(service_point_data['kota'] == selected_kota) & 
                                               (service_point_data['kecamatan'] == selected_kecamatan)]['service_point'].unique()
else:
    # When only Kota is selected, show all service points under the selected Kota
    service_point_options = service_point_data[service_point_data['kota'] == selected_kota]['service_point'].unique()

selected_service_point = st.sidebar.selectbox("service_point", ["-"] + list(service_point_options))

# Function to plot stacked bar chart with enhanced readability
def plot_stacked_bar_chart(level, filter_value):        
    # Select appropriate data from tot_status based on the level
    if level == "Kota":
        # Aggregate data for all rows under the selected Kota
        selected_data = tot_status_data[tot_status_data['kota'] == filter_value]
    elif level == "Kecamatan":
        # Aggregate data for all rows under the selected Kecamatan within the chosen Kota
        selected_data = tot_status_data[(tot_status_data['kota'] == selected_kota) & 
                                        (tot_status_data['kecamatan'] == filter_value)]
    elif level == "Kelurahan":
        # Aggregate data for all rows under the selected Kelurahan within the chosen Kota and Kecamatan
        selected_data = tot_status_data[(tot_status_data['kota'] == selected_kota) & 
                                        (tot_status_data['kecamatan'] == selected_kecamatan) &
                                        (tot_status_data['kelurahan'] == filter_value)]
    else:
        # Filter by all levels down to the Service Point
        selected_data = tot_status_data[(tot_status_data['kota'] == selected_kota) & 
                                        (tot_status_data['kecamatan'] == selected_kecamatan) &
                                        (tot_status_data['kelurahan'] == selected_kelurahan) &
                                        (tot_status_data['service_point'] == filter_value)]

    # Aggregate columns of interest and calculate percentage if there are multiple rows
    columns_to_plot = ['total_selesai', 'total_proses', 'total_ditolak_dibatalkan']
    aggregated_values = selected_data[columns_to_plot].sum()
    total_diajukan_sum = selected_data['total_diajukan'].sum()  # Baseline for calculating percentages

    if total_diajukan_sum > 0:
        percentage_values = (aggregated_values / total_diajukan_sum) * 100

        # Enhanced stacked bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#4CAF50', '#2196F3', '#FF9800']  # Colors for each category
        bars = ax.barh(aggregated_values.index, aggregated_values, color=colors)

        # Adding text labels on each bar
        for bar, value, pct in zip(bars, aggregated_values, percentage_values):
            ax.text(value + 1, bar.get_y() + bar.get_height() / 2, f"{value} ({pct:.2f}%)", va='center', ha='left')

        # Labels and title
        ax.set_xlabel("Total Pengajuan")
        ax.set_title(f"Service Status Distribution for {filter_value} ({level})")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        # Display message if no data is available for the selected filter
        st.write(f"No data available for {filter_value} at the {level} level.")

# Determine the appropriate level and plot chart
if selected_service_point and selected_service_point != "-":
    plot_stacked_bar_chart("Service Point", selected_service_point)
elif selected_kelurahan and selected_kelurahan != "-":
    plot_stacked_bar_chart("Kelurahan", selected_kelurahan)
elif selected_kecamatan and selected_kecamatan != "-":
    plot_stacked_bar_chart("Kecamatan", selected_kecamatan)
else:
    plot_stacked_bar_chart("Kota", selected_kota)