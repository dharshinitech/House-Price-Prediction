import streamlit as st
import extra_streamlit_components as stx


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="House Value Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# COOKIE MANAGER
# IMPORTANT: UNIQUE KEY
# ============================================================

cookie_manager = stx.CookieManager(
    key="main_cookie_manager"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ============================================================
# RESTORE LOGIN AFTER REFRESH
# ============================================================

login_cookie = cookie_manager.get(
    "house_price_login"
)

if login_cookie == "true":
    st.session_state.logged_in = True

# ============================================================
# GLOBAL CSS
# ============================================================

st.html("""
<style>

/* ================================
   MAIN PAGE
================================ */

.stApp {
    background: #f5f7fa;
}

.main .block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    max-width: 1500px;
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #172a46 0%, #203b5f 100%);
    border-right: 1px solid #314d70;
}

section[data-testid="stSidebar"] * {
    color: #ffffff;
}


/* ================================
   TOP BRAND BAR
================================ */

.brand-bar {
    height: 76px;
    width: 100%;

    background: #ffffff;

    display: flex;
    align-items: center;

    padding: 0 42px;

    border-bottom: 1px solid #e5eaf0;

    box-sizing: border-box;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    width: 44px;
    height: 44px;

    border-radius: 11px;

    background: #eaf2fb;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 24px;
}

.brand-main {
    font-size: 18px;
    font-weight: 850;
    letter-spacing: 0.5px;
    color: #18324f;
}

.brand-sub {
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 1.6px;
    color: #3474b7;
    margin-top: 2px;
}


/* ================================
   HERO
================================ */

.hero {
    display: grid;

    grid-template-columns: 44% 56%;

    min-height: 455px;

    background: #ffffff;
}


/* LEFT */

.hero-content {

    background:
        linear-gradient(
            135deg,
            #f8fbff 0%,
            #eaf2fb 100%
        );

    padding: 54px 54px;

    display: flex;

    flex-direction: column;

    justify-content: center;
}


.hero-tag {

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1.5px;

    color: #3475b9;

    margin-bottom: 17px;
}


.hero-heading {

    font-size: 45px;

    line-height: 1.08;

    font-weight: 850;

    color: #172f4c;

    margin: 0;
}


.hero-heading span {
    color: #3275bb;
}


.hero-line {

    width: 68px;

    height: 4px;

    background: #3275bb;

    border-radius: 10px;

    margin: 20px 0;
}


.hero-description {

    max-width: 500px;

    color: #64758a;

    font-size: 14px;

    line-height: 1.75;

    margin: 0;
}


/* HERO MINI ITEMS */

.hero-mini {

    display: flex;

    gap: 28px;

    margin-top: 27px;
}


.mini-item {

    display: flex;

    align-items: center;

    gap: 8px;
}


.mini-icon {
    font-size: 20px;
}


.mini-text {

    color: #607187;

    font-size: 10px;

    line-height: 1.4;
}


/* RIGHT IMAGE */

.hero-image {

    min-height: 455px;

    background-image:
        url(
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=90"
        );

    background-size: cover;

    background-position: center;
}


/* ================================
   BLUE STAT BAR
================================ */

.stat-bar {

    background: #316ba5;

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    padding: 25px 34px;
}


.stat {

    text-align: center;

    color: white;

    border-right:
        1px solid
        rgba(255,255,255,0.25);

    padding: 2px 15px;
}


.stat:last-child {
    border-right: none;
}


.stat-icon {
    font-size: 23px;
}


.stat-number {

    font-size: 20px;

    font-weight: 850;

    margin-top: 4px;
}


.stat-label {

    font-size: 10px;

    opacity: 0.9;

    margin-top: 3px;
}


/* ================================
   SECTION COMMON
================================ */

.section {

    background: #ffffff;

    padding: 48px 42px;
}


.section-heading {

    text-align: center;

    font-size: 28px;

    font-weight: 850;

    color: #1c334e;

    margin-bottom: 7px;
}


.section-description {

    text-align: center;

    color: #77869a;

    font-size: 12px;

    margin-bottom: 28px;
}


/* ================================
   FEATURE CARDS
================================ */

.feature-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 22px;
}


.feature-card {

    border: 1px solid #e1e7ee;

    background: #ffffff;

    border-radius: 10px;

    overflow: hidden;

    box-shadow:
        0 6px 18px
        rgba(35,55,80,0.06);
}


.feature-icon-area {

    height: 105px;

    background: #edf4fb;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 48px;
}


.feature-body {

    padding: 19px 20px 21px;
}


.feature-title {

    color: #1c3552;

    font-size: 17px;

    font-weight: 800;

    margin-bottom: 8px;
}


.feature-text {

    color: #728095;

    font-size: 11px;

    line-height: 1.7;
}


/* ================================
   ABOUT PROJECT
================================ */

.about-section {

    background:
        linear-gradient(
            135deg,
            #edf5fc,
            #f8fbff
        );

    padding: 48px 60px;

    display: grid;

    grid-template-columns:
        0.8fr 2.2fr 0.9fr;

    align-items: center;

    gap: 30px;
}


.about-house {

    text-align: center;

    font-size: 76px;
}


.about-content {

    text-align: center;
}


.about-title {

    font-size: 27px;

    font-weight: 850;

    color: #1b304a;

    margin-bottom: 13px;
}


.about-line {

    width: 52px;

    height: 3px;

    background: #3475b9;

    margin: 0 auto 16px;
}


.about-text {

    color: #68798d;

    font-size: 12px;

    line-height: 1.8;
}


.about-highlight {

    background: #ffffff;

    border: 1px solid #dce5ee;

    border-radius: 11px;

    padding: 21px;

    text-align: center;

    box-shadow:
        0 5px 16px
        rgba(40,70,100,0.06);
}


.about-highlight-icon {
    font-size: 31px;
}


.about-highlight-title {

    color: #1d3552;

    font-size: 14px;

    font-weight: 800;

    margin-top: 6px;
}


.about-highlight-text {

    color: #77869a;

    font-size: 10px;

    line-height: 1.55;

    margin-top: 5px;
}


/* ================================
   WORKFLOW
================================ */

.workflow {

    background: #ffffff;

    padding: 45px 42px;
}


.workflow-title {

    text-align: center;

    color: #1c334e;

    font-size: 27px;

    font-weight: 850;

    margin-bottom: 27px;
}


.workflow-grid {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 18px;
}


.workflow-card {

    text-align: center;

    background: #f8fafc;

    border: 1px solid #e2e8ef;

    border-radius: 10px;

    padding: 20px 16px;
}


.workflow-number {

    width: 36px;

    height: 36px;

    margin: 0 auto;

    border-radius: 50%;

    background: #316ba5;

    color: white;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 12px;

    font-weight: 850;
}


.workflow-name {

    color: #1d3552;

    font-size: 14px;

    font-weight: 800;

    margin-top: 10px;
}


.workflow-text {

    color: #748296;

    font-size: 10px;

    line-height: 1.6;

    margin-top: 6px;
}


/* ================================
   FOOTER
================================ */

.footer {

    background: #111f2e;

    padding: 34px 48px 17px;

    color: white;
}


.footer-grid {

    display: grid;

    grid-template-columns:
        1.7fr 1fr 1fr 1fr;

    gap: 35px;
}


.footer-brand {

    font-size: 18px;

    font-weight: 850;
}


.footer-brand span {
    color: #4c8dd4;
}


.footer-text {

    max-width: 300px;

    color: #9baabd;

    font-size: 10px;

    line-height: 1.7;

    margin-top: 9px;
}


.footer-title {

    font-size: 11px;

    font-weight: 800;

    margin-bottom: 8px;
}


.footer-item {

    color: #9baabd;

    font-size: 10px;

    line-height: 1.9;
}


.footer-bottom {

    border-top:
        1px solid
        rgba(255,255,255,0.1);

    margin-top: 25px;

    padding-top: 13px;

    text-align: center;

    color: #78889a;

    font-size: 9px;
}


/* ================================
   RESPONSIVE
================================ */

@media (max-width: 900px) {

    .hero {
        grid-template-columns: 1fr;
    }

    .hero-image {
        min-height: 300px;
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .stat-bar {
        grid-template-columns: repeat(2, 1fr);
        gap: 18px;
    }

    .stat:nth-child(2) {
        border-right: none;
    }

    .about-section {
        grid-template-columns: 1fr;
        padding: 40px 25px;
    }

    .workflow-grid {
        grid-template-columns: 1fr 1fr;
    }

    .footer-grid {
        grid-template-columns: 1fr 1fr;
    }
}

</style>
""")


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    # ========================================================
    # BRAND HEADER
    # ========================================================

    st.html("""
    <div class="brand-bar">

        <div class="brand">

            <div class="brand-icon">
                🏠
            </div>

            <div>

                <div class="brand-main">
                    HOUSE VALUE
                </div>

                <div class="brand-sub">
                    PREDICTOR
                </div>

            </div>

        </div>

    </div>
    """)


    # ========================================================
    # HERO
    # ========================================================

    st.html("""
    <div class="hero">

        <div class="hero-content">

            <div class="hero-tag">
                DATA SCIENCE • MACHINE LEARNING • REAL ESTATE
            </div>


            <div class="hero-heading">
                Predict Smarter.<br>
                Understand<br>
                <span>Property Value.</span>
            </div>


            <div class="hero-line"></div>


            <div class="hero-description">
                House Price Prediction is a Data Science and
                Machine Learning project designed to analyze
                housing data, understand property characteristics
                and estimate house prices using a trained
                Random Forest Regression model.
            </div>


            <div class="hero-mini">

                <div class="mini-item">

                    <div class="mini-icon">
                        📊
                    </div>

                    <div class="mini-text">
                        Data<br>
                        Analytics
                    </div>

                </div>


                <div class="mini-item">

                    <div class="mini-icon">
                        🧠
                    </div>

                    <div class="mini-text">
                        Machine<br>
                        Learning
                    </div>

                </div>


                <div class="mini-item">

                    <div class="mini-icon">
                        🎯
                    </div>

                    <div class="mini-text">
                        Price<br>
                        Prediction
                    </div>

                </div>

            </div>

        </div>


        <div class="hero-image"></div>

    </div>
    """)


    # ========================================================
    # STATISTICS
    # ========================================================

    st.html("""
    <div class="stat-bar">


        <div class="stat">

            <div class="stat-icon">
                🏠
            </div>

            <div class="stat-number">
                2,000+
            </div>

            <div class="stat-label">
                Properties Analyzed
            </div>

        </div>


        <div class="stat">

            <div class="stat-icon">
                📊
            </div>

            <div class="stat-number">
                10+
            </div>

            <div class="stat-label">
                Property Features
            </div>

        </div>


        <div class="stat">

            <div class="stat-icon">
                🧠
            </div>

            <div class="stat-number">
                Random Forest
            </div>

            <div class="stat-label">
                Regression Model
            </div>

        </div>


        <div class="stat">

            <div class="stat-icon">
                🎯
            </div>

            <div class="stat-number">
                Smart
            </div>

            <div class="stat-label">
                Price Prediction
            </div>

        </div>


    </div>
    """)


    # ========================================================
    # FEATURES
    # ========================================================

    st.html("""
    <div class="section">

        <div class="section-heading">
            What This Project Offers
        </div>

        <div class="section-description">
            From housing data analysis to intelligent machine
            learning based price prediction.
        </div>


        <div class="feature-grid">


            <div class="feature-card">

                <div class="feature-icon-area">
                    📊
                </div>

                <div class="feature-body">

                    <div class="feature-title">
                        Data Analytics
                    </div>

                    <div class="feature-text">
                        Analyze housing records, identify patterns,
                        study distributions and understand the
                        relationship between property features
                        and prices.
                    </div>

                </div>

            </div>


            <div class="feature-card">

                <div class="feature-icon-area">
                    🧠
                </div>

                <div class="feature-body">

                    <div class="feature-title">
                        Machine Learning
                    </div>

                    <div class="feature-text">
                        A Random Forest Regression model is trained
                        using important property characteristics
                        to learn housing price patterns.
                    </div>

                </div>

            </div>


            <div class="feature-card">

                <div class="feature-icon-area">
                    🎯
                </div>

                <div class="feature-body">

                    <div class="feature-title">
                        Price Prediction
                    </div>

                    <div class="feature-text">
                        Property details are processed through the
                        trained model to generate an estimated
                        house price.
                    </div>

                </div>

            </div>


        </div>

    </div>
    """)


    # ========================================================
    # ABOUT PROJECT
    # ========================================================

    st.html("""
    <div class="about-section">


        <div class="about-house">
            🏡
        </div>


        <div class="about-content">

            <div class="about-title">
                A Data-Driven Way to Understand House Prices
            </div>

            <div class="about-line"></div>

            <div class="about-text">
                This project combines Data Cleaning,
                Exploratory Data Analysis, Feature Engineering
                and Machine Learning to study housing patterns
                and predict property prices. Property
                characteristics such as area, bedrooms,
                bathrooms, location, condition, garage and
                house age are used to build the prediction
                system.
            </div>

        </div>


        <div class="about-highlight">

            <div class="about-highlight-icon">
                📈
            </div>

            <div class="about-highlight-title">
                Data Driven
            </div>

            <div class="about-highlight-text">
                Turning housing data into meaningful insights
                and predictions.
            </div>

        </div>


    </div>
    """)


    # ========================================================
    # WORKFLOW
    # ========================================================

    st.html("""
    <div class="workflow">

        <div class="workflow-title">
            Project Workflow
        </div>


        <div class="workflow-grid">


            <div class="workflow-card">

                <div class="workflow-number">
                    01
                </div>

                <div class="workflow-name">
                    Data Collection
                </div>

                <div class="workflow-text">
                    Housing records are collected and prepared
                    for analysis.
                </div>

            </div>


            <div class="workflow-card">

                <div class="workflow-number">
                    02
                </div>

                <div class="workflow-name">
                    Data Preparation
                </div>

                <div class="workflow-text">
                    Missing values, duplicates and categorical
                    information are processed.
                </div>

            </div>


            <div class="workflow-card">

                <div class="workflow-number">
                    03
                </div>

                <div class="workflow-name">
                    Data Analysis
                </div>

                <div class="workflow-text">
                    Patterns, relationships and important
                    property features are analyzed.
                </div>

            </div>


            <div class="workflow-card">

                <div class="workflow-number">
                    04
                </div>

                <div class="workflow-name">
                    Prediction
                </div>

                <div class="workflow-text">
                    The trained Random Forest model estimates
                    the house price.
                </div>

            </div>


        </div>

    </div>
    """)


    # ========================================================
    # FOOTER
    # ========================================================

    st.html("""
    <div class="footer">

        <div class="footer-grid">


            <div>

                <div class="footer-brand">
                    HOUSE VALUE
                    <span>PREDICTOR</span>
                </div>

                <div class="footer-text">
                    A Data Science and Machine Learning application
                    designed to analyze housing data and estimate
                    property prices using intelligent prediction
                    techniques.
                </div>

            </div>


            <div>

                <div class="footer-title">
                    PROJECT
                </div>

                <div class="footer-item">
                    Data Cleaning
                </div>

                <div class="footer-item">
                    EDA
                </div>

                <div class="footer-item">
                    Feature Engineering
                </div>

                <div class="footer-item">
                    Model Evaluation
                </div>

            </div>


            <div>

                <div class="footer-title">
                    MACHINE LEARNING
                </div>

                <div class="footer-item">
                    Random Forest
                </div>

                <div class="footer-item">
                    Regression
                </div>

                <div class="footer-item">
                    Prediction
                </div>

            </div>


            <div>

                <div class="footer-title">
                    TECHNOLOGY
                </div>

                <div class="footer-item">
                    Python
                </div>

                <div class="footer-item">
                    Pandas
                </div>

                <div class="footer-item">
                    Scikit-learn
                </div>

                <div class="footer-item">
                    Streamlit
                </div>

            </div>


        </div>


        <div class="footer-bottom">
            © 2026 House Value Predictor
            • Data Science & Machine Learning Project
        </div>

    </div>
    """)


# ============================================================
# PAGE DEFINITIONS
# ============================================================

login_page = st.Page(
    "login.py",
    title="Login",
    icon="🔐"
)

registration_page = st.Page(
    "registration.py",
    title="Register",
    icon="📝"
)

home_navigation = st.Page(
    home_page,
    title="Home",
    icon="🏠"
)

dashboard_page = st.Page(
    "app.py",
    title="Dashboard",
    icon="📊"
)


# ============================================================
# LOGOUT
# ============================================================

if st.session_state.logged_in:

    with st.sidebar:

        st.markdown("---")

        st.markdown(
            """
            <div style="
                color:#ffffff;
                font-weight:700;
                font-size:13px;
                padding:5px 0;
            ">
                Account
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🚪 Logout",
            use_container_width=True,
            key="logout_button"
        ):

            # Delete login cookie
            cookie_manager.delete(
                "house_price_login"
            )

            # Clear session
            st.session_state.logged_in = False

            st.rerun()


# ============================================================
# NAVIGATION
# ============================================================

if st.session_state.logged_in:

    page = st.navigation(
        {
            "Select Page": [
                home_navigation,
                dashboard_page
            ]
        },
        position="sidebar"
    )

else:

    page = st.navigation(
        {
            "Account": [
                login_page,
                registration_page
            ]
        },
        position="sidebar"
    )


# ============================================================
# RUN
# ============================================================

page.run()