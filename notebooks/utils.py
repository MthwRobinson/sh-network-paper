import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.decomposition import PCA

def glm_marginal_effect(variable, res, X, all_data):
    """Computes the GLM marginal effects for the variable.

    Parameters
    ----------
    variable : str
        the variable for which we would like to calculate the marginal effect
    res : sm.model
        results of the linear regression
    X : pd.DataFrame
        the input to the linear regression
    all_data : pd.DataFrame
        the full set of input data

    Returns
    -------
    marginal_effect : float
    """
    data = all_data.copy(deep=True)
    param = res.params[variable]
    cross_term = '{}Xcrowd_pct'.format(variable)
    if cross_term in res.params:
        data['effect'] = param + data['crowd_pct'] * res.params[cross_term]
    else:
        data['effect'] = param
    data['prediction'] = res.predict(X)
    data['marginal_effect'] = data['effect'] * data['prediction']
    return data['marginal_effect'].mean()

def compute_pca(X, n_components=50):
    """Compute principal component analysis only on the topic columns

    Parameters
    ----------
    X : pd.DataFrame
        the dataframe that contains the columns for the regression model
    n_compnents : int
        the number of principal components to retain

    Returns
    -------
    final_df : pd.DataFrame
        the data frame for the linear regression, with the topic columns
        replaced by their principal components
    """
    topic_columns = [x for x in X.columns if 'topic' in x]
    topic_matrix = X[topic_columns]
    pca = PCA(n_components=n_components)
    pca_matrix = pca.fit_transform(topic_matrix)
    pca_df = pd.DataFrame(data = pca_matrix, columns = ['pc_{}'.format(i) for i in range(pca_matrix.shape[1])])
    pca_df['index'] = range(len(pca_df))
    X['index'] = range(len(X))
    final_df = X.merge(pca_df)
    del final_df['index']
    for col in final_df:
        if 'topic' in col:
            del final_df[col]
    return final_df

def calc_total_effect(all_data, res, X, crowd_pct=None, avg_clustering=None,
                      avg_min_path=None, gini_coefficient=None):
    """Calculates the total effect of crowd_pct in the GLM model

    Parameters
    ----------
    all_data : pd.DataFrame
        the input data to the regression model
    res : regression results
        the output of the regression model

    Returns
    -------
    total_effect : float
    """
    effects_data = X.copy(deep=True)

    effects_data['crowd_pct'] = all_data['crowd_pct'] if not crowd_pct else crowd_pct
    effects_data['crowd_pct_2'] = effects_data['crowd_pct']**2

    effects_data['avg_clustering'] = all_data['avg_clustering'] if not avg_clustering else avg_clustering
    effects_data['avg_min_path'] = all_data['avg_min_path'] if not avg_min_path else avg_min_path
    effects_data['gini_coefficient'] = all_data['gini_coefficient'] if not gini_coefficient else gini_coefficient

    effects_data['avg_clusteringXcrowd_pct'] = effects_data['crowd_pct'] * effects_data['avg_clustering']
    effects_data['avg_min_pathXcrowd_pct'] = effects_data['crowd_pct'] * effects_data['avg_min_path']
    effects_data['gini_coefficientXcrowd_pct'] = effects_data['crowd_pct'] * effects_data['gini_coefficient']

    params = {}
    param_vars = ['crowd_pct', 'crowd_pct_2', 'avg_clusteringXcrowd_pct',
                  'avg_min_pathXcrowd_pct', 'gini_coefficientXcrowd_pct']
    for var in param_vars:
        params[var] = 0 if var not in res.params else res.params[var]

    columns = [x for x in res.params.keys()]
    pred_data = effects_data[columns]
    predictions = res.predict(pred_data)

    crowd_pct_2_effect =  predictions * params['crowd_pct_2']
    crowd_pct_param = params['crowd_pct'] + (effects_data['avg_clustering'] * params['avg_clusteringXcrowd_pct']
                       + effects_data['gini_coefficient'] * params['gini_coefficientXcrowd_pct']
                       + effects_data['avg_min_path'] * params['avg_min_pathXcrowd_pct'])

    total_effect = predictions * (2 * params['crowd_pct_2'] * effects_data['crowd_pct'] + crowd_pct_param)
    avg_effect = total_effect.mean()
    return avg_effect

def build_crowd_pct_variation(all_data, X):
    """Used to created an input data set that holds all variables
    at their average value except for crowd_pct, which is varied.
    Used to show the marginal effect of crowd_pct

    Parameters
    ----------
    all_data : pd.DataFrame
        this is the full set of input data for the models
    X : pd.DataFrame
        this is the input data set specific to the model
        whose marginal effects we are trying ot determine

    Returns
    -------
    crowd_pct_variation : pd.DataFrame
        a dataframe that has the input data with crowd_pct
        varied from 0 to 0.99
    """
    mean_values = all_data.mean()
    data = {x: [] for x in X.columns}
    for i in range(100):
        crowd_pct = float(i/100)
        for field in data:
            if field == 'Intercept':
                data[field].append(1)
            elif 'crowd_pct' not in field:
                if ':' in field:
                    fields = field.split(':')
                    data[field].append(mean_values[fields[0]]*
                                       mean_values[fields[1]])
                else:
                    data[field].append(mean_values[field])
            elif field == 'crowd_pct':
                data[field].append(crowd_pct)
            elif field == 'crowd_pct_2':
                data[field].append(crowd_pct**2)
            elif 'X' in field and 'crowd_pct' in field:
                fields = field.split('X')
                data[field].append(crowd_pct * mean_values[fields[0]])
    crowd_pct_variation = pd.DataFrame(data)
    return crowd_pct_variation
