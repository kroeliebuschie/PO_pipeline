#!/usr/bin/Rscript
## analyse the profit outpot files
##
## Author: Mehdi Nellen, 2015

library(tools)
library(ggplot2)

#get the sys args
args <- commandArgs(TRUE)

getRMS <- function(lines) {
  # This function will return a list of 
  # names and their RMSD
  
  # grep the names and RMS values
  names <- grep("##",  lines, value=TRUE) 
  rmsds <- grep("RMS", lines, value=TRUE) 
  
  # remove any unwanted text 
  names <- basename(names)
  rmsds <- gsub("RMS:| ", "", rmsds)

  # make numbers
  rmsds <- as.numeric(rmsds)

  # combine them
  table <- data.frame(names, rmsds, stringsAsFactors = FALSE) 
  return(table)
}

gg_color_hue <- function(n) {
  # function for ggplot colors
  hues = seq(15, 375, length=n+1)
  hcl(h=hues, l=65, c=100)[1:n]
}

# initiate a list
f.list <- list()
f.name <- character()

# loop over the sys args
for(ari in seq(length(args))) {
  print(paste("Reading lines from:",args[ari]))
  file.n <- basename(args[ari])
  con    <- file(args[ari], open="r")
  lines  <- readLines(con)
  rmstbl <- getRMS(lines)

  # make a list of all the output and 
  # make the listnames out of file names 
  f.list <- c(f.list, list(rmstbl))
  f.name <- c(f.name, file.n)
 
}

# after looping add the names to the list
names(f.list) <- f.name

## plotting
#reshape data 
res <- numeric()
for(li in names(f.list)) {
  df  <- f.list[names(f.list) == li][[1]][2]
  tmp <- data.frame(rep(li, length(df)), df, stringsAsFactors = FALSE)
  res <- rbind(res, tmp)
}
colnames(res) <- c("filenames", "RMS")

#plotting
pdf(file = "densityPlot.pdf",
          width = 10, height = 5)
p <- ggplot(data=res, aes(x=RMS, fill=filenames)) + geom_density(alpha = 0.5)
plot(p)
dev.off()
