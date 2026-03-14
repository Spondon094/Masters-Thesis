# Master-Thesis

## Topic

Analyzing motion patterns in Fetal MRI.

## Task 

# 🧬 Analyzing Motion Patterns in Fetal MRI

A research-level project developed as part of a **Masters Thesis** at S-MRI lab, Friedrich Alexander University, Erlangen-Nuremberg. This project automatically detects and analyzes motion patterns from Fetal MRI scans across different gestational ages using advanced mathematical algorithms.

---

## 📌 Research Overview

Fetal MRI is challenging due to unpredictable movements of the fetus during scanning. This project develops an automated pipeline to:
- Detect and classify different types of fetal motion
- Analyze motion patterns across different gestational ages
- Separate fetal motion from maternal breathing artifacts
- Visualize motion flow across MRI time series

---

## 🔬 Methods & Algorithms

### 1. Singular Value Decomposition (SVD)
SVD breaks the MRI data into three main components:

| Component | Role |
|---|---|
| **U** | Captures temporal dynamics — how movement evolves over time |
| **Σ** | Singular values indicating significance of each data component |
| **Vt** | Encodes spatial information — shapes and structures in MRI images |

### 2. Low Rank + Sparse Matrix Decomposition (L+S)
Separates static background from motion artifacts:
- **Low Rank** → Separates the static background
- **Sparsity** → Captures motion and artifacts from the foreground

### 3. Discrete Wavelet Transformation (DWT)
Applied on the sparse image to extract maternal breathing frequency from fetal motion, enabling clean separation of motion sources.

### 4. Farnebäck Optical Flow Algorithm
- Uses a **Polynomial Model** for smoother and more precise motion estimates
- **Dense Flow Estimation** — calculates motion for every pixel
- Higher accuracy in complex regions

### 5. Duality Based TV-L1 Optical Flow Algorithm
- Specializes in capturing finer motion details like breathing frequency
- Uses **Total Variation (TV) regularization** and **L1-norm data fidelity**
- Captures smaller, more abrupt changes that can get lost in noise

---

## 🗂️ Project Structure

```
Masters-Thesis/
│
├── src/
│   ├── main.py                    # Main pipeline script
│   └── modules/
│       ├── __init__.py            # Module initialization
│       ├── data_loader.py         # NIFTI data loading
│       ├── optical_flow.py        # TV-L1 optical flow computation
│       ├── visualize_flow.py      # Flow visualization and plotting
│       └── save_results.py        # Save flow data and magnitudes
│
├── output/
│   ├── flow_visualizations/       # Saved flow visualization images
│   ├── flow_plots/                # Smoothed magnitude plots
│   ├── flows.pkl                  # Saved optical flow data
│   └── mean_flow_magnitudes_per_time_step.csv
│
└── README.md
```

---

## 🔄 Pipeline Workflow

```
Step 1: Load NIFTI Data
        → Loads all .nii.gz MRI files from folder
        → Returns time steps and slices per time step
            ↓
Step 2: Compute TV-L1 Optical Flow
        → Computes flow between consecutive MRI slices
        → Uses multiprocessing for faster computation
            ↓
Step 3: Save Results
        → Saves flow data as .pkl file
        → Saves mean flow magnitudes as .csv
            ↓
Step 4: Visualize Optical Flow
        → Draws motion vectors on MRI slices
        → Saves visualizations as .png images
            ↓
Step 5: Plot Motion Patterns
        → Applies Gaussian smoothing
        → Plots mean flow magnitude over time steps
```

---

## 📦 Key Components

### 📂 data_loader.py
- Loads all `.nii.gz` NIFTI files from a folder
- Returns MRI data, time steps, and slices per time step
- Uses `nibabel` for NIFTI file handling

### 🔍 optical_flow.py
- Implements **TV-L1 Optical Flow** using OpenCV
- Uses **multiprocessing** (`mp.Pool`) for parallel computation across all CPU cores
- Computes flow between every consecutive pair of MRI slices

### 🎨 visualize_flow.py
- Draws **motion vector arrows** on MRI slices using OpenCV
- Saves flow visualizations as high-resolution PNG images
- Plots **smoothed mean flow magnitude** over time using Gaussian filter

### 💾 save_results.py
- Saves computed optical flow data using `pickle`
- Computes and saves **mean flow magnitude per time step** to CSV
- Groups magnitudes by time step for temporal analysis

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core programming language |
| NumPy | Numerical computations |
| OpenCV | Optical flow computation and visualization |
| nibabel | Loading NIFTI MRI files |
| matplotlib | Plotting motion patterns |
| scipy | Gaussian smoothing |
| multiprocessing | Parallel flow computation |

---

## 🚀 How to Run

**Install dependencies:**
```bash
pip install numpy opencv-python nibabel matplotlib scipy
```

**Run the pipeline:**
```bash
cd src
python main.py
```

**Output will be saved in:**
```
output/flow_visualizations/   → Motion vector images
output/flow_plots/            → Smoothed magnitude plots
output/flows.pkl              → Raw flow data
output/mean_flow_magnitudes_per_time_step.csv → Magnitude data
```

---

## 🎓 Academic Context

- **Degree:** Masters in Computer Science
- **University:** Friedrich Alexander University, Erlangen-Nuremberg, Germany
- **Topic:** Analyzing Motion Patterns in Fetal MRI
- **Focus:** Automated detection and classification of fetal motion across gestational ages using mathematical decomposition and optical flow algorithms

---

## 💡 Key Contributions

- ✅ Automated pipeline for fetal motion analysis
- ✅ Separation of fetal motion from maternal breathing artifacts
- ✅ Multi-algorithm approach combining SVD, L+S, DWT and Optical Flow
- ✅ Parallel processing for efficient computation on large MRI datasets
- ✅ Quantitative motion analysis with temporal visualization

---

## 👨‍💻 Author

**Spondon Sarker**
Masters Graduate — Friedrich Alexander University, Erlangen-Nuremberg
