import os
import requests
import zipfile
import pandas as pd
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from Core.logger import *
from Core.utils import *

logger = Logger().setup_logs()

class DataLoader:
    def __init__(self):
        self.data_dir = "./Data"
        self.data_zip = "./Data/online_retail_data.zip"
        self.data = "./Data/Online Retail.xlsx"
        #Data Folder
        if not os.path.exists(self.data_dir):
            logger.info("Data Folder Not Found. Adding Data Folder.")
            os.mkdir(self.data_dir)
        #Zip Data
        if not os.path.exists(self.data_zip):
            url = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print("Getting Data from the Source.")
                    logger.info("Successfully retrieved the response from the data source and downloaded the data ZIP file.")
                    with open(self.data_zip, 'wb') as file:
                        file.write(response.content)
                        logger.info("Successfully downloaded the Data ZIP file.")
            except Exception as e:
                print(f"An issue occurred while downloading data from the source: {url}. Error: {e}")
                logger.error(f"An issue occurred while downloading data from the source: {url}. Error: {e}")
                sys.exit(1)
        # File Data
        if not os.path.exists(self.data):
            logger.info("Extracting the Data from ZIP file.")
            with zipfile.ZipFile(self.data_zip, "r") as zip_ref:
                zip_ref.extractall(self.data_dir)
                logger.info("Extracted Successfully Data from ZIP file.") 
        #reading the excel file        
        try:
            logger.info("Started Reading Data File.")
            self.dataframe = pd.read_excel(self.data)
            columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate',
       'UnitPrice', 'CustomerID', 'Country']
            if list(self.dataframe.columns) != columns:
                print(f"The columns are missing or not in the expected order: {columns}")
                logger.error(f"The columns are missing or not in the expected order: {columns}")
                #terminating the system - columns do not match
                sys.exit(0)
            self.unclean_dataframe = self.dataframe
        except Exception as e:
            print(f"Got the Error while Reading the Dataset from the File: {e}")
            logger.error(f"Got the Error while Reading the Dataset from the File: {e}")
            sys.exit(1)
        self.data_cleaning()

    def data_cleaning(self):
        self.dataframe = self.dataframe.dropna(subset=["CustomerID"])
        #removing the cancel orders
        self.dataframe = self.dataframe[~self.dataframe["InvoiceNo"].astype(str).str.startswith('C')]
        #removing the negative or zero unitPrice
        self.dataframe = self.dataframe[self.dataframe["UnitPrice"] > 0]
        logger.info("Data Cleaning Completed.")
        self.feature_adding()

    def feature_adding(self):
        #adding column where price is in the dollar 
        self.dataframe["UnitPriceDollar"] = self.dataframe["UnitPrice"].apply(lambda x:x*1.34)
        #adding the Revenue column
        self.dataframe["Revenue"] = self.dataframe["Quantity"] * self.dataframe["UnitPriceDollar"]
        #adding the month and year columns 
        self.dataframe["Month"] = self.dataframe["InvoiceDate"].dt.to_period("M").astype(str)
        self.dataframe["Year"] = self.dataframe["InvoiceDate"].dt.to_period("Y").astype(str)
        logger.info("Features Added to the Data Frame Successfully.")


    def _generate_kpis(self):
        self.unclean_total_transaction = self.unclean_dataframe["InvoiceNo"].nunique()
        self.total_transaction = self.dataframe["InvoiceNo"].nunique() 
        self.total_revenue = self.dataframe["Revenue"].sum()
        self.per_cancel_order = 100 - ((self.total_transaction / self.unclean_total_transaction) * 100)
        self.unclean_unique_customers = self.unclean_dataframe["CustomerID"].nunique()
        self.unique_customers = self.dataframe["CustomerID"].nunique() 
        self.per_cancel_customer = 100 - ((self.unique_customers / self.unclean_unique_customers) * 100)
        self.avg_revenue = self.total_revenue / self.total_transaction
        self.num_countries = len(self.dataframe['Country'].unique())
        self.top_product = self.dataframe['Description'].value_counts().idxmax()
        self.top_country_customers = self.dataframe['Country'].value_counts().idxmax()
        logger.info("KPI's generated Successfully.")

    def _handle_level_1(self):
        self._generate_kpis()
        data_desc = "This is a Transactional data set which contains all the Transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and Registered non store Online Retail. The Company mainly Sells unique all occasion gifts. Many Customers of the Company are Wholesalers."
        column_descriptions = {
            "InvoiceNo": "A 6-digit integral number uniquely assigned to each Transaction. If this code starts with letter 'c', it indicates a Cancellation",
            "StockCode": "A 5-digit integral number uniquely assigned to each distinct product",
            "Description": "Product Name",
            "Quantity": "The Quantities of each Product (item) per Transaction",
            "InvoiceDate": "The day and time when each Transaction was generated",
            "UnitPrice": "Product Price per Unit",
            "CustomerID": "A 5-digit integral number uniquely assigned to each Customer",
            "Country": "The name of the country where each Customer resides"
        }
        data_types ={
            "InvoiceNo": ["Categorical","Text"],
            "StockCode": ["Categorical","Text"],
            "Description": ["Categorical","Text"],
            "Quantity": ["Integer","Numeric"],
            "InvoiceDate": ["Date","Datetime"],
            "UnitPrice": ["Continuous","Numeric"],
            "CustomerID": ["Categorical","Numeric"],
            "Country": ["Categorical","Text"]
            }
        kpis = {
            "Total Transaction": f"{Utils.formater(self.total_transaction)}",
            "Total Revenue": f"{Utils.currency_format(self.total_revenue)}",
            "Average Revenue": f"{Utils.currency_format(self.avg_revenue)}",
            "Unique Customers": f"{Utils.formater(self.unclean_unique_customers)}",
        }
        interesting_facts = {
            "interesting_fact1": f"The dataset originally contained {Utils.formater(self.unclean_total_transaction)} transaction records. After cleaning, {Utils.formater(self.total_transaction)} records remain. A total of {Utils.formater(self.unclean_total_transaction - self.total_transaction)} records were removed due to negative prices or quantities (representing canceled transactions) and missing Customer IDs.",
            "interesting_fact2": f"The percentage of canceled orders in the dataset is {Utils.decimal_format(self.per_cancel_order)}%, which involves only {Utils.decimal_format(self.per_cancel_customer)}% of the customers.",
            "interesting_fact3": f"The dataset contains {Utils.formater(self.num_countries)} unique countries.",
            "interesting_fact4" : f"The most frequently purchased product in the dataset is {self.top_product}.",
            "interesting_fact5": f"The country with the highest number of customers is {self.top_country_customers}.",
            "interesting_fact6": f"The dataset originally contained {Utils.formater(self.unclean_unique_customers)} unique customers. After data cleaning, {Utils.formater(self.unique_customers)} unique customers remain."
            }
        logger.info("Level 1 Data Successfully Created.")
        return {
            "description" : data_desc,
            "column_descriptions": column_descriptions,
            "data_types": data_types,
            "kpis": kpis,
            "interesting_facts": interesting_facts            
        }
    
    def _handle_level_2(self):
        # 1. Plot - Monthly Revenue
        try:
            monthly_revenue = self.dataframe.groupby('Month')['Revenue'].sum().sort_index()
            plt.figure(figsize=(12, 5))
            ax = sns.lineplot(x=monthly_revenue.index, y=monthly_revenue.values, marker='o')
            ax.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            plt.title("Monthly Revenue Trend")
            plt.xticks(rotation=45)
            plt.ylim(0, monthly_revenue.max() * 1.1)
            plt.ylabel("Total Revenue ($)")
            plt.xlabel("Month")
            plt.grid(True) 
            plt.savefig("./Data/1. monthly_revenue_plot.png", dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Successfully created and saved the Monthly Revenue Trend Plot.")
        except Exception as e:
            print(f"Got Error in 1st Plot: Monthly Revenue Trend: {e}")
            logger.error(f"Got Error in 1st Plot: Monthly Revenue Trend: {e}")

        # 2. Plot - Yearly Revenue
        try:
            yearly_revenue = self.dataframe.groupby('Year')['Revenue'].sum().sort_index()
            plt.figure(figsize=(12, 5))
            ax = sns.barplot(x=yearly_revenue.index, y=yearly_revenue.values)
            ax.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            for i, value in enumerate(yearly_revenue.values):
                plt.text(i, value + 1000, f'{value:,.0f}', ha='center', va='bottom', fontsize=10)
            plt.title("Yearly Revenue Trend")
            plt.ylim(0, yearly_revenue.max() * 1.1)
            plt.ylabel("Total Revenue ($)")
            plt.xlabel("Year")
            plt.grid(True) 
            plt.savefig("./Data/2. yearly_revenue_plot.png", dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Successfully created and saved the Yearly Revenue Trend Plot.")
        except Exception as e:
            print(f"Got Error in 2nd Plot: Yearly Revenue Trend: {e}")
            logger.error(f"Got Error in 2nd Plot: Yearly Revenue Trend: {e}")

        # 3. Plot - Top 10 Country by revenue
        try:
            country_revenue = self.dataframe.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10)
            plt.figure(figsize=(12, 5))
            ax = sns.barplot(x=country_revenue.index, y=country_revenue.values, hue=country_revenue.index)
            ax.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            plt.ylim(0, country_revenue.max() * 1.1)
            for i, value in enumerate(country_revenue.values):
                plt.text(i, value + 1000, f'{value:,.0f}', ha='center', va='bottom', fontsize=10)
            plt.title("Top 10 Countries by Revenue")
            plt.xlabel("Country")
            plt.ylabel("Total Revenue ($)")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.grid(True) 
            plt.savefig("./Data/3. top_10_country_by_revenue.png", dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Successfully created and saved the Top 10 Countries by Revenue Plot.")
        except Exception as e:
            print(f"Got Error in Plot: Top 10 Countries by Revenue: {e}")
            logger.error(f"Got Error in Plot: Top 10 Countries by Revenue: {e}")

        # 4. Plot - Top 10 Purchase
        try:
            purchase_by_custome = self.dataframe.groupby(['CustomerID', 'Country'])['Revenue'].sum().sort_values(ascending=False).head(10)
            purchase_by_custome = purchase_by_custome.reset_index()
            plt.figure(figsize=(12,5))
            ax = sns.barplot(x=purchase_by_custome["CustomerID"].astype(int).astype(str), y=purchase_by_custome["Revenue"], hue=purchase_by_custome["Country"])
            ax.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            plt.ylim(0, purchase_by_custome["Revenue"].max() * 1.1 )
            for i, value in enumerate(purchase_by_custome["Revenue"]):
                plt.text(i, value + 1000, f'{value:,.0f}', ha='center', va='bottom', fontsize=10)
            plt.title("Top 10 Customer by Purchase by Country")
            plt.xlabel("Customer ID")
            plt.ylabel("Total Purchase ($)")
            plt.tight_layout()
            plt.grid(True) 
            plt.savefig("./Data/4. top_10_customer_by_purchase.png", dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Successfully created and saved the Top 10 Customer by Purchase by Country Plot.")
        except Exception as e:
            print(f"Got Error in Plot: Top 10 Customer by Purchase by Country: {e}")
            logger.error(f"Got Error in Plot: Top 10 Customer by Purchase by Country: {e}")
        

        self.plot = {
            "monthly_revenue_plot": "./Data/1. monthly_revenue_plot.png",
            "yearly_revenue_plot": "./Data/2. yearly_revenue_plot.png",
            "top_10_country_by_revenue": "./Data/3. top_10_country_by_revenue.png",
            "top_10_customer_by_purchase": "./Data/4. top_10_customer_by_purchase.png"
        }
        return self.plot

    def _handle_level_3(self):
        # 5. Plot - Top 10 Country by No. of Customers
        try: 
            customers_by_country = self.dataframe.groupby("Country")["CustomerID"].count().sort_values(ascending=False).head(10)
            plt.figure(figsize=(12,5))
            ax = sns.barplot(x=customers_by_country.index, y=customers_by_country.values, hue=customers_by_country.index)
            ax.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            plt.ylim(0, customers_by_country.values.max() * 1.1 )
            for i, value in enumerate(customers_by_country.values):
                plt.text(i, value + 1000, f'{value:,.0f}', ha='center', va='bottom', fontsize=10)
            plt.grid(True)
            plt.ylabel("No. of Customers")
            plt.xlabel("Country")
            plt.title("Top 10 Country by No. of Customers")
            plt.tight_layout()
            plt.savefig("./Data/5. top_10_country_by_no_of_customers.png", dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Successfully created and saved the Top 10 Country by No. of Customers Plot.")
        except Exception as e:
            print(f"Got Error in Plot: Top 10 Country by No. of Customers: {e}")
            logger.error(f"Got Error in Plot: Top 10 Country by No. of Customers: {e}")

        # 6. Plot - Quantity VS Revenue for Top 10 Countries
        try:
            df_clean_fil = self.dataframe[(self.dataframe["Quantity"] < 5000) & (self.dataframe["Revenue"] < 10000)]
            top_countries = df_clean_fil.groupby("Country")["Revenue"].sum().nlargest(10).index
            quantity_revenue = df_clean_fil[df_clean_fil["Country"].isin(top_countries)]
            plt.figure(figsize=(12,5))
            ax = sns.scatterplot(data=quantity_revenue, x="Quantity", y="Revenue", hue="Country")
            ax.get_xaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            ax.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            plt.grid(True)
            plt.ylabel("Revenue")
            plt.xlabel("Quantity")
            plt.title("Quantity VS Revenue for Top 10 Countries")
            plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig("./Data/6. top_10_country_qunatity_vs_revenue.png", dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Successfully created and saved the Quantity VS Revenue for Top 10 Countries Plot.")
        except Exception as e:
            print(f"Got Error in Plot: Quantity VS Revenue for Top 10 Countries: {e}")
            logger.error(f"Got Error in Plot: Quantity VS Revenue for Top 10 Countries: {e}")
        
        # 7. Plot - Top 10 Products by Quantity Sold
        try:
            product_quantity = self.dataframe.groupby("Description")["Quantity"].count().nlargest(10)
            plt.figure(figsize=(12,5))
            ax = sns.barplot(y=product_quantity.index.str.slice(0,12) + "..", x=product_quantity.values, hue=product_quantity.index)
            ax.get_xaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
            plt.xlim(0, product_quantity.values.max() * 1.1 )
            for i, value in enumerate(product_quantity.values):
                plt.text(value + 1, i, f'{value:,.0f}', ha='left', va='center', fontsize=10)
            plt.grid(True)
            plt.xlabel("Quantity")
            plt.ylabel("Product Description")
            plt.title("Top 10 Products by Quantity Sold")
            plt.tight_layout()
            plt.savefig("./Data/7. top_10_product_by_quantity_sold.png", dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Successfully created and saved the Top 10 Products by Quantity Sold Plot.")
        except Exception as e:
            print(f"Got Error in Plot: Top 10 Products by Quantity Sold: {e}")
            logger.error(f"Got Error in Plot: Top 10 Products by Quantity Sold: {e}")

        # 8. Plot - Correlation Matrix
        try:
            corr_df = self.dataframe[["Quantity", "Revenue", "UnitPrice"]].corr()
            plt.figure(figsize=(8, 6))
            sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="crest")
            plt.title("Correlation Matrix")
            plt.tight_layout()
            plt.savefig("./Data/8. correlation_matrix_heatmap.png", dpi=300, bbox_inches='tight')
            plt.close()
            logger.info("Successfully created and saved the Correlation Matrix Plot.")
        except Exception as e:
            print(f"Got Error in Plot: Correlation Matrix: {e}")
            logger.error(f"Got Error in Plot: Correlation Matrix: {e}")
        self.plot = {
            "top_10_country_by_no_of_customers": "./Data/5. top_10_country_by_no_of_customers.png",
            "top_10_country_qunatity_vs_revenue": "./Data/6. top_10_country_qunatity_vs_revenue.png",
            "top_10_product_by_quantity_sold": "./Data/7. top_10_product_by_quantity_sold.png",
            "correlation_matrix_heatmap": "./Data/8. correlation_matrix_heatmap.png"
        }
        return self.plot