# def insert_patient_data(name,age): # we are not doing type validation here
    
#     print(name)
#     print(age)
#     print("inserted into database")

# insert_patient_data("shiva",'eighteen')

def insert_patient_data(name:str,age:int): # fixed here but again error it doesnt show error
    if type(name)==str and type(age)==int:
        print(name)
        print(age)
        print("inserted")
    else:
        raise TypeError("incorrect")
insert_patient_data("shiva",-1999)    
    
def update(name:str,age:int): # fixed here but again error it doesnt show error
    if type(name)==str and type(age)==int:
        print(name)
        print(age)
        print("updated")
    else:
        raise TypeError("incorrect")
