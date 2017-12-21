ggplot(boxplot.melt, aes(x=DIS, y=value, fill=RE)) + facet_wrap( ~ RE) +
geom_violin() + scale_fill_manual(values=c('lightblue', 'gray')) +
guides(fill=guide_legend(title='Readmissions')) +
xlab( 'Discharge Disposition') + ylab('Length of Stay') +
ggtitle('Violin Plots of Length of Stay by Readmission Status and Discharge Disposition')
