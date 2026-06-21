import streamlit as st
import pandas as pd
import plotly.express as px
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def format_number(num):
    if num >= 10_000_000:
        return f"₹{num/10_000_000:.2f} Cr"
    elif num >= 100_000:
        return f"₹{num/100_000:.2f} L"
    elif num >= 1000:
        return f"₹{num/1000:.2f} K"
    else:
        return f"₹{num:.2f}"
    
def format_count(num):
    if num >= 10_000_000:
        return f"{num/10_000_000:.2f} Cr"
    elif num >= 100_000:
        return f"{num/100_000:.2f} L"
    elif num >= 1000:
        return f"{num/1000:.2f} K"
    else:
        return f"{num:.0f}"

st.set_page_config(
    page_title='Cloud Kitchen Dashboard',
    page_icon=os.path.join(BASE_DIR, 'Data', 'Logo.jpg'),
    layout='wide'
)

@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, 'kitchen_pnl_cleaned.csv'))
    df['month'] = pd.to_datetime(df['month'])
    return df

df = load_data()

st.sidebar.image(os.path.join(BASE_DIR, 'Data', 'Logo.jpg'), width=150)
st.sidebar.title('Cloud Kitchen Dashboard')
page = st.sidebar.radio(
    "Select Dashboard",
    ["Dashboard 1 : Kitchen PNL", "Dashboard 2 : Variance PNL", "Dashboard 3 : Business Insights"]
)

