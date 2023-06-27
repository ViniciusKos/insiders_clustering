library(shiny)
library(shinydashboard)
library(ggplot2)
library(dplyr)

# Sample customer data
mydb <- dbConnect(RSQLite::SQLite(), "P:/Python/GitHub/insiders_clustering/insiders_cluster.db")
dbGetQuery(mydb, "SELECT 
    name
FROM 
    sqlite_master
WHERE 
    type ='table' AND 
    name NOT LIKE 'sqlite_%';")

customer_data <- dbGetQuery(mydb, "SELECT * FROM insiders")

dbDisconnect(mydb)



# Define UI
ui <- dashboardPage(
  dashboardHeader(title = "Customer Cluster Analysis"),
  dashboardSidebar(),
  dashboardBody(
    fluidRow(
      box(
        title = "Gross Revenue vs. Gross Returns",
        status = "primary",
        solidHeader = TRUE,
        collapsible = TRUE,
        width = 6,
        plotOutput("revenue_returns_plot")
      ),
      box(
        title = "Recency vs. Frequency",
        status = "primary",
        solidHeader = TRUE,
        collapsible = TRUE,
        width = 6,
        plotOutput("recency_frequency_plot")
      )
    ),
    fluidRow(
      box(
        title = "Number of Items vs. Number of Returns",
        status = "info",
        solidHeader = TRUE,
        collapsible = TRUE,
        width = 6,
        plotOutput("items_returns_plot")
      ),
      box(
        title = "Average Ticket by Cluster",
        status = "info",
        solidHeader = TRUE,
        collapsible = TRUE,
        width = 6,
        plotOutput("avg_ticket_plot")
      )
    ),
    fluidRow(
      box(
        title = "Profit by Cluster",
        status = "warning",
        solidHeader = TRUE,
        collapsible = TRUE,
        width = 12,
        plotOutput("profit_plot")
      )
    )
  )
)

# Define server
server <- function(input, output) {
  # Gross Revenue vs. Gross Returns plot
  output$revenue_returns_plot <- renderPlot({
    ggplot(customer_data, aes(x = gross_revenue, y = gross_returns, color = as.factor(cluster))) +
      geom_point() +
      labs(title = "Gross Revenue vs. Gross Returns",
           x = "Gross Revenue",
           y = "Gross Returns",
           color = "Cluster") +
      theme_minimal()
  })
  
  # Recency vs. Frequency plot
  output$recency_frequency_plot <- renderPlot({
    ggplot(customer_data, aes(x = recencydays, y = frequency, color = as.factor(cluster))) +
      geom_point() +
      labs(title = "Recency vs. Frequency",
           x = "Recency (Days)",
           y = "Frequency",
           color = "Cluster") +
      theme_minimal()
  })
  
  # Number of Items vs. Number of Returns plot
  output$items_returns_plot <- renderPlot({
    ggplot(customer_data, aes(x = qtd_items, y = qtd_items_return, color = as.factor(cluster))) +
      geom_point() +
      labs(title = "Number of Items vs. Number of Returns",
           x = "Number of Items",
           y = "Number of Returns",
           color = "Cluster") +
      theme_minimal()
  })
  
  # Average Ticket by Cluster plot
  output$avg_ticket_plot <- renderPlot({
    ggplot(customer_data, aes(x = as.factor(cluster), y = avg_ticket, fill = as.factor(cluster))) +
      geom_boxplot() +
      labs(title = "Average Ticket by Cluster",
           x = "Cluster",
           y = "Average Ticket",
           fill = "Cluster") +
      theme_minimal()
  })
  
  # Profit by Cluster plot
  output$profit_plot <- renderPlot({
    ggplot(customer_data, aes(x = as.factor(cluster), y = profit, fill = as.factor(cluster))) +
      geom_bar(stat = "identity") +
      labs(title = "Profit by Cluster",
           x = "Cluster",
           y = "Profit",
           fill = "Cluster") +
      theme_minimal()
  })
}

# Run the application
shinyApp(ui = ui, server = server)
