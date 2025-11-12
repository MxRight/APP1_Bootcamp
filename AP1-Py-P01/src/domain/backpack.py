
class Backpack:
  MAXCAPACITY = 9

  def __init__(self):
    self.maxcapacity = self.MAXCAPACITY
    self.num_of_items = 0
    self.items = dict()

  def add_item(self):
    pass

  def del_item(self, item_id: int):
    pass

  def select_item(self, item_id: int):
    self.items[item_id].use()

    self.del_item(item_id)

    
