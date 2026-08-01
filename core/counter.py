class ObjectCounter:

    def __init__(self):

        self.unique_ids = set()

    def update(self, track_id):

        self.unique_ids.add(track_id)

    def get_count(self):

        return len(self.unique_ids)