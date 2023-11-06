class FIFOQueue:
  def __init__(self):
    self._items = []

  def enqueue(self, item):
    self._items.append(item)

  def dequeue(self):
    if not self._items:
      raise IndexError("Queue is empty")
    return self._items.pop(0)
  
  def query(self, index):
    if not self._items:
      raise IndexError("Queue is empty")
    return self._items[index]

  def is_empty(self):
    return not self._items

  def __len__(self):
    return len(self._items)