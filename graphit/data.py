
class Datum(object):
  def __init__(self,x_value,y_value,series=None):
    self.x_value = x_value
    self.y_value = y_value
    self.series = series
  def to_hash(self):
    return {'series': series, 'x': {'value':self.x_value}, 'y': {'value':self.y_value}}

class DataSet(object):
  def __init__(self):
    self.data = []
  def add_datum(self, x_value, y_value, series=None):
    self.data.append(Datum(x_value, y_value, series).to_hash())
     
