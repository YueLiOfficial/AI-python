import torch
from torch import nn
import matplotlib.pyplot as plt

img = plt.imread("./data/duck.jpg")

input_img = torch.tensor(img, dtype=torch.float).permute(2, 0, 1)

conv = nn.Conv2d(
    3,
    3,
    (9, 9),
    3
)

output = conv(input_img)

output_img = (output - output.min()) / (output.max() - output.min())

output_img = output_img.permute(1, 2, 0).detach()

fig, ax = plt.subplots(1, 2)

ax[0].imshow(img)
ax[1].imshow(output_img)

plt.show()