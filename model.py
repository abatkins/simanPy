from elements import *
import subprocess


class Model:
    def __init__(self, filename):
        self.filename = filename
        self.exp = []
        self.mod = []
        self.collections = {}

    # Allocates block and element data to correct file
    def add(self, obj):
        if obj.type == "mod":
            if hasattr(obj, "blocks") and obj.blocks:  # check if superblock
                for block in obj.blocks:
                    self._add_element(block)
            else:  # normal block
                self._add_element(obj)
            self.mod.append(obj)
        elif obj.type == "exp":  # Element block
            self.exp.append(obj)
        else:
            raise ValueError("Extension type %s is not recognized" % obj.type)

    # Adds element stored in blocks
    def _add_element(self, obj):
        if hasattr(obj, "element") and obj.element:
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
            elif key == "Attribute":
                collection = self.collections.get(key, Attributes())
                collection.add(obj.element)
                self.collections[key] = collection
            elif key == "Variable":
                collection = self.collections.get(key, Variables())
                collection.add(obj.element)
                self.collections[key] = collection
            else:
                raise ValueError("Class name not recognized!")

    # Writes to SIMAN files
    def compile(self):
        self.exp += self.collections.values()
        mod_filename = self.filename + ".mod"
        exp_filename = self.filename + ".exp"
        self._to_file(mod_filename, self.mod)
        self._to_file(exp_filename, self.exp)

        return mod_filename, exp_filename

    def link(self, mod_file, exp_file):
        subprocess.run("liner %s %s" % (mod_file, exp_file), shell=True, check=True)

    def run_siman(self):
        p_filename = self.filename + '.p'
        subprocess.run("siman %s" % p_filename, shell=True, check=True)

    def run(self):
        mod_filename, exp_filename = self.compile()
        self.link(mod_filename, exp_filename)
        self.run_siman()

    def _to_file(self,filename, objs):
        file = open(filename, 'w')
        file.write("%s\n" % str(Begin()))
        for obj in objs:
            file.write("%s\n" % obj)
        file.write(str(End()))
        file.close()