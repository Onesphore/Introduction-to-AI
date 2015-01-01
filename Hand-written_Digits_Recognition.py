# ============================================================================
#
# Author: TA Jiseong Kim
#
# ============================================================================
import sys, math, random


# ============================================================================
# Global variables 1 (for the data)
# ============================================================================
# The size of row and colum of a digit image.
row_num = 28
col_num = 28

# The variable storing training and test data
training_data_num_loaded = 100 # The number of training data to be loaded. The maximum is 60,000.
training_data = [] # It contains a tuple like (input_vector (data type: list), label)

test_data = [] # It contains a tuple like (input_vector (data type: list), label)

# ============================================================================
# Global variables 2 (for the network)
# ============================================================================
# The attributes of the ANN
hidden_layer_num = 6

input_node_num = row_num * col_num
output_node_num = 10
hidden_node_num = 25

# The variable storing weights of edges from the input layer to the first hidden layer.
# E.g., i_h_weight[i][j] is the weight of the edge from the input node i to the first hidden layer node j.
i_h_weights = [None] * input_node_num
for i in range(input_node_num):
    i_h_weights[i] = [0.0] * hidden_node_num

# The variable storing weights of edges from a hidden layer to the next hidden layer.
# E.g., h_h_weight[h][i][j] is the weight of the edge from the hidden node i in the hidden layer h to the hidden node j in the hidden layer h+1.
h_h_weights = [None] * (hidden_layer_num - 1)
for i in range(hidden_layer_num - 1):
    h_h_weights[i] = [None] * hidden_node_num
    for j in range(hidden_node_num):
        h_h_weights[i][j] = [0.0] * hidden_node_num

# The variable storing weights of edges from the last hidden layer to the output layer.
# E.g., h_o_weight[i][j] is the weight of the edge from the last hidden layer node i to the output node j.
h_o_weights = [None] * hidden_node_num
for i in range(hidden_node_num):
    h_o_weights[i] = [0.0] * output_node_num

# The variable storing weights of edges from the bias node to a hidden node.
b_h_weights = [None] * hidden_layer_num
for i in range(hidden_layer_num):
    b_h_weights[i] = [0.0] * hidden_node_num

# The variable storing weights of edges from the bias node to a output node.
b_o_weights = [0.0] * output_node_num

# ============================================================================
# Global variables 3 (temporary variables for training and test)
# ============================================================================
# The variable storing temporary output values of nodes during learning.
input_node_values = [0.0] * input_node_num
output_node_values = [0.0] * output_node_num
hidden_node_values = [None] * hidden_layer_num
for i in range(hidden_layer_num):
    hidden_node_values[i] = [0.0] * hidden_node_num

# The variable storing temporary error values of nodes during learning.
output_node_errors = [0.0] * output_node_num
hidden_node_errors = [None] * hidden_layer_num
for i in range(hidden_layer_num):
    hidden_node_errors[i] = [0.0] * hidden_node_num

# ============================================================================
# Global variables 3 (other constants)
# ============================================================================
bias_value = 1.0
learning_rate = 0.7

# ============================================================================
# Global functions (for training and test)
# ============================================================================
# The function resetting all temporary values.
def reset_temp_values():
    input_node_values = [0.0] * input_node_num
    output_node_values = [0.0] * output_node_num
    hidden_node_values = [None] * hidden_layer_num
    for i in range(hidden_layer_num):
        hidden_node_values[i] = [0.0] * hidden_node_num

    output_node_errors = [0.0] * output_node_num
    hidden_node_errors = [None] * hidden_layer_num
    for i in range(hidden_layer_num):
        hidden_node_errors[i] = [0.0] * hidden_node_num

# The function setting the initial weights of all edges.
def init_weights():
    ##################################################
    # To do: Initialize weights of all edges.
    # Fill your code below.
    ##################################################

    #from input nodes to hidden nodes in the first layer
    for i in range(input_node_num):
        for j in range(hidden_node_num):
            i_h_weights[i][j] = round(random.uniform(-1, -0.5), 4)

    #between hidden layers
    for l in range(hidden_layer_num-1):
        if l == 0:
            continue
        for i in range(hidden_node_num):
            for j in range(hidden_node_num):
               h_h_weights[l][i][j] = round(random.uniform(-1, -0.5), 4)

    #from last hidden layer to ouput layer
    for i in range(hidden_node_num):
        for j in range(output_node_num):
            h_o_weights[i][j] = round(random.uniform(-1, -0.5), 4)

    # from a bias node to a hidden layer
    for i in range(hidden_layer_num):
        for j in range (hidden_node_num):
            b_h_weights[i][j] = round(random.uniform(0.5, 1), 4)

    # from a bias node to an output layer

    for i in range(output_node_num):
        b_o_weights[i] = round(random.uniform(0.5, 1), 4)

    ##################################################
    # Fill your code above.
    ##################################################

