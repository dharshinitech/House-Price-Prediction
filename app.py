import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="House Price Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL POWER BI-STYLE THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f7f4fb 0%,
        #eef7f6 52%,
        #f8f9fc 100%
    );
}

.main .block-container {
    max-width: 1480px;
    padding: 0.8rem 1rem 1rem 1rem !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #35245f 0%,
        #49327a 55%,
        #26756f 100%
    );
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Header */
.dashboard-header {
    background: linear-gradient(
        135deg,
        #35245f 0%,
        #5b438e 52%,
        #26756f 100%
    );
    padding: 18px 24px;
    border-radius: 15px;
    margin-bottom: 12px;
    box-shadow: 0 7px 20px rgba(53,36,95,0.14);
}

.dashboard-header h1 {
    color: #ffffff !important;
    margin: 0 !important;
    font-size: 29px !important;
    font-weight: 800 !important;
}

.dashboard-header p {
    color: #eee9f7;
    margin: 5px 0 0 0;
    font-size: 13px;
}

/* Section headings */
.section-heading {
    color: #35245f;
    font-size: 17px;
    font-weight: 800;
    margin: 8px 0 5px 0;
}

/* KPI cards */
.kpi-card {
    background: rgba(255,255,255,0.97);
    border: 1px solid #e2dced;
    border-radius: 13px;
    min-height: 82px;
    padding: 12px 15px;
    box-shadow: 0 4px 14px rgba(53,36,95,0.07);
}

