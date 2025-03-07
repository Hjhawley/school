import csv

# Name of the CSV file with predictions
csv_filename = "validation_predictions.csv"
# Name of the HTML file to generate
html_filename = "predictions.html"

# Start building the HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Validation Predictions</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
        img { max-width: 200px; height: auto; }
    </style>
</head>
<body>
    <h1>Validation Predictions</h1>
    <table>
        <tr>
            <th>Image</th>
            <th>Predictions</th>
        </tr>
"""

# Read the CSV and add a row for each image
with open(csv_filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        image_path = row["image_path"]
        predictions = row["top_two_predictions"]
        # Add a table row with the image and its predictions
        html_content += f"""
        <tr>
            <td><img src="{image_path}" alt="Image"></td>
            <td>{predictions}</td>
        </tr>
        """

# Close the table and body
html_content += """
    </table>
</body>
</html>
"""

# Write the HTML content to a file
with open(html_filename, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML file '{html_filename}' has been generated. Open it in a browser to view the predictions.")
