from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
from bson import ObjectId
st.sidebar.title("Navigation")


uri = "mongodb+srv://admin:user123@cluster0.ntr7sqq.mongodb.net/?appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    db = client['StudentManagementSystemDB']
    collection = db['students']

    
    dic=[]
    # Initialize session_state keys if not present
    if "mode" not in st.session_state:
        st.session_state.mode = "show"  # can be "add" or "show"

    # Buttons to set the mode
    if st.sidebar.button("Add"):
        st.session_state.mode = "add"
    if st.sidebar.button("Show"):
        st.session_state.mode = "show"
    if st.sidebar.button("Delete"):
        st.session_state.mode = "Delete"
    if st.sidebar.button("Update"):
        st.session_state.mode="Update"

    # ✅ ADD DATA SECTION
    if st.session_state.mode == "add":
        with st.container():
            st.title("Enter Data")
            name = st.text_input("Enter Name : ")
            dept = st.text_input("Enter Department : ")
            if st.button("Submit"):
                if name and dept:
                    data = {"name": name.strip(), "dept": dept.strip()}
                    collection.insert_one(data)
                    st.success("✅ Data inserted successfully!")
                else:
                    st.warning("⚠️ Please fill in all fields before submitting.")

    # ✅ SHOW DATA SECTION
    elif st.session_state.mode == "show":
        with st.container():
            
            search = st.text_input("", placeholder="Search by name...")
            if search != "":
                for student in collection.find():
                    if search.lower() in student['name'].lower():
                        
                        dic.append(student)
            else:
                for student in collection.find():
                    
                    dic.append(student)

            if dic:
                st.dataframe(dic)
            else:
                st.info("No matching records found.")

    elif st.session_state.mode == "Delete":
        with st.container():
            del_id=st.text_input("",placeholder="Enter id to delete...")
            if st.button("Delete"):
                if del_id.strip()!="":
                    collection.delete_one({"_id":ObjectId(del_id)})
                    
                else:
                    st.warning("Please Enter Id")

    elif st.session_state.mode == "Update":
        with st.container():
            Update_id = st.text_input("", placeholder="Enter ID to update...")
            new_name = st.text_input("Enter new name:")
            new_dept = st.text_input("Enter new department:")

            if st.button("Update"):
                if Update_id.strip() != "":
                    collection.update_one({"_id": ObjectId(Update_id)}, {"$set": {"name": new_name, "dept": new_dept}})
                    st.success("✅ Data updated successfully!")

                else:
                    st.warning("Please enter a valid id to update.")




except Exception as e:
    st.error(f"❌ Error connecting to MongoDB: {e}")
