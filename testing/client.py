import flwr as fl
from model import create_model
from data import load_data, split_data
import sys

def main(client_id, num_clients):
    # Load and split data
    (x_train, y_train), _ = load_data()
    client_data, client_labels = split_data(x_train, y_train, num_clients)
    
    # Create client model
    model = create_model()

    # Define Flower client
    class FLClient(fl.client.NumPyClient):
        def get_parameters(self):
            return model.get_weights()

        def set_parameters(self, parameters):
            model.set_weights(parameters)

        def fit(self, parameters, config):
            self.set_parameters(parameters)
            model.fit(client_data[int(client_id)], client_labels[int(client_id)], epochs=1, batch_size=32)
            return self.get_parameters(), len(client_data[int(client_id)]), {}

        def evaluate(self, parameters, config):
            self.set_parameters(parameters)
            loss, accuracy = model.evaluate(client_data[int(client_id)], client_labels[int(client_id)])
            return loss, len(client_data[int(client_id)]), {"accuracy": accuracy}

    # Start client
    fl.client.start_numpy_client(server_address="127.0.0.1:8080", client=FLClient())

if __name__ == "__main__":
    client_id = sys.argv[1]
    num_clients = int(sys.argv[2])
    main(client_id, num_clients)
