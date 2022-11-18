# Modified from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user
ARG DEVCONTAINER_ROS_IMAGE_TAG=noetic
FROM ros:${DEVCONTAINER_ROS_IMAGE_TAG}

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \

    # [Optional] Source ROS when starting
    && echo 'source /opt/ros/${ROS_DISTRO}/setup.sh' >> /home/${USERNAME}/.bashrc \
    
    # Create workspace directory in which to clone repo
    && mkdir -p /home/${USERNAME}/infield_robotics_ws/src \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME} 

# Fix catkin issue in Noetic: https://answers.ros.org/question/353113/catkin-build-in-ubuntu-2004-noetic/?answer=353115#post-id-353115
RUN apt-get update \
    && apt-get install -y \
        python3-catkin-tools \ 
        python3-osrf-pycommon

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
