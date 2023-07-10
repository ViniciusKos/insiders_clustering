library(shiny)

# Define the UI
ui <- fluidPage(
  titlePanel("KPI Panel"),
  fluidRow(
    column(
      width = 2,
      align = "center",
      valueBoxOutput("kpi1"),
      valueBoxOutput("kpi2"),
      valueBoxOutput("kpi3"),
      valueBoxOutput("kpi4"),
      valueBoxOutput("kpi5"),
      valueBoxOutput("kpi6")
    )
  )
)

# Define the server logic
server <- function(input, output) {
  
  # KPI values
  kpi_values <- c(100, 80, 70, 90, 95, 75)
  
  output$kpi1 <- renderValueBox({
    valueBox(
      kpi_values[1],
      "KPI 1",
      icon = icon("check"),
      color = "green"
    )
  })

}

# Run the Shiny app
shinyApp(ui, server)

