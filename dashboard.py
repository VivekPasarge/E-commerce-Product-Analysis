
import streamlit as st
import pandas as pd
from pymongo import MongoClient

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="E-commerce Product Analysis",
    page_icon="🛒",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f4f7fb;
}

/* Main headings */
h1, h2, h3 {
    color: #17365d;
    font-weight: 700;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #64748b;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #eaf0f8;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

/* Containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px;
}

/* Horizontal divider */
hr {
    border-color: #dbe3ef;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:
    st.title("DataSphere")

    st.markdown("---")

    st.subheader("E-commerce Analytics")

    st.write(
        "A MongoDB-based system for processing "
        "and analysing e-commerce data."
    )

    st.markdown("---")

    st.subheader("Technologies Used")

    st.write("Python")
    st.write("MongoDB")
    st.write("PyMongo")
    st.write("Pandas")
    st.write("Streamlit")

    st.markdown("---")

    st.caption("Academic Big Data Analytics Project")

# --------------------------------
# MAIN HEADER
# --------------------------------

st.markdown("""
<div style="padding: 10px 0 20px 0;">
    <h1 style="color:#17365d; font-size:36px;">
        E-commerce Product Analysis
    </h1>
    <p style="color:#64748b; font-size:16px;">
        MongoDB-Based Big Data Processing and Analytics System
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# --------------------------------
# MONGODB CONNECTION
# --------------------------------

@st.cache_resource
def get_database():

    client = MongoClient(
        "mongodb://localhost:27017",
        serverSelectionTimeoutMS=5000
    )

    client.admin.command("ping")

    return client["ecommerce_analysis"]


try:

    db = get_database()

    # --------------------------------
    # KEY METRICS
    # --------------------------------

    st.subheader("Project Overview")

    total_products = db.products.count_documents({})
    total_items = db.order_items.count_documents({})
    total_orders = db.orders.count_documents({})

    review_data = list(db.reviews.aggregate([
        {
            "$group": {
                "_id": None,
                "average_score": {"$avg": "$review_score"},
                "total_reviews": {"$sum": 1}
            }
        }
    ]))

    average_score = (
        round(review_data[0]["average_score"], 2)
        if review_data and
        review_data[0]["average_score"] is not None
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Products",
        f"{total_products:,}"
    )

    col2.metric(
        "Order Items",
        f"{total_items:,}"
    )

    col3.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col4.metric(
        "Average Review Score",
        f"{average_score}/5"
    )

    st.divider()

    # --------------------------------
    # ORDERS BY STATUS
    # --------------------------------

    st.subheader("📦 Orders by Status")

    status_data = list(db.orders.aggregate([
        {
            "$group": {
                "_id": "$order_status",
                "total": {"$sum": 1}
            }
        },
        {"$sort": {"total": -1}}
    ]))

    if status_data:

        status_df = pd.DataFrame(status_data).rename(
            columns={
                "_id": "Order Status",
                "total": "Orders"
            }
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.bar_chart(
                status_df,
                x="Order Status",
                y="Orders",
                horizontal=True
            )

        with col2:
            st.dataframe(
                status_df,
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    # --------------------------------
    # TOP 10 PRODUCT CATEGORIES
    # --------------------------------

    st.subheader("🏷️ Top 10 Product Categories by Product Count")

    category_data = list(db.products.aggregate([
        {
            "$match": {
                "product_category_name": {"$ne": None}
            }
        },
        {
            "$group": {
                "_id": "$product_category_name",
                "total_products": {"$sum": 1}
            }
        },
        {"$sort": {"total_products": -1}},
        {"$limit": 10}
    ]))

    if category_data:

        category_df = pd.DataFrame(category_data).rename(
            columns={
                "_id": "Category",
                "total_products": "Products"
            }
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.bar_chart(
                category_df,
                x="Category",
                y="Products",
                horizontal=True
            )

        with col2:
            st.dataframe(
                category_df,
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    # --------------------------------
    # REVENUE BY PRODUCT CATEGORY
    # --------------------------------

    st.subheader("💰 Revenue by Product Category")

    with st.spinner("Calculating category-wise revenue..."):

        revenue_category_data = list(db.order_items.aggregate([
            {
                "$lookup": {
                    "from": "products",
                    "localField": "product_id",
                    "foreignField": "product_id",
                    "as": "product"
                }
            },
            {"$unwind": "$product"},
            {
                "$group": {
                    "_id": "$product.product_category_name",
                    "total_revenue": {"$sum": "$price"}
                }
            },
            {
                "$match": {
                    "_id": {"$ne": None}
                }
            },
            {"$sort": {"total_revenue": -1}},
            {"$limit": 10}
        ]))

    if revenue_category_data:

        revenue_df = pd.DataFrame(
            revenue_category_data
        ).rename(
            columns={
                "_id": "Category",
                "total_revenue": "Revenue"
            }
        )

        revenue_df["Revenue"] = (
            revenue_df["Revenue"].round(2)
        )

        st.caption(
            "Top 10 categories ranked by total item-price revenue."
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.bar_chart(
                revenue_df,
                x="Category",
                y="Revenue",
                horizontal=True
            )

        with col2:
            st.dataframe(
                revenue_df,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.warning("No category revenue data found.")

    st.divider()

    # --------------------------------
    # TOP 10 PRODUCTS BY SALES VALUE
    # --------------------------------

    st.subheader("📊 Top 10 Products by Item-Price Value")

    sales_data = list(db.order_items.aggregate([
        {
            "$group": {
                "_id": "$product_id",
                "total_sales": {"$sum": "$price"},
                "times_ordered": {"$sum": 1}
            }
        },
        {"$sort": {"total_sales": -1}},
        {"$limit": 10}
    ]))

    if sales_data:

        sales_df = pd.DataFrame(sales_data).rename(
            columns={
                "_id": "Product ID",
                "total_sales": "Item-Price Value",
                "times_ordered": "Order Item Records"
            }
        )

        sales_df["Item-Price Value"] = (
            sales_df["Item-Price Value"].round(2)
        )

        st.dataframe(
            sales_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No sales data was found.")

    st.divider()

    # --------------------------------
    # CUSTOMER REVIEW ANALYSIS
    # --------------------------------

    st.subheader("⭐ Customer Review Analysis")

    review_distribution = list(db.reviews.aggregate([
        {
            "$group": {
                "_id": "$review_score",
                "total_reviews": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]))

    if review_distribution:

        review_df = pd.DataFrame(
            review_distribution
        ).rename(
            columns={
                "_id": "Rating",
                "total_reviews": "Number of Reviews"
            }
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.bar_chart(
                review_df,
                x="Rating",
                y="Number of Reviews"
            )

        with col2:
            st.dataframe(
                review_df,
                use_container_width=True,
                hide_index=True
            )

    else:
        st.info("No customer review data found.")

# --------------------------------
# ERROR HANDLING
# --------------------------------

except Exception as e:

    st.error("Could not load the dashboard data.")

    st.exception(e)

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.markdown("""
<div style="text-align:center; padding:15px;">
    <p style="color:#64748b; font-size:13px;">
        E-commerce Product Analysis |
        MongoDB | Python | Streamlit
    </p>
    <p style="color:#94a3b8; font-size:12px;">
        Academic Big Data Processing and Analytics Project
    </p>
</div>
""", unsafe_allow_html=True)
