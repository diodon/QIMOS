#!/bin/bash
## get VISST HW8 cloud product from satcorps
## clip the image to GBR region (lat -30, -7,45, lon 141, 160)
## extract cloud_percentage variable for cloud_type 1 (total cloud)
## concatenate into daily files
## E Klein. eklein@gmail.com
## last version 20201020

for yy in $(seq 2018 2019) 
do
    echo $yy
    lftp -e "cls -1 > months.txt; exit" "https://satcorps.larc.nasa.gov/prod/HIMWARI-FD/visst-grid-netcdf/$yy"
    #for mm in $(cat months.txt)
    for mm in {11..12}
    do
        echo $mm
        lftp -e "cls -1 > days.txt; exit" "https://satcorps.larc.nasa.gov/prod/HIMWARI-FD/visst-grid-netcdf/$yy/$mm"
        for dd in $(cat days.txt)
        do
            echo $dd
            lftp -e "mirror -i SH -O ./TMP/; exit" "https://satcorps.larc.nasa.gov/DPO-prod/HIMWARI-FD/visst-grid-netcdf/$yy/$mm/$dd"
            cd ./TMP
            for ff in $(ls *.NC)
            do
                echo $ff
                ncks --mk_rec_dim time -v cloud_percentage -d lat,391,481 -d lon,1028,1089 -d cld_type,0,0 $ff ../GBR/GBR_$ff
            done
            rm *.NC
            cd ../GBR
            ncrcat *.NC GBR_cloud-percentage_$yy$mm$dd.nc
            rm *.NC
            cd ..
            #break
        done
        #break
    done
done

