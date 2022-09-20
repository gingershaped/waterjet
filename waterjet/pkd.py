import toml
import os, os.path
import importlib
import sys

#PKD_PATH = os.path.join(os.path.expanduser("~"), ".local", "waterjet", "pkd")
PKD_PATH = "pkds/"


class Package:
    def __init__(self, pkd, name, version, path, installName = None, local = False):
        self.name = name
        if not installName:
            self.installName = name
        else:
            self.installName = installName
        self.version = version
        self.path = path
        self.pkd = pkd

class AdHocPackage:
    def __init__(self, name, version, path, filename, extra={}):
        self.name = name
        self.version = version
        self.path = path
        self.filename = filename
        self.extra = extra
        self.pkd = None

class PKDFactory:
    def __init__(self, cm):
        self._pkds = {}
        self.cm = cm
        self.categories = {"all": set()}
        
        with os.scandir(PKD_PATH) as d:
            sys.path.insert(0, PKD_PATH)
            for entry in d:
                if entry.is_dir():
                    module = importlib.import_module(entry.name)
                    self._pkds[entry.name] = pkd = module.PKD(entry.name, self.cm)
                    for category in pkd.categories:
                        if category not in self.categories:
                                self.categories[category] = set()
                        self.categories[category].add(entry.name)
                        self.categories["all"].add(entry.name)
            sys.path.pop(0)
                        
    def __len__(self):
        return len(self._pkds)
    def __getitem__(self, key):
        return self._pkds[key]
    def __iter__(self):
        return iter(self._pkds.values())
    def __contains__(self, thing):
        return thing in self._pkds.keys()

class BasePKD:
    def __init__(self, ident, name, categories):
        self.ident = ident
        self.name = name
        self.categories = categories
    def resolvePackage(self, p):
        raise NotImplementedError
    def resolveDeps(self, p):
        raise NotImplementedError
    def install(self, p):
        raise NotImplementedError
    def uninstall(self, p):
        raise NotImplementedError


class AdHocPKD:
    def __init__(self, ident, name, categories):
        self.ident = ident
        self.name = name
        self.categories = categories
    def download(self, command, p):
        raise NotImplementedError
    
# DO NOT USE THIS CLASS
class OldPKD:
    def __init__(self, module, ident, name, categories, installFlow = "traditional"):
        self.modulePath = module
        self.module = None
        self.ident = ident
        self.name = name
        self.categories = categories
        self.installFlow = installFlow

    def load(self):
        if self.module:
            return
        
        

    def resolve(self, p):
        p = self.module.resolve(p)
        if not p:
            return None
        p.pkd = self
        return p

    def download(self, cm, p):
        self.module.download(cm, p)