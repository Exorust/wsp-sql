```python
# Build a small set of custom prompts to see whether the model's thinking EVER terminates (and how the ending looks)
tiny_schema="CREATE TABLE city ( id INTEGER PRIMARY KEY, name TEXT, population INTEGER )"
p1="What is 2+2?"
p2=f"Database schema (SQLite):\n{tiny_schema}\nQuestion: How many cities are there?\nWrite one SQLite query that answers the question. Reply with the query in a {bt*3}sql code block."
p3="Write a Python function that returns the sum of two numbers."
p4=f"Database schema (SQLite):\n{tiny_schema}\nQuestion: What is the name of the city with the largest population?\nWrite one SQLite query that answers the question."
p5="Translate to French: 'The cat sleeps on the sofa.'"
p6=prompt_text('sp2265')
greq9={"type":"generate","model":"original","prompts":[p1,p2,p3,p4,p5,p6],"max_tokens":3000}
s9=json.dumps(greq9).replace(bt,'\\u0060'); print(s9)
```