# The activation function
def act_func(x, w): # x is a list of input values and w is a list of corresponding weights of edges.
    ##################################################
    # To do: Implement the activation function.
    # Fill your code below.
    ##################################################
    sum = 0.0
    for i in range(len(x)):
        sum += x[i]*w[i]

    output = 1.0/(1.0+math.exp(-sum))

    return output

    ##################################################
    # Fill your code above.
    ##################################################

# The backpropagation function
def backpropagation():
    init_weights()

    converged = False

    count = 0
    prev = 0.0

    while not converged:

        sum_e = 0.0
        for i in range(len(training_data)):
            input_vector = training_data[i][0]
            # The vector of length 10 which element stores 1 if the element's index is equal to the label of input_vector. Otherwise the element stores 0.
            # E.g., if the label is 0, target_vector[0] = 1 and any other elements of target_vector store 0.
            target_vector = training_data[i][1]

            reset_temp_values()

            forward_pass(input_vector)
            reverse_pass(target_vector)
            update_weights()

            avg_input_error = 0.0
            for i in range(len(target_vector)):
                avg_input_error += abs(target_vector[i] - output_node_values[i])

            avg_input_error /= len(target_vector)
            sum_e += avg_input_error


        ##################################################
        # To do: Check whether the network is converged.
        # If converged, the loop should be terminated.
        # Fill your code below.
        ##################################################




        sum_e /= len(training_data)
        norm_sum_e = sum_e*100.0

        if(norm_sum_e > 91.0) or (count > 200):
            converged = True
        else:
            prev = norm_sum_e

        count += 1

# The function calculating output values of all nodes.
def forward_pass(input_vector):

    ##################################################
    # To do: Implement the forward pass.
    # Fill your code below.
    ##################################################

    #input to first hidden layer
    for i in range(hidden_node_num):
        w = [0.0]*(input_node_num+1)
        for j in range (input_node_num):
            w[j] = i_h_weights[j][i]

        w[input_node_num] = b_h_weights[0][i]

        x = [0.0]*(input_node_num+1)
        for k in range(len(input_vector)):
           x[k] = input_vector[k]
        x[input_node_num] = bias_value

        hidden_node_values[0][i] = act_func(x, w)


    #bewtween hidden layers
    for l in range(hidden_layer_num):
        if l == 0:
            continue

        for i in range(hidden_node_num):
            w = [0.0]*(hidden_node_num+1)
            for j in range(hidden_node_num):
               w[j] = h_h_weights[l-1][j][i]
            w[hidden_node_num] = b_h_weights[l][i]

            x = [0.0]*(hidden_node_num+1)
            for k in range(hidden_node_num):
               x[k] = hidden_node_values[l-1][k]
            x[hidden_node_num] = bias_value


            hidden_node_values[l][i] = act_func(x, w)


    #from the last hidden layer to the output layer
    for i in range(output_node_num):
        w = [0.0]*(hidden_node_num+1)
        for j in range(hidden_node_num):
            w[j] = h_o_weights[j][i]
        w[hidden_node_num] = h_o_weights[hidden_layer_num-1][i]

        x = [0.0]*(hidden_node_num+1)
        for k in range(hidden_node_num):
            x[k] = hidden_node_values[hidden_layer_num-1][k]
        x[hidden_node_num] = bias_value

        output_node_values[i] = act_func(x, w)

    ##################################################
    # Fill your code above.
    ##################################################

# The function calculating error values of all nodes from back to front.
def reverse_pass(target_vector):

    # the derivative of g(x) = g(x)-square(g(x))

    # error values in the output nodes
    for i in range(output_node_num):
        ai = output_node_values[i]
        output_node_errors[i] = (ai-(ai*ai))*(target_vector[i]-ai)

    #error values in the last hidden layer nodes

    for i in range(hidden_node_num):
        ai = hidden_node_values[hidden_layer_num-1][i]
        wd = 0.0
        for j in range(output_node_num):
            wd += h_o_weights[i][j]*output_node_errors[j]

        hidden_node_errors[hidden_layer_num-1][i] = (ai- (ai*ai))*wd

    # between layers

    if hidden_layer_num > 1:
        for l in reversed(range(hidden_layer_num)):
            if l == hidden_layer_num-1:
                continue

            for i in range(hidden_node_num):
                ai = hidden_node_values[l][i]
                wd = 0.0

                for j in range(hidden_node_num):
                    wd += h_h_weights[l][i][j]*hidden_node_errors[l+1][j]
                hidden_node_errors[l][i] = (ai-(ai*ai))*wd





    ##################################################
    # To do: Implement the reverse pass.
    # Fill your code below.
    ##################################################


    ##################################################
    # Fill your code above.
    ##################################################

