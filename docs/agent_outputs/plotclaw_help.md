# plotclaw: /help

PlotClaw v3 - 13 Chart Types + Data I/O
  CHARTS:   /bar /pie /plot /scatter /hist /box /heatmap /polar /surface /compare /animate /stats /dashboard
  DATA:     /csv <file.csv> [column] [chart_type]  |  /data (list files)  |  /import <file.json>
  SHARED:   /shared read [key]  |  /shared write key:value  |  /publish <data>
  DELEGATE: /delegate <agent> <task>
  FLAGS:    --ylim 0,100 --xlim -5,5 --figsize 12,8 --dpi 200 --fontsize 12 --cmap magma --theme dark
            --format svg|pdf|png --save-only
  /stats