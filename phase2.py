# Phase2:

import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
from config import config_file_path


# Load environment variables
load_dotenv("MIT.env")

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)



def encode_image(image_path):
    """Convert image to base64 with error handling"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"\n Error encoding {image_path}: {str(e)}")
        return None

def process_images(directory, obj_type, total_count):
    """Process images and generate captions"""
    descriptions = []
    try:
        images = sorted([img for img in os.listdir(directory) 
                       if img.lower().endswith(('.png', '.jpg', '.jpeg'))])
        
        print(f"\nFound {len(images)}/{total_count} {obj_type} images in {directory}")
        
        for idx, img in enumerate(images, 1):
            img_path = os.path.join(directory, img)
            print(f"\n Processing {obj_type[:-1]} {idx}: {img}")
            
            base64_image = encode_image(img_path)
            if not base64_image:
                continue
                
            try:
                completion = client.chat.completions.create(
                    model="google/gemini-2.0-flash-lite-preview-02-05:free",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"Angle from {idx} of {total_count} {obj_type} of the 3D Model. Generate a 50-word technical caption"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }],
                    timeout=30
                )
                
                caption = completion.choices[0].message.content.strip('"')
                descriptions.append(f'Angle from {idx} of {total_count} {obj_type}: "{caption}"\n')
                print(f" Success: Caption {idx}/{total_count} generated")
                
            except Exception as e:
                print(f" API Error: {str(e)}")
                descriptions.append(f'Angle from {idx} of {total_count} {obj_type}: "Caption generation failed"\n')
        
        return descriptions
    
    except Exception as e:
        print(f"Critical error: {str(e)}")
        return []

def phase2_py():
    # Configuration
    from config import config_file_path
    file_path = config_file_path
    output = []
    
    print("Starting Caption Generator")
    
    # Verify environment file
    if not os.path.exists("MIT.env"):
        print("\n ERROR: MIT.env file not found in script directory!")
        exit(1)
        
    # Verify API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("\n ERROR: Add OPENROUTER_API_KEY to MIT.env!")
        exit(1)
    
    # Process vertices
    vertex_dir = os.path.join(file_path, "vertex_images")
    if os.path.exists(vertex_dir):
        output += process_images(vertex_dir, "Vertices", 8)
    else:
        print(f"\n Missing vertex_images directory: {vertex_dir}")
    
    # Process faces
    face_dir = os.path.join(file_path, "face_images")
    if os.path.exists(face_dir):
        output += process_images(face_dir, "Faces", 6)
    else:
        print(f"\n Missing face_images directory: {face_dir}")
    
    # Save output
    if output:
        output_path = os.path.join(file_path, "output_desc.txt")

        
        output_dir = config_file_path
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
        output_path = os.path.join(output_dir, "output_desc.txt")

        try:
            with open(output_path, "w") as f:
                f.writelines(output)
            print(f"\n Saved {len(output)} descriptions to: {output_path}")
        except Exception as e:
            print(f"\n Failed to save output: {str(e)}")
    else:
        print("\n No descriptions generated!")
    
    print("\nProcess completed")




# End of Phase2 - A Sukanth Original Design