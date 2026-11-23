# DataSphere
## MongoDB-Based Big Data Processing and Analytics System

DataSphere is a data processing and analytics application developed using Python and MongoDB.

The system stores large-scale e-commerce data, processes records, performs analytical operations and presents meaningful insights through an interactive dashboard.

### Objectives
- Store large datasets using MongoDB.
- Process and manage large volumes of data.
- Perform data analysis using Python.
- Generate meaningful analytical reports.
- Visualize results through interactive charts and dashboards.

### Technologies Used
- Python
- MongoDB
- PyMongo
- Pandas
- Streamlit

### Project Domain
Big Data Management and Analytics.



### Features

- MongoDB database integration.
- Storage of e-commerce product information.
- Large-scale order and review data management.
- Order status analysis.
- Top 10 product categories analysis.
- Revenue analysis by product category.
- Top 10 products by item-price value.
- Customer review analysis.
- Interactive data visualization using Streamlit.
- MongoDB aggregation and data processing using PyMongo.



### Database Structure

Database Name: `ecommerce_analysis`

Collections:

| Collection | Description |
|---|---|
| products | Stores product information |
| sellers | Stores seller information |
| orders | Stores order details |
| order_items | Stores individual order items |
| reviews | Stores customer reviews |



### Installation and Execution

**1. Clone the repository**

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**2. Navigate to the project folder**

```bash
cd ecommerce-product-analysis-main
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Start MongoDB**

Make sure MongoDB Server is installed and running.

**5. Import the Olist CSV datasets**

Import the required datasets into the `ecommerce_analysis` database using MongoDB Compass.

**6. Run the application**

```bash
python -m streamlit run dashboard.py
```

**7. Open the dashboard**

Visit:

http://localhost:8501