# The function updating the weights of all edges.
def update_weights():

    # from input to the first hidden layer
    for i in range(input_node_num):
        for j in range(hidden_node_num):
            i_h_weights[i][j] += learning_rate*input_node_values[i]*hidden_node_errors[0][j]


    # between hidden layers

    if hidden_layer_num > 1:
        for l in range(hidden_layer_num):
            if l == hidden_layer_num-1:
                break

            for i in range(hidden_node_num):
                for j in range(hidden_node_num):
                   h_h_weights[l][i][j] += learning_rate*hidden_node_values[l][i]*hidden_node_errors[l+1][j]

    #from the last hidden layer to the output layer
    for i in range(hidden_node_num):
        for j in range(output_node_num):
            h_o_weights[i][j] +=learning_rate*hidden_node_values[hidden_layer_num-1][i]*output_node_errors[j]

    #bias weight, to hidden layers

    for l in range(hidden_layer_num):
        for i in range(hidden_node_num):
            b_h_weights[l][i] += learning_rate*hidden_node_errors[l][i]

    for i in range(output_node_num):
        b_o_weights[i] += learning_rate*output_node_errors[i]



    ##################################################
    # To do: Update the weights of all edges using
    # the pre-calculated output values and errors of nodes.
    # Fill your code below.
    ##################################################


    ##################################################
    # Fill your code above.
    ##################################################   
     
# ============================================================================
# Training data loading
# ============================================================================
input_vector = []
load_cnt = 0
f = open('Training_Data.txt', 'r')
line = f.readline()

while line:
    if line[0] == '#':
        line = f.readline()
        continue
    
    line = line[0:-1]
    for i in range(len(line)):
        input_vector.append(float(line[i]))

    if len(input_vector) >= row_num * col_num:
        target_vector = [0.0] * output_node_num
        target_vector[int(f.readline()[0:-1])] = 1.0
        training_data.append((input_vector, target_vector))

        input_vector = []
        load_cnt += 1

    if load_cnt >= training_data_num_loaded:
        break
    
    line = f.readline()

# ============================================================================
# Test data loading
# - Do not modify any codes in this section.
# ============================================================================
input_vector = []
f = open('Test_Data.txt', 'r')
line = f.readline()
while line:
    if line[0] == '#':
        line = f.readline()
        continue
    
    line = line[0:-1]
    for i in range(len(line)):
        input_vector.append(float(line[i]))

    if len(input_vector) >= row_num * col_num:
        target_vector = [0.0] * output_node_num
        target_vector[int(f.readline()[0:-1])] = 1.0
        test_data.append((input_vector, target_vector))

        input_vector = []
    
    line = f.readline()

# ============================================================================
# Training
# ============================================================================


backpropagation()


# ============================================================================
# Saving the trained network
# ============================================================================
save_file = open('Trained_Network.txt', 'w+')
save_file.write(str(i_h_weights) + '\n')
save_file.write(str(h_h_weights) + '\n')
save_file.write(str(h_o_weights) + '\n')
save_file.write(str(b_h_weights) + '\n')
save_file.write(str(b_o_weights) + '\n')

# ============================================================================
# Test and Scoring
# - Do not modify any codes in this section.
# ============================================================================
avg_total_error = 0.0

for i in range(len(test_data)):
    input_vector = test_data[i][0]
    target_vector = test_data[i][1]
    
    forward_pass(input_vector)
    
    avg_input_error = 0.0
    for i in range(len(target_vector)):
        avg_input_error += abs(target_vector[i] - output_node_values[i])

    avg_input_error /= len(target_vector)

    avg_total_error += avg_input_error

avg_total_error /= len(test_data)
norm_avg_total_error = avg_total_error * 100.0
total_score = 100 - norm_avg_total_error

# The total score indicates how your network does well in classifying the given test data.
print 'Your total score (min=0.0, max=100.0) =', total_score

