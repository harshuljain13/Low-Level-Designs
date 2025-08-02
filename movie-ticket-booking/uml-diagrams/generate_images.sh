#!/bin/bash

# Generate PNG images from Mermaid files
echo "Generating UML diagram images..."

# Generate images for all diagrams
mmdc -i 01_movie_system.mmd -o 01_movie_system.png
mmdc -i 02_screen_hierarchy.mmd -o 02_screen_hierarchy.png
mmdc -i 03_seat_hierarchy.mmd -o 03_seat_hierarchy.png
mmdc -i 04_pricing_strategy.mmd -o 04_pricing_strategy.png
mmdc -i 05_user_hierarchy.mmd -o 05_user_hierarchy.png
mmdc -i 06_core_business_classes.mmd -o 06_core_business_classes.png
mmdc -i 07_manager_classes.mmd -o 07_manager_classes.png

echo "All images generated successfully!"
ls -la *.png 