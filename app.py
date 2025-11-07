from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st

st.title("Enter Data")

name = st.text_input("Enter Name : ")

dept = st.text_input("Enter Department : ")

# MongoDB connection URI
uri = "mongodb+srv://admin:user123@cluster0.ntr7sqq.mongodb.net/?appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    db = client['StudentManagementSystemDB']
    collection = db['students']

    # ✅ Insert data
    if st.button("Submit"):
        if name and dept:
            data = {"name": name.strip(), "dept": dept.strip()}
            collection.insert_one(data)
            st.success("✅ Data inserted successfully!")
        else:
            st.warning("⚠️ Please fill in all fields before submitting.")

    # ✅ Search and Display Data
    dic = []

    search = st.text_input("", placeholder="Search by name...")
    if search != "":
        for student in collection.find():
            if search in student['name']:
                student.pop('_id', None)
                dic.append(student)
     
    else:
        for student in collection.find():
            student.pop('_id', None)
            dic.append(student)
    st.table(dic)

    # Optional: print to console for debugging
    print("📄 Documents in 'students' collection:")
    for doc in collection.find():
        print(doc)

except Exception as e:
    st.error(f"❌ Error connecting to MongoDB: {e}")
