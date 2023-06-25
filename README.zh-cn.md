有点懒，先用chatgpt翻译一下英文的，晚点改

这个FEH开放助手是基于Python图像识别的游戏辅助工具。它包括两个主要功能，自动许愿助手和主线剧情通关助手。同时，它带有一个简陋的界面用于详细设置。由于FEH是一款移动游戏，你需要明智地选择一个模拟器。在我的测试环境中，我设置了一个LDPlayer（Android 9）和一个MuMu Player 12（Android 12），分辨率为540P进行测试。

警告！作者对使用本项目或无法使用本项目而导致的任何直接或间接损失不承担责任。这包括但不限于宝石损失、账号封禁等。

如果在使用过程中遇到任何问题，可以向我寻求帮助。

## Folder structure

- **/logs**: Holds log files generated by the project during runtime. 
- **/finished_wishes**: Records the history of past wishes with screenshots.
- **/config**: Holds configuration files or settings used in the project.(would be created when the program started)
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
  - **/pics/aftergame_close.png**
  - **/pics/auto_confirm.png**
  - **/pics/auto_ingame.png**
  - **/pics/backward.png**
  - **/pics/give_up.png**
  - **/pics/haschamp.png**
  - **/pics/main_ticked.png**
  - **/pics/over.png**
  - **/pics/refill.png**
  - **/pics/second_ticked.png**
  - **/pics/skip.png**
  - **/pics/ship_green.png**
  - **/pics/stage_clear.png**
  - **/pics/stage_clear_part.png**
  - **/pics/start_fight.png**
  - **/pics/start_fight_ingame.png**


## Requirements

- pip install pygetwindow
- pip install opencv-python
- pip install pyautogui
- pip install numpy
- pip install scikit-image
- pip install tkinter
- pip install configparser

## 如何使用

> 首先，你需要将主要按钮和图标的截图作为模板，它们在上面的"Folder structure"部分中列出。我会在sample_pics文件夹中提供我用于测试的模板，但是即使模拟器的设置与我的相同，由于界面略有差异（某些模拟器将侧边栏计入分辨率，而其他模拟器则不计入），它们可能并不适用。我强烈建议你自己截图，并牢记一点，一旦你改变了游戏中资源的质量，先前的模板可能也无法正常工作。

> 其次，你需要在环境设置中关闭必要的设置，例如动画效果。

![ingame settings](sample_pictures/e_settings.png)

---

> 在这些步骤完成后，你可以开始配置并运行程序。

---

![ingame settings](sample_pictures/main_menu_1.png)

> 对于主线剧情通关助手，你需要根据你使用的模拟器输入窗口名称，它不需要是完整的窗口名称，你可以使用关键字来完成。但是请注意，使用不准确的关键字可能会将其他窗口错误地视为模拟器。
> 
> 对于template_path，它最初设计为模板文件夹的绝对路径，但我懒得更改。因此，模板文件夹现在被固定在与代码/可执行文件相同的文件夹下。但是，你可以使用不同的后缀来使程序读取不同的文件夹以进行不同的任务。例如，默认文件夹是/pics/first_level，如果你需要在困难模式下运行，你可以重新截取屏幕截图作为模板，并创建一个/pics/first_level_hard文件夹来存储它们。然后，只需要在template_name项中添加"_hard"。请记住，更改此设置不会更改对按钮的识别，因此如果你想更改模拟器的分辨率，你需要手动替换pics文件夹下的模板。
> 
> 阈值滑块表示模拟器中的按钮图像与模板的相似度容忍度，你可以根据运行情况调整该值。
> 
> 下面的单选按钮决定了在主菜单和二级菜单中检查模板的算法，第二个选项会主动减少与勾选图标匹配的结果，而第一个选项则不会。因此，第一个选项可能会导致程序在低阈值下意外选择通过的关卡，而第二个选项在高阈值下无法正确识别图标。请在你自己的环境中进行测试，并选择适当的阈值。
> 
> 最后两个选项给用户提供了在获得识别到的模板的坐标后调整程序点击位置的能力。由于图像识别方法可能会给出具有轻微偏移的坐标，例如位于左上角，而按钮可能无法被正确点击，你可以添加一些偏移量来纠正这个问题。
> 完成上述步骤后，你可以开始使用这个工具。你需要前往下面列出的菜单。

![ingame settings](sample_pictures/first_level.png)

> 它将直接进行一整部的剧情通关。但是你仍然需要手动切换到另一部剧情，因为我认为一次通关所有剧情可能并不需要。另外，你需要确保你的队伍足够强大，如果被击败，程序将终止运行。



---