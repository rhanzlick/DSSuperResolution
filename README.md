# DSSuperResolution
This project implements the classic Diamond-Square fractal algorithm to perform image superresolution.
Using a linear interpolation variant, the algorithm - in its current form - will increase height and width by a factor of 2.
Currently it works on both greyscale and RGB images.

# CLI
The algorithm is wrapped in a lightweight CLI implemented with argparse called upscale.py.
See the upscale.py help options for usage.

# Sample Image
The repo contains a sample image used for testing.

# Notes
The algorithm will throw an exception for images where any dimension is larger than 13,000
