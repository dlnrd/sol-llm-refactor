import argparse
import os
import glob
import ollama

# Define a predefined prompt
PREDEFINED_PROMPT = "Analyze the following Solidity code and provide a summary of potential security issues and improvements."


def process_sol_file(file_path):
    # Read the .sol file content
    with open(file_path, 'r') as f:
        file_content = f.read()

    # Use the Ollama package to process the file with the predefined prompt
    try:
        response = ollama.chat(model='deepseek-r1', messages=[
                               {"role": "user", "content": file_content}])
        return response["text"]
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return ""


def save_output(output_dir, file_name, result):
    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the result to a file in the output directory
    output_file = os.path.join(output_dir, f"{file_name}_processed.txt")
    with open(output_file, 'w') as f:
        f.write(result)


def process_files(input_dir, output_dir):
    # Get all .sol files in the input directory
    sol_files = glob.glob(os.path.join(input_dir, "*.sol"))

    for sol_file in sol_files:
        file_name = os.path.basename(sol_file)
        print(f"Processing {file_name}...")

        # Process the .sol file using Ollama
        result = process_sol_file(sol_file)

        # Save the result to the output directory
        if result:
            save_output(output_dir, file_name, result)
            print(f"Saved processed result for {file_name}")


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Process .sol files using Ollama.")
    parser.add_argument('-i', '--input', required=True,
                        help="Directory containing .sol files")
    parser.add_argument('-o', '--output', required=True,
                        help="Directory to save processed results")

    args = parser.parse_args()

    # Process the files
    process_files(args.input, args.output)


if __name__ == "__main__":
    main()
