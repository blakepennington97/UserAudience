from user_audience import UserAudience

program = UserAudience()

is_custom = int(input("Enter 0 to use default data (20 x 10), or 1 to use custom dimensions: "))
if is_custom == 1:
    num_users = input("How many users? (N-dimension): ")
    num_segments = input("How many segments? (M-dimension): ")
    print("Generating data...")
    program.generate_data(int(num_users), int(num_segments))
    print("Finished generating data :)")
elif is_custom == 0:
    program.set_default_data()
else:
    quit(f"ERROR: Invalid selection ({is_custom})\n")


while True:
    query = input("Please enter your query: ")
    result = ""
    if program.is_query_valid(query):
        result = program.process_query(query)
    else:
        result = "ERROR: Invalid input\nEnter --help for help on formatting\n"

    print(result)
