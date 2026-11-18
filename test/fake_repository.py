class FakeRepository:
    def __init__(self):
        self.items = []
        self._next_id = 1

    def save(self, item):
        item.id = self._next_id
        self._next_id += 1
        self.items.append(item)
        return item

    def list(self):
        return self.items

    def get_by_id(self, id):
        for item in self.items:
            if item.id == id:
                return item
        return None