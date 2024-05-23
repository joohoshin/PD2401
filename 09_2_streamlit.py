import streamlit as st
from PIL import Image
import pandas as pd

# 제목 설정
st.title("Streamlit Features Demo")

# st.write
st.write("This demonstrates some of the common Streamlit features.")

# st.text
st.text("This is plain text.")

# st.markdown
st.markdown("## This is a Markdown header")

# st.image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

# st.dataframe
df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4],
    'Column 2': [10, 20, 30, 40]
})
st.dataframe(df)

# st.button
if st.button('Click me'):
    st.write('Button clicked!')

# st.slider
value = st.slider("Select a value", 0, 100, 50)
st.write("Selected value:", value)

# st.selectbox
option = st.selectbox(
    'Select an option',
    ['Option 1', 'Option 2', 'Option 3']
)
st.write('You selected:', option)

# st.checkbox
if st.checkbox('Show dataframe'):
    st.dataframe(df)

# st.radio
genre = st.radio(
    "What's your favorite genre?",
    ('Comedy', 'Drama', 'Documentary')
)

if genre == 'Comedy':
    st.write("You selected comedy.")
elif genre == 'Drama':
    st.write("You selected drama.")
else:
    st.write("You selected documentary.")
