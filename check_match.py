from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["ecommerce_analysis"]

result = list(db.order_items.aggregate([
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
    {"$sort": {"total_revenue": -1}},
    {"$limit": 10}
]))

print("TOP 10 CATEGORIES BY REVENUE")

for item in result:
    print(item["_id"], ":", round(item["total_revenue"], 2))

print("Total categories found:", len(result))

client.close()