# Instructions rqt Machine-Learning-Plugin (MLP) #
This repository offers a new rqt plugin that allows you to produce a dataset for machine learning. <br/>
#### In order to install the rqt plugin, MLP, please follow the following steps: ####
 * Install Ubuntu 14.04 64-bit
 * Install Indigo ROS distribution: http://wiki.ros.org/indigo/Installation/Ubuntu
 * Install and configure your ROS environment: http://wiki.ros.org/ROS/Tutorials/InstallingandConfiguringROSEnvironment
 * Install RoboTiCan project: http://wiki.ros.org/robotican/Tutorials/Installation
 * Install python and the following python packages:
    * Install pandas package:
      ```{r, engine='sh', count_lines}
      sudo apt-get install python-pip
      ```
      -- if you have dependence problems, run the following command to fix it:
      ```{r, engine='sh', count_lines}
      sudo apt-get -f install
      ```
      Then run:
      ```{r, engine='sh', count_lines}
      sudo pip install numpy
      sudo pip install pandas
      ```
    * Install statistics package:
         ```{r, engine='sh', count_lines}
      sudo pip install statistics
      ```

 * Download or clone this project using terminal/bash:
   ```{r, engine='sh', count_lines}
   cd ~/catkin_ws/src/
   git clone https://github.com/matansar/rqt_mlp.git
   ```
 * Run the setup.sh file and compile:
   ```{r, engine='sh', count_lines}
   cd ~/catkin_ws/src/rqt_mlp/install/setup.sh
   ```
 * First time you run rqt, you need to run:
   ```{r, engine='sh', count_lines}
   cd ~/catkin_ws/
   rqt --force-discover
   ```
