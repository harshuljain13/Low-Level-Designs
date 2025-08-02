#!/bin/bash

# Generate high-definition PNG images from Mermaid files
echo "Generating high-definition UML diagram images..."

# High-quality settings
WIDTH=3840
HEIGHT=2160
SCALE=3
THEME="custom_theme.css"

# Generate images for all diagrams with high-definition settings
echo "Generating 01_movie_system.png..."
mmdc -i 01_movie_system.mmd -o 01_movie_system.png -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 02_screen_hierarchy.png..."
mmdc -i 02_screen_hierarchy.mmd -o 02_screen_hierarchy.png -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 03_seat_hierarchy.png..."
mmdc -i 03_seat_hierarchy.mmd -o 03_seat_hierarchy.png -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 04_pricing_strategy.png..."
mmdc -i 04_pricing_strategy.mmd -o 04_pricing_strategy.png -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 05_user_hierarchy.png..."
mmdc -i 05_user_hierarchy.mmd -o 05_user_hierarchy.png -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 06_core_business_classes.png..."
mmdc -i 06_core_business_classes.mmd -o 06_core_business_classes.png -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 07_manager_classes.png..."
mmdc -i 07_manager_classes.mmd -o 07_manager_classes.png -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "Generating 08_complete_system.png..."
mmdc -i 08_complete_system_simplified.mmd -o 08_complete_system.png -b transparent -w $WIDTH -H $HEIGHT --scale $SCALE -C $THEME

echo "All high-definition images generated successfully!"
echo "File sizes:"
ls -lh *.png 