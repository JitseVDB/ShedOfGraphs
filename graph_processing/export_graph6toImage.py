import os
import networkx as nx
import matplotlib.pyplot as plt

def export_graph_image(graph6_str: str, image_format: str, output_folder: str) -> None:
    """
    Exports a graph given in graph6 format to an image file.

    Parameters:
        graph6_str (str): A string representing the graph in graph6 format.
                          For example: "E?bg".
        image_format (str): The desired image format for export (e.g., "png", "jpg", "svg").
                            Must be supported by matplotlib's savefig function.
        output_folder (str): The path to the directory where the image will be saved.
                             The directory will be created if it doesn't exist.

    Raises:
        ValueError: If the provided graph6 string is invalid and cannot be parsed.

    The image will be saved with a filename based on the graph6 string. Characters that may 
    conflict with file naming (such as '?') are replaced with safe substitutes.

    Example:
        >>> export_graph_image("E?bg", "png", "./graph_images")
    """
    try:
        # Convert the graph6 string into a NetworkX graph object
        G = nx.from_graph6_bytes(graph6_str.encode('ascii'))
    except Exception as e:
        raise ValueError(f"Invalid graph6 string: {e}")

    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create a safe filename by replacing problematic characters
    safe_graph_name = graph6_str.replace("?", "_q_").replace("/", "_slash_")
    filename = f"{safe_graph_name}.{image_format}"
    filepath = os.path.join(output_folder, filename)

    # Plot and export the graph
    plt.figure(figsize=(4, 4))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)
    plt.axis('off')
    plt.savefig(filepath, format=image_format, bbox_inches='tight')
    plt.close()

# Example call
if __name__ == "__main__":
    export_graph_image("EUzW", "png", "./graph_images")
