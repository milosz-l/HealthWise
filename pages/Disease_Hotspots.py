import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
from sktime.forecasting.statsforecast import StatsForecastAutoCES
from sktime.forecasting.base import ForecastingHorizon

from matplotlib.ticker import MaxNLocator
from dotenv import load_dotenv

load_dotenv()


def authenticate_hotspots():
    """Authenticates the user for the Disease Hotspots page."""
    password = os.getenv("HOTSPOTS_PASSWORD")

    if "is_hotspots_authenticated" not in st.session_state:
        st.session_state.is_hotspots_authenticated = False

    if not st.session_state.is_hotspots_authenticated:
        entered_password = st.text_input(
            "Enter password for Disease Hotspots:", type="password"
        )
        if entered_password == password:
            st.session_state.is_hotspots_authenticated = True
        elif entered_password:
            st.error("Incorrect password.")

    return st.session_state.is_hotspots_authenticated


st.set_page_config(page_title="HealthWise - Hotspots", page_icon="📈")

if authenticate_hotspots():
    DATASET = "Hotspots.csv"
    DAYS_TO_PREDICT = 14
    LAT_CENTER = 20.7967
    LON_CENTER = -156.3319
    DEFAULT = pd.DataFrame({"LAT": [LAT_CENTER], "LON": [LON_CENTER]})
from dotenv import load_dotenv

load_dotenv()


def authenticate_hotspots():
    """Authenticates the user for the Disease Hotspots page."""
    password = os.getenv("HOTSPOTS_PASSWORD")

    if "is_hotspots_authenticated" not in st.session_state:
        st.session_state.is_hotspots_authenticated = False

    if not st.session_state.is_hotspots_authenticated:
        entered_password = st.text_input(
            "Enter password for Disease Hotspots:", type="password"
        )
        if entered_password == password:
            st.session_state.is_hotspots_authenticated = True
        elif entered_password:
            st.error("Incorrect password.")

    return st.session_state.is_hotspots_authenticated


st.set_page_config(page_title="HealthWise - Hotspots", page_icon="📈")

if authenticate_hotspots():
    DATASET = "Hotspots.csv"
    DAYS_TO_PREDICT = 14
    LAT_CENTER = 20.7967
    LON_CENTER = -156.3319
    DEFAULT = pd.DataFrame({"LAT": [LAT_CENTER], "LON": [LON_CENTER]})

    @st.cache_data
    def load_data():
        return pd.read_csv(
            DATASET,
            sep=";",
            header=None,
            names=["USER_ID", "DISEASE", "DATE", "LAT", "LON", "SUMMARY"],
        )
    @st.cache_data
    def load_data():
        return pd.read_csv(
            DATASET,
            sep=";",
            header=None,
            names=["USER_ID", "DISEASE", "DATE", "LAT", "LON", "SUMMARY"],
        )

    def count_disease_by_id(df, id_column, target_id):
        return df[id_column].eq(target_id).sum()

    def rgba_to_hex(rgba):
        return "#{:02x}{:02x}{:02x}{:02x}".format(
            int(rgba[0] * 255),
            int(rgba[1] * 255),
            int(rgba[2] * 255),
            int(rgba[3] * 255),
        )
    
    def predict_data(cumulative_count):

        extended_dates = pd.date_range(
            cumulative_count.index[-1], periods=DAYS_TO_PREDICT, freq="D"
        )[1:]

        y_train = cumulative_count.values
        fh = ForecastingHorizon(extended_dates, is_relative=False)
        preds = model.fit_predict(y_train, fh=fh)
        ax2.plot(
            extended_dates, preds, color="red", linestyle="--", label="Predicted Trend"
        )
        ax2.legend()

    df = load_data()
    df["USER_ID"] = df["USER_ID"].astype("string")
    df["DISEASE"] = df["DISEASE"].astype("string")
    df["DATE"] = pd.to_datetime(df["DATE"], format="%d.%m.%Y", errors="coerce")
    df["LAT"] = df["LAT"].astype("float")
    df["LON"] = df["LON"].astype("float")
    df["SUMMARY"] = df["SUMMARY"].astype("string")
    df = load_data()
    df["USER_ID"] = df["USER_ID"].astype("string")
    df["DISEASE"] = df["DISEASE"].astype("string")
    df["DATE"] = pd.to_datetime(df["DATE"], format="%d.%m.%Y", errors="coerce")
    df["LAT"] = df["LAT"].astype("float")
    df["LON"] = df["LON"].astype("float")
    df["SUMMARY"] = df["SUMMARY"].astype("string")

    min_date = df["DATE"].min().date()
    max_date = df["DATE"].max().date()
    unique_diseases = list(df["DISEASE"].unique())
    num_unique_diseases = len(unique_diseases)
    min_date = df["DATE"].min().date()
    max_date = df["DATE"].max().date()
    unique_diseases = list(df["DISEASE"].unique())
    num_unique_diseases = len(unique_diseases)

    if num_unique_diseases > 256:
        raise ValueError(
            f"The number of unique diseases ({num_unique_diseases}) exceeds the maximum number of colors available (256)."
        )
    if num_unique_diseases > 256:
        raise ValueError(
            f"The number of unique diseases ({num_unique_diseases}) exceeds the maximum number of colors available (256)."
        )

    colors = plt.get_cmap("viridis", num_unique_diseases)
    colors = [rgba_to_hex(colors(i)) for i in range(num_unique_diseases)]
    colors = plt.get_cmap("viridis", num_unique_diseases)
    colors = [rgba_to_hex(colors(i)) for i in range(num_unique_diseases)]

    df["COLOR"] = df["DISEASE"].map(dict(zip(unique_diseases, colors)))
    df["COLOR"] = df["DISEASE"].map(dict(zip(unique_diseases, colors)))

    fig1, ax1 = plt.subplots()
    ax1.set_xlabel("Date")
    ax1.set_ylabel("New Cases")
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    fig1, ax1 = plt.subplots()
    ax1.set_xlabel("Date")
    ax1.set_ylabel("New Cases")
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    fig2, ax2 = plt.subplots()
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Cumulative Number of Cases")
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    fig2, ax2 = plt.subplots()
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Cumulative Number of Cases")
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.grid()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.grid()

    fig3, ax3 = plt.subplots()
    ax3.axis("equal")
    fig3, ax3 = plt.subplots()
    ax3.axis("equal")

    model = StatsForecastAutoCES()

    with st.sidebar:
        start_date = st.date_input(
            label="Start date", min_value=min_date, max_value=max_date
        )
        end_date = st.date_input(
            label="End date", min_value=start_date, max_value=max_date
        )
        main_df = df[
            (df["DATE"].dt.date >= start_date) & (df["DATE"].dt.date <= end_date)
        ][["DISEASE", "DATE", "LAT", "LON", "SUMMARY", "COLOR"]]
    with st.sidebar:
        start_date = st.date_input(
            label="Start date", min_value=min_date, max_value=max_date
        )
        end_date = st.date_input(
            label="End date", min_value=start_date, max_value=max_date
        )
        main_df = df[
            (df["DATE"].dt.date >= start_date) & (df["DATE"].dt.date <= end_date)
        ][["DISEASE", "DATE", "LAT", "LON", "SUMMARY", "COLOR"]]

    if not main_df.empty:
        ids = ["All"] + unique_diseases
        disease_id = st.sidebar.selectbox("Choose disease ID", ids, key="disease_id")
        st.write("### Reported Cases:")
        count_sick = 0
    if not main_df.empty:
        ids = ["All"] + unique_diseases
        disease_id = st.sidebar.selectbox("Choose disease ID", ids, key="disease_id")
        st.write("### Reported Cases:")
        count_sick = 0

        if disease_id == "All":
            count_sick = main_df["DISEASE"].count()
        if disease_id == "All":
            count_sick = main_df["DISEASE"].count()

            if count_sick == 0:
                st.map(DEFAULT, color="#00000000", zoom=8)
            if count_sick == 0:
                st.map(DEFAULT, color="#00000000", zoom=8)

            else:
                st.map(main_df, color="COLOR", zoom=9)
            else:
                st.map(main_df, color="COLOR", zoom=9)

                if start_date != end_date:
                    ratio = []
                if start_date != end_date:
                    ratio = []

                    for color_idx, id in enumerate(unique_diseases):
                        count_per_date = (
                            main_df[main_df["DISEASE"] == id]
                            .groupby("DATE")["DISEASE"]
                            .count()
                        )
                        cumulative_count = count_per_date.cumsum()
                        ax2.plot(
                            cumulative_count.index,
                            cumulative_count,
                            marker="o",
                            linestyle="-",
                            label=id,
                            color=colors[color_idx],
                        )
                        ratio.append(count_per_date.sum())
                    for color_idx, id in enumerate(unique_diseases):
                        count_per_date = (
                            main_df[main_df["DISEASE"] == id]
                            .groupby("DATE")["DISEASE"]
                            .count()
                        )
                        cumulative_count = count_per_date.cumsum()
                        ax2.plot(
                            cumulative_count.index,
                            cumulative_count,
                            marker="o",
                            linestyle="-",
                            label=id,
                            color=colors[color_idx],
                        )
                        ratio.append(count_per_date.sum())

                    ax2.legend()
                    ax2.legend()

                    st.write("### Predicting the Disease Spread Rate:")
                    st.pyplot(fig2)
                    st.write("### Predicting the Disease Spread Rate:")
                    st.pyplot(fig2)

                    ax3.pie(
                        ratio,
                        labels=unique_diseases,
                        autopct="%1.1f%%",
                        startangle=90,
                        colors=colors,
                    )
                    st.write("### Disease Distribution Analysis:")
                    st.pyplot(fig3)
                    ax3.pie(
                        ratio,
                        labels=unique_diseases,
                        autopct="%1.1f%%",
                        startangle=90,
                        colors=colors,
                    )
                    st.write("### Disease Distribution Analysis:")
                    st.pyplot(fig3)

        else:
            count_sick = count_disease_by_id(main_df, "DISEASE", disease_id)
        else:
            count_sick = count_disease_by_id(main_df, "DISEASE", disease_id)

            if count_sick == 0:
                st.map(DEFAULT, color="#00000000", zoom=8)
            if count_sick == 0:
                st.map(DEFAULT, color="#00000000", zoom=8)

            else:
                color_idx = unique_diseases.index(disease_id)
                st.map(
                    main_df[main_df["DISEASE"] == disease_id],
                    color=colors[color_idx],
                    zoom=9,
                )
            else:
                color_idx = unique_diseases.index(disease_id)
                st.map(
                    main_df[main_df["DISEASE"] == disease_id],
                    color=colors[color_idx],
                    zoom=9,
                )

                if start_date != end_date:
                    count_per_date = (
                        main_df[main_df["DISEASE"] == disease_id]
                        .groupby("DATE")["DISEASE"]
                        .count()
                    )
                    cumulative_count = count_per_date.cumsum()
                if start_date != end_date:
                    count_per_date = (
                        main_df[main_df["DISEASE"] == disease_id]
                        .groupby("DATE")["DISEASE"]
                        .count()
                    )
                    cumulative_count = count_per_date.cumsum()

                    ax1.hist(
                        count_per_date.index,
                        bins=len(count_per_date),
                        weights=count_per_date,
                        color=colors[color_idx],
                        edgecolor="black",
                    )
                    st.write("### Analysis of New Cases:")
                    st.pyplot(fig1)
                    ax1.hist(
                        count_per_date.index,
                        bins=len(count_per_date),
                        weights=count_per_date,
                        color=colors[color_idx],
                        edgecolor="black",
                    )
                    st.write("### Analysis of New Cases:")
                    st.pyplot(fig1)

                    ax2.plot(
                        cumulative_count.index,
                        cumulative_count,
                        color=colors[color_idx],
                        marker="o",
                        linestyle="-",
                        label="Cumulative Number of Cases",
                    )
                    predict_data(cumulative_count)
                    ax2.plot(
                        cumulative_count.index,
                        cumulative_count,
                        color=colors[color_idx],
                        marker="o",
                        linestyle="-",
                        label="Cumulative Number of Cases",
                    )
                    predict_data(cumulative_count)

                    st.write("### Predicting the Disease Spread Rate:")
                    st.pyplot(fig2)
                    st.write("### Predicting the Disease Spread Rate:")
                    st.pyplot(fig2)

        col1, col2, col3 = st.columns(3)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Disease ID", value=disease_id)
        with col1:
            st.metric("Disease ID", value=disease_id)

        with col2:
            st.metric("Infected", value=count_sick)
        with col2:
            st.metric("Infected", value=count_sick)

        with col3:
            if disease_id != "All":
                unique_users = main_df["DISEASE"].count()
                infected_percentage = (
                    (count_sick / unique_users) * 100 if unique_users > 0 else 0
                )
                st.metric(
                    "Percentage Infected", value=f"{round(infected_percentage, 2)}%"
                )
        with col3:
            if disease_id != "All":
                unique_users = main_df["DISEASE"].count()
                infected_percentage = (
                    (count_sick / unique_users) * 100 if unique_users > 0 else 0
                )
                st.metric(
                    "Percentage Infected", value=f"{round(infected_percentage, 2)}%"
                )

        if disease_id != "All":
            st.write("### Detailed Data for", disease_id)
            st.dataframe(
                main_df[main_df["DISEASE"] == disease_id][
                    ["DATE", "LAT", "LON", "SUMMARY"]
                ]
            )
else:
    st.warning("Please enter the password to access the admin panel.")
        if disease_id != "All":
            st.write("### Detailed Data for", disease_id)
            st.dataframe(
                main_df[main_df["DISEASE"] == disease_id][
                    ["DATE", "LAT", "LON", "SUMMARY"]
                ]
            )
else:
    st.warning("Please enter the password to access the admin panel.")
