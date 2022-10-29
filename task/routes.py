from fastapi import APIRouter
from model import ImageInput
from PIL import Image
import io, base64
import numpy as np

router = APIRouter()

class CustomException(Exception):
    def __init__(self, details: str):
        self.details = details


def find_cell_size(img):
    """to find cell size function iterates over the second column (the first column contains gridline) starting
    with 2 row (first row has gridline) and going to bottom. When the current cell is white pixel, we check whether
    it is possible that it is part of gridline. If yes, we found the size of the cell. If no, then this white pixel
    is just a part of the cell. Returns the size of the cell"""
    col = 1
    cell_size = 1
    row = 2
    grid_found = False
    while row < img.shape[0] and not grid_found:
        if img[row, col] == 0:
            grid_found = is_cell_size(img, cell_size)
        cell_size += 1
        row += 1
    cell_size-=1
    if grid_found:
        return cell_size
    else:
        return False


def is_cell_size(img, s):
    """checks whether the size of cell in grid is valid. If it is correct then there will be full white gridlines
    on anticipated positions (multiples of cell size). If on at least one row/column, where we expect gridline to be
    was found dark pixel - this size of cell is impossible. Returns the boolean value if the cell size is correct."""
    # checking if there is white grid line in anticipated columns
    h, w = img.shape
    for i in range(0, w//(s+1)):
        if sum(img[:, (1+s)*i]) != 0: #summing whole column
            return False
    # checking if there is white grid line in anticipated rows
    for i in range(0, h//(s+1)):
        if sum(img[(s+1)*i, :]) != 0: #summing whole column
            return False
    return True


def divide_grid(img, s):
    """Divides grid on cells, calculating darkness of each of them. Returns the array with darkness of each cell"""
    h, w = img.shape
    cells_h = h//(s+1) # amount of cells vertically
    cells_w = w//(s+1) # amount of cells horizontally
    cells = np.empty([cells_h, cells_w])
    for i in range(cells_h):
        for j in range(cells_w):
            # coordinates of left-top corner of the cell in image
            img_i = i*(s+1)+1
            img_j = j*(s+1)+1
            # finding mean of pixels of whole cell
            cells[i, j] = np.mean(img[img_i:min(img_i+s,h), img_j:min(img_j+s, w)])
            cells[i, j] *= 100 # converting to the level 0-100
    cells = np.around(cells)
    return cells


def find_mines(cells, min_level):
    """considering the level of each cell, saves the ones with probability higher than min_level and
    returns them in json format"""
    mines = []
    h, w = cells.shape
    for i in range(h):
        for j in range(w):
            if cells[i, j] >= min_level:
                mine = {}
                mine['x'] = j
                mine['y'] = i
                mine['level'] =  cells[i, j]
                mines.append(mine)
    return mines


def darkness(pixel):
    """returns darkness of pixel as number between 0 and 1.
    0 - white. 1 - black"""
    return 1-pixel/255


def raise_exception(details_string: str):
    raise CustomException(
        details=details_string
    )


@router.post("/image-input", status_code=200)
async def read_image(image_data: ImageInput) -> dict:
    if image_data.min_level > 100 or image_data.min_level < 0:
        raise_exception("Invalid provided minimum level data.")
    try:
        base64_str = image_data.image.replace("data:image/png;base64,", "")
        img_array = np.array(Image.open(io.BytesIO(base64.decodebytes(bytes(base64_str, "utf-8")))))
        print(img_array.shape)
    except:
        raise_exception("Unprocessable image.")
    h, w = img_array.shape[:2]
    bw_img = np.empty([h, w])
    for row in range(h):
        for col in range(w):
            pixel = 0
            if len(img_array.shape) == 3:
                pixel = np.mean(img_array[row, col])
            else:
                pixel = img_array[row, col]
            bw_img[row, col] = darkness(pixel)
    bw_img = np.around(bw_img, decimals=5)
    # finding the size of the cell in the grid
    cell_size = find_cell_size(bw_img)
    if cell_size == False:
        raise_exception("The provided image has no grid.")
    # dividing grid on cells and calculating their darkness
    cells = divide_grid(bw_img, cell_size)
    # checking if cell may contain mine
    mines = find_mines(cells, image_data.min_level)
    return mines