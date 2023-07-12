


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

qtd_loyal_customers <- df %>% filter(cluster==2) %>% nrow()

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
df2


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
      title = "Revenue Comparison",
      status = "primary",
      solidHeader = TRUE,
      width = 6,
      plotlyOutput(outputId = "revenue_plot")
    ),
  ))


ui <- dashboardPage( header, sidebar, body)


server <- function( input, output, session) {
  output$revenue_plot <- renderPlotly({
    plot_ly(
      data = df2,
      x = ~cluster,
      y = ~gross_revenue,
      type = "bar",
      name = "Revenue",
      marker = list(color = "#007BFF")
    ) %>%
      layout(
        title = "Revenue Comparison",
        xaxis = list(title = "Cluster"),
        yaxis = list(title = "Revenue"),
        annotations = list(
          x = df2$cluster,
          y = df2$gross_revenue,
          text = df2$gross_revenue,
          showarrow = FALSE,
          font = list(size = 12, color = "black")
        )
      )
  })
  
  }



shinyApp( ui, server)