from random import uniform
import numpy as np
from constants import MUTATION_RATE, NUM_OUTPUT_NEURONS, HIDDEN_LAYERS, NUM_INPUT_NEURONS


class Brain:
    """
    Represents the brain of a creature, which includes a neural network.

    Attributes:
        num_inputs (int): The number of input neurons in the neural network.
        num_hidden (int): The number of hidden neurons in the neural network.
        num_outputs (int): The number of output neurons in the neural network.
        activation_func (callable): The activation function used by the neurons.
    """

    def __init__(self, num_inputs, hidden_layers, num_outputs):
        self.num_inputs = num_inputs
        self.hidden_layers = hidden_layers
        self.num_outputs = num_outputs
        self.activation_function = self.sigmoid
        self.input_hidden_weights = []
        self.hidden_hidden_weights = []
        self.hidden_output_weights = []
        self.output_values = []
    

    def initialize_weights(self):
        self.input_hidden_weights = []
        self.hidden_hidden_weights = []
        num_hidden_layers = len(self.hidden_layers)

        # Initialize weights for the input to first hidden layer
        input_hidden_layer_weights = np.random.rand(self.num_inputs, self.hidden_layers[0])
        self.input_hidden_weights.append(input_hidden_layer_weights)

        # Initialize weights for the hidden layers
        for i in range(num_hidden_layers - 1):
            hidden_layer_weights = np.random.rand(self.hidden_layers[i], self.hidden_layers[i + 1])
            self.hidden_hidden_weights.append(hidden_layer_weights)

        # Initialize weights for the last hidden layer to output layer
        hidden_output_weights = np.random.rand(self.hidden_layers[-1], self.num_outputs)
        self.hidden_output_weights = hidden_output_weights


    def set_inputs(self, input_values):
        """
        Sets the input values for the neural network.

        Parameters:
            input_values (list): A list of input values representing the creature's environment and state.
                The values should be provided in the following order:
                    - Index 0 corresponds to closest_plant_distance: the distance from the closest plant.
                    - Index 1 corresponds to angle_from_closest_plant: the angle between the creature and the closest plant.
                    - Index 2 corresponds to can_reproduce: a boolean value indicating if the creature can reproduce.
                    - Index 3 corresponds to screen_edge_distance: the distance from the edge of the screen.
                    - Index 4 corresponds to can_move_forward: a boolean value indicating if the creature can move forward.
                    - Index 5 corresponds to energy_level: the current energy level of the creature.
                             
                    The number of input values should match the number of input neurons in the neural network.

        Raises:
            ValueError: If the number of input values does not match the number of input neurons.

        """
        if len(input_values) != self.num_inputs:
            raise ValueError("Number of input values does not match the number of input neurons.")

        self.input_values = np.array(input_values)


    def forward_propagation(self):
        # Clear the output values list
        self.output_values = []

        # Compute the output values for the input layer
        self.output_values.append(self.input_values)

        # Iterate over each hidden layer
        for i in range(len(self.hidden_layers)):
            # Compute the weighted sum of inputs for each neuron in the current hidden layer
            if i == 0:
                weighted_sums_hidden = np.dot(self.output_values[i], self.input_hidden_weights[i])
            else:
                weighted_sums_hidden = np.dot(self.output_values[i], self.hidden_hidden_weights[i - 1])

            # Apply the activation function to obtain the output values of the current hidden layer
            hidden_outputs = self.activation_function(weighted_sums_hidden)

            # Append the output values of the current hidden layer to the output values list
            self.output_values.append(hidden_outputs)

        # Compute the weighted sum of inputs for each neuron in the output layer
        weighted_sums_output = np.dot(self.output_values[-1], self.hidden_output_weights)

        # Apply the activation function to obtain the output values of the output layer
        output_outputs = self.activation_function(weighted_sums_output)

        # Append the output values of the output layer to the output values list
        self.output_values.append(output_outputs)


    @staticmethod
    def sigmoid(x):
        """
        Computes the sigmoid activation function for a given input.

        Args:
            x: The input value.

        Returns:
            The output value after applying the sigmoid function.
        """
        try:
            return 1 / (1 + np.exp(-x))
        except RuntimeWarning:
            return 0


    def mutate_weights(self):
        # Mutate input-hidden layer weights
        mask = np.random.rand(*self.input_hidden_weights[0].shape) < MUTATION_RATE
        self.input_hidden_weights[0] += np.random.normal(0, 0.1, self.input_hidden_weights[0].shape) * mask

        # Mutate hidden-hidden layer weights
        for hidden_weights in self.hidden_hidden_weights:
            mask = np.random.rand(*hidden_weights.shape) < MUTATION_RATE
            hidden_weights += np.random.normal(0, 0.1, hidden_weights.shape) * mask

        # Mutate hidden-output layer weights
        mask = np.random.rand(*self.hidden_output_weights.shape) < MUTATION_RATE
        self.hidden_output_weights += np.random.normal(0, 0.1, self.hidden_output_weights.shape) * mask


    def choose_action(self):
        """
        Choose and perform an action based on the output values of the neural network.

        This function selects the action with the highest output value among the available actions.
        If multiple actions have the same highest value, the first one encountered will be chosen.

        The available actions are defined in the `actions` dictionary, where the keys represent
        the action indices and the values are the corresponding action functions.

        Note that the actions dictionary should be updated if additional actions are added in the future.

        Returns:
            None
        """
        actions = {
            0: "move",
            1: "turn",
            2: "reproduce"
            # Add more actions here in the future if needed
        }
        
        # Find the action index with the highest output value
        max_action = max(actions, key=lambda x: self.output_values[-1][x])
        
        # Call the corresponding action function
        return actions[max_action]


    def decide_action(self):
        self.forward_propagation()
        action = self.choose_action()

        if action == "reproduce":
            value = 1
        elif action == "move":
            value = self.output_values[-1][3]  # Use the first element of the last output neuron for strength
        elif action == "turn":
            value = self.output_values[-1][4]  # Use the second element of the last output neuron for strength

        return action, value


if __name__ == "__main__":
    brain = Brain(NUM_INPUT_NEURONS, HIDDEN_LAYERS, NUM_OUTPUT_NEURONS)
    brain.initialize_weights()
    brain.set_inputs([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    print(brain.decide_action())
    for i in range(1000):
        brain.mutate_weights()
        print(brain.decide_action())
