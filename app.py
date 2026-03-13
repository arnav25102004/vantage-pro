
import streamlit as st          
import cv2                     
import numpy as np              
import plotly.graph_objects as go  
import random                   
from PIL import Image         
st.set_page_config(
    page_title="Vantage Pro | CHRIST MCA",
    page_icon="🎓",
    layout="wide",
)
RAW_MAX_CIA1 = 20
RAW_MAX_CIA2 = 50
RAW_MAX_CIA3 = 20
MAX_CIA1 = 10
MAX_CIA2 = 25
MAX_CIA3 = 10
MAX_ATTENDANCE = 5
MAX_ENDSEM = 50
TOTAL = MAX_CIA1 + MAX_CIA2 + MAX_CIA3 + MAX_ATTENDANCE + MAX_ENDSEM


def scale_mark(raw_mark, raw_max, scaled_max):
    return round((raw_mark / raw_max) * scaled_max, 2)

st.markdown("""
<style>
/* Light blue gradient background */
.stApp { background: linear-gradient(135deg, #e8f0fe, #ffffff); }

/* Sidebar — deep blue with white text */
section[data-testid="stSidebar"] { background-color: #0d47a1; }
section[data-testid="stSidebar"] * { color: #ffffff !important; }

/* ★ FIX: Force ALL main-area text to dark blue (#003366) ★ */
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp p, .stApp span, .stApp label, .stApp div,
.stApp li, .stApp td, .stApp th {
    color: #003366 !important;
}

/* Banner */
.banner {
    background: linear-gradient(90deg, #0d47a1, #1976d2);
    padding: 1.2rem; border-radius: 10px;
    text-align: center; margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(13,71,161,0.3);
}
.banner h1 { color: #ffffff !important; font-size: 1.8rem; margin: 0; }
.banner p  { color: #bbdefb !important; margin: 0.3rem 0 0 0; font-size: 0.9rem; }

/* Feedback boxes */
.ok-box  { background:#e8f5e9; border-left:5px solid #43a047;
           padding:1rem; border-radius:8px; color:#003366 !important; }
.warn-box{ background:#fff3e0; border-left:5px solid #ff9800;
           padding:1rem; border-radius:8px; color:#003366 !important; }
.err-box { background:#ffebee; border-left:5px solid #e53935;
           padding:1rem; border-radius:8px; color:#003366 !important; }
</style>
""", unsafe_allow_html=True)


def process_image(uploaded_file):
    pil_img = Image.open(uploaded_file).convert("RGB")
    img = np.array(pil_img)

   
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    
    _, thresh = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    
    random.seed(img.shape[0] % 50)
    mock_cia1 = random.randint(10, 19)
    mock_cia2 = random.randint(20, 45)
    mock_cia3 = random.randint(10, 19)
    mock_att = random.randint(3, 5)

    return img, gray, thresh, mock_cia1, mock_cia2, mock_cia3, mock_att

