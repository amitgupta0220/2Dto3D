import torch
import os
import sys
from flask import Flask, request, send_file
from PIL import Image
from torchvision import transforms
from flask_cors import CORS
# Add Pix2Vox path to sys.path
sys.path.append(os.path.join(os.getcwd(), 'Pix2Vox'))

# Import the Pix2Vox model
from models.pix2vox_model import Pix2VoxModel
from config import cfg


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

def remove_module_prefix(state_dict):
    """Removes 'module.' prefix from keys in state_dict if necessary."""
    new_state_dict = {}
    for key, value in state_dict.items():
        if key.startswith("module."):
            new_state_dict[key[7:]] = value  # Remove the 'module.' prefix
        else:
            new_state_dict[key] = value
    return new_state_dict

# Load the pretrained model
def load_model():
    model = Pix2VoxModel(cfg)
    checkpoint_path = 'Pix2Vox/checkpoints/Pix2Vox-A-ShapeNet.pth'
    
    # Load the checkpoint
    checkpoint = torch.load(checkpoint_path, map_location='cpu')
    
     # Remove 'module.' prefix from the state dict keys
    encoder_state_dict = remove_module_prefix(checkpoint['encoder_state_dict'])
    decoder_state_dict = remove_module_prefix(checkpoint['decoder_state_dict'])
    refiner_state_dict = remove_module_prefix(checkpoint['refiner_state_dict'])
    merger_state_dict = remove_module_prefix(checkpoint['merger_state_dict'])

    # Load the weights for each component
    model.encoder.load_state_dict(encoder_state_dict)
    model.decoder.load_state_dict(decoder_state_dict)
    model.refiner.load_state_dict(refiner_state_dict)
    model.merger.load_state_dict(merger_state_dict)

    model.eval()  # Set the model to evaluation mode
    return model

# Preprocess the image for the model
def preprocess_image(img):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize image to 224x224
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])  # Normalize to match training settings
    ])
    return transform(img)

# Convert the voxel grid to a 3D mesh using Marching Cubes
def voxel_to_mesh(voxels):
    from skimage import measure
    verts, faces, normals, values = measure.marching_cubes(voxels.squeeze().cpu().numpy(), level=0.1)
    return verts, faces

# Save the 3D mesh to an OBJ file
def save_mesh_as_obj(verts, faces, output_path):
    with open(output_path, 'w') as f:
        # Write vertices
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        
        # Write faces (OBJ indexing starts at 1)
        for face in faces:
            f.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")

# Flask route for uploading the image and getting the OBJ file
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image uploaded!', 400

    file = request.files['image']
    img = Image.open(file.stream).convert('RGB')

    # Preprocess the image
    input_tensor = preprocess_image(img).unsqueeze(0).unsqueeze(0)  # Add batch and view dimensions

    # Run inference
    with torch.no_grad():
        output = model(input_tensor)

    # Convert the output to a 3D OBJ file
    verts, faces = voxel_to_mesh(output)
    output_path = 'output/model.obj'
    save_mesh_as_obj(verts, faces, output_path)

    # Send the OBJ file as a response
    return send_file(output_path, mimetype='application/octet-stream', as_attachment=True, attachment_filename='model.obj')

# Initialize the model when the server starts
model = load_model()

# Run the Flask app
if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)  # Ensure output directory exists
    app.run(debug=True)