if page == "Dashboard 1 : Kitchen PNL":
    st.title("Kitchen Level PNL")
    st.markdown("---")

    st.subheader('Filters')

    col1, col2, col3, col4 = st.columns(4)

    with col1 :
        store_filter = st.multiselect(
            "Store",
            options = sorted(df['store'].unique()),
            default=[]
        )

    with col2 :
        city_filter = st.multiselect(
            "City",
            options = sorted(df['city'].unique()),
            default=[]
        )

    with col3 :
        zone_filter = st.multiselect(
            "Zone",
            options = sorted(df['zone_mapping'].unique()),
            default=[]

        )
    
    with col4 :
        month_filter = st.multiselect(
            "Month",
            options = sorted(df['month'].dt.strftime('%B %Y').unique()),
            default=[]
        )

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        revenue_cohort_filter = st.multiselect(
            "Revenue Cohort",
            options=sorted(df['revenue_cohort'].unique()),
            default=[]
        )

    with col6:
        ebitda_category_filter = st.multiselect(
            "EBITDA Category",
            options=sorted(df['ebitda_category'].unique()),
            default=[]
        )
    
    with col7:
        ebitda_cohort_filter = st.multiselect(
            "EBITDA Cohort",
            options=sorted(df['ebitda_cohort'].unique()),
            default=[]
        )
    
    with col8:
        cm_cohort_filter = st.multiselect(
            "CM Cohort",
            options=sorted(df['cm_cohort'].unique()),
            default=[]
        )


    col9, col10, col11 = st.columns(3)

    with col9 :
        revenue_range = st.slider(
            "Net Revenue Range(₹)",
            min_value=float(df['net_revenue'].min()),
            max_value=float(df['net_revenue'].max()),
            value=(float(df['net_revenue'].min()), float(df['net_revenue'].max()))
        )

    with col10 :
        ebitda_range = st.slider(
            "Ebitda Range",
            min_value=float(df['kitchen_ebitda'].min()),
            max_value=float(df['kitchen_ebitda'].max()),
            value = (float(df['kitchen_ebitda'].min()), float(df['kitchen_ebitda'].max()) )
        )

    with col11 :
        cm_range = st.slider(
            "CM Range",
            min_value=float(df['cm'].min()),
            max_value=float(df['cm'].max()),
            value = (float(df['cm'].min()), float(df['cm'].max()) )
        )

    st.markdown("---")

    filtered_df = df.copy()

    if store_filter :
        filtered_df = filtered_df[filtered_df['store'].isin(store_filter)]
    if city_filter :
        filtered_df = filtered_df[filtered_df['city'].isin(city_filter)]
    if zone_filter :
        filtered_df = filtered_df[filtered_df['zone_mapping'].isin(zone_filter)]
    if month_filter :
        filtered_df = filtered_df[filtered_df['month'].dt.strftime('%B %Y').isin(month_filter)]
    if revenue_cohort_filter :
        filtered_df = filtered_df[filtered_df['revenue_cohort'].isin(revenue_cohort_filter)]
    if ebitda_category_filter :
        filtered_df = filtered_df[filtered_df['ebitda_category'].isin(ebitda_category_filter)]
    if ebitda_cohort_filter :
        filtered_df = filtered_df[filtered_df['ebitda_cohort'].isin(ebitda_cohort_filter)]
    if cm_cohort_filter :
        filtered_df = filtered_df[filtered_df['cm_cohort'].isin(cm_cohort_filter)]
    

    filtered_df = filtered_df[
        (filtered_df['net_revenue'] >= revenue_range[0])&
        (filtered_df['net_revenue'] <= revenue_range[1])&
        (filtered_df['kitchen_ebitda'] >= ebitda_range[0])&
        (filtered_df['kitchen_ebitda'] <= ebitda_range[1])&
        (filtered_df['cm'] >= cm_range[0])&
        (filtered_df['cm'] <= cm_range[1])
    ]

    st.caption(f"Showing {len(filtered_df)} records after filter")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(label="Total Net Revenue", value=format_number(filtered_df['net_revenue'].sum()))

    with col2:
        st.metric(label="Total Orders", value=format_count(filtered_df['order_count'].sum()))

    with col3:
        st.metric(label="Average GM%", value=f"{filtered_df['gm%'].mean()*100:.2f}%")

    with col4:
        st.metric(label="Average EBITDA %", value=f"{filtered_df['ebitda_margin%'].mean()*100:.2f}%")

    with col5:
        st.metric(label="Total Stores", value=(filtered_df['store'].nunique()))


    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        top_stores = filtered_df.groupby('store')['net_revenue'].sum().sort_values(ascending=False).head(10).reset_index()
        fig1 = px.bar(
        top_stores,
        x = 'store',
        y = 'net_revenue',
        title="Top 10 Stores by Revenue"
    )
        st.plotly_chart(fig1, use_container_width=True)


    with row1_col2:
        ebitda_by_store = filtered_df.groupby('store')['kitchen_ebitda'].sum().sort_values(ascending=False).head(10).reset_index()
        fig2 = px.bar(
            ebitda_by_store,
            x = 'store',
            y = 'kitchen_ebitda',
            title="Top 10 Stores by EBITDA"
    )
        st.plotly_chart(fig2, use_container_width=True)

    
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1 :

        monthy_trend = filtered_df.groupby('month')['net_revenue'].sum().reset_index()
        fig3 = px.line(
            monthy_trend,
            x = 'month',
            y='net_revenue',
            title='Monthly Revenue Trend'
        )
        st.plotly_chart(fig3, use_container_width=True)

    with row2_col2 :

        monthly_discount_trend = filtered_df.groupby('month')['discount%'].sum().reset_index()
        fig4 = px.line(
            monthly_discount_trend,
            x = 'month',
            y='discount%',
            title='Monthly Discount Trend'
        )
        st.plotly_chart(fig4, use_container_width=True)

    with row2_col3 :

        monthly_orders_trend = filtered_df.groupby('month')['order_count'].sum().reset_index()
        fig4 = px.line(
            monthly_orders_trend,
            x = 'month',
            y='order_count',
            title='Monthly Orders Trend'
        )
        st.plotly_chart(fig4, use_container_width=True)

    table_df = filtered_df[['store', 'net_revenue', 'gm%', 'cm%', 'kitchen_ebitda', 'ebitda_margin%', 'month']]
    table_df = table_df.copy()
    table_df['month'] = table_df['month'].dt.strftime('%b %Y')
    pivot = table_df.pivot_table(
            index='store',
            columns='month',
            values=['net_revenue', 'gm%', 'cm%', 'kitchen_ebitda', 'ebitda_margin%'],
            aggfunc={
                'net_revenue': 'sum',
                'kitchen_ebitda': 'sum',
                'gm%': 'mean',
                'cm%': 'mean',
                'ebitda_margin%': 'mean'
    }
            )
    pivot = pivot.swaplevel(axis=1)
    pivot = pivot.sort_index(axis=1, level=[0, 1], ascending=[False, True])
    pivot = pivot.sort_index(
        axis=1,
        level=0,
        key=lambda x: pd.to_datetime(x, format='%b %Y'),
        ascending=False
    )
    st.subheader("Kitchen Snapshot")
    pct_cols = [col for col in pivot.columns if col[1] in ['gm%', 'cm%', 'ebitda_margin%']]
    num_cols = [col for col in pivot.columns if col[1] in ['net_revenue', 'kitchen_ebitda']]
    format_dict = {}
    for col in pct_cols:
        format_dict[col] = '{:.2%}'
    for col in num_cols:
        format_dict[col] = '₹{:,.0f}'
    
    st.dataframe(pivot.style.format(format_dict), use_container_width=True)

    st.markdown("---")
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv,
        file_name="kitchen_pnl_filtered.csv",
        mime="text/csv"
    )


