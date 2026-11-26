import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import date
import joblib
import pandas as pd
model_data = joblib.load("healthcare_model.pkl")
model = model_data["model"]
feature_columns = model_data["feature_columns"]
# Load trained ML model
model_data = joblib.load("healthcare_model.pkl")

model = model_data["model"]
feature_columns = model_data["feature_columns"]

def render_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = True
    return True

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="MediCare AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
[data-testid="stSidebar"] {
    background-color: #102a43;
}
[data-testid="stSidebar"] * {
    color: white;
}
h1 {
    color: #123b5d;
    font-weight: 700;
}
[data-testid="stMetric"] {
    background-color: white;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #e1e8f0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.05);
}
.stButton > button {
    background-color: #087e8b;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 20px;
}
h2, h3 {
    color: #176b87;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# AUTHENTICATION
# =====================================

if not render_auth():
    st.stop()

# =====================================
# DATABASE
# =====================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "medicare.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            symptoms TEXT,
            date TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient TEXT,
            doctor TEXT,
            appointment_date TEXT
        )
    """)

    conn.commit()
    conn.close()

def get_patients():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    return df

def get_appointments():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM appointments", conn)
    conn.close()
    return df

create_tables()

# =====================================
# DATASET
# =====================================

def get_dataset():

    data_folder = BASE_DIR.parent / "data"
    dataset_file = data_folder / "Cleaned_Dataset.csv"

    if not dataset_file.exists():
        st.error("Dataset file not found!")
        return None

    try:
        df = pd.read_csv(dataset_file)
        return df

    except Exception as e:
        st.error(f"Dataset loading error: {e}")
        return None

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🏥 MediCare AI")
st.sidebar.caption("Healthcare Recommendation & Analytics")

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Home Dashboard",
        "Dataset Overview",
        "Disease Analytics",
        "Disease Prediction",
        "Medicine",
        "Patient Registration",
        "Symptom Analysis",
        "AI Prediction",
        "Doctor Recommendation",
        "Appointment",
        "Patient History",
        "Health Analytics",
        "Admin"
    ],
    key="main_navigation"
)

st.sidebar.divider()
st.sidebar.success("Welcome to MediCare AI")

if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

# =====================================
# 1. HOME DASHBOARD
# =====================================

if page == "Home Dashboard":
    st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

    st.title("🏥 MediCare AI")
    st.caption("Healthcare Recommendation & Analytics Platform")

    st.markdown(
        "Welcome to **MediCare AI** — a healthcare analytics "
        "and patient management demonstration platform."
    )

    patients = get_patients()
    appointments = get_appointments()
    df = get_dataset()

    # =====================================
    # DASHBOARD METRICS
    # =====================================

    total_patients = len(patients)
    total_appointments = len(appointments)

    total_diseases = (
        df["disease"].nunique()
        if df is not None and "disease" in df.columns
        else 0
    )

    total_departments = (
        df["department"].nunique()
        if df is not None and "department" in df.columns
        else 0
    )

    st.subheader("📊 Dashboard Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("👥 Total Patients", f"{total_patients:,}")
    c2.metric("📅 Appointments", f"{total_appointments:,}")
    c3.metric("🦠 Diseases", f"{total_diseases:,}")
    c4.metric("🏥 Departments", f"{total_departments:,}")

    st.divider()
    # PATIENT DATA PREVIEW

    st.subheader("📋 Recent Patient Records")

    if not patients.empty:

        st.dataframe(
            patients.tail(10),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No patient records available yet.")

    # =====================================
    # QUICK ACCESS
    # =====================================

    st.subheader("⚡ Platform Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.info(
            "**📝 Patient Registration**\n\n"
            "Register and manage patient details."
        )

        st.info(
            "**🩺 Disease Analytics**\n\n"
            "Explore disease-related dataset insights."
        )

    with col2:
        st.info(
            "**📅 Appointment Management**\n\n"
            "Manage patient appointment records."
        )

        st.info(
            "**🤖 AI Prediction**\n\n"
            "Explore educational prediction features."
        )

    st.divider()
    chart1, chart2 = st.columns(2)
# =====================================
    # DISEASE DISTRIBUTION CHART
    # =====================================

    st.subheader("🦠 Disease Distribution Analysis")

    if df is not None and "disease" in df.columns:

        disease_counts = df["disease"].value_counts()

        st.bar_chart(
            disease_counts,
            height=350
        )

        st.caption(
            "This chart displays the distribution of diseases in the sample dataset."
        )

    else:

        st.warning("Disease column not available.")
        # =====================================
    # DEPARTMENT DISTRIBUTION
    # =====================================

    st.subheader("🏥 Department Distribution")

    if df is not None and "department" in df.columns:

        department_counts = df["department"].value_counts()

        st.bar_chart(
            department_counts,
            height=350
        )

        st.caption(
            "Department-wise distribution from the sample dataset."
        )

    else:

        st.warning("Department column not available.")
        # =====================================
    # AGE GROUP ANALYSIS
    # =====================================

    st.subheader("👥 Patient Age Group Analysis")

    if df is not None and "age" in df.columns:

        age_data = df.copy()

        age_data["age"] = pd.to_numeric(
            age_data["age"],
            errors="coerce"
        )

        age_data["Age Group"] = pd.cut(
            age_data["age"],
            bins=[0, 18, 35, 50, 65, 100],
            labels=[
                "0-18",
                "19-35",
                "36-50",
                "51-65",
                "65+"
            ]
        )

        age_counts = age_data["Age Group"].value_counts(
            sort=False
        )

        st.bar_chart(
            age_counts,
            height=350
        )

        st.caption(
            "Sample patient records grouped by age range."
        )

    else:

        st.warning("Age column not available.")
        # =====================================
    # GENDER DISTRIBUTION
    # =====================================

    st.subheader("👥 Gender Distribution")

    if df is not None and "gender" in df.columns:

        gender_counts = df["gender"].astype(str).value_counts()

        st.bar_chart(
            gender_counts,
            height=350
        )

        st.caption(
            "Gender-wise distribution in the sample dataset."
        )

    else:

        st.warning("Gender column not available.")
        # =====================================
    # PATIENT RISK LEVEL ANALYSIS
    # =====================================

    st.subheader("⚠️ Patient Risk Level Analysis")

    if df is not None and "risk_level" in df.columns:

        risk_counts = df["risk_level"].value_counts()

        st.bar_chart(
            risk_counts,
            height=350
        )

        st.caption(
            "Risk level distribution from the sample dataset."
        )

    else:

        st.warning("Risk level column not available.")
        # =====================================
    # BLOOD PRESSURE ANALYSIS
    # =====================================

    st.subheader("🩺 Blood Pressure Distribution")

    if df is not None and "blood_pressure" in df.columns:

        bp_counts = df["blood_pressure"].astype(str).value_counts()

        st.bar_chart(
            bp_counts,
            height=350
        )

        st.caption(
            "Blood pressure category distribution in the sample dataset."
        )

    else:

        st.warning("Blood pressure column not available.")
        # =====================================
    # CHOLESTEROL ANALYSIS
    # =====================================

    st.subheader("🧪 Cholesterol Level Analysis")

    if df is not None and "cholesterol_level" in df.columns:

        cholesterol_data = pd.to_numeric(
            df["cholesterol_level"],
            errors="coerce"
        ).dropna()

        st.bar_chart(
            cholesterol_data.value_counts().sort_index(),
            height=350
        )

        st.caption(
            "Cholesterol value distribution in the sample dataset."
        )

    else:

        st.warning("Cholesterol column not available.")   
      # =====================================
    # PATIENT STATISTICS SUMMARY
    # =====================================

    st.subheader("📊 Patient Statistics Summary")

    if df is not None and "age" in df.columns:

        age_values = pd.to_numeric(
            df["age"],
            errors="coerce"
        ).dropna()

        if not age_values.empty:

            col1, col2, col3 = st.columns(3)

            col1.metric("Average Age", round(age_values.mean(), 1))
            col2.metric("Minimum Age", int(age_values.min()))
            col3.metric("Maximum Age", int(age_values.max()))

    # =====================================
    # PATIENT SEARCH
    # =====================================

    st.subheader("🔎 Patient Name Search")

    if df is not None and "patient_name" in df.columns:

        search_name = st.text_input(
            "Enter Patient Name",
            key="home_patient_search"
        )

        if search_name.strip():

            search_result = df[
                df["patient_name"].astype(str).str.contains(
                    search_name,
                    case=False,
                    na=False
                )
            ]

            if not search_result.empty:

                st.success(f"Found {len(search_result)} records")

                st.dataframe(
                    search_result,
                    use_container_width=True
                )

            else:
                st.warning("Patient not found.")

    else:
        st.info("Dataset patient_name column not available.")
            # =====================================
    # =====================================
        # PATIENT GENDER SUMMARY
        # =====================================

        if df is not None and "gender" in df.columns:

            st.subheader("👥 Gender Summary")

            gender_counts = df["gender"].value_counts()

            st.bar_chart(gender_counts)


    # =====================================
    # DATASET INFORMATION
    # =====================================

    st.subheader("📁 Dataset Information")

    if df is not None:

        d1, d2, d3 = st.columns(3)

        d1.metric("Dataset Records", f"{len(df):,}")
        d2.metric("Dataset Columns", f"{len(df.columns):,}")
        d3.metric(
            "Missing Values",
            f"{int(df.isnull().sum().sum()):,}"
        )
# =====================================
        # DOWNLOAD DATASET
        # =====================================

        st.subheader("📥 Download Healthcare Dataset")

        st.download_button(
            label="Download Dataset CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="medicare_dataset.csv",
            mime="text/csv"
        )
    else:

        st.warning("Dataset unavailable.")

 # =====================================
# 2. DATASET OVERVIEW
# =====================================

elif page == "Dataset Overview":

    st.title("📁 Healthcare Dataset Overview")
    st.caption("Patient data analysis, filtering and downloadable reports")

    df = get_dataset()

    if df is not None:

        st.success("Dataset Loaded Successfully!")

        # KPI CARDS
        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Records", f"{len(df):,}")
        c2.metric("Total Columns", len(df.columns))
        c3.metric("Missing Values", int(df.isnull().sum().sum()))
        c4.metric("Duplicate Records", int(df.duplicated().sum()))

        st.divider()

        # PATIENT ID CHECK
        if "patient_id" in df.columns:
            st.success("Patient ID Available")
        else:
            st.warning("Patient ID column not found")

        # FILTERS
        st.subheader("🔍 Patient Filters")

        filtered_df = df.copy()

        f1, f2 = st.columns(2)

        # NAME FILTER
        with f1:
            if "patient_name" in filtered_df.columns:

                name_filter = st.text_input("Search Patient Name")

                if name_filter.strip():

                    filtered_df = filtered_df[
                        filtered_df["patient_name"].astype(str).str.contains(
                            name_filter.strip(),
                            case=False,
                            na=False
                        )
                    ]

        # DEPARTMENT FILTER
        with f2:
            if "department" in filtered_df.columns:

                departments = ["All"] + sorted(
                    filtered_df["department"].dropna().astype(str).unique().tolist()
                )

                selected_department = st.selectbox(
                    "Select Department",
                    departments
                )

                if selected_department != "All":

                    filtered_df = filtered_df[
                        filtered_df["department"].astype(str) == selected_department
                    ]

        # DATE FILTER
        if "visit_date" in filtered_df.columns:

            filtered_df["visit_date"] = pd.to_datetime(
                filtered_df["visit_date"],
                errors="coerce"
            )

            valid_dates = filtered_df["visit_date"].dropna()

            if not valid_dates.empty:

                date_range = st.date_input(
                    "Filter Visit Date Range",
                    value=(valid_dates.min().date(), valid_dates.max().date())
                )

                if isinstance(date_range, tuple) and len(date_range) == 2:

                    start_date, end_date = date_range

                    filtered_df = filtered_df[
                        filtered_df["visit_date"].dt.date.between(
                            start_date,
                            end_date
                        )
                    ]

        st.divider()

        # PATIENT ID SEARCH
        if "patient_id" in filtered_df.columns:

            st.subheader("🆔 Patient ID Search")

            search_id = st.text_input(
                "Enter Patient ID",
                key="patient_id_search"
            )

            if search_id.strip():

                result = filtered_df[
                    filtered_df["patient_id"].astype(str).str.contains(
                        search_id.strip(),
                        case=False,
                        na=False
                    )
                ]

                if not result.empty:

                    st.success("Patient Record Found!")

                    st.dataframe(
                        result,
                        use_container_width=True,
                        hide_index=True
                    )

                else:
                    st.warning("No matching Patient ID found.")

        # FILTERED DATA
        st.subheader("📊 Filtered Dataset")

        st.write(f"Records Found: **{len(filtered_df):,}**")

        st.dataframe(
            filtered_df.head(100),
            use_container_width=True,
            hide_index=True
        )

        # COLUMN INFORMATION
        st.subheader("📋 Column Information")

        info = pd.DataFrame({
            "Column Name": filtered_df.columns,
            "Data Type": filtered_df.dtypes.astype(str).values,
            "Missing Values": filtered_df.isnull().sum().values
        })

        st.dataframe(
            info,
            use_container_width=True,
            hide_index=True
        )

        # STATISTICS
        st.subheader("📈 Statistical Summary")

        st.dataframe(
            filtered_df.describe(include="all").transpose(),
            use_container_width=True
        )

        # DOWNLOAD
        st.subheader("📥 Download Report")

        st.download_button(
            label="Download Filtered Dataset CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="medicare_filtered_dataset.csv",
            mime="text/csv"
        )

    else:

        st.warning("CSV dataset not found.")

        st.info(
            "Place your healthcare CSV file inside the project data folder."
        )

# =====================================
# 3. DISEASE ANALYTICS
# =====================================

elif page == "Disease Analytics":

    st.title("📊 Disease Analytics")

    df = get_dataset()

    if df is not None:

        disease_columns = [
            col for col in df.columns
            if any(
                word in col.lower()
                for word in ["disease", "diagnosis", "condition"]
            )
        ]

        if disease_columns:

            disease_col = st.selectbox(
                "Select Disease Column",
                disease_columns
            )

            counts = (
                df[disease_col]
                .fillna("Unknown")
                .astype(str)
                .value_counts()
            )

            c1, c2 = st.columns(2)

            c1.metric("Total Records", len(df))
            c2.metric("Disease Categories", df[disease_col].nunique())

            st.subheader("Disease Distribution")
            st.bar_chart(counts)

            st.subheader("Disease Records")

            st.dataframe(
                counts.rename_axis("Disease").reset_index(name="Count"),
                use_container_width=True,
                hide_index=True
            )

        else:
            st.warning("Disease column not detected.")
            st.write("Available columns:", list(df.columns))

    else:
        st.info("Please add a healthcare CSV file inside the data folder.")

    st.divider()
    st.subheader("Registered Patient Analytics")

    patients = get_patients()

    if not patients.empty:

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Patients", len(patients))
        c2.metric("Average Age", round(patients["age"].mean(), 1))
        c3.metric("Gender Categories", patients["gender"].nunique())

        symptoms = (
            patients["symptoms"]
            .fillna("")
            .str.split(",")
            .explode()
            .str.strip()
        )

        symptoms = symptoms[symptoms != ""]

        if not symptoms.empty:
            st.subheader("Patient Symptom Distribution")
            st.bar_chart(symptoms.value_counts())

    else:
        st.info("No registered patient data.")
# =====================================
# 4. DISEASE PREDICTION
# =====================================

elif page == "Disease Prediction":

    st.title("🤖 AI Disease Prediction")

    st.info(
        "Educational ML prediction only. "
        "This is not a medical diagnosis."
    )

    age = st.number_input(
        "Patient Age", 1, 120, 25, key="disease_age"
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        key="disease_gender"
    )

    bp = st.text_input(
        "Blood Pressure Category",
        value="Normal"
    )

    cholesterol = st.text_input(
        "Cholesterol Level",
        value="Normal"
    )

    st.subheader("Select Symptoms")

    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    fatigue = st.checkbox("Fatigue")
    breathing = st.checkbox("Difficulty Breathing")

    if st.button("Predict Disease"):

        if breathing:
            st.warning(
                "Breathing difficulty can be serious. "
                "Seek urgent medical evaluation if severe."
            )

        patient = pd.DataFrame([{
            "fever": int(fever),
            "cough": int(cough),
            "fatigue": int(fatigue),
            "difficulty_breathing": int(breathing),
            "age": age,
            "gender": gender,
            "blood_pressure": bp,
            "cholesterol_level": cholesterol
        }])

        patient = pd.get_dummies(patient)

        patient = patient.reindex(
            columns=feature_columns,
            fill_value=0
        )

        prediction = model.predict(patient)

        st.subheader("Prediction Result")

        st.success(
            f"Predicted Disease: {prediction[0]}"
        )

        st.warning(
            "This ML result is experimental and "
            "must not be used to diagnose or treat disease."
        )

# =====================================
# 5. MEDICINE
# =====================================

elif page == "Medicine":

    st.title("💊 Medicine Information")

    medicine_data = pd.DataFrame({
        "Medicine": [
            "Paracetamol", "Cetirizine", "ORS",
            "Omeprazole", "Ibuprofen"
        ],
        "Category": [
            "Pain and Fever", "Antihistamine",
            "Oral Rehydration", "Acid Reduction",
            "Pain Relief"
        ],
        "Information": [
            "Used for pain and fever relief.",
            "Used for allergy symptoms.",
            "Helps replace fluids and electrolytes.",
            "Reduces stomach acid.",
            "Used for pain and inflammation."
        ]
    })

    search = st.text_input("Search Medicine")

    if search:
        result = medicine_data[
            medicine_data["Medicine"].str.contains(
                search,
                case=False,
                na=False
            )
        ]
    else:
        result = medicine_data

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    selected = st.selectbox(
        "Select Medicine",
        medicine_data["Medicine"]
    )

    details = medicine_data[
        medicine_data["Medicine"] == selected
    ].iloc[0]

    st.write("Category:", details["Category"])
    st.write("Information:", details["Information"])

    st.warning(
        "Reference information only. Consult a doctor or pharmacist before using medicines."
    )

# =====================================
# 6. PATIENT REGISTRATION
# =====================================

elif page == "Patient Registration":

    st.title("📝 Patient Registration")
    st.caption("Register and store patient information.")

    with st.form("registration_form"):

        name = st.text_input("Patient Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        gender = st.selectbox(
            "Gender",
            ["Select", "Male", "Female", "Other"]
        )

        symptoms = st.text_area("Symptoms")

        submit = st.form_submit_button(
            "📝 Register Patient",
            use_container_width=True
        )

        if submit:

            if not name.strip():
                st.warning("Please enter patient name.")

            elif gender == "Select":
                st.warning("Please select gender.")

            elif not symptoms.strip():
                st.warning("Please enter patient symptoms.")

            else:

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO patients
                    (name, age, gender, symptoms, date)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    name.strip(),
                    age,
                    gender,
                    symptoms.strip(),
                    str(date.today())
                ))

                conn.commit()

                patient_id = cursor.lastrowid

                conn.close()

                st.success("✅ Patient Registered Successfully!")

                st.info(f"Patient ID: {patient_id}")

                st.write("**Patient Name:**", name)
                st.write("**Age:**", age)
                st.write("**Gender:**", gender)
                st.write("**Symptoms:**", symptoms)
                st.write("**Registration Date:**", date.today())

# =====================================
# 7. SYMPTOM ANALYSIS
# =====================================

elif page == "Symptom Analysis":

    st.title("🩺 Symptom Analysis")

    symptoms_list = [
        "Fever", "Cough", "Headache", "Fatigue",
        "Cold", "Body Pain", "Breathing Difficulty",
        "Vomiting", "Stomach Pain"
    ]

    selected = st.multiselect(
        "Select Your Symptoms",
        symptoms_list
    )

    duration = st.selectbox(
        "Symptom Duration",
        ["Today", "2-3 Days", "4-7 Days", "More than a week"]
    )

    if st.button("Analyze Symptoms"):

        if selected:
            st.success("Symptom Assessment Completed!")
            st.write("Selected Symptoms:", selected)
            st.write("Duration:", duration)

            st.info("This tool does not provide a medical diagnosis.")

        else:
            st.warning("Please select symptoms.")

# =====================================
# 8. AI PREDICTION
# =====================================

elif page == "AI Prediction":

    st.title("🤖 AI Health Risk Assessment")

    age = st.number_input(
        "Patient Age", 1, 120, key="prediction_age"
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        key="prediction_gender"
    )

    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    headache = st.checkbox("Headache")
    fatigue = st.checkbox("Fatigue")
    breathing = st.checkbox("Breathing Difficulty")
    body_pain = st.checkbox("Body Pain")

    if st.button("Generate Health Assessment"):

        score = sum([
            fever, cough, headache, fatigue,
            breathing, body_pain
        ])

        st.metric("Selected Symptoms", score)

        if breathing:
            st.error(
                "Breathing difficulty selected. Seek prompt medical evaluation."
            )

        elif score >= 4:
            st.warning(
                "Multiple symptoms selected. Consult a healthcare professional."
            )

        elif score >= 1:
            st.info(
                "Monitor your symptoms and seek medical advice if needed."
            )

        else:
            st.success("No listed symptoms selected.")

        st.caption(
            "Rule-based demonstration, not a trained AI model or diagnosis."
        )

# =====================================
# 9. DOCTOR RECOMMENDATION
# =====================================

elif page == "Doctor Recommendation":

    st.title("Doctor Recommendation")
    st.caption("Choose a health concern to view a suggested department.")

    departments = {
        "General Health": ("Dr. Arun", "General Medicine"),
        "Heart Problem": ("Dr. Kumar", "Cardiology"),
        "Skin Problem": ("Dr. Priya", "Dermatology"),
        "Brain / Nerve Problem": ("Dr. Raj", "Neurology"),
        "Bone / Joint Problem": ("Dr. Suresh", "Orthopedics"),
        "Child Health": ("Dr. Meena", "Pediatrics")
    }

    department = st.selectbox(
        "Select Your Health Concern",
        list(departments.keys())
    )

    doctor, specialization = departments[department]

    st.subheader("Recommended Department")
    st.success(f"Department: {specialization}")
    st.write("Suggested Doctor:", doctor)

    st.info("Demo recommendation only. Please consult a qualified healthcare professional.")

# =====================================
# APPOINTMENT
# =====================================

elif page == "Appointment":

    st.title("📅 Appointment Booking")
    st.caption("Schedule and manage patient appointments.")

    patients = get_patients()

    with st.form("appointment_form"):

        patient_name = st.text_input("Patient Name")

        doctor_name = st.selectbox(
            "Select Doctor",
            [
                "Dr. Arun - General Medicine",
                "Dr. Priya - Cardiology",
                "Dr. Kumar - Neurology",
                "Dr. Meena - Dermatology",
                "Dr. Ravi - Orthopedics"
            ]
        )

        appointment_date = st.date_input(
            "Appointment Date",
            min_value=date.today()
        )

        appointment_time = st.time_input("Appointment Time")

        reason = st.text_area("Appointment Reason")

        submit_appointment = st.form_submit_button(
            "📅 Book Appointment",
            use_container_width=True
        )

        if submit_appointment:

            if not patient_name.strip():
                st.warning("Enter patient name.")

            elif not reason.strip():
                st.warning("Enter appointment reason.")

            else:

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO appointments
                    (patient_name, doctor_name, date, time, reason)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    patient_name.strip(),
                    doctor_name,
                    str(appointment_date),
                    str(appointment_time),
                    reason.strip()
                ))

                conn.commit()
                conn.close()

                st.success("✅ Appointment booked successfully!")

                st.write("**Patient:**", patient_name)
                st.write("**Doctor:**", doctor_name)
                st.write("**Date:**", appointment_date)
                st.write("**Time:**", appointment_time)

# =====================================
# 11. PATIENT HISTORY
# =====================================

elif page == "Patient History":

    st.title("📋 Patient History")
    st.caption("Search and view registered patient records.")

    patients = get_patients()

    if not patients.empty:

        col1, col2 = st.columns(2)

        col1.metric("Total Patient Records", len(patients))

        search = st.text_input("🔎 Search Patient Name")

        if search.strip():

            patients = patients[
                patients["name"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.subheader("Patient Records")

        st.dataframe(
            patients,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 Download Patient History",
            data=patients.to_csv(index=False),
            file_name="patient_history.csv",
            mime="text/csv"
        )

    else:
        st.info("No patient records found.")
        # =====================================
# 12. HEALTH ANALYTICS
# =====================================

elif page == "Health Analytics":

    st.title("📊 Health Analytics")
    st.caption("Patient data statistics and visualization")

    patients = get_patients()

    if not patients.empty:

        col1, col2, col3 = st.columns(3)

        col1.metric("👥 Total Patients", len(patients))

        col2.metric(
            "📊 Average Age",
            round(patients["age"].mean(), 1)
        )

        col3.metric(
            "⚧ Gender Categories",
            patients["gender"].nunique()
        )

        st.divider()

        st.subheader("👥 Gender Distribution")
        st.bar_chart(patients["gender"].value_counts())

        st.divider()

        st.subheader("📈 Age Distribution")
        st.bar_chart(
            patients["age"].value_counts().sort_index()
        )

        st.divider()

        st.subheader("🧑 Age Group Analysis")

        age_groups = pd.cut(
            patients["age"],
            bins=[0, 18, 35, 50, 65, 120],
            labels=["0-18", "19-35", "36-50", "51-65", "65+"]
        )

        st.bar_chart(age_groups.value_counts().sort_index())

    else:
        st.info("Register patients to view analytics.")
        # =====================================
# 13. ADMIN
# =====================================

elif page == "Admin":

    st.title("⚙️ Admin Dashboard")
    st.caption("Patient and appointment records management")

    patients = get_patients()
    appointments = get_appointments()

    # SUMMARY
    col1, col2 = st.columns(2)

    col1.metric("👥 Total Patients", len(patients))
    col2.metric("📅 Total Appointments", len(appointments))

    st.divider()

    # PATIENT RECORDS
    st.subheader("👥 Patient Records")

    if not patients.empty:

        st.dataframe(
            patients,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 Download Patient Data",
            data=patients.to_csv(index=False),
            file_name="patient_records.csv",
            mime="text/csv"
        )

    else:
        st.info("No patient records available.")

    st.divider()
    # =====================================
    # DISEASE ANALYSIS
    # =====================================

    st.divider()
    st.subheader("🦠 Disease Distribution")

    df = get_dataset()

    if df is not None and "disease" in df.columns:

        disease_count = df["disease"].value_counts().head(10)

        st.bar_chart(disease_count)

    else:
        st.info("Disease dataset unavailable.")

    # APPOINTMENT RECORDS
    st.subheader("📅 Appointment Records")

    if not appointments.empty:

        st.dataframe(
            appointments,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 Download Appointment Data",
            data=appointments.to_csv(index=False),
            file_name="appointment_records.csv",
            mime="text/csv"
        )

    else:
        st.info("No appointment records available.")
