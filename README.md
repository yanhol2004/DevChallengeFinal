# DevChallenge Final Round
This repository contains my submission for the DevChallenge final round, where I secured 3rd place overall. You can find the task description [here](https://docs.google.com/document/d/1QuUdFZ3fPTpMuq6sk1urZyVMuxt4nTVOD9-z69jk2M4/edit). 

Below are the instructions to run the code, along with an explanation of my algorithm and the reasoning behind specific design choices.
## Short task summary
This task involves processing grayscale PNG images representing remote scans, where darker cells indicate higher probabilities of mines. The image has a white coordinate grid with each cell starting from (0,0) at the top left. The API takes a base64-encoded image and a min_level (0-100) threshold, returning a list of cells with probabilities of mines higher than the given threshold.
**Example of the input image:**

<img width="351" alt="image" src="https://github.com/user-attachments/assets/464c0ccf-a3ce-4eb6-9932-26b69e9dcbd0">


## Short explanation of the solution
The program receives images through API endpoint, converts them to grayscale, and stores the image data in a NumPy array for memory efficiency and ease of manipulation. Then it finds the grid by iterating through the image, identifying white pixels to determine the grid structure, and handles multiple grid variations. If no grid is found, an error is returned. Once the grid is detected, the program calculates the darkness level of each cell (which constists of multiple greyscale pixels), returns the probability of mines, and filters cells based on a minimum level threshold.



##  How to run the application
To start the service in the directory with the docker-compose file, execute the terminal command "docker-compose up."
##  How to run the tests
    1. Run docker-compose up
    2. Open the docker container Terminal Console
    3. Run "pytest" command

## Implementation

### Input of data
- The program is designed to read both greyscale and colored RGB images(transferring them to greyscale).
- Then, image data is saved to the numpy array. Numpy was chosen over regular Python lists because
they occupy much less memory (an advantage for saving big images) and are generally designed to work with big data.
Also, it simplifies the code, as numpy has more tools to operate on the array.
- After reading the image, the greyscale value 0-255 is converted to the darkness of each pixel, with 0 being white and 1 being black
### Finding the grid on the input image
- To find a grid, the function iterates over the second column, starting with the second row and going down. With every white pixel found, the function checks whether it may be part of the grid. If yes - we found a grid if no -
this pixel was just part of the cell.
- Because of that, if there are few possible grid variations, the program will find the grid with the lowest possible cell size. For example, if a full white picture is provided, the program will find a grid with each cell being 1 pixel in size.
- if the grid was not found, the program responds with an error message with details of grid absence provided
### Computing results
When the cell size in the grid is defined, we operate with loops, slicing the image array and finding its elements mean (numpy flattens two-dimensional array). So we have a new array with the darkness of each cell(mean of the darkness of its pixels), which is multiplied by 100 to get the level of probability that mine is there and then rounded to the nearest integer. Then, the program constructs JSON response with those cells whose level was >= minimum level provided. The indexes returned are those of the cells themselves.

## Possible improvements
- In the worst case, finding the gridline will operate O(n^3) in the case when the second column has all white pixels, and the program will run gridline checking in each of them. This could be improved by iterating over column/row with the least white pixels. (Though finding such row/column may also be complex in terms of time)

- The next improvements could also include adapting a program for finding grids with cells that are rectangles. This can be implemented by iterating over all white cells and checking whether the found cell can be part of the gridline. The smart choice of order for iterating over white cells can improve the time complexity of the suggested approach.

- Also, there is room for improvement in memory usage to improve efficiency with big images.

- Additionally, we may cache images to handle requests on the same image but with different min_level faster.
