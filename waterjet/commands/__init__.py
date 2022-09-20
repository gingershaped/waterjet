from cleo import Command
from waterjet.pkd import PKDFactory
from waterjet.pkd import AdHocPKD

class BaseCommand(Command):
    def handle(self):
        self.add_style("pk", fg="blue")
        self.add_style("warning", fg="yellow", options=["bold"])

    def locatePackages(self, packages):
        try:
            pkdFactory = PKDFactory(self)
        except Exception:
            self.line("\n<error>Exception occured while loading package definition %s:" % pkdIdent)
            raise
        l = []
        progress = self.progress_bar(len(packages))
        progress.start()
        
        for package in packages:
            pkdsToCheck = set()
            category = package[package.rfind("@") + 1:]
            if category.startswith(":"):
                package = package[:package.rfind("@")]
                if category in pkdFactory:
                    pkdsToCheck.add(category)
                else:
                    self.line_error("\nPackage category '%s' is not valid." % category)
                    continue
            else:
                if category not in pkdFactory.categories or not category:
                    category = "all"
                else:
                    package = package[:package.rfind("@")]
                pkdsToCheck.update(pkdFactory.categories[category])
            candidates = {}
            for pkdIdent in pkdsToCheck:
                pkd = pkdFactory[pkdIdent]    
                r = pkd.resolvePackage(package)
                if r:
                    candidates[pkd] = r
            l.append(candidates)
            progress.advance()
            
        progress.finish()
        bases = []
        for candidates in l:
            if not len(candidates):
                self.line_error("\n<error>Unable to find package: %s" % package)
                continue
            if len(candidates) > 1:
                self.line("\nMultiple sources found for package <pk>%s</pk>" % package)
                candidate = candidates[pkdFactory[self.choice(
                    "Which source do you want to use?",
                    [c.pkd.ident for c in candidates.values()],
                    0
                )]]
            else:
                candidate = list(candidates.values())[0]
            bases.append(candidate)
        return bases

    def resolveDependencies(self, bases):
        packagesForPkds = {}
        toInstall = []
        for package in bases:
            if isinstance(package.pkd, AdHocPKD):
                self.line("\n<warning>Package %s's dependencies cannot be pre-resolved and will not be listed.</warning>" % package.name)
            else:
                if package.pkd not in packagesForPkds:
                    packagesForPkds[package.pkd] = [package]
                else:
                    packagesForPkds[package.pkd].append(package)
        for pkd in packagesForPkds:
            [toInstall.append(i) for i in pkd.resolveDeps(packagesForPkds[pkd])]
        return toInstall
        