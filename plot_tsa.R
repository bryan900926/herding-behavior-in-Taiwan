plot_with_shaded_areas <- function(x,y,z,condition, shade_color = "yellow", line_color = "blue",title) {
  plot(x, y, type = "l", col = line_color, lwd = 2, xlab='date', ylab='value',main=title)
  shaded_indices <- which(condition(y))
  start_indices <- c(shaded_indices[1], shaded_indices[which(diff(shaded_indices) > 1) + 1])
  end_indices <- c(shaded_indices[which(diff(shaded_indices) > 1)], shaded_indices[length(shaded_indices)])
  for (i in seq_along(start_indices)) {
    x_shade <- c(x[start_indices[i]], x[end_indices[i]], x[end_indices[i]], x[start_indices[i]])
    y_shade <- c(min(y), min(y), max(y), max(y))
    polygon(x_shade, y_shade, col = shade_color, border = NA)
  }
  lines(x, y, col = line_color, lwd = 2)
}
library('readr')
df_us = read.csv("C:\\Users\\bryan\\OneDrive\\桌面\\python\\market_return^2.csv") 
df_us$date = as.Date(df_us$date)
plot_with_shaded_areas(df_us$date,df_us$sum_coef,df_us$p_value, condition = function(z) z <0.05, 
                       shade_color = "yellow",line_color = "blue","Sum of coefficient for market squared return in US market")
df_tw = read.csv("C:\\Users\\bryan\\OneDrive\\桌面\\python\\tw_rolling_var.csv") 
df_tw$date = as.Date(df_tw$date)
plot_with_shaded_areas(df_tw$date,df_tw$sum_coef,df_us$p_value, condition = function(z) z <0.05, 
                       shade_color = "yellow",line_color = "blue","Sum of coefficient for market squared return in TW market")
sectors = list('Paper and Packaging', 'Tourism and Leisure', 
           'Technology and Electronics', 'Consumer Goods and Services', 
           'Finance and Insurance', 'Energy and Environment', 
           'Manufacturing and Materials', 'Cultural and Creative Industries', 
           'Agriculture and Biotechnology')
plot_leading_sectors = function(leading_sector){
  par(mfrow = c(3, 3), mar = c(3, 3, 3, 3))
  for (caused_sector in sectors) {
    if (caused_sector != leading_sector) {
      print(caused_sector)
      file_path <- paste0("C:/Users/bryan/OneDrive/桌面/python/", leading_sector, "_", caused_sector, ".csv")
      if (!file.exists(file_path)) {
        file_path <- paste0("C:/Users/bryan/OneDrive/桌面/python/", caused_sector, "_", leading_sector, ".csv")
        }
      df <- read.csv(file_path,check.names = FALSE)
      coef_col <- paste0("sum_coef_", caused_sector)
      pval_col <- paste0("p_value_", caused_sector)
      df$date = as.Date(df$date)
      plot_with_shaded_areas(
        x = df$date,
        y = df[[coef_col]],
        z= df[[pval_col]],
        condition = function(z) z < 0.05,
        shade_color = "yellow",
        line_color = "blue",
        title = paste0("Spillover effect from ", leading_sector, " to ", caused_sector)
      )   }             
  }
  par(mfrow = c(1, 1))
  }
                                      

plot_leading_sectors('Technology and Electronics')
plot_leading_sectors('Finance and Insurance')
