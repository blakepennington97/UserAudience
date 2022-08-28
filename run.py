from user_audience import UserAudience

program = UserAudience()

numUsers = input("How many users? (N-dimension): ")
numSegments = input("How many segments? (M-dimension): ")

print("Generating data...")
program.generate_data(int(numUsers), int(numSegments))
print("Finished generating data :)\n")

while True:
    query = input("Please enter your query: ")
    result = ""
    if program.is_query_valid(query):
        result = program.process_query(query)
    else:
        result = "ERROR: Invalid input\nEnter --help for help on formatting"

    print(result)
