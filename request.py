
    
import requests

# URL
url = 'https://fathomless-thicket-49759.herokuapp.com//api'

# Change the value of experience that you want to test
r = requests.post(url, json={'url':'www.gooogle.com', })
print(r.json())
