
class Datum(object):
  def __init__(self,x_value,y_value):
    self.x_value = x_value
    self.y_value = y_value
  def to_hash(self):
    return {'x': {'value':self.x_value}, 'y': {'value':self.y_value}}

class DataSet(object):
  def __init__(self):
    self.data = []
  def add_datum(self, x_value, y_value):
    self.data.append(Datum(x_value, y_value).to_hash())
     
