import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

connection = sqlite3.connect(r"D:/Guvi Projects/fwms.db")
cursor = connection.cursor()


st.sidebar.header("Project Content Navigation")
options = ["Project Introduction", "Filter Food Donations", "Contact Food Provider", "CRUD Operations", "Execute Queries"]
choice = st.sidebar.radio("Select an Option:", options)

#Project Introduction
if choice == "Project Introduction":
    st.title("Food Waste Management System")
    st.image("D:/Guvi Projects/9969525.jpg")
    st.write("The **Food Waste Management System (FWMS)** connects food providers with surplus supply to receivers in need, including NGOs assisting vulnerable populations. It facilitates food listings by providers, allowing receivers to claim based on type, location, and availability. This system reduces food waste while ensuring that edible food reaches those facing food insecurity. Users can filter donations, contact providers, and track distribution. FWMS fosters a sustainable food redistribution network, maximizing community support and minimizing waste.")
    st.image("D:/Guvi Projects/medium-shot-volunteers-with-food-packs.jpg")


# Filter food donations
elif choice == "Filter Food Donations":
    st.header("Filter Food Donations based on following options")

    location_options = [row[0] for row in cursor.execute("SELECT DISTINCT Location FROM 'food_listing'").fetchall()]
    provider_options = [row[0] for row in cursor.execute("SELECT DISTINCT Name FROM Providers").fetchall()]
    food_type_options = [row[0] for row in cursor.execute("SELECT DISTINCT Food_Type FROM 'food_listing'").fetchall()]

    Location = st.selectbox("Location", ["All"] + location_options)
    Provider = st.selectbox("Provider", ["All"] + provider_options)
    Food_Type = st.selectbox("Food Type", ["All"] + food_type_options)

    query = '''
        SELECT fl.Food_ID, fl.Food_Name, fl.Food_Type, fl.Quantity, fl.Location, p.Name, p.Contact
        FROM 'food_listing' fl 
        LEFT JOIN providers p ON fl.Provider_ID = p.Provider_ID
        WHERE 1=1
        '''

    if Location != "All":
        query += " AND fl.Location = ?"
    if Provider != "All":
        query += " AND p.Name = ?"
    if Food_Type != "All":
        query += " AND fl.Food_Type = ?"

    params = []
    if Location != "All": params.append(Location)
    if Provider != "All": params.append(Provider)
    if Food_Type != "All": params.append(Food_Type)

    food_listing = pd.read_sql(query, connection, params=params)
    st.dataframe(food_listing)


#Contacting provider
elif choice == "Contact Food Provider":
    st.header("Food Provider's Contact Details:")

    provider_query = cursor.execute("SELECT DISTINCT Name FROM Providers").fetchall()
    provider_names = [row[0] for row in provider_query]
    selected_provider = st.selectbox("Select a Provider", ["Select"] + provider_names)

    if selected_provider != "Select":
        provider_data = cursor.execute("SELECT Contact FROM Providers WHERE Name = ?", (selected_provider,)).fetchone()

        if provider_data:
            st.success(f"Contact provider at: {provider_data[0]}")

            if st.button("Click to call"):
                st.write("Calling The Provider...")

