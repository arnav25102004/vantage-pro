
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
MAX_CIA1 = 20           
MAX_CIA2 = 20           
MAX_ATTENDANCE = 5     
MAX_ENDSEM = 50         
TOTAL = MAX_CIA1 + MAX_CIA2 + MAX_ATTENDANCE + MAX_ENDSEM  

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

    # Grayscale conversion
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Binary threshold using Otsu's method
    _, thresh = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Mock OCR — return dummy marks seeded from image dimensions
    random.seed(img.shape[0] % 50)
    mock_cia1 = random.randint(10, 19)
    mock_cia2 = random.randint(9, 18)
    mock_att  = random.randint(3, 5)

    return img, gray, thresh, mock_cia1, mock_cia2, mock_att

st.markdown("""
<div class="banner">
    <h1> Vantage Pro</h1>
    <p>Vision-Integrated Academic Performance &amp; Goal Predictor
       &nbsp;|&nbsp; CHRIST University </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("Enter Your Marks")
cia1       = st.sidebar.slider("CIA 1  (out of 20)",      0, MAX_CIA1, 14)
cia2       = st.sidebar.slider("CIA 2  (out of 20)",      0, MAX_CIA2, 13)
attendance = st.sidebar.slider("Attendance (out of 5)",    0, MAX_ATTENDANCE, 4)

st.sidebar.markdown("---")
st.sidebar.header(" Set Your Target")
target     = st.sidebar.slider("Target Total (out of 95)", 0, TOTAL, 70)

internal = cia1 + cia2 + attendance         

needed_in_ese = target - internal           
pct = (target / TOTAL) * 100
gpa = (10.0 if pct >= 90 else 9.0 if pct >= 80 else 8.0 if pct >= 70
       else 7.0 if pct >= 60 else 6.0 if pct >= 50 else 5.0 if pct >= 40
       else 0.0)

st.header(" Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Internal Total",  f"{internal} / 45")
col2.metric("Internal %",      f"{round(internal / TOTAL * 100, 1)}%")
col3.metric("Target Total",    f"{target} / 95")
col4.metric("Target GPA (≈)",  gpa)
left, right = st.columns([3, 2])
with left:
    st.subheader("End-Sem Marks Required")
    
    progress_val = max(0, min(needed_in_ese / 50, 1.0))

    st.title(f"{needed_in_ese} / 50")
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
            f'You need <b>{needed_in_ese}</b> but max End-Sem is '
            f'<b>{MAX_ENDSEM}</b>. Short by <b>{gap}</b> marks.</div>',
            unsafe_allow_html=True)

    elif needed_in_ese > MAX_ENDSEM * 0.85:
        st.markdown(
            f'<div class="warn-box"><b>Tough but Possible</b><br>'
            f'You need <b>{needed_in_ese}/{MAX_ENDSEM}</b> '
            f'({round(needed_in_ese / MAX_ENDSEM * 100, 1)}%). '
            f'Study hard!</div>',
            unsafe_allow_html=True)

    else:
        st.markdown(
            f'<div class="ok-box"><b>✅ On Track!</b><br>'
            f'You need <b>{needed_in_ese}/{MAX_ENDSEM}</b> '
            f'({round(needed_in_ese / MAX_ENDSEM * 100, 1)}%). '
            f'Keep it up!</div>',
            unsafe_allow_html=True)


st.header("Marks Comparison")

if "avg" not in st.session_state:
    st.session_state.avg = {
        "CIA 1": round(random.uniform(11, 16), 1),
        "CIA 2": round(random.uniform(10, 15), 1),
        "Attendance": round(random.uniform(3, 4.5), 1),
    }
avg = st.session_state.avg

components = ["CIA 1", "CIA 2", "Attendance"]
your_vals  = [cia1, cia2, attendance]
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
        original, gray, thresh, m_cia1, m_cia2, m_att = process_image(uploaded)

        # Show the 3 processing stages
        c1, c2, c3 = st.columns(3)
        c1.image(original, caption="Original",    use_container_width=True)
        c2.image(gray,     caption="Grayscale",   use_container_width=True)
        c3.image(thresh,   caption="Thresholded", use_container_width=True)

        # Show mock-detected marks
        st.subheader(" Detected Marks (Mock OCR)")
        d1, d2, d3 = st.columns(3)
        d1.metric("CIA 1",      f"{m_cia1} / {MAX_CIA1}")
        d2.metric("CIA 2",      f"{m_cia2} / {MAX_CIA2}")
        d3.metric("Attendance", f"{m_att} / {MAX_ATTENDANCE}")

        st.info(f"Set sidebar sliders to: CIA 1 = {m_cia1}, "
                f"CIA 2 = {m_cia2}, Attendance = {m_att}")

    except Exception as e:
        st.error(f" Could not process image: {e}")

st.header(" Marks Breakdown")

st.table({
    "Component":  ["CIA 1", "CIA 2", "Attendance",
                   "End-Sem (Required)", "Projected Total"],
    "Your Marks": [cia1, cia2, attendance,
                   min(needed_in_ese, MAX_ENDSEM) if needed_in_ese <= MAX_ENDSEM
                   else f"{needed_in_ese} ⚠️",
                   min(target, internal + MAX_ENDSEM)],
    "Maximum":    [MAX_CIA1, MAX_CIA2, MAX_ATTENDANCE, MAX_ENDSEM, TOTAL],
})
with st.expander(" GPA Reference Table"):
    st.markdown("""
| % Range   | GPA  | Grade |
|:---------:|:----:|:-----:|
| 90 – 100  | 10.0 | O     |
| 80 – 89   | 9.0  | A+    |
| 70 – 79   | 8.0  | A     |
| 60 – 69   | 7.0  | B+    |
| 50 – 59   | 6.0  | B     |
| 40 – 49   | 5.0  | C     |
| < 40      | 0.0  | F     |

> *Approximate mapping. Refer to MCA handbook for exact rules.*
""")

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#78909c !important; font-size:0.85rem;'>"
    "<b>Vantage Pro</b> — Built by ARNAV NARULA 2547115 "
    "| CHRIST University 3MCA-A</p>",
    unsafe_allow_html=True)
