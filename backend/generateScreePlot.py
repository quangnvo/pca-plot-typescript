import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

bp = Blueprint('generateScreePlot', __name__)


@bp.route('/api/generate_scree_plot', methods=['POST'])
def generate_scree_plot():
    #########################
    # Get the initial data and do some initial preparation
    #########################

    # Things done in the following code:
    # 1. Get the data from the request
    # 2. Convert the data into a DataFrame
    initialData = request.json
    convertedData = pd.DataFrame(data=initialData)

    # Assume that the first column is the column that contains the names of the genes (like gene1, gene2, etc.), so here we set the first column as the index of the DataFrame
    # ==> so the Dataframe will not use it for the calculations
    # Things done in the following code:
    # 1. Take the name of the first column in the DataFrame
    # 2. Based on that name, let the first column be the index of the DataFrame
    nameOfTheFirstColumn = list(initialData[0].keys())[0]
    convertedData.set_index(nameOfTheFirstColumn, inplace=True)

    # Things done in the following code:
    # 1. Replace comma with dot in the DataFrame
    # 2. Convert string values to float
    # 3. Remove rows with NaN values
    # 4. Transpose the DataFrame
    convertedData = convertedData.replace(',', '.', regex=True)
    convertedData = convertedData.astype(float)
    convertedData = convertedData.dropna()

    print("🚀🚀🚀 CONVERTED DATA")
    print(convertedData)

    #########################
    # Standardize the data
    #########################

    # Things done in the following code:
    # 1. Create a StandardScaler object by using StandardScaler() of scikit-learn
    # 2. Pass the data into the scaling object ==> data will be standardized (centered and scaled)
    standardScalerObject = StandardScaler()
    dataAfterStandardization = standardScalerObject.fit_transform(
        convertedData.T)

    # print("🚀🚀🚀 DATA AFTER STANDARDIZATION")
    # print(dataAfterStandardization)

    #########################
    # Calculate the percentage of explained variance per principal component
    #########################

    # Things done in the following code:
    # 1. Create a PCA object by using PCA() of scikit-learn
    # 2. Pass the standardized data into the PCA object
    pcaObject = PCA(n_components=8)
    pcaObject.fit_transform(dataAfterStandardization)

    # Calculate the percentage of explained variance per principal component
    percentageOfVariance = np.round(
        pcaObject.explained_variance_ratio_ * 100, decimals=1)

    #########################
    # Prepare the result following the Plotly format
    #########################

    # Things done in the following code:
    # 1. Create labels for the scree plot, like "PC1", "PC2", etc.
    # 2. Calculate the cumulative explained variance
    # 3. Prepare the data for the scree plot
    # 4. Prepare the layout for the scree plot
    # 5. Combine the data and the layout into a dictionary and return it as a JSON object

    labels = ['PC' + str(x) for x in range(1, len(percentageOfVariance)+1)]

    cumulativeVariance = np.cumsum(percentageOfVariance)

    screePlotFormatData = [
        {
            'type': 'bar',
            'x': labels,
            'y': percentageOfVariance.tolist(),
            # Display the percentage on top of each bar
            'text': [f'{value}%' for value in percentageOfVariance.tolist()],
            'textposition': 'auto',
            'marker': {
                'color': 'yellow',
                'line': {
                    'color': 'black',
                    'width': 2,
                },
            },
            'name': 'Individual'
        },
        {
            'type': 'scatter',
            'x': labels,
            'y': cumulativeVariance.tolist(),
            'mode': 'lines+markers',
            'name': 'Cumulative',
            'line': {
                'color': 'black',
                'width': 2,
            },
            'marker': {
                'size': 7,
            },
        }
    ]

    layoutScreePlotForReact = {
        'title': {
            'text': 'Scree Plot',
            'font': {
                    'size': 30,
                    'color': 'black',
            },
        },
        'xaxis': {
            'title': 'Principal component',
            'titlefont': {
                'size': 20,
                'color': 'black',
            },
        },
        'yaxis': {
            'title': 'Explained variance (%)',
            'titlefont': {
                'size': 20,
                'color': 'black',
            },
        },
        'autosize': True,
        'hovermode': 'closest',
        'showlegend': False,
        'height': 400,
    }

    result = {
        'data': screePlotFormatData,
        'layout': layoutScreePlotForReact
    }

    return jsonify(result)
