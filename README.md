# Fire-Emblem-Hero-Auto-Player
This FEH open helper is a game helper based on python image recognition. It includes two major functions, an auto wishes helper and main story passer. And it comes with an ugly interface for the detailed settings.
Since FEH is a mobile game, you need to select an emulator wisely. In my test environment, i set up a LDPlayer (Andriod 9) and a MuMu Player 12(Andriod 12) in 540P for testing.

Warning! The author is not liable for any direct or indirect losses caused by the use of this project or the inability to use it. This includes, but is not limited to, loss of gems, account bann.

## Folder structure

- **/logs**: Holds log files generated by the project during runtime. 
- **/finished_wishes**: Records the history of past wishes with screenshots.
- **/config**: Holds configuration files or settings used in the project.
  - **/config/config_loot.ini** Stores the settings for loot help
  - **/config/config_passer.ini** Stores the settings for story passer
- **/pics**: This folder holds the necessary templates for image recognition
  - **/pics/first_level**: Contains the templates for main menu. Since the icon is animated, so you can add different exclamation marks and corner of the icon in the folder for better recognition. 
  - **/pics/second_level**: Contains the templates for second menu, and the same with above one. *Detailed usage would be explained below.*
  - **/pics/loot**: Contains the templates for loot helper
    - **/pics/loot/colors/**: Groups the templates with different colors
      - **/pics/loot/colors/blue_with_pos**
      - **/pics/loot/colors/blue_hide_with_pos**
      - **/pics/loot/colors/green_with_pos**
      - **/pics/loot/colors/green_hide_with_pos**
      - **/pics/loot/colors/red_with_pos**
      - **/pics/loot/colors/red_hide_with_pos**
      - **/pics/loot/colors/white_with_pos**
      - **/pics/loot/colors/white_hide_with_pos**

## Requirements

pip install pygetwindow
pip install opencv-python
pip install pyautogui
pip install numpy
pip install scikit-image
pip install tkinter
pip install configparser

## How to use it
