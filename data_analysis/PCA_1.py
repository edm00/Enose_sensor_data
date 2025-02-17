import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from google.colab import drive


def perform_pca(data_files, labels, title):
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    try:
        dfs = [pd.read_csv(file) for file in data_files]
    except FileNotFoundError:
        print("Error: One or more data files not found.")
        return

    data = pd.concat(dfs, keys=labels)
    columns_to_remove = ['temperature', 'humidity', 'Time']
    for col in columns_to_remove:
        if col in data.columns:
            data = data.drop(col, axis=1)

    features = data.columns
    x = data.loc[:, features].values
    x = StandardScaler().fit_transform(x)
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data=principalComponents, columns=['principal component 1', 'principal component 2'])
    finalDf = pd.concat([principalDf, data.reset_index(drop=False)], axis=1)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title(title, fontsize=20)

    for target, color in zip(labels, ['blue', 'red', 'green']):
        indicesToKeep = finalDf['level_0'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'],
                   finalDf.loc[indicesToKeep, 'principal component 2'],
                   c=color, s=50)
    ax.legend(labels)
    ax.grid()
    plt.show()