#IMPORT LIBRARIES
from flask import Flask, render_template, request
from PIL import Image

# Convert an RGB color tuple to a HEX color code
def rgb2hex(color):

    r=color[0]
    g=color[1]
    b=color[2]

    return "#{:02x}{:02x}{:02x}".format(r,g,b)

# Extract the 10 most common colors from an image
def get_colors(file_path):

    # Open an image and ensure RGB mode
    img = Image.open(file_path).convert("RGB")

    # Get colors with a custom maxcolors limit
    colors = img.getcolors(maxcolors=1000000)

    # Sort colors by pixel count, from most to least common
    colors = sorted(colors, reverse=True)
    top_10 = colors[:10]

    # Calculate the total number of pixels in the image
    total_pixels = img.size[0] * img.size[1]

    # Store the processed color information
    colors = []

    for color in top_10:
        color_rgb= color[1]
        color_value = color[0]
        # Convert the RGB value to HEX
        color_hex = rgb2hex(color_rgb)
        # Calculate what percentage of the image is this color
        color_procent = color_value/total_pixels*100

        color_data = {
            "color_rgb":color_rgb,
            "color_procent":color_procent,
            "color_hex":color_hex,
        }
        colors.append(color_data)
    return colors

app = Flask(__name__)

# Display the homepage with the default example image
@app.route('/')
def home():
    file_path = "example.jpg"
    # Extract the most common colors from the example image
    colors = get_colors(f"static/{file_path}")
    return render_template('index.html',colors=colors,file_path="example.jpg")

# Handle image uploads
@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded image from the form
    file = request.files['image']
    # Check if the user submitted the form without selecting an image
    if file.filename  == '':
        return render_template(
            "index.html",
            error="Please select an image before uploading.")
    # Save the uploaded image to the static folder
    file.save("static/user_upload.jpg")
    file_path = "user_upload.jpg"
    # Extract the most common colors from the uploaded image
    colors = get_colors(f"static/{file_path}")
    # Display the results using the uploaded image
    return render_template("index.html",colors=colors,file_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)
