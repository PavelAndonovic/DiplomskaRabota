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

*** USE THE PROVIDED TABLE AND COLUMN NAMES FROM THE INDEX.
DO NOT MIX COLUMNS FROM DIFFERENT TABLES WITHOUT JOINING THEM.**

Use the following example to generate the required result:

---> Beginning of examples

# Index:

'[
{{
    "CLASS_CODE": "The code representing the class. DataType: int",
    "STU_NUM": "The student number. DataType: int",
    "ENROLL_GRADE": "The grade the student received in the class. DataType: varchar",
    "table_explanation": "This table contains information about the enrollment of students in different classes.",
    "table_name": "ENROLL"
}},
{{
    "CLASS_CODE": "The unique identifier for each class. DataType: int",
    "CRS_CODE": "The code of the course associated with the class. DataType: varchar",
    "CLASS_SECTION": "The section number of the class. DataType: int",
    "CLASS_TIME": "The time schedule of the class. DataType: varchar",
    "CLASS_ROOM": "The room where the class takes place. DataType: varchar",
    "PROF_NUM": "The unique identifier for the professor teaching the class. DataType: int",
    "table_explanation": "This table contains information about different classes offered. Each row represents a class, with details such as class code, course code, section number, class time, class room, and professor number.",
    "table_name": "CLASS"
}}
]
'


###

# Question:

'Return the number of students taking the class with course code equal to "CS1".'

### 

# Answer:

'
SELECT COUNT(distinct e.STU_NUM)
FROM ENROLL as e
JOIN CLASS as c
ON e.CLASS_CODE=c.CLASS_CODE
WHERE c.CRS_CODE="CS1";
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

    -> Example:
    {
        "CustomerID": "The unique identifier for each customer. DataType: int",
        "Purchases": "The number of purchases that customer has made. DataType: int",
        "ProductName": "The name of the purchased product. DataType: varchar"
    }
    -> End example

    Add to that dictionary a key named 'table_explanation', where the value is the explanation of the entire table.
    The table_explanation needs to be inside the dictionary.
    Transform the dictionary to a json format file.
    Do not invent column names that are not already present in the table."""

TABLE_CREATING_USER_PROMPT = """
    Using the instructions given in the system prompt, explain the following table
    The column list is: {columns}
    The table you need to explain is:
    {sample}"""