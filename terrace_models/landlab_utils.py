import numpy as np

def extract_top_outlet_node_ids(mg, field='drainage_area', limit=100000):
    max_y = mg.y_of_node.max()
    top_row = mg.y_of_node==mg.y_of_node.max()
    # top_row_values = mg.at_node[field][mg.y_of_node==max_y]
    over_limit_values = mg.at_node[field] > limit
    top_row_top_values_cond = np.logical_and(top_row, over_limit_values)
    node_ids = mg.nodes.reshape(mg.number_of_nodes)
    top_row_top_values_ids = node_ids[top_row_top_values_cond]
    return top_row_top_values_ids


def extract_row_outlet_node_ids(mg, row_y, field='drainage_area', limit=100000):
    row = mg.y_of_node==row_y
    over_limit_values = mg.at_node[field] > limit
    row_top_values_cond = np.logical_and(row, over_limit_values)
    node_ids = mg.nodes.reshape(mg.number_of_nodes)
    row_top_values_ids = node_ids[row_top_values_cond]
    return row_top_values_ids


def extract_row_transsect(mg, row_y, field='drainage_area'):
    """
    Extract values from the chosen field for a row.

    Parameters
    ----------
    mg : RasterModelGrid
        The RasterModelGrid to analyse.
    row_y : int/float
        Y coordinate of chosen row.
    field : str, optional
        Valid field name in mg. The default is 'drainage_area'.

    Returns
    -------
    values : Arr
        Values in the chosen row from the specified field.

    """
    row = mg.y_of_node==row_y
    values = mg.at_node[field][row]
    return values