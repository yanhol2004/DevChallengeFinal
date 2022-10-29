1. HOW TO RUN APPLICATION
To start the service in the directory with the docker-compose file, execute the terminal command "docker-compose up"

2. HOW TO RUN TESTS
    1. Run docker-compose up
    2. Open docker container Terminal Console
    3. Run "pytest" command

3. IMPLEMENTATION

A) INPUT OF DATA
    Program is designed to read both greyscale and coloured RGB images(transferring them to greyscale).
    Then image data is saved to the numpy array. Numpy was chosen over regular python lists for the reason that
    they ocuppy much less memory (advantage for saving big images), and generally designed to work with big data.
    Also it simplifies the code, as numpy has more tools to operate on array.
    After reading the image the greyscale value 0-255 is converted to the darkness of each pixel with 0 being white, and 1 being black
B) FINDING GRID
    To find a grid function iterates over second column starting with second row, going down. With every white pixel found, function check whether it is possible that it is part of the grid. If yes - we found grid, if no -
    this pixel was just part of the cell.
    Because of thet, if there are few possible variations of grid, program will find the grid with lowest possible cell size. For example provided full white picture, program will find grid with each cell being 1 pixel size.
    if the grid was not found, program responses with error message with details of grid absense provided
C) FINDING RESULTS
    When the size of cell in the grid is defined, we operate with loops, slicing the image array, and finding its elements mean (numpy flattens two dimensional array). So that we have new array with the darkness of each cell(mean of darkness of its pixels), which are multiplied by 100 to get level of probability that mine is there, and then rounded to the nearest integer. During the operation of program all darkness values are stored with precision to 5 digits. Then program constructs json response with those cells whose level was >= minimum level provided. The indexes returned are those of the cells themselves.

4. POSSIBLE IMPROVEMENTS
    In worst case finding gridline will operate O(n^3), in case when the second column has all white pixels, and program will run gridline checking in each of them. This could be improved by iterating over column/row, that has the least amount of white pixels. (Though finding such row/column may also be complex in terms of time)

    Next improvements could also be adapting program for finding grid with cells being rectangles. This can be implemented with iterating over all white cells, and checking whether found cell can be the the part of gridline. The smart choice of order how to iterate over white cells can improve the time complexity of the suggested approach.

    Also there is room for improvement in memory usage, to improve efficiency with big images.

    Additionaly, we may cache images to handle requestes on the same image but with different min_level faster.