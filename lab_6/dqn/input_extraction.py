import matplotlib.pyplot as plt
import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image
from pygame.surfarray import array3d

from game.game import *

plt.ion()

pygame.init()
screen = pygame.display.set_mode((MAZE_WIDTH, MAZE_HEIGHT))
clock = pygame.time.Clock()

resize = T.Compose([T.ToPILImage(),
                    T.Resize(40, interpolation=Image.CUBIC),
                    T.ToTensor()])


def get_screen():
    screen1 = array3d(screen).transpose((2, 0, 1))
    screen1 = np.ascontiguousarray(screen1, dtype=np.float32) / 255
    screen1 = torch.from_numpy(screen1)
    return resize(screen1).unsqueeze(0)
