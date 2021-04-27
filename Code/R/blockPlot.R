## blockPlot: produce a string with blocks indicating where the data is
## python equivalent: blockPlot.py
## E Klein
## eklein at ocean-analytics dot com dot au

blockPlot = function(x, lineLength = 80){
  ## blockPlot: produce a string with blocks indicating where the data is
  ## make data 1 no data 0
  blockSymbols = c('\u2593', '\u2591')
  xOne = as.numeric(is.na(x))
  xRLE = rle(xOne)
  blockFactor = lineLength/sum(xRLE$lengths)
  strPlot = character()
  for (i in 1:length(xRLE$lengths)){
    strPlot = paste0(strPlot, paste0(rep(blockSymbols[xRLE$values[i]+1], round(xRLE$lengths[i]*blockFactor)), collapse = ""), collapse = "")
  }
  # ## fix length of the blockplot
  nChars = lineLength - nchar(strPlot)
  if (nChars>0){
    strPlot = paste0(strPlot, paste0(rep(blockSymbols[2], nChars), collapse=""))
  }else if (nChars<0){
    strPlot = substr(strPlot,1,lineLength)
  }
  return(strPlot)
}


