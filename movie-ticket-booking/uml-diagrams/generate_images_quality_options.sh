#!/bin/bash

# Generate PNG images with different quality options
echo "UML Diagram Image Generator with Quality Options"
echo "================================================"
echo "1. Standard Quality (1920x1080, scale 1)"
echo "2. High Quality (2560x1440, scale 2)"
echo "3. Ultra HD (3840x2160, scale 3)"
echo "4. Print Quality (5120x2880, scale 4)"
echo ""

read -p "Select quality level (1-4): " quality

case $quality in
    1)
        WIDTH=1920
        HEIGHT=1080
        SCALE=1
        SUFFIX=""
        echo "Generating standard quality images..."
        ;;
    2)
        WIDTH=2560
        HEIGHT=1440
        SCALE=2
        SUFFIX="_hd"
        echo "Generating high quality images..."
        ;;
    3)
        WIDTH=3840
        HEIGHT=2160
        SCALE=3
        SUFFIX="_ultra_hd"
        echo "Generating ultra HD images..."
        ;;
    4)
        WIDTH=5120
        HEIGHT=2880
        SCALE=4
        SUFFIX="_print"
        echo "Generating print quality images..."
        ;;
    *)
        echo "Invalid option. Using standard quality."
        WIDTH=1920
        HEIGHT=1080
        SCALE=1
        SUFFIX=""
        ;;
esac

THEME="custom_theme.css"

# Generate images for all diagrams
echo "Generating 01_movie_system${SUFFIX}.png..."
mmdc -i 01_movie_system.mmd -o "01_movie_system${SUFFIX}.png" -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 02_screen_hierarchy${SUFFIX}.png..."
mmdc -i 02_screen_hierarchy.mmd -o "02_screen_hierarchy${SUFFIX}.png" -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 03_seat_hierarchy${SUFFIX}.png..."
mmdc -i 03_seat_hierarchy.mmd -o "03_seat_hierarchy${SUFFIX}.png" -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 04_pricing_strategy${SUFFIX}.png..."
mmdc -i 04_pricing_strategy.mmd -o "04_pricing_strategy${SUFFIX}.png" -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 05_user_hierarchy${SUFFIX}.png..."
mmdc -i 05_user_hierarchy.mmd -o "05_user_hierarchy${SUFFIX}.png" -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 06_core_business_classes${SUFFIX}.png..."
mmdc -i 06_core_business_classes.mmd -o "06_core_business_classes${SUFFIX}.png" -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 07_manager_classes${SUFFIX}.png..."
mmdc -i 07_manager_classes.mmd -o "07_manager_classes${SUFFIX}.png" -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 08_complete_system${SUFFIX}.png..."
mmdc -i 08_complete_system_simplified.mmd -o "08_complete_system${SUFFIX}.png" -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "All images generated successfully!"
echo "File sizes:"
ls -lh *${SUFFIX}.png 