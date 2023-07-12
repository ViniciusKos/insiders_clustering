library(shiny)
library(shinydashboard)
library(plotly)

# Sample data
cluster_data <- data.frame(
  Cluster = c("Cluster A", "Cluster B", "Cluster C"),
  Revenue = c(5000, 3000, 4000),
  Satisfaction = c(4, 3, 5)
)

# UI
ui <- dashboardPage(
  dashboardHeader(title = "Cluster Comparison"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Cluster Comparison", tabName = "cluster_comparison")
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(
        tabName = "cluster_comparison",
        fluidRow(
          box(
            title = "Revenue Comparison",
            status = "primary",
            solidHeader = TRUE,
            width = 6,
            plotlyOutput(outputId = "revenue_plot")
          ),
          box(
            title = "Satisfaction Comparison",
            status = "primary",
            solidHeader = TRUE,
            width = 6,
            plotlyOutput(outputId = "satisfaction_plot")
          )
        )
      )
    )
    )
  )


# Server
server <- function(input, output) {
  # Render revenue plot
  output$revenue_plot <- renderPlotly({
    plot_ly(
      data = cluster_data,
      x = ~Cluster,
      y = ~Revenue,
      type = "bar",
      name = "Revenue",
      marker = list(color = "#007BFF")
    ) %>%
      layout(
        title = "Revenue Comparison",
        xaxis = list(title = "Cluster"),
        yaxis = list(title = "Revenue"),
        annotations = list(
          x = cluster_data$Cluster,
          y = cluster_data$Revenue,
          text = cluster_data$Revenue,
          showarrow = FALSE,
          font = list(size = 12, color = "black")
        )
      )
  })
  
  # Render satisfaction plot
  output$satisfaction_plot <- renderPlotly({
    plot_ly(
      data = cluster_data,
      x = ~Cluster,
      y = ~Satisfaction,
      type = "bar",
      name = "Satisfaction",
      marker = list(color = "#FFC107")
    ) %>%
      layout(
        title = "Satisfaction Comparison",
        xaxis = list(title = "Cluster"),
        yaxis = list(title = "Satisfaction"),
        annotations = list(
          x = cluster_data$Cluster,
          y = cluster_data$Satisfaction,
          text = cluster_data$Satisfaction,
          showarrow = FALSE,
          font = list(size = 12, color = "black")
        )
      )
  })
}

# Run the app
shinyApp(ui, server)