elif page == "Dashboard 2 : Variance PNL":
    st.title("Variance Level PNL")
    st.markdown("---")
    

    st.subheader('Filters')

    col1, col2, col3, col4 = st.columns(4)

    with col1 :
        variance_category_filter = st.multiselect(
            "Variance Category",
            options = sorted(df['variance_category'].unique()),
            default=[]
        )

    with col2 :
        month_filter = st.multiselect(
            "Month",
            options = sorted(df['month'].dt.strftime('%B %Y').unique()),
            default=[]
        )

    with col3 :
        city_filter = st.multiselect(
            "City",
            options= sorted(df['city'].unique()),
            default=[]
        )

    with col4 :
        zone_filter = st.multiselect(
            "Zone",
            options= sorted(df['zone_mapping'].unique()),
            default=[]
        )

    col5, col6, col7 = st.columns(3)

    with col5 :
        net_revenue_range = st.slider(
            "Net Revenue (₹)",
            min_value=float(df['net_revenue'].min()),
            max_value=float(df['net_revenue'].max()),
            value = (float(df['net_revenue'].min()), float(df['net_revenue'].max()))
        )

    with col6 :
        ebitda_range_filter = st.slider(
            "EBITDA Range",
            min_value=float(df['kitchen_ebitda'].min()),
            max_value=float(df['kitchen_ebitda'].max()),
            value = (float(df['kitchen_ebitda'].min()), float(df['kitchen_ebitda'].max()))
        )

    with col7 :
        cm_filter = st.slider(
            "CM Filter",
            min_value = float(df['cm'].min()),
            max_value= float(df['cm'].max()),
            value = (float(df['cm'].min()), float(df['cm'].max()))
        )

    st.markdown('---')

    filtered_df = df.copy()

    if variance_category_filter :
        filtered_df = filtered_df[filtered_df['variance_category'].isin(variance_category_filter)]

    if month_filter :
        filtered_df = filtered_df[filtered_df['month'].dt.strftime('%B %Y').isin(month_filter)]

    if city_filter :
        filtered_df = filtered_df[filtered_df['city'].isin(city_filter)]

    if zone_filter :
        filtered_df = filtered_df[filtered_df['zone_mapping'].isin(zone_filter)]


    filtered_df = filtered_df[
        (filtered_df['net_revenue'] >= net_revenue_range[0])&
        (filtered_df['net_revenue'] <= net_revenue_range[1])&
        (filtered_df['kitchen_ebitda'] >= ebitda_range_filter[0])&
        (filtered_df['kitchen_ebitda'] <= ebitda_range_filter[1])&
        (filtered_df['cm'] >= cm_filter[0])&
        (filtered_df['cm'] <= cm_filter[1])
    ]

    st.caption(f"Showing {len(filtered_df)} records after filter")

    col5, col6, col7, col8 = st.columns(4)

    with col5 :
        st.metric(label= "Average Variance", value= format_count(filtered_df['variance'].mean()))

    with col6 :
        st.metric(label = "Total Stores", value= format_count(filtered_df['store'].nunique()))

    with col7 :
        st.metric(label = "Average Net Revenue", value = format_number(filtered_df['net_revenue'].mean()))

    with col8 :
        st.metric(label = "Average EBITDA", value = format_count(filtered_df['kitchen_ebitda'].mean()))

    pivot_df = filtered_df.copy()
    pivot_df['month'] = pivot_df['month'].dt.strftime('%B %Y')

    st.markdown("---")

    st.subheader("Variance by Revenue Category")

    var_pivot = pivot_df.pivot_table(
        index= 'revenue_cohort',
        columns= 'month',
        values= 'variance%',
        aggfunc= 'mean'
    ).round(4)

    var_pivot.columns.name = None

    var_pivot = var_pivot.sort_index(
        axis=1,
        key=lambda x: pd.to_datetime(x, format='%B %Y'),
        ascending=False
        )
    
    var_pivot.loc['Grand Total'] = var_pivot.mean()

    st.dataframe(var_pivot.style.format("{:.2%}"), use_container_width=True)

    st.markdown('---')

    st.subheader("Store Count by Revenue Category")

    store_pivot = pivot_df.pivot_table(
        index = 'revenue_cohort',
        columns = 'month',
        values = 'store',
        aggfunc='nunique'
    )

    store_pivot.columns.name = None

    store_pivot = store_pivot.sort_index(
        axis =1,
        key = lambda x : pd.to_datetime(x, format ='%B %Y'),
        ascending = False
    )

    store_pivot.loc['Grand_Total'] = store_pivot.sum()

    st.dataframe(store_pivot, use_container_width=True)


