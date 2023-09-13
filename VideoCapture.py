import cv2
import numpy as np
from PIL import Image, ImageSequence

# import apng in class -> only if needed


class WebpFrames:
    def __init__(self, file_path):
        self.file_path = file_path
        self.img = Image.open(file_path)
        self.index = 0

    def __iter__(self):
        self.img.seek(0)
        return self

    def __next__(self):
        if self.img.tell() < self.img.n_frames - 1:  # Check if current frame is not the last frame
            self.img.seek(self.img.tell() + 1)
            return True, cv2.cvtColor(np.array(self.img.convert('RGB')), cv2.COLOR_RGB2BGR)
        else:
            return False, None

    def read(self):
        return next(self)
    
    def __len__(self):
        return self.img.n_frames


class GifFrames:
    def __init__(self, file_path):
        self.file_path = file_path
        self.frames = []
        self.index = 0
        self.__iter__()  # Call __iter__ to populate self.frames

    def __iter__(self):
        self.frames = []
        with Image.open(self.file_path) as im:
            for frame in ImageSequence.Iterator(im):
                self.frames.append(np.array(frame.convert('RGB')))
        return self

    def __next__(self):
        if self.index < len(self.frames):
            frame = self.frames[self.index]
            self.index += 1
            return True, frame
        else:
            return False, None

    def __len__(self):
        if not self.frames:
            with Image.open(self.file_path) as im:
                for frame in ImageSequence.Iterator(im):
                    self.frames.append(np.array(frame.convert('RGB')))
        return len(self.frames)

    def read(self):
        ret, frame = next(self)

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            return ret, frame
        else:
            return ret, None
    

class PngFrames:
    try:
        import apng
    except:
        apng = None
        raise ImportError('apng is not installed. Please install it with "pip install apng" to use animated png files.')

    def __init__(self, file_path):
        self.file_path = file_path
        self.frames = []
        self.index = 0
        self.__iter__()

    def __iter__(self):
        self.frames = []
        with Image.open(self.file_path) as im:
            for frame in ImageSequence.Iterator(im):
                self.frames.append(np.array(frame.convert('RGB')))
        return self

    def __next__(self):
        if self.index < len(self.frames):
            frame = self.frames[self.index]
            self.index += 1
            return True, frame
        else:
            return False, None

    def __len__(self):
        if not self.frames:
            with Image.open(self.file_path) as im:
                for frame in ImageSequence.Iterator(im):
                    self.frames.append(np.array(frame.convert('RGB')))
        return len(self.frames)

    def read(self):
        ret, frame = next(self)
        if ret:
            return ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        else:
            return ret, None


# WRAPPER FUNCTION
def VideoCapture(file_path):
    file_type = file_path.split('.')[-1]

    # animated webp
    if file_type == 'webp':
        cap = WebpFrames(file_path)
        print('webp:', cap.__len__(), "frames")        
    
    # animated gif
    elif file_type == 'gif':
        cap = GifFrames(file_path)
        print('gif:', cap.__len__(), "frames")
    
    # animated png
    elif file_type == 'png':
        cap = PngFrames(file_path)
        print('png:', cap.__len__(), "frames")

    # video file
    elif file_type in ['mp4', 'avi', 'mpeg', 'wmv', 'asf', 'mov']:
        cap = cv2.VideoCapture(file_path)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(file_type, "using opencv:", length, "frames")
    
    # webcam
    elif file_path.isdigit():
        cap = cv2.VideoCapture(int(file_path))
        print('opencv webcam ID', file_type)
    
    # video URL
    elif type(file_path) == str:
        cap = cv2.VideoCapture(file_path)
        print('opencv video URL:', file_type)
    
    return cap


if __name__ == '__main__':

    path = 'media/cars2.webp'
    # path = 'media/slow_traffic_small.mp4'
    # path = 'media/monsters.gif'
    # path = 'media/bouncing_ball.png'

    cap = VideoCapture(path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Frame', frame)
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break
    
    # cap.release()
    # cv2.destroyAllWindows()
