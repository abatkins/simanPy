from elements import _Begin, _End, _Queues, _Entities, _Counters, _Resources, _Attributes, _Variables, _Dstats, \
    _Tallies, _Storages, _Outputs
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

    def _to_collection(self, key, elements_inst, obj):
        collection = self.collections.get(key, elements_inst)
        if obj.element.number == "":
            obj.element.number = len(collection.elements) + 1
        collection.add(obj.element)
        self.collections[key] = collection

    # Adds element stored in blocks
    def _add_element(self, obj):
        if hasattr(obj, "element") and obj.element:
            key = obj.element.__class__.__name__
            if key == "Queue":
                self._to_collection(key, _Queues(), obj)
            elif key == "Resource":
                self._to_collection(key, _Resources(), obj)
            elif key == "Counter":
                self._to_collection(key, _Counters(), obj)
            elif key == "Attribute":
                self._to_collection(key, _Attributes(), obj)
            elif key == "Variable":
                self._to_collection(key, _Variables(), obj)
            elif key == "Dstat":
                self._to_collection(key, _Dstats(), obj)
            elif key == "Tally":
                self._to_collection(key, _Tallies(), obj)
            elif key == "Storage":
                self._to_collection(key, _Storages(), obj)
            elif key == "Entity":
                self._to_collection(key, _Entities(), obj)
            elif key == "Output":
                self._to_collection(key, _Outputs(), obj)
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

    # Run model.exe
    def run_mod(self, input_file, output_file=None):
        if not output_file:
            output_file = input_file.split('.')[0] + '.m'
        subprocess.run('model {} {}'.format(input_file, output_file), shell=True, check=True)
        return output_file

    # Run expmt.exe
    def run_expmt(self, input_file, output_file=None):
        if not output_file:
            output_file = input_file.split('.')[0] + '.e'
        subprocess.run('expmt {} {}'.format(input_file, output_file),shell=True, check=True)
        return output_file

    # Run linker.exe
    def run_link(self, mod_file, exp_file, output_file=None):
        if not output_file:
            output_file = mod_file.split('.')[0] + '.p'
        subprocess.run('linker {} {} {}'.format(mod_file, exp_file, output_file), shell=True, check=True)
        return output_file

    # Run siman.exe
    def run_siman(self, input_file):
        subprocess.run('siman {}'.format(input_file), shell=True, check=True)

    # Run Simulation
    def run(self):
        mod_filename, exp_filename = self.compile()
        m_filename = self.run_mod(mod_filename)
        e_filename = self.run_expmt(exp_filename)
        p_filename = self.run_link(m_filename, e_filename)
        self.run_siman(p_filename)

    def _to_file(self,filename, objs):
        file = open(filename, 'w')
        file.write("%s\n" % str(_Begin()))
        for obj in objs:
            file.write("%s\n" % obj)
        file.write(str(_End()))
        file.close()