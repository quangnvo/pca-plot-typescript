import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

bp = Blueprint('generatePCA', __name__)


@bp.route('/api/generate_pca', methods=['POST'])
def generate_pca():
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
    convertedData = convertedData.replace(',', '.', regex=True)
    convertedData = convertedData.astype(float)
    convertedData = convertedData.dropna()

    #########################
    # Standardize the data
    #########################
    # Things done in the following code:
    # 1. Create a StandardScaler object by using StandardScaler() of scikit-learn
    # 2. Pass the data into the scaling object ==> data will be standardized
    standardScalerObject = StandardScaler()
    dataAfterStandardization = standardScalerObject.fit_transform(
        convertedData.T)

    #########################
    # Do the PCA
    #########################
    # Things done in the following code:
    # 1. Create a PCA object by using PCA() of scikit-learn
    # 2. Pass the standardized data into the PCA object
    pcaObject = PCA()
    pcaData = pcaObject.fit_transform(dataAfterStandardization)

    #########################
    # Get the % of variance explained by each PC
    #########################
    pcaVariancePercentage = pcaObject.explained_variance_ratio_

    #########################
    # Prepare the result following the Plotly format
    #########################
    # Things done in the following code:
    # 1. Prepare the data for the PCA plot
    # 2. Prepare the layout for the PCA plot
    # 3. Combine the data and the layout into a dictionary and return it as a JSON object

    pcaScatterCoordinates = [
        {
            'type': 'scatter',
            'mode': 'markers',
            'x': [pcaData[i, 0]],
            'y': [pcaData[i, 1]],
            'marker': {
                'size': 12,
                # 'color': colors_hex[i],
                "color": "#fa8072",
                'line': {
                    'color': 'black',
                    'width': 2,
                }
            },
            'name': convertedData.columns[i]
        } for i in range(len(convertedData.columns))
    ]

    layoutPCAPlotForReact = {
        'title': {
            'text': 'PCA Plot',
            'font': {
                'size': 30,
                'color': 'black',
            },
        },
        'xaxis': {
            'title': f'PC1 ({pcaVariancePercentage[0]*100:.2f}%)',
            'titlefont': {
                'size': 20,
                'color': 'black',
            },
        },
        'yaxis': {
            'title': f'PC2 ({pcaVariancePercentage[1]*100:.2f}%)',
            'titlefont': {
                'size': 20,
                'color': 'black',
            },
        },
        'autosize': True,
        # There are other options for hovermode, such as 'x', 'y', 'x unified'
        # The 'closest' option means that the hover label will be placed at the closest point among all the traces
        # Other options can be found here: https://plotly.com/python/hover-text-and-formatting/
        'hovermode': 'closest',
        'showlegend': True,
        'height': 400,
    }

    result = {
        'data': pcaScatterCoordinates,
        'layout': layoutPCAPlotForReact
    }

    #########################
    # Return the result
    #########################
    return jsonify(result)
