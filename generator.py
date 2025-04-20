import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from PIL import Image
import os
import datetime

class SuspectSketchGenerator:
    def __init__(self):
        """Initialize the Stable Diffusion model for suspect sketching."""
        print("Initializing Suspect Sketch Generator...")
        
        # Create output directory
        os.makedirs("generated_sketches", exist_ok=True)
        
        # Determine device (CPU or GPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load the model
        try:
            print("Loading Stable Diffusion model...")
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "CompVis/stable-diffusion-v1-4",  # Using v1-4 as it has fewer access restrictions
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None
            )
            
            # Use better scheduler for faster inference
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.pipe.scheduler.config
            )
            
            # Move to device
            self.pipe = self.pipe.to(self.device)
            
            # Enable memory optimization if using GPU
            if self.device == "cuda":
                self.pipe.enable_attention_slicing()
                print("Attention slicing enabled for memory optimization")
            
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
        
    def generate_sketch(self, description, case_number="", height=512, width=512, 
                      num_inference_steps=30, guidance_scale=7.5, seed=None):
        """Generate a suspect sketch based on the text description."""
        # Set seed for reproducibility if provided
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)
        else:
            generator = None
            
        # Enhance the prompt for police sketch generation
        prompt = f"police forensic photo generator, front view portrait of {description}, realistic detailed color photo, neutral background, clear facial features. Generate only one face at the center of the generated image."
        
        # Negative prompt to avoid unrealistic elements
        negative_prompt = "unrealistic, cartoon, anime, 3d, painting, deformed, blurry, low quality, distorted features, extra fingers, extra limbs, disfigured"
            
        # Generate the image
        print(f"Generating suspect photo based on description: {description}")
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            height=height,
            width=width,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator
        )
        
        # Save the image
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        case_suffix = f"_{case_number}" if case_number else ""
        filename = f"generated_sketches/suspect{case_suffix}_{timestamp}.png"
        image = result.images[0]
        image.save(filename)
        
        print(f"Sketch saved as {filename}")
        return image, filename
