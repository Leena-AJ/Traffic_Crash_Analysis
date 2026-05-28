import streamlit as st
import pandas as pd
import pymysql

def get_connection():
    return pymysql.connect(
    host="localhost",               
    user="root",            
    password="Aro788n4",              
    database="traffic_crash"  
    )

def execute_query(query):
    conn = get_connection()
    df = pd.read_sql(query,conn)
    conn.close()
    return df

st.title("Traffic Crash Analytics And Safety Intelligence Platform")
st.header("MySQL Query Selector")



queries = {
"Top 5 most dangerous combinations of weather and crash type": """
SELECT WEATHER_CONDITION,CRASH_TYPE,SUM(INJURIES_TOTAL) AS TOTAL_INJURIES 
FROM traffic_crash_data
GROUP BY WEATHER_CONDITION,CRASH_TYPE
ORDER BY TOTAL_INJURIES DESC
LIMIT 5
;
""",

"Top 10 streets with the highest number of injury crashes": """
SELECT STREET_NAME ,COUNT(*) AS TOTAL_INJURIES
FROM traffic_crash_data
WHERE INJURIES_TOTAL > 0
GROUP BY STREET_NAME
ORDER BY TOTAL_INJURIES DESC
LIMIT 10
;
""",

"Percentage of crashes that resulted in injuries for each crash type": """
SELECT CRASH_TYPE,COUNT(*) AS TOTAL ,COUNT(*) *100.0 / 
(SELECT COUNT(*) FROM traffic_crash_data) AS PERCENTAGE
FROM traffic_crash_data
GROUP BY CRASH_TYPE
ORDER BY PERCENTAGE
;
""",

"Peak crash hour for each month": """
SELECT CRASH_MONTH,CRASH_HOUR,TOTAL_CRASHES
FROM
(
SELECT CRASH_MONTH,CRASH_HOUR,COUNT(*) AS TOTAL_CRASHES,
RANK() OVER ( PARTITION BY CRASH_MONTH ORDER BY COUNT(*) DESC ) AS r
FROM traffic_crash_data
GROUP BY CRASH_MONTH,CRASH_HOUR
)peak_hours
WHERE r = 1;
""",
      
"Top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18)":"""
SELECT PRIM_CONTRIBUTORY_CAUSE,COUNT(*) AS TOTAL_CRASHES
FROM traffic_crash_data
WHERE CRASH_HOUR >= 18 
GROUP BY PRIM_CONTRIBUTORY_CAUSE
ORDER BY TOTAL_CRASHES DESC
LIMIT 5
;
""",

"Average number of injuries in daylight vs darkness conditions":"""
SELECT LIGHTING_CONDITION,avg(INJURIES_TOTAL) AS AVG_NO_OF_INJURIES
FROM traffic_crash_data
WHERE LIGHTING_CONDITION IN ('DAYLIGHT' , 'DARKNESS')
GROUP BY LIGHTING_CONDITION;
""",

"Traffic control device type has the highest average injuries per crash":"""
SELECT TRAFFIC_CONTROL_DEVICE,avg(INJURIES_TOTAL) AS AVG_NO_OF_INJURIES
FROM traffic_crash_data
GROUP BY TRAFFIC_CONTROL_DEVICE
ORDER BY AVG_NO_OF_INJURIES DESC ;
""",

"Top 5 locations (latitude/longitude) with the highest crash frequency":"""
SELECT LOCATION, COUNT(*) AS TOTAL_CRASHES
FROM traffic_crash_data
GROUP BY LOCATION
ORDER BY TOTAL_CRASHES DESC
LIMIT 5 ;
""",

"Top 5 streets with the highest injury rate, considering only streets with more than 100 crashes":"""
SELECT STREET_NAME,AVG(INJURIES_TOTAL) AS INJURY_RATE,COUNT(*) AS TOTAL_CRASHES
FROM traffic_crash_data
GROUP BY STREET_NAME
HAVING TOTAL_CRASHES > 100
ORDER BY INJURY_RATE DESC
LIMIT 5 ;
""",

"For each year, identify the most common crash type":"""
SELECT year,CRASH_TYPE,TOTAL_CRASHES
FROM
(
SELECT year,CRASH_TYPE,COUNT(*) AS TOTAL_CRASHES,
RANK() OVER ( PARTITION BY year ORDER BY COUNT(*) DESC ) AS r
FROM traffic_crash_data
GROUP BY year,CRASH_TYPE
)common_crash
WHERE r = 1;
""",

"Day of the week with the highest average crashes per hour":"""
SELECT CRASH_DAY_OF_WEEK,COUNT(*)/24.0 AS CRASH_PER_HOUR
FROM traffic_crash_data
GROUP BY  CRASH_DAY_OF_WEEK
ORDER BY CRASH_PER_HOUR DESC;
""",

"Identify high-risk time slots":"""
SELECT 
CASE 
WHEN CRASH_HOUR between 6 AND 11
THEN 'MORNING'
WHEN CRASH_HOUR between 12 AND 17
THEN 'AFTERNOON'
WHEN CRASH_HOUR between 17 AND 21
THEN 'EVENING'
ELSE 'NIGHT'
END AS CRASH_HOUR_BUCKET,
COUNT(*) AS TOTAL_CRASHES
FROM traffic_crash_data
GROUP BY CRASH_HOUR_BUCKET
ORDER BY TOTAL_CRASHES DESC;
""",

"Top 3 contributing causes for each crash type":"""
SELECT  * FROM
(
SELECT CRASH_TYPE,PRIM_CONTRIBUTORY_CAUSE,COUNT(*) AS TOTAL_CRASHES,
                       
RANK() OVER ( PARTITION BY CRASH_TYPE
ORDER BY COUNT(*) DESC
) 
AS CRASH_RANK
FROM traffic_crash_data
GROUP BY CRASH_TYPE, PRIM_CONTRIBUTORY_CAUSE) RESULT
WHERE CRASH_RANK <=3;
""",

"Year-over-year growth rate of crashes":"""
SELECT year,total_crashes,
LAG(total_crashes) OVER (ORDER BY year) AS PREV_YEAR_CRASHES,
ROUND(
  ( (total_crashes - LAG(total_crashes) OVER (ORDER BY year) )* 100  )/ LAG(total_crashes) OVER (ORDER BY year),
  2 ) AS GROWTH_RATE
FROM
(SELECT year,COUNT(*) as total_crashes
FROM traffic_crash_data
GROUP BY year)crashes_by_year;
""",

"Find top 10 zones with highest crashes":"""
SELECT 
ROUND(LATITUDE,2) AS LATITUDE_ZONE,
ROUND(LONGITUDE,2) AS LONGITUDE_ZONE,
COUNT(*) AS TOTAL_CRASHES
FROM traffic_crash_data
WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL
GROUP BY ROUND(LATITUDE,2) , ROUND(LONGITUDE,2) 
ORDER BY TOTAL_CRASHES DESC
LIMIT 10;
"""
}


