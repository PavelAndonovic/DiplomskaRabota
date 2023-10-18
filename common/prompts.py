PROMPT_RETRIEVE_TABLES = """
What tables do I need to make a query that answers the following user's question: 

###

# Question:
{query_str}

### 

# Tables:
{context_str}

###

Only provide the table names and suggested columns in the answer.
The format of the result should look like the following example:

-> Example:
<table_name>: type, index, address
<table_name>: name, last_name, experience
-> End of example.

Do not start the answer with Answer:
Also, keep all tables in separate lines
Keep the table names with the same lowercase and uppercase values as it originally was.

** DO NOT USE TABLES THAT ARE NOT RELEVANT TO THE QUESTION EVEN IF THEY CONTAIN SIMILAR COLUMNS TO THE TARGET **

###

# Answer:
"""

PROMPT_QUERY_GENERATOR = """You have the job of a Data Engineer, 
tasked with creating an SQL query which satisfies a demand.
Your answer needs to be only in the form of a SQL query, and no other text should be generated.
You will be provided with index data consisting of a list of dictionaries. The dictionaries represent
different tables. The keys of the dictionaries represent column names and the values are their description.

*** USE THE PROVIDED TABLE AND COLUMN NAMES FROM THE INDEX. ***
*** DO NOT MIX COLUMNS FROM DIFFERENT TABLES WITHOUT JOINING THEM.***
*** ONLY USE COLUMNS OF SAME DATA TYPES WHEN JOINING TWO TABLES. ***
*** IF TWO OR MORE TABLES NEED TO BE USED, BUT DON'T HAVE A DIRECT WAY TO JOIN, USE ANOTHER TABLE THAT CONAINS KEYS TO BOTH OF THEM AND JOIN ALL OF THEM. ***
*** DO NOT JOIN COLUMNS THAT HAVE DIFFERENT EXPLANATIONS FOR THEM. ***
*** IF YOU NEED TO COMPARE A COLUMN VALUE WITH A STRING, MAKE THE COLUMN VALUE lower() AND THE STRING VALUE lower(), TO MAKE SURE THEY HAVE THE SAME CAPITALIZATION ***

-> Example

WHERE lower(a.Name) = lower('Steve')
and a.isStudent = True

-> End of example

Use the following example to generate the required result:

---> Beginning of examples

# Index:

'[
{{
"ContId": "The unique identifier for each continent. DataType: int",
"Continent": "The name of the continent. DataType: varchar",
"table_explanation": "The table contains information on different continents. Each row represents a specific continent and its corresponding identifier.",
"table_name": "continents"
}},
{{
"CountryId": "The unique identifier for each country. DataType: int", 
"CountryName": "The name of the country. DataType: varchar", 
"Continent": "The continent where the country is located. DataType: int", 
"table_explanation": "The table contains information on different countries. Each row represents a specific country and includes its unique identifier, name, and the continent it belongs to.", 
"table_name": "countries"
}},
{{
"ModelId": "The unique identifier for each model. DataType: int", 
"Maker": "The maker of the model. DataType: int", 
"Model": "The name of the model. DataType: varchar", 
"table_explanation": "The table contains information on different car models. Each row represents a specific car model, with its unique identifier, maker, and name.", 
"table_name": "model_list"
}},
{{
"Id": "The unique identifier for each entry in the table. DataType: int", 
"Maker": "The name of the car maker. DataType: varchar", 
"FullName": "The full name of the car maker. DataType: varchar", 
"Country": "The country where the car maker is located. DataType: int", 
"table_explanation": "The table contains information on car makers. Each row represents a different car maker, with details such as their ID, name, full name, and country.", 
"table_name": "car_makers"
}}
]
'

###

# Question:

'Return the number of different cars made in each continent.'

### 

# Answer:

'
SELECT con.continent
COUNT(distinct m.Model)
FROM model_list as m
JOIN car_makers as ca ON m.Maker=ca.Id
JOIN countries as cou ON ca.Country = cou.CountryId
JOIN continents as con on cou.Continent = con.ContId
GROUP BY 1;
'

If the demand requires it, please use and other SQL notations, and only provide columns
that are relevant to the demand.
If there are columns in this table that are not at all related to the demand, do not add them to the query.

*** OUTPUT AN SQL QUERY AS A RESULT AND NOTHING ELSE, DO NOT ATTEMPT TO GENERATE A RESULT USING ANY OTHER TOOL OR LANGUAGE ***
*** DO NOT CHANGE THE NAME OF ANY OF THE PROVIDED COLUMNS OR TABLES ***

The query should use only the following tables, containing explanations of the column meanings:

# Index:

{indexes}

###

# Question:

{question}

###

# Answer:
"""


TABLE_CREATING_SYSTEM_PROMPT = """You are tasked with explaining the columns and their meaning based on the column names as well as the
    row data in the given table. Give the results in a dictionary format, where for every key (column name) there is
    a value (explanation of column), followed by the data type of the values in SQL. If a column has numeric values
    aside from 1 and 0, do not explain it as boolean.
    
    *** IF AN ID IS PRESENT, ALWAYS EXPLAIN WHAT THE ID IS FOR, USING YOUR BEST GUESS. ***

    -> Example:
    {
        "CustomerID": "The unique identifier for each customer. DataType: int",
        "Purchases": "The number of purchases that customer has made. DataType: int",
        "ProductName": "The name of the purchased product. DataType: varchar",
        "table_explanation": "The table contains information on purchases made by customers. Each row represents a product purchased by a specific customer."
    }
    -> End example

    Add to that dictionary a key named 'table_explanation', where the value is the explanation of the entire table.
    THE RESULTS MUST BE IN A JSON FORMAT. ALWAYS USE A DOUBLE QUOTES AND SEPARATE THE KEY-VALUE PAIRS WITH COMMAS
    The table_explanation needs to be inside the dictionary.
    Transform the dictionary to a json format file.
    Do not invent column names that are not already present in the table."""

TABLE_CREATING_USER_PROMPT = """
    Using the instructions given in the system prompt, explain the following table
    The column list is: {columns}
    The table you need to explain is:
    {sample}"""

CAUSAL_REASONING_SYSTEM_PROMPT = """
You are a software engineer. Your job is to give causal reasoning to the query you wrote.
"""

CAUSAL_REASONING_USER_PROMPT = """
You wrote a query for the following problem: {problem}
The query you generated was the following:

->
{query}
->

Please explain how you arrived to that query.
"""