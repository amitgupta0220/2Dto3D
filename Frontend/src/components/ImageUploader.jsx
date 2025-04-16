import { useState } from "react";
import ObjectViewer from "./ObjectViewer"; // Component for 3D object rendering

// eslint-disable-next-line react/prop-types
const ImageUploader = ({ onUploadComplete }) => {
  const [image, setImage] = useState(null);
  const [objUrl, setObjUrl] = useState(null); // Store the OBJ file URL
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    setImage(URL.createObjectURL(e.target.files[0])); // Preview the image
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("image", e.target.files[0]);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const blob = await response.blob();
      const objUrl = URL.createObjectURL(blob);
      setObjUrl(objUrl); // Save OBJ URL to display 3D model
      onUploadComplete(objUrl);
    } catch (error) {
      console.error("Error uploading the image:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold mb-2">
          Upload an image to generate a 3D model
        </h1>
        <p className="text-lg text-gray-600">
          Preview the image and the generated 3D object below
        </p>
      </div>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center space-y-4"
      >
        <input
          type="file"
          onChange={handleImageChange}
          accept="image/*"
          className="py-2 px-4 bg-white shadow-sm rounded-lg border"
        />
        <button
          type="submit"
          className={`px-6 py-2 bg-blue-500 text-white rounded-lg ${
            loading ? "opacity-50 cursor-not-allowed" : ""
          }`}
          disabled={loading}
        >
          {loading ? "Processing..." : "Upload Image"}
        </button>
      </form>

      {image && objUrl && (
        <div className="mt-12 flex space-x-8">
          {/* Display Uploaded Image */}
          <div className="w-1/2">
            <h2 className="text-xl font-bold mb-4">Uploaded Image</h2>
            <img
              src={image}
              alt="Uploaded"
              className="w-full h-auto rounded-lg shadow-lg"
            />
          </div>

          {/* Display 3D Object */}
          <div className="w-1/2">
            <h2 className="text-xl font-bold mb-4">Generated 3D Model</h2>
            <ObjectViewer objUrl={objUrl} />
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