elif page == "Dashboard 3 : Business Insights":
    st.title("Business Insights & Recommendations")
    st.markdown("---")
    
    with st.container(border=True):
        st.subheader("Revenue Distribution Analysis")

        st.markdown("""
        ### Observation
        Revenue across stores is fairly balanced overall, with most stores earning 
        between ₹2.9M and ₹4.1M. However, a few stores are performing significantly 
        better than others, crossing ₹6M in revenue. This indicates that a small 
        group of outlets contributes a major share of the overall business revenue.
        """)

        st.success("""
        ### Implication
        These top-performing stores are clearly doing something right. The business 
        should identify what is driving their success — whether it is location, 
        pricing, customer demand, or operational efficiency — and replicate those 
        strategies across mid-performing stores.
        """)
        st.markdown("---")

    with st.container(border=True):
        
        st.subheader("City-Level Profitability — Mumbai vs Pune")

        st.markdown("""
        ### Observation
        Mumbai is generating higher overall revenue compared to Pune. However, Pune 
        is delivering stronger EBITDA margins, which indicates better profitability 
        and operational efficiency despite lower revenue.
        """)

        st.success("""
        ### Implication
        Higher revenue does not always guarantee better profitability. Pune appears 
        to have stronger cost management and operational discipline. The business 
        should study Pune’s operating model and identify practices that can also be 
        implemented in Mumbai.
        """)
        st.markdown("---")


    with st.container(border=True):

        st.subheader("January 2024 — AOV-Driven Profitability")

        st.markdown("""
        ### Observation
        In January 2024, order volume decreased, but both revenue and EBITDA increased. 
        This was mainly driven by an increase in Average Order Value (AOV), meaning 
        customers spent more per transaction.
        """)

        st.success("""
        ### Implication
        This suggests that profitability is not solely dependent on order count. 
        Factors such as premium menu mix, upselling, combo offers, or lower discounting 
        may have improved AOV. Replicating these strategies could help improve margins 
        consistently across future months.
        """)
        st.markdown("---")

    with st.container(border=True):

        st.subheader("Discount Strategy — Volume vs Profitability")

        st.markdown("""
        ### Observation
        Discounting appears to increase order volume, but it does not significantly 
        improve revenue or EBITDA. More orders are being generated, but the value 
        and profitability of those orders remain weak.
        """)

        st.success("""
        ### Implication
        The current discount strategy is trading margins for volume without creating 
        meaningful revenue growth. Instead of broad discounting, the business should 
        focus on targeted discounts for high-margin products or loyal customer segments.
        """)
        st.markdown("---")

    with st.container(border=True):

        st.subheader("Correlation Analysis")

        st.markdown("""
        ### Observation
        Gross Margin and Kitchen EBITDA show an extremely strong correlation (0.99), 
        indicating that EBITDA performance is heavily dependent on gross margins.

        AOV has almost no relationship with order count (-0.03), meaning stores with 
        higher order volumes are not necessarily generating higher-value orders.

        Discounting also shows only a moderate relationship with revenue, suggesting 
        that aggressive discounting does not directly translate into stronger earnings.
        """)

        st.success("""
        ### Implication
        Improving profitability will require stronger focus on pricing strategy, menu 
        optimisation, and food cost control instead of only increasing order volume.

        Since AOV and order count are independent, the business can separately focus 
        on upselling and premium offerings to improve basket size without relying 
        heavily on discounts.
        """)
        st.markdown("---")

    with st.container(border=True):

        st.subheader("Monthly Revenue Trend")

        st.markdown("""
        ### Observation
        Revenue followed a fluctuating trend between Oct 2023 and Mar 2024, with 
        repeated dips and recoveries instead of stable growth. December recorded 
        the lowest revenue, January showed the highest spike, and February declined 
        again before March recovered slightly.

        Although revenue fluctuated month-on-month, the overall revenue range remained 
        relatively narrow, indicating business stability but limited growth momentum.
        """)

        st.success("""
        ### Implication
        Revenue performance currently appears dependent on short-term spikes driven 
        by campaigns, promotions, or seasonal demand rather than sustainable growth.

        The business should identify the key drivers behind January’s strong performance 
        and explore ways to replicate those strategies consistently across future months.
        """)
        st.markdown("---")

    with st.container(border=True):

        st.subheader("November vs December Revenue Performance")

        st.markdown("""
        ### Observation
        November recorded lower revenue mainly due to lower order volume. In December, 
        order count increased, but revenue declined even further despite the higher 
        number of orders.

        This happened because heavier discounts were used to acquire customers, which 
        reduced the revenue generated per order.
        """)

        st.success("""
        ### Implication
        Increasing order volume alone is not enough if profitability is impacted by 
        aggressive discounting. The December trend suggests that discount-driven orders 
        contributed lower-value revenue and weaker margins.

        The business should focus on balancing customer acquisition with sustainable 
        pricing strategies instead of relying heavily on discounts for growth.
        """)

