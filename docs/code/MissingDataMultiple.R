plot_missing <- function(dr, filename, number, percent = TRUE){
  library(tidyverse)
  library(patchwork)
  f <- paste(dr, "/", filename, "_", 1, ".csv", sep = "")
  print(f)
  df <- read.csv(f)
  
  missing_patterns <- data.frame(is.na(df)) %>%
    group_by_all() %>%
    count(name = "count", sort = TRUE) %>%
    ungroup()
  for (i in 2:number){
    stringi = as.character(i)
    text = paste("C:/Users/juhyu/eclipse-workspace/ChessData/600+0_", stringi, ".csv", sep = "")
    print(text)
    df <- read.csv(text)
    mp <- data.frame(is.na(df)) %>%
      group_by_all() %>%
      count(name = "count", sort = TRUE) %>%
      ungroup()
    missing_patterns$count = missing_patterns$count + mp$count
  }
  missing_patterns[missing_patterns == "WhiteRatingDiff"] = "WRatingDiff"
  missing_patterns[missing_patterns == "BlackRatingDiff"] = "BRatingDiff"
  
    dim <- dim(missing_patterns)
  plot1var<- data.frame(names = colnames(missing_patterns)[1:dim[2]-1],
                        count = rep(0, dim[2]-1))
  overall1 = sum(missing_patterns$count)
  for (j in 1:(dim[2]-1)){
    sum = 0
    for(i in 1:dim[1]){
      if(missing_patterns[i, j] == TRUE){
        sum = sum + missing_patterns$count[i]
      }
    }
    plot1var$count[j] = sum
  }
  
  plot1var <- plot1var[order(-plot1var$count),]
  plot1var$names <- factor(plot1var$names, levels = plot1var$names)
  
  complete <- c(-1)
  labels <- c("")
  for (i in 1:dim[1]){
    x = FALSE
    for (j in 1:(dim[2] - 2)){
      x = x | missing_patterns[i, j]
    }
    if(!x){
      complete <- append(complete, i)
      labels <- append(labels, "complete cases")
    }
    else{
      labels <- append(labels, "")
    }
  }
  labels <- labels[2:dim[1] + 1]
  pat <- missing_patterns %>% rownames_to_column("id") %>%
    gather(key, value, -id) %>%
    mutate(missing = ifelse(value, "yes", "no"))
  for (i in 1:dim[1]){
    if(is.element(i, complete)){
      pat[pat$id == i, 'missing']<- 'complete'
    }
  }
  pat$missing <- as.factor(pat$missing)
  plot2var <- filter(pat, key != 'count' & key != 'incomplete')
  plot2var$id <- as.integer(plot2var$id)
  plot2var$id <- as.factor(plot2var$id)
  
  plot3var <- select(missing_patterns, count)
  plot3var$ind = 1:dim[1]
  plot3var$ind <- as.factor(plot3var$ind)
  overall3 = sum(plot3var$count)
  colors <- 1:dim[1]
  for (i in plot3var$ind){
    if(is.element(i, complete)){
      colors[i] <- "#6BAED6"
    }
    else{
      colors[i] <- "#BDD7E7"
    }
  }
  plt1lab = "num rows missing"
  plt3lab = "row count"
  
  
  p1 <- ggplot(data = plot1var, aes(x = fct_inorder(names), y = count)) + 
    geom_bar(stat = "identity", fill = "#6BAED6") + 
    ggtitle("Missing value patterns") + 
    labs(x = "", y = plt1lab) + 
    theme_bw() + 
    theme(legend.position = "none")
  p2 <- ggplot(plot2var, aes(x = key, y = fct_rev(id))) + 
    geom_raster(aes(fill = missing)) + 
    scale_fill_manual(values = c("darkgrey", "grey", "#6BAED6")) +
    theme_bw() + 
    labs(x = "variable", y = "missing pattern") + 
    theme(legend.position = "none")
  p3 <- ggplot(data = plot3var, aes(x = ind, y = count, fill = ind)) + 
    geom_bar(stat = "identity") + 
    scale_fill_manual(values = colors) + 
    labs(x = "", y = plt3lab) + 
    theme_bw() + 
    theme(legend.position = "none") +
    scale_x_discrete(limits = rev(levels(plot3var$ind))) + 
    coord_flip()
  if(percent == TRUE){
    plt1lab = "% rows missing"
    plot1var$count = plot1var$count / overall1 * 100
    plt3lab = "% rows"
    plot3var$count = plot3var$count / overall3 * 100
    
    p1 <- ggplot(data = plot1var, aes(x = fct_inorder(names), y = count)) + 
      geom_bar(stat = "identity", fill = "#6BAED6") + 
      ggtitle("Missing value patterns") + 
      labs(x = "", y = plt1lab) + 
      ylim(0, 10) + 
      theme_bw() + 
      theme(legend.position = "none")
    p3 <- ggplot(data = plot3var, aes(x = ind, y = count, fill = ind)) + 
      geom_bar(stat = "identity") + 
      scale_fill_manual(values = colors) + 
      labs(x = "", y = plt3lab) + 
      ylim(0, 100) + 
      theme_bw() +
      theme(legend.position = "none") +
      scale_x_discrete(limits = rev(levels(plot3var$ind))) + 
      coord_flip()
  }
  p1 + plot_spacer()+ p2 + p3 +
    plot_layout(widths = c(4, 1), heights = c(1, 3))
}