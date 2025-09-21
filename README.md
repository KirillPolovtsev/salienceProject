# salienceProject
Project for CS 4485 for content-based prediction of 360 degree viewports. A python 360 degree video viewer that projects an equirectangular video onto a virtual sphere and renders a user navigable perspective using a pinhole camera model.

---
## Features
- Load equirectangular .mp4 360 degree videos
- Project video frames onto a sphere using ray sampling
- Pinhole camera model with FOV control
- Interactive navigation using 'WASD':
  - 'W' Pitch Up
  - 'S' Pitch Down
  - 'A' Yaw Left
  - 'D' Yaw Rgiht
- ESC quits the viewer

#Dependencies
-opencv
-numpy

-Using the stanford 360 video dataset from: https://vhil.stanford.edu/downloads/360data
