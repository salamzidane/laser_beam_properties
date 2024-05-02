import os
import numpy as np
import tifffile
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def read_input(input_file):
    with open(input_file, "r") as f:
        directory = f.readline().strip()
        sensor_size_x_mm = float(f.readline().strip())
    return directory, sensor_size_x_mm

def load_images(directory):
    images = []
    for filename in os.listdir(directory):
        
        if filename.endswith(".tiff"):
            filepath = os.path.join(directory, filename)
            image = tifffile.imread(filepath)
            images.append(image)
    
    return images

def calculate_pixel_size(sensor_size_x_mm, image_width_px):
    return convert_mm_to_um(sensor_size_x_mm) / image_width_px

def convert_mm_to_um(sensor_size_mm):
    return sensor_size_mm * 1000
      


def gaussian(x, amplitude, mean, stddev, background):
    return amplitude * np.exp(-((x - mean) / stddev)**2 / 2) + background


def fit_gaussian(axis_values, data):
    #[ampltude, x0,sigma, backgrund]
    guesses = [np.max(data), np.argmax(data), 0.2,np.min(data)]
    lower_bound = (0, 0, 0, 0)
    upper_bound = (np.inf, len(data), np.inf, np.inf)
    popt, _ = curve_fit(gaussian, axis_values, data, p0=guesses,bounds=(lower_bound, upper_bound))
    return popt[2], popt[1]




def calculate_beam_properties(sensor_size_x_mm, pixel_size_um, sigma_px):
    beam_size_um = 2 * sigma_px * pixel_size_um
    return beam_size_um



def calculate_beam_center(gaussian_parameters):
    return gaussian_parameters[1]

def calculate_pointing_stability(beam_centers):
    mean_position = np.mean(beam_centers)
    squared_diff = (beam_centers - mean_position)**2
    rms = np.sqrt(np.mean(squared_diff))
    return rms

def main():
    input_file = "input.txt"
    output_file = "Beam_Size_measurement_results.txt"

    directory, sensor_size_x_mm = read_input(input_file)
    images = load_images(directory)
    pixel_size_um = calculate_pixel_size(sensor_size_x_mm, images[0].shape[1])
 



    beam_centers_x = []
    beam_centers_y = []
    beam_size_x = []
    beam_size_y = []
 
    
  
    for idx, image in enumerate(images):
        #calculate beam size x and y
        sum_over_columns = np.sum(image, axis=0)
        sum_over_rows = np.sum(image, axis=1)
        sigma_x_px, mean_x_px = fit_gaussian(np.arange(len(sum_over_columns)), sum_over_columns)
        sigma_y_px, mean_y_px = fit_gaussian(np.arange(len(sum_over_rows)), sum_over_rows)
        beam_size_x_um = calculate_beam_properties(sensor_size_x_mm, pixel_size_um, sigma_x_px)
        beam_size_y_um = calculate_beam_properties(sensor_size_x_mm, pixel_size_um, sigma_y_px)

        #save the relevant values
        beam_centers_x.append(mean_x_px)
        beam_centers_y.append(mean_y_px)

        beam_size_x.append(beam_size_x_um)
        beam_size_y.append(beam_size_y_um)
        
      cd ..

              

            
    beam_position_x_um = np.mean(beam_centers_x)
    beam_position_y_um = np.mean(beam_centers_y)
    beam_size_x_um = np.mean(beam_size_x)
    beam_size_y_um = np.mean(beam_size_y)
    pointing_stability_x_um = calculate_pointing_stability(np.array(beam_centers_x))*pixel_size_um
    pointing_stability_y_um = calculate_pointing_stability(np.array(beam_centers_y))*pixel_size_um
    pointing_stability_r_um = np.sqrt(pointing_stability_x_um**2 + pointing_stability_y_um**2)

   
    


    with open(output_file, 'w') as f:
        f.write(f"Beam size x in micrometers = {beam_size_x_um:.2e}\n")
        f.write(f"Beam size y in micrometers = {beam_size_y_um:.2e}\n")
        f.write(f"Pointing stability in axis x in micrometers = {pointing_stability_x_um:.1f}\n")
        f.write(f"Pointing stability in axis y in micrometers = {pointing_stability_y_um:.1f}\n")
        f.write(f"Pointing stability in axis r in micrometers = {pointing_stability_r_um:.1f}\n")
        f.write(f"Beams average x position in pixels = {np.mean(beam_position_x_um):.2e}\n")
        f.write(f"Beams average y position in pixels = {np.mean(beam_position_y_um):.2e}\n")
        f.write(f"Pixel size in micrometers = {pixel_size_um:.1f}\n")
        f.write(f"Name of the directory of the images = {directory}\n")
        
        
      
        
        

        
  

