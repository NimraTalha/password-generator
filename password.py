import streamlit as st
import random
import string
import pyperclip
from zxcvbn import zxcvbn

def generate_password(length, use_digits, use_special, use_upper):
    characters = string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def main():
    st.set_page_config(page_title="Advanced Password Generator", layout="centered")
    st.title("🔐 Advanced Password Generator & Strength Checker")
    
    length = st.slider("Select Password Length", min_value=8, max_value=64, value=16)
    use_upper = st.checkbox("Include Uppercase Letters", value=True)
    use_digits = st.checkbox("Include Numbers", value=True)
    use_special = st.checkbox("Include Special Characters", value=True)
    
    if st.button("Generate Password"):
        password = generate_password(length, use_digits, use_special, use_upper)
        st.text_input("Generated Password", password, key="password")
        
        strength = zxcvbn(password)
        score = strength['score']
        entropy = strength['guesses_log10']
        
        st.markdown(f"**Password Strength:** {['Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong'][score]}")
        st.markdown(f"**Entropy:** {entropy:.2f} bits")
        
        if st.button("Copy to Clipboard"):
            pyperclip.copy(password)
            st.success("Password copied to clipboard!")
    
    if st.button("Download Password as TXT"):
        with open("password.txt", "w") as f:
            f.write(st.session_state.get("password", ""))
        st.download_button(label="Download", data="password.txt", file_name="password.txt", mime="text/plain")
    
if __name__ == "__main__":
    main()