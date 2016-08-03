#!/Users/dionhagan/anaconda/bin/python
from app import app
# app.run(debug=True)

# for development in c9.io - comment out later
import os
app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))