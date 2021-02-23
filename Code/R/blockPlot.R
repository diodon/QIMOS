## blockPlot: produce a string with blocks indicating where the data is
## python equivalent: blockPlot.py
## EKlein. 2020-10-29

blockPlot = function(x, lineLength = 80){
  ## make data 1 no data 0
  blockSymbols = c('\u2593', '\u2591')
  xOne = as.numeric(is.na(x))
  xRLE = rle(xOne)
  blockFactor = lineLength/sum(xRLE$lengths)
  strPlot = character()
  for (i in 1:length(xRLE$lengths)){
    strPlot = paste0(strPlot, paste0(rep(blockSymbols[xRLE$values[i]+1], round(xRLE$lengths[i]*blockFactor)), collapse = ""), collapse = "")
  }
  return(strPlot)
}


