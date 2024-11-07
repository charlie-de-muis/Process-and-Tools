import psycopg2

from models.base import Base

class Clients(Base):
    def __init__(self):
        self.dbfile = "Cargohub_database"

    def get_client(self, client_id):
        print("hi")
        

    def add_client(self, client):
        client["created_at"] = self.get_timestamp()
        client["updated_at"] = self.get_timestamp()
        self.data.append(client)

    def update_client(self, client_id, client):
        client["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == client_id:
                self.data[i] = client
                break

    def remove_client(self, client_id):
        for x in self.data:
            if x["id"] == client_id:
                self.data.remove(x)

    def get_clients(self):
        print("hi")