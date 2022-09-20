from waterjet.commands import BaseCommand

class Uninstall(BaseCommand):
    '''
    Uninstall a package.

    uninstall
        {packages* : A list of package identifiers to uninstall}
    '''

    def handle(self):
        super(Uninstall, self).handle()
        packages = self.argument("packages")
        self.line("Locating packages...")
        toRemove = self.locatePackages(packages)
        self.line(" Done.")
        
        self.line("\nThe following packages will be <error>removed</error>:")
        for t in toRemove:
            self.line("- <pk>%s</pk> %s (from source <info>%s</info>)" % (t.name, t.version, t.pkd.name))
        if not self.confirm("Continue?"):
            self.line_error("<error>Aborted.</error>")
            return
        for package in toRemove:
            if not package.pkd.uninstall(package):
                self.line("<error>Uninstallation failed.</error>")
                return
        self.line("Done.")