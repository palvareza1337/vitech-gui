class area:
    name = ""
    id = ""

    def __init__(self, name, id):
        self.name = name
        self.id = int(id)

    def __str__(self):
        return self.name
    
    def __int__(self):
        return self.id


test = area("god", "0")

print(test)
print(int(test))