# CRUD 
elif choice == "CRUD Operations":
    action = st.selectbox("Select Action", ["Select", "Add", "Update", "Delete"])
    if action != "Select":
        table = st.selectbox("Select Table", ["providers", "receivers", "food_listing", "claims"])
        #Add
        if action == "Add":
            with st.form(f"add_form_{table.lower()}"):
                if table == "providers":
                    Provider_ID = st.number_input("Provider_ID", step = 1)
                    name = st.text_input("Provider_Name")
                    Type = st.text_input("Provider_type")
                    Address = st.text_area("Address")
                    City = st.text_input("City")
                    contact = st.text_input("Contact")
                    submitted = st.form_submit_button("Add Provider")
                    if submitted and Provider_ID and name and Type and Address and City and contact:
                        cursor.execute("INSERT INTO providers (Provider_ID, Name, Type, Address, City, Contact) VALUES (?, ?, ?, ?, ?, ?)", (Provider_ID, name, Type, Address, City, contact))
                        connection.commit()
                        st.success("Provider added successfully")
            
                elif table == "receivers":
                    Receiver_ID = st.number_input("Receiver_ID", step = 1)
                    Name = st.text_input("Receiver_Name")
                    Type = st.text_input("Receiver_Type")
                    City = st.text_input("City")
                    contact = st.text_input("Contact")
                    submitted = st.form_submit_button("Add Receiver")
                    if submitted and Receiver_ID and Name and Type and City and contact:
                        cursor.execute("INSERT INTO receivers (Receiver_ID, Name, Type, City, Contact) VALUES (?, ?, ?, ?, ?)", (Receiver_ID, Name, Type, City, contact))
                        connection.commit()
                        st.success("Receiver added successfully")
            
                elif table == "food_listing":
                    Food_ID = st.number_input("Food_ID", step = 1)
                    Food_Name = st.text_input("Food_Name")
                    Quantity = st.number_input("Quantity", step = 1)
                    Location = st.text_input("Location")
                    Food_Type = st.text_input("Food_Type")
                    Meal_Type = st.text_input("Meal_Type")
                    submitted = st.form_submit_button("Add Food details")
                    if submitted and Food_ID and Food_Name and Quantity and Location and Food_Type and Meal_Type:
                        cursor.execute("INSERT INTO food_listing(Food_ID, Food_Name, Quantity, Location, Food_Type, Meal_Type) VALUES (?, ?, ?, ?, ?, ?)", (Food_ID, Food_Name, Quantity, Location, Food_Type, Meal_Type))
                        connection.commit()
                        st.success("Food details added successfully")
            
                elif table == "claims":
                    Claim_ID = st.number_input("Claim_ID")
                    Status = st.text_input("Status")
                    submitted = st.form_submit_button("Add claims")
                    if submitted and Claim_ID and Status:
                        cursor.execute("INSERT INTO claims (Claim_ID, Status) VALUES (?, ?)", (Claim_ID, Status))
                        connection.commit()
                        st.success("Claims added successfully")

        # Update
        elif action == "Update":
            if table == "food_listing":
                new_Meal_type = st.text_input("New Meal Type")
                new_quantity = st.number_input("New Quantity", step=1)
                new_location = st.text_input("New Location")
                Food_ID = st.number_input("Food_ID", step = 1)
                if st.button("Update Listing"):
                    cursor.execute("UPDATE 'food_listing' SET Meal_Type = ?, Quantity = ?, Location = ? WHERE Food_ID = ?", (new_Meal_type, new_quantity, new_location, Food_ID))
                    connection.commit()
                    st.success("Listing updated successfully")
        

            elif table == "providers":
                New_Name = st.text_input("Name")
                New_Type = st.text_input("Type")
                New_Address = st.text_area("Address")
                New_City = st.text_input("City")
                New_Contact = st.text_input("Contact")
                Provider_ID = st.number_input("Provider_ID", step = 1)
                if st.button("Update Providers list"):
                    cursor.execute("UPDATE 'providers' SET Name = ?, Type = ?, Address = ?, City = ?, Contact = ? WHERE Provider_ID = ?", (New_Name,New_Type, New_Address, New_City, New_Contact, Provider_ID))
                    connection.commit()
                    st.success("Provider updated successfully")

            elif table == "receivers":
                New_Name = st.text_input("Name")
                New_Type = st.text_input("Type")
                New_City = st.text_input("City")
                New_Contact = st.text_input("Contact")
                Receiver_ID = st.number_input("Receiver_ID", step = 1)
                if st.button("Update Receiver list"):
                    cursor.execute("UPDATE 'receivers' SET Name = ?, Type = ?, City = ?, Contact = ? WHERE Receiver_ID = ?", (New_Name,New_Type, New_City, New_Contact, Receiver_ID))
                    connection.commit()
                    st.success("Receiver updated successfully")

            elif table == 'claims':
                New_Status = st.text_input("Status")
                Claim_ID = st.number_input("Claim_ID", step = 1)
                if st.button("Update claims"):
                    cursor.execute("UPDATE 'claims' SET Status = ? WHERE Claim_ID = ?", (New_Status, Claim_ID))
                    connection.commit()
                    st.success("Claim status updated successfully")
                

        # Delete
        elif action == "Delete":
            if table == "receivers":
                Receiver_ID = st.number_input("Enter Receiver ID to Delete", step=1)
                if st.button("Delete Record"):
                    cursor.execute(f"DELETE FROM '{table}' WHERE Receiver_ID = ?", (Receiver_ID,))
                    connection.commit()
                    st.success("Record deleted successfully")

            elif table == "providers":
                Provider_ID = st.number_input("Enter Provider ID to Delete", step = 1)
                if st.button("Delete Record"):
                    cursor.execute(f"DELETE FROM '{table}' WHERE Provider_ID = ?", (Provider_ID))
                    connection.commit()
                    st.success("Record deleted successfully")         
 
            elif table == "food_listing":
                Food_ID = st.number_input("Enter Food ID to Delete", step = 1)
                if st.button("Delete Record"):
                    cursor.execute(f"DELETE FROM '{table}' WHERE Food_ID = ?", (Food_ID))
                    connection.commit()
                    st.success("Record deleted successfully")

            elif table == "claims":
                Claim_ID = st.number_input("Enter Provider ID to Delete", step = 1)
                if st.button("Delete Record"):
                    cursor.execute(f"DELETE FROM '{table}' WHERE Claim_ID = ?", (Claim_ID))
                    connection.commit()
                    st.success("Record deleted successfully")

