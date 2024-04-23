import streamlit as st
import mysql.connector

# Connect to MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="remote-host",
            port=accesible-port-number,
            user="username",
            password="pasword-databases",
            database="database-name"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Login Page
def login_page():
    st.title("Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        conn = connect_db()
        
        if conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            
            user = cursor.fetchone()
            
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
                
                st.experimental_rerun()

            else:
                st.error("Invalid username or password")
            
            cursor.close()
            conn.close()
        else:
            st.error("Failed to connect to database")

# Home Page with Data Insertion for Purchasing Survey
def home_page():
    st.title("Purchasing Survey - Data Insertion")
    
    name = st.text_input("Name", max_chars=50)
    age = st.number_input("Age", min_value=0, max_value=150)
    
    gender = st.selectbox("Gender", ["Male", "Female"])
    
    products = st.multiselect("Products you buy frequently", 
                              ["Electronics", "Clothing", "Groceries", "Books", "Healthcare"])
    
    feedback = st.text_area("Feedback", max_chars=500)
    
    if st.button("Submit Survey"):
        conn = connect_db()
        
        if conn:
            cursor = conn.cursor()
            
            # Convert products list to comma-separated string
            products_str = ', '.join(products)
            
            query = """
            INSERT INTO survey_data (name, age, gender, products, feedback) 
            VALUES (%s, %s, %s, %s, %s)
            """
            
            try:
                cursor.execute(query, (name, age, gender, products_str, feedback))
                conn.commit()
                st.success("Survey submitted successfully!")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            
            cursor.close()
            conn.close()
        else:
            st.error("Failed to connect to database")

# Main Function
def main():
    st.sidebar.title("Navigation")
    
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        page = st.sidebar.radio("Go to", ["Login"])
        
        if page == "Login":
            login_page()
    else:
        home_page()

if __name__ == "__main__":
    main()