st.markdown("""
<div class="banner">
    <h1> Vantage Pro</h1>
    <p>Vision-Integrated Academic Performance &amp; Goal Predictor
       &nbsp;|&nbsp; CHRIST University </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Enter Your Marks")
cia1_raw = st.sidebar.slider("CIA 1  (out of 20)", 0, RAW_MAX_CIA1, 14)
cia2_raw = st.sidebar.slider("CIA 2  (out of 50)", 0, RAW_MAX_CIA2, 30)
cia3_raw = st.sidebar.slider("CIA 3  (out of 20)", 0, RAW_MAX_CIA3, 14)
attendance = st.sidebar.slider("Attendance (out of 5)", 0, MAX_ATTENDANCE, 4)

st.sidebar.markdown("---")
st.sidebar.header(" Set Your Target")
target = st.sidebar.slider("Target Total (out of 100)", 0, TOTAL, 70)

cia1 = scale_mark(cia1_raw, RAW_MAX_CIA1, MAX_CIA1)
cia2 = scale_mark(cia2_raw, RAW_MAX_CIA2, MAX_CIA2)
cia3 = scale_mark(cia3_raw, RAW_MAX_CIA3, MAX_CIA3)
scaled_cia_total = round(cia1 + cia2 + cia3, 2)
internal = round(scaled_cia_total + attendance, 2)

needed_in_ese = target - internal           
pct = (target / TOTAL) * 100
cgpa = (4.0 if pct >= 90 else 3.6 if pct >= 80 else 3.2 if pct >= 70
    else 2.8 if pct >= 60 else 2.4 if pct >= 50 else 2.0 if pct >= 40
    else 0.0)

st.header(" Dashboard Overview")

st.subheader("Raw vs Scaled CIA")
r1, r2, r3 = st.columns(3)
r1.metric("CIA 1", f"{cia1_raw} / {RAW_MAX_CIA1}", f"Scaled: {cia1:.2f} / {MAX_CIA1}")
r2.metric("CIA 2", f"{cia2_raw} / {RAW_MAX_CIA2}", f"Scaled: {cia2:.2f} / {MAX_CIA2}")
r3.metric("CIA 3", f"{cia3_raw} / {RAW_MAX_CIA3}", f"Scaled: {cia3:.2f} / {MAX_CIA3}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Internal Total",  f"{internal} / 50")
col2.metric("Internal %",      f"{round(internal / TOTAL * 100, 2)}%")
col3.metric("Target Total",    f"{target} / 100")
col4.metric("Target CGPA (≈)",  cgpa)
left, right = st.columns([3, 2])
with left:
    st.subheader("End-Sem Marks Required")
    
    progress_val = max(0, min(needed_in_ese / 50, 1.0))

    st.title(f"{needed_in_ese:.2f} / 50")
    st.progress(progress_val)

with right:
    if needed_in_ese <= 0:
        st.markdown(
            '<div class="ok-box"><b> Congratulations!</b><br>'
            'Your internals already exceed the target!</div>',
            unsafe_allow_html=True)
        st.balloons()

    elif needed_in_ese > MAX_ENDSEM:
        gap = needed_in_ese - MAX_ENDSEM
        st.markdown(
            f'<div class="err-box"><b>Target Unreachable</b><br>'
            f'You need <b>{needed_in_ese:.2f}</b> but max End-Sem is '
            f'<b>{MAX_ENDSEM}</b>. Short by <b>{gap:.2f}</b> marks.</div>',
            unsafe_allow_html=True)

    elif needed_in_ese > MAX_ENDSEM * 0.85:
        st.markdown(
            f'<div class="warn-box"><b>Tough but Possible</b><br>'
            f'You need <b>{needed_in_ese:.2f}/{MAX_ENDSEM}</b> '
            f'({round(needed_in_ese / MAX_ENDSEM * 100, 1)}%). '
            f'Study hard!</div>',
            unsafe_allow_html=True)

    else:
        st.markdown(
            f'<div class="ok-box"><b>✅ On Track!</b><br>'
            f'You need <b>{needed_in_ese:.2f}/{MAX_ENDSEM}</b> '
            f'({round(needed_in_ese / MAX_ENDSEM * 100, 1)}%). '
            f'Keep it up!</div>',
            unsafe_allow_html=True)


st.header("Marks Comparison")

if "avg" not in st.session_state:
    st.session_state.avg = {
        "CIA 1": round(random.uniform(4.5, 8.5), 2),
        "CIA 2": round(random.uniform(11.0, 20.0), 2),
        "CIA 3": round(random.uniform(4.5, 8.5), 2),
        "Attendance": round(random.uniform(3, 4.5), 1),
    }
avg = st.session_state.avg

components = ["CIA 1", "CIA 2", "CIA 3", "Attendance"]
your_vals  = [cia1, cia2, cia3, attendance]
avg_vals   = [avg[c] for c in components]

bar = go.Figure()
bar.add_trace(go.Bar(name="Your Marks",    x=components, y=your_vals,
                     marker_color="#1565c0", text=your_vals,
                     textposition="outside"))
bar.add_trace(go.Bar(name="Class Average", x=components, y=avg_vals,
                     marker_color="#90caf9", text=avg_vals,
                     textposition="outside"))
bar.update_layout(barmode="group", yaxis=dict(range=[0, 25]), height=380,
                  paper_bgcolor="rgba(0,0,0,0)",
                  plot_bgcolor="rgba(0,0,0,0)",
                  title={"text": "Your Marks vs Class Average",
                         "font": {"color": "#003366"}},
                  font={"color": "#003366"})
st.plotly_chart(bar, use_container_width=True)

st.header(" Vision: Upload Marksheet Image")
st.write("Upload a marksheet photo. OpenCV processes it "
         "(Grayscale → Threshold) and a **mock OCR** extracts marks.")

uploaded = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded:
    try:
        original, gray, thresh, m_cia1, m_cia2, m_cia3, m_att = process_image(uploaded)
        m_cia1_scaled = scale_mark(m_cia1, RAW_MAX_CIA1, MAX_CIA1)
        m_cia2_scaled = scale_mark(m_cia2, RAW_MAX_CIA2, MAX_CIA2)
        m_cia3_scaled = scale_mark(m_cia3, RAW_MAX_CIA3, MAX_CIA3)

        # Show the 3 processing stages
        c1, c2, c3 = st.columns(3)
        c1.image(original, caption="Original",    use_container_width=True)
        c2.image(gray,     caption="Grayscale",   use_container_width=True)
        c3.image(thresh,   caption="Thresholded", use_container_width=True)

        # Show mock-detected marks
        st.subheader(" Detected Marks (Mock OCR)")
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("CIA 1",      f"{m_cia1} / {RAW_MAX_CIA1}", f"Scaled: {m_cia1_scaled:.2f} / {MAX_CIA1}")
        d2.metric("CIA 2",      f"{m_cia2} / {RAW_MAX_CIA2}", f"Scaled: {m_cia2_scaled:.2f} / {MAX_CIA2}")
        d3.metric("CIA 3",      f"{m_cia3} / {RAW_MAX_CIA3}", f"Scaled: {m_cia3_scaled:.2f} / {MAX_CIA3}")
        d4.metric("Attendance", f"{m_att} / {MAX_ATTENDANCE}")

        st.info(f"Set sidebar sliders to: CIA 1 = {m_cia1}, "
            f"CIA 2 = {m_cia2}, CIA 3 = {m_cia3}, Attendance = {m_att}")

    except Exception as e:
        st.error(f" Could not process image: {e}")

st.header(" Marks Breakdown")

st.table({
    "Component":  ["CIA 1", "CIA 2", "CIA 3", "Attendance", "CIA Scaled Subtotal",
                   "Internal Final", "End-Sem (Required)", "Projected Total"],
    "Raw Input":  [cia1_raw, cia2_raw, cia3_raw, attendance, "-", "-", "-", "-"],
    "Scaled/Used": [f"{cia1:.2f}", f"{cia2:.2f}", f"{cia3:.2f}", f"{attendance:.2f}",
                   f"{scaled_cia_total:.2f}", f"{internal:.2f}",
                   f"{min(needed_in_ese, MAX_ENDSEM):.2f}" if needed_in_ese <= MAX_ENDSEM
                   else f"{needed_in_ese:.2f} ⚠️",
                   f"{min(target, internal + MAX_ENDSEM):.2f}"],
    "Maximum":    [f"{RAW_MAX_CIA1} → {MAX_CIA1}", f"{RAW_MAX_CIA2} → {MAX_CIA2}",
                   f"{RAW_MAX_CIA3} → {MAX_CIA3}", MAX_ATTENDANCE, 45, 50, MAX_ENDSEM, TOTAL],
})
with st.expander(" CGPA Reference Table"):
    st.markdown("""
| % Range   | CGPA (Out of 4) | Grade |
|:---------:|:----:|:-----:|
| 90 – 100  | 4.0            | O     |
| 80 – 89   | 3.6            | A+    |
| 70 – 79   | 3.2            | A     |
| 60 – 69   | 2.8            | B+    |
| 50 – 59   | 2.4            | B     |
| 40 – 49   | 2.0            | C     |
| < 40      | 0.0            | F     |

> *Approximate mapping to 4-point scale. Refer to MCA Christ Rules for exact rules.*
""")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#78909c !important; font-size:0.85rem;'>"
    "<b>Vantage Pro</b> — Built by ARNAV NARULA 2547115 "
    "| CHRIST University 3MCA-A</p>",
    unsafe_allow_html=True)