# Queries 
elif choice == "Execute Queries":
    st.header("Listed Queries")
    queries = {
        '1.How many food providers and receivers are there in each city?': """ SELECT 
        p.City AS City, 
        COUNT(DISTINCT p.Provider_ID) AS Number_of_Providers, 
        COUNT(DISTINCT r.Receiver_ID) AS Number_of_Receivers
        FROM 
            providers p
        LEFT JOIN 
            receivers r ON p.City = r.City
        GROUP BY 
            p.City;""",
           
        '2.Which type of food provider (restaurant, grocery store, etc.) contributes the most food?': """
        SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
        FROM food_listing
        GROUP BY Provider_Type
        ORDER BY Total_Quantity DESC
        LIMIT 1; """,
        '3.What is the contact information of food providers in a specific city?': """
        SELECT Name, Contact
        FROM Providers
        WHERE City = ?; """, 
        '4.Which receivers have claimed the most food?':  """ 
        SELECT r.Name, r.Receiver_ID, COUNT(c.claim_ID) AS Total_Claims
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY c.Receiver_ID
        ORDER BY Total_Claims DESC
        LIMIT 1; """ , 
        '5.What is the total quantity of food available from all providers?': """
        SELECT SUM(Quantity) AS Total_Quantity
        FROM food_listing; """ , 
        '6.Which city has the highest number of food listings?': """
        SELECT Location, COUNT(*) AS Listings_Count
        FROM food_listing
        GROUP BY Location
        ORDER BY Listings_Count DESC
        LIMIT 1; """, 
        '7.What are the most commonly available food types?': """ SELECT Food_Type, COUNT(*) AS Count
        FROM food_listing
        GROUP BY Food_Type
        ORDER BY Count DESC;""" , 
        '8.How many food claims have been made for each food item?': """ SELECT  f.Food_Name, 
        f.Food_ID, 
        COUNT(c.Claim_ID) AS Total_Claims
        FROM 
            claims c
        JOIN 
            food_listing f ON c.Food_ID = f.Food_ID
        GROUP BY 
            c.Food_ID
        ORDER BY 
            Total_Claims DESC;""", 
        '9.Which provider has had the highest number of successful food claims?': """ SELECT 
        p.Name AS Provider_Name,
        p.Provider_ID,
        COUNT(c.Claim_ID) AS Successful_Claims
        FROM claims C
        JOIN food_listing f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Provider_ID
        ORDER BY Successful_claims DESC
        LIMIT 1;""" , 
        '10.What percentage of food claims are completed vs. pending vs. canceled?' : """ SELECT Status,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS Percentage
        FROM claims 
        GROUP BY Status;""" , 
        '11.What is the average quantity of food claimed per receiver?': """ SELECT c.Receiver_ID, r.Name,
        AVG(f.Quantity) AS Avg_Food_Claimed_Quantity
        FROM claims c
        JOIN food_listing f ON c.Food_ID = f.Food_ID
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY c.Receiver_ID
        ORDER BY Avg_Food_Claimed_Quantity DESC;""",
        '12. Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?': """ SELECT f.Meal_Type,
        COUNT(*) AS Total_Claims
        FROM claims c
        JOIN food_listing f ON c.Food_ID = f.Food_ID
        GROUP BY f.Meal_Type
        ORDER BY Total_Claims DESC
        LIMIT 1; """,
        '13.What is the total quantity of food donated by each provider?': """  SELECT 
        p.Provider_ID, p.Name,
        SUM(f.Quantity) AS Total_Donated
        FROM food_listing f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Provider_ID
        ORDER BY Total_Donated DESC;""" ,
        '14.Which provider has had the highest number of failured food claims?': """ SELECT 
        p.Name AS Provider_Name,
        p.Provider_ID,
        COUNT(c.Claim_ID) AS Unsuccessful_Claims
        FROM claims C
        JOIN food_listing f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Cancelled'
        GROUP BY p.Provider_ID
        ORDER BY Unsuccessful_claims DESC
        LIMIT 1; """, 
        '15.What are all the foods grocery can supply?': """ SELECT DISTINCT f.Food_Name
        FROM food_listing f
        WHERE f.Provider_Type = "Grocery Store";""" , 
        '16.What is the total quantity of food available in each city?': """ SELECT f.Location AS City,
        SUM(f.Quantity) AS Total_Quantity
        FROM food_listing f
        GROUP BY f.Location
        ORDER BY Total_Quantity DESC;""", 
        '17.How many pending claims are there for each city?': """ SELECT f.Location AS City,
        COUNT(c.Claim_ID) AS Pending_claims
        FROM claims c
        JOIN food_listing f ON c.Food_ID = f.Food_ID
        WHERE Status = 'Pending'
        GROUP BY f.Location
        ORDER BY Pending_claims DESC;""",
        '18.What types of food are supplied by each provider?': """ SELECT DISTINCT f.Food_Type AS Type,
        p.Name AS Provider_name
        FROM food_listing f
        JOIN providers p ON p.Provider_ID = f.Provider_ID
        ORDER BY p.Provider_ID DESC; """,
        '19.Which receivers have claimed both veg and non-veg foods?': """SELECT c.Receiver_ID, r.Name
        FROM claims c
            JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
            JOIN food_listing f ON c.Food_ID = f.Food_ID
        GROUP BY c.Receiver_ID, r.Name
        HAVING
            SUM(CASE WHEN f.Food_Type = 'Vegetarian' THEN 1 ELSE 0 END) >0
            AND
            SUM(CASE WHEN f.Food_Type = 'Non-Vegetarian' THEN 1 ELSE 0 END) >0; """,
        '20.Which receiver has claimed the most breakfast items?': """ SELECT c.Receiver_ID, r.Name,
        COUNT(c.Claim_ID) AS Breakfast_claims
        FROM claims c
            JOIN food_listing f ON c.Food_ID = f.Food_ID
            JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        WHERE f.Meal_Type = 'Breakfast'
        GROUP BY c.Receiver_ID, r.Name
        ORDER BY Breakfast_claims DESC
        LIMIT 1;""" , 
        '21.What are the top 5 commonly claimed food items across all receivers?': """SELECT f.Food_Name, 
        COUNT(c.Claim_ID) AS Claim_Count
        FROM claims c
            JOIN food_listing f ON c.Food_ID = f.Food_ID
        GROUP BY 
            f.Food_ID, f.Food_Name
        ORDER BY 
            Claim_Count DESC
        LIMIT 5; """,
        '22.Which type of receiver is more in quantity?': """SELECT r.Type AS Receiver_Type,
        COUNT(r.Receiver_ID) AS Receiver_Count
        FROM receivers r
        GROUP BY r.Type
        ORDER BY Receiver_Count DESC
        LIMIT 1;""", 
        '23.What is the total quantity of food claimed by NGO?': """SELECT 
        SUM(f.Quantity) AS Total_Quantity_Claimed
        FROM 
            claims c
            JOIN food_listing f ON c.Food_ID = f.Food_ID
            JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        WHERE 
            r.Type = 'NGO';"""
        }

    query_options = list(queries.keys())
    selected_query = st.selectbox("Select a Query", ["Select"] + query_options)

    if selected_query != "Select":
        query = queries[selected_query]
        result = pd.read_sql(query, connection)
        st.dataframe(result)

connection.commit()
connection.close()
