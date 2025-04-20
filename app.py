import datetime
import streamlit as st
from generator import SuspectSketchGenerator
import torch
import os
import time
import random
import speech_recognition as sr
from audiorecorder import audiorecorder
import whisper
import tempfile
import streamlit as st
# Page configuration
st.set_page_config(
    page_title="AI Suspect Sketch Generator",
    page_icon="🔍",
    layout="wide"
)

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# App title and description
st.title("🔍 AI Suspect Sketch Generator")
st.markdown("Generate suspect sketches from verbal descriptions using AI. This tool helps law enforcement quickly create visual representations based on witness accounts.")

# Initialize session state for storing generated sketches
if 'generated_sketches' not in st.session_state:
    st.session_state.generated_sketches = []

# Initialize the model only once
@st.cache_resource
def load_model():
    return SuspectSketchGenerator()

# Try to load the model with error handling
try:
    generator = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.info("Please check your internet connection and try again. The model needs to be downloaded the first time you run the app.")
    model_loaded = False

# Sidebar for system info and example descriptions
with st.sidebar:
    st.header("System Information")
    device_info = f"Device: {'GPU (CUDA)' if torch.cuda.is_available() else 'CPU'}"
    st.info(device_info)
    
    if torch.cuda.is_available():
        gpu_info = f"GPU: {torch.cuda.get_device_name(0)}"
        memory_info = f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB"
        st.info(gpu_info)
        st.info(memory_info)
    else:
        st.warning("Running on CPU. Sketch generation will be slow (3-5 minutes per sketch).")
    
    # Example descriptions
    st.header("Example Descriptions")
    example_descriptions = [
        "male, early 30s, oval face, short brown hair, thin eyebrows, blue eyes, straight nose, thin lips, clean shaven",
        "female, mid 40s, round face, long blonde hair, thick eyebrows, green eyes, small nose, full lips, high cheekbones",
        "male, late 20s, square jaw, bald, bushy eyebrows, brown eyes, large nose with a bump, thin lips, stubble beard",
        "female, early 20s, heart-shaped face, curly black hair, arched eyebrows, hazel eyes, button nose, full lips",
        "male, late 50s, elongated face, receding gray hair, thick eyebrows, deep-set brown eyes, prominent nose, mustache"
    ]
    
    def use_example_description(description):
        st.session_state.description = description
    
    for i,description in  enumerate(example_descriptions):
        st.button(f"Use: {description[:30]}...", on_click=use_example_description, args=(description,), key=f"example_{i}")

