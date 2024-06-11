import argparse, sys, re
from typing import Union, List
from pathlib import Path
import cv2
import numpy as np
import datetime

class DiamondSquare(object):
    '''The Core Upscaling Algorithm: DiamondSquare'''
    
    supported_types = ['.jpg', '.png']
    output_suffix = '_scaled'
    max_filesize = 12_000

    def __init__(self, src:str, target:str = None, allow_overwrite:bool = False):
        
        self.source:Path = Path(src)
        if not (self.source.exists() and self.source.is_file() and self.source.suffix in DiamondSquare.supported_types):
            raise Exception('Invalid source image.')
        
        if not target:
            self.target = self.source
            self.target = self.GetUniqueName()
        else:
            self.target = Path(target)
            if not (self.target.exists() and self.target.is_file() and self.target.suffix in DiamondSquare.supported_types):
                raise Exception('Invalid target file.')

        self.array: np.ndarray = None
    
    @staticmethod
    def Parser():
        desc = '''
        The upscale command uses the classic fractal: 'Diamond-Square' algorithm
        to double the input image resolution.
        '''
        parser = argparse.ArgumentParser(description=desc)
        #parser.add_argument('--configuration', '-rel', action='store_true', help = 'Include for Release, omit for Debug')
        #parser.add_argument('--platform', '-p', type = int, default = Utils.supported_platforms, nargs='*', choices = Utils.supported_platforms)
        source_help = f'''The path to the image to be upscaled.'''
        parser.add_argument('--Source', '-s', type=str, help=source_help)

        target_help = f'''Sets the directory of the output image.
        Optionally, a filename can be included to set the filename of the output image.
        Default is the input image directory.
        '''
        parser.add_argument('--Target', '-t', type=str, default=None, help=target_help)

        overwrite_help = f'''Include argument to allow overwrite of Target file. 
        '''
        parser.add_argument('--Overwrite', '-o', action='store_true', help=overwrite_help)
        
        return parser
    
    def Execute(self):
        
        print(f'Expanding Image @ {datetime.datetime.now()}', flush=True)
        print(f'Input Image:\n{self.source.absolute().as_posix()}', flush=True)

        #parse image file
        arr = DiamondSquare.ReadImage(self.source.absolute().as_posix())
        print(f'original size: {arr.shape}', flush=True)

        if any(d > DiamondSquare.max_filesize for d in arr.shape):
            arr = None
            raise Exception('Maximum file size exceeded.')
        
        #extract channels from BGR image
        channels = [arr[:,:,c] for c in range(arr.shape[2])]

        #expand array for each channel
        channels = [DiamondSquare.ExpandArray(c) for c in channels]
        print()

        channels = [self.DiamondSquareAlgorithm(c) for c in channels]

        self.array = np.dstack(channels)

        self.Save()
    
    def DiamondSquareAlgorithm(self, arr:np.ndarray) -> np.ndarray:
        #return arr.astype(int)
        sq_start = np.array([2,2])
        DiamondSquare.SquareCompVec(arr, sq_start)
        #return arr.astype(int)
        d1_start = np.array([1,2])
        DiamondSquare.DiamondCompVec(arr, d1_start)
        #return arr.astype(int)
        d2_start = np.array([2,1])
        DiamondSquare.DiamondCompVec(arr, d2_start)
        
        #omit padding at output
        return arr[1:-1,1:-1].astype(int)

    @staticmethod
    def ReadImage(path:str) -> np.ndarray:
        try:
            arr = cv2.imread(path, cv2.IMREAD_COLOR)
            if len(arr.shape) == 2: arr = arr[..., None]
            return arr
        except Exception as ex:
            print('Error reading image file.', flush=True)
            #print(ex, flush=True)
    
    @staticmethod
    def ExpandArray(arr: np.ndarray):
        #allocate empty array
        z = np.zeros(2 * np.array(arr.shape[:2]) + 1)
        #fill current values
        z[1::2,1::2] = arr
        return z
    
    @staticmethod
    def GetSlice(arr_dims:np.ndarray, start_idx:np.ndarray, offset:np.ndarray = np.array([0,0])) -> np.ndarray:
        strides = (arr_dims - start_idx - 1).astype(int)
        starts = (start_idx + offset).astype(int)
        row_end, col_end = np.min(np.vstack([arr_dims, starts + strides]), axis=0).astype(int)
        return np.s_[starts[0]: row_end: 2, starts[1]: col_end: 2]
    
    @staticmethod
    def SquareCompVec(arr: np.ndarray, start_idx:np.ndarray):
        dims = np.array(arr.shape)
        centers = DiamondSquare.GetSlice(dims, start_idx)
        top_left = DiamondSquare.GetSlice(dims, start_idx, np.array([-1, -1]))
        bottom_left = DiamondSquare.GetSlice(dims, start_idx, np.array([1, -1]))
        top_right = DiamondSquare.GetSlice(dims, start_idx, np.array([-1, 1]))
        bottom_right = DiamondSquare.GetSlice(dims, start_idx, np.array([1, 1]))

        st = np.dstack([arr[top_left], arr[bottom_left], arr[top_right], arr[bottom_right]])
        arr[centers] = np.round(st.mean(axis = -1))

    @staticmethod
    def DiamondCompVec(arr: np.ndarray, start_idx: np.ndarray):
        dims = np.array(arr.shape)
        centers = DiamondSquare.GetSlice(dims, start_idx)
        top_slice = DiamondSquare.GetSlice(dims, start_idx, np.array([-1, 0]))
        bottom_slice = DiamondSquare.GetSlice(dims, start_idx, np.array([1, 0]))
        left_slice = DiamondSquare.GetSlice(dims, start_idx, np.array([0, -1]))
        right_slice = DiamondSquare.GetSlice(dims, start_idx, np.array([0, 1]))

        st = np.dstack([arr[top_slice], arr[bottom_slice], arr[left_slice], arr[right_slice]])

        arr[centers] = np.round(st.mean(axis = -1))
    
    def GetUniqueName(self) -> Path:
        if not self.target or self.target.absolute().as_posix() == self.source.absolute().as_posix():
            return Path(self.source.parent/f'{self.source.stem}{DiamondSquare.output_suffix}{self.source.suffix}')

    # def GetUniqueName(self):
    #     if self.dest.stem.endswith(DiamondSquare.output_suffix):
    #         return self.dest.stem.replace(DiamondSquare.output_suffix, DiamondSquare.output_suffix+'_1')
        
    #     matches = re.findall(f'_{DiamondSquare.output_suffix}_(\d+)$', self.dest.stem)
    #     if len(matches) == 1:
    #         num = int(matches[0])
    #         temp = self.dest.stem
    #         return re.sub('\d+$', str(num+1), self.dest.stem)+self.dest.suffix

    def Save(self):
        if self.target.exists() and not self.allow_overwrite:
            raise('Overwriting the target file is forbidden.')

        try:
            print(f'Saving new image:\n{self.target.absolute().as_posix()}', flush=True)
            cv2.imwrite(self.target.absolute().as_posix(), self.array)
            
        except:
            raise Exception('Error saving new image.')


if __name__ == '__main__':
    exit(1)