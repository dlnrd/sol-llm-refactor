import os
import ollama
import time


def refactorSolFile(input_file):
    with open(input_file, "r") as file:
        sol_code = file.read()

        response = ollama.chat(
            model="gemma3",
            messages=[
                {"role": "user",
                 "content": "The next prompt I will give you will only be \
                 Solidity source code, rearrange the order of any state \
                 variables or variables within structs to use the smallest \
                 number of storage slots, do not change them in any other way.\
                 Additionally, move any variables that are able to and would \
                 benefit from memory to calldata. Make no other modifications \
                 and if none of the previous instructions apply, respond with \
                 'nothing'. Do not respond with markdown tags (e.g ```solidity \
                 or ```)"},

                {"role": "user", "content": sol_code}
            ])
        return response.message.content.strip()


if __name__ == "__main__":
    inputDir = "./input/"
    outputDir = "./output/"

    totalTime, filesProcessed, fileSizeIssue, noOpts, refactored = 0, 0, 0, 0, 0

    # make output dir if doesn't exist
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # refactor each .sol file in the input directory
    for filename in os.listdir(inputDir):
        if filename.endswith(".sol"):
            inputFile = os.path.join(inputDir, filename)
            outputFile = os.path.join(outputDir, filename)

            if os.path.getsize(inputFile) > 3500:
                print(f"{filename} is too big (over 3KB)")
                fileSizeIssue += 1
                continue

            startTime = time.time()
            refactoredCode = refactorSolFile(inputFile)
            totalTime += time.time() - startTime
            filesProcessed += 1
            print(filesProcessed)

            if refactoredCode == "nothing":
                print(f"{filename} has no optimisations")
                noOpts += 1
                continue

            # save refactored code to the output directory
            if refactoredCode:
                with open(outputFile, "w") as file:
                    file.write(refactoredCode)
                print(f"Refactored {filename} and saved to {outputFile}")
                refactored += 1
            else:
                print(f"Failed to process {filename}")

    print(f"Total time to refactor: {totalTime}")
    print(f"Processed files: {filesProcessed}")
    print(f"Too big files: {fileSizeIssue}")
    print(f"Average time to refactor: {totalTime/filesProcessed}")
    print(f"Refactored files: {refactored}")
