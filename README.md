# online-store

### Step1: Setup Virtual Environment
```
python -m venv .
```

### Step2: Install requirements.txt
```
source bin/activate
pip install -r requirements.txt
```

### Step3: Setup Database ( MYSQL with pymysql )
#### Also ensure db/base.py is setup correctly
#### Create db called ulmdb
```
export MYSQL_DB_PASS=<your-db-pass>
export JWT_SECRET=<your-jwt-secret>
```

### Step4: Populate Database.
#### Create a directory inside db called archive a.k.a ./db/archive
#### Copy csv files into archive. 
#### Expected columns: [name, image, actual_price, main_category, ratings, no_of_ratings]
```
python db/populatedate.py
```

### Step5: Create admin.
```
python createadmin.py
```

### Step6: Run Server.
```
python api/server.py
```

