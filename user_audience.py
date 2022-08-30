import random
import pandas as pd
import numpy as np
from pprint import pprint


class UserAudience:
    def __init__(self):
        self.data = None

    # Generates the dataframe with dimensions: num_users x num_segments
    def generate_data(self, num_users, num_segments, ):
        segments = [f"segment{i}" for i in range(1, num_segments + 1)]
        users = [f"user{i}" for i in range(1, num_users + 1)]
        self.data = pd.DataFrame(data=np.random.randint(0, 2, size=(num_users, num_segments), dtype=bool),
                                 columns=segments, dtype=bool)
        self.data.insert(0, 'User ID', users)

    def set_default_data(self):
        segments = ["segment1", "segment2", "segment3", "segment4"]
        users = ["user1", "user2", "user3", "user4", "user5"]
        default_data = [[1, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 1, 0],
                        [1, 1, 0, 1],
                        [0, 0, 0, 0]]
        self.data = pd.DataFrame(data=default_data, columns=segments, dtype=bool)
        self.data.insert(0, 'User ID', users)

    # Gets the number of users that exist in the given segment
    def get_num_users(self, segment):
        return self.data[segment].sum()

    # Gets the number of users that exist in the given criteria
    def get_num_users_custom(self, segments, op):
        segments = [segment.strip() for segment in segments]  # trim whitespace from segments
        res = pd.DataFrame()
        if op == "AND":
            res = self.data.loc[self.data[segments].all(1)]
        elif op == "OR":
            res = self.data.loc[self.data[segments].any(1)]
        return len(res)

    # Returns a boolean indicating if the user query is valid
    def is_query_valid(self, query):
        split_query = query.split(',')
        # Non-conditional query
        if "help" in query:
            return True
        if len(split_query) == 1 and "segment" in split_query[0].lower():
            segment_id = split_query[0].split('segment')[1]
            if not segment_id.isnumeric() or int(segment_id) >= len(self.data.columns):
                return False
        # Conditional query
        elif len(split_query) > 1 and ("AND" in split_query[0] or "OR" in split_query[0]):
            segments = split_query[1:]
            if len(segments) >= 5:
                print("Too many segments! There is a max of 4")
                return False
            for segment in segments:
                segment = segment.strip()
                if "segment" in segment.lower():
                    segment_id = segment.lower().split('segment')[1]
                    if not segment_id.isnumeric() or int(segment_id) >= len(self.data.columns):
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

    def write_table(self):
        compression_opts = dict(method='zip', archive_name='data.csv')
        self.data.to_csv('data.zip', index=False, compression=compression_opts, chunksize=10000)
