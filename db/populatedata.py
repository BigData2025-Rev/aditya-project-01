# from db.session import session
import pandas as pd
import sys
import os
import random


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import Category
from model import Product
from db.base import Base, engine
from db.session import session as Db


def convert_rupees_to_usd(value):
    value = value.replace("₹", "")
    value = value.replace(",", "")
    return round(float(value)*0.012, 2)

if __name__=='__main__':
    import time
    start = time.time()
    print("Started at: %s" %start)
    directory_path = './db/archive/'
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    files_and_folders = os.listdir(directory_path)

    for i in range(10):
        ran = random.randint(1, len(files_and_folders))
        with open(directory_path+files_and_folders[ran], 'r') as file:
            data = pd.read_csv(file)

            list_cats = data['main_category'].unique()

            with Db() as session:
                for val in list_cats:
                    categ = session.query(Category).filter(Category.name==val).first()
                    if not categ:
                        new_category = Category(name=val)
                        session.add(new_category)
                        session.commit()
            
            with Db() as session:
                for id, row in data.iterrows():
                    if not type(row['actual_price']) == float and not type(row['no_of_ratings']) == float:
                        try:
                            no_ratings = float(row['no_of_ratings'])
                            rating = float(row['ratings'])
                            ctgry = session.query(Category).filter(Category.name==row['main_category']).first()
                            product = Product(name=row['name'], category_id=ctgry.id, image=row['image'], rating=rating, no_of_ratings=no_ratings, price=convert_rupees_to_usd(row['actual_price']), stock_quantity=random.randint(0, 50))
                            session.add(product)
                            session.commit()
                        except ValueError:
                            continue

    print("Stopped at: %s" %str(time.time()-start))
