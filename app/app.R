


setwd("P:/Python/GitHub/insiders_clustering/app")
# renv::init("P:/Python/GitHub/insiders_clustering/app")
# renv::snapshot()
# renv::status()
# renv::restore()

# Load Packages 
library(shiny)
library(ggplot2)
library(DBI)
library(magrittr) # needs to be run every time you start R and want to use %>%
library(dplyr)    # alternatively, this also loads %>%
library(shinydashboard)
library(scales)
library(viridis)
library(plotly)


# Query data in Database

mydb <- dbConnect(RSQLite::SQLite(), "P:/Python/GitHub/insiders_clustering/insiders_cluster.db")
dbGetQuery(mydb, "SELECT 
    name
FROM 
    sqlite_master
WHERE 
    type ='table' AND 
    name NOT LIKE 'sqlite_%';")

df <- dbGetQuery(mydb, "SELECT * FROM insiders")

dbDisconnect(mydb)

head(df)


distincts_clusters <- length(unique(df[["cluster"]]))

qtd_total_customers <- df %>% nrow()

qtd_loyal_customers <- df %>% filter(cluster==3) %>% nrow()

proportion_loyal <- qtd_loyal_customers/qtd_total_customers %>% trunc(digits=2)


# Set the path to the file
file_path <- paste0(getwd(),"/insiders_cluster.db")
file_info <- file.info(file_path)
last_modified <- file_info$mtime
print(last_modified)



df2 <- data.frame(df) %>% group_by(cluster) %>% 
  summarise(across(everything(), mean, .names = "{.col}"),customers = n()) %>% 
  select(c("cluster","customers","gross_revenue", "recencydays", "n_purchases_unique","qtd_items", "qtd_items_return")) %>% 
  ungroup()
df2$cluster <- df2$cluster+1
df2$recencyweeks <- df2$recencydays/7
df2


cl <- "cluster"

df2[[cl]]



qtd_total_customers

# Create dashboard

header <- dashboardHeader( title = "Insiders Clustering" )

sidebar <- dashboardSidebar(disable = TRUE)

body <- dashboardBody(
  fluidRow(
    infoBox("Total Customers", value=qtd_total_customers, subtitle="customers", icon = icon("people-group",verify_fa = FALSE), color="light-blue", width=3),
    infoBox("Loyal Customers", value=qtd_loyal_customers, subtitle="customers", icon = icon("crown",verify_fa = FALSE), color="light-blue", width=3),
    infoBox("Proportion loyal", value=label_percent()(proportion_loyal), icon = icon("percent",verify_fa = FALSE), color="light-blue", width=3),
    infoBox("Distinct Groups", value=distincts_clusters, icon = icon("user-group",verify_fa = FALSE), color="light-blue", width=3)
  ),
  fluidRow(
    box(
      title = "Number of Customers",
      status = "primary",
      solidHeader = TRUE,
      width = 4,
      plotlyOutput(outputId = "customer_plot")
    ),
      box(
        title = "Revenue Comparison",
        status = "primary",
        solidHeader = TRUE,
        width = 4,
        plotlyOutput(outputId = "revenue_plot")
      ),
    box(
      title = "Recency Weeks",
      status = "primary",
      solidHeader = TRUE,
      width = 4,
      plotlyOutput(outputId = "recency_plot")
    ))
  )

ui <- dashboardPage( header, sidebar, body)


server <- function( input, output, session) {
  
  df2["customers"]
  
    colors1 <- ifelse(df2[["customers"]] == max(df2["customers"]), "#1F77B4", "#AEC6CF")
    
    output$customer_plot <- renderPlotly({
      plot_ly(df2, x = ~customers, y = ~cluster, type = 'bar',
              orientation = 'h',
              marker = list(color = colors1)) %>%
        layout(title = "Customers by Cluster",
               xaxis = list(title = "Number of Customers"),
               yaxis = list(title = "Cluster"),
               annotations = list(
                 x = df2[["customers"]],
                 y = df2[["cluster"]],
                 text = round(df2[["customers"]]),
                 showarrow = FALSE,
                 font = list(size = 12, color = "black"
                             )))})
    
    colors2 <- ifelse(df2[["gross_revenue"]] == max(df2["gross_revenue"]), "#1F77B4", "#AEC6CF")
    
    output$revenue_plot <- renderPlotly({
    plot_ly(df2, x = ~gross_revenue, y = ~cluster, type = 'bar',
            orientation = 'h',
            marker = list(color = colors2)) %>%
      layout(title = "Gross_Revenue by Cluster",
             xaxis = list(title = "Gross Revenue $"),
             yaxis = list(title = "Cluster"),
             annotations = list(
               x = df2[["gross_revenue"]],
               y = df2[["cluster"]],
               text = round(df2[["gross_revenue"]]),
               showarrow = FALSE,
               font = list(size = 12, color = "black")))})
      
      
      colors3 <- ifelse(df2[["recencydays"]] == max(df2["recencydays"]), "#1F77B4", "#AEC6CF")
      
      variablex <- "recencyweeks"
      
      output$recency_plot <- renderPlotly({
        plot_ly(df2, x = ~recencydays, y = ~cluster, type = 'bar',
                orientation = 'h',
                marker = list(color = colors3)) %>%
          layout(title = "Recency Weeks by Cluster",
                 xaxis = list(title = "Recency Weeks"),
                 yaxis = list(title = "Cluster"),
                 annotations = list(
                   x = df2[[variablex]],
                   y = df2[["cluster"]],
                   text = round(df2[[variablex]]),
                   showarrow = FALSE,
                   font = list(size = 12, color = "black")
                    ))})
      
}


shinyApp( ui, server)