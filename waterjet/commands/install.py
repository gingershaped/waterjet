import tempfile
import requests
import os.path
from clikit.api.io.flags import *
from waterjet.commands import BaseCommand
from waterjet.util import *

class Install(BaseCommand):
    '''
    Install a package.

    install
        {packages* : A list of package identifiers to install}
        {--f|force-install : Install packages even if they are already installed}
    '''

    def handle(self):
        super(Install, self).handle()
        self.line("Locating packages...")
        packages = self.argument("packages")
        bases = self.locatePackages(packages)
        self.line(" Done.")
        _ = []
        for base in bases:
            if base.pkd.isInstalled(base):
                self.line("<warning>Package %s is already installed.</warning>" % base.name)
                _.append(base)
        for b in _:
            bases.remove(b)
        if not bases:
            self.line_error("<error>No packages to install.</error>")
            return
        self.line("Resolving dependencies...")
        toInstall = self.resolveDependencies(bases)
        self.line(" Done.")
        _ = []
        for p in toInstall:
            if p.pkd.isInstalled(p):
                self.line("<warning>Package %s is already installed.</warning>" % p.name)
                _.append(p)
        for b in _:
            toInstall.remove(b)
        
        self.line("\nThe following packages will be <info>installed</info>:")
        for t in toInstall:
            self.line("- <pk>%s</pk> %s (from source <info>%s</info>)" % (t.name, t.version, t.pkd.name))
        if not self.confirm("Continue?"):
            self.line_error("<error>Aborted.</error>")
            return

        with tempfile.TemporaryDirectory() as target:
            for package in toInstall:
                self.line("\nDownloading <pk>%s</pk> from <info>%s</info>" % (package.name, package.pkd.name))
                r = requests.get(package.path, stream=True)
                size = r.headers.get("Content-Length", None)
                if size:
                    progress = self.progress_bar(int(size) // 1024)
                else:
                    progress = self.progress_bar()
                with open(os.path.join(target, package.installName), "wb") as f:
                    for c, chunk in enumerate(r.iter_content(1024)):
                        f.write(chunk)
                        progress.advance()
                package.path = os.path.join(target, package.installName)
            self.line("")
            for package in toInstall:
                if not package.pkd.install(package):
                    self.line("<error>Installation failed.</error>")
                    return
            self.line("Done.")
            
           
        

        

        
        
            
            
                
            
                