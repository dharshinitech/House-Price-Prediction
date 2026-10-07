# ============================================================
# LIBRARY IMPORT
# ============================================================

import streamlit as st
from database import register_user


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Register",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "registration_success" not in st.session_state:
    st.session_state.registration_success = False


# ============================================================
# CSS STYLE
# ============================================================

st.markdown("""
<style>

body {
    font-family: Arial, Helvetica, sans-serif;
}


/* ---------- Main Background ---------- */

.stApp {
    background: linear-gradient(
        135deg,
        #e8f1f8 0%,
        #f5f9fc 50%,
        #dfeaf3 100%
    );
}


/* ---------- Main Container ---------- */

.main .block-container {
    max-width: 900px;
    padding-top: 45px;
    padding-bottom: 45px;
}


/* ---------- Full Registration Form ---------- */

[data-testid="stForm"] {
    background-color: white;
    padding: 35px 35px 30px 35px;
    border-radius: 16px;
    border: 1px solid #e1e8ee;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.10);
}


/* ---------- Title ---------- */

.title {
    color: #1f3c56;
    font-size: 34px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}


/* ---------- Horizontal Line ---------- */

hr {
    border: none;
    border-top: 1px solid #e1e8ee;
    margin: 15px 0 25px 0;
}


/* ---------- Labels ---------- */

label {
    color: #263746 !important;
    font-weight: 600 !important;
}


/* ---------- Input Fields ---------- */

.stTextInput {
    margin-bottom: 10px;
}


.stTextInput input {
    background-color: #f8fafc;
    border: 1px solid #d5dfe8;
    border-radius: 8px;
    height: 46px;
    color: #263746;
}


/* ---------- Input Focus ---------- */

.stTextInput input:focus {
    border: 1px solid #4a90b8;
    box-shadow: 0 0 5px rgba(74, 144, 184, 0.15);
}


/* ---------- Terms ---------- */

.terms {
    color: #5f6f7d;
    font-size: 13px;
    margin-top: 12px;
    margin-bottom: 20px;
}


.terms a {
    color: #2878a8;
    text-decoration: none;
    font-weight: 600;
}


/* ---------- Register Button ---------- */

.stFormSubmitButton > button {
    background-color: #2f80a8;
    color: white;
    border: none;
    border-radius: 8px;
    height: 46px;
    font-size: 15px;
    font-weight: 600;
}


.stFormSubmitButton > button:hover {
    background-color: #256b8d;
    color: white;
}


/* ---------- Success Message ---------- */

.success-box {
    background-color: #d9f0df;
    color: #26733f;
    border: 1px solid #a9d5b5;
    border-radius: 8px;
    padding: 12px;
    margin-top: 18px;
    text-align: center;
    font-size: 14px;
    font-weight: 600;
}


/* ---------- Sign In Box ---------- */

.signin-box {
    background-color: rgba(255, 255, 255, 0.85);
    text-align: center;
    padding: 14px;
    margin-top: 15px;
    border-radius: 10px;
    border: 1px solid #e1e8ee;
}


.signin-text {
    color: #4b5d6b;
    font-size: 13px;
}


.signin-text a {
    color: #2878a8;
    text-decoration: none;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# REGISTRATION FORM
# ============================================================

with st.form("registration_form"):

    # ========================================================
    # REGISTRATION HEADER
    # ========================================================

    st.markdown("""
    <div class="title">Register</div>

    <hr>
    """, unsafe_allow_html=True)


    # ========================================================
    # EMAIL
    # ========================================================

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )


    # ========================================================
    # PASSWORD
    # ========================================================

    password = st.text_input(
        "Password",
        placeholder="Enter your password",
        type="password"
    )


    # ========================================================
    # REPEAT PASSWORD
    # ========================================================

    repeat_password = st.text_input(
        "Repeat Password",
        placeholder="Repeat your password",
        type="password"
    )


    # ========================================================
    # TERMS AND PRIVACY
    # ========================================================

    st.markdown("""
    <div class="terms">
    By creating an account you agree to our
    <a href="#">Terms & Privacy</a>.
    </div>
    """, unsafe_allow_html=True)


    # ========================================================
    # REGISTER BUTTON
    # ========================================================

    register = st.form_submit_button(
        "Register",
        use_container_width=True
    )


# ============================================================
# REGISTER VALIDATION
# ============================================================

if register:

    if email.strip() == "":
        st.error("Please enter your email.")

    elif password.strip() == "":
        st.error("Please enter your password.")

    elif repeat_password.strip() == "":
        st.error("Please repeat your password.")

    elif password != repeat_password:
        st.error("Passwords do not match.")

    else:

        # ====================================================
        # SAVE USER TO DATABASE
        # ====================================================

        saved = register_user(
            email.strip(),
            password
        )


        # ====================================================
        # REGISTRATION SUCCESS
        # ====================================================

        if saved:

            st.session_state.registration_success = True

            st.markdown("""
            <div class="success-box">
            Registration successful!
            </div>
            """, unsafe_allow_html=True)


        # ====================================================
        # DUPLICATE EMAIL
        # ====================================================

        else:

            st.error(
                "An account with this email already exists."
            )


# ============================================================
# SIGN IN SECTION
# ============================================================

if st.session_state.registration_success:

    st.markdown("""
    <div class="signin-box">

    <div class="signin-text">
    Already have an account?
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.page_link(
        "login.py",
        label="Sign in"
    )