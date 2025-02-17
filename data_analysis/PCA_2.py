import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def perform_pca(file_paths, columns_to_remove=None, n_components=2):
    """
    Function to perform PCA on different data samples and visualize the result.

    Parameters:
    - file_paths (dict): A dictionary where keys are the labels (e.g. 'Air', 'Oil', 'Aloevera')
                          and values are the file paths to the datasets.
    - columns_to_remove (list): A list of columns to remove from the data before performing PCA.
    - n_components (int): The number of principal components to keep.
    """
    # Try reading the data files and handle missing files gracefully
    try:
        data_frames = {}
        for label, file_path in file_paths.items():
            data_frames[label] = pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return  # Exit the function if files are not found

    # Combine all dataframes into one
    data = pd.concat(data_frames.values(), keys=data_frames.keys())
    print('keys = ',data_frames.keys())
    # Remove specified columns if needed
    if columns_to_remove is not None:
        for col in columns_to_remove:
            if col in data.columns:
                data = data.drop(col, axis=1)

    # Prepare data for PCA
    features = data.columns
    x = data.loc[:, features].values
    x = StandardScaler().fit_transform(x)  # Standardize the data

    # Apply PCA
    pca = PCA(n_components=n_components)  # Reduce to specified principal components
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=principalComponents, columns=[f'principal component {i+1}' for i in range(n_components)])

    # Add labels back to DataFrame
    finalDf = pd.concat([principalDf, data.reset_index(drop=False)], axis=1)

    # Plotting
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(f'Principal Component 1', fontsize=15)
    ax.set_ylabel(f'Principal Component 2', fontsize=15)
    ax.set_title(f'{n_components} component PCA', fontsize=20)

    targets = list(file_paths.keys())
    colors = ['blue', 'red', 'green', 'purple', 'orange'][:len(targets)]  # Color limit based on number of targets
    for target, color in zip(targets, colors):
        indicesToKeep = finalDf['level_0'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'],
                   finalDf.loc[indicesToKeep, 'principal component 2'],
                   c=color, s=50)
    ax.legend(targets)
    ax.grid()
    plt.show()