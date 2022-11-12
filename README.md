<img src=https://user-images.githubusercontent.com/64495168/129553804-9baec55b-e3bf-407c-a5f5-8b229490bd27.png alt="Rossmann logo" title="Rossmann" align="right" height="60" class="center"/>

# Customer Segmentation - Fidelity Program Insiders


## 1) Business Issue
Select the most valuable customers for a loyalty program.

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
The data was collected in Kaggle (UK-High value Customer Identification - https://www.kaggle.com/code/cheekonglim/uk-high-value-customers-identification) and all the columns attributes are explained below:

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

Through the mind map, we can compare our hypothesis by factors (like Country, Products, etc...) and their attributes (Store Size, Product Price, etc...)

There are some hypothesis judged to be most relevant and could drive our Exploratory Data Analysis. They are listed below.

1. Stores with larger assortments should sell more.
2. Stores with closer competitors should sell less.
3. Stores with longer competitors should sell more.
4. Stores with longer active promotions should sell more.
5. Stores with more promotion days should sell more.
6. Stores with more aggressive promotion should sell more
7. Stores with more consecutive promotions should sell more.
8. Stores open on the Christmas holiday should sell more.
9. Stores should sell more over the years.
10. Stores should sell more in the second half of the year.
11. Stores should sell more after the 10th of each month.
12. Stores should sell less on weekends.
13. Stores should sell less during school holidays.

Some of them might not be tested in advance for lack of information in this DataSet. Thus it can be tested in the next CRISP-DM circle.

**Below are the summary of the TOP 3 INSIGHTS achieved through the tested hypotheses.**
1. Stores with larger assortments should sell more. **TRUE**

![image](https://user-images.githubusercontent.com/73034020/180753446-e35fd0a4-9b15-44c5-80f7-3104ccbe1079.png)

![image](https://user-images.githubusercontent.com/73034020/180751961-8b4593ec-df14-441b-afd7-b97414b57818.png)

There are proportionally more sales in bigger assortments than the basic ones.

2. Stores should sell more in the second half of the year. **TRUE**

![image](https://user-images.githubusercontent.com/73034020/182120827-f38d1da6-5502-43dc-a779-2b4902fa387d.png)

Stores sell more in the second half of the year, especially in December.

3. Stores with closer competitors should sell less. **FALSE**

![image](https://user-images.githubusercontent.com/73034020/182124593-5d93259b-6c4a-4524-a1ce-c73a148009f3.png)


Stores sell more when close to competitors.

## 5) Machine learning models applied and performances.

Before starting the machine learning models tests, we should state a baseline, a metric to be beaten. Usually, a baseline is a simple prediction based on the mean of the values, in this case, the mean metrics are in the table below.

![image](https://user-images.githubusercontent.com/73034020/186864386-7c6a6c45-fb10-4255-8088-128ee901a06d.png)

Four different models were evaluated through time series cross-validation, the idea for this method is to divide the training set into two folds at each iteration on the condition that the validation set is always ahead of the training set, below it's shown how it works.

![cv](https://user-images.githubusercontent.com/73034020/182566611-46001688-3c88-4799-90c6-6fc007c990ec.png)

These four models got the following cross-val results:

![image](https://user-images.githubusercontent.com/73034020/182563192-4d98c42f-542e-41bf-8fad-e5439afd5cd6.png)

Although RandomForestRegressor performed better we are going to choose XGBRegressor as the "winner" model, because it is much lighter to operate in production 
and it doesn't have a big difference in RMSE (Root Mean Squared Error). 
It is very important to consider the model performance WHILE in PRODUCTION.

**Hyperparameter tuning and final model**

After the candidate model selection, we need to optimize it through hyperparameter tuning. In this project it was tuned:
n_estimators, learning_rate, max_depth, subsample, colsample_bytee, min_child_weight and gamma.

The train and test results of the chosen model considering performance in production are shown below.

Train:  
![image](https://user-images.githubusercontent.com/73034020/182584516-327c9baa-2633-4f2d-a094-7aa52e743682.png)

Final evaluation on holdout set:  
![image](https://user-images.githubusercontent.com/73034020/182584550-766751f2-486a-4b66-ab88-610532d6b46c.png)

Comparing our tuned model with the baseline:
(1817.7/1331.4)-1 = 36,5%
Our final model has an RMSE of 36,5% less than simply calculating the sales average.



## 6) Business Results.
After the prediction’s evaluation, we must translate the model performance to the business.
One of the most intuitive ways to do so is by showing easier interpretable performance metrics like error and percentage error:
error: sales-predictions
error rate: predictions/sales  

![image](https://user-images.githubusercontent.com/73034020/182585638-53d3052e-158b-4d9f-9f85-8514e723a9d1.png)  

The top-left graph shows us the predictions are close to the real sales values.  
The top-right graph shows us the prediction’s errors tend to underestimate the real sales value.  
The bottom-left graph shows us the error predictions are mainly distributed around 0, which is a very good indicator.  
The bottom-right graph shows us the model performance is consistent through all sales magnitude sizes.  

Overall, the model performed well (better than a simple average prediction), however following the CRISP methodology, if a new round is needed, it may be considered to train stores individually or even in groups of them, for example. Another possibility is to explore other machine learning models as well as new features.

Further details on business performance are available in the notebook.

## 7) Deploy to the Google Cloud.
Both the model and telegram Bot was deployed on Google Cloud Platform.
To get the prediction, type the store number in the telegram bot and deliver the forecast for the next 6 weeks.

An example of the bot working is shown below:
![Animation3](https://user-images.githubusercontent.com/73034020/189437514-b52a4492-bad2-4f2f-830a-1bf76260bea7.gif)

## 8) Next Steps:
Re-evaluate the set of parameters' models including more parameters in or making a different optimation strategy, i.e the Bayesian Search.
Include the pessimistic and positivistic scenarios in predictions.



