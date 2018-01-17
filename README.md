# opencv_raster_cleanup
A small script for making areas of a jpeg or png image transparent. Looks for white in the four corners and floodfills with pink if found, and then masks and makes that area transparent and saves the new image as png.
