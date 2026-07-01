# Serverless Event-Driven ETL Pipeline 🚀

## Project Overview
This project is a fully automated, serverless Data Engineering pipeline built on AWS. It extracts JSON data from three different public APIs (Earthquakes, Weather, and E-commerce Products), routes them through an S3 event-driven architecture, transforms the data using AWS Lambda, and loads the cleaned records into Amazon DynamoDB.

Additionally, the project features a fully configured CI/CD pipeline using GitHub Actions and AWS CodePipeline to ensure continuous integration and syntax validation upon every push to the `main` branch.

## Architecture & Workflow
1. **Extract (Mock/Fetch):** Data is sourced from the USGS Earthquake API, Open-Meteo API, and DummyJSON Products API.
2. **Trigger:** Raw `.json` files are uploaded to specific prefix folders in an Amazon S3 bucket (`raw/earthquakes/`, `raw/weather/`, `raw/products/`).
3. **Transform (AWS Lambda):** S3 ObjectCreated events automatically trigger specific Python Lambda functions based on the folder prefix.
4. **Load (Amazon DynamoDB):** The Lambdas clean the data, apply business logic, and insert the formatted items into highly scalable NoSQL DynamoDB tables.
5. **CI/CD:** AWS CodePipeline listens to the GitHub repository. On every commit, AWS CodeBuild executes a `buildspec.yml` file to validate all Python syntax before deployment.

---

## Reflection Questions

**1. Why use DynamoDB for this project instead of a relational database like RDS?**
DynamoDB was chosen because it is a fully managed, serverless NoSQL database that natively handles JSON document structures. Since the APIs (especially USGS GeoJSON) return highly nested and sometimes unpredictable schemas, a NoSQL structure allows for flexible schema-on-read. Additionally, DynamoDB's `PAY_PER_REQUEST` billing mode is incredibly cost-effective for an event-driven architecture with sporadic workloads, as there are no idle server costs.

**2. What are the Partition Keys for your tables and why?**
* **EarthquakeTable:** `event_id` (A unique string provided by the USGS API for every seismic event).
* **WeatherTable:** `reading_id` (A custom composite key generated using the prefix `wx-` combined with the Unix timestamp of the reading, ensuring every weather fetch is uniquely stored).
* **ProductTable:** `product_id` (The unique integer ID provided by the DummyJSON catalog).
These keys were chosen because they provide high cardinality, ensuring data is evenly distributed across DynamoDB's underlying storage partitions, preventing hot partitions.

**3. What specific transformation rules did your Lambda functions apply?**
* **Data Cleansing (Earthquake):** The function drops any event missing a valid magnitude or ID.
* **Derived Fields (Earthquake):** Calculated a new field called `alert_level`, tagging the event as "CRITICAL" if the magnitude was >= 5.0, and "NORMAL" otherwise.
* **Data Cleansing (Weather):** Rejects any JSON payload that is missing both temperature and windspeed metrics.
* **Derived Fields (Weather):** Created a `wind_status` field, tagging the entry as an "ADVISORY" if wind speeds exceed 15.0 km/h.
* **Transformations (Products):** Extracted the `price` and `discountPercentage`, and applied math to calculate a brand new `sale_price` derived field before pushing to the database.