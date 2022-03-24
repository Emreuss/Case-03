import psycopg2 as db
from fastapi import FastAPI
import pandas as pd 


app = FastAPI()
conn_string="host=localhost dbname=yemeksepetidb user=postgres password=Pa55w.rd"
conn = db.connect(conn_string)
cur = conn.cursor()


restaurant_credit_score_df = pd.read_sql_query("""select *,(avg_service_point * 0.30 
               + avg_speed_point  * 0.30 + avg_flavor_point * 0.40 + extra_measuring + popularity_rate *0.60) :: numeric as credit_score 
from vw_restaurant_loan_support_report""", con=conn)


credit_info_dct=restaurant_credit_score_df.to_dict()



@app.get("/")
def  root():
    return {"Welcome my Rest API"}


@app.get("/restaurants")
def get_all_restaurant():
    return  credit_info_dct 


@app.get("/restaurants/{restaurant_id}")
def get_restaurant_credit_info(restaurant_id: int):

     return  credit_info_dct['restaurant_name'][restaurant_id] , credit_info_dct['credit_score'][restaurant_id]

