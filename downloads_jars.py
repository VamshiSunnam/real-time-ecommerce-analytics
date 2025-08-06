import os
import urllib.request

# Create jars directory
os.makedirs("jars", exist_ok=True)

jars = [
    "https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.3.2/spark-sql-kafka-0-10_2.12-3.3.2.jar",
    "https://repo1.maven.org/maven2/org/postgresql/postgresql/42.5.0/postgresql-42.5.0.jar"
]

for jar_url in jars:
    filename = jar_url.split("/")[-1]
    filepath = f"jars/{filename}"
    if not os.path.exists(filepath):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(jar_url, filepath)
        print(f"✅ Downloaded {filename}")
    else:
        print(f"✅ {filename} already exists")

print("All JAR files ready!")