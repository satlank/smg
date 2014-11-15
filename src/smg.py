import os.path
import sys

import smg.config as smgcfg
import smg.mb as smgmb
import smg.store as smgstore
import smg.engine as smgengine


def printUsage(name):
    print("Usage: {} [<configfile>] <scriptfile>".format(name))
    print("   configfile:  XML configuration for run (optional).")
    print("                Defaults to '{}'".format(smgcfg.DefaultConfigFileName))
    print("                If the file does not exists, a new one will")
    print("                be created interactively.")
    print("   scriptfile:  Name of the file to which the resulting")
    print("                script should be writting.")


if __name__ == '__main__':
    # Parse cmdline
    if len(sys.argv) == 2:
        cfgFile = smgcfg.DefaultConfigFileName
        scriptFile = sys.argv[1]
    elif len(sys.argv) == 3:
        cfgFile = sys.argv[1]
        scriptFile = sys.argv[2]
    else:
        printUsage(sys.argv[0])
        sys.exit(1)

    # Verify target
    if os.path.isfile(scriptFile):
        choice = input("File '{}' already exists. Overwrite? (y|n): ".format(scriptFile))
        if choice != 'y' and choice != 'Y':
            print('Bailing out...')
            sys.exit(0)

    # Obtain cfg
    if os.path.isfile(cfgFile):
        print("Using {}".format(cfgFile))
        cfg = smgcfg.getConfig(cfgFile)
    else:
        print("Creating {}".format(cfgFile))
        cfg = smgcfg.createConfig(cfgFile)

    # Run
    if not os.path.isfile(cfg['pickleFileName']):
        print("Obtaining data from MusicBrainz")
        release = smgmb.getReleaseFromMB(cfg['releaseId'])
        print('Writing data to {}'.format(cfg['pickleFileName']))
        smgstore.writeReleaseToPickle(release, cfg['pickleFileName'])
    print('Using data from {}'.format(cfg['pickleFileName']))
    release = smgstore.getReleaseFromPickle(cfg['pickleFileName'])

    # Create script
    print("Writing script to '{}'".format(scriptFile))
    script = smgengine.generateScript(release, cfg['genres'])
    with open(scriptFile, 'w') as f:
        f.write(script)
