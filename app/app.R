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
library(magrittr) # needs to be run every time you start R and want to use %>%
library(dplyr)    # alternatively, this also loads %>%
library(tidyr)

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


df2 <- data.frame(df)

colnames(df)

df2 <- df2 %>% pivot_wider( id_cols = cluster, 
                            values_from = c("gross_revenue","recencydays","n_purchases_unique","qtd_items","qtd_items_return"),
                            values_fn = mean )


# Create dashboard
ui <- fluidPage()

server <- function( input, output, session) {}


shinyApp( ui, server)

