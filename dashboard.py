#!/usr/bin/env python3
"""
Dashboard Remuneraciones — Municipio de Purén 2025
"""

import re
import unicodedata
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

try:
    import base64 as _b64
    with open("logo_gestiona.png", "rb") as _lf:
        _LOGO_B64 = _b64.b64encode(_lf.read()).decode()
except Exception:
    _LOGO_B64 = ""

def make_footer(title):
    """Footer con impresion formal: nueva ventana con titulo, tablas, fecha y web."""
    t = title.replace("\\", "\\\\").replace("'", "\\'")
    # Usamos entidades HTML para los iconos (sin emoji en JS para evitar UnicodeEncodeError)
    btn_html = (
        '<div style="padding-top:14px;border-top:2px solid #EEF3FF;display:flex;'
        'justify-content:space-between;align-items:center;font-family:Inter,sans-serif;margin-top:6px;">'
        '<span style="font-size:.82rem;color:#555;font-weight:600;">'
        '&#128202; <a href="https://www.gestionadatos.cl" target="_blank" '
        'style="color:#003DA5;font-weight:800;text-decoration:none;">www.gestionadatos.cl</a>'
        '</span>'
        '<button onclick="printSec()" style="background:#003DA5;color:white;padding:8px 20px;'
        'border-radius:8px;font-weight:700;font-size:13px;cursor:pointer;border:none;">'
        '&#128424; Imprimir'
        '</button>'
        '</div>'
    )
    js = """<script>
function printSec(){
  var T='""" + t + """';
  try{
    var pd=window.parent.document;
    var fr=pd.getElementsByTagName('iframe'),tf=null;
    for(var i=0;i<fr.length;i++){try{if(fr[i].contentWindow===window){tf=fr[i];break;}}catch(e){}}
    var el=tf,exp=null;
    for(var j=0;j<35;j++){el=el?el.parentElement:null;if(!el)break;
      if(el.getAttribute&&el.getAttribute('data-testid')==='stExpander'){exp=el;break;}}
    var tbs=exp?exp.querySelectorAll('table'):[];
    var th='';
    tbs.forEach(function(tb){th+=tb.outerHTML+'<br/>';});
    // Capture Plotly charts as SVG images
    var plots=exp?exp.querySelectorAll('.js-plotly-plot'):[];
    var chartHtml='';
    plots.forEach(function(plot){
      try{
        var svg=plot.querySelector('svg.main-svg');
        if(svg){
          var s=new XMLSerializer();
          var svgStr=s.serializeToString(svg);
          chartHtml+='<div style="text-align:center;margin:16px 0 24px;page-break-inside:avoid;">'
            +'<img src="data:image/svg+xml,'+encodeURIComponent(svgStr)+'" style="max-width:100%;height:auto;border:1px solid #EEF3FF;border-radius:6px;padding:8px;"/>'
            +'</div>';
        }
      }catch(ex){}
    });
    if(chartHtml) th=chartHtml+(th?'<div style="margin-top:20px;">'+th+'</div>':'');
    if(!th)th='<p style="color:#888;font-style:italic">Sin datos en esta seccion.</p>';
    var mn=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
    var nd=new Date(),fe=nd.getDate()+' de '+mn[nd.getMonth()]+' de '+nd.getFullYear();
    var css=[
      '*{font-family:Inter,Arial,sans-serif;box-sizing:border-box;}',
      'body{margin:0;padding:0;color:#1A2B4A;background:#fff;}',
      '.ph{text-align:center;padding:28px 50px 18px;border-bottom:4px solid #003DA5;margin-bottom:24px;}',
      '.ph-org{font-size:10pt;font-weight:700;color:#003DA5;letter-spacing:2px;text-transform:uppercase;margin-bottom:7px;}',
      '.ph h1{font-size:19pt;font-weight:900;color:#1A2B4A;margin:0 0 5px;}',
      '.ph-sub{font-size:9pt;color:#666;}',
      '.cnt{padding:0 44px 90px;}',
      '.ft{position:fixed;bottom:0;left:0;right:0;display:flex;justify-content:space-between;',
      'font-size:8.5pt;color:#777;border-top:1px solid #ddd;padding:6px 22px;background:#fff;}',
      'table{width:100%;border-collapse:collapse;font-size:11pt;margin-bottom:20px;}',
      'th{background:#003DA5;color:#fff;padding:9px 12px;font-weight:700;',
      '-webkit-print-color-adjust:exact;print-color-adjust:exact;}',
      'th:first-child{text-align:left;}th:not(:first-child){text-align:right;}',
      'td{padding:8px 12px;border-bottom:1px solid #EEF3FF;}',
      'td:first-child{text-align:left;font-weight:600;color:#003DA5;}',
      'td:not(:first-child){text-align:right;}',
      'tr:last-child td{background:#EEF3FF;font-weight:800;',
      '-webkit-print-color-adjust:exact;print-color-adjust:exact;}',
      '@media print{@page{margin:2cm 2cm 3cm;size:A4;}',
      'canvas,button,select,input{display:none!important;}.ft{position:fixed;bottom:0;}}'
    ].join('');
    var html=[
      '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>'+T+'</title>',
      '<style>'+css+'</style></head><body>',
      '<div class="ph">',
      '<div class="ph-org">Municipalidad de Pur\u00e9n &mdash; Transparencia en el Sector P\u00fablico</div>',
      '<h1>'+T+'</h1>',
      '<div class="ph-sub">Per\u00edodo 2025 &nbsp;&middot;&nbsp; Datos elaborados por <strong>Gestiona tus datos</strong></div>',
      '</div>',
      '<div class="cnt">'+th+'</div>',
      '<div class="ft"><span>www.gestionadatos.cl</span><span>Fecha de impresi\u00f3n: '+fe+'</span></div>',
      '<'+'script>setTimeout(function(){window.print();},800);<'+'/sc'+'ript>',
      '</body></html>'
    ].join('');
    var pw=window.parent.open('','_blank','width=920,height=720');
    pw.document.write(html);
    pw.document.close();
  }catch(e){window.parent.print();}
}
</script>"""
    return btn_html + js


# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Remuneraciones Purén 2025", page_icon="🏛️", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:#EEF3FF;}
section[data-testid="stSidebar"]{background:#003DA5!important;}
section[data-testid="stSidebar"] *{color:white!important;}
section[data-testid="stSidebar"] .stTextInput input{
  background:rgba(255,255,255,.15)!important;border:1px solid rgba(255,255,255,.4)!important;
  color:white!important;border-radius:8px;}
section[data-testid="stSidebar"] .stSelectbox>div>div{
  background:rgba(255,255,255,.15)!important;border:1px solid rgba(255,255,255,.4)!important;border-radius:8px;}
section[data-testid="stSidebar"] input[type="checkbox"]{accent-color:#27AE60 !important;width:17px;height:17px;}
section[data-testid="stSidebar"] label{font-weight:600!important;letter-spacing:.02em;}
.hdr{background:linear-gradient(135deg,#003DA5,#0055CC);border-radius:14px;padding:26px 32px;margin-bottom:28px;}
.hdr h1{font-size:1.9rem;font-weight:900;color:white;margin:0;}
.hdr p{font-size:1rem;color:rgba(255,255,255,.85);margin:5px 0 0;}
.sec{font-size:1.1rem;font-weight:800;color:#000000;border-left:5px solid #4DA3FF;padding-left:12px;margin:30px 0 14px;}
.wrap{background:white;border-radius:14px;box-shadow:0 2px 12px rgba(0,61,165,.1);overflow:hidden;margin-bottom:8px;}
table{width:100%;border-collapse:collapse;font-size:14px;}
table thead th{background:#003DA5;color:white;padding:11px 15px;font-weight:700;font-size:13px;text-align:right;}
table thead th:first-child{text-align:left;}
table.t-res td{padding:10px 15px;border-bottom:1px solid #EEF3FF;color:#1A2B4A;text-align:right;}
table.t-res td:first-child{text-align:left;font-weight:600;color:#003DA5;}
table.t-res tr:hover td{background:#F0F5FF;}
table.t-res tr.hl td{background:#E8F0FF;}
table.t-res tr.tot td{background:#003DA5;color:white!important;font-weight:800;border-bottom:none;}
table.t-top td{padding:9px 14px;border-bottom:1px solid #EEF3FF;color:#1A2B4A;text-align:left;vertical-align:top;}
table.t-top td:first-child{text-align:center;width:28px;font-weight:800;color:#4DA3FF;}
table.t-top td:last-child{text-align:right;font-weight:700;color:#003DA5;white-space:nowrap;}
table.t-top tr:hover td{background:#F0F5FF;}
table.t-mes td{padding:10px 15px;border-bottom:1px solid #EEF3FF;color:#1A2B4A;}
table.t-mes td:last-child{text-align:right;font-weight:700;color:#003DA5;}
table.t-mes tr:hover td{background:#F0F5FF;}
.kpis{display:flex;gap:14px;margin:20px 0;flex-wrap:wrap;}
.kpi{flex:1;min-width:140px;border-radius:12px;padding:16px;text-align:center;}
.kpi .lbl{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:rgba(255,255,255,.85);margin-bottom:5px;}
.kpi .val{font-size:1.15rem;font-weight:900;color:white;}
.ficha{background:white;border-radius:14px;box-shadow:0 2px 12px rgba(0,61,165,.1);padding:26px 30px;margin-top:6px;}
.f-nom{font-size:1.4rem;font-weight:900;color:#003DA5;margin-bottom:3px;}
.f-sub{font-size:.93rem;color:#0066CC;font-weight:600;margin-bottom:18px;}
.f-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px;}
.f-item{background:#F0F5FF;border-radius:10px;padding:12px 14px;}
.f-lbl{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#0066CC;margin-bottom:3px;}
.f-val{font-size:.92rem;font-weight:700;color:#1A2B4A;}
.print-btn{display:inline-block;margin-top:18px;padding:10px 24px;background:#003DA5;color:white!important;
  font-weight:700;font-size:14px;border-radius:9px;cursor:pointer;border:none;text-decoration:none;}
.print-btn:hover{background:#0055CC;}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary *{color:#000000!important;fill:#000000!important;font-weight:700;}
details[open]>summary,details[open]>summary *{background:#003DA5!important;color:#ffffff!important;
  fill:#ffffff!important;border-radius:6px 6px 0 0;padding-left:12px !important;}
.inf-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:14px;}
.inf-card{border-radius:10px;padding:13px 16px;}
.inf-card .ic-lbl{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px;}
.inf-card .ic-val{font-size:.95rem;font-weight:800;}
.inf-card .ic-det{font-size:.75rem;margin-top:3px;opacity:.85;}
.torta-resumen{background:white;border-radius:14px;box-shadow:0 2px 12px rgba(0,61,165,.1);padding:20px 22px;}
.torta-item{border-bottom:1px solid #EEF3FF;padding:10px 0;}
.torta-item:last-child{border-bottom:none;}
.torta-label{font-size:.85rem;font-weight:700;color:#000000;}
.torta-val{font-size:.85rem;color:#000000;}
@media print{
  section[data-testid="stSidebar"],.hdr,.sec,button,.stTextInput,.stSelectbox,
  [data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
  .ficha{box-shadow:none;border:1px solid #ccc;}
  .stApp{background:white!important;}
  .print-footer-bar{display:block!important;}
}
.print-footer-bar{display:none;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTES Y HELPERS
# ─────────────────────────────────────────────────────────────────────────────
MESES = {"01":"Enero","02":"Febrero","03":"Marzo","04":"Abril","05":"Mayo",
          "06":"Junio","07":"Julio","08":"Agosto","09":"Septiembre",
          "10":"Octubre","11":"Noviembre","12":"Diciembre"}
MESES_INV = {v:k for k,v in MESES.items()}
AREAS  = ["EDUCACION","JARDINES","MUNICIPAL","SALUD"]
LABELS = {"EDUCACION":"Educación","JARDINES":"Jardines (JUNJI)",
          "MUNICIPAL":"Municipal","SALUD":"Salud"}
COLORS = {"EDUCACION":"#27AE60","JARDINES":"#B8860B",
          "MUNICIPAL":"#003DA5","SALUD":"#C0392B"}
TOP_BG = {"EDUCACION":"#27AE60","JARDINES":"#B8860B",
          "MUNICIPAL":"#003DA5","SALUD":"#C0392B"}

def norm_str(s):
    s = str(s).strip().upper()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", s)

def parse_clp(s):
    if not s or str(s).strip() in ("","nan","None"): return None
    s = str(s).strip()
    if re.match(r"^\s*(\(\d+\))+\s*$", s): return None
    if re.match(r"^\d+\.\d+$", s): return round(float(s))
    digits = re.sub(r"[^\d]","",s)
    if not digits: return None
    v = int(digits)
    return v if v <= 50_000_000 else None

def fmt(v):
    if v is None or (isinstance(v,float) and pd.isna(v)): return "—"
    return "$" + f"{int(v):,}".replace(",",".")

def pv(df_func, col):
    s = df_func[col].replace("",pd.NA).dropna()
    return str(s.iloc[0]).strip() if len(s)>0 else "—"

@st.cache_data
def load():
    df = pd.read_parquet("remuneraciones_2025.parquet")
    df["rem_n"]      = df["rem_bruta"].apply(parse_clp)
    df["mes_nombre"] = df["mes"].map(MESES)
    df["mes_ord"]    = df["mes"].astype(int)
    df["ap_n"]  = df["apellido_paterno"].apply(norm_str)
    df["am_n"]  = df["apellido_materno"].apply(norm_str)
    df["nom_n"] = df["nombres"].apply(norm_str)
    df["key"]   = df["ap_n"] + "|" + df["am_n"] + "|" + df["nom_n"] + "|" + df["area"]
    display_map = (
        df.groupby("key")
        .apply(lambda g: (
            g["apellido_paterno"].mode()[0] + " " +
            g["apellido_materno"].mode()[0] + ", " +
            g["nombres"].mode()[0]
        ))
        .to_dict()
    )
    df["nombre_display"] = df["key"].map(display_map)
    return df

df_all = load()

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔎  Filtros")
    st.markdown("---")
    st.markdown("**🏢  Área**")
    cbs       = {a: st.checkbox(LABELS[a], value=True, key=f"area_{a}") for a in AREAS}
    areas_sel = [a for a in AREAS if cbs[a]]
    st.markdown("---")
    st.markdown("**📅  Año — Compras Públicas**")
    ANIOS_CP  = ["2022","2023","2024","2025"]
    cbs_anio  = {yr: st.checkbox(yr, value=True, key=f"anio_{yr}") for yr in ANIOS_CP}
    anios_sel = [yr for yr in ANIOS_CP if cbs_anio[yr]]
    st.markdown("---")
    st.markdown("""
<div style="margin-top:4px;">
  <p style="font-size:.72rem;opacity:.85;margin:0 0 4px;font-weight:700;">📋 Fuentes de datos:</p>
  <p style="font-size:.70rem;opacity:.8;margin:0 0 6px;">Remuneraciones: <a href="https://munipuren.cl/transparencia/" target="_blank" style="color:#90CAF9;text-decoration:none;">munipuren.cl/transparencia</a></p>
  <p style="font-size:.70rem;opacity:.8;margin:0 0 14px;">Compras: <a href="https://datos-abiertos.chilecompra.cl/descargas" target="_blank" style="color:#90CAF9;text-decoration:none;">datos-abiertos.chilecompra.cl</a></p>
</div>""", unsafe_allow_html=True)
    st.markdown(f'''<div style="text-align:center;margin-top:8px;padding-top:10px;border-top:1px solid rgba(255,255,255,.2);">
  <img src="data:image/png;base64,{_LOGO_B64}" style="max-width:150px;opacity:.95;" alt="Gestiona tus datos"/>
  <p style="font-size:.65rem;opacity:.75;margin:6px 0 2px;text-align:center;">
    <a href="https://www.gestionadatos.cl" target="_blank" style="color:#90CAF9;text-decoration:none;">www.gestionadatos.cl</a></p>
  <p style="font-size:.65rem;opacity:.75;margin:0;text-align:center;">
    <a href="mailto:contacto@gestionadatos.cl" style="color:#90CAF9;text-decoration:none;">contacto@gestionadatos.cl</a></p>
</div>''', unsafe_allow_html=True)

# Compatibilidad con código de remuneraciones que usa sel_mes / mes_num
sel_mes = "Todos los meses"

if not areas_sel:
    st.warning("Selecciona al menos un área.")
    st.stop()

mes_num  = MESES_INV[sel_mes] if sel_mes != "Todos los meses" else None
periodo  = sel_mes if sel_mes != "Todos los meses" else "Enero – Diciembre 2025"
areas_txt = " · ".join(LABELS[a] for a in areas_sel)

# ─────────────────────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hdr">
  <h1>&#127963; REPERTORIO NACIONAL, TRANSPARENCIA EN EL SECTOR P&#218;BLICO</h1>
  <h2 style="margin:0 0 6px;font-size:1.05rem;font-weight:600;opacity:.85;letter-spacing:1px;">COMUNA DE PUR&#201;N</h2>
  <p style="margin:4px 0 2px;font-size:.95rem;">Período: <b>{periodo}</b> &nbsp;|&nbsp; {areas_txt}</p>
  <p style="margin:0;font-size:.78rem;opacity:.75;">Trabajo realizado por <b>Gestiona tus datos</b> &nbsp;·&nbsp; <a href="https://www.gestionadatos.cl" style="color:rgba(255,255,255,.9)">www.gestionadatos.cl</a></p>
</div>""", unsafe_allow_html=True)
st.markdown('<div class="print-footer-bar" style="text-align:center;font-size:11px;color:#555;padding:4px;border-top:1px solid #ccc;font-family:Inter,sans-serif;">📊 www.gestionadatos.cl — Transparencia Municipal Purén 2025</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════════════════
#  MÓDULO REMUNERACIONES
# ═════════════════════════════════════════════════════════════════════════════
with st.expander("🏛️  REMUNERACIONES", expanded=False):

    #  SECCIÓN 1 — TABLA RESUMEN (colapsable)
    # ═════════════════════════════════════════════════════════════════════════════
    with st.expander("📊  Remuneración Bruta Total por Mes y Área", expanded=False):
        piv = (
            df_all[df_all["area"].isin(areas_sel) & df_all["rem_n"].notna()]
            .pivot_table(index="mes", columns="area", values="rem_n",
                         aggfunc="sum", fill_value=0)
            .reset_index().sort_values("mes")
        )
        piv["mes_nombre"] = piv["mes"].map(MESES)
        for a in areas_sel:
            if a not in piv.columns: piv[a] = 0
        piv["TOTAL"] = piv[areas_sel].sum(axis=1)

        ths  = "".join(f"<th>{LABELS[a]}</th>" for a in areas_sel)
        body = ""
        for _, r in piv.iterrows():
            cls  = ' class="hl"' if r["mes_nombre"] == sel_mes else ""
            cds  = "".join(f"<td>{fmt(r[a])}</td>" for a in areas_sel)
            body += f"<tr{cls}><td>{r['mes_nombre']}</td>{cds}<td>{fmt(r['TOTAL'])}</td></tr>\n"
        tots  = "".join(f"<td>{fmt(piv[a].sum())}</td>" for a in areas_sel)
        body += f'<tr class="tot"><td>TOTAL AÑO</td>{tots}<td>{fmt(piv["TOTAL"].sum())}</td></tr>'

        st.markdown(
            f'<div class="wrap"><table class="t-res"><thead><tr>'
            f'<th>Mes</th>{ths}<th>TOTAL</th>'
            f'</tr></thead><tbody>{body}</tbody></table></div>',
            unsafe_allow_html=True
        )

        components.html(make_footer("Remuneración Bruta Total por Mes y Área"), height=55)

    # ═════════════════════════════════════════════════════════════════════════════
    #  SECCIÓN 2 — GRÁFICO DE TORTA (colapsable)
    # ═════════════════════════════════════════════════════════════════════════════
    with st.expander("🥧  Distribución del Gasto por Área", expanded=False):
        df_torta = df_all[
            df_all["area"].isin(areas_sel) &
            df_all["rem_n"].notna() &
            (df_all["rem_n"] > 0)
        ]
        if mes_num:
            df_torta = df_torta[df_torta["mes"] == mes_num]

        torta_data = df_torta.groupby("area")["rem_n"].sum().reset_index()
        torta_data = torta_data[torta_data["area"].isin(areas_sel)]
        total_torta = torta_data["rem_n"].sum()

        pie_labels = [LABELS[a] for a in torta_data["area"]]
        pie_values = torta_data["rem_n"].tolist()
        pie_colors = [COLORS[a] for a in torta_data["area"]]
        titulo_torta = f"Distribución — {sel_mes}" if mes_num else "Distribución — Año 2025"

        fig_pie = go.Figure(go.Pie(
            labels=pie_labels,
            values=pie_values,
            hole=0.45,
            marker=dict(colors=pie_colors, line=dict(color="white", width=2)),
            textinfo="label+percent",
            textposition="inside",
            insidetextfont=dict(size=13, family="Inter", color="#ffffff"),
            outsidetextfont=dict(size=13, family="Inter", color="#000000"),
            hovertemplate="<b>%{label}</b><br>%{percent}<br>%{customdata}<extra></extra>",
            customdata=[fmt(v) for v in pie_values],
        ))
        fig_pie.update_layout(
            title=dict(text=titulo_torta,
                       font=dict(size=15, family="Inter", color="#000000"), x=0.5),
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter", size=13, color="#000000"),
            height=400,
            margin=dict(t=50, b=20, l=20, r=20),
            legend=dict(orientation="h", y=-0.1,
                        font=dict(size=13, color="#000000")),
            showlegend=True,
        )

        col_pie, col_res = st.columns([2, 1])
        with col_pie:
            st.plotly_chart(fig_pie, use_container_width=True)
        with col_res:
            detalle_rows = ""
            for label, val, color in zip(pie_labels, pie_values, pie_colors):
                pct = val / total_torta * 100 if total_torta > 0 else 0
                detalle_rows += f"""
    <tr>
      <td style="padding:9px 12px;border-bottom:1px solid #EEF3FF;">
        <span style="display:inline-block;width:10px;height:10px;border-radius:50%;
          background:{color};margin-right:7px;vertical-align:middle;"></span>
        <span style="font-weight:700;color:#000;font-size:.85rem;">{label}</span>
      </td>
      <td style="padding:9px 12px;border-bottom:1px solid #EEF3FF;text-align:right;
        font-size:.85rem;color:#000;">{fmt(val)}</td>
      <td style="padding:9px 12px;border-bottom:1px solid #EEF3FF;text-align:right;
        font-size:.85rem;font-weight:700;color:#000;">{pct:.1f}%</td>
    </tr>"""
            st.markdown(f"""
    <div style="background:white;border-radius:14px;box-shadow:0 2px 12px rgba(0,61,165,.1);
      padding:20px;margin-top:8px;">
      <div style="text-align:center;font-weight:900;font-size:1rem;color:#000;
        margin-bottom:14px;letter-spacing:.05em;">DETALLE</div>
      <table style="width:100%;border-collapse:collapse;">
        <thead><tr>
          <th style="text-align:left;font-size:.72rem;color:#666;padding:6px 12px;
            border-bottom:2px solid #EEF3FF;">Área</th>
          <th style="text-align:right;font-size:.72rem;color:#666;padding:6px 12px;
            border-bottom:2px solid #EEF3FF;">Total</th>
          <th style="text-align:right;font-size:.72rem;color:#666;padding:6px 12px;
            border-bottom:2px solid #EEF3FF;">%</th>
        </tr></thead>
        <tbody>{detalle_rows}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)
        components.html(make_footer("Distribución del Gasto por Área"), height=55)

    # ═════════════════════════════════════════════════════════════════════════════
    #  SECCIÓN 3 — TOP 10 POR ÁREA (4 expanders uno debajo de otro)
    # ═════════════════════════════════════════════════════════════════════════════
    def make_top10_html(area):
        sub = df_all[
            (df_all["area"] == area) &
            df_all["rem_n"].notna() &
            (df_all["rem_n"] > 0)
        ].copy()
        top = (
            sub.groupby("key")
            .agg(
                prom=("rem_n","mean"),
                nombre_display=("nombre_display","first"),
                cargo=("cargo", lambda x: x.mode()[0] if len(x)>0 else "—"),
            )
            .reset_index()
            .sort_values("prom", ascending=False)
            .head(10)
            .reset_index(drop=True)
        )
        filas = ""
        for i, r in top.iterrows():
            cargo_str = str(r["cargo"]).strip() if r["cargo"] else "—"
            filas += (
                f"<tr><td>{i+1}</td>"
                f"<td><b>{r['nombre_display']}</b>"
                f"<br><span style='font-size:11px;color:#555'>{cargo_str}</span></td>"
                f"<td>{fmt(r['prom'])}</td></tr>"
            )
        return (
            f'<div class="wrap">'
            f'<table class="t-top"><thead><tr>'
            f'<th>#</th><th>Funcionario</th><th>Prom. Mensual</th>'
            f'</tr></thead><tbody>{filas}</tbody></table></div>'
        )

    with st.expander("🏆  Remuneraciones más altas", expanded=False):
        _area_opts_top = ["Todas las áreas"] + [LABELS[a] for a in areas_sel]
        _sel_area_top  = st.selectbox("🏢  Filtrar por área", _area_opts_top, key="top_area_sel")
        if _sel_area_top == "Todas las áreas":
            _df_top = df_all[df_all["area"].isin(areas_sel) & df_all["rem_n"].notna() & (df_all["rem_n"]>0)]
        else:
            _area_key_top = [k for k,v in LABELS.items() if v == _sel_area_top][0]
            _df_top = df_all[(df_all["area"] == _area_key_top) & df_all["rem_n"].notna() & (df_all["rem_n"]>0)]
        _top10 = (
            _df_top.groupby("key")
            .agg(prom=("rem_n","mean"), nombre_display=("nombre_display","first"),
                 area=("area","first"),
                 cargo=("cargo", lambda x: x.mode()[0] if len(x)>0 else "—"))
            .reset_index().sort_values("prom", ascending=False).head(10).reset_index(drop=True)
        )
        _filas10 = ""
        for _i, _r in _top10.iterrows():
            _ac = COLORS.get(_r["area"],"#003DA5")
            _al = LABELS.get(_r["area"],_r["area"])
            _filas10 += (
                f"<tr><td style='padding:9px 14px;border-bottom:1px solid #EEF3FF;"
                f"text-align:center;font-weight:800;color:#4DA3FF'>{_i+1}</td>"
                f"<td style='padding:9px 14px;border-bottom:1px solid #EEF3FF'>"
                f"<b>{_r['nombre_display']}</b><br>"
                f"<span style='font-size:11px;color:#555'>{str(_r['cargo']).strip()}</span><br>"
                f"<span style='font-size:10px;background:{_ac};color:white;border-radius:3px;padding:1px 5px'>{_al}</span></td>"
                f"<td style='padding:9px 14px;border-bottom:1px solid #EEF3FF;"
                f"text-align:right;font-weight:700;color:#003DA5;white-space:nowrap'>{fmt(_r['prom'])}</td></tr>"
            )
        st.markdown(
            '<div class="wrap"><table class="t-top" style="width:100%"><thead><tr>' +
            '<th style="text-align:center;width:36px">#</th>' +
            '<th>Funcionario</th>' +
            '<th style="text-align:right">Prom. Mensual</th>' +
            f'</tr></thead><tbody>{_filas10}</tbody></table></div>',
            unsafe_allow_html=True
        )
        components.html(make_footer("Remuneraciones más altas"), height=55)

    # ═════════════════════════════════════════════════════════════════════════════
    #  SECCIÓN 3b — TOTAL FUNCIONARIOS POR MES
    # ═════════════════════════════════════════════════════════════════════════════
    with st.expander("👤  Total Funcionarios", expanded=False):
        _df_func = df_all[df_all["area"].isin(areas_sel) & df_all["rem_n"].notna() & (df_all["rem_n"]>0)].copy()
        _func_mes = (
            _df_func.groupby(["mes","mes_ord"])["key"]
            .nunique().reset_index()
            .rename(columns={"key":"total"})
            .sort_values("mes_ord")
        )
        _func_mes["mes_nombre"] = _func_mes["mes"].map(MESES)
        _func_por_area = (
            _df_func.groupby(["mes","mes_ord","area"])["key"]
            .nunique().reset_index()
            .rename(columns={"key":"total"})
            .sort_values("mes_ord")
        )
        _func_por_area["mes_nombre"] = _func_por_area["mes"].map(MESES)

        fig_func = go.Figure()
        # Línea total
        fig_func.add_trace(go.Scatter(
            x=_func_mes["mes_nombre"], y=_func_mes["total"],
            mode="lines+markers+text",
            name="Total",
            line=dict(color="#003DA5", width=3),
            marker=dict(size=9, color="#003DA5"),
            text=_func_mes["total"].astype(str),
            textposition="top center",
            textfont=dict(size=12, color="#003DA5", family="Inter"),
        ))
        # Líneas por área
        for _a in areas_sel:
            _sub = _func_por_area[_func_por_area["area"]==_a]
            if len(_sub)==0: continue
            fig_func.add_trace(go.Scatter(
                x=_sub["mes_nombre"], y=_sub["total"],
                mode="lines+markers",
                name=LABELS[_a],
                line=dict(color=COLORS[_a], width=1.5, dash="dot"),
                marker=dict(size=6),
            ))
        fig_func.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            height=380,
            margin=dict(t=40, b=20, l=10, r=10),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#000")),
            yaxis=dict(showgrid=True, gridcolor="#EEF3FF",
                       tickfont=dict(size=11, color="#000"), zeroline=False,
                       title=dict(text="N° Funcionarios", font=dict(size=11))),
            legend=dict(orientation="h", y=-0.15, font=dict(size=11)),
            title=dict(text="Total de funcionarios por mes — 2025",
                       font=dict(size=13, color="#000", family="Inter"), x=0),
        )
        st.plotly_chart(fig_func, use_container_width=True)

        # KPI total máximo y mínimo
        if len(_func_mes):
            _max_m = _func_mes.loc[_func_mes["total"].idxmax()]
            _min_m = _func_mes.loc[_func_mes["total"].idxmin()]
            st.markdown(
                f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:4px;">' +
                f'<div style="flex:1;min-width:140px;background:#003DA5;border-radius:10px;padding:12px 16px;text-align:center;">' +
                f'<div style="font-size:.65rem;color:rgba(255,255,255,.8);font-weight:700;text-transform:uppercase;">Mes con más funcionarios</div>' +
                f'<div style="font-size:1.1rem;font-weight:900;color:white;">{_max_m['mes_nombre']} — {int(_max_m['total'])}</div></div>' +
                f'<div style="flex:1;min-width:140px;background:#4DA3FF;border-radius:10px;padding:12px 16px;text-align:center;">' +
                f'<div style="font-size:.65rem;color:rgba(255,255,255,.8);font-weight:700;text-transform:uppercase;">Mes con menos funcionarios</div>' +
                f'<div style="font-size:1.1rem;font-weight:900;color:white;">{_min_m['mes_nombre']} — {int(_min_m['total'])}</div></div>' +
                '</div>',
                unsafe_allow_html=True
            )
        components.html(make_footer("Total Funcionarios"), height=55)

    # ═════════════════════════════════════════════════════════════════════════════
    #  SECCIÓN 4 — BUSCADOR Y FICHA
    # ═════════════════════════════════════════════════════════════════════════════
    # Construir listado deduplicado
    listado = (
        df_all[df_all["area"].isin(areas_sel) & df_all["rem_n"].notna() & (df_all["rem_n"]>0)]
        .groupby(["key","area","tipo_contrato"])
        .agg(
            nombre_display=("nombre_display","first"),
            apellido_paterno=("apellido_paterno","first"),
            apellido_materno=("apellido_materno","first"),
            nombres=("nombres","first"),
            ap_n=("ap_n","first"),
            am_n=("am_n","first"),
            nom_n=("nom_n","first"),
            cargo=("cargo", lambda x: x.mode()[0] if len(x)>0 else "—"),
        )
        .reset_index()
        .sort_values(["ap_n","nom_n"])
        .reset_index(drop=True)
    )
    listado["cargo_n"] = listado["cargo"].apply(norm_str)
    listado["opcion"] = (
        listado["nombre_display"] + "  —  " +
        listado["area"].map(LABELS) + " (" + listado["tipo_contrato"] + ")"
    )

    PLACEHOLDER = "— Escribe o selecciona un funcionario —"

    with st.expander("🔍  Buscar por cargo o funcionario", expanded=False):

        # Filtro por cargo
        cargos_unicos = sorted(listado["cargo"].dropna().unique().tolist())
        cargo_opts = ["Todos los cargos"] + cargos_unicos
        sel_cargo = st.selectbox("💼  Filtrar por cargo", cargo_opts, label_visibility="visible")

        if sel_cargo != "Todos los cargos":
            listado_filtrado = listado[listado["cargo"] == sel_cargo]
        else:
            listado_filtrado = listado

        todas_opciones = [PLACEHOLDER] + listado_filtrado["opcion"].tolist()
        sel_opt = st.selectbox(
            "🔍  Busca por nombre o apellido y selecciona",
            todas_opciones,
            label_visibility="visible"
        )

        # ─────────────────────────────────────────────────────────────────────────
        #  FICHA — dentro del expander para que colapse junto
        # ─────────────────────────────────────────────────────────────────────────
        if sel_opt and sel_opt != PLACEHOLDER:
            st.markdown('<div class="sec">📋 Detalle del Funcionario</div>', unsafe_allow_html=True)

            fila = listado_filtrado[listado_filtrado["opcion"] == sel_opt].iloc[0]
            df_func = df_all[df_all["key"] == fila["key"]].sort_values("mes_ord").copy()

            nom    = fila["nombre_display"]
            cargo  = pv(df_func, "cargo")
            area_l = LABELS.get(fila["area"], fila["area"])
            cal    = pv(df_func, "calificacion")
            grad   = pv(df_func, "grado_eus")
            tper   = pv(df_func, "tipo_personal")

            rems   = df_func["rem_n"].dropna()
            prom_v = rems.mean()  if len(rems) else None
            max_v  = rems.max()   if len(rems) else None
            min_v  = rems.min()   if len(rems) else None
            tot_v  = rems.sum()   if len(rems) else None

            # Porcentaje de aumento acumulado
            rems_ord = df_func[df_func["rem_n"].notna() & (df_func["rem_n"]>0)]["rem_n"].tolist()
            cambios  = []
            for i in range(1, len(rems_ord)):
                ant = rems_ord[i-1]
                act = rems_ord[i]
                if ant > 0:
                    cambios.append((act - ant) / ant * 100)

            pct_total = sum(cambios) if cambios else None
            pct_str   = (f"{pct_total:+.1f}%" if pct_total is not None else "—")
            pct_color = "#27AE60" if (pct_total is not None and pct_total >= 0) else "#E74C3C"

            # Ficha HTML
            ficha_html = f"""
    <div class="ficha" id="ficha-print">
      <div class="f-nom">{nom}</div>
      <div class="f-sub">{cargo} &nbsp;·&nbsp; {area_l}</div>
      <div class="f-grid">
        <div class="f-item"><div class="f-lbl">Área</div><div class="f-val">{area_l}</div></div>
        <div class="f-item"><div class="f-lbl">Cargo</div><div class="f-val">{cargo}</div></div>
        <div class="f-item"><div class="f-lbl">Calificación</div><div class="f-val">{cal}</div></div>
        <div class="f-item"><div class="f-lbl">Grado EUS</div><div class="f-val">{grad}</div></div>
        <div class="f-item"><div class="f-lbl">Tipo Personal</div><div class="f-val">{tper}</div></div>
        <div class="f-item"><div class="f-lbl">Meses con datos</div><div class="f-val">{len(df_func)} de 12</div></div>
      </div>
      <div class="kpis">
        <div class="kpi" style="background:#003DA5">
          <div class="lbl">Promedio Mensual</div><div class="val">{fmt(prom_v)}</div></div>
        <div class="kpi" style="background:#0066CC">
          <div class="lbl">Rem. Máxima</div><div class="val">{fmt(max_v)}</div></div>
        <div class="kpi" style="background:#4DA3FF">
          <div class="lbl">Rem. Mínima</div><div class="val">{fmt(min_v)}</div></div>
        <div class="kpi" style="background:#0044BB">
          <div class="lbl">Total Acumulado Año</div><div class="val">{fmt(tot_v)}</div></div>
        <div class="kpi" style="background:{pct_color}">
          <div class="lbl">% de Aumento Acumulado</div><div class="val">{pct_str}</div></div>
      </div>
      <button class="print-btn" onclick="window.parent.print()">🖨️&nbsp; Imprimir ficha</button>
    </div>
    """
            col_f, col_g = st.columns([1, 1])

            with col_f:
                st.markdown(ficha_html, unsafe_allow_html=True)

            with col_g:
                df_bar = df_func[df_func["rem_n"].notna() & (df_func["rem_n"] > 0)].copy()
                if len(df_bar) > 0:
                    bar_c = ["#003DA5" if v == max_v else "#4DA3FF" for v in df_bar["rem_n"]]
                    fig2  = go.Figure(go.Bar(
                        x=df_bar["mes_nombre"],
                        y=df_bar["rem_n"],
                        marker_color=bar_c,
                        text=df_bar["rem_n"].apply(fmt),
                        textposition="outside",
                        textfont=dict(size=10, color="#000000"),
                        hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>",
                    ))
                    fig2.update_layout(
                        plot_bgcolor="white", paper_bgcolor="white",
                        font=dict(family="Inter", size=12, color="#000000"),
                        height=420,
                        margin=dict(t=40, b=20, l=10, r=10),
                        xaxis=dict(showgrid=False, tickangle=-40,
                                   tickfont=dict(size=11, color="#000000")),
                        yaxis=dict(showticklabels=False, gridcolor="#EEF3FF", zeroline=False),
                        showlegend=False,
                        title=dict(text="Remuneración Bruta Mensual",
                                   font=dict(size=14, color="#000000", family="Inter"), x=0.5),
                    )
                    st.plotly_chart(fig2, use_container_width=True)

                    # Informe de componentes salariales
                    def num(col):
                        return pd.to_numeric(df_func[col], errors="coerce").fillna(0)

                    rem_adic  = num("rem_adicionales").sum()
                    bonos     = num("bonos_incentivos").sum()
                    hex_n     = num("horas_diurnas_n").sum() + num("horas_nocturnas_n").sum() + num("horas_festivas_n").sum()
                    hd_monto  = num("horas_diurnas_monto").sum()
                    hn_monto  = num("horas_nocturnas_monto").sum()
                    hf_monto  = num("horas_festivas_monto").sum()
                    hex_total = hd_monto + hn_monto + hf_monto

                    def card(activo, color_on, color_off, icono, titulo, valor_str, detalle=""):
                        bg = color_on if activo else color_off
                        tc = "#ffffff" if activo else "#888888"
                        return (
                            f'<div class="inf-card" style="background:{bg}">'
                            f'<div class="ic-lbl" style="color:{tc}">{icono} {titulo}</div>'
                            f'<div class="ic-val" style="color:{tc}">{valor_str}</div>'
                            + (f'<div class="ic-det" style="color:{tc}">{detalle}</div>' if detalle else "")
                            + '</div>'
                        )

                    cards_html = (
                        card(hex_total > 0, "#1A6B3C", "#E8F5EE", "⏱️", "Horas Extras",
                             fmt(hex_total) if hex_total > 0 else "Sin pagos",
                             f"{int(hex_n)} hrs acumuladas" if hex_total > 0 else "")
                        + card(hd_monto > 0, "#0055AA", "#EEF3FF", "🌤️", "Horas Diurnas",
                             fmt(hd_monto) if hd_monto > 0 else "Sin pagos")
                        + card(hn_monto > 0, "#1A3A6B", "#F0F4FF", "🌙", "Horas Nocturnas",
                             fmt(hn_monto) if hn_monto > 0 else "Sin pagos")
                        + card(hf_monto > 0, "#7B3F00", "#FFF5EE", "📅", "Horas Festivas",
                             fmt(hf_monto) if hf_monto > 0 else "Sin pagos")
                        + card(bonos > 0, "#6A0572", "#F8F0FF", "🎯", "Bonos e Incentivos",
                             fmt(bonos) if bonos > 0 else "Sin pagos")
                        + card(rem_adic > 0, "#B8860B", "#FFFBEA", "➕", "Rem. Adicionales",
                             fmt(rem_adic) if rem_adic > 0 else "Sin pagos")
                    )

                    st.markdown(
                        f'<div style="margin-top:18px;font-weight:800;font-size:.95rem;'
                        f'color:#000;border-left:4px solid #4DA3FF;padding-left:10px;margin-bottom:10px;">'
                        f'Resumen de Componentes Salariales</div>'
                        f'<div class="inf-grid">{cards_html}</div>',
                        unsafe_allow_html=True
                    )
        components.html(make_footer("Buscar por cargo o funcionario"), height=55)

    # ═════════════════════════════════════════════════════════════════════════════
    #  SECCIÓN 5 — HORAS EXTRAS Y OTROS PAGOS
    # ═════════════════════════════════════════════════════════════════════════════
    with st.expander("⏱️  Horas Extras y Otros Pagos", expanded=False):

        def numcol(df, col):
            return pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Construir tabla agregada por funcionario (key)
        df_pagos = df_all[df_all["area"].isin(areas_sel)].copy()
        for c in ["horas_diurnas_n","horas_diurnas_monto","horas_nocturnas_n",
                  "horas_nocturnas_monto","horas_festivas_n","horas_festivas_monto",
                  "bonos_incentivos","rem_adicionales"]:
            df_pagos[c] = numcol(df_pagos, c)

        df_pagos["hex_horas"] = df_pagos["horas_diurnas_n"] + df_pagos["horas_nocturnas_n"] + df_pagos["horas_festivas_n"]
        df_pagos["hex_monto"] = df_pagos["horas_diurnas_monto"] + df_pagos["horas_nocturnas_monto"] + df_pagos["horas_festivas_monto"]
        df_pagos["otros_monto"] = df_pagos["bonos_incentivos"] + df_pagos["rem_adicionales"]

        resumen = (
            df_pagos.groupby(["key","area"])
            .agg(
                nombre_display=("nombre_display","first"),
                cargo=("cargo", lambda x: x.mode()[0] if len(x)>0 else "—"),
                hex_horas=("hex_horas","sum"),
                hex_monto=("hex_monto","sum"),
                hd_n=("horas_diurnas_n","sum"),
                hd_m=("horas_diurnas_monto","sum"),
                hn_n=("horas_nocturnas_n","sum"),
                hn_m=("horas_nocturnas_monto","sum"),
                hf_n=("horas_festivas_n","sum"),
                hf_m=("horas_festivas_monto","sum"),
                bonos=("bonos_incentivos","sum"),
                rem_adic=("rem_adicionales","sum"),
                otros_monto=("otros_monto","sum"),
                meses_hex=("hex_monto", lambda x: (x>0).sum()),
                meses_bonos=("bonos_incentivos", lambda x: (x>0).sum()),
            )
            .reset_index()
        )

        # Selector de área
        area_opts_pagos = ["Todas las áreas"] + [LABELS[a] for a in areas_sel]
        sel_area_pagos  = st.selectbox("🏢  Área", area_opts_pagos, key="sel_area_pagos")
        if sel_area_pagos != "Todas las áreas":
            area_key = [k for k, v in LABELS.items() if v == sel_area_pagos][0]
            resumen_f = resumen[resumen["area"] == area_key]
        else:
            resumen_f = resumen

        if "hex_sel" not in st.session_state:
            st.session_state.hex_sel = -1
        if "hex_chart_prev" not in st.session_state:
            st.session_state.hex_chart_prev = []

        if True:
            top_hex = (resumen_f[resumen_f["hex_monto"] > 0]
                       .sort_values("hex_monto", ascending=False)
                       .head(20).reset_index(drop=True))

            if top_hex.empty:
                st.info("No hay registros de horas extras para el área seleccionada.")
            else:
                # Gráfico de barras horizontal
                fig_hex = go.Figure(go.Bar(
                    y=top_hex["nombre_display"],
                    x=top_hex["hex_monto"],
                    orientation="h",
                    marker_color="#1A6B3C",
                    text=top_hex["hex_monto"].apply(fmt),
                    textposition="outside",
                    textfont=dict(size=10, color="#000"),
                    hovertemplate="<b>%{y}</b><br>Total: %{text}<extra></extra>",
                ))
                fig_hex.update_layout(
                    plot_bgcolor="white", paper_bgcolor="white",
                    height=max(320, len(top_hex)*38),
                    margin=dict(t=30, b=20, l=10, r=120),
                    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                    yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#000")),
                    showlegend=False,
                    title=dict(text="Top funcionarios — Monto total horas extras acumulado",
                               font=dict(size=13, color="#000", family="Inter"), x=0),
                )
                event_hex = st.plotly_chart(fig_hex, use_container_width=True,
                                            on_select="rerun", key="chart_hex")
                _sp = (event_hex or {}).get("selection", {}).get("points", [])
                _prev = st.session_state.hex_chart_prev
                _changed = (len(_sp) != len(_prev) or
                            (_sp and _prev and _sp[0].get("point_index") != _prev[0].get("point_index")))
                if _changed:
                    st.session_state.hex_chart_prev = _sp
                    st.session_state.hex_sel = _sp[0]["point_index"] if _sp else -1

                # Botones de nombres (5 por fila)
                st.markdown("<p style='font-size:11px;color:#888;margin:4px 0 6px;'>&#128100; O haz clic en un nombre:</p>",
                            unsafe_allow_html=True)
                _hcols = 5
                for _hr in range((len(top_hex) + _hcols - 1) // _hcols):
                    _hbc = st.columns(_hcols)
                    for _hc in range(_hcols):
                        _hi = _hr * _hcols + _hc
                        if _hi < len(top_hex):
                            _hn = top_hex.iloc[_hi]["nombre_display"].split(",")[0].strip()
                            if _hbc[_hc].button(_hn, key=f"hex_btn_{_hi}", use_container_width=True):
                                st.session_state.hex_sel = _hi
                                st.session_state.hex_chart_prev = []
                                st.rerun()

                # Tabla condicional
                _hidx = st.session_state.hex_sel
                if _hidx >= 0 and _hidx < len(top_hex):
                    r = top_hex.iloc[_hidx]
                    area_label = LABELS.get(r["area"], r["area"])
                    area_color = COLORS.get(r["area"], "#003DA5")
                    fila_hex = (
                        f"<tr>"
                        f"<td style='padding:9px 12px;border-bottom:1px solid #EEF3FF;"
                        f"font-weight:700;color:#003DA5;'>{_hidx+1}</td>"
                        f"<td style='padding:9px 12px;border-bottom:1px solid #EEF3FF;'>"
                        f"<b>{r['nombre_display']}</b><br>"
                        f"<span style='font-size:11px;color:#555;'>{r['cargo']}</span><br>"
                        f"<span style='font-size:11px;background:{area_color};color:white;"
                        f"border-radius:4px;padding:1px 6px;'>{area_label}</span></td>"
                        f"<td style='padding:9px 12px;border-bottom:1px solid #EEF3FF;text-align:center;'>"
                        f"{int(r['hd_n'])} diurnas<br>{int(r['hn_n'])} nocturnas<br>"
                        f"{int(r['hf_n'])} festivas<br><b>{int(r['hex_horas'])} hrs total</b></td>"
                        f"<td style='padding:9px 12px;border-bottom:1px solid #EEF3FF;text-align:right;'>"
                        f"<span style='font-size:11px;color:#555;'>Diurnas</span><br><b>{fmt(r['hd_m'])}</b><br>"
                        f"<span style='font-size:11px;color:#555;'>Nocturnas</span><br><b>{fmt(r['hn_m'])}</b><br>"
                        f"<span style='font-size:11px;color:#555;'>Festivas</span><br><b>{fmt(r['hf_m'])}</b></td>"
                        f"<td style='padding:9px 12px;border-bottom:1px solid #EEF3FF;text-align:right;"
                        f"font-size:1.05rem;font-weight:900;color:#1A6B3C;'>{fmt(r['hex_monto'])}</td>"
                        f"<td style='padding:9px 12px;border-bottom:1px solid #EEF3FF;text-align:center;"
                        f"color:#555;font-size:12px;'>{int(r['meses_hex'])} meses</td></tr>"
                    )
                    st.markdown(
                        '<div class="wrap" style="margin-top:10px;">'
                        '<table style="width:100%;border-collapse:collapse;font-size:13px;">'
                        '<thead><tr>'
                        '<th style="background:#1A6B3C;color:white;padding:10px 12px;text-align:left;width:30px">#</th>'
                        '<th style="background:#1A6B3C;color:white;padding:10px 12px;text-align:left;">Funcionario</th>'
                        '<th style="background:#1A6B3C;color:white;padding:10px 12px;text-align:center;">Horas acumuladas</th>'
                        '<th style="background:#1A6B3C;color:white;padding:10px 12px;text-align:right;">Detalle por tipo</th>'
                        '<th style="background:#1A6B3C;color:white;padding:10px 12px;text-align:right;">Total acumulado</th>'
                        '<th style="background:#1A6B3C;color:white;padding:10px 12px;text-align:center;">Meses con pago</th>'
                        f'</tr></thead><tbody>{fila_hex}</tbody></table></div>',
                        unsafe_allow_html=True)
                    if st.button("&#10006; Limpiar selecci&#243;n", key="hex_clear_btn"):
                        st.session_state.hex_sel = -1
                        st.session_state.hex_chart_prev = []
                        st.rerun()
                else:
                    st.markdown(
                        '<div style="text-align:center;padding:24px 0;color:#888;font-size:14px;">'
                        '&#128070; Haz clic en una barra del gr&#225;fico o en un nombre para ver el detalle</div>',
                        unsafe_allow_html=True)

        components.html(make_footer("Horas Extras y Otros Pagos"), height=55)

    # ═════════════════════════════════════════════════════════════════════════════
    #  SECCIÓN 6 — Principales Aumentos de sueldo
    # ═════════════════════════════════════════════════════════════════════════════
    with st.expander("📈  Principales Aumentos de sueldo", expanded=False):
        st.markdown("""
<div style="background:linear-gradient(135deg,#F39C12,#F1C40F);border-radius:12px;
  padding:14px 20px;margin-bottom:18px;box-shadow:0 2px 10px rgba(243,156,18,.35);">
  <span style="font-size:1rem;font-weight:800;color:#1A2B4A;">
    ⚠️ Funcionarios con mayor incremento salarial — 2025
  </span><br>
  <span style="font-size:.80rem;color:#5D4000;">
    Solo considera funcionarios con remuneración inicial &gt; $1.000.000 y datos en al menos 2 meses.
    Compara el primer y el último mes disponible del año.
  </span>
</div>""", unsafe_allow_html=True)

        df_base_aum = df_all[
            df_all["area"].isin(areas_sel) &
            df_all["rem_n"].notna() &
            (df_all["rem_n"] > 0)
        ].copy()

        _records = []
        for _key, _grp in df_base_aum.groupby("key"):
            _g = _grp.sort_values("mes_ord")
            if len(_g) < 2:
                continue
            _ini = _g["rem_n"].iloc[0]
            _fin = _g["rem_n"].iloc[-1]
            if _ini < 1_000_000:
                continue
            _pct = (_fin - _ini) / _ini * 100
            if _pct <= 0:
                continue
            _records.append({
                "nombre":    _g["nombre_display"].iloc[0],
                "area":      _g["area"].iloc[0],
                "sueldo_ini": _ini,
                "sueldo_fin": _fin,
                "diferencia": _fin - _ini,
                "pct":        _pct,
                "mes_ini":    _g["mes_nombre"].iloc[0],
                "mes_fin":    _g["mes_nombre"].iloc[-1],
            })

        if "aum_sel" not in st.session_state:
            st.session_state.aum_sel = -1
        if "aum_chart_prev" not in st.session_state:
            st.session_state.aum_chart_prev = []

        if not _records:
            st.info("No se encontraron aumentos significativos para el área y período seleccionados.")
        else:
            top_aum = (
                pd.DataFrame(_records)
                .sort_values("pct", ascending=False)
                .head(10)
                .reset_index(drop=True)
            )

            # ── Gráfico ──────────────────────────────────────────────────────
            fig_aum = go.Figure(go.Bar(
                y=top_aum["nombre"],
                x=top_aum["pct"],
                orientation="h",
                marker_color="#F39C12",
                text=[f"+{p:.1f}%" for p in top_aum["pct"]],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(size=13, color="white", family="Inter"),
            ))
            fig_aum.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                height=max(300, len(top_aum)*55),
                margin=dict(t=35, b=20, l=10, r=30),
                xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#000")),
                title=dict(
                    text="% Aumento — primer mes vs. último mes con datos (2025)",
                    font=dict(size=13, color="#000", family="Inter"), x=0
                ),
                uniformtext=dict(mode="hide", minsize=10),
            )
            event_aum = st.plotly_chart(fig_aum, use_container_width=True,
                                        on_select="rerun", key="chart_aum")
            _spa = (event_aum or {}).get("selection", {}).get("points", [])
            _preva = st.session_state.aum_chart_prev
            _chga = (len(_spa) != len(_preva) or
                     (_spa and _preva and _spa[0].get("point_index") != _preva[0].get("point_index")))
            if _chga:
                st.session_state.aum_chart_prev = _spa
                st.session_state.aum_sel = _spa[0]["point_index"] if _spa else -1

            # Botones de nombres (5 por fila)
            st.markdown("<p style='font-size:11px;color:#888;margin:4px 0 6px;'>&#128100; O haz clic en un nombre:</p>",
                        unsafe_allow_html=True)
            _acols = 5
            for _ar in range((len(top_aum) + _acols - 1) // _acols):
                _abc = st.columns(_acols)
                for _ac_i in range(_acols):
                    _ai = _ar * _acols + _ac_i
                    if _ai < len(top_aum):
                        _an = top_aum.iloc[_ai]["nombre"].split(",")[0].strip()
                        if _abc[_ac_i].button(_an, key=f"aum_btn_{_ai}", use_container_width=True):
                            st.session_state.aum_sel = _ai
                            st.session_state.aum_chart_prev = []
                            st.rerun()

            # Tabla condicional
            _aidx = st.session_state.aum_sel
            if _aidx >= 0 and _aidx < len(top_aum):
                _rows_to_show = top_aum.iloc[[_aidx]]
            else:
                _rows_to_show = None

            if _rows_to_show is not None:
                # ── Tabla ─────────────────────────────────────────────────────────
                _filas_aum = ""
                for _i, _r in _rows_to_show.iterrows():
                    _ac = COLORS.get(_r["area"], "#003DA5")
                    _al = LABELS.get(_r["area"], _r["area"])
                    _filas_aum += (
                    f"<tr>"
                    f"<td style='padding:10px 12px;border-bottom:1px solid #FFF3CD;"
                    f"font-weight:800;color:#F39C12;text-align:center'>{_i+1}</td>"
                    f"<td style='padding:10px 12px;border-bottom:1px solid #FFF3CD'>"
                    f"<b style='color:#1A2B4A'>{_r['nombre']}</b><br>"
                    f"<span style='font-size:11px;background:{_ac};color:white;"
                    f"border-radius:4px;padding:1px 6px;'>{_al}</span></td>"
                    f"<td style='padding:10px 12px;border-bottom:1px solid #FFF3CD;"
                    f"text-align:center;font-size:11px;color:#777'>"
                    f"{_r['mes_ini']} → {_r['mes_fin']}</td>"
                    f"<td style='padding:10px 12px;border-bottom:1px solid #FFF3CD;"
                    f"text-align:right;color:#555;font-weight:600'>{fmt(_r['sueldo_ini'])}</td>"
                    f"<td style='padding:10px 12px;border-bottom:1px solid #FFF3CD;"
                    f"text-align:right;font-weight:700;color:#003DA5'>{fmt(_r['sueldo_fin'])}</td>"
                    f"<td style='padding:10px 12px;border-bottom:1px solid #FFF3CD;"
                    f"text-align:right;color:#27AE60;font-weight:700'>{fmt(_r['diferencia'])}</td>"
                    f"<td style='padding:10px 12px;border-bottom:1px solid #FFF3CD;"
                    f"text-align:center'>"
                    f"<span style='background:#F39C12;color:white;border-radius:6px;"
                    f"padding:4px 10px;font-weight:800;font-size:.95rem'>+{_r['pct']:.1f}%</span>"
                    f"</td></tr>"
                    )
                st.markdown(
                    f'<div class="wrap"><table style="width:100%;border-collapse:collapse;font-size:13px;">'
                    '<thead><tr>'
                    '<th style="background:#E67E22;color:white;padding:10px 12px;text-align:center;width:32px">#</th>'
                    '<th style="background:#E67E22;color:white;padding:10px 12px;text-align:left">Funcionario</th>'
                    '<th style="background:#E67E22;color:white;padding:10px 12px;text-align:center">Per&#237;odo</th>'
                    '<th style="background:#E67E22;color:white;padding:10px 12px;text-align:right">Sueldo Inicial</th>'
                    '<th style="background:#E67E22;color:white;padding:10px 12px;text-align:right">Sueldo Final</th>'
                    '<th style="background:#E67E22;color:white;padding:10px 12px;text-align:right">Diferencia</th>'
                    '<th style="background:#E67E22;color:white;padding:10px 12px;text-align:center">% Aumento</th>'
                    '</tr></thead>'
                    f'<tbody>{_filas_aum}</tbody></table></div>',
                    unsafe_allow_html=True
                )
                if st.button("&#10006; Limpiar selecci&#243;n", key="aum_clear_btn"):
                    st.session_state.aum_sel = -1
                    st.session_state.aum_chart_prev = []
                    st.rerun()
            else:
                st.markdown(
                    '<div style="text-align:center;padding:24px 0;color:#888;font-size:14px;">'
                    '&#128070; Haz clic en una barra del gr&#225;fico o en un nombre para ver el detalle</div>',
                    unsafe_allow_html=True)

        components.html(make_footer("Principales Aumentos de sueldo"), height=55)


# ═════════════════════════════════════════════════════════════════════════════
#  MÓDULO COMPRAS PÚBLICAS
# ═════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_compras():
    # Parquet construido directamente desde los CSV oficiales de mercadopublico.cl
    # (carpeta "COMPRAS MUNI PUREN"). Montos ya correctos, sin corrección necesaria.
    df = pd.read_parquet("compras_puren.parquet")

    # MontoNetoOC = monto neto real; MontoTotalOC = monto bruto (neto + IVA)
    # El dashboard muestra monto bruto para alinear con mercadopublico.cl
    df["monto_neto"]  = pd.to_numeric(df["MontoNetoOC"], errors="coerce").fillna(0)
    df["monto"]       = pd.to_numeric(df["MontoTotalOC"], errors="coerce").fillna(0)

    df = df[df["monto"] > 0].copy()

    # FechaEnvioOC ya está parseada como datetime en el parquet
    if not pd.api.types.is_datetime64_any_dtype(df["FechaEnvioOC"]):
        df["FechaEnvioOC"] = pd.to_datetime(df["FechaEnvioOC"], dayfirst=True, errors="coerce")
    df["fecha"] = df["FechaEnvioOC"]
    if "anio" not in df.columns:
        df["anio"] = df["fecha"].dt.year.astype("Int64")
    return df

cp = load_compras()

def fmt_cp(v):
    if v is None or (isinstance(v, float) and pd.isna(v)): return "—"
    return "$" + f"{int(v):,}".replace(",",".")

# ── Mapeo UnidadCompra → área municipal (usado para filtrar y para GASTO POR UNIDAD)
AREA_CP_COLORS = {
    "MUNICIPAL":  "#003DA5",
    "EDUCACIÓN":  "#27AE60",
    "SALUD":      "#C0392B",
    "JARDINES":   "#B8860B",
    "OTROS":      "#888888",
}
AREA_CP_SIDEBAR = {
    "EDUCACION": "EDUCACIÓN",
    "JARDINES":  "JARDINES",
    "MUNICIPAL": "MUNICIPAL",
    "SALUD":     "SALUD",
}
def map_area_cp(u):
    if not u or str(u).strip() in ("","nan","None"): return "OTROS"
    u2 = str(u).upper()
    if "SALUD"    in u2: return "SALUD"
    if any(x in u2 for x in ("JARDINES","VTF","JUNJI")): return "JARDINES"
    if any(x in u2 for x in ("EDUCAC","ESCUELA","LICEO","COLEGIO")): return "EDUCACIÓN"
    if any(x in u2 for x in ("MUNICIPAL","PUREN","PURÉN")): return "MUNICIPAL"
    return "OTROS"

cp["area_cp"] = cp["UnidadCompra"].apply(map_area_cp)

# Aplicar filtro de año del sidebar (checkboxes)
if anios_sel:
    cp_base = cp[cp["anio"].astype(str).isin(anios_sel)].copy()
else:
    cp_base = cp.copy()

# Aplicar filtro de área del sidebar → filtra también Compras Públicas
areas_cp_sel = [AREA_CP_SIDEBAR[a] for a in areas_sel if a in AREA_CP_SIDEBAR]
if areas_cp_sel:
    cp_base = cp_base[cp_base["area_cp"].isin(areas_cp_sel + ["OTROS"])].copy()

TIPO_COLORS = {"COMPRA AGIL":"#003DA5","LICITACION":"#27AE60",
               "TRATO DIRECTO":"#B8860B","CONVENIO MARCO":"#6A0572"}

with st.expander("🛒  COMPRAS PÚBLICAS", expanded=False):

    # Filtros internos (tipo)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        tipos_disp = ["Todos"] + sorted(cp_base["TipoCompra"].dropna().unique().tolist())
        sel_tipo = st.selectbox("📋  Tipo de Compra", tipos_disp, key="cp_tipo")
    with col_f2:
        estados_disp = ["Todos"] + sorted(cp_base["EstadoOC"].dropna().unique().tolist())
        sel_estado = st.selectbox("✅  Estado OC", estados_disp, key="cp_estado")

    cp_f = cp_base.copy()
    if sel_tipo   != "Todos": cp_f = cp_f[cp_f["TipoCompra"] == sel_tipo]
    if sel_estado != "Todos": cp_f = cp_f[cp_f["EstadoOC"]   == sel_estado]

    total_cp = cp_f["monto"].sum()
    n_oc     = cp_f["codigoOC"].nunique()
    n_prov   = cp_f["Proveedor"].nunique()
    prom_oc  = cp_f["monto"].mean() if len(cp_f) else 0
    periodo_cp = " · ".join(sorted(anios_sel)) if anios_sel else "Todos los años"

    # KPIs
    st.markdown(f"""
<div class="kpis" style="margin-bottom:20px;">
  <div class="kpi" style="background:#003DA5"><div class="lbl">Total Compras · {periodo_cp}</div><div class="val">{fmt_cp(total_cp)}</div></div>
  <div class="kpi" style="background:#0066CC"><div class="lbl">Órdenes de Compra</div><div class="val">{n_oc:,}</div></div>
  <div class="kpi" style="background:#1A6B3C"><div class="lbl">Proveedores únicos</div><div class="val">{n_prov:,}</div></div>
  <div class="kpi" style="background:#6A0572"><div class="lbl">Promedio por OC</div><div class="val">{fmt_cp(prom_oc)}</div></div>
</div>""", unsafe_allow_html=True)

    # ── RESUMEN ───────────────────────────────────────────────────────────────
    with st.expander("📊  RESUMEN", expanded=False):
        piv_cp = cp_f.pivot_table(index="anio", columns="TipoCompra", values="monto",
                                  aggfunc="sum", fill_value=0).reset_index().sort_values("anio")
        tipos_cols = [c for c in piv_cp.columns if c != "anio"]
        piv_cp["TOTAL"] = piv_cp[tipos_cols].sum(axis=1)
        ths_cp  = "".join(f"<th>{t}</th>" for t in tipos_cols)
        rows_cp = ""
        for _, r in piv_cp.iterrows():
            tds = "".join(f"<td style='text-align:right'>{fmt_cp(r[t])}</td>" for t in tipos_cols)
            rows_cp += (f"<tr><td style='font-weight:700;color:#003DA5'>{int(r['anio'])}</td>"
                        f"{tds}<td style='text-align:right;font-weight:800'>{fmt_cp(r['TOTAL'])}</td></tr>")
        # fila total
        tots = "".join(f"<td style='text-align:right'>{fmt_cp(piv_cp[t].sum())}</td>" for t in tipos_cols)
        rows_cp += (f"<tr class='tot'><td>TOTAL</td>{tots}"
                    f"<td style='text-align:right'>{fmt_cp(piv_cp['TOTAL'].sum())}</td></tr>")
        st.markdown(f"""
<div class="wrap"><table class="t-res">
<thead><tr><th>Año</th>{ths_cp}<th>TOTAL</th></tr></thead>
<tbody>{rows_cp}</tbody></table></div>""", unsafe_allow_html=True)

        fig_tipo = go.Figure()
        for t in tipos_cols:
            fig_tipo.add_trace(go.Bar(
                name=t, x=piv_cp["anio"].astype(str), y=piv_cp[t],
                marker_color=TIPO_COLORS.get(t,"#888"),
                text=piv_cp[t].apply(fmt_cp), textposition="inside",
                textfont=dict(size=10, color="white"),
            ))
        fig_tipo.update_layout(
            barmode="stack", plot_bgcolor="white", paper_bgcolor="white",
            height=320, margin=dict(t=30,b=20,l=10,r=10),
            font=dict(family="Inter",size=12,color="#000"),
            legend=dict(orientation="h",y=-0.18),
            xaxis=dict(showgrid=False),
            yaxis=dict(showticklabels=False,showgrid=False),
            title=dict(text="Gasto por tipo de compra y año",
                       font=dict(size=13,color="#000",family="Inter"),x=0),
        )
        st.plotly_chart(fig_tipo, use_container_width=True)
        components.html(make_footer("Compras Públicas — Resumen"), height=55)

    # ── GASTO POR UNIDAD ─────────────────────────────────────────────────────
    with st.expander("🏷️  GASTO POR UNIDAD", expanded=False):

        por_area = (cp_f.groupby("area_cp")
                    .agg(monto=("monto","sum"), n_oc=("codigoOC","nunique"))
                    .sort_values("monto", ascending=False).reset_index())
        total_area = por_area["monto"].sum()
        por_area["pct"] = por_area["monto"] / total_area * 100

        colores_bar = [AREA_CP_COLORS.get(a,"#888888") for a in por_area["area_cp"]]
        texto_bar   = [f"{fmt_cp(m)}<br>{p:.1f}%" for m,p in zip(por_area["monto"],por_area["pct"])]

        fig_area = go.Figure(go.Bar(
            y=por_area["area_cp"], x=por_area["monto"], orientation="h",
            marker_color=colores_bar,
            text=texto_bar, textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=14, color="white", family="Inter"),
        ))
        fig_area.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            height=max(300, len(por_area)*90),
            margin=dict(t=40, b=20, l=10, r=30),
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(autorange="reversed", tickfont=dict(size=14, color="#000", family="Inter")),
            title=dict(text="Gasto total por área municipal",
                       font=dict(size=14, color="#000", family="Inter"), x=0),
            uniformtext=dict(mode="hide", minsize=10),
        )
        st.plotly_chart(fig_area, use_container_width=True)

        # ── Tabla por área con sub-filas para Educación ──
        # Pre-calcular sub-unidades de Educación
        edu_subs = (cp_f[cp_f["area_cp"]=="EDUCACIÓN"]
                    .groupby("UnidadCompra")
                    .agg(monto=("monto","sum"), n_oc=("codigoOC","nunique"))
                    .sort_values("monto", ascending=False).reset_index())
        total_edu = edu_subs["monto"].sum()

        filas_area = ""
        for _, r in por_area.iterrows():
            col_dot = AREA_CP_COLORS.get(r["area_cp"],"#888")
            filas_area += f"""<tr style="background:#F8FAFF;">
  <td style="padding:10px 14px;border-bottom:1px solid #EEF3FF;">
    <span style="display:inline-block;width:13px;height:13px;border-radius:50%;
      background:{col_dot};margin-right:9px;vertical-align:middle;"></span>
    <b style="font-size:13px;">{r['area_cp']}</b>
  </td>
  <td style="padding:10px 14px;border-bottom:1px solid #EEF3FF;text-align:center;color:#555;font-weight:700">{int(r['n_oc'])}</td>
  <td style="padding:10px 14px;border-bottom:1px solid #EEF3FF;text-align:right;font-weight:800;color:#003DA5;font-size:14px">{fmt_cp(r['monto'])}</td>
  <td style="padding:10px 14px;border-bottom:1px solid #EEF3FF;text-align:right;color:#555">{r['pct']:.1f}%</td>
</tr>"""
            # Si es EDUCACIÓN, agregar sub-filas inmediatamente debajo
            if r["area_cp"] == "EDUCACIÓN" and len(edu_subs) > 0:
                for _, es in edu_subs.iterrows():
                    pct_sub = es["monto"]/total_edu*100 if total_edu else 0
                    filas_area += f"""<tr style="background:#F0F9F2;">
  <td style="padding:7px 14px 7px 38px;border-bottom:1px solid #E8F5EC;font-size:12px;color:#27AE60;">
    ↳ {es['UnidadCompra']}
  </td>
  <td style="padding:7px 14px;border-bottom:1px solid #E8F5EC;text-align:center;font-size:12px;color:#555">{int(es['n_oc'])}</td>
  <td style="padding:7px 14px;border-bottom:1px solid #E8F5EC;text-align:right;font-weight:700;color:#27AE60;font-size:12px">{fmt_cp(es['monto'])}</td>
  <td style="padding:7px 14px;border-bottom:1px solid #E8F5EC;text-align:right;font-size:12px;color:#777">{pct_sub:.1f}%</td>
</tr>"""

        st.markdown(f"""
<div class="wrap"><table style="width:100%;border-collapse:collapse;">
<thead><tr>
  <th style="background:#003DA5;color:white;padding:10px 14px;text-align:left">Área</th>
  <th style="background:#003DA5;color:white;padding:10px 14px;text-align:center">N° OC</th>
  <th style="background:#003DA5;color:white;padding:10px 14px;text-align:right">Monto total</th>
  <th style="background:#003DA5;color:white;padding:10px 14px;text-align:right">%</th>
</tr></thead><tbody>{filas_area}</tbody></table></div>""", unsafe_allow_html=True)
        components.html(make_footer("Gasto por Unidad Municipal"), height=55)

    # ── TOP PROVEEDORES ───────────────────────────────────────────────────────
    with st.expander("🏢  TOP PROVEEDORES", expanded=False):
        top_prov = (cp_f.groupby("Proveedor")
                    .agg(monto=("monto","sum"), n_oc=("codigoOC","nunique"),
                         actividad=("ActividadProveedor","first"),
                         tamano=("TamanoProveedor","first"),
                         region=("RegionProveedor","first"))
                    .sort_values("monto",ascending=False).head(20).reset_index())

        # Texto en cada barra: monto en la primera línea, N° OC en la segunda
        texto_prov = [
            f"{fmt_cp(m)}<br>{int(n)} OC{'s' if n!=1 else ''}"
            for m, n in zip(top_prov["monto"], top_prov["n_oc"])
        ]

        fig_prov = go.Figure(go.Bar(
            y=top_prov["Proveedor"], x=top_prov["monto"], orientation="h",
            marker_color="#27AE60",
            text=texto_prov,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=12, color="white", family="Inter"),
        ))
        fig_prov.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            height=max(480, len(top_prov)*50),
            margin=dict(t=40, b=20, l=10, r=30),
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="#000")),
            title=dict(text="Top 20 proveedores — monto acumulado y N° órdenes de compra",
                       font=dict(size=13, color="#000", family="Inter"), x=0),
            uniformtext=dict(mode="hide", minsize=9),
        )
        st.plotly_chart(fig_prov, use_container_width=True)
        components.html(make_footer("Top Proveedores"), height=55)

    # ── BUSCAR OC ─────────────────────────────────────────────────────────────
    with st.expander("🔍  BUSCAR OC", expanded=False):
        busq_oc = st.text_input("Busca por nombre de OC, proveedor o rubro",
                                key="busq_oc", placeholder="Ej: maquinaria, capacitación, proveedor...")

        # Tabla base: top 30 por monto del periodo/filtros actuales
        if busq_oc.strip():
            termino = busq_oc.strip().lower()
            mask_oc = (
                cp_f["NombreOC"].str.lower().str.contains(termino, na=False) |
                cp_f["Proveedor"].str.lower().str.contains(termino, na=False) |
                cp_f["RubroN1"].str.lower().str.contains(termino, na=False) |
                cp_f["RubroN2"].str.lower().str.contains(termino, na=False)
            )
            tabla_oc = cp_f[mask_oc].sort_values("monto", ascending=False).head(50)
            st.caption(f"{len(tabla_oc)} resultados encontrados para «{busq_oc}»")
        else:
            tabla_oc = cp_f.sort_values("monto", ascending=False).head(30)
            st.caption(f"Mostrando las 30 compras de mayor monto — {periodo_cp}")

        filas_oc = ""
        for _, r in tabla_oc.iterrows():
            fecha_str = r["fecha"].strftime("%d/%m/%Y") if pd.notna(r["fecha"]) else "—"
            cod_oc    = str(r["codigoOC"]) if pd.notna(r["codigoOC"]) else "—"
            rubro_str = str(r["RubroN1"])[:45] + "…" if len(str(r["RubroN1"])) > 45 else str(r["RubroN1"])
            tipo_color = TIPO_COLORS.get(str(r["TipoCompra"]),"#888")
            filas_oc += f"""
<tr>
  <td style="padding:8px 10px;border-bottom:1px solid #EEF3FF;font-size:11px;color:#555;white-space:nowrap">{fecha_str}</td>
  <td style="padding:8px 10px;border-bottom:1px solid #EEF3FF">
    <b style="font-size:12px">{r['NombreOC']}</b><br>
    <span style="font-size:11px;color:#555">{r['Proveedor']}</span>
  </td>
  <td style="padding:8px 10px;border-bottom:1px solid #EEF3FF;font-size:11px;color:#555">{rubro_str}</td>
  <td style="padding:8px 10px;border-bottom:1px solid #EEF3FF;text-align:center">
    <span style="background:{tipo_color};color:white;border-radius:4px;padding:2px 7px;font-size:10px;white-space:nowrap">{r['TipoCompra']}</span>
  </td>
  <td style="padding:8px 10px;border-bottom:1px solid #EEF3FF;text-align:right;font-weight:700;color:#003DA5;white-space:nowrap">{fmt_cp(r['monto'])}</td>
  <td style="padding:8px 10px;border-bottom:1px solid #EEF3FF;text-align:center;font-family:monospace;font-size:11px;color:#555;white-space:nowrap">{cod_oc}</td>
</tr>"""
        st.markdown(f"""
<div class="wrap"><table style="width:100%;border-collapse:collapse;font-size:13px;">
<thead><tr>
  <th style="background:#003DA5;color:white;padding:10px 10px;text-align:left">Fecha</th>
  <th style="background:#003DA5;color:white;padding:10px 10px;text-align:left">OC / Proveedor</th>
  <th style="background:#003DA5;color:white;padding:10px 10px;text-align:left">Rubro</th>
  <th style="background:#003DA5;color:white;padding:10px 10px;text-align:center">Tipo</th>
  <th style="background:#003DA5;color:white;padding:10px 10px;text-align:right">Monto neto</th>
  <th style="background:#003DA5;color:white;padding:10px 10px;text-align:center">Orden de Compra</th>
</tr></thead><tbody>{filas_oc}</tbody></table></div>""", unsafe_allow_html=True)
        components.html(make_footer("Búsqueda de Órdenes de Compra"), height=55)

# ─────────────────────────────────────────────────────────────────────────────
#  REDES SOCIALES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@keyframes socialPulse {
  0%,100% { transform: scale(1) translateY(0); box-shadow: 0 4px 15px rgba(0,0,0,.15); }
  50%      { transform: scale(1.07) translateY(-4px); box-shadow: 0 10px 25px rgba(0,0,0,.25); }
}
@keyframes socialFadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.social-wrap {
  display: flex; justify-content: center; align-items: center;
  gap: 24px; flex-wrap: wrap;
  padding: 40px 20px 20px;
  animation: socialFadeIn .8s ease both;
}
.social-btn {
  display: flex; align-items: center; gap: 10px;
  padding: 13px 26px; border-radius: 50px; text-decoration: none;
  font-family: Inter, sans-serif; font-weight: 700; font-size: 15px;
  animation: socialPulse 3s ease-in-out infinite;
  transition: filter .2s;
}
.social-btn:hover { filter: brightness(1.12); }
.social-fb  { background: #1877F2; color: white; animation-delay: 0s; }
.social-tt  { background: #010101; color: white; animation-delay: .4s; }
.social-ig  {
  background: linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);
  color: white; animation-delay: .8s;
}
.social-icon { width: 24px; height: 24px; fill: white; flex-shrink: 0; }
.social-label-block { display:flex; flex-direction:column; line-height:1.1; }
.social-name  { font-size: 11px; font-weight: 400; opacity: .85; }
.social-title { font-size: 15px; font-weight: 800; }
.social-section-title {
  text-align: center; font-family: Inter, sans-serif;
  font-size: 13px; color: #888; font-weight: 600;
  letter-spacing: 2px; text-transform: uppercase;
  margin-top: 36px; margin-bottom: 0;
  animation: socialFadeIn .6s ease both;
}
</style>

<p class="social-section-title">S&#237;guenos en redes sociales</p>
<div class="social-wrap">

  <!-- Facebook -->
  <a class="social-btn social-fb"
     href="https://www.facebook.com/profile.php?id=61576422992301" target="_blank" rel="noopener">
    <svg class="social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M24 12.073C24 5.404 18.627 0 12 0S0 5.404 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.027 1.792-4.697 4.533-4.697 1.312 0 2.686.236 2.686.236v2.97h-1.513c-1.491 0-1.956.93-1.956 1.886v2.268h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/>
    </svg>
    <span class="social-label-block">
      <span class="social-name">Facebook</span>
      <span class="social-title">Gestiona Tus Datos</span>
    </span>
  </a>

  <!-- TikTok -->
  <a class="social-btn social-tt"
     href="https://www.tiktok.com/@gestionatusdatos" target="_blank" rel="noopener">
    <svg class="social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1V9.01a6.34 6.34 0 0 0-.79-.05 6.34 6.34 0 0 0-6.34 6.34 6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.33-6.34V9.03a8.16 8.16 0 0 0 4.77 1.52V7.1a4.85 4.85 0 0 1-1-.41z"/>
    </svg>
    <span class="social-label-block">
      <span class="social-name">TikTok</span>
      <span class="social-title">@gestionatusdatos</span>
    </span>
  </a>

  <!-- Instagram -->
  <a class="social-btn social-ig"
     href="https://www.instagram.com/gestionatusdatos/" target="_blank" rel="noopener">
    <svg class="social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/>
    </svg>
    <span class="social-label-block">
      <span class="social-name">Instagram</span>
      <span class="social-title">@gestionatusdatos</span>
    </span>
  </a>

</div>
<p style="text-align:center;font-size:11px;color:#bbb;margin:8px 0 30px;font-family:Inter,sans-serif;">
  &#169; 2025 Gestiona Tus Datos &nbsp;&middot;&nbsp; www.gestionadatos.cl
</p>
""", unsafe_allow_html=True)
