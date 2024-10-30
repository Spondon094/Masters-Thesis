# Master-Thesis

## Topic

Analyzing motion patterns in Fetal MRI.

## Task

- Automatically detect and analyze different motion pattern from different gestational ages by using advanced mathematical algorithms.

## Methods

**Singular Value Decomposition**<br>
SVD breaks the data into three main components: U, Σ, and Vt. Here’s a brief overview of each:

- **U**: Captures changes over time, giving insight into temporal dynamics, such as the baby's movements across time steps.
  - This helps us understand how movement evolves over time, which is essential in motion analysis.
- **Σ**: Contains singular values that indicate the significance of each part of the data, helping prioritize important features.
  - These values allow us to focus on the most impactful components.
- **Vt**: Encodes spatial information, reflecting the shapes and structures within the images.
  - This part captures spatial patterns, like the layout of different body parts in fetal imaging.

**Low Rank plus Sparse matrix Decomposition**<br>
To get the clearer visualization we need to implement L+S

- **Low Rank**: Helps to separate the static background.
- **Sparsity**: capture the motion and artifact from the foreground.

**Discrete Wavelet Transformation**<br>

We implement it on sparse image to extract the maternal breathing frequency from the fetus motion.

**Farnebäck Gruner Optical Flow Algorithm**<br>

- **Higher Accuracy**: As it uses **Polynomial Model**, this providing smoother and more precise motion estimates in complex regions.
- **Dense Flow Estimation**: Farnebäck calculates motion for every pixel.

**Duality Based TV-L1 Optical Flow Algorithm**<br>

To capture the smaller, more abrupt changes like breathing frequency, which can get lost in noise. TV-L1, with its total variation (TV) regularization and L1-norm data fidelity, specializes in capturing those finer details.
