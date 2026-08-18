user={
    "name":"Tufail Ahmed",
    "age":20,
    "city":"Thane",
    "country":"India"
}

for key in user:
    print(key)
    
user["born"]="1999"
print(user)
    
for values in user:
    print(user[values])