import os
import xml.etree.ElementTree as ET
import pandas as pd


xml_dir = r'C:\Users\blaze\python\Data\Raw_XMLs'


namespaces = {
    '': 'http://www.irs.gov/efile',  
}


data = []

# Loop 
for filename in os.listdir(xml_dir):
    if filename.endswith('.xml'):
        file_path = os.path.join(xml_dir, filename)
        
        # Parse XML
        tree = ET.parse(file_path)
        root = tree.getroot()
        
       
        try:
            # Extrac tax year
            tax_year = root.find('.//TaxYr', namespaces).text
            
            # Extract revenue 
            revenue = root.find('.//GrossReceiptsAmt', namespaces).text

            
  
            data.append({'tax_year': tax_year, 'revenue': float(revenue)})
        except AttributeError:
            print(f"Skipping {filename} due to missing data")


df = pd.DataFrame(data)
df.to_csv('financial_data.csv', index=False)

# Frequency of tax years
year_counts = df['tax_year'].value_counts()
print("Tax Year Frequency:\n", year_counts)

# Statistics for revenue
print("\nRevenue Statistics:\n", df['revenue'].describe())

with open('data_analysis_summary.txt', 'w') as f:
    f.write("Tax Year Frequency:\n")
    f.write(year_counts.to_string())
    f.write("\n\nRevenue Statistics:\n")
    f.write(df['revenue'].describe().to_string())
