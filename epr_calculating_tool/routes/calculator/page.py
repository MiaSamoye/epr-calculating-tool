import streamlit as st
import epr_calculating_tool.routes.calculator.data as data
import pandas as pd
from babel.numbers import format_currency


st.title("Estimate your EPR financial contribution")

industries_list = data.get_industries()


option = st.selectbox(
    label="Which industry is your factory in?",
    options=industries_list.id,
    format_func=lambda x: industries_list.loc[industries_list["id"] == x, "name"].iloc[0],
    index=industries_list.id.tolist().index(st.session_state.get("industry_option", industries_list.id[0]))
)
st.session_state.industry_option = option

classifications_data = data.get_classifications(option)
# st.write(classifications_data)

classifications = st.multiselect(
    label="Which products/packages do you want to estimate?",
    options=classifications_data.id,
    format_func=lambda x: classifications_data.loc[classifications_data["id"] == x, "name"].iloc[0],
    default=st.session_state.get("selected_classifications", []) # Use session state if available
)
st.session_state.selected_classifications = classifications

recycling_rate_dict = {}
volumes_dict = {}
for each in classifications:
    recycling_rate_dict[each] = classifications_data.loc[classifications_data["id"] == each, "recycling_rate"].iloc[0]

# st.write(recycling_rate_dict)

volumes_dict = {}

for each in classifications:
    st.markdown(f"#### Volume of {classifications_data.loc[classifications_data['id'] == each, 'name'].iloc[0]}: ")
    if f"volume_{each}" not in st.session_state:
        st.session_state[f"volume_{each}"] = 0.0 
    volumes_dict[each] = st.number_input(
        f"Enter value",
        min_value=0.0,
        value=st.session_state.get(f"volume_{each}", 0.0),
        key=f"volume_{each}",
        label_visibility="collapsed"
    )
required_fee = 0

st.write(
    "Do you want to use the data of your factory?"
)
confirm_use_own_data = st.checkbox("Yes", value=st.session_state.get("confirm_use_own_data", False))
st.session_state.confirm_use_own_data = confirm_use_own_data

product_recycle_cost_dict = {}

if not confirm_use_own_data:
    for each in classifications:
        product_recycle_cost_dict[each] = classifications_data.loc[
            classifications_data["id"] == each, "fs_cost"
        ].iloc[0]

    # st.write(product_recycle_cost_dict)


else:

    for each in classifications:
        classification_name = classifications_data.loc[classifications_data["id"] == each, "name"].iloc[0]
        avg_classification_cost = f"{int(classifications_data.loc[classifications_data['id'] == each, 'classification_cost'].iloc[0]):,} VND/kg"
        avg_transport_cost = f"{int(classifications_data.loc[classifications_data['id'] == each, 'transportation_cost'].iloc[0]):,} VND/kg"
        avg_recycling_cost = f"{int(classifications_data.loc[classifications_data['id'] == each, 'recycling_cost'].iloc[0]):,} VND/kg"
        factor =  classifications_data.loc[classifications_data['id'] == each, 'factor'].iloc[0]
        st.markdown(f"#### Fs cost for {classification_name}")

        classifications_cost = st.number_input(
            f"Classification and collection cost: (Average: {avg_classification_cost})",
            min_value=0.0,
            key=f"classification_cost_{each}",
        )

        transport_cost = st.number_input(
            f"Transportation cost: (Average: {avg_transport_cost})",
            min_value=0.0,
            key=f"transport_cost_{each}",
        )

        recycling_cost = st.number_input(
            f"Recycling cost: (Average: {avg_recycling_cost})",
            min_value=0.0,
            key=f"recycling_cost_{each}",
        )

        product_recycle_cost_dict[each] = (classifications_cost + transport_cost + recycling_cost) * 1.03 * factor


st.header("Your financial contribution:")
df_res = pd.DataFrame(
    [volumes_dict, recycling_rate_dict, product_recycle_cost_dict, {}]
).T
df_res.columns = [ "Volume", "Recycling rate", "Fs", "Total fee"]

# Rename row names to proper names
df_res.index = df_res.index.map(
    lambda x: classifications_data.loc[classifications_data["id"] == x, "name"].iloc[0]
)

for index, row in df_res.iterrows():
    df_res.loc[index, "Total fee"] = (
        round(row["Volume"] * row["Recycling rate"] * row["Fs"], 2)
    )

st.write(df_res)

total = df_res["Total fee"].sum()
if total is not None:
   st.markdown(
        f"""
        <div style="border: 1px solid #ccc; padding: 10px 20px; border-radius: 10px; text-align: left; background-color: #1E1E1E; color: #FFF;">
            <p style="font-size: 18px; margin-bottom: 5px;">Total financial contribution:</p>
            <p style="font-size: 40px; font-weight: bold; color: #5E8FFC;">{format_currency(total, 'VND', locale='vi_VN.UTF-8')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )