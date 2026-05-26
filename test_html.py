import streamlit as st

st.set_page_config(page_title="Test", layout="wide")

st.markdown("# Test HTML Rendering")

# Test 1: Direct markdown
st.markdown("## Test 1: Direct markdown")
st.markdown('<div style="color:red;font-size:2rem;">This should be RED</div>', unsafe_allow_html=True)

# Test 2: Using st.empty() placeholder
st.markdown("## Test 2: Using st.empty() placeholder")
placeholder = st.empty()
placeholder.markdown('<div style="color:green;font-size:2rem;">This should be GREEN</div>', unsafe_allow_html=True)

# Test 3: The actual render_pipeline pattern
st.markdown("## Test 3: Actual pattern from render_pipeline")

def test_render(target=None):
    content = '<div style="background:#0b1118;border:1px solid #22c55e;border-radius:18px;padding:1rem;"><div style="color:#22c55e;font-size:1.5rem;">✓ Pipeline Step</div></div>'
    
    if target is not None:
        target.markdown(content, unsafe_allow_html=True)
    else:
        st.markdown(content, unsafe_allow_html=True)

test_ph = st.empty()
test_render(target=test_ph)