.kpi-purple { border-left: 5px solid #6f55a5; }
.kpi-teal { border-left: 5px solid #2d8c84; }
.kpi-orange { border-left: 5px solid #e49a52; }
.kpi-indigo { border-left: 5px solid #5c63a8; }

.kpi-label {
    color: #70727d;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}

.kpi-value {
    color: #35245f;
    font-size: 22px;
    font-weight: 800;
    margin-top: 4px;
}

/* Performance cards */
.performance-card {
    background: rgba(255,255,255,0.97);
    border: 1px solid #e2dced;
    border-radius: 13px;
    min-height: 88px;
    padding: 12px 16px;
    box-shadow: 0 4px 14px rgba(53,36,95,0.07);
}

.performance-label {
    color: #70727d;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
}

.performance-value {
    color: #35245f;
    font-size: 24px;
    font-weight: 800;
    margin-top: 4px;
}

.performance-note {
    color: #81858c;
    font-size: 10px;
}

/* Chart title */
.chart-title {
    color: #35245f;
    background: rgba(255,255,255,0.92);
    border-left: 4px solid #6f55a5;
    border-radius: 7px 7px 0 0;
    padding: 6px 9px;
    font-size: 11px;
    font-weight: 800;
    margin-top: 4px;
}

/* Prediction card */
.prediction-card {
    background: linear-gradient(135deg,#f1ebfa 0%,#e9f7f4 100%);
    border: 1px solid #ddd3ee;
    border-radius: 17px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 7px 20px rgba(53,36,95,0.10);
}

.prediction-label {
    color: #686675;
    font-size: 14px;
    font-weight: 600;
}

.prediction-value {
    color: #35245f;
    font-size: 36px;
    font-weight: 800;
}

/* Inputs */
div[data-baseweb="select"],
div[data-baseweb="input"] {
    border-radius: 8px;
}

.stButton > button {
    background: linear-gradient(135deg,#5b438e,#26756f);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

/* Tables */
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_csv("House Price Prediction Dataset.csv")


@st.cache_resource
def load_model():
    model = joblib.load("house_price_model_compressed.pkl")
    location_encoder = joblib.load("location_encoder.pkl")
    condition_encoder = joblib.load("condition_encoder.pkl")
    garage_encoder = joblib.load("garage_encoder.pkl")

    return (
        model,
        location_encoder,
        condition_encoder,
        garage_encoder
    )


df = load_data()

model, le_location, le_condition, le_garage = load_model()


# ============================================================
# SIDEBAR MENU
# ============================================================

st.sidebar.title("Dashboard Menu")

page = st.sidebar.radio(
    "Select Page",
    [
        "Dashboard",
        "Dataset",
        "Missing Values",
        "Duplicate Values",
        "Data Cleaning",
        "Label Encoding",
        "EDA & Statistics",
        "Visualizations",
        "Correlation",
        "Feature Importance",
        "House Price Prediction",
        "Download Dataset"
    ]
)


# ============================================================
# DATA CLEANING
# ============================================================

clean_df = df.copy()

if "Id" in clean_df.columns:
    clean_df = clean_df.drop("Id", axis=1)

clean_df["House_Age"] = 2026 - clean_df["YearBuilt"]

numerical_columns = [
    "Area",
    "Bedrooms",
    "Bathrooms",
    "Floors",
    "YearBuilt",
    "Price"
]

for column in numerical_columns:
    if column in clean_df.columns:
        clean_df[column] = clean_df[column].fillna(
            clean_df[column].mean()
        )

categorical_columns = [
    "Location",
    "Condition",
    "Garage"
]

for column in categorical_columns:
    if column in clean_df.columns:
        clean_df[column] = clean_df[column].fillna(
            clean_df[column].mode()[0]
        )

clean_df = clean_df.drop_duplicates()


# ============================================================
# ENCODING
# ============================================================

encoded_df = clean_df.copy()

encoded_df["Location"] = le_location.transform(
    encoded_df["Location"]
)

encoded_df["Condition"] = le_condition.transform(
    encoded_df["Condition"]
)

encoded_df["Garage"] = le_garage.transform(
    encoded_df["Garage"]
)


# ============================================================
# MODEL EVALUATION
# ============================================================

X = encoded_df.drop("Price", axis=1)
y = encoded_df["Price"]

X_train_eval, X_test_eval, y_train_eval, y_test_eval = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

evaluation_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

evaluation_model.fit(
    X_train_eval,
    y_train_eval
)

test_predictions = evaluation_model.predict(X_test_eval)

mae = mean_absolute_error(
    y_test_eval,
    test_predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test_eval,
        test_predictions
    )
)

r2 = r2_score(
    y_test_eval,
    test_predictions
)


# ============================================================
# HELPER FOR COMPACT CHARTS
# ============================================================

def style_chart(ax, title=None):
    ax.set_facecolor("#FFFFFF")
    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.15
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if title:
        ax.set_title(
            title,
            fontsize=10,
            fontweight="bold",
            color="#35245f"
        )

    ax.tick_params(
        labelsize=8
    )

    plt.tight_layout()


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown("""
    <div class="dashboard-header">
        <h1>🏠 House Price Analytics Dashboard</h1>
        <p>
            Interactive Data Science Dashboard
            • Random Forest Regression
        </p>
    </div>
    """, unsafe_allow_html=True)


    # ========================================================
    # FILTERS
    # ========================================================

    st.markdown(
        '<div class="section-heading">Dashboard Filters</div>',
        unsafe_allow_html=True
    )

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        locations = ["All"] + sorted(
            clean_df["Location"].astype(str).unique().tolist()
        )

        selected_location = st.selectbox(
            "Location",
            locations,
            key="dashboard_location"
        )

    with f2:
        bedrooms_list = ["All"] + sorted(
            clean_df["Bedrooms"].dropna().unique().tolist()
        )

        selected_bedrooms = st.selectbox(
            "Bedrooms",
            bedrooms_list,
            key="dashboard_bedrooms"
        )

    with f3:
        conditions = ["All"] + sorted(
            clean_df["Condition"].astype(str).unique().tolist()
        )

        selected_condition = st.selectbox(
            "Condition",
            conditions,
            key="dashboard_condition"
        )

    with f4:
        garages = ["All"] + sorted(
            clean_df["Garage"].astype(str).unique().tolist()
        )

        selected_garage = st.selectbox(
            "Garage",
            garages,
            key="dashboard_garage"
        )


    f5, f6 = st.columns(2)

    with f5:
        min_area = float(clean_df["Area"].min())
        max_area = float(clean_df["Area"].max())

        area_range = st.slider(
            "Area Range",
            min_value=min_area,
            max_value=max_area,
            value=(min_area, max_area),
            step=50.0,
            key="dashboard_area"
        )

    with f6:
        min_year = int(clean_df["YearBuilt"].min())
        max_year = int(clean_df["YearBuilt"].max())

        year_range = st.slider(
            "Year Built",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            key="dashboard_year"
        )


    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered = clean_df.copy()

    if selected_location != "All":
        filtered = filtered[
            filtered["Location"].astype(str)
            == str(selected_location)
        ]

    if selected_bedrooms != "All":
        filtered = filtered[
            filtered["Bedrooms"] == selected_bedrooms
        ]

    if selected_condition != "All":
        filtered = filtered[
            filtered["Condition"].astype(str)
            == str(selected_condition)
        ]

    if selected_garage != "All":
        filtered = filtered[
            filtered["Garage"].astype(str)
            == str(selected_garage)
        ]

    filtered = filtered[
        (filtered["Area"] >= area_range[0])
        &
        (filtered["Area"] <= area_range[1])
    ]

    filtered = filtered[
        (filtered["YearBuilt"] >= year_range[0])
        &
        (filtered["YearBuilt"] <= year_range[1])
    ]


    # ========================================================
    # KPI CARDS
    # ========================================================

    st.markdown(
        '<div class="section-heading">Key Performance Indicators</div>',
        unsafe_allow_html=True
    )

    if len(filtered) > 0:

        total_houses = len(filtered)
        average_price = filtered["Price"].mean()
        average_area = filtered["Area"].mean()
        average_bedrooms = filtered["Bedrooms"].mean()

    else:

        total_houses = 0
        average_price = 0
        average_area = 0
        average_bedrooms = 0


    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card kpi-purple">
            <div class="kpi-label">Total Houses</div>
            <div class="kpi-value">{total_houses:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card kpi-teal">
            <div class="kpi-label">Average Price</div>
            <div class="kpi-value">₹ {average_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card kpi-orange">
            <div class="kpi-label">Average Area</div>
            <div class="kpi-value">{average_area:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card kpi-indigo">
            <div class="kpi-label">Average Bedrooms</div>
            <div class="kpi-value">{average_bedrooms:.1f}</div>
        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # MODEL PERFORMANCE
    # ========================================================

    st.markdown(
        '<div class="section-heading">Model Performance</div>',
        unsafe_allow_html=True
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="performance-card">
            <div class="performance-label">R² Score</div>
            <div class="performance-value">{r2:.3f}</div>
            <div class="performance-note">Goodness of fit</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="performance-card">
            <div class="performance-label">MAE</div>
            <div class="performance-value">₹ {mae:,.0f}</div>
            <div class="performance-note">Mean Absolute Error</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="performance-card">
            <div class="performance-label">RMSE</div>
            <div class="performance-value">₹ {rmse:,.0f}</div>
            <div class="performance-note">Root Mean Squared Error</div>
        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # CHARTS
    # ========================================================

    st.markdown(
        '<div class="section-heading">House Price Analysis</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)


    # --------------------------------------------------------
    # PRICE BY LOCATION
    # --------------------------------------------------------

    with c1:

        st.markdown(
            '<div class="chart-title">Average Price by Location</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(5, 2.4))
        fig.patch.set_facecolor("#FFFFFF")

        if len(filtered) > 0:

            location_price = (
                filtered
                .groupby("Location")["Price"]
                .mean()
                .sort_values(ascending=False)
            )

            ax.bar(
                location_price.index.astype(str),
                location_price.values,
                color="#6f55a5"
            )

        style_chart(ax)

        ax.tick_params(
            axis="x",
            rotation=35
        )

        ax.set_ylabel("Price", fontsize=8)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    # --------------------------------------------------------
    # PRICE BY BEDROOMS
    # --------------------------------------------------------

    with c2:

        st.markdown(
            '<div class="chart-title">Average Price by Bedrooms</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(5, 2.4))
        fig.patch.set_facecolor("#FFFFFF")

        if len(filtered) > 0:

            bedroom_price = (
                filtered
                .groupby("Bedrooms")["Price"]
                .mean()
                .sort_index()
            )

            ax.bar(
                bedroom_price.index.astype(str),
                bedroom_price.values,
                color="#2d8c84"
            )

        style_chart(ax)

        ax.set_xlabel("Bedrooms", fontsize=8)
        ax.set_ylabel("Price", fontsize=8)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    # --------------------------------------------------------
    # CONDITION DISTRIBUTION
    # --------------------------------------------------------

    with c3:

        st.markdown(
            '<div class="chart-title">House Condition</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(5, 2.4))
        fig.patch.set_facecolor("#FFFFFF")

        if len(filtered) > 0:

            condition_counts = (
                filtered["Condition"]
                .value_counts()
            )

            ax.pie(
                condition_counts.values,
                labels=condition_counts.index,
                autopct="%1.0f%%",
                startangle=90,
                wedgeprops={"width": 0.42}
            )

        ax.set_aspect("equal")

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    c4, c5, c6 = st.columns(3)


    # --------------------------------------------------------
    # AREA VS PRICE
    # --------------------------------------------------------

    with c4:

        st.markdown(
            '<div class="chart-title">Area vs House Price</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(5, 2.4))
        fig.patch.set_facecolor("#FFFFFF")

        if len(filtered) > 0:

            ax.scatter(
                filtered["Area"],
                filtered["Price"],
                s=18,
                alpha=0.65,
                color="#e49a52"
            )

        style_chart(ax)

        ax.set_xlabel("Area", fontsize=8)
        ax.set_ylabel("Price", fontsize=8)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    # --------------------------------------------------------
    # PRICE DISTRIBUTION
    # --------------------------------------------------------

    with c5:

        st.markdown(
            '<div class="chart-title">House Price Distribution</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(5, 2.4))
        fig.patch.set_facecolor("#FFFFFF")

        if len(filtered) > 0:

            ax.hist(
                filtered["Price"],
                bins=15,
                color="#5c63a8",
                edgecolor="white"
            )

        style_chart(ax)

        ax.set_xlabel("Price", fontsize=8)
        ax.set_ylabel("Houses", fontsize=8)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    # --------------------------------------------------------
    # GARAGE DISTRIBUTION
    # --------------------------------------------------------

    with c6:

        st.markdown(
            '<div class="chart-title">Garage Distribution</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(5, 2.4))
        fig.patch.set_facecolor("#FFFFFF")

        if len(filtered) > 0:

            garage_counts = (
                filtered["Garage"]
                .value_counts()
            )

            ax.bar(
                garage_counts.index.astype(str),
                garage_counts.values,
                color="#3d9b78"
            )

        style_chart(ax)

        ax.set_xlabel("Garage", fontsize=8)
        ax.set_ylabel("Houses", fontsize=8)

        ax.tick_params(
            axis="x",
            rotation=30
        )

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    # ========================================================
    # MODEL ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section-heading">Model Analysis</div>',
        unsafe_allow_html=True
    )

    a1, a2 = st.columns(2)


    # --------------------------------------------------------
    # FEATURE IMPORTANCE
    # --------------------------------------------------------

    with a1:

        st.markdown(
            '<div class="chart-title">Feature Importance</div>',
            unsafe_allow_html=True
        )

        feature_df = pd.DataFrame({
            "Feature": X.columns,
            "Importance": evaluation_model.feature_importances_
        })

        feature_df = feature_df.sort_values(
            "Importance",
            ascending=True
        )

        fig, ax = plt.subplots(figsize=(7, 3))
        fig.patch.set_facecolor("#FFFFFF")

        ax.barh(
            feature_df["Feature"],
            feature_df["Importance"],
            color="#6f55a5"
        )

        style_chart(ax)

        ax.set_xlabel("Importance", fontsize=8)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    # --------------------------------------------------------
    # ACTUAL VS PREDICTED
    # --------------------------------------------------------

    with a2:

        st.markdown(
            '<div class="chart-title">Actual vs Predicted Price</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(figsize=(7, 3))
        fig.patch.set_facecolor("#FFFFFF")

        ax.scatter(
            y_test_eval,
            test_predictions,
            s=18,
            alpha=0.65,
            color="#26756f"
        )

        minimum = min(
            y_test_eval.min(),
            test_predictions.min()
        )

        maximum = max(
            y_test_eval.max(),
            test_predictions.max()
        )

        ax.plot(
            [minimum, maximum],
            [minimum, maximum],
            linestyle="--",
            color="#e49a52",
            linewidth=2
        )

        style_chart(ax)

        ax.set_xlabel("Actual Price", fontsize=8)
        ax.set_ylabel("Predicted Price", fontsize=8)

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)


    # ========================================================
    # FILTER STATUS
    # ========================================================

    st.markdown(
        f"""
        <div style="
            text-align:right;
            color:#747982;
            font-size:10px;
            margin-top:4px;
        ">
            Showing <b>{len(filtered):,}</b> houses based on selected filters.
            KPI cards and analytical charts update automatically.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DATASET
# ============================================================

elif page == "Dataset":

    st.title("House Dataset")

    st.write("Original Dataset")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.write(
        "Dataset Shape:",
        df.shape
    )


# ============================================================
# MISSING VALUES
# ============================================================

elif page == "Missing Values":

    st.title("Missing Values Analysis")

    missing = df.isnull().sum()

    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values
    })

    missing_df = missing_df[
        missing_df["Missing Values"] > 0
    ]

    if len(missing_df) == 0:

        st.success("No missing values found.")

    else:

        st.dataframe(
            missing_df,
            use_container_width=True
        )


# ============================================================
# DUPLICATE VALUES
# ============================================================

elif page == "Duplicate Values":

    st.title("Duplicate Values")

    duplicate_count = df.duplicated().sum()

    st.metric(
        "Total Duplicate Rows",
        duplicate_count
    )

    if duplicate_count > 0:

        st.dataframe(
            df[df.duplicated()],
            use_container_width=True
        )

    else:

        st.success("No duplicate values found.")


# ============================================================
# DATA CLEANING
# ============================================================

elif page == "Data Cleaning":

    st.title("Data Cleaning")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Original Rows",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Cleaned Rows",
            clean_df.shape[0]
        )

    st.subheader("Cleaned Dataset")

    st.dataframe(
        clean_df,
        use_container_width=True
    )


# ============================================================
# LABEL ENCODING
# ============================================================

elif page == "Label Encoding":

    st.title("Label Encoding")

    st.write(
        "Categorical columns are converted into numerical values."
    )

    st.subheader("Encoded Dataset")

    st.dataframe(
        encoded_df,
        use_container_width=True
    )

    st.subheader("Location Encoding")

    location_mapping = pd.DataFrame({
        "Location": le_location.classes_,
        "Encoded Value": range(
            len(le_location.classes_)
        )
    })

    st.dataframe(
        location_mapping,
        use_container_width=True
    )

    st.subheader("Condition Encoding")

    condition_mapping = pd.DataFrame({
        "Condition": le_condition.classes_,
        "Encoded Value": range(
            len(le_condition.classes_)
        )
    })

    st.dataframe(
        condition_mapping,
        use_container_width=True
    )

    st.subheader("Garage Encoding")

    garage_mapping = pd.DataFrame({
        "Garage": le_garage.classes_,
        "Encoded Value": range(
            len(le_garage.classes_)
        )
    })

    st.dataframe(
        garage_mapping,
        use_container_width=True
    )


# ============================================================
# EDA & STATISTICS
# ============================================================

elif page == "EDA & Statistics":

    st.title("EDA & Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Rows", clean_df.shape[0])

    with c2:
        st.metric("Columns", clean_df.shape[1])

    with c3:
        st.metric(
            "Numerical Columns",
            len(
                clean_df.select_dtypes(
                    include=np.number
                ).columns
            )
        )

    with c4:
        st.metric(
            "Categorical Columns",
            len(
                clean_df.select_dtypes(
                    exclude=np.number
                ).columns
            )
        )

    st.subheader("Column Names")

    st.write(
        list(clean_df.columns)
    )

    st.subheader("Data Types")

    dtype_df = pd.DataFrame({
        "Column": clean_df.columns,
        "Data Type": clean_df.dtypes.astype(str)
    })

    st.dataframe(
        dtype_df,
        use_container_width=True
    )

    st.subheader("Statistical Summary")

    st.dataframe(
        clean_df.describe(),
        use_container_width=True
    )


# ============================================================
# VISUALIZATIONS
# ============================================================

elif page == "Visualizations":

    st.title("House Price Visualizations")

    chart_type = st.selectbox(
        "Select Visualization",
        [
            "House Price Histogram",
            "Bedrooms Bar Chart",
            "Bedrooms vs Price",
            "Area vs Price"
        ]
    )

    if chart_type == "House Price Histogram":

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.hist(
            clean_df["Price"],
            bins=20,
            color="#008C95",
            edgecolor="white"
        )

        ax.set_xlabel("House Price")
        ax.set_ylabel("Number of Houses")
        ax.set_title("House Price Distribution")

        st.pyplot(fig)
        plt.close(fig)

    elif chart_type == "Bedrooms Bar Chart":

        bedroom_count = (
            clean_df["Bedrooms"]
            .value_counts()
            .sort_index()
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.bar(
            bedroom_count.index,
            bedroom_count.values,
            color="#4C78A8"
        )

        ax.set_xlabel("Number of Bedrooms")
        ax.set_ylabel("Number of Houses")
        ax.set_title("Number of Houses by Bedrooms")

        st.pyplot(fig)
        plt.close(fig)

    elif chart_type == "Bedrooms vs Price":

        bedroom_price = (
            clean_df
            .groupby("Bedrooms")["Price"]
            .mean()
        )

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.bar(
            bedroom_price.index,
            bedroom_price.values,
            color="#7A5195"
        )

        ax.set_xlabel("Bedrooms")
        ax.set_ylabel("House Price")
        ax.set_title("Bedrooms vs House Price")

        st.pyplot(fig)
        plt.close(fig)

    elif chart_type == "Area vs Price":

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.scatter(
            clean_df["Area"],
            clean_df["Price"],
            color="#E45756",
            s=50,
            alpha=0.7
        )

        ax.set_xlabel("Area")
        ax.set_ylabel("House Price")
        ax.set_title("Area vs House Price")

        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# CORRELATION
# ============================================================

elif page == "Correlation":

    st.title("Correlation Analysis")

    correlation = encoded_df.corr()

    st.subheader("Correlation with Price")

    price_correlation = (
        correlation["Price"]
        .sort_values(ascending=False)
    )

    st.dataframe(
        price_correlation,
        use_container_width=True
    )

    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots(figsize=(10, 6))

    im = ax.imshow(
        correlation,
        cmap="YlGnBu",
        aspect="auto"
    )

    ax.set_xticks(
        range(len(correlation.columns))
    )

    ax.set_xticklabels(
        correlation.columns,
        rotation=45,
        ha="right"
    )

    ax.set_yticks(
        range(len(correlation.index))
    )

    ax.set_yticklabels(
        correlation.index
    )

    for i in range(len(correlation.index)):
        for j in range(len(correlation.columns)):

            ax.text(
                j,
                i,
                f"{correlation.iloc[i, j]:.2f}",
                ha="center",
                va="center",
                fontsize=8
            )

    fig.colorbar(
        im,
        ax=ax,
        fraction=0.046,
        pad=0.04
    )

    ax.set_title(
        "House Price Correlation Heatmap"
    )

    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

elif page == "Feature Importance":

    st.title("Feature Importance")

    feature_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    feature_model.fit(
        X,
        y
    )

    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": feature_model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    )

    st.subheader(
        "Important Features for House Price"
    )

    st.dataframe(
        importance_df,
        use_container_width=True
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.barh(
        importance_df["Feature"],
        importance_df["Importance"],
        color="#2A9D8F"
    )

    ax.invert_yaxis()

    ax.set_xlabel("Importance")
    ax.set_title(
        "Feature Importance for House Price"
    )

    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# HOUSE PRICE PREDICTION
# ============================================================

elif page == "House Price Prediction":

    st.title("House Price Prediction")

    st.write(
        "Enter house details to predict the estimated price."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        area = st.number_input(
            "Area",
            min_value=100.0,
            value=1500.0,
            step=50.0
        )

        bedrooms = st.number_input(
            "Bedrooms",
            min_value=1.0,
            value=3.0,
            step=1.0
        )

        bathrooms = st.number_input(
            "Bathrooms",
            min_value=1.0,
            value=2.0,
            step=1.0
        )

        floors = st.number_input(
            "Floors",
            min_value=1.0,
            value=1.0,
            step=1.0
        )

    with col2:

        year_built = st.number_input(
            "Year Built",
            min_value=1900.0,
            max_value=2026.0,
            value=2015.0,
            step=1.0
        )

        location = st.selectbox(
            "Location",
            le_location.classes_
        )

        condition = st.selectbox(
            "Condition",
            le_condition.classes_
        )

        garage = st.selectbox(
            "Garage",
            le_garage.classes_
        )

    if st.button(
        "Predict House Price",
        use_container_width=True
    ):

        location_encoded = le_location.transform(
            [location]
        )[0]

        condition_encoded = le_condition.transform(
            [condition]
        )[0]

        garage_encoded = le_garage.transform(
            [garage]
        )[0]

        house_age = 2026 - year_built

        input_data = pd.DataFrame({
            "Area": [area],
            "Bedrooms": [bedrooms],
            "Bathrooms": [bathrooms],
            "Floors": [floors],
            "YearBuilt": [year_built],
            "Location": [location_encoded],
            "Condition": [condition_encoded],
            "Garage": [garage_encoded],
            "House_Age": [house_age]
        })

        input_data = input_data[
            model.feature_names_in_
        ]

        prediction = model.predict(
            input_data
        )[0]

        st.success(
            "House Price Prediction Completed!"
        )

        st.markdown(
            f"""
            <div class="prediction-card">
                <div class="prediction-label">
                    Estimated House Price
                </div>
                <div class="prediction-value">
                    ₹ {prediction:,.2f}
                </div>
                <div>
                    Random Forest Regression
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader(
            "Model Evaluation Summary"
        )

        p1, p2, p3 = st.columns(3)

        with p1:
            st.metric(
                "R² Score",
                f"{r2:.3f}"
            )

        with p2:
            st.metric(
                "MAE",
                f"₹ {mae:,.0f}"
            )

        with p3:
            st.metric(
                "RMSE",
                f"₹ {rmse:,.0f}"
            )


# ============================================================
# DOWNLOAD DATASET
# ============================================================

elif page == "Download Dataset":

    st.title("Download Dataset")

    csv = clean_df.to_csv(
        index=False
    )

    st.download_button(
        label="Download Clean Dataset",
        data=csv,
        file_name="clean_house_price_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.success(
        "Cleaned dataset is ready for download."
    )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "House Price Prediction"
)

st.sidebar.caption(
    "Random Forest Regression"
)

st.markdown(
    """
    <div style="
        text-align:center;
        padding:12px 0 4px 0;
        color:#747982;
        font-size:10px;
    ">
        House Price Prediction | Data Science Project
    </div>
    """,
    unsafe_allow_html=True
)