selected_query = st.selectbox("Select a query:",list(queries.keys()))

if st.button("Run Query"):
    with st.spinner("Fetching Data..."):
         df = execute_query(queries[selected_query])
         st.success("Query executed successfully")
         st.dataframe(df)

         if selected_query =="Top 5 most dangerous combinations of weather and crash type":
             st.info("Clear weather and No Injury crash occur frequently")

         elif selected_query =="Top 10 streets with the highest number of injury crashes":
             st.info("Western Ave has recorded first place in higher injury crashes")

         elif selected_query =="Percentage of crashes that resulted in injuries for each crash type":
             st.info("70 percent of crashes are no injury type remaining 30 percent result in injury")

         elif selected_query =="Peak crash hour for each month":
             st.info("More crashes occur between 3pm to 5pm")

         elif selected_query =="Top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18)":
             st.info("Unable to determine is the top cause for most crashes")
   
         elif selected_query =="Average number of injuries in daylight vs darkness conditions":
             st.info("Average crashes are slightly higher in darkness compared to daylight")

         elif selected_query =="Traffic control device type has the highest average injuries per crash":
             st.info("Bicycle crossing sign and pedestrian crossing sign are the top two traffic control device which has recorded highest average injuries")
    
         elif selected_query =="Top 5 locations (latitude/longitude) with the highest crash frequency":
             st.info(" ")
    
         elif selected_query =="Top 5 streets with the highest injury rate, considering only streets with more than 100 crashes":
             st.info(" ")
    
         elif selected_query =="For each year, identify the most common crash type":
             st.info("No Injury/Drive away is the common crash type for all the years")
    
         elif selected_query =="Day of the week with the highest average crashes per hour":
             st.info("Average crashes per hour are high on Friday")

         elif selected_query =="Identify high-risk time slots":
             st.info("Crashes are more in afternoon and lesser during night")

         elif selected_query =="Top 3 contributing causes for each crash type":
             st.info("Unable to determine and Failing to yield right way are the two common causes for both the crash type")

         elif selected_query =="Year-over-year growth rate of crashes":
             st.info("Growth rate is very high in the year 2021 compared to all the other years")

         elif selected_query =="Find top 10 zones with highest crashes":
             st.info(" ")