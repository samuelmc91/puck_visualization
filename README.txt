###################### Puck Visualization ######################

Designed by Samuel M. Clark, Herbert J. Bernstein, Edwin Lazo

Copyright 01 Jun 2020, Samuel M. Clark as a copyleft for the GPL and LGPL

YOU MAY REDISTRIBUTE THE PUCK_VISUALIZATION PACKAGE UNDER THE TERMS OF THE GPL
                     
ALTERNATIVELY YOU MAY REDISTRIBUTE THE PUCK_VISUALIZATION API UNDER THE TERMS
OF THE LGPL

/*************************** GPL NOTICES ******************************
 *                                                                    *
 * This program is free software; you can redistribute it and/or      *
 * modify it under the terms of the GNU General Public License as     *
 * published by the Free Software Foundation; either version 2 of     *
 * (the License, or (at your option) any later version.               *
 *                                                                    *
 * This program is distributed in the hope that it will be useful,    *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of     *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the      *
 * GNU General Public License for more details.                       *
 *                                                                    *
 * You should have received a copy of the GNU General Public License  *
 * along with this program; if not, write to the Free Software        *
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA           *
 * 02111-1307  USA                                                    *
 *                                                                    *
 **********************************************************************/

/************************* LGPL NOTICES *******************************
 *                                                                    *
 * This library is free software; you can redistribute it and/or      *
 * modify it under the terms of the GNU Lesser General Public         *
 * License as published by the Free Software Foundation; either       *
 * version 2.1 of the License, or (at your option) any later version. *
 *                                                                    *
 * This library is distributed in the hope that it will be useful,    *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of     *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU  *
 * Lesser General Public License for more details.                    *
 *                                                                    *
 * You should have received a copy of the GNU Lesser General Public   *
 * License along with this library; if not, write to the Free         *
 * Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,    *
 * MA  02110-1301  USA                                                *
 *                                                                    *
 **********************************************************************/

###################### Description ######################

A monitoring software that communicates with Control System Studio (CSS) to be run at MX beamlines.
Uses CSS to take an image on a dewar rotation, crops the image, and predicts each cap location.

A daily directory is made for the first rotation on any given date. All images will then be placed
into this directory for ease of access. 

Prediction is done through a trained Convolutional Neural Network (CNN).
Categories: Tilted, Straight, Empty

Meant to prevent conditions dangerous to the automated robotic gripper.

Predictions are sorted by category and moved into respective directories.

###################### Requirements ######################

Python3 --> pip3 install -r requirements.txt

###################### How to run ######################

With Python3 run from puck_visualization folder with ./runPuckVis.py

Can do single image predictions using single_image_prediction.py

For data collection puck_view_snaps data_collect.py should be ran at all times.

###################### BIN ######################

Contains all files required for running the program

###################### PUCK_VIEW_SNAP ######################

Contains the file for data collection.

All Images obtained while running the data collection script are saved in the puck_view_snap
folder.

###################### SINGLE_IMAGE_PREDICTION ######################

Contains all files required for predicting a single image.

Image should be passed in as argument: python3 single_image_prediction.py /home/var/puck_C_fullPuck_silverCaps_96.4_emptying.jpg

###################### VAR ######################

Contains all images and training models.
Each model that is trained has a corresponding training graph located within the model directory.