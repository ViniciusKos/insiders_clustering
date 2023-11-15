<img src=https://user-images.githubusercontent.com/73034020/201500075-24c94d3c-8979-4453-b9e8-e6f71ea1fc40.png alt="Rossmann logo" title="Rossmann" align="right" height="150" width="300" class="center"/>

# Customer Segmentation - Fidelity Program Insiders.


## 1) Business Issue
Select the most valuable customers for a loyalty program.

Business Assumptions:
Invoice dates are between 2016-11-29 and 2017-12-07;
Negative unit price values are considered returns

## 2) Solution methodology
The resolution of the challenge was carried out following the CRISP-DM (CRoss-Industry Standard Process for data mining) methodology, which is a cyclical approach that streamlines the delivery of value to the business through fast and valuable MVPs.

Benefits of Using CRISP-DM
This method is cost-effective as it includes several processes to take out simple data mining tasks.
CRISP-DM encourages best practices and allows projects to replicate.
This methodology provides a uniform framework for planning and managing a project.
Being a cross-industry standard, CRISP-DM can be implemented in any Data Science project irrespective of its domain.

For more details about CRISP-DM methodology: https://analyticsindiamag.com/why-is-crisp-dm-gaining-grounds/

![image](https://user-images.githubusercontent.com/73034020/180753015-7945d745-3420-4fd0-9681-6487fb066c80.png)

The strategy used to solve this was divided into 10 steps, each of which can be seen in the notebook.

Step 01. Data Description:  
Step 02. Data Filtering:  
Step 03. Feature Engineering:  
Step 04. Feature Selection:  
Step 05. Exploratory Data Analysis:  
Step 06. Data Preparation:  
Step 07. Hyperparameter Tuning and Model Selection:  
Step 08. Machine Learning Modelling:  
Step 09. Cluster Analysis and Business Value:  
Step 10. Deploy Model to Production:  

## 3) Data collection
The data was collected in Kaggle (UK-High value Customer Identification) and all the columns attributes are explained below:

Invoiceno - Invoice Number
StockCode - Product Stock Code
Description - Product Description
Quantity - Product Quantity
InvoiceDate - Invoice Date
UnitPrice - Product Unit Price
Customerid - Customer identification Number
Country - Customer Country


## 4) Data Understanding through mind map Hypotheses and **top 3 insights**
In this section we will list some hypotheses that can be tested using this data, these hypothesis generally comes from brainstorming 
with business areas and are very important to drive our analyses.
If they are not enough to separate the most valuable customers we would search for more data and formulate new hypotheses

Through the mind map, we can assess if the a specific feature has a big variance, thus it may be good separing the customers.

There are some features created in order tho find the most valuable customers. They were based on RFV Metrics:

![image](https://user-images.githubusercontent.com/73034020/201492747-560ab488-a9b3-4154-a8e8-3d87cfa04c66.png)


1. Profit = (Quantity of purchases * Unit Price) - (Quantity of returns * Unit Price)
2. Recency = Days between today and the last purchase.
3. Frequency = Average interval between a purchase and another.


## 5) Machine learning models applied and performances.

Several models were tested to find which has the highest Silhouette Score.

The Silhouette Coefficient is calculated using the mean intra-cluster distance (a) and the mean nearest-cluster distance (b) for each sample. The Silhouette Coefficient for a sample is (b - a) / max(a, b). To clarify, b is the distance between a sample and the nearest cluster that the sample is not a part of. 
The best value is 1 and the worst value is -1. Values near 0 indicate overlapping clusters. Negative values generally indicate that a sample has been assigned to the wrong cluster, as a different cluster is more similar. (Source: Sklearn Documentation - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)

![image](https://user-images.githubusercontent.com/73034020/201493041-98bde2d8-f7a4-4366-8d75-6a6d0af48541.png)


Below are the models's Silhouette Score for a given the number of Clusters.

![image](https://user-images.githubusercontent.com/73034020/201500353-6c4d9449-bb36-4f1f-8812-107e59062997.png)

DBSCan model was tested as well, but since it has no built in method for chosing the number of cluster and it had low silhouette scores it was not selected for the final model (Further details on notebook).
For this first CRISP-DM circle, KMeans was chosen since it has the biggest average Silhouette Scores for the given number of clusters.



**Hyperparameter tuning and final model**

The first approach with KMeans didn't result in good Silhouette Score (for more details, see Notebook section 7.1). So the data was reduced by an UMAP Reducer and the 2 resulting components are shown below.

![image](https://user-images.githubusercontent.com/73034020/203521938-872ee227-426f-4314-8d44-08c8178458ec.png)

The Silhouette Plot below show us the silhouette shape for each cluster using KMeans in the data reduced by UMAP.

![image](https://user-images.githubusercontent.com/73034020/203522270-cfc982d9-9c89-4da6-8014-bcd38052ee4a.png)

It resulted in a average's Silhouette Score of 0.51.

## 6) Business Results.

In a real business context, we could present these clusters (mainly the Insiders one) to the business/CRM/marketing team and let them decide what should be done regarding marketing actions and customer delight programs.
Cluster Personas: Every cluster characteristc should drive a marketing action.

The cluster 2 is the most valuable customer cluster, the INSIDERS one. They are responsible for 65% of profit share and it represents 30% of all customers.
The Cluster 1 has the highest avr_ticket and highest frequency of purchase, they are very engaged and almost part of the Insiders Cluster.
The cluster 3 has the highest recency days between the last purchase, low engagement.
The remaining clusters (0, 4, 5) has no highlights but should be monitored.

Cluster Dashboard:
![image](https://user-images.githubusercontent.com/73034020/203866250-57c61fd1-6746-4fb7-ac20-f0e12d392aea.png)


## 7) Deploy on AWS
Infrastructure and planning

![image](https://github.com/ViniciusKos/insiders_clustering/assets/73034020/929a53f0-97b7-4dca-b272-0fe9ddde0765)





