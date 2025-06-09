def process_file(action, input_path, output_path):
    """
    Process the input file and write the result to the output file.

    Args:
        action (str): The type of processing to perform.
        input_path (str): Path to the input file.
        output_path (str): Path to the output file.

    Returns:
        str: Status message.
    """
    try:
        print(f"Action: {action}")
        print(f"Input: {input_path}")
        print(f"Output: {output_path}")

        # Read from input file
        with open(input_path, 'r') as infile:
            data = infile.read()

        # Process and write to output file
        with open(output_path, 'w') as outfile:
            outfile.write(data + f"\nProcessed for {action}")

        return f"{action.capitalize()} processed successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

