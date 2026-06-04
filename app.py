import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="USA Sales Report",
    layout="wide",
    page_icon="🇺🇸",
    initial_sidebar_state="expanded"
)

# ── Global CSS (gold/dark theme, sticky table headers, no sidebar line) ────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg-base:        #0A0A0A;
        --bg-panel:       #111111;
        --border-dark:    rgba(212, 175, 55, 0.12);
        --border-bright:  rgba(212, 175, 55, 0.35);
        --gold:           #D4AF37;
        --gold-light:     #F1C40F;
        --gold-dim:       rgba(212, 175, 55, 0.60);
        --accent:         #E67E22;
        --sidebar-text:   #B0B0B0;
        --sidebar-accent: #D4AF37;
    }

    * { font-family: 'Outfit', sans-serif; box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-base) !important;
    }

    /* ── Dot-grid background ──────────────────────────────────────────── */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed; inset: 0;
        background-image: radial-gradient(circle, rgba(212,175,55,0.03) 1px, transparent 1px);
        background-size: 28px 28px;
        pointer-events: none;
        z-index: 0;
    }

    /* ── Hide ALL Streamlit chrome ────────────────────────────────────── */
    #MainMenu                          { visibility: hidden !important; display: none !important; }
    footer                             { visibility: hidden !important; display: none !important; }
    header                             { visibility: hidden !important; display: none !important; }
    [data-testid="stToolbar"]          { display: none !important; }
    [data-testid="stDecoration"]       { display: none !important; }
    [data-testid="stStatusWidget"]     { display: none !important; }
    [data-testid="manage-app-button"]  { display: none !important; }
    .viewerBadge_container__r5tak     { display: none !important; }
    .viewerBadge_link__qRIco          { display: none !important; }
    [data-testid="baseButton-header"]  { display: none !important; }
    button[kind="header"]              { display: none !important; }
    .stDeployButton                    { display: none !important; }
    ._profileContainer_gzau3_53       { display: none !important; }

    /* ── Sidebar collapse/expand tab ──────────────────────────────────── */
    [data-testid="collapsedControl"] {
        top: 10px !important;
        height: 32px !important;
        width: 20px !important;
    }
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button {
        width: 32px !important;
        height: 32px !important;
        border-radius: 8px !important;
        background: linear-gradient(135deg, #1A1A1A 0%, #0E0E0E 100%) !important;
        border: 1px solid rgba(212, 175, 55, 0.45) !important;
        box-shadow: 0 2px 12px rgba(212, 175, 55, 0.18) !important;
        color: #D4AF37 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="collapsedControl"] button:hover,
    [data-testid="stSidebarCollapseButton"] button:hover {
        border-color: #F1C40F !important;
        box-shadow: 0 4px 20px rgba(212, 175, 55, 0.40) !important;
        background: linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%) !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg {
        stroke: #D4AF37 !important;
        fill: none !important;
    }
    [data-testid="stSidebarCollapseButton"] { top: 10px !important; }
    [data-testid="stSidebar"] > div:first-child { padding-top: 54px !important; }

    /* ── Report title ── */
    .report-title {
        background: linear-gradient(135deg, #1A1A1A 0%, #0E0E0E 100%);
        color: #D4AF37;
        padding: 18px 28px;
        border-radius: 12px;
        text-align: center;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 14px;
        border: 1px solid var(--border-bright);
        box-shadow: 0 8px 30px rgba(0,0,0,0.8), 0 0 15px rgba(212,175,55,0.15);
        position: relative;
        overflow: hidden;
    }
    .report-title::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #D4AF37, #F1C40F, #E67E22, transparent);
    }
    .report-subtitle {
        font-size: 13px;
        color: var(--gold-dim);
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 500;
        font-family: 'Outfit', sans-serif;
    }

    /* ── KPI cards ────────────────────────────────────────────────────── */
    .kpi-card {
        background: linear-gradient(145deg, #1A1A1A 0%, #101010 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 12px;
        padding: 18px 16px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(0,0,0,0.7), 0 0 8px rgba(212,175,55,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(212,175,55,0.2);
    }
    .kpi-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #D4AF37, #F1C40F, transparent);
    }
    .kpi-icon   { font-size: 20px; margin-bottom: 5px; }
    .kpi-label  {
        font-size: 10px; font-weight: 700; letter-spacing: 2px;
        text-transform: uppercase; color: #FFFFFF; margin-bottom: 5px;
    }
    .kpi-value  {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 32px; font-weight: 900;
        letter-spacing: 2px; color: #D4AF37; line-height: 1;
    }

    /* ── Section headings ── */
    .section-heading {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 22px;
        color: #D4AF37;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(212,175,55,0.2);
    }

    /* ── Card title (table header bar) ───────────────────────────────── */
    .card-title {
        background: #1C1C1C;
        color: #D4AF37;
        padding: 9px 16px;
        border-radius: 10px 10px 0 0;
        font-size: 11px; font-weight: 900;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        text-align: center;
        border: 1px solid rgba(212,175,55,0.25);
        border-bottom: 1px solid rgba(212,175,55,0.15);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }

    /* ══════════════════════════════════════════════════════════════════
       Gold‑theme HTML tables – with STICKY HEADERS
       ══════════════════════════════════════════════════════════════════ */
    .table-scroll {
        overflow-y: auto;
        border: 1px solid rgba(212,175,55,0.2);
        border-top: none;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 6px 22px rgba(0,0,0,0.6);
        margin-bottom: 0;
    }
    .table-scroll table {
        width: 100%;
        border-collapse: collapse;
        table-layout: auto;
        font-family: 'Outfit', sans-serif;
        font-size: 13px;
        font-weight: 800;
        color: #FFFFFF;
        background: #131313;
    }
    .table-scroll th {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 12.5px !important;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        padding: 10px 12px;
        text-align: left !important;
        white-space: nowrap;
        /* ── Clean look & STICKY ── */
        border: none !important;
        position: sticky;
        top: 0;
        z-index: 2;
    }
    .table-scroll th:not(:first-child) { text-align: center !important; }

    .table-scroll td {
        padding: 7px 12px;
        border-bottom: 1px solid rgba(212,175,55,0.10);
        border-right: 1px solid rgba(212,175,55,0.10);
        font-weight: 800;
        font-size: 13px;
        text-align: left;
        color: #FFFFFF;
        white-space: nowrap;
    }
    .table-scroll td:last-child { border-right: none; }

    /* Numeric columns (2nd onwards) — gold + centered */
    .table-scroll td:not(:first-child) {
        text-align: center;
        font-weight: 900;
        color: #D4AF37;
    }

    .table-scroll tr:nth-child(even) td { background-color: #191919; }
    .table-scroll tr:nth-child(odd)  td { background-color: #131313; }
    .table-scroll tr:hover td {
        background-color: #2A2A2A !important;
        color: #F1C40F !important;
    }

    /* ── Sidebar (no vertical line) ────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0C0C0C 0%, #0A0A0A 100%) !important;
        border-right: none !important;
    }
    [data-testid="stAppViewContainer"] { border-right: none !important; }
    [data-testid="stMain"]            { border-right: none !important; }
    .block-container                  { border-right: none !important; }

    [data-testid="stSidebar"] * { color: var(--sidebar-text) !important; }
    [data-testid="stSidebar"] h3 {
        color: var(--sidebar-accent) !important;
        font-size: 11px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] strong { color: #E6C300 !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stRadio label {
        color: var(--gold-dim) !important;
        font-weight: 600 !important;
        font-size: 10px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #888 !important;
        font-size: 11px !important;
    }
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiSelect"] > div > div {
        background: #1A1A1A !important;
        border: 1px solid var(--border-dark) !important;
        color: #D4AF37 !important;
        border-radius: 8px !important;
        font-size: 12px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1A1A1A 0%, #0E0E0E 100%) !important;
        color: var(--gold-light) !important;
        border: 1px solid var(--border-bright) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        box-shadow: 0 2px 10px rgba(212,175,55,0.12) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%) !important;
        box-shadow: 0 4px 18px rgba(212,175,55,0.30) !important;
        border-color: var(--gold-light) !important;
    }

    [data-testid="stFileUploader"] {
        background: #1A1A1A !important;
        border: 2px dashed rgba(212,175,55,0.25) !important;
        border-radius: 12px !important;
        padding: 28px !important;
    }
    [data-testid="stAlert"] {
        background: #1A1A1A !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: 8px !important;
        color: var(--sidebar-text) !important;
    }

    .stat-pill {
        background: #1A1A1A;
        border: 1px solid var(--border-dark);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 11px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
    }
    .stat-pill span:first-child { color: #999; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; }
    .stat-pill span:last-child  { font-weight: 700; color: var(--gold-light); }

    hr { border-color: var(--border-dark) !important; margin: 12px 0 !important; }
    p, .stMarkdown p { color: var(--sidebar-text) !important; font-size: 12px !important; }
    label { color: var(--gold-dim) !important; }

    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #0A0A0A; }
    ::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.25); border-radius: 2px; }

    .block-container { padding: 3.5rem 1rem 0.5rem; }
    div[data-testid="stVerticalBlock"] > div { margin-top: 0; padding-top: 0; }
    .stColumn { padding: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Keyboard shortcut: R = open sidebar, O = close sidebar ──────────────────
components.html("""
<script>
(function() {
    function clickSidebarToggle(action) {
        const doc = window.parent.document;
        if (action === 'open') {
            const expandBtn = doc.querySelector('[data-testid="collapsedControl"] button');
            if (expandBtn) { expandBtn.click(); return; }
        }
        if (action === 'close') {
            const collapseBtn = doc.querySelector('[data-testid="stSidebarCollapseButton"] button');
            if (collapseBtn) { collapseBtn.click(); return; }
        }
    }
    window.parent.document.addEventListener('keydown', function(e) {
        const tag = e.target.tagName;
        if (tag === 'INPUT' || tag === 'TEXTAREA' || e.target.isContentEditable) return;
        if (e.key === 'r' || e.key === 'R') { clickSidebarToggle('open');  }
        if (e.key === 'o' || e.key === 'O') { clickSidebarToggle('close'); }
    });
})();
</script>
""", height=0)

# ── Chart palette / layout helpers ───────────────────────────────────────────
GOLD_PALETTE = [
    "#D4AF37", "#F1C40F", "#E67E22", "#E6B800", "#C0932F",
    "#F4A261", "#E9C46A", "#2A9D8F", "#3EAFBD", "#52C4C0",
    "#95D5B2", "#B7E4C7", "#457B9D", "#264653", "#6D3A7C"
]

PLOT_BG    = "#0F0F0F"
PAPER_BG   = "#0F0F0F"
GRID_COLOR = "rgba(212,175,55,0.07)"
AXIS_COLOR = "rgba(212,175,55,0.3)"
TEXT_COLOR = "#C8C8C8"
TITLE_COLOR = "#D4AF37"

AXIS_FONT  = dict(size=12, color=TEXT_COLOR,  family="Outfit, sans-serif")
TICK_FONT  = dict(size=11, color=TEXT_COLOR,  family="Outfit, sans-serif")
TITLE_FONT = dict(size=15, color=TITLE_COLOR, family="Outfit, sans-serif")


def _dark_layout(fig, xaxis_title, yaxis_title, extra_xaxis=None, height=500):
    xax = dict(
        title=dict(text=xaxis_title, font=AXIS_FONT, standoff=12),
        tickfont=TICK_FONT,
        tickangle=-90,
        linecolor=AXIS_COLOR,
        linewidth=1,
        showgrid=False,
        ticks="outside",
        ticklen=4,
        tickcolor=AXIS_COLOR,
        automargin=True,
    )
    if extra_xaxis:
        xax.update(extra_xaxis)

    fig.update_layout(
        height=height,
        font=dict(family="Outfit, sans-serif", size=11, color=TEXT_COLOR),
        title_font=TITLE_FONT,
        title_x=0.5,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        margin=dict(t=70, b=140, l=70, r=30),
        xaxis=xax,
        yaxis=dict(
            title=dict(text=yaxis_title, font=AXIS_FONT, standoff=10),
            tickfont=TICK_FONT,
            linecolor=AXIS_COLOR,
            linewidth=1,
            gridcolor=GRID_COLOR,
            gridwidth=1,
            zeroline=False,
        ),
        coloraxis_showscale=False,
        showlegend=False,
    )
    fig.update_traces(
        textfont=dict(size=10, color="#ffffff", family="Outfit, sans-serif"),
        textangle=0,
        textposition="outside",
        cliponaxis=False,
    )
    return fig


# ── HTML table renderer (gold/dark theme, sticky headers already in CSS) ─────
def show_html_table(table_data, display_name, table_height=420):
    """Render a distribution table using the same gold/dark HTML theme
    as the Brand Sales Dashboard — replaces st.dataframe()."""
    if table_data.empty:
        st.info(f"No data for {display_name}")
        return

    display_df = table_data.copy()

    # Rename internal column names → friendly display names
    display_df = display_df.rename(columns={
        'INITIAL_QTY':      'Initial Qty',
        'TOTAL_QTY':        'Total Qty Sold',
        'BALANCE':          'Balance Qty',
        'SALES_PERCENTAGE': 'Sales %',
    })

    # Format numeric columns
    display_df['Initial Qty']    = display_df['Initial Qty'].apply(lambda x: f"{int(x):,}")
    display_df['Total Qty Sold'] = display_df['Total Qty Sold'].apply(lambda x: f"{int(x):,}")
    display_df['Balance Qty']    = display_df['Balance Qty'].apply(lambda x: f"{int(x):,}")
    display_df['Sales %']        = display_df['Sales %'].apply(lambda x: f"{x:.1f}%")

    html = display_df.to_html(index=False, escape=False, border=0)
    st.markdown(
        f'<div class="table-scroll" style="max-height:{table_height}px;">{html}</div>',
        unsafe_allow_html=True
    )


# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="report-title">
    🇺🇸  USA Sales Report
    <div class="report-subtitle" style="font-size:13px;letter-spacing:3px;color:rgba(212,175,55,0.6);
         font-family:'Outfit',sans-serif;font-weight:500;margin-top:4px;">
        Comprehensive Sales Analytics Dashboard · Apr 2026
    </div>
</div>
<hr>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Excel File with Sheets 'A' and 'B'",
    type=['xlsx', 'xls']
)


# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def load_and_process_data(uploaded_file):
    try:
        sheet_a = pd.read_excel(uploaded_file, sheet_name='A')
        sheet_b = pd.read_excel(uploaded_file, sheet_name='B')
        sheet_a.columns = sheet_a.columns.astype(str).str.strip()
        sheet_b.columns = sheet_b.columns.astype(str).str.strip()

        def find_column(df, possible_names):
            df_cols_upper = {col.upper().strip(): col for col in df.columns}
            for name in possible_names:
                if name.upper().strip() in df_cols_upper:
                    return df_cols_upper[name.upper().strip()]
            return None

        # ── Sheet A ────────────────────────────────────────────────────────
        season_col      = find_column(sheet_a, ['SEASON', 'Season'])
        brand_col       = find_column(sheet_a, ['BRAND', 'Brand'])
        category_col    = find_column(sheet_a, ['CATEGORY', 'Category'])
        subcategory_col = find_column(sheet_a, ['Subcategory', 'SUBCATEGORY', 'Sub Category'])
        style_names_col = find_column(sheet_a, ['STYLE NAMES', 'Style Names', 'STYLE_NAMES'])
        style_no_col    = find_column(sheet_a, ['STYLE NO.', 'STYLE NO', 'Style No', 'STYLE_NUMBER'])
        color_col       = find_column(sheet_a, ['COLOR', 'Color'])
        colab_col_a     = find_column(sheet_a, ['COLAB', 'Colab'])
        initial_qty_col = find_column(sheet_a, ['INITIAL QTY', 'Initial Qty', 'INITIAL_QTY'])
        total_qty_col   = find_column(sheet_a, ['Total Qty', 'TOTAL QTY', 'Total_Qty'])
        balance_col     = find_column(sheet_a, ['Balance', 'BALANCE'])

        required_cols_a = {
            'BRAND': brand_col, 'SEASON': season_col, 'CATEGORY': category_col,
            'Subcategory': subcategory_col, 'COLOR': color_col, 'COLAB': colab_col_a,
            'INITIAL QTY': initial_qty_col, 'Total Qty': total_qty_col, 'Balance': balance_col
        }
        missing_a = [k for k, v in required_cols_a.items() if v is None]
        if missing_a:
            st.error(f"❌ Missing required columns in Sheet A: {', '.join(missing_a)}")
            st.info("Available columns in Sheet A: " + ", ".join(sheet_a.columns))
            st.stop()

        sheet_a_clean = pd.DataFrame({
            'SEASON':      sheet_a[season_col].astype(str).str.strip().str.upper(),
            'BRAND':       sheet_a[brand_col].astype(str).str.strip().str.upper(),
            'CATEGORY':    sheet_a[category_col].astype(str).str.strip().str.upper() if category_col else 'N/A',
            'SUBCATEGORY': sheet_a[subcategory_col].astype(str).str.strip().str.upper() if subcategory_col else 'N/A',
            'STYLE_NAMES': sheet_a[style_names_col].astype(str).str.strip().str.upper() if style_names_col else 'N/A',
            'STYLE_NO':    sheet_a[style_no_col].astype(str).str.strip().str.upper() if style_no_col else 'N/A',
            'COLOR':       sheet_a[color_col].astype(str).str.strip().str.upper(),
            'COLAB':       sheet_a[colab_col_a].astype(str).str.strip().str.upper(),
            'INITIAL_QTY': pd.to_numeric(sheet_a[initial_qty_col], errors='coerce').fillna(0),
            'TOTAL_QTY':   pd.to_numeric(sheet_a[total_qty_col], errors='coerce').fillna(0),
            'BALANCE':     pd.to_numeric(sheet_a[balance_col], errors='coerce').fillna(0)
        })
        sheet_a_unique = sheet_a_clean.drop_duplicates(subset=['COLAB'], keep='first')

        # ── Sheet B ────────────────────────────────────────────────────────
        website_col    = find_column(sheet_b, ['WEBSITE', 'Website'])
        sku_col        = find_column(sheet_b, ['SKU', 'Sku'])
        size_col       = find_column(sheet_b, ['SIZE (US)', 'SIZE', 'Size US', 'Size'])
        qty_col        = find_column(sheet_b, ['QTY', 'Qty', 'Quantity'])
        order_date_col = find_column(sheet_b, ['ORDER RECV DATE', 'Order Recv Date', 'ORDER_DATE'])
        colab_col_b    = find_column(sheet_b, ['COLAB', 'Colab'])

        required_cols_b = {
            'WEBSITE': website_col, 'SIZE (US)': size_col, 'QTY': qty_col,
            'ORDER RECV DATE': order_date_col, 'COLAB': colab_col_b
        }
        missing_b = [k for k, v in required_cols_b.items() if v is None]
        if missing_b:
            st.error(f"❌ Missing required columns in Sheet B: {', '.join(missing_b)}")
            st.info("Available columns in Sheet B: " + ", ".join(sheet_b.columns))
            st.stop()

        sheet_b_raw = pd.DataFrame({
            'WEBSITE':    sheet_b[website_col].astype(str).str.strip().str.upper(),
            'SKU':        sheet_b[sku_col].astype(str).str.strip().str.upper() if sku_col else 'N/A',
            'SIZE_US':    sheet_b[size_col].astype(str).str.strip().str.upper(),
            'QTY':        pd.to_numeric(sheet_b[qty_col], errors='coerce').fillna(0),
            'ORDER_DATE': pd.to_datetime(sheet_b[order_date_col], errors='coerce'),
            'COLAB':      sheet_b[colab_col_b].astype(str).str.strip().str.upper()
        })
        sheet_b_raw['MONTH_NUM']  = sheet_b_raw['ORDER_DATE'].dt.month
        sheet_b_raw['YEAR_NUM']   = sheet_b_raw['ORDER_DATE'].dt.year
        sheet_b_raw['MONTH_YEAR'] = sheet_b_raw['ORDER_DATE'].dt.strftime('%b-%y')

        # No more merged_df – return raw data only
        return sheet_a_unique, sheet_b_raw

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        st.write("Detailed error:", traceback.format_exc())
        st.stop()


# ── Main dashboard ─────────────────────────────────────────────────────────────
if uploaded_file is not None:
    try:
        with st.spinner('Loading and processing data…'):
            sheet_a_unique, sheet_b_raw = load_and_process_data(uploaded_file)

        total_initial_qty = sheet_a_unique['INITIAL_QTY'].sum()
        total_qty_sold    = sheet_a_unique['TOTAL_QTY'].sum()  # only for initial placeholder
        total_balance     = sheet_a_unique['BALANCE'].sum()
        sales_pct         = (total_qty_sold / total_initial_qty * 100) if total_initial_qty > 0 else 0
        return_pct        = 35  # placeholder

        st.success(f"✅ Data loaded successfully! {len(sheet_a_unique):,} unique COLABs in stock")
        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Sidebar ────────────────────────────────────────────────────────────
        with st.sidebar:
            st.markdown("### SORT TABLES")
            sort_column = st.selectbox(
                "Sort by",
                ['Total Qty', 'Initial Qty', 'Balance', 'Sales%'],
                key='sort_measure'
            )
            sort_order = st.radio("Order", ['Descending', 'Ascending'], horizontal=True)
            st.markdown("---")

            st.markdown("### TABLE HEIGHT")
            table_height = st.slider("Height (px):", 150, 1500, 420, 10)
            st.markdown("---")

            # Dimension lists
            brands        = sorted(sheet_a_unique['BRAND'].dropna().unique())
            seasons       = sorted(sheet_a_unique['SEASON'].dropna().unique())
            categories    = sorted(sheet_a_unique['CATEGORY'].dropna().unique())
            subcategories = sorted(sheet_a_unique['SUBCATEGORY'].dropna().unique())
            colors        = sorted(sheet_a_unique['COLOR'].dropna().unique())
            colabs        = sorted(sheet_a_unique['COLAB'].dropna().unique())
            websites      = sorted(sheet_b_raw['WEBSITE'].dropna().unique())
            sizes         = sorted(
                sheet_b_raw[
                    sheet_b_raw['SIZE_US'].notna() &
                    (sheet_b_raw['SIZE_US'].str.strip() != '') &
                    (~sheet_b_raw['SIZE_US'].str.upper().isin(['NAN', '0', 'NONE', 'N/A']))
                ]['SIZE_US'].unique()
            )
            my_df = sheet_b_raw[sheet_b_raw['ORDER_DATE'].notna()].copy()
            if not my_df.empty:
                my_df_agg = (
                    my_df.groupby(['MONTH_NUM', 'YEAR_NUM', 'MONTH_YEAR'])
                    .size().reset_index()
                    .sort_values(['YEAR_NUM', 'MONTH_NUM'])
                )
                month_years = my_df_agg['MONTH_YEAR'].tolist()
            else:
                month_years = []

            st.markdown("### FILTERS")
            selected_brands        = st.multiselect("Brand",       ['All'] + brands,        default='All')
            selected_seasons       = st.multiselect("Season",      ['All'] + seasons,       default='All')
            selected_categories    = st.multiselect("Category",    ['All'] + categories,    default='All')
            selected_subcategories = st.multiselect("Subcategory", ['All'] + subcategories, default='All')
            selected_colors        = st.multiselect("Color",       ['All'] + colors,        default='All')
            selected_colabs        = st.multiselect("Colab",       ['All'] + colabs,        default='All')
            st.markdown("---")
            selected_websites    = st.multiselect("Website",    ['All'] + websites,    default='All')
            selected_sizes       = st.multiselect("Size (US)",  ['All'] + sizes,       default='All')
            selected_month_years = st.multiselect("Month-Year", ['All'] + month_years, default='All')

            # ── Cross‑filter logic: intersection of Sheet A and Sheet B COLABs ──
            # 1. COLABs that pass Sheet A filters
            filtered_a = sheet_a_unique.copy()
            if 'All' not in selected_brands        and selected_brands:
                filtered_a = filtered_a[filtered_a['BRAND'].isin(selected_brands)]
            if 'All' not in selected_seasons       and selected_seasons:
                filtered_a = filtered_a[filtered_a['SEASON'].isin(selected_seasons)]
            if 'All' not in selected_categories    and selected_categories:
                filtered_a = filtered_a[filtered_a['CATEGORY'].isin(selected_categories)]
            if 'All' not in selected_subcategories and selected_subcategories:
                filtered_a = filtered_a[filtered_a['SUBCATEGORY'].isin(selected_subcategories)]
            if 'All' not in selected_colors        and selected_colors:
                filtered_a = filtered_a[filtered_a['COLOR'].isin(selected_colors)]
            if 'All' not in selected_colabs        and selected_colabs:
                filtered_a = filtered_a[filtered_a['COLAB'].isin(selected_colabs)]

            valid_a_colabs = set(filtered_a['COLAB'].unique())

            # 2. COLABs that appear in Sheet B after Website + Month‑Year filters
            filtered_b_intersect = sheet_b_raw[sheet_b_raw['COLAB'].isin(valid_a_colabs)].copy()
            if 'All' not in selected_websites and selected_websites:
                filtered_b_intersect = filtered_b_intersect[filtered_b_intersect['WEBSITE'].isin(selected_websites)]
            if 'All' not in selected_month_years and selected_month_years:
                filtered_b_intersect = filtered_b_intersect[filtered_b_intersect['MONTH_YEAR'].isin(selected_month_years)]

            valid_b_colabs = set(filtered_b_intersect['COLAB'].unique())

            # Intersection = visible COLABs
            valid_colabs = valid_a_colabs.intersection(valid_b_colabs)

            # 3. Final filtered datasets for KPIs, tables, charts
            filtered_sheet_a = sheet_a_unique[sheet_a_unique['COLAB'].isin(valid_colabs)].copy()

            # Orders after all B filters (Website, Size, Month‑Year) – used everywhere
            filtered_b_final = sheet_b_raw[sheet_b_raw['COLAB'].isin(valid_colabs)].copy()
            if 'All' not in selected_websites and selected_websites:
                filtered_b_final = filtered_b_final[filtered_b_final['WEBSITE'].isin(selected_websites)]
            if 'All' not in selected_sizes and selected_sizes:
                filtered_b_final = filtered_b_final[filtered_b_final['SIZE_US'].isin(selected_sizes)]
            if 'All' not in selected_month_years and selected_month_years:
                filtered_b_final = filtered_b_final[filtered_b_final['MONTH_YEAR'].isin(selected_month_years)]

            # ── Sidebar DATASET pills (updated with cross‑filter numbers) ──
            st.markdown("---")
            st.markdown("### DATASET")
            st.markdown(f"""
<div class="stat-pill"><span>COLABs</span><span>{len(valid_colabs):,}</span></div>
<div class="stat-pill"><span>Seasons</span><span>{filtered_sheet_a['SEASON'].nunique()}</span></div>
<div class="stat-pill"><span>Subcategories</span><span>{filtered_sheet_a['SUBCATEGORY'].nunique()}</span></div>
<div class="stat-pill"><span>Websites</span><span>{filtered_b_final['WEBSITE'].nunique()}</span></div>
<div class="stat-pill"><span>Months</span><span>{filtered_b_final['MONTH_YEAR'].nunique()}</span></div>
""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(
                '<p style="color:#555 !important; font-size:10px !important; text-align:center; letter-spacing:1px;">'
                'Press <b style="color:#D4AF37 !important;">R</b> to open &nbsp;·&nbsp; '
                '<b style="color:#D4AF37 !important;">O</b> to close</p>',
                unsafe_allow_html=True
            )

        # ── Guard clause ─────────────────────────────────────────────────────
        if len(valid_colabs) == 0:
            st.warning("⚠️ No COLABs match the selected filters. Please adjust your selections.")
            st.stop()

        # ── KPI row (stock from A, orders from B) ─────────────────────────
        st.markdown('<div class="section-heading">◈  Key Performance Indicators</div>', unsafe_allow_html=True)

        f_init = filtered_sheet_a['INITIAL_QTY'].sum()
        f_bal  = filtered_sheet_a['BALANCE'].sum()
        f_sold = filtered_b_final['QTY'].sum()               # from orders
        f_spct = (f_sold / f_init * 100) if f_init > 0 else 0

        col1, col2, col3, col4, col5 = st.columns(5)
        kpis = [
            (col1, "📦", "Initial Qty",    f"{f_init:,.0f}"),
            (col2, "💰", "Total Qty Sold", f"{f_sold:,.0f}"),
            (col3, "⚖️", "Balance Qty",   f"{f_bal:,.0f}"),
            (col4, "🔄", "Return % Jan-Apr 2026",       f"{return_pct:.1f}%"),
            (col5, "📈", "Sales %",        f"{f_spct:.1f}%"),
        ]
        for col, icon, label, value in kpis:
            with col:
                st.markdown(f"""
<div class='kpi-card'>
  <div class='kpi-icon'>{icon}</div>
  <div class='kpi-label'>{label}</div>
  <div class='kpi-value'>{value}</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Distribution tables (left‑join on COLAB, aggregate) ──────────
        st.markdown('<div class="section-heading">◈  Sales Distribution Tables</div>', unsafe_allow_html=True)

        # Merge stock (filtered_sheet_a) with aggregated orders (filtered_b_final)
        orders_agg = filtered_b_final.groupby('COLAB')['QTY'].sum().reset_index()
        orders_agg.rename(columns={'QTY': 'TOTAL_QTY'}, inplace=True)

        # Only COLABs that are in the intersection (already guaranteed)
        merged_for_tables = pd.merge(
            filtered_sheet_a[['COLAB', 'BRAND', 'SEASON', 'CATEGORY', 'SUBCATEGORY', 'COLOR',
                              'INITIAL_QTY', 'BALANCE']],
            orders_agg,
            on='COLAB',
            how='inner'   # intersection ensures no missing
        )

        def analyze_group_crossfilter(group_col, display_name):
            if group_col not in merged_for_tables.columns:
                return pd.DataFrame()
            grouped = merged_for_tables.groupby(group_col, observed=True).agg(
                INITIAL_QTY=('INITIAL_QTY', 'sum'),
                TOTAL_QTY=('TOTAL_QTY', 'sum'),
                BALANCE=('BALANCE', 'sum')
            ).reset_index()
            grouped['SALES_PERCENTAGE'] = np.where(
                grouped['INITIAL_QTY'] > 0,
                (grouped['TOTAL_QTY'] / grouped['INITIAL_QTY']) * 100, 0
            )
            sort_map = {
                'Total Qty': 'TOTAL_QTY', 'Initial Qty': 'INITIAL_QTY',
                'Balance': 'BALANCE', 'Sales%': 'SALES_PERCENTAGE'
            }
            grouped = grouped.sort_values(sort_map[sort_column], ascending=(sort_order == 'Ascending'))
            grouped.rename(columns={group_col: display_name}, inplace=True)
            return grouped

        tables_config = [
            ('BRAND', 'Brand'), ('SEASON', 'Season'),
            ('CATEGORY', 'Category'), ('SUBCATEGORY', 'Subcategory'),
            ('COLOR', 'Color'), ('COLAB', 'Colab')
        ]
        for i in range(0, len(tables_config), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(tables_config):
                    col_name, display_name = tables_config[i + j]
                    with cols[j]:
                        st.markdown(
                            f'<div class="card-title">◆  {display_name} Wise Distribution</div>',
                            unsafe_allow_html=True
                        )
                        table_data = analyze_group_crossfilter(col_name, display_name)
                        show_html_table(table_data, display_name, table_height)

        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Visual Charts (based on filtered_b_final) ──────────────────
        st.markdown('<div class="section-heading">◈  Visual Analytics</div>', unsafe_allow_html=True)

        # CHART 1 — Marketplace
        st.markdown('<div class="chart-wrap"><div class="chart-label">🌐  Marketplace Wise Qty Sold</div>', unsafe_allow_html=True)
        website_data = (
            filtered_b_final[
                filtered_b_final['WEBSITE'].notna() &
                (filtered_b_final['WEBSITE'].str.strip() != '') &
                (filtered_b_final['WEBSITE'].str.upper() != 'NAN')
            ]
            .groupby('WEBSITE')['QTY'].sum()
            .reset_index()
            .sort_values('QTY', ascending=False)
        )
        if not website_data.empty:
            n = len(website_data)
            bar_colors = [GOLD_PALETTE[i % len(GOLD_PALETTE)] for i in range(n)]
            fig_ws = go.Figure(go.Bar(
                x=website_data['WEBSITE'],
                y=website_data['QTY'],
                text=website_data['QTY'].apply(lambda v: f"{v:,.0f}"),
                marker=dict(color=bar_colors, line=dict(color='rgba(255,255,255,0.06)', width=1), cornerradius=6),
            ))
            fig_ws.update_layout(title="Sales by Marketplace till Apr 2026")
            fig_ws = _dark_layout(fig_ws, "Marketplace", "Quantity Sold",
                                  extra_xaxis={'categoryorder': 'array',
                                               'categoryarray': website_data['WEBSITE'].tolist()})
            st.plotly_chart(fig_ws, use_container_width=True)
        else:
            st.info("No marketplace data available for the current filters")
        st.markdown("</div>", unsafe_allow_html=True)

        # CHART 2 — Size
        st.markdown('<div class="chart-wrap"><div class="chart-label">📏  Size Wise Qty Distribution</div>', unsafe_allow_html=True)
        size_data = (
            filtered_b_final[
                filtered_b_final['SIZE_US'].notna() &
                (filtered_b_final['SIZE_US'].str.strip() != '') &
                (~filtered_b_final['SIZE_US'].str.upper().isin(['NAN', '0', 'NONE', 'N/A']))
            ]
            .groupby('SIZE_US')['QTY'].sum()
            .reset_index()
            .sort_values('QTY', ascending=False)
        )
        if not size_data.empty:
            size_data['SIZE_LABEL'] = size_data['SIZE_US'].astype(str).str.strip()
            all_size_labels = size_data['SIZE_LABEL'].tolist()
            import plotly.colors as pc
            gradient = pc.sample_colorscale(
                [[0, "#D4AF37"], [0.4, "#E67E22"], [0.8, "#F1C40F"], [1.0, "#C0932F"]],
                max(len(size_data), 2)
            )
            fig_sz = go.Figure(go.Bar(
                x=size_data['SIZE_LABEL'],
                y=size_data['QTY'],
                text=size_data['QTY'].apply(lambda v: f"{v:,.0f}"),
                marker=dict(color=gradient, line=dict(color='rgba(255,255,255,0.06)', width=1), cornerradius=6),
            ))
            fig_sz.update_layout(title="Sales by Size (US) till Apr 2026")
            fig_sz = _dark_layout(
                fig_sz, "Size (US)", "Quantity Sold",
                extra_xaxis={
                    'type': 'category',
                    'categoryorder': 'array',
                    'categoryarray': all_size_labels,
                    'tickmode': 'array',
                    'tickvals': all_size_labels,
                    'ticktext': all_size_labels,
                },
                height=520
            )
            st.plotly_chart(fig_sz, use_container_width=True)
        else:
            st.info("No size data available for the current filters")
        st.markdown("</div>", unsafe_allow_html=True)

        # CHART 3 — Month-Year
        st.markdown('<div class="chart-wrap"><div class="chart-label">📅  Month-Year Wise Qty Distribution</div>', unsafe_allow_html=True)
        monthly_b = filtered_b_final[filtered_b_final['ORDER_DATE'].notna()].copy()
        if not monthly_b.empty:
            monthly_b['MONTH_NUM']   = monthly_b['ORDER_DATE'].dt.month
            monthly_b['YEAR_NUM']    = monthly_b['ORDER_DATE'].dt.year
            monthly_b['MONTH_LABEL'] = monthly_b['ORDER_DATE'].dt.strftime('%b-%y')

            monthly_agg = (
                monthly_b.groupby(['MONTH_NUM', 'YEAR_NUM', 'MONTH_LABEL'])['QTY']
                .sum().reset_index()
                .sort_values(['MONTH_NUM', 'YEAR_NUM'])
            )
            ordered_labels = monthly_agg['MONTH_LABEL'].tolist()

            MONTH_COLORS = {
                1: "#D4AF37", 2: "#F1C40F", 3: "#E6B800",
                4: "#E67E22", 5: "#C0932F", 6: "#F4A261",
                7: "#E9C46A", 8: "#3EAFBD", 9: "#2A9D8F",
                10: "#52C4C0", 11: "#457B9D", 12: "#264653",
            }
            bar_colors = [MONTH_COLORS.get(m, "#D4AF37") for m in monthly_agg['MONTH_NUM']]

            fig_mo = go.Figure(go.Bar(
                x=monthly_agg['MONTH_LABEL'],
                y=monthly_agg['QTY'],
                text=monthly_agg['QTY'].apply(lambda v: f"{v:,.0f}"),
                marker=dict(color=bar_colors, line=dict(color='rgba(255,255,255,0.06)', width=1), cornerradius=5),
            ))
            fig_mo.update_layout(title="Sales by Month-Year till Apr 2026")
            fig_mo = _dark_layout(
                fig_mo, "Month-Year", "Quantity Sold",
                extra_xaxis={'categoryorder': 'array', 'categoryarray': ordered_labels},
                height=540
            )
            st.plotly_chart(fig_mo, use_container_width=True)
        else:
            st.info("No order date data available for the current filters")
        st.markdown("</div>", unsafe_allow_html=True)

        # Raw data expander
        with st.expander("🔍 View Filtered Order Data"):
            st.dataframe(filtered_b_final, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        import traceback
        st.write("Detailed error:", traceback.format_exc())

else:
    st.markdown("""
<div style='text-align:center; padding:40px 20px; color:rgba(212,175,55,0.5); font-size:15px; letter-spacing:2px;'>
  👆  Upload an Excel file to begin analysing your data.
</div>""", unsafe_allow_html=True)

    with st.expander("📋 Required Excel File Structure"):
        st.markdown("""
**Sheet A Columns (Required):**
`SEASON` · `BRAND` · `CATEGORY` · `Subcategory` · `COLOR` · `COLAB` · `INITIAL QTY` · `Total Qty` · `Balance`

**Sheet B Columns (Required):**
`WEBSITE` · `SIZE (US)` · `QTY` · `ORDER RECV DATE` · `COLAB`

**Sidebar Filters — Sheet A:** Brand · Season · Category · Subcategory · Color · Colab  
**Sidebar Filters — Sheet B:** Website · Size (US) · Month-Year
""")
