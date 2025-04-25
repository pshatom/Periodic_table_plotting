import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Set page config to wide mode to reduce margins
st.set_page_config(layout="wide")

# App title with EleMap branding
st.markdown("""
# <span style='color:#4285F4;'>Ele</span><span style='color:#EA4335;'>Map</span> 🧪
## Interactive Periodic Table Property Visualizer
""", unsafe_allow_html=True)

st.markdown("Upload a CSV with **2 columns**: `Element` and a numeric `Property`. Select the desired periodic table range and settings to generate the heatmap.")

# Row 1: Upload & Colormap
col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
with col2:
    colormap = st.selectbox("Colormap", sorted(plt.colormaps()), index=plt.colormaps().index("coolwarm"))

# Row 2: Group Start-End
col3, col4 = st.columns(2)
group_start = col3.number_input("Group start", min_value=1, max_value=18, value=1)
group_end = col4.number_input("Group end", min_value=1, max_value=18, value=18)

# Row 3: Period Start-End
col5, col6 = st.columns(2)
period_start = col5.number_input("Period start (1-9, where 8=La, 9=Ac)", min_value=1, max_value=9, value=1)
period_end = col6.number_input("Period end (1-9, where 8=La, 9=Ac)", min_value=1, max_value=9, value=7)

# Row 4: Format and DPI
col7, col8 = st.columns(2)
export_format = col7.selectbox("Image format", ["png", "svg", "tiff"])
dpi_value = col8.selectbox("Quality (DPI)", [300, 600, 900, 1200], index=0)

