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
    max_revenue <- max(cluster_data$Revenue)
    colors <- ifelse(cluster_data$Revenue == max_revenue, "#1F77B4", "#AEC6CF")
    plot_ly(
      data = cluster_data,
      x = ~Revenue,
      y = ~Cluster,
      type = "bar",
      name = "Revenue",
      orientation = "h",
      marker = list(color = colors)
    ) %>%
      layout(
        title = "Revenue Comparison",
        xaxis = list(title = "Revenue"),
        yaxis = list(title = "Cluster"),
        annotations = list(
          x = cluster_data$Revenue,
          y = cluster_data$Cluster,
          text = cluster_data$Revenue,
          showarrow = FALSE,
          font = list(size = 12, color = "black")
        )
      )
  })
  
  # Render satisfaction plot
  output$satisfaction_plot <- renderPlotly({
    max_satisfaction <- max(cluster_data$Satisfaction)
    colors <- ifelse(cluster_data$Satisfaction == max_satisfaction, "#1F77B4", "#AEC6CF")
    plot_ly(
      data = cluster_data,
      x = ~Satisfaction,
      y = ~Cluster,
      type = "bar",
      name = "Satisfaction",
      orientation = "h",
      marker = list(color = colors)
    ) %>%
      layout(
        title = "Satisfaction Comparison",
        xaxis = list(title = "Satisfaction"),
        yaxis = list(title = "Cluster"),
        annotations = list(
          x = cluster_data$Satisfaction,
          y = cluster_data$Cluster,
          text = cluster_data$Satisfaction,
          showarrow = FALSE,
          font = list(size = 12, color = "black")
        )
      )
  })
}

# Run the app
shinyApp(ui, server)
