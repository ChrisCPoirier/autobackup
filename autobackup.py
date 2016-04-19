import os
import shutil

class MyAutoBackup:
    """
    Class to run rsync from source to dest then cleanup any files deleted from source that still exist in dest.
    The files will be placed in a temporary holding directory and touched. If the files are not recovered after
    xx amount of time the files will be deleted.
    """
    def __init__(self, source, dest, keep_time=None, trash_folder=None):
        self.source = source
        self.dest = dest
        self.trash = dest + '/.autobackup-trash-1000'
        self.ignore_dirs = [self.trash]

        if not keep_time:
            # one day second * minutes * hours
            keep_time = 60 * 60 * 24

        if not trash_folder:
            trash_folder = self.dest + "/.MyAutoBackupTrash"


    def run(self):
        self.backup()
        self.cleanup()

    def backup(self):
        print("backingup",self.source,"to",self.dest)
        os.system("rsync -avz " + self.source + " " + self.dest)

    def cleanup(self):
        """
        loop through destination folder and find all files that do not exist in source.
        if the file does not exist move it to the trash_folder in the dest directory.
        use the touch command to set the date modified on the file when moved into this directory
        """
	print "clean up on " + self.dest
        for root, folders, files in os.walk(self.dest):
            for ignore_dir in self.ignore_dirs:
                if ignore_dir in folders:
                    folders.remove(ignore_dir)
		    
            for folder in folders:
                backupdir = os.path.join(root,folders)
                sourcedir = bakupdir.replace(destination,source) 
                if not os.path.exists(sourcedir):
                    trash = backupdir.replace(destination,trash_dir)
                    # shutil.move(backupdir, trash)
                    print("move",backupdir,"to",trash)
                    # os.utime(trash, None)
            
            for filename in files:
                checkfile = root + "/" + filename
                checkfile = checkfile.replace(self.dest, self.source)
                print("checking if ", checkfile, "exists")
                if not os.path.exists(checkfile): 
                    print os.path.join(root,filename)
		    backupfile = checkfile.replace(self.source,self.dest)
                    trash = self.trash + checkfile.replace(self.source, "")
                    # shutil.move(backupfile, trash)
                    print("move",backupfile,"to",trash)
                    # os.utime(trash, None)

if __name__ == '__main__':
    backup = MyAutoBackup("/home/chris/bitbucket/autobackup/test/source/", "/home/chris/bitbucket/autobackup/test/dest")
    backup.run() 
