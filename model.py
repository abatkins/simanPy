from elements import *

class Model:
    def __init__(self, filename):
        self.filename = filename
        self.exp = []
        self.mod = []
        self.collections = {}

    def add(self, obj):
        if obj.type == "mod":
            if obj.element:
                key = obj.element.__class__.__name__
                if key == "Queue":
                    collection = self.collections.get(key, Queues())
                    collection.add(obj.element)
                    self.collections[key] = collection
                elif key == "Entity":
                    collection = self.collections.get(key, Entities())
                    collection.add(obj.element)
                    self.collections[key] = collection
                elif key == "Resource":
                    collection = self.collections.get(key, Resources())
                    collection.add(obj.element)
                    self.collections[key] = collection
                elif key == "Counter":
                    collection = self.collections.get(key, Counters())
                    collection.add(obj.element)
                    self.collections[key] = collection
                else:
                    raise ValueError("Class name not recongized!")
            self.mod.append(obj)
        elif obj.type == "exp":
            self.exp.append(obj)
        else:
            raise ValueError("Extension type %s is not recognized" % obj.type)

    def compile(self):
        print(self.collections.values())
        self.exp += self.collections.values()
        self._to_file(".mod", self.mod)
        self._to_file(".exp", self.exp)


    #def link(self, mod_file, exp_file):

    #def run_siman(self, p_file):

    #def run(self):

    def _to_file(self, ext, objs):
        file = open(self.filename + ext, 'w')
        file.write("%s\n" % str(Begin()))
        for obj in objs:
            file.write("%s\n" % obj)
        file.write(str(End()))
        file.close()