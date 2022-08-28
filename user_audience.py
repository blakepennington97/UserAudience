import random


class UserAudience:
    def __init__(self):
        self.data = dict()  # segmentX --> set(userA, userB, ..)

    # Generates the data structure with dimensions: num_users x num_segments
    def generate_data(self, num_users, num_segments):
        for i in range(num_segments):
            segment_id = f"segment{i}"
            random_user_set = set()
            for j in range(num_users):
                user_id = f"user{j}"
                # Randomly choose if user is in this segment (coin-flip)
                is_user_in_segment = random.choice([True, False])
                if is_user_in_segment:
                    random_user_set.add(user_id)
            self.data[segment_id] = random_user_set

    # Gets the number of users that exist in the given segment
    def get_num_users(self, segment):
        return len(self.data[segment])

    # Gets the number of users that exist in the given criteria
    def get_num_users_custom(self, segments, op):
        matches = self.data[segments[0].strip()]

        for segment in segments:
            segment = segment.strip()
            if "and" in op.lower():
                matches = matches.intersection(self.data[segment])  # users must exist in all segments
            elif "or" in op.lower():
                matches = matches.union(self.data[segment])  # users only have to exist in one segment

        return len(matches)

    # Returns a boolean indicating if the user query is valid
    def is_query_valid(self, query):
        split_query = query.split(',')
        # Non-conditional query
        if "help" in query:
            return True
        if len(split_query) == 1 and "segment" in split_query[0].lower():
            segment_id = split_query[0].split('segment')[1]
            if not segment_id.isnumeric() or int(segment_id) >= len(self.data):
                return False
        # Conditional query
        elif len(split_query) > 1 and ("AND" in split_query[0] or "OR" in split_query[0]):
            segments = split_query[1:]
            if len(segments) > 5:
                print("Too many segments! There is a max of 4")
                return False
            for segment in segments:
                if "segment" in segment.lower():
                    segment_id = segment.lower().split('segment')[1]
                    if not segment_id.isnumeric() or int(segment_id) >= len(self.data):
                        return False
        else:
            return False

        return True

    # Returns the result of the user query
    def process_query(self, query):
        if "help" in query:
            self.teach_user()
            return
        split_query = query.split(',')
        # Non-conditional query
        if len(split_query) == 1:
            segment = split_query[0]
            return self.get_num_users(segment)
        # Conditional query
        else:
            operation = split_query[0]
            segments = split_query[1:]
            return self.get_num_users_custom(segments, operation)

    def teach_user(self):
        ex1 = "segment1"
        ex2 = "AND, segment1, segment2"
        ex3 = "OR, segment1, segment2"

        print(f"To find the number of users who are in a given segment, simply input: segmentA")
        print(f"Here's an example: {ex1}\n")
        print(
            f"To find the number of users who are in a given combination of segments, input: AND, segmentA, segmentB, ...")
        print(f"Here's an example: {ex2}\n")
        print(
            f"To find the number of users in at least one segment in a given combination of segments, input: OR, segmentA, segmentB, ..")
        print(f"Here's an example: {ex3}\n")
