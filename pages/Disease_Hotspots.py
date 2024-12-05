import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator
from sklearn.neural_network import MLPRegressor


def count_disease_by_id(df, id_column, target_id):
    return df[id_column].eq(target_id).sum()


def rgba_to_hex(rgba):
    return '#{:02x}{:02x}{:02x}{:02x}'.format(int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255), int(rgba[3] * 255))


def predict_data(cumulative_count):
    dates_as_numbers = np.array((cumulative_count.index - cumulative_count.index[0]).days).reshape(-1, 1)
    model.fit(dates_as_numbers, cumulative_count.values)
    
    extended_dates = pd.date_range(cumulative_count.index[-1], periods=DAYS_TO_PREDICT, freq='D')[1:]
    extended_dates_as_numbers = np.array((extended_dates - cumulative_count.index[0]).days).reshape(-1, 1)
    preds = model.predict(extended_dates_as_numbers)
    ax2.plot(extended_dates, preds, color='red', linestyle='--', label="Predicted Trend")
    ax2.legend()


st.set_page_config(
    page_title="HealthWise - Hotspots",
    page_icon="💬"
)

DATASET = "Hotspots.csv"
DAYS_TO_PREDICT = 14
LAT_CENTER = 20.7967
LON_CENTER = -156.3319
DEFAULT = pd.DataFrame({"LAT": [LAT_CENTER], "LON": [LON_CENTER]})

df = pd.read_csv(DATASET, sep=";", header=None, names=["USER_ID", "DISEASE_ID", "DATE", "LAT", "LON"])
df["USER_ID"] = df["USER_ID"].astype("string")
df["DISEASE_ID"] = df["DISEASE_ID"].astype("int")
df["DATE"] = pd.to_datetime(df["DATE"], format="%d.%m.%Y", errors='coerce')
df["LAT"] = df["LAT"].astype("float")
df["LON"] = df["LON"].astype("float")

min_date = df["DATE"].min().date()
max_date = df["DATE"].max().date()
unique_diseases = sorted(list(df["DISEASE_ID"].unique()))
colors = plt.cm.get_cmap("viridis", len(unique_diseases))
colors = [rgba_to_hex(colors(i)) for i in range(len(unique_diseases))]

df["COLOR"] = df["DISEASE_ID"].map(dict(zip(unique_diseases, colors)))

fig1, ax1 = plt.subplots()
ax1.set_xlabel("Date")
ax1.set_ylabel("New Infections")
ax1.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.xticks(rotation=45, ha='right')
plt.tight_layout()

fig2, ax2 = plt.subplots()
ax2.set_xlabel("Date")
ax2.set_ylabel("Cumulative Number of Infections")
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid()

model = MLPRegressor()

with st.sidebar:
    start_date = st.date_input(label="Start date", min_value=min_date, max_value=max_date)
    end_date = st.date_input(label="End date", min_value=start_date, max_value=max_date)
    main_df = df[(df["DATE"].dt.date >= start_date) & (df["DATE"].dt.date <= end_date)][["DISEASE_ID", "DATE", "LAT", "LON", "COLOR"]]
    
if not main_df.empty:
    ids = ["All"] + unique_diseases
    disease_id = st.sidebar.selectbox("Choose disease ID", ids, key="disease_id")
    st.write("Reported Infection Cases:")
    count_sick = 0

    if disease_id == "All":
        count_sick = main_df["DISEASE_ID"].count()

        if count_sick == 0:
            st.map(DEFAULT, color="#00000000", zoom=8)
        
        else:
            st.map(main_df, color="COLOR", zoom=9)

            if start_date != end_date:
                count_per_date = main_df.groupby("DATE")["DISEASE_ID"].count()            
                ax1.hist(count_per_date.index, bins=len(count_per_date), weights=count_per_date, edgecolor='black')
                st.write("Analysis of New Cases:")
                st.pyplot(fig1)

                count_per_date = main_df.groupby("DATE")["DISEASE_ID"].count()
                cumulative_count = count_per_date.cumsum()
                ax2.plot(cumulative_count.index, cumulative_count, marker='o', linestyle='-', label="Cumulative Number of Infections")
                predict_data(cumulative_count)
                st.write("Predicting the Disease Spread Rate:")
                st.pyplot(fig2)

    else:
        count_sick = count_disease_by_id(main_df, "DISEASE_ID", disease_id)

        if count_sick == 0:
            st.map(DEFAULT, color="#00000000", zoom=8)
        
        else:
            color_idx = unique_diseases.index(disease_id)
            st.map(main_df[main_df["DISEASE_ID"] == disease_id], color=colors[color_idx], zoom=9)        

            if start_date != end_date:
                count_per_date = main_df[main_df['DISEASE_ID'] == disease_id].groupby("DATE")["DISEASE_ID"].count()            
                ax1.hist(count_per_date.index, bins=len(count_per_date), weights=count_per_date, color=colors[color_idx], edgecolor='black')
                st.write("Analysis of New Cases:")
                st.pyplot(fig1)
                 
                count_per_date = main_df[main_df['DISEASE_ID'] == disease_id].groupby("DATE")["DISEASE_ID"].count()
                cumulative_count = count_per_date.cumsum()
                ax2.plot(cumulative_count.index, cumulative_count, color=colors[color_idx], marker='o', linestyle='-', label="Cumulative Number of Infections")
                predict_data(cumulative_count)
                st.write("Predicting the Disease Spread Rate:")
                st.pyplot(fig2)
                
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric('Disease ID', value=disease_id)
    
    with col2:
        st.metric('Infected', value=count_sick)

    with col3:
        if disease_id != "All":
            unique_users = main_df["DISEASE_ID"].count()
            infected_percentage = (count_sick / unique_users) * 100 if unique_users > 0 else 0
            st.metric("Percentage Infected", value=f"{round(infected_percentage, 2)}%")
        