import streamlit as st
import extra_streamlit_components as stx
from database import login_user
from datetime import datetime, timedelta


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)


# ============================================================
# COOKIE MANAGER
# ============================================================

cookie_manager = stx.CookieManager(
    key="login_cookie_manager"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ============================================================
# CHECK EXISTING LOGIN
# ============================================================

login_cookie = cookie_manager.get(
    "house_price_login"
)

if login_cookie == "true":
    st.session_state.logged_in = True


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #e8f1f8 0%,
        #f5f9fc 50%,
        #dfeaf3 100%
    );
}

.main .block-container {
    max-width: 540px;
    padding-top: 45px;
    padding-bottom: 45px;
}

[data-testid="stForm"] {
    background-color: white;
    padding: 35px;
    border-radius: 16px;
    border: 1px solid #e1e8ee;
    box-shadow: 0 8px 30px rgba(0,0,0,0.10);
}

.title {
    color: #1f3c56;
    font-size: 34px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

hr {
    border: none;
    border-top: 1px solid #e1e8ee;
    margin: 15px 0 25px 0;
}

label {
    color: #263746 !important;
    font-weight: 600 !important;
}

.stTextInput input {
    background-color: #f8fafc;
    border: 1px solid #d5dfe8;
    border-radius: 8px;
    height: 46px;
    color: #263746;
}

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
}

.register-box {
    background-color: rgba(255,255,255,0.85);
    text-align: center;
    padding: 14px;
    margin-top: 15px;
    border-radius: 10px;
    border: 1px solid #e1e8ee;
}

.register-text {
    color: #4b5d6b;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN FORM
# ============================================================

with st.form("login_form"):

    st.markdown(
        """
        <div class="title">Login</div>
        <hr>
        """,
        unsafe_allow_html=True
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        placeholder="Enter your password",
        type="password"
    )

    login = st.form_submit_button(
        "Login",
        use_container_width=True
    )


# ============================================================
# LOGIN VALIDATION
# ============================================================

if login:

    if email.strip() == "":
        st.error("Please enter your email.")

    elif password.strip() == "":
        st.error("Please enter your password.")

    else:

        user = login_user(
            email.strip(),
            password
        )

        if user:

            # Save session
            st.session_state.logged_in = True

            # Save browser cookie for 7 days
            cookie_manager.set(
                "house_price_login",
                "true",
                expires_at=datetime.now() + timedelta(days=7)
            )

            st.success("Login successful!")

            st.rerun()

        else:

            st.error("Invalid email or password.")


# ============================================================
# REGISTER
# ============================================================

st.markdown(
    """
    <div class="register-box">
        <div class="register-text">
            Don't have an account?
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.page_link(
    "registration.py",
    label="Register"
)