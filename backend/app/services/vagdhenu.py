from pathlib import Path 
import json
import uuid 
import subprocess 
import os 
import sys 

#Locate the external Vagdhenu repository

# __file__ points to:
# peaceful-shlokas-ai/backend/app/services/vagdhenu.py
#
# parents[3] takes us back to:
# peaceful-shlokas-ai/

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Vāgdhenu currently lives beside our portfolio project:
#
# AI_voice_models_indic/
# ├── peaceful-shlokas-ai/
# └── vagdhenu/
VAGDHENU_ROOT = PROJECT_ROOT.parent /"vagdhenu"

# ---------------------------------------------------------
# Helper functions for checking the Vāgdhenu installation
# ---------------------------------------------------------


def get_vagdhenu_path() -> Path:
    """Return the path to the local Vagdhenu repo."""
    return VAGDHENU_ROOT 

def is_vagdhenu_available() ->bool:
    """Check whether Vāgdhenu's render script exists."""
    render_script = VAGDHENU_ROOT / "src" / "render.py"
    return render_script.exists()

# ---------------------------------------------------------
# Generate Sanskrit chant audio using Vāgdhenu
# ---------------------------------------------------------

def generate_chant(text: list[str]):

    #Create a unique ID for this generation request.
    #
    #This prevents different requests from using the same
    #filename and will later allow us to track individual jobs.

    job_id = str(uuid.uuid4())

     # -----------------------------------------------------
    # Build the inference request expected by Vāgdhenu
    # -----------------------------------------------------

    # Vāgdhenu expects a list of generation jobs.
    #
    # "padas" contains the individual lines of the Sanskrit verse.
    # For now we use the anushtubh meter and a fixed seed.


    job_data = [
        {
            "id":job_id,
            "meter":"anushtubh",
            "padas":text,
            "seed":60,
            "no_sandhi":True
        }
    ]

    # -----------------------------------------------------
    # Save the request as JSON
    # -----------------------------------------------------

    # Create a unique request file inside the Vāgdhenu repository.


    request_file = VAGDHENU_ROOT / f"request_{job_id}.json"

    with open(request_file,"w", encoding="utf-8") as f:
        json.dump(job_data, f, ensure_ascii=False, indent=2)

    print("Created:",request_file)

    # -----------------------------------------------------
    # Configure BigVGAN
    # -----------------------------------------------------

    # Vāgdhenu uses NVIDIA BigVGAN as its neural vocoder.
    # BigVGAN converts the model's generated acoustic
    # representation into the final audio waveform.

    bigvgan_path = VAGDHENU_ROOT / "BigVGAN"

    # Copy the current process environment so the subprocess
    # keeps variables such as PATH and the active Conda environment.

    env = os.environ.copy()

    # Add the cloned BigVGAN repository to PYTHONPATH.
    #
    # This allows render.py to successfully run:
    #
    #     import bigvgan
    #
    # without permanently modifying the user's system PYTHONPATH.

    env["PYTHONPATH"] = (
        str(bigvgan_path)
        + os.pathsep
        + env.get("PYTHONPATH", "")
    )

    # -----------------------------------------------------
    # Run Vāgdhenu inference
    # -----------------------------------------------------

    # Launch Vāgdhenu's render.py as a separate Python process.
    #
    # sys.executable ensures that the subprocess uses the same
    # Python environment as this application. During development,
    # we therefore run this project from the "vagdhenu" Conda env.

    result = subprocess.run(
        [
            sys.executable,
            "src/render.py",
            "--shard",
            str(request_file),
            "--results",
            "results.json",
            "--outdir",
            "out"
        ],
        # Run the command from inside the Vāgdhenu repository
        # because render.py expects paths relative to that project.
        cwd = VAGDHENU_ROOT,

        #Pass our modified environment containing BigVGAN.
        env = env,

        #Captured stdout and stderr so our application can inspect Vagdhenu's output.
        capture_output=True,
        text=True
    )

     # -----------------------------------------------------
    # Locate and verify the generated WAV file
    # -----------------------------------------------------

    # Vāgdhenu names the generated audio using the job ID
    # and stores it inside the directory passed to --outdir.

    audio_file = VAGDHENU_ROOT / "out" / f"{job_id}.wav"
    print("Audio file:",audio_file)
    print("Audio exists",audio_file.exists())

     # -----------------------------------------------------
    # Temporary debugging output
    # -----------------------------------------------------

    # These prints are useful while developing the integration.
    # Later we will replace them with proper error handling/logging.

    print("Return code:", result.returncode)
    print("Output:", result.stdout)
    print("Error:", result.stderr)