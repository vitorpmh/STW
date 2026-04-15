# Skin Tone In the Wild Dataset (STW)

This repository contains the processing scripts and data organization structure for our facial skin tone identification dataset. The dataset aggregates several sources to provide a robust collection of full-frame and segmented facial images with corresponding skin tone annotations.

The dataset contains roughly 40k thousand images of 3.5k individuals.
---

⚠️ Work in Progress
This is an open repository. The current state of the code and data does not yet reflect the results presented in the paper.


## 🚀 Setup & Installation

To clone this repo:
```bash
git clone ...
```

Create a venv and install requirements

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📂 Project Structure

To set up the environment, your local `data/` directory should be organized as follows:

```text
data/
├── OpenData/                        # Raw external datasets (CASIA-Face-Africa, CASIA-FaceV5(BMP), data_celeb_a)        
│   ├── CASIA-Face-Africa/   
│   ├── CASIA-FaceV5/
│   └── data_celeb_a/                # CelebA data should be structured
│       └── img_align_celeba/
├── images/                          # Images downloaded from drive (or you could download them all to Open data and process them yourself)      
└── splits/                          # Downloaded train/test split definitions from drive (these will be rewritten)
```
---


### 1. Download Core Files
First, access our [Google Drive Folder](https://drive.google.com/drive/u/0/folders/1jPVDyY0m_WH9VRwS6uaEtLyAhiWKF7ye) and perform the following:
* Download the contents of the `images` folder and place them into your local `data/` directory.
* Download the `splits` folder and place it inside the `data/` directory. The training scripts are pre-configured to look for them there.

### 2. External Data Requirements
Due to licensing, some datasets must be downloaded directly from the providers. Place all of these unzipped files into `data/OpenData/`:

| Dataset | Source | Requirements |
| :--- | :--- | :--- |
| **CasiaFaceAfrica** | [IdealTest](https://www.idealtest.org/#/) | Account required |
| **CasiaV5** | [IdealTest](https://www.idealtest.org/#/) | Account required |
| **CelebA** | [MMLab](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) | Download "Align&Cropped Images" (`img_align_celeba.zip,identity_CelebA.txt`) |

### 3. Data Processing
Once the external datasets are in `data/OpenData/`, run:

```bash
chmod +x data/dataset_creation/create_data.sh
./data/dataset_creation/create_data.sh
```

**What this script does:**
1. Generates full-image and segmented facial crops.
2. Populates the `image/` subfolders with the new assets.
3. Refactors the annotation.csv to be consistent with the repo path.
4. Creates individual and images splits.

---

## 🛠️ Usage

The training scripts are designed to automatically detect the `splits/` folder within the `data/` directory. Once the processing script has finished, you are ready to begin training or evaluation.




## Annotations.

If you'd like to try, you can rewrite the scripts under the `annotation` folder to annotate your own data.