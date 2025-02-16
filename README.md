# 3D_VLM_Captions

## Overview
A code that generates captions for your 3D model. The process is divided into three phases to ensure a smooth workflow from 3D model processing to caption generation.

## Uncut Video Demonstration
[Watch the demonstration on YouTube](https://youtu.be/Wop6hv2dUaE)

## Usage Instructions

### Step 1: Prepare Your 3D Model
- Place your desired 3D model in .STL format inside the **STL_Files** directory.

### Step 2: Run the Script
- Run `main.py` and follow the prompts.

### Step 3: Model Name Input
- When prompted, type the name of the model (e.g., "Panda.STL").

### Step 4: Wait for Phases to Complete
- Wait for **Phase1**, **Phase2**, and **Phase3** to finish processing, which will generate the desired output.

## Code Design

## Phase 1: 3D Model Setup in Blender
- **Initializes the environment in Blender using bpy**
- **Coordinates Calculation**: Determines the X, Y, Z midpoint of the 3D model
- **Scene Initialization**: Clears any previous objects (meshes, lights, cameras)
- **Lighting Setup**: Adds light sources at specific coordinates
- **Camera Setup**: Adds cameras at predefined positions
- **Snapshot Creation**: Captures snapshots from 14 different camera angles and saves them to the specified directory

### Camera and Light Positions
Detailed descriptions for the **Face Cameras**, **Light Sources**, and **Vertex Cameras** used for the snapshots.

## Phase 2: Caption Generation Using VLM
- **VLM Integration**: Uses OpenRouter with Google Gemini 2.0 to generate captions for all 14 images.
- **Flexible Model Choice**: Google Gemini 2.0 Flash is used by default, but the model can be swapped as needed.

## Phase 3: Summary Caption Generation
- **Caption Summarization**: Google Gemini 2.0 processes the captions from all 14 snapshots and generates a comprehensive caption summarizing the entire 3D model.

## main.py: Script Flow
- Executes all phases in sequential order: **Phase 1**, **Phase 2**, **Phase 3**.

## config.py: Centralized Directory Management
- Ensures easy communication of directory paths across all three phases to maintain a centralized approach and prevent issues caused by Blender's independent Python environment.

## MIT.env FLAG Usage
- The **FLAG** in **MIT.env** ensures smooth transitions between phases. It ensures that **Phase1** completes before **Phase2** begins, and so on, by tracking when each phase finishes.

![Face Camera 4 (Skull)](https://github.com/Sukanth-Original/3D_VLM_Captions/blob/main/skull/face_images/faceCamera4.png?raw=true)

![Vertex Camera 2 (Skull)](https://github.com/Sukanth-Original/3D_VLM_Captions/blob/main/skull/vertex_images/vertexCamera2.png?raw=true)

2 out of 14 images.

Output: "This 3D rendered model presents a human skull, crafted with anatomical accuracy. The object is depicted with a neutral gray aesthetic, indicative of a wireframe, or shaded model, emphasizing the bone structure without extraneous color or texture. The viewpoint is slightly oblique, offering a detailed perspective of the cranium, orbital cavities, nasal aperture, and the articulated mandible displaying the teeth. The lighting is subtle, rendering soft shadows for depth perception, and revealing surface contours. The absence of external or internal supporting structures suggests a standalone digital model, potentially designed for educational, medical, or artistic purposes. The environment is a plain monochromatic backdrop.


![Face Camera 1](https://github.com/Sukanth-Original/3D_VLM_Captions/blob/main/Panda/face_images/faceCamera1.png?raw=true)

![Vertex Camera 2](https://github.com/Sukanth-Original/3D_VLM_Captions/blob/main/Panda/vertex_images/vertexCamera2.png?raw=true)

2 out of 14 images.

Output: "This 3D model is a stylized bear rendering, constructed from simplified geometric primitives suggesting a low-poly aesthetic. The design utilizes rounded forms for the head and limbs, contrasting with the overall segmented body. The model is viewed from a reclined position, showcasing a top-down perspective. The surface material appears uniform with a grayscale rendering and diffuse shading, which highlights the forms and structural integrity. Absence of textures aids in visualizing the underlying geometry. The lack of color and detailed surfacing suggests a focus on form over photorealism.
"

"


---
