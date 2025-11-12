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

  def has_item_type(self, cls):
      return any(isinstance(i, cls) for i in self.items)  # проверяем есть ли в рюкзаке такой предмет нужного класса

  def select_item(self, item_id: int):
    self.items[item_id].use()

    self.del_item(item_id)

    
