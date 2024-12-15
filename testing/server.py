import flwr as fl
from model import create_model
from data import load_data

# Load test data for evaluation
_, (x_test, y_test) = load_data()

# Define server strategy
class FedAvgStrategy(fl.server.strategy.FedAvg):
    def evaluate(self, parameters, config):
        model = create_model()
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test)
        return loss, {"accuracy": accuracy}

# Start the server
if __name__ == "__main__":
    strategy = FedAvgStrategy()
    fl.server.start_server(strategy=strategy, num})
