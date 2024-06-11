import argparse, sys
from typing import Union, Sequence

class SR_CLI():
    def __init__(self):
        desc = '''
        SuperResolve CLI - A lightweight command line interface for manipulating image files.
        '''
        parser = argparse.ArgumentParser(description=desc)
        #parser.add_argument('command', help=f'Available commands include: upscale, Copy')
        parser.add_argument('command', help=f'Available commands include: upscale')
        args = parser.parse_args(sys.argv[1:2])
        try:
            args = parser.parse_args(sys.argv[1:2])
        except:
            parser.print_help()
            exit(1)
            
        if hasattr(self, args.command):
            getattr(self, args.command)()
        else:
            parser.print_help()
            exit(1)

    def upscale(self):
        print('run upscale command', flush=True)
        

if __name__ == '__main__':
    SR_CLI()