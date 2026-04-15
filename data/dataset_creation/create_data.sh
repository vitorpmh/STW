echo "Creating full image dataset..."
python data/dataset_creation/images/full_image_dataset.py
echo "Creating skin only dataset..."
python data/dataset_creation/images/skin_only_dataset.py
echo "Creating cheeks and nose dataset..."
python data/dataset_creation/images/cheeks_and_nose_dataset.py

echo "All datasets created successfully."

echo "Creating splits"
echo "Refactoring annotations..."
python data/splits/refactor_annotations.py
echo "Creating train/test splits..."
python data/splits/images_train_test_splits.py
python data/splits/individual_train_test_splits.py