import copy
from rotation import RotationType
from helper import *


class Item:
    def __init__(self, partno, name, LWH, weight, value=0, rotation=0):
        ''' '''
        self.partno = partno
        self.name = name
        # self.typeof = typeof
        self.width = LWH[1]
        self.height = LWH[2]
        self.length = LWH[0]
        self.position = []
        self.rotation_type = rotation
        self.weight = weight
        #self.volume = self.get_volume()
        self.value = value
        self.is_projection_needed = False
        self.is_fit = False
        self.under = []
        self.top = []
        self.besideR = []
        self.besideL = []
        self.front = []
        self.back = []
        self.onBase = False
        self.pps = []
        self.allVertices = {}

    def get_LWH_R(self):
        return [self.length,self.width,self.height,self.rotation_type]
    def item_passport(self):
        return f"{self.get_id()},{self.get_LWH_R()},{self.get_volume()}"

    def get_dimention(self):
        ''' rotation type '''
        if self.rotation_type == RotationType.RT_LWH:
            dimension = [self.length, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WLH:
            dimension = [self.width, self.length, self.height]
        elif self.rotation_type == RotationType.RT_LHW:
            dimension = [self.length, self.height,  self.width]
        elif self.rotation_type == RotationType.RT_WHL:
            dimension = [self.width, self.height, self.length]
        elif self.rotation_type == RotationType.RT_HWL:
            dimension = [self.height, self.width, self.length]
        elif self.rotation_type == RotationType.RT_HLW:
            dimension = [self.height, self.length, self.width]
        else:
            dimension = [self.length, self.width, self.height]

        return dimension

    def get_id(self):
        return self.partno+self.name
    
    def get_plot_data(self):
        data = self.position+self.get_dimention()
        data.append(int(self.name.split("C-")[1]))
        data.append(self.partno)
        return data

    def get_under(self):
        return self.under

    def get_front(self):
        return self.front

    def get_beside(self):
        return self.beside

    def get_volume(self):
        return self.length*self.width*self.height

    def get_allVertices(self):
        return self.allVertices

    def get_pps(self):
        return self.pps
    
    def get_position(self):
            return self.position

    def add_under(self, item):
        self.under.append(item)

    def add_front(self, item):
        self.front.append(item)

    def add_beside(self, item):
        self.beside.append(item)

    def set_onBase(self, flag):
        self.onBase = flag

    def set_pps(self, pps):
        self.pps = pps
    
    def set_position(self,pos):
        self.position = pos
    
    def set_allvertices(self,vertices):
        self.allVertices = copy.deepcopy(get_vertices(vertices))#get_vertices(self.position+self.getDimention())
