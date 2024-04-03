def map_value_pos(x):
    # Define the input and output range
    i_min = 0
    i_max = 250
    o_min = 30
    o_max = 250

    # Map the input value to the output range
    mapped_value = (x-i_min) * (o_max-o_min) / (i_max - i_min) + o_min

    return mapped_value


def map_value_neg(x):
    # Define the input and output range
    i_min = -1.0
    i_max = -255.0
    o_min = -26.0
    o_max = -255.0

    # Map the input value to the output range
    mapped_value = (x-i_min) * (o_max-o_min) / (i_max - i_min) + o_min

    return mapped_value


# Example usage:
input_value = 50  # Example input value
if (input_value >= 1):
    output_value = map_value_pos(input_value)
elif (input_value <= -1):
    output_value = map_value_neg(input_value)
else:
    output_value = 0
print("Mapped value:", output_value)