# Main content area - split into two columns
if model_loaded:
    col1, col2 = st.columns([1, 1])

    # Input parameters column
    with col1:
        st.header("Suspect Description")
        
        # Case information
        case_number = st.text_input("Case Number (optional)", value="", help="Enter case number for reference")
        officer_name = st.text_input("Officer Name", value="", help="Enter your name for record-keeping")

        st.subheader("🎤 Or record a verbal description")

        # Record audio with explicit Start/Stop buttons
        audio = audiorecorder("Start Recording", "Stop Recording")

        if len(audio) > 0:
            st.audio(audio.export().read(), format="audio/wav")
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                audio.export(tmpfile.name, format="wav")
                st.info("Transcribing audio to text...")
                try:
                    model = whisper.load_model("base")  # or "tiny" for faster, less accurate
                    result = model.transcribe(tmpfile.name)
                    transcript = result["text"].strip()
                    st.success("Transcription complete!")
                    st.write(transcript)
                    # Button to use transcription as the description
                    if st.button("Use this transcription as description"):
                        st.session_state.description = transcript
                        st.success("Description field updated from audio!")
                except Exception as e:
                    st.error(f"Transcription failed: {e}")
        # Text description
        if 'description' not in st.session_state:
            st.session_state.description = "male, mid 30s, oval face, short brown hair, thick eyebrows, blue eyes, straight nose, thin lips, clean shaven"
            
        description = st.text_area(
            "Suspect Description (be as detailed as possible)",
            value=st.session_state.description,
            height=150,
            help="Describe facial features, age, gender, hair, eyes, nose, mouth, facial hair, etc."
        )
        
        # Feature-specific inputs for more structured description
        with st.expander("Detailed Feature Input (Optional)"):
            st.info("Use these fields to add specific details to your description")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                gender = st.selectbox("Gender", ["Male", "Female"])
                age_range = st.selectbox("Age Range", ["Child (under 12)", "Teen (13-19)", "20s", "30s", "40s", "50s", "60s", "70+"])
                face_shape = st.selectbox("Face Shape", ["Oval", "Round", "Square", "Heart", "Long", "Diamond"])
                eye_color = st.selectbox("Eye Color", ["Brown", "Blue", "Green", "Hazel", "Gray"])
            
            with col_b:
                hair_type = st.selectbox("Hair Type", ["Short", "Medium", "Long", "Bald", "Balding", "Receding"])
                hair_color = st.selectbox("Hair Color", ["Black", "Brown", "Blonde", "Red", "Gray", "White"])
                facial_hair = st.selectbox("Facial Hair", ["None", "Stubble", "Mustache", "Goatee", "Full Beard"])
                distinguishing_features = st.text_input("Distinguishing Features", placeholder="Scars, tattoos, etc.")
            
            # Button to add structured details to the main description
            if st.button("Add to Description"):
                structured_description = f"{gender.lower()}, {age_range.lower()}, {face_shape.lower()} face, {hair_type.lower()} {hair_color.lower()} hair, {eye_color.lower()} eyes"
                
                if facial_hair != "None":
                    structured_description += f", {facial_hair.lower()}"
                
                if distinguishing_features:
                    structured_description += f", {distinguishing_features}"
                
                st.session_state.description = structured_description
                st.rerun()
        
        # Advanced options in an expander
        with st.expander("Advanced Options"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                width = st.select_slider(
                    "Width",
                    options=[512, 576, 640, 704, 768],
                    value=512
                )
                
                num_steps = st.slider(
                    "Detail Level",
                    min_value=20,
                    max_value=50,
                    value=30,
                    help="Higher values produce more detailed sketches but take longer"
                )
            
            with col_b:
                height = st.select_slider(
                    "Height",
                    options=[512, 576, 640, 704, 768],
                    value=512
                )
                
                guidance_scale = st.slider(
                    "Description Adherence",
                    min_value=5.0,
                    max_value=15.0,
                    value=7.5,
                    step=0.5,
                    help="How closely to follow the description (higher = more faithful)"
                )
            
            use_random_seed = st.checkbox("Use random seed", value=True)
            
            if not use_random_seed:
                seed = st.number_input(
                    "Seed",
                    value=42,
                    min_value=0,
                    max_value=2147483647,
                    step=1,
                    help="Random seed for reproducibility"
                )
            else:
                seed = random.randint(0, 2147483647)
                st.info(f"Using random seed: {seed}")
        
        # Generate button
        if st.button("Generate Suspect Sketch", key="generate"):
            if not description.strip():
                st.error("Please enter a suspect description before generating a sketch.")
            else:
                with st.spinner(f"Generating suspect sketch... This may take a while on {'CPU' if not torch.cuda.is_available() else 'GPU'}."):
                    try:
                        # Record start time
                        start_time = time.time()
                        
                        # Generate the sketch
                        image, filename = generator.generate_sketch(
                            description=description,
                            case_number=case_number,
                            height=height,
                            width=width,
                            num_inference_steps=num_steps,
                            guidance_scale=guidance_scale,
                            seed=seed
                        )
                        
                        # Calculate generation time
                        generation_time = time.time() - start_time
                        
                        # Add to session state
                        st.session_state.generated_sketches.append({
                            "image": image,
                            "filename": filename,
                            "description": description,
                            "case_number": case_number,
                            "officer": officer_name,
                            "time": generation_time,
                            "seed": seed,
                            "steps": num_steps,
                            "guidance": guidance_scale,
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Success message
                        st.success(f"Sketch generated in {generation_time:.2f} seconds!")
                        
                    except Exception as e:
                        st.error(f"Error generating sketch: {str(e)}")

    # Results column
    with col2:
        st.header("Generated Sketch")
        
        if st.session_state.generated_sketches:
            # Get the most recent sketch
            latest_sketch = st.session_state.generated_sketches[-1]
            
            # Display the image
            st.image(latest_sketch["image"], caption=f"Suspect Sketch - Case #{latest_sketch['case_number']}", use_column_width=True)
            
            # Sketch metadata
            with st.expander("Sketch Details", expanded=True):
                st.write(f"**Case Number:** {latest_sketch['case_number'] if latest_sketch['case_number'] else 'Not specified'}")
                st.write(f"**Officer:** {latest_sketch['officer'] if latest_sketch['officer'] else 'Not specified'}")
                st.write(f"**Description:** {latest_sketch['description']}")
                st.write(f"**Generated On:** {latest_sketch['timestamp']}")
                st.write(f"**Seed:** {latest_sketch['seed']}")
                st.write(f"**Generation Time:** {latest_sketch['time']:.2f} seconds")
            
            # Download button
            with open(latest_sketch["filename"], "rb") as file:
                st.download_button(
                    label="Download Sketch",
                    data=file,
                    file_name=os.path.basename(latest_sketch["filename"]),
                    mime="image/png"
                )
                
            # Feedback section
            st.subheader("Sketch Feedback")
            feedback = st.radio(
                "How accurate is this sketch based on the description?",
                ["Select an option", "Very Accurate", "Somewhat Accurate", "Needs Refinement", "Not Accurate"]
            )
            
            feedback_notes = st.text_area("Additional feedback or notes about this sketch", height=100)
            
            if st.button("Submit Feedback"):
                st.success("Feedback submitted. This information can help improve future sketches.")
        else:
            # Placeholder when no sketch has been generated
            st.info("The generated suspect sketch will appear here. Enter a description and click 'Generate Suspect Sketch' to create one.")
        
    # Case history section
    if len(st.session_state.generated_sketches) > 1:
        st.header("Case History")
        
        # Display previous generations in reverse order (newest first)
        for i, item in enumerate(reversed(st.session_state.generated_sketches[:-1])):
            case_display = f"Case #{item['case_number']}" if item['case_number'] else f"Sketch {i+1}"
            with st.expander(f"Previous {case_display}: {item['description'][:50]}...", expanded=False):
                st.image(item["image"], use_column_width=True)
                st.write(f"**Description:** {item['description']}")
                st.write(f"**Generated On:** {item['timestamp']}")
                
                # Download button for historical sketches
                with open(item["filename"], "rb") as file:
                    st.download_button(
                        label="Download This Sketch",
                        data=file,
                        file_name=os.path.basename(item["filename"]),
                        mime="image/png",
                        key=f"download_{i}"
                    )

# Footer
st.markdown("---")
st.markdown("**Disclaimer:** This tool is intended for law enforcement use only. AI-generated sketches should be used as investigative aids and not as definitive identifications. All sketches are generated locally - no data leaves your machine.")