# Use custom CSS to reduce margins and add branding elements
st.markdown("""
<style>
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 90%;
    }
    .css-18e3th9 {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    /* EleMap branding styles */
    .stApp {
        background: linear-gradient(to bottom right, #f8f9fa, #e9ecef);
    }
    h1 {
        font-size: 3rem !important;
        font-weight: 700 !important;
        letter-spacing: -1px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    h2 {
        margin-top: -0.5rem !important;
        font-weight: 400 !important;
        color: #555;
    }
    .stButton button {
        background-color: #4285F4 !important;
        color: white !important;
        font-weight: 500 !important;
    }
    .stButton button:hover {
        background-color: #3367d6 !important;
    }
    /* Fix for matplotlib figure */
    .stPlotlyChart, .stImage, .main > div[data-testid="stImage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex;
        justify-content: center;
    }
    /* Remove the white background from plots */
    .main svg, .main img {
        background: transparent !important;
    }
    /* Custom pyplot settings */
    [data-testid="stDecoration"], [data-testid="stDecoration"] + div {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Periodic table layout
elements_matrix = [
    ['H',  None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'He'],
    ['Li', 'Be', None, None, None, None, None, None, None, None, None, None, 'B', 'C', 'N', 'O', 'F', 'Ne'],
    ['Na', 'Mg', None, None, None, None, None, None, None, None, None, None, 'Al', 'Si', 'P', 'S', 'Cl', 'Ar'],
    ['K',  'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr'],
    ['Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe'],
    ['Cs', 'Ba', None, 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn'],
    ['Fr', 'Ra', None, 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'],
    [None, None, None, 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'],
    [None, None, None, 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr']
]
group_labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
period_labels = ['1', '2', '3', '4', '5', '6', '7', 'La', 'Ac']

# Add a small footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About EleMap")
st.sidebar.markdown("EleMap helps chemists and researchers visualize periodic trends and element properties.")

# Process only if file is uploaded
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, skipinitialspace=True)
        if df.shape[1] != 2:
            st.error("CSV must have exactly two columns: [Element, Property]")
        else:
            prop_name = df.columns[1]
            elements_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
            
            # Group and period filtering
            group_idx = [i for i, g in enumerate(group_labels) if group_start <= int(g) <= group_end]
            period_idx = []
            for i, p in enumerate(period_labels):
                if (p.isdigit() and period_start <= int(p) <= period_end) or (p == 'La' and 8 in range(period_start, period_end+1)) or (p == 'Ac' and 9 in range(period_start, period_end+1)):
                    period_idx.append(i)
                    
            cropped_matrix = []
            for row_idx in period_idx:
                row = elements_matrix[row_idx]
                filtered_row = [row[i] if i in group_idx else None for i in range(len(row))]
                cropped_matrix.append([elem for i, elem in enumerate(filtered_row) if i in group_idx])
                
            # Value grid
            value_grid = np.full((len(cropped_matrix), len(cropped_matrix[0])), np.nan)
            for i, row in enumerate(cropped_matrix):
                for j, element in enumerate(row):
                    if element and element in elements_dict:
                        try:
                            val = float(elements_dict[element])
                            if not np.isnan(val):
                                value_grid[i, j] = val
                        except:
                            continue
                            
            if np.isnan(value_grid).all():
                st.warning("⚠️ No valid property values found in the selected range.")
            else:
                # Use full width of the page for the figure
                fig_width = 1.5 * len(cropped_matrix[0])
                fig_height = 1.2 * len(cropped_matrix)
                
                # Create figure with transparent background and no extra padding
                plt.rcParams['figure.facecolor'] = 'none'
                plt.rcParams['axes.facecolor'] = 'none'
                fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='none')
                
                # Remove all figure padding
                fig.tight_layout(pad=0)
                fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
                
                # Plot the heatmap
                cmap = plt.get_cmap(colormap)
                cax = ax.matshow(value_grid, cmap=cmap, vmin=np.nanmin(value_grid), vmax=np.nanmax(value_grid))
                cbar = fig.colorbar(cax, ax=ax, label=f"{prop_name}", fraction=0.025, pad=0.04)
                # Increase font size for colorbar label and ticks
                cbar.ax.tick_params(labelsize=20)  # Adjust tick font size
                cbar.set_label(f"{prop_name}", fontsize=20)  # Adjust label font size
                
                # Add EleMap watermark to plot
                plt.figtext(0.02, 0.02, "EleMap", fontsize=14, color='gray', alpha=0.5)
                
                for i, row in enumerate(cropped_matrix):
                    for j, element in enumerate(row):
                        if element:
                            val = elements_dict.get(element, np.nan)
                            label = element if pd.isna(val) else f"{element}\n{int(float(val))}"
                            ax.text(j, i, label, ha='center', va='center', fontsize=16, color='white')
                
                # Group/Period Labels with larger font
                ax.set_xticks(np.arange(len(group_idx)))
                ax.set_xticklabels([group_labels[i] for i in group_idx], fontsize=20)
                ax.set_yticks(np.arange(len(period_idx)))
                ax.set_yticklabels([period_labels[i] for i in period_idx], fontsize=20)
                ax.spines[:].set_visible(False)
                ax.xaxis.set_ticks_position('none')
                ax.yaxis.set_ticks_position('none')
                
                # Display the plot using the full width of the page
                st.pyplot(fig, use_container_width=True)
                
                # Save + download
                buffer = BytesIO()
                # Save with transparent background
                fig.savefig(buffer, format=export_format, dpi=dpi_value, bbox_inches='tight', facecolor='none', transparent=True)
                buffer.seek(0)
                st.download_button(
                    label=f"📥 Download as {export_format.upper()} ({dpi_value} dpi)",
                    data=buffer,
                    file_name=f"elemap_periodic_table.{export_format}",
                    mime=f"image/{'svg+xml' if export_format == 'svg' else export_format}"
                )
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    # Display a sample image or instructions when no file is uploaded
    st.info("👆 Upload a CSV file to start visualizing element properties. Your file should have exactly two columns: Element symbols and their corresponding property values.")
    
    # Display example data format
    st.markdown("### Example CSV format:")
    example = pd.DataFrame({
        "Element": ["H", "He", "Li", "Be", "B"],
        "Electronegativity": [2.20, 0.00, 0.98, 1.57, 2.04]
    })
    st.dataframe(example)
