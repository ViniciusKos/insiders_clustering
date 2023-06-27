#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

#install.packages("ztable")

library(ztable)


setwd("P:/Python/GitHub/insiders_clustering/app")
# renv::init("P:/Python/GitHub/insiders_clustering/app")
# renv::snapshot()
# renv::status()
# renv::restore()
# install.packages("RSQLite")
# install.packages("shinydashboard")
# Load Packages 
library(shiny)
library(ggplot2)
library(DBI)
library(shinydashboard)
library(magrittr) # needs to be run every time you start R and want to use %>%
library(dplyr)    # alternatively, this also loads %>%


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


# Create dashboard


ui <- dashboardPage( 
  dashboardHeader(title = "Most Valuable Customers Analysis"),
  
  dashboardSidebar(
    sidebarMenu(
      # Create two `menuItem()`s, "Dashboard" and "data"
      menuItem(text = "Dashboard",
               tabName = "dashboard"), 
      menuItem(text = "Data", 
               tabName = "data"))),
    
  dashboardBody(
    tabItems(
      # Option 1 content
      tabItem(tabName = "dashboard",
              h2("Dashboard"),
              fluidRow(
                box(width = 12, plotOutput("plot"))
              )
      ),
      
      # Option 2 content
      tabItem(tabName = "data",
              h2("Data"),
              fluidRow(
                box(width = 12, dataTableOutput("table")))
              ))))

server <- function( input, output, session) {
  observeEvent(input$sidebarItemExpanded, {
    selectedTab <- input$sidebarItemExpanded
    
    if (selectedTab == "dashboard") {
      updateTabItems(session, "sidebar", selected="dashboard")}
    else if (selectedTab == "data") {
      updateTabItems(session, "sidebar", selected="data")}})
  output$plot <- renderPlot({
    ggplot(df, aes(x=cluster, y=profit)) +
             geom_point() +
             labs(x = "Cylinders", y="Miles per Gallon") +
             theme_minimal()})
  output$table <- renderPlot({
    ztable(df) %>% 
      makeHeatmap(palette="Blues")
    
  })
  
  }


shinyApp( ui, server)

