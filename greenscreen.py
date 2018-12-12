###
### Author: Faye Bandet
### Description: This is a program that can combine a still image with a green, blue, or red screen, with a background (or fill) image.
###
def get_image_dimensions_string(file_name):
    '''
    Given the file name for a valid PPM file, this function will return the
    image dimensions as a string. For example, if the image stored in the
    file is 150 pixels wide and 100 pixels tall, this function should return
    the string '150 100'.
    file_name: A string. A PPM file name.
    '''
    image_file = open(file_name, 'r')
    image_file.readline()
    return image_file.readline().strip('\n')

def load_image_pixels(file_name):
    ''' Load the pixels from the image saved in the file named file_name.
    The pixels will be stored in a 3d list, and the 3d list will be returned.
    Each list in the outer-most list are the rows of pixels.
    Each list within each row represents and individual pixel.
    Each pixels is representd by a list of three ints, which are the RGB values of that pixel.
    '''
    pixels = []
    image_file = open(file_name, 'r')
    image_file.readline()
    image_file.readline()
    image_file.readline()
    width_height = get_image_dimensions_string(file_name)
    width_height = width_height.split(' ')
    width = int(width_height[0])
    height = int(width_height[1])
    for line in image_file:
        rgb_row = line.strip().split(' ')
        row = []
        for i in range(0, len(rgb_row), 3):
            pixel = [int(rgb_row[i]), int(rgb_row[i+1]), int(rgb_row[i+2])]
            row.append(pixel)
        pixels.append(row)
    return pixels

def implement_greenscreen(loaded_fi, loaded_gs, channel_difference, channel):
    if channel == 'r':
        c = 0
    elif channel == 'g':
        c = 1
    elif channel == 'b':
        c = 2
    for i in range(len(loaded_fi)):
        for j in range(len(loaded_fi[i])):
            if (loaded_gs[i][j][c]) > (loaded_gs[i][j][(c + 1) % 3] * channel_difference) \
            and (loaded_gs[i][j][c]) > (loaded_gs[i][j][(c + 2) % 3] * channel_difference):
                loaded_gs[i][j] = loaded_fi[i][j]
    return loaded_gs
    
def write_new_file(out_file, greenscreen_image, gs_file):
    out_file = open(out_file, 'w')
    ### Saves the new image to a file.
    image_file = open(gs_file, 'r')
    out_file.write(image_file.readline())
    out_file.write(image_file.readline())
    out_file.write(image_file.readline())
    for row in greenscreen_image:
        for pixel in row:
            out_file.write(str(pixel[0]) + ' ' + str(pixel[1]) + ' ' + str(pixel[2]) + ' ')
        out_file.write('\n')    
    out_file.close()
    print('Output file written. Exiting.')

from os import _exit as exit
def main():
    # Get the 5 input values from the user, as described in the specification
    # Check for valid inputs
    channel = input('Enter color channel \n')
    if channel != 'r' and channel != 'g' and channel != 'b':
        print('Channel must be r, g, or b. Will exit.')
        exit()
    channel_difference = float(input('Enter color channel difference \n'))
    if channel_difference > 10.0 or channel_difference < 1.0:
        print('Invalid channel difference. Will exit.')
        exit()
    gs_file = input('Enter greenscreen image file name \n')
    fi_file = input('Enter fill image file name \n')
    ### Compare dimensions to check if image files are the same size.
    gs_file_dimension = get_image_dimensions_string(gs_file)
    fi_file_dimension = get_image_dimensions_string(fi_file)
    if gs_file_dimension == fi_file_dimension:
        out_file = input('Enter output file name \n')
        if '.ppm' not in out_file:
            print('Error')
            exit()
        loaded_gs = load_image_pixels(gs_file)
        loaded_fi = load_image_pixels(fi_file)
    ### If the the input is valid, implement the greenscreen.
        greenscreen_image = implement_greenscreen(loaded_fi, loaded_gs, channel_difference, channel)
        write_new_file(out_file, greenscreen_image, gs_file)
    else:
        print('Images not the same size. Will exit.')
        exit()
